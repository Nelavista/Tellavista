"""public impact metrics

Revision ID: 20261123_1200
Revises: 20261121_1200
Create Date: 2026-11-23

The marketing site's /impact page now reads live aggregates from the product
database. Ops needs a way to stop publishing a number while it is checked, so
the single platform settings row gains `impact_metrics_enabled`.

A boolean with a server default is safe on SQLite and Postgres, and every
existing settings row keeps publishing (the documented default) until someone
switches it off.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261123_1200"
down_revision: str | None = "20261121_1200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("platform_settings") as batch:
        batch.add_column(
            sa.Column(
                "impact_metrics_enabled",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("platform_settings") as batch:
        batch.drop_column("impact_metrics_enabled")
