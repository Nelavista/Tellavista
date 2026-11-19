"""announcements and newsletter subscribers

Revision ID: 20261113_1000
Revises: 20261108_1300
Create Date: 2026-11-13

The two tables the operations team works with directly:

* `announcements` -- one row per message, delivered in-product, by email, or both.
  Publishing stamps `published_at`; `email_sent_at`/`email_recipient_count` record
  what the send actually did so a re-run is visibly a re-run.
* `newsletter_subscribers` -- an address plus its consent state. The unique index
  on `email` is the reason re-subscribing is idempotent, and keeping unsubscribed
  rows is why an import cannot silently opt someone back in.

No existing table changes, so this is a safe online migration.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261113_1000"
down_revision: str | None = "20261108_1300"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "announcements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("audience", sa.String(length=16), nullable=False, server_default="all"),
        sa.Column("channel", sa.String(length=16), nullable=False, server_default="platform"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("email_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "email_recipient_count", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "newsletter_subscribers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=40), nullable=False, server_default="public"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("unsubscribed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_newsletter_subscribers_email", "newsletter_subscribers", ["email"], unique=True
    )
    op.create_index(
        "ix_newsletter_subscribers_user_id", "newsletter_subscribers", ["user_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_newsletter_subscribers_user_id", table_name="newsletter_subscribers")
    op.drop_index("ix_newsletter_subscribers_email", table_name="newsletter_subscribers")
    op.drop_table("newsletter_subscribers")
    op.drop_table("announcements")
