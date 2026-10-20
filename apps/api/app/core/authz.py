"""Role permissions (PRD §14, ADR-0009).

Roles are data (`roles` table), but the *capability* each role confers is code —
an explicit, reviewable matrix beats storing permissions in rows that can drift
from what the endpoints actually check.

Object-level authorisation is separate and stricter: a `student` may only ever
touch rows whose `user_id` is their own. `require_permission` gates the route;
`ensure_owner` gates the row.
"""
from __future__ import annotations

from collections.abc import Iterable

from fastapi import Depends, HTTPException, status

from app.core.errors import ApiError
from app.models.admin import (
    ROLE_COMPANY,
    ROLE_DEPARTMENT_REP,
    ROLE_OPS_ADMIN,
    ROLE_REVIEWER,
    ROLE_STUDENT,
    ROLE_SUPER_ADMIN,
)

PERMISSION_BY_ROLE: dict[str, frozenset[str]] = {
    ROLE_STUDENT: frozenset({"self.read", "self.write", "learning.read", "learning.write"}),
    ROLE_REVIEWER: frozenset(
        {"self.read", "self.write", "review.read", "review.write", "talent.read"}
    ),
    ROLE_OPS_ADMIN: frozenset(
        {
            "self.read",
            "self.write",
            "review.read",
            "review.write",
            "talent.read",
            "project.read",
            "project.write",
            "cohort.write",
            "ledger.read",
            "payout.request",
            "import.run",
            "audit.read",
            # Ops can read the policy it works under; only a super admin may
            # change currency, payout thresholds or the terms in force.
            "settings.read",
        }
    ),
    ROLE_SUPER_ADMIN: frozenset({"*"}),
    ROLE_DEPARTMENT_REP: frozenset({"self.read", "talent.read", "department.read"}),
    ROLE_COMPANY: frozenset({"self.read", "talent.read", "project.read"}),
}

STAFF_ROLES = frozenset({ROLE_REVIEWER, ROLE_OPS_ADMIN, ROLE_SUPER_ADMIN})


def has_permission(role_code: str | None, permission: str) -> bool:
    if not role_code:
        return False
    granted = PERMISSION_BY_ROLE.get(role_code, frozenset())
    return "*" in granted or permission in granted


def require_permission(*permissions: str):
    """FastAPI dependency factory. All listed permissions are required."""
    from app.api.deps import get_current_user  # local import: avoid a cycle

    def _guard(user=Depends(get_current_user)):
        role_code = user.role.code if user.role else None
        missing = [p for p in permissions if not has_permission(role_code, p)]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this action.",
            )
        return user

    return _guard


def ensure_owner(current_user, owner_id: int | None) -> None:
    """Object-level check: a student may only read or write their own rows."""
    role_code = current_user.role.code if current_user.role else None
    if owner_id is not None and current_user.id == owner_id:
        return
    if has_permission(role_code, "talent.read"):  # reviewer/ops/super may inspect
        return
    raise ApiError(403, "forbidden", "You do not have access to this record.")


def ensure_any_role(user, roles: Iterable[str]) -> None:
    role_code = user.role.code if user.role else None
    if role_code not in set(roles):
        raise ApiError(403, "forbidden", "You do not have access to this action.")
