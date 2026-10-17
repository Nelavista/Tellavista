"""Roles and the audit log (05-domain-map.md: the `admin` module).

Roles are **data, not code**: adding `department_rep` or a company role later is
a seed row, never a branch in application logic. `is_staff` marks the roles that
may reach `apps/admin` at all; the per-action permission checks live in
`app/core/authz.py` (Phase 0 PR 0.10).

`AuditLog` is append-only by construction: it has no `updated_at`, and the
service that writes it only inserts. Sensitive actions (role changes, overrides,
payout approvals, data deletion) must be explainable afterwards, so each row
records the actor, the action, the target, an optional mandatory reason, and the
request id that ties it to logs.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

JSONPayload = JSON().with_variant(JSONB, "postgresql")

# The seeded roles (Phase 0 answer #10 / ADR-0009). `student` is the default for
# every new account; the rest are staff-facing. The last two are reserved now so
# departments and companies never need a schema change.
ROLE_STUDENT = "student"
ROLE_REVIEWER = "reviewer"
ROLE_OPS_ADMIN = "ops_admin"
ROLE_SUPER_ADMIN = "super_admin"
ROLE_DEPARTMENT_REP = "department_rep"
ROLE_COMPANY = "company"

SEED_ROLES: tuple[tuple[str, str, bool], ...] = (
    (ROLE_STUDENT, "Student", False),
    (ROLE_REVIEWER, "Quality reviewer", True),
    (ROLE_OPS_ADMIN, "Ops admin", True),
    (ROLE_SUPER_ADMIN, "Super admin", True),
    (ROLE_DEPARTMENT_REP, "Department representative", True),
    (ROLE_COMPANY, "Company contact", True),
)


class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    # Staff roles are the only ones eligible for admin surfaces and MFA.
    is_staff: Mapped[bool] = mapped_column(default=False, nullable=False)


class AuditLog(Base):
    """Append-only record of sensitive actions. Never updated, never deleted."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Null for system actions (jobs, imports, migrations).
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    # Snapshot of the role at the time: the audit row must not change meaning when
    # someone is promoted or demoted.
    actor_role_code: Mapped[str | None] = mapped_column(String(40))
    action: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    target_type: Mapped[str | None] = mapped_column(String(60))
    target_id: Mapped[str | None] = mapped_column(String(64))
    # Mandatory for overrides and any manual money/verification decision.
    reason: Mapped[str | None] = mapped_column(String(255))
    request_id: Mapped[str | None] = mapped_column(String(64))
    ip_hash: Mapped[str | None] = mapped_column(String(64))
    context: Mapped[dict | None] = mapped_column(JSONPayload)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
