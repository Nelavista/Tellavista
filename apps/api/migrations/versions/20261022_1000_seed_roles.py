"""seed the six reference roles

Revision ID: 20261022_1000
Revises: 20261020_1000
Create Date: 2026-10-22

Roles are created with the schema in 20261016_1200 but were only *populated* by
the local seed and the tests. A fresh DEV/PROD database therefore had no
`student` row, so a signup got `role_id = NULL` and every permission check
failed. This revision makes the reference data part of the schema journey.

Idempotent: it inserts only the codes that are missing. Downgrade is deliberately
a no-op — deleting roles that `users.role_id` may reference would either violate
the foreign key or strip every account of its permissions. The rows are reference
data, not something a rollback should remove.
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "20261022_1000"
down_revision: str | None = "20261020_1000"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Kept identical to app.models.admin.SEED_ROLES. The migration must be
# self-contained (it cannot import application code), and the test suite compares
# the two lists so they cannot drift.
ROLES: tuple[tuple[str, str, bool], ...] = (
    ("student", "Student", False),
    ("reviewer", "Quality reviewer", True),
    ("ops_admin", "Ops admin", True),
    ("super_admin", "Super admin", True),
    ("department_rep", "Department representative", True),
    ("company", "Company contact", True),
)


def _sql_literal(value: str) -> str:
    """Quote a constant. The only inputs are the ROLES tuple above."""
    return "'" + value.replace("'", "''") + "'"


def upgrade() -> None:
    # Idempotent at the database level, so this also runs on a DEV database that
    # the local seed already populated. No SELECT: this must also work in
    # `alembic upgrade head --sql` (offline compile), where there is no connection.
    values = ", ".join(
        f"({_sql_literal(code)}, {_sql_literal(name)}, {'true' if is_staff else 'false'})"
        for code, name, is_staff in ROLES
    )
    dialect = op.get_context().dialect.name
    if dialect == "sqlite":
        op.execute(
            f"INSERT OR IGNORE INTO roles (code, name, is_staff) VALUES {values}"
        )
    else:
        op.execute(
            "INSERT INTO roles (code, name, is_staff) VALUES "
            f"{values} ON CONFLICT (code) DO NOTHING"
        )


def downgrade() -> None:
    # Reference data with live foreign keys: do not delete it on a rollback.
    pass
