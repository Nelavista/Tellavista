"""Phase 0 PR 0.1a — identity base tables and the rules they encode.

The schema is built from the models on an in-memory SQLite database, so these
need no service. They assert the invariants later PRs depend on: roles are seeded
data, one identity per email, one profile per user, deletion is soft, and the
audit log is append-only and survives the deletion of its actor.

The migration is exercised separately in `test_migrations.py` (it is what
actually creates these tables, and it must agree with the models).
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine, event, inspect, select
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.admin import ROLE_OPS_ADMIN, ROLE_STUDENT, SEED_ROLES, AuditLog, Role
from app.models.identity import User, UserProfile
from app.seed.roles import seed_roles

EXPECTED_TABLES = {
    "audit_logs",
    "courses",
    "departments",
    "faculties",
    "materials",
    "roles",
    "universities",
    "user_profiles",
    "users",
}


@pytest.fixture()
def db() -> Session:
    engine = create_engine("sqlite://")  # in-memory

    # SQLite ignores foreign keys unless asked: without this, ON DELETE CASCADE /
    # SET NULL look like they work and the tests prove nothing.
    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _record) -> None:  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_roles(session)
        yield session
        session.rollback()


def _user(db: Session, **overrides) -> User:
    student = db.scalar(select(Role).where(Role.code == ROLE_STUDENT))
    data = {
        "email": f"u{uuid.uuid4().hex[:8]}@example.test",
        "username": f"u{uuid.uuid4().hex[:8]}",
        "name": "Ada",
        "email_verified": True,
        "role_id": student.id if student else None,
    }
    data.update(overrides)
    user = User(**data)
    db.add(user)
    db.flush()
    return user


def test_expected_tables_exist(db: Session) -> None:
    assert EXPECTED_TABLES <= set(inspect(db.get_bind()).get_table_names())


def test_seed_roles_is_idempotent_and_authoritative(db: Session) -> None:
    assert {r.code for r in db.scalars(select(Role))} == {code for code, _, _ in SEED_ROLES}
    # Re-running must not duplicate or fail.
    assert seed_roles(db) == 0
    assert db.scalar(select(sa.func.count()).select_from(Role)) == len(SEED_ROLES)
    # Only staff roles may reach the admin app (enforced properly in PR 0.10).
    assert db.scalar(select(Role.is_staff).where(Role.code == ROLE_STUDENT)) is False
    assert db.scalar(select(Role.is_staff).where(Role.code == ROLE_OPS_ADMIN)) is True


def test_role_code_is_unique(db: Session) -> None:
    db.add(Role(code=ROLE_STUDENT, name="Duplicate", is_staff=False))
    with pytest.raises(IntegrityError):
        db.flush()


def test_user_email_and_username_are_unique(db: Session) -> None:
    first = _user(db)
    with pytest.raises(IntegrityError):
        _user(db, email=first.email)
    db.rollback()


def test_user_has_a_role_and_a_profile(db: Session) -> None:
    user = _user(db)
    db.add(UserProfile(user_id=user.id, display_name="Ada", preferred_path="skills"))
    db.flush()
    assert (
        db.scalar(select(UserProfile.preferred_path).where(UserProfile.user_id == user.id))
        == "skills"
    )
    assert user.role is not None and user.role.code == ROLE_STUDENT


def test_profile_is_one_to_one(db: Session) -> None:
    user = _user(db)
    db.add(UserProfile(user_id=user.id))
    db.flush()
    db.add(UserProfile(user_id=user.id))
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_deleting_a_user_removes_the_profile(db: Session) -> None:
    user = _user(db)
    db.add(UserProfile(user_id=user.id))
    db.flush()
    db.delete(user)
    db.flush()
    assert db.scalar(select(sa.func.count()).select_from(UserProfile)) == 0


def test_account_deletion_is_soft(db: Session) -> None:
    user = _user(db)
    assert user.is_deleted is False and user.deleted_at is None
    user.is_deleted = True
    user.deleted_at = datetime.now(UTC)
    db.flush()
    assert user.deleted_at is not None


def test_audit_log_is_append_only_by_shape(db: Session) -> None:
    columns = set(AuditLog.__table__.columns.keys())
    assert "updated_at" not in columns, "audit rows must never be updated"
    assert {
        "actor_user_id",
        "actor_role_code",
        "action",
        "target_type",
        "target_id",
        "reason",
        "request_id",
        "created_at",
    } <= columns

    user = _user(db)
    db.add(
        AuditLog(
            actor_user_id=user.id,
            actor_role_code=ROLE_OPS_ADMIN,
            action="verification.override",
            target_type="verification_record",
            target_id="42",
            reason="gold task mis-scored",
            context={"from": "unverified", "to": "verified"},
        )
    )
    db.flush()
    row = db.scalars(select(AuditLog)).one()
    assert row.reason == "gold task mis-scored" and row.context["to"] == "verified"


def test_audit_log_survives_actor_deletion(db: Session) -> None:
    """Deleting an account must not erase the record of what it did."""
    user = _user(db)
    db.add(AuditLog(actor_user_id=user.id, action="account.deleted", target_type="user"))
    db.flush()
    db.delete(user)
    db.flush()
    row = db.scalars(select(AuditLog)).one()
    assert row.actor_user_id is None  # ON DELETE SET NULL, not CASCADE


def test_json_columns_use_jsonb_on_postgres_and_json_elsewhere() -> None:
    """Audit context is JSONB on Postgres (indexable) and portable JSON in tests."""
    column = AuditLog.__table__.c.context
    assert isinstance(column.type.dialect_impl(postgresql.dialect()), JSONB)
    assert not isinstance(column.type.dialect_impl(sqlite.dialect()), JSONB)
