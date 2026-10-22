"""academia: academic calendar, enrolments, topics, RAG chunks, CBT bank

Revision ID: 20261016_1400
Revises: 20261016_1300
Create Date: 2026-10-16

Phase 0 PR 0.2a. Seven new tables, nothing altered — the skeleton taxonomy
(`universities` → `faculties` → `departments` → `courses` → `materials`) is left
exactly as it is, so this revision is safe on an environment that already holds
V1-derived data.

`enrolments` is the important one: it is what the M1 onboarding wizard writes and
what replaces the free-string `users.university/department/level` columns once
those are backfilled.

Order of creation follows the foreign keys: calendar before enrolment, topics
before questions.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261016_1400"
down_revision: str | None = "20261016_1300"
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
        "academic_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=True),
        sa.Column("ends_on", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_timestamps(),
        sa.UniqueConstraint("name", name="uq_academic_sessions_name"),
    )

    op.create_table(
        "semesters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("academic_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=True),
        sa.Column("ends_on", sa.Date(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("session_id", "ordinal", name="uq_semester_session_ordinal"),
    )
    op.create_index("ix_semesters_session_id", "semesters", ["session_id"])

    op.create_table(
        "enrolments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("academic_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "semester_id",
            sa.Integer(),
            sa.ForeignKey("semesters.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="active"),
        *_timestamps(),
        sa.UniqueConstraint(
            "user_id", "course_id", "session_id", name="uq_enrolment_user_course_session"
        ),
    )
    op.create_index("ix_enrolments_user_id", "enrolments", ["user_id"])
    op.create_index("ix_enrolments_course_id", "enrolments", ["course_id"])

    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("course_id", "ordinal", name="uq_topic_course_ordinal"),
    )
    op.create_index("ix_topics_course_id", "topics", ["course_id"])

    op.create_table(
        "material_chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "material_id",
            sa.Integer(),
            sa.ForeignKey("materials.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("material_id", "ordinal", name="uq_chunk_material_ordinal"),
    )
    op.create_index("ix_material_chunks_material_id", "material_chunks", ["material_id"])

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "topic_id", sa.Integer(), sa.ForeignKey("topics.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("options", JSONPayload, nullable=False),
        sa.Column("correct_key", sa.String(length=8), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("difficulty", sa.String(length=10), nullable=False, server_default="medium"),
        sa.Column("source", sa.String(length=30), nullable=False, server_default="seed"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_timestamps(),
    )
    op.create_index("ix_questions_course_id", "questions", ["course_id"])

    op.create_table(
        "question_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("selected_key", sa.String(length=8), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column(
            "answered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_question_attempts_user_id", "question_attempts", ["user_id"])
    op.create_index("ix_question_attempts_question_id", "question_attempts", ["question_id"])


def downgrade() -> None:
    op.drop_index("ix_question_attempts_question_id", table_name="question_attempts")
    op.drop_index("ix_question_attempts_user_id", table_name="question_attempts")
    op.drop_table("question_attempts")

    op.drop_index("ix_questions_course_id", table_name="questions")
    op.drop_table("questions")

    op.drop_index("ix_material_chunks_material_id", table_name="material_chunks")
    op.drop_table("material_chunks")

    op.drop_index("ix_topics_course_id", table_name="topics")
    op.drop_table("topics")

    op.drop_index("ix_enrolments_course_id", table_name="enrolments")
    op.drop_index("ix_enrolments_user_id", table_name="enrolments")
    op.drop_table("enrolments")

    op.drop_index("ix_semesters_session_id", table_name="semesters")
    op.drop_table("semesters")

    op.drop_table("academic_sessions")
