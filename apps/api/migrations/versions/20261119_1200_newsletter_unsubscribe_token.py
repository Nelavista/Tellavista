"""newsletter unsubscribe tokens

Revision ID: 20261119_1200
Revises: 20261113_1000
Create Date: 2026-11-19

Every newsletter email now carries a one-click unsubscribe link. The link holds an
opaque per-subscriber token rather than the address, because an address in a URL
would let anyone unsubscribe anyone else by guessing it, and because possession of
the token is the only thing the public endpoint should need to authorise.

Existing rows are backfilled with their own token here: a subscriber who has
already received an issue must be able to leave from the next one, not only from
issues sent after this release. The column stays nullable so a row can exist
without a token (a manual insert), and unique so two subscribers can never share
one unsubscribe link.

Safe on SQLite and Postgres: one column add plus one index, no table rewrite.
"""
from __future__ import annotations

import secrets
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "20261119_1200"
down_revision: str | None = "20261113_1000"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "newsletter_subscribers", sa.Column("unsubscribe_token", sa.String(length=64), nullable=True)
    )
    op.create_index(
        "ix_newsletter_subscribers_unsubscribe_token",
        "newsletter_subscribers",
        ["unsubscribe_token"],
        unique=True,
    )

    # Backfill: one token per existing address, so people already on the list can
    # leave from the next issue. Issued per row rather than derived from the
    # address, so the token cannot be recomputed by anyone who knows an email.
    #
    # Skipped when Alembic is only emitting static SQL (`--sql`): there is no
    # connection to read rows from, and the data step is not part of the DDL.
    if context.is_offline_mode():
        return
    conn = op.get_bind()
    ids = [row[0] for row in conn.execute(sa.text("SELECT id FROM newsletter_subscribers"))]
    for subscriber_id in ids:
        conn.execute(
            sa.text(
                "UPDATE newsletter_subscribers SET unsubscribe_token = :token WHERE id = :id"
            ),
            {"token": secrets.token_urlsafe(32), "id": subscriber_id},
        )


def downgrade() -> None:
    op.drop_index(
        "ix_newsletter_subscribers_unsubscribe_token",
        table_name="newsletter_subscribers",
    )
    op.drop_column("newsletter_subscribers", "unsubscribe_token")
