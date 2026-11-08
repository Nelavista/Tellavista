"""Add provenance and descriptive metadata to courses.

Revision ID: 20261108_1300
Revises: 20261108_1200
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261108_1300"
down_revision: str | None = "20261108_1200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("courses", sa.Column("semester", sa.String(length=20), nullable=True))
    op.add_column("courses", sa.Column("course_type", sa.String(length=20), nullable=True))
    op.add_column("courses", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("courses", sa.Column("source", sa.String(length=30), nullable=True))


def downgrade() -> None:
    for column in ("source", "description", "course_type", "semester"):
        op.drop_column("courses", column)
