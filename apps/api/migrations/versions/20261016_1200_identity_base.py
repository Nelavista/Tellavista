"""identity base: roles, user role, profiles, audit log

Revision ID: 20261016_1200
Revises: 20261016_0000
Create Date: 2026-10-16

Phase 0 PR 0.1a. Expand-only: the existing `users` columns are untouched (the
free-string university/department/level columns stay until M1 adds the academia
foreign keys and backfills them). The credential tables — refresh/email tokens,
consent, idempotency — are PR 0.1b, and quality/ledger tables wait for M5/M6.

Two things this revision fixes on purpose:
* `created_at`/`updated_at` on the skeleton tables were created nullable while
  the models (TimestampMixin) declare them NOT NULL. Both carry
  server_default=now(), so tightening cannot fail on an existing row.
* the `users` alteration runs before the child tables exist, so the table
  recreation SQLite needs (it cannot ADD CONSTRAINT in place) has no dependants.
  On Postgres the batch context emits plain ALTERs.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261016_1200"
down_revision: str | None = "20261016_0000"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")

TIMESTAMP_COLUMNS = ("created_at", "updated_at")
# Leaf tables first: SQLite's batch mode recreates a table, and recreating a
# parent before its children is the riskier order. Reversed for the downgrade.
SKELETON_TABLES_LEAF_FIRST = ("materials", "courses", "departments", "faculties", "universities")
SKELETON_TABLES_PARENT_FIRST = tuple(reversed(SKELETON_TABLES_LEAF_FIRST))


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=40), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_staff", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("code", name="uq_roles_code"),
    )
    op.create_index("ix_roles_code", "roles", ["code"])

    # --- users: role + soft-deletion timestamp, and NOT NULL timestamps ---
    with op.batch_alter_table("users") as batch:
        batch.add_column(sa.Column("role_id", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
        batch.create_foreign_key(
            "fk_users_role_id_roles", "roles", ["role_id"], ["id"], ondelete="SET NULL"
        )
        batch.create_index("ix_users_role_id", ["role_id"])
        for column in TIMESTAMP_COLUMNS:
            batch.alter_column(column, existing_type=sa.DateTime(timezone=True), nullable=False)

    for table in SKELETON_TABLES_LEAF_FIRST:
        with op.batch_alter_table(table) as batch:
            for column in TIMESTAMP_COLUMNS:
                batch.alter_column(column, existing_type=sa.DateTime(timezone=True), nullable=False)

    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("display_name", sa.String(length=150), nullable=True),
        sa.Column("avatar_url", sa.String(length=1024), nullable=True),
        sa.Column("bio", sa.String(length=500), nullable=True),
        sa.Column("locale", sa.String(length=10), nullable=False, server_default="en"),
        sa.Column("timezone", sa.String(length=64), nullable=True),
        sa.Column("preferred_path", sa.String(length=16), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("onboarding_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notify_email", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("notify_push", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "profile_visibility", sa.String(length=16), nullable=False, server_default="private"
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "actor_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("actor_role_code", sa.String(length=40), nullable=True),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("target_type", sa.String(length=60), nullable=True),
        sa.Column("target_id", sa.String(length=64), nullable=True),
        sa.Column("reason", sa.String(length=255), nullable=True),
        sa.Column("request_id", sa.String(length=64), nullable=True),
        sa.Column("ip_hash", sa.String(length=64), nullable=True),
        sa.Column("context", JSONPayload, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_audit_logs_created_at", table_name="audit_logs")
    op.drop_index("ix_audit_logs_action", table_name="audit_logs")
    op.drop_index("ix_audit_logs_actor_user_id", table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_table("user_profiles")

    for table in SKELETON_TABLES_PARENT_FIRST:
        with op.batch_alter_table(table) as batch:
            for column in TIMESTAMP_COLUMNS:
                batch.alter_column(column, existing_type=sa.DateTime(timezone=True), nullable=True)

    with op.batch_alter_table("users") as batch:
        batch.drop_index("ix_users_role_id")
        batch.drop_constraint("fk_users_role_id_roles", type_="foreignkey")
        batch.drop_column("deleted_at")
        batch.drop_column("role_id")

    op.drop_index("ix_roles_code", table_name="roles")
    op.drop_table("roles")
