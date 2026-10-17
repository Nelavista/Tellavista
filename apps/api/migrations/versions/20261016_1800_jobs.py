"""jobs: durable queue with retries

Revision ID: 20261016_1800
Revises: 20261016_1700
Create Date: 2026-10-16

Phase 0 PR 0.6. One new table. A job row is committed in the same transaction as
the work that needs it, so a verification email cannot be lost by a restart; the
worker claims due rows, retries with backoff and leaves exhausted rows `failed`.

`idempotency_key` is unique so a retried request cannot enqueue the same job twice.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261016_1800"
down_revision: str | None = "20261016_1700"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("payload", JSONPayload, nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="pending"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="5"),
        sa.Column(
            "run_after", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=80), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("idempotency_key", name="uq_jobs_idempotency_key"),
    )
    op.create_index("ix_jobs_name", "jobs", ["name"])
    op.create_index("ix_jobs_status_run_after", "jobs", ["status", "run_after"])


def downgrade() -> None:
    op.drop_index("ix_jobs_status_run_after", table_name="jobs")
    op.drop_index("ix_jobs_name", table_name="jobs")
    op.drop_table("jobs")
