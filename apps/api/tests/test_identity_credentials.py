"""Phase 0 PR 0.1b — credential and reliability tables.

These assert the shapes the auth and idempotency services (PR 0.5/0.8) will rely
on, not the services themselves: a bearer value is only ever stored as a hash, a
refresh token is single-use by construction, consent and audit evidence is
append-only, and an idempotency key can describe exactly one write.

They run on the shared `db` fixture from conftest.py (in-memory SQLite with
foreign keys enabled), so cascade/set-null behaviour is real.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import (
    REVOKE_REUSE_DETECTED,
    Consent,
    EmailToken,
    IdempotencyKey,
    RefreshToken,
    User,
)

EXPECTED_TABLES = {"refresh_tokens", "email_tokens", "consents", "idempotency_keys"}


def _user(db: Session) -> User:
    student = db.scalar(select(Role).where(Role.code == ROLE_STUDENT))
    user = User(
        email=f"u{uuid.uuid4().hex[:8]}@example.test",
        username=f"u{uuid.uuid4().hex[:8]}",
        role_id=student.id if student else None,
    )
    db.add(user)
    db.flush()
    return user


def _refresh(db: Session, user: User, family: str | None = None) -> RefreshToken:
    token = RefreshToken(
        user_id=user.id,
        family_id=family or str(uuid.uuid4()),
        token_hash=uuid.uuid4().hex + uuid.uuid4().hex,
        expires_at=datetime.now(UTC) + timedelta(days=30),
    )
    db.add(token)
    db.flush()
    return token


def test_tables_exist_and_store_only_hashes(db: Session) -> None:
    tables = set(inspect(db.get_bind()).get_table_names())
    assert EXPECTED_TABLES <= tables
    # The raw bearer value is never a column; only its hash is.
    for model in (RefreshToken, EmailToken):
        columns = set(model.__table__.columns.keys())
        assert "token_hash" in columns
        assert "token" not in columns and "plaintext" not in columns


def test_refresh_token_hash_is_unique(db: Session) -> None:
    user = _user(db)
    first = _refresh(db, user)
    duplicate = RefreshToken(
        user_id=user.id,
        family_id=first.family_id,
        token_hash=first.token_hash,
        expires_at=first.expires_at,
    )
    db.add(duplicate)
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_rotation_keeps_one_family_and_replaces_the_link(db: Session) -> None:
    user = _user(db)
    first = _refresh(db, user)
    assert first.platform == "web" and first.used_at is None and first.revoked_at is None

    first.used_at = datetime.now(UTC)
    replacement = _refresh(db, user, family=first.family_id)
    first.replaced_by_id = replacement.id
    db.flush()

    family = db.scalars(
        select(RefreshToken).where(RefreshToken.family_id == first.family_id)
    ).all()
    assert len(family) == 2
    assert first.used_at is not None and replacement.used_at is None


def test_reuse_revocation_is_recorded(db: Session) -> None:
    user = _user(db)
    token = _refresh(db, user)
    token.revoked_at = datetime.now(UTC)
    token.revoked_reason = REVOKE_REUSE_DETECTED
    db.flush()
    assert db.scalar(select(RefreshToken.revoked_reason)) == "reuse_detected"


def test_credentials_are_removed_with_the_account(db: Session) -> None:
    user = _user(db)
    _refresh(db, user)
    db.add(
        EmailToken(
            user_id=user.id,
            purpose="reset_password",
            token_hash=uuid.uuid4().hex * 2,
            expires_at=datetime.now(UTC) + timedelta(hours=1),
        )
    )
    db.flush()
    db.delete(user)
    db.flush()
    assert db.scalars(select(RefreshToken)).all() == []
    assert db.scalars(select(EmailToken)).all() == []


def test_email_token_hash_is_unique(db: Session) -> None:
    user = _user(db)
    email = EmailToken(
        user_id=user.id,
        purpose="verify_email",
        token_hash=uuid.uuid4().hex * 2,
        expires_at=datetime.now(UTC) + timedelta(hours=24),
    )
    db.add(email)
    db.flush()
    db.add(
        EmailToken(
            user_id=user.id,
            purpose="reset_password",
            token_hash=email.token_hash,
            expires_at=datetime.now(UTC) + timedelta(hours=1),
        )
    )
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_consent_is_append_only_evidence(db: Session) -> None:
    assert "updated_at" not in Consent.__table__.columns, "consent must never be edited"

    user = _user(db)
    for version, granted in (("1.0", True), ("2.0", False)):
        db.add(
            Consent(
                user_id=user.id,
                kind="terms_of_service",
                document_version=version,
                granted=granted,
            )
        )
    db.flush()
    history = db.scalars(
        select(Consent).where(Consent.user_id == user.id).order_by(Consent.id)
    ).all()
    assert [c.document_version for c in history] == ["1.0", "2.0"]

    # Evidence outlives the account, but stops identifying the person.
    # (expire_all: the ON DELETE SET NULL happens in the database, not the ORM.)
    db.delete(user)
    db.flush()
    db.expire_all()
    retained = db.scalars(select(Consent)).all()
    assert len(retained) == 2 and all(c.user_id is None for c in retained)


def test_idempotency_key_describes_one_write(db: Session) -> None:
    user = _user(db)
    key = str(uuid.uuid4())
    db.add(
        IdempotencyKey(
            key=key,
            user_id=user.id,
            method="POST",
            path="/v1/work/submissions",
            request_fingerprint=uuid.uuid4().hex * 2,
            expires_at=datetime.now(UTC) + timedelta(hours=24),
        )
    )
    db.flush()

    # In flight: the first attempt has not completed yet, so a replay must wait.
    row = db.scalars(select(IdempotencyKey)).one()
    assert row.completed_at is None and row.response_status is None

    row.completed_at = datetime.now(UTC)
    row.response_status = 201
    row.response_body = {"id": 7}
    db.flush()
    assert db.scalar(select(IdempotencyKey.response_body))["id"] == 7

    # The same key with a different body is a client bug, not a second write.
    other = _user(db)
    db.add(
        IdempotencyKey(
            key=key,
            user_id=other.id,
            method="POST",
            path="/v1/work/submissions",
            request_fingerprint=uuid.uuid4().hex * 2,
            expires_at=datetime.now(UTC) + timedelta(hours=24),
        )
    )
    with pytest.raises(IntegrityError):
        db.flush()
