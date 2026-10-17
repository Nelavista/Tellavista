"""talent, languages, availability, practice, practical tasks and Ask Nelavista

Revision ID: 20261017_1200
Revises: 20261017_1100
Create Date: 2026-10-17

Phases 1–8. Eight new tables and five expand-only alterations.

The alterations are deliberately nullable: an existing row keeps working while a
backfill catches up. `question_attempts.client_key` is unique so an answer queued
offline can be retried without creating a second attempt; it is nullable because
server-created attempts have no client key.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261017_1200"
down_revision: str | None = "20261017_1100"
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
    # --- expand-only changes to existing tables -----------------------------
    op.add_column("user_profiles", sa.Column("location", sa.String(length=120), nullable=True))
    # Batch mode for the alterations that carry a constraint: SQLite cannot ALTER
    # a constraint in place, and the migration test runs the real DDL on SQLite.
    with op.batch_alter_table("learning_path_steps") as batch:
        batch.add_column(
            sa.Column(
                "task_template_id",
                sa.Integer(),
                sa.ForeignKey(
                    "task_templates.id",
                    ondelete="SET NULL",
                    name="fk_learning_path_steps_task_template_id",
                ),
                nullable=True,
            )
        )
    op.add_column(
        "assessment_attempts", sa.Column("presented_task_ids", JSONPayload, nullable=True)
    )
    op.add_column("assessment_attempts", sa.Column("answers", JSONPayload, nullable=True))
    with op.batch_alter_table("question_attempts") as batch:
        batch.add_column(sa.Column("client_key", sa.String(length=64), nullable=True))
        batch.create_unique_constraint("uq_question_attempts_client_key", ["client_key"])

    # --- new tables ---------------------------------------------------------
    op.create_table(
        "user_languages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("language", sa.String(length=60), nullable=False),
        sa.Column("level", sa.String(length=20), nullable=False, server_default="fluent"),
        *_timestamps(),
        sa.UniqueConstraint("user_id", "language", name="uq_user_language"),
    )
    op.create_index("ix_user_languages_user_id", "user_languages", ["user_id"])

    op.create_table(
        "user_availability",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("hours_per_week", sa.Integer(), nullable=True),
        sa.Column("available_from", sa.Date(), nullable=True),
        sa.Column("note", sa.String(length=255), nullable=True),
        *_timestamps(),
    )

    op.create_table(
        "talent_shares",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("token_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("label", sa.String(length=120), nullable=True),
        sa.Column("scopes", JSONPayload, nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_viewed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_talent_shares_user_id", "talent_shares", ["user_id"])

    op.create_table(
        "opportunity_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "opportunity_id",
            sa.Integer(),
            sa.ForeignKey("opportunities.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="interested"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint(
            "opportunity_id", "user_id", name="uq_application_opportunity_user"
        ),
    )
    op.create_index(
        "ix_opportunity_applications_opportunity_id", "opportunity_applications", ["opportunity_id"]
    )
    op.create_index("ix_opportunity_applications_user_id", "opportunity_applications", ["user_id"])

    op.create_table(
        "practice_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "template_id",
            sa.Integer(),
            sa.ForeignKey("task_templates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("answer", JSONPayload, nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_practice_attempts_user_id", "practice_attempts", ["user_id"])
    op.create_index("ix_practice_attempts_template_id", "practice_attempts", ["template_id"])
    op.create_index("ix_practice_attempts_created_at", "practice_attempts", ["created_at"])

    op.create_table(
        "practical_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "practical_task_id",
            sa.Integer(),
            sa.ForeignKey("practical_tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("payload", JSONPayload, nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="submitted"),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column(
            "reviewed_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("client_key", sa.String(length=64), nullable=True, unique=True),
        sa.Column(
            "submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        *_timestamps(),
    )
    op.create_index(
        "ix_practical_submissions_practical_task_id", "practical_submissions", ["practical_task_id"]
    )
    op.create_index("ix_practical_submissions_user_id", "practical_submissions", ["user_id"])

    op.create_table(
        "ask_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("title", sa.String(length=160), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_ask_sessions_user_id", "ask_sessions", ["user_id"])
    op.create_index("ix_ask_sessions_course_id", "ask_sessions", ["course_id"])

    op.create_table(
        "ask_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("ask_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(length=12), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("citations", JSONPayload, nullable=True),
        sa.Column("declined", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_ask_messages_session_id", "ask_messages", ["session_id"])
    op.create_index("ix_ask_messages_created_at", "ask_messages", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_ask_messages_created_at", table_name="ask_messages")
    op.drop_index("ix_ask_messages_session_id", table_name="ask_messages")
    op.drop_table("ask_messages")

    op.drop_index("ix_ask_sessions_course_id", table_name="ask_sessions")
    op.drop_index("ix_ask_sessions_user_id", table_name="ask_sessions")
    op.drop_table("ask_sessions")

    op.drop_index("ix_practical_submissions_user_id", table_name="practical_submissions")
    op.drop_index(
        "ix_practical_submissions_practical_task_id", table_name="practical_submissions"
    )
    op.drop_table("practical_submissions")

    op.drop_index("ix_practice_attempts_created_at", table_name="practice_attempts")
    op.drop_index("ix_practice_attempts_template_id", table_name="practice_attempts")
    op.drop_index("ix_practice_attempts_user_id", table_name="practice_attempts")
    op.drop_table("practice_attempts")

    op.drop_index("ix_opportunity_applications_user_id", table_name="opportunity_applications")
    op.drop_index(
        "ix_opportunity_applications_opportunity_id", table_name="opportunity_applications"
    )
    op.drop_table("opportunity_applications")

    op.drop_index("ix_talent_shares_user_id", table_name="talent_shares")
    op.drop_table("talent_shares")

    op.drop_table("user_availability")

    op.drop_index("ix_user_languages_user_id", table_name="user_languages")
    op.drop_table("user_languages")

    with op.batch_alter_table("question_attempts") as batch:
        batch.drop_constraint("uq_question_attempts_client_key", type_="unique")
        batch.drop_column("client_key")
    op.drop_column("assessment_attempts", "answers")
    op.drop_column("assessment_attempts", "presented_task_ids")
    with op.batch_alter_table("learning_path_steps") as batch:
        batch.drop_column("task_template_id")
    op.drop_column("user_profiles", "location")
