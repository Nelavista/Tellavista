"""two-factor columns and push device tokens

Revision ID: 20261018_0900
Revises: 20261017_1300
Create Date: 2026-10-18

Phase 0 security (F1/C8) and Phase 5 delivery (F4/D1).

* `users.totp_secret`/`totp_enabled_at`/`totp_recovery_hashes` are expand-only and
  nullable, so existing accounts keep working with 2FA off.
* `push_devices` stores one row per install. The token is unique: a phone that
  signs into a second account moves its token instead of duplicating delivery.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261018_0900"
down_revision: str | None = "20261017_1300"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")


def upgrade() -> None:
    op.add_column("users", sa.Column("totp_secret", sa.String(length=64), nullable=True))
    op.add_column(
        "users", sa.Column("totp_enabled_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("users", sa.Column("totp_recovery_hashes", JSONPayload, nullable=True))

    op.create_table(
        "push_devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("platform", sa.String(length=10), nullable=False, server_default="android"),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token", name="uq_push_devices_token"),
    )
    op.create_index("ix_push_devices_user_id", "push_devices", ["user_id"])
    op.create_index("ix_push_devices_token", "push_devices", ["token"])


def downgrade() -> None:
    op.drop_index("ix_push_devices_token", table_name="push_devices")
    op.drop_index("ix_push_devices_user_id", table_name="push_devices")
    op.drop_table("push_devices")
    op.drop_column("users", "totp_recovery_hashes")
    op.drop_column("users", "totp_enabled_at")
    op.drop_column("users", "totp_secret")
