"""Phase 0 PR 0.8 — identity service rules.

Written now, run with the rest of the suite in the verification pass. These are
the tests that decide whether the security boundary holds: single-use refresh
tokens with reuse detection, V1 hash upgrade, one-use email tokens, and deletion
that anonymises without erasing the audit trail.
"""
from __future__ import annotations

import hashlib
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.security import hash_token
from app.models.admin import ROLE_STUDENT, AuditLog, Role
from app.models.identity import Consent, RefreshToken, User
from app.models.jobs import Job
from app.services.identity import auth

PASSWORD = "correct horse battery"


def _signup(db: Session, *, accept_terms: bool = True):
    return auth.register(
        db,
        email=f"u{uuid.uuid4().hex[:8]}@example.test",
        username=f"u{uuid.uuid4().hex[:8]}",
        password=PASSWORD,
        accept_terms=accept_terms,
        platform="web",
    )


def test_register_creates_one_student_identity(db: Session) -> None:
    user, access, refresh, expires = _signup(db)

    assert user.role is not None and user.role.code == ROLE_STUDENT
    assert user.profile is not None
    assert user.email_verified is False
    assert db.scalar(select(Consent).where(Consent.user_id == user.id)).granted is True
    # The verification email is queued in the same transaction as the account.
    assert db.scalar(select(Job).where(Job.name == "send_email")) is not None
    assert access and refresh and expires


def test_duplicate_email_is_rejected(db: Session) -> None:
    user, *_ = _signup(db)
    with pytest.raises(ApiError) as excinfo:
        auth.register(
            db,
            email=user.email,
            username=f"u{uuid.uuid4().hex[:8]}",
            password=PASSWORD,
        )
    assert excinfo.value.status_code == 409
    assert excinfo.value.code == "email_taken"


def test_login_upgrades_a_v1_pbkdf2_hash(db: Session) -> None:
    salt = "abc123"
    iterations = 260000
    digest = hashlib.pbkdf2_hmac("sha256", b"v1-password", salt.encode(), iterations).hex()
    user = User(
        email=f"v1-{uuid.uuid4().hex[:8]}@example.test",
        username=f"v1-{uuid.uuid4().hex[:8]}",
        password_hash=f"pbkdf2:sha256:{iterations}${salt}${digest}",
        role_id=db.scalar(select(Role.id).where(Role.code == ROLE_STUDENT)),
    )
    db.add(user)
    db.flush()

    upgraded = auth.authenticate(db, email=user.email, password="v1-password")
    assert upgraded.password_hash is not None
    assert upgraded.password_hash.startswith("$argon2")
    # The second login uses the new hash and still works.
    assert auth.authenticate(db, email=user.email, password="v1-password").id == user.id


def test_unknown_email_and_wrong_password_are_indistinguishable(db: Session) -> None:
    user, *_ = _signup(db)
    with pytest.raises(ApiError) as wrong:
        auth.authenticate(db, email=user.email, password="not the password")
    with pytest.raises(ApiError) as unknown:
        auth.authenticate(db, email=f"nobody-{uuid.uuid4().hex[:6]}@example.test", password="x")
    assert wrong.value.code == unknown.value.code == "invalid_credentials"


def test_refresh_rotation_keeps_the_family_and_reuse_revokes_it(db: Session) -> None:
    _user, _access, refresh, _expires = _signup(db)

    _access2, new_refresh, _expires2 = auth.rotate(db, raw_token=refresh)
    assert new_refresh != refresh

    first = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(refresh)))
    assert first is not None
    assert first.used_at is not None and first.replaced_by_id is not None

    # Replaying the exchanged token is reuse: the whole family dies.
    with pytest.raises(ApiError) as excinfo:
        auth.rotate(db, raw_token=refresh)
    assert excinfo.value.code == "refresh_token_reused"

    family = db.scalars(
        select(RefreshToken).where(RefreshToken.family_id == first.family_id)
    ).all()
    assert len(family) == 2
    assert all(token.revoked_at is not None for token in family)

    with pytest.raises(ApiError):
        auth.rotate(db, raw_token=new_refresh)


def test_email_verification_token_is_single_use(db: Session, monkeypatch) -> None:
    fixed = "raw-verify-token-1234567890"
    monkeypatch.setattr(auth, "new_email_token", lambda: (fixed, hash_token(fixed)))

    user, *_ = _signup(db)
    verified = auth.verify_email(db, raw_token=fixed)
    assert verified.email_verified is True

    with pytest.raises(ApiError) as excinfo:
        auth.verify_email(db, raw_token=fixed)
    assert excinfo.value.code == "invalid_token"


def test_resend_verification_replaces_the_previous_link(db: Session, monkeypatch) -> None:
    issued = iter(["raw-signup-token-1234567890", "raw-resend-token-1234567890"])

    def next_token():
        raw = next(issued)
        return raw, hash_token(raw)

    monkeypatch.setattr(auth, "new_email_token", next_token)

    user, *_ = _signup(db)
    auth.resend_verification(db, user=user)

    # The first link stops working the moment a second one is sent.
    with pytest.raises(ApiError) as excinfo:
        auth.verify_email(db, raw_token="raw-signup-token-1234567890")
    assert excinfo.value.code == "invalid_token"

    assert auth.verify_email(db, raw_token="raw-resend-token-1234567890").email_verified is True
    jobs = db.scalars(select(Job).where(Job.name == "send_email")).all()
    assert len(jobs) == 2


def test_resend_verification_refuses_a_verified_account(db: Session, monkeypatch) -> None:
    fixed = "raw-verify-token-1234567890"
    monkeypatch.setattr(auth, "new_email_token", lambda: (fixed, hash_token(fixed)))

    user, *_ = _signup(db)
    auth.verify_email(db, raw_token=fixed)

    with pytest.raises(ApiError) as excinfo:
        auth.resend_verification(db, user=user)
    assert excinfo.value.status_code == 409
    assert excinfo.value.code == "already_verified"


def test_password_reset_changes_the_password_and_kills_sessions(db: Session, monkeypatch) -> None:
    fixed = "raw-reset-token-1234567890"
    user, _access, refresh, _expires = _signup(db)

    monkeypatch.setattr(auth, "new_email_token", lambda: (fixed, hash_token(fixed)))
    auth.request_password_reset(db, email=user.email)
    auth.reset_password(db, raw_token=fixed, new_password="a brand new password")

    token = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(refresh)))
    assert token.revoked_at is not None
    assert auth.authenticate(db, email=user.email, password="a brand new password").id == user.id

    with pytest.raises(ApiError):
        auth.reset_password(db, raw_token=fixed, new_password="another password 1")


def test_reset_request_is_silent_for_an_unknown_email(db: Session) -> None:
    # No exception, no account enumeration.
    auth.request_password_reset(db, email=f"ghost-{uuid.uuid4().hex[:6]}@example.test")


def test_delete_account_anonymises_and_keeps_the_audit_trail(db: Session) -> None:
    user, *_ = _signup(db)
    user_id = user.id
    auth.delete_account(db, user=user)
    db.expire_all()

    stored = db.get(User, user_id)
    assert stored is not None
    assert stored.is_deleted is True and stored.deleted_at is not None
    assert stored.email.endswith("@deleted.invalid")
    assert stored.password_hash is None and stored.google_sub is None

    audit = db.scalar(select(AuditLog).where(AuditLog.action == "account.deleted"))
    assert audit is not None and audit.target_id == str(user_id)
