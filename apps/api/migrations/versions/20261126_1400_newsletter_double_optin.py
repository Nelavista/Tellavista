"""newsletter double opt-in

Revision ID: 20261126_1400
Revises: 20261123_1200
Create Date: 2026-11-26

Submitting an address now only starts the opt-in: a confirmation link is mailed
and the row stays pending until it is clicked. `confirm_token` holds that link's
token and `confirmed_at` is the state the send path checks, so a typo or someone
else's address cannot put them on the list without their own click.

Existing rows are backfilled as confirmed: every address already on the list was
added with an explicit opt-in before this release and has been receiving mail, so
requiring a new click from them would silently drop real subscribers. Only rows
that are currently active are backfilled; an unsubscribed address stays inactive
and is never mailed again.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "20261126_1400"
down_revision: str | None = "20261123_1200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "newsletter_subscribers", sa.Column("confirm_token", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "newsletter_subscribers", sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.create_index(
        "ix_newsletter_subscribers_confirm_token",
        "newsletter_subscribers",
        ["confirm_token"],
        unique=True,
    )

    # Skipped for `--sql`: there is no connection to read rows from, and the data
    # step is not part of the emitted DDL.
    if context.is_offline_mode():
        return
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "UPDATE newsletter_subscribers SET confirmed_at = created_at "
            "WHERE is_active = true AND confirmed_at IS NULL"
        )
    )


def downgrade() -> None:
    op.drop_index(
        "ix_newsletter_subscribers_confirm_token", table_name="newsletter_subscribers"
    )
    op.drop_column("newsletter_subscribers", "confirmed_at")
    op.drop_column("newsletter_subscribers", "confirm_token")
