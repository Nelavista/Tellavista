"""Phase 0 security and delivery: 2FA, absolute email links, push, scheduling.

These run with the suite. The rules under test are the ones that fail *silently*
in production if they drift: a password-only staff login, a relative link in an
inbox, a push sent to a phone that signed out, or a daily job that never runs.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from factories import make_ops, make_user, unique
from sqlalchemy import select

from app.core import ratelimit
from app.core.errors import ApiError
from app.core.security import create_access_token, hash_token
from app.models.engagement import PushDevice
from app.models.identity import User
from app.models.jobs import DONE, Job
from app.services.identity import auth, twofa
from app.worker.scheduler import enqueue_scheduled

# RFC 6238's SHA-1 secret, base32-encoded, for the published test vectors.
RFC_SECRET = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"


def test_totp_matches_the_rfc_vector() -> None:
    at = datetime(1970, 1, 1, 0, 0, 59, tzinfo=UTC)
    # The RFC publishes 94287082 for 8 digits; six digits are its last six.
    assert twofa.code_at(RFC_SECRET, at) == "287082"


def test_totp_accepts_one_step_of_clock_skew_only() -> None:
    now = datetime(2026, 10, 18, 12, 0, 0, tzinfo=UTC)
    code = twofa.code_at(RFC_SECRET, now)
    assert twofa.verify_code(RFC_SECRET, code, now)
    assert twofa.verify_code(RFC_SECRET, code, now + timedelta(seconds=30))
    assert not twofa.verify_code(RFC_SECRET, code, now + timedelta(seconds=120))


def test_enrolment_is_pending_until_confirmed(db) -> None:
    user = make_ops(db)

    secret, uri = twofa.begin_enrollment(db, user)
    assert uri.startswith("otpauth://totp/")
    assert secret in uri
    assert not twofa.is_enabled(user)

    codes = twofa.confirm_enrollment(db, user, twofa.code_at(secret))
    assert twofa.is_enabled(user)
    assert len(codes) == twofa.RECOVERY_CODE_COUNT
    assert all(len(code.replace("-", "")) == 10 for code in codes)
    # Only hashes are stored.
    assert all(hash_token(code.replace("-", "")) in user.totp_recovery_hashes for code in codes)


def test_recovery_codes_work_once(db) -> None:
    user = make_ops(db)
    secret, _uri = twofa.begin_enrollment(db, user)
    codes = twofa.confirm_enrollment(db, user, twofa.code_at(secret))

    assert twofa.verify_login_code(db, user, codes[0])
    assert not twofa.verify_login_code(db, user, codes[0])
    assert twofa.verify_login_code(db, user, codes[1])


def test_disable_needs_a_current_code(db) -> None:
    user = make_ops(db)
    secret, _uri = twofa.begin_enrollment(db, user)
    twofa.confirm_enrollment(db, user, twofa.code_at(secret))

    with pytest.raises(ApiError) as excinfo:
        twofa.disable(db, user, "000000")
    assert excinfo.value.code == "invalid_two_factor_code"
    assert twofa.is_enabled(user)

    twofa.disable(db, user, twofa.code_at(secret))
    assert not twofa.is_enabled(user)


def test_a_staff_login_with_two_factor_is_not_a_session(api) -> None:
    client, db = api
    staff = make_ops(db, password_hash=auth.hash_password("staff-password-1"))
    secret, _uri = twofa.begin_enrollment(db, staff)
    twofa.confirm_enrollment(db, staff, twofa.code_at(secret))
    db.commit()

    response = client.post(
        "/v1/auth/login",
        json={"email": staff.email, "password": "staff-password-1", "platform": "admin"},
    )
    assert response.status_code == 403
    body = response.json()["error"]
    assert body["code"] == "mfa_required"
    challenge = body["details"]["mfa_token"]

    ok = client.post(
        "/v1/auth/2fa/verify",
        json={"mfa_token": challenge, "code": twofa.code_at(secret)},
    )
    assert ok.status_code == 200
    assert ok.json()["access_token"]


def test_an_access_token_cannot_be_used_as_an_mfa_challenge(api) -> None:
    client, db = api
    user = make_user(db)
    access = create_access_token(user.id, user.role.code if user.role else None)

    response = client.post(
        "/v1/auth/2fa/verify", json={"mfa_token": access, "code": "123456"}
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_mfa_token"


def test_verification_email_contains_an_absolute_web_link(db, monkeypatch) -> None:
    raw = "raw-verify-token-1234567890"
    monkeypatch.setattr(auth, "new_email_token", lambda: (raw, hash_token(raw)))

    auth.register(
        db,
        email=f"mail-{unique('x')}@example.test",
        username=unique("mail"),
        password="correct horse battery",
    )
    job = db.scalar(select(Job).where(Job.name == "send_email"))
    assert job is not None
    body = job.payload["body"]
    assert "http://localhost:5173/auth/verify?token=" in body
    assert not body.strip().endswith(f": /auth/verify?token={raw}")


def test_registering_a_push_token_moves_it_to_the_new_owner(api) -> None:
    client, db = api
    first = make_user(db)
    second = make_user(db)
    token = unique("ExponentPushToken")

    def headers(user: User) -> dict:
        return {"Authorization": f"Bearer {create_access_token(user.id, None)}"}

    created = client.post(
        "/v1/me/push-devices", headers=headers(first), json={"token": token, "platform": "ios"}
    )
    assert created.status_code == 201

    moved = client.post(
        "/v1/me/push-devices", headers=headers(second), json={"token": token, "platform": "ios"}
    )
    assert moved.status_code == 201
    assert moved.json()["id"] == created.json()["id"]
    assert db.scalar(select(PushDevice.user_id).where(PushDevice.token == token)) == second.id


def test_the_scheduler_enqueues_one_reconciliation_per_day(db) -> None:
    day = datetime(2026, 10, 18, tzinfo=UTC).date()
    assert enqueue_scheduled(db, today=day) == 1
    assert enqueue_scheduled(db, today=day) == 0

    jobs = db.scalars(select(Job).where(Job.name == "reconcile_daily")).all()
    assert len(jobs) == 1
    assert jobs[0].idempotency_key == f"reconcile:{day.isoformat()}"

    # The next day is a new key, so the run is not lost.
    assert enqueue_scheduled(db, today=day + timedelta(days=1)) == 1


def test_rate_limit_reports_when_to_retry() -> None:
    ratelimit.reset()
    for _ in range(3):
        ratelimit.check("scope:test", limit=3, window_seconds=60)
    with pytest.raises(ApiError) as excinfo:
        ratelimit.check("scope:test", limit=3, window_seconds=60)
    assert excinfo.value.status_code == 429
    assert excinfo.value.details["retry_after_seconds"] >= 1
    ratelimit.reset()


def test_a_finished_job_stays_done(api) -> None:
    """The scheduler must not re-enqueue a run that already finished."""
    _client, db = api
    day = datetime(2026, 10, 18, tzinfo=UTC).date()
    job = db.scalar(select(Job).where(Job.idempotency_key == f"reconcile:{day.isoformat()}"))
    assert job is None
    enqueue_scheduled(db, today=day)
    job = db.scalar(select(Job).where(Job.idempotency_key == f"reconcile:{day.isoformat()}"))
    assert job is not None
    job.status = DONE
    db.commit()
    assert enqueue_scheduled(db, today=day) == 0
