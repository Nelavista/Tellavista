"""submissions: gold-task marker and expected answer

Revision ID: 20261017_1300
Revises: 20261017_1200
Create Date: 2026-10-17

Phase 5. Two expand-only, nullable/defaulted columns.

A gold task is live work with a known correct answer, mixed in at a configurable
rate. `gold_expected` is server-only: no student response includes it.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261017_1300"
down_revision: str | None = "20261017_1200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")


def upgrade() -> None:
    op.add_column(
        "submissions",
        sa.Column("is_gold", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("submissions", sa.Column("gold_expected", JSONPayload, nullable=True))


def downgrade() -> None:
    op.drop_column("submissions", "gold_expected")
    op.drop_column("submissions", "is_gold")
