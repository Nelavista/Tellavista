"""Language profile: dialect and self-reported capabilities.

The verified side of the profile is derived from verification records, so this
migration only adds the student-reported columns. Nothing here grants proof.

Revision ID: 20261108_1200
Revises: 20261104_2100
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")

revision: str = "20261108_1200"
down_revision: str | None = "20261104_2100"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("user_languages", sa.Column("dialect", sa.String(length=60), nullable=True))
    for column in (
        "can_speak",
        "can_read",
        "can_write",
        "can_transcribe",
        "can_translate",
    ):
        op.add_column(
            "user_languages",
            sa.Column(column, sa.Boolean(), nullable=False, server_default=sa.false()),
        )
    # Practice scores are persisted now that scoring is deterministic.
    op.add_column("practice_attempts", sa.Column("score", sa.Integer(), nullable=True))
    op.add_column("practice_attempts", sa.Column("result", JSONPayload, nullable=True))


def downgrade() -> None:
    op.drop_column("practice_attempts", "result")
    op.drop_column("practice_attempts", "score")
    for column in (
        "can_translate",
        "can_transcribe",
        "can_write",
        "can_read",
        "can_speak",
        "dialect",
    ):
        op.drop_column("user_languages", column)
