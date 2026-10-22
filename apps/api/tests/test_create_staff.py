"""The guarded staff-promotion helper (tools/create_staff.py)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tools.create_staff import promote_user  # noqa: E402

from app.models.admin import AuditLog, Role  # noqa: E402
from app.models.identity import User  # noqa: E402


def _user(db: Session, email: str = "staff@example.test") -> User:
    user = User(email=email, username=email.split("@")[0], name="Staff")
    db.add(user)
    db.commit()
    return user


def test_promote_sets_role_verifies_email_and_audits_once(db: Session) -> None:
    user = _user(db)

    promoted, role, changed = promote_user(db, email="STAFF@example.test", role_code="ops_admin")

    assert changed is True
    assert promoted.id == user.id
    assert promoted.role_id == role.id
    assert promoted.email_verified is True
    logs = db.scalars(select(AuditLog).where(AuditLog.action == "staff.role_granted")).all()
    assert len(logs) == 1
    assert logs[0].target_id == str(user.id)
    assert logs[0].context == {
        "email": "staff@example.test",
        "role": "ops_admin",
        "source": "cli",
    }

    # Idempotent: no second audit row, no error.
    again, same_role, changed_again = promote_user(
        db, email="staff@example.test", role_code="ops_admin"
    )
    assert again.id == user.id and same_role.id == role.id
    assert changed_again is False
    assert (
        db.scalar(
            select(func.count()).select_from(AuditLog).where(AuditLog.action == "staff.role_granted")
        )
        == 1
    )


def test_unknown_email_tells_the_operator_to_sign_up_first(db: Session) -> None:
    with pytest.raises(LookupError, match="Sign up"):
        promote_user(db, email="missing@example.test", role_code="ops_admin")


def test_student_role_is_not_a_staff_role(db: Session) -> None:
    _user(db)
    with pytest.raises(ValueError, match="not a staff role"):
        promote_user(db, email="staff@example.test", role_code="student")


def test_unknown_role_is_reported_with_the_known_ones(db: Session) -> None:
    _user(db)
    with pytest.raises(LookupError, match="super_admin"):
        promote_user(db, email="staff@example.test", role_code="does_not_exist")


def test_role_rows_are_the_expected_staff_set(db: Session) -> None:
    staff = set(db.scalars(select(Role.code).where(Role.is_staff.is_(True))))
    assert {"reviewer", "ops_admin", "super_admin", "department_rep", "company"} <= staff
    assert "student" not in staff
