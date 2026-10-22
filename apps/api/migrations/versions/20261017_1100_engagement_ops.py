"""engagement and ops: notifications, messages, import receipts, campus, waitlist

Revision ID: 20261017_1100
Revises: 20261017_1000
Create Date: 2026-10-17

Phases 1, 5 and 9. Five new tables, no alterations.

`import_runs` is the receipt for every V1 bridge import, including dry runs: counts
and checksums are kept so a reconciliation report can be compared against V1
without trusting a console log.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261017_1100"
down_revision: str | None = "20261017_1000"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")


def _timestamps() -> tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("body", sa.String(length=500), nullable=False),
        sa.Column("data", JSONPayload, nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("pushed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_notifications_kind", "notifications", ["kind"])

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "sender_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "recipient_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "assignment_id",
            sa.Integer(),
            sa.ForeignKey("assignments.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_messages_sender_user_id", "messages", ["sender_user_id"])
    op.create_index("ix_messages_recipient_user_id", "messages", ["recipient_user_id"])
    op.create_index("ix_messages_assignment_id", "messages", ["assignment_id"])

    op.create_table(
        "import_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=40), nullable=False),
        sa.Column("mode", sa.String(length=10), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="pending"),
        sa.Column(
            "started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("counts", JSONPayload, nullable=True),
        sa.Column("checksums", JSONPayload, nullable=True),
        sa.Column("errors", JSONPayload, nullable=True),
        sa.Column(
            "created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
    )
    op.create_index("ix_import_runs_source", "import_runs", ["source"])
    op.create_index("ix_import_runs_started_at", "import_runs", ["started_at"])

    op.create_table(
        "campus_info",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "university_id",
            sa.Integer(),
            sa.ForeignKey("universities.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=30), nullable=False, server_default="info"),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("latitude_micro", sa.Integer(), nullable=True),
        sa.Column("longitude_micro", sa.Integer(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_timestamps(),
    )
    op.create_index("ix_campus_info_university_id", "campus_info", ["university_id"])

    op.create_table(
        "university_waitlist",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("university_name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("user_id", "university_name", name="uq_waitlist_user_university"),
    )
    op.create_index(
        "ix_university_waitlist_university_name", "university_waitlist", ["university_name"]
    )
    op.create_index("ix_university_waitlist_user_id", "university_waitlist", ["user_id"])
    op.create_index(
        "ix_university_waitlist_created_at", "university_waitlist", ["created_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_university_waitlist_created_at", table_name="university_waitlist")
    op.drop_index("ix_university_waitlist_user_id", table_name="university_waitlist")
    op.drop_index("ix_university_waitlist_university_name", table_name="university_waitlist")
    op.drop_table("university_waitlist")

    op.drop_index("ix_campus_info_university_id", table_name="campus_info")
    op.drop_table("campus_info")

    op.drop_index("ix_import_runs_started_at", table_name="import_runs")
    op.drop_index("ix_import_runs_source", table_name="import_runs")
    op.drop_table("import_runs")

    op.drop_index("ix_messages_assignment_id", table_name="messages")
    op.drop_index("ix_messages_recipient_user_id", table_name="messages")
    op.drop_index("ix_messages_sender_user_id", table_name="messages")
    op.drop_table("messages")

    op.drop_index("ix_notifications_kind", table_name="notifications")
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")
