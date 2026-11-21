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


def test_the_complete_first_login_enrolment_flow(api) -> None:
    """The browser flow, end to end, at the API boundary.

    A brand-new staff account has no second factor. The first sign-in therefore
    succeeds with a password alone -- the admin shell is what refuses to render
    anything until enrolment finishes -- and the flow the shell then drives is:

        login -> /me (mfa_enabled false) -> /2fa -> /2fa/setup -> /2fa/enable

    After enrolment the same account must not get a session from a password
    again: the next login is a challenge and only asking for the code finishes
    it. This is the sequence that used to be covered in pieces (service-level
    enrolment, one challenge) but never as one first-login path.
    """
    client, db = api
    staff = make_ops(db, password_hash=auth.hash_password("first-login-pass"))
    db.commit()

    # 1. First sign-in: allowed, because there is no factor to present yet.
    first = client.post(
        "/v1/auth/login",
        json={"email": staff.email, "password": "first-login-pass", "platform": "admin"},
    )
    assert first.status_code == 200, first.text
    access = first.json()["access_token"]
    headers = {"Authorization": f"Bearer {access}"}

    # 2. The shell's own gate checks these two reads before rendering anything.
    me = client.get("/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["mfa_enabled"] is False

    status = client.get("/v1/auth/2fa", headers=headers)
    assert status.status_code == 200
    assert status.json()["enabled"] is False
    assert status.json()["is_staff"] is True

    # 3. Setup mints a pending secret; it does not change login until enabled.
    setup = client.post("/v1/auth/2fa/setup", headers=headers)
    assert setup.status_code == 200
    secret = setup.json()["secret"]
    assert setup.json()["otpauth_uri"].startswith("otpauth://totp/")
    assert twofa.is_enabled(db.get(User, staff.id)) is False

    # 4. The code from the authenticator confirms it, and recovery codes come back once.
    enabled = client.post(
        "/v1/auth/2fa/enable",
        json={"code": twofa.code_at(secret)},
        headers=headers,
    )
    assert enabled.status_code == 200, enabled.text
    assert enabled.json()["enabled"] is True
    codes = enabled.json()["recovery_codes"]
    assert len(codes) == twofa.RECOVERY_CODE_COUNT

    # 5. The session that enrolled the factor keeps working: finishing setup must
    #    not sign the operator out of the screen they are standing on.
    assert client.get("/v1/auth/me", headers=headers).json()["mfa_enabled"] is True

    # 6. From now on a password alone is not a session.
    second = client.post(
        "/v1/auth/login",
        json={"email": staff.email, "password": "first-login-pass", "platform": "admin"},
    )
    assert second.status_code == 403
    assert second.json()["error"]["code"] == "mfa_required"

    # 7. The challenge plus a current code finishes the sign-in.
    challenge = second.json()["error"]["details"]["mfa_token"]
    verified = client.post(
        "/v1/auth/2fa/verify",
        json={"mfa_token": challenge, "code": twofa.code_at(secret)},
    )
    assert verified.status_code == 200
    assert verified.json()["access_token"]


def test_a_recovery_code_also_finishes_a_first_login(api) -> None:
    """The lost-phone path, through the same login endpoint: a recovery code is a
    second factor and must produce a session rather than a 403."""
    client, db = api
    staff = make_ops(db, password_hash=auth.hash_password("recovery-pass"))
    secret, _uri = twofa.begin_enrollment(db, staff)
    codes = twofa.confirm_enrollment(db, staff, twofa.code_at(secret))
    db.commit()

    first = client.post(
        "/v1/auth/login",
        json={"email": staff.email, "password": "recovery-pass", "platform": "admin"},
    )
    challenge = first.json()["error"]["details"]["mfa_token"]

    ok = client.post(
        "/v1/auth/2fa/verify", json={"mfa_token": challenge, "code": codes[0]}
    )
    assert ok.status_code == 200
    assert ok.json()["access_token"]

    # It is single-use, so the same code cannot finish a second sign-in.
    again = client.post(
        "/v1/auth/login",
        json={"email": staff.email, "password": "recovery-pass", "platform": "admin"},
    )
    reused = client.post(
        "/v1/auth/2fa/verify",
        json={"mfa_token": again.json()["error"]["details"]["mfa_token"], "code": codes[0]},
    )
    # 400, not 401: the challenge is valid, the code is not -- and either way no
    # session is issued.
    assert reused.status_code == 400
    assert "access_token" not in reused.json()


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


def test_a_web_device_keeps_the_subscription_needed_to_deliver(api) -> None:
    client, db = api
    user = make_user(db)
    endpoint = f"https://push.example.test/{unique('sub')}"
    headers = {"Authorization": f"Bearer {create_access_token(user.id, None)}"}

    created = client.post(
        "/v1/me/push-devices",
        headers=headers,
        json={
            "token": endpoint,
            "platform": "web",
            "subscription": {"endpoint": endpoint, "p256dh": "p256dh-key", "auth": "auth-key"},
        },
    )
    assert created.status_code == 201
    row = db.scalar(select(PushDevice).where(PushDevice.token == endpoint))
    assert row is not None
    assert row.subscription == {"endpoint": endpoint, "p256dh": "p256dh-key", "auth": "auth-key"}

    # Re-subscribing with rotated keys must replace them: keeping the old ones
    # means every later delivery fails to encrypt.
    again = client.post(
        "/v1/me/push-devices",
        headers=headers,
        json={
            "token": endpoint,
            "platform": "web",
            "subscription": {
                "endpoint": endpoint,
                "p256dh": "rotated-p256dh",
                "auth": "rotated-auth",
            },
        },
    )
    assert again.status_code == 201
    assert again.json()["id"] == created.json()["id"]
    db.refresh(row)
    assert row.subscription["p256dh"] == "rotated-p256dh"


def test_a_web_device_without_a_matching_subscription_is_rejected(api) -> None:
    client, db = api
    user = make_user(db)
    headers = {"Authorization": f"Bearer {create_access_token(user.id, None)}"}
    endpoint = f"https://push.example.test/{unique('sub')}"

    missing = client.post(
        "/v1/me/push-devices", headers=headers, json={"token": endpoint, "platform": "web"}
    )
    assert missing.status_code == 400
    assert missing.json()["error"]["code"] == "subscription_required"

    mismatch = client.post(
        "/v1/me/push-devices",
        headers=headers,
        json={
            "token": endpoint,
            "platform": "web",
            "subscription": {
                "endpoint": "https://push.example.test/somewhere-else",
                "p256dh": "p256dh-key",
                "auth": "auth-key",
            },
        },
    )
    assert mismatch.status_code == 400
    assert mismatch.json()["error"]["code"] == "subscription_mismatch"


def test_web_push_signs_each_browser_and_revokes_a_gone_endpoint(monkeypatch) -> None:
    import json

    import pywebpush

    from app.core.config import get_settings
    from app.worker import tasks

    settings = get_settings()
    monkeypatch.setattr(settings, "VAPID_PRIVATE_KEY", "test-private-key")
    monkeypatch.setattr(settings, "VAPID_SUBJECT", "mailto:test@example.test")

    subscriptions = [
        (1, {"endpoint": "https://push.example.test/live", "p256dh": "k1", "auth": "a1"}),
        (2, {"endpoint": "https://push.example.test/gone", "p256dh": "k2", "auth": "a2"}),
    ]
    monkeypatch.setattr(tasks, "_web_subscriptions", lambda user_id: subscriptions)

    sent: list[dict] = []

    class GoneResponse:
        status_code = 410

    def fake_webpush(**kwargs) -> None:
        sent.append(kwargs)
        if kwargs["subscription_info"]["endpoint"].endswith("/gone"):
            raise pywebpush.WebPushException("subscription is gone", response=GoneResponse())

    monkeypatch.setattr(pywebpush, "webpush", fake_webpush)
    revoked: list[tuple[int, str]] = []
    monkeypatch.setattr(
        tasks, "_revoke_push_device", lambda device_id, reason: revoked.append((device_id, reason))
    )

    tasks._send_web_push(
        {"user_id": 7, "notification_id": 3, "title": "New work", "body": "A task needs you"},
        settings,
    )

    assert [row["subscription_info"]["endpoint"] for row in sent] == [
        "https://push.example.test/live",
        "https://push.example.test/gone",
    ]
    assert sent[0]["subscription_info"]["keys"] == {"p256dh": "k1", "auth": "a1"}
    assert sent[0]["vapid_claims"] == {"sub": "mailto:test@example.test"}
    payload = json.loads(sent[0]["data"])
    assert payload["title"] == "New work"
    assert payload["notification_id"] == 3
    # Only the dead endpoint is revoked; the live one keeps receiving.
    assert revoked == [(2, "web_push_410")]


def test_web_push_is_skipped_without_vapid_keys(monkeypatch) -> None:
    from app.core.config import get_settings
    from app.worker import tasks

    settings = get_settings()
    monkeypatch.setattr(settings, "VAPID_PRIVATE_KEY", "")
    # If it tried to read devices or deliver, this would raise.
    monkeypatch.setattr(
        tasks, "_web_subscriptions", lambda user_id: pytest.fail("must not look up devices")
    )
    tasks._send_web_push({"user_id": 7, "title": "x", "body": "y"}, settings)


def test_the_public_config_carries_the_web_push_key_only(monkeypatch, db) -> None:
    from app.core.config import get_settings
    from app.services.platform import settings as policy

    monkeypatch.setattr(get_settings(), "VAPID_PUBLIC_KEY", "public-test-key")
    row = policy.get_platform_settings(db)
    body = policy.public_config(row)
    assert body["push_public_key"] == "public-test-key"
    assert "private" not in " ".join(str(value) for value in body.values()).lower()


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
