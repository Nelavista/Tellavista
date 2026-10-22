"""verification: records, evidence events, assessments, practical tasks, transcript

Revision ID: 20261016_1600
Revises: 20261016_1500
Create Date: 2026-10-16

Phase 0 PR 0.3a. Seven new tables, nothing altered.

`verification_events` is append-only by shape (no `updated_at`) and requires an
`evidence_type`/`evidence_id` on every row, so a status can never change without
naming what proved it. `assessment_tasks.expected_answer` is the gold standard the
attempt is graded against; `payload` is self-contained so retiring a task template
(`SET NULL`) does not corrupt an assessment that already graded real students.

The transcript's unique key is the anti-duplication rule for replaying events.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261016_1600"
down_revision: str | None = "20261016_1500"
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
        "verification_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="unverified"),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_evaluated_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("user_id", "skill_id", name="uq_verification_user_skill"),
    )
    op.create_index("ix_verification_records_user_id", "verification_records", ["user_id"])
    op.create_index("ix_verification_records_skill_id", "verification_records", ["skill_id"])

    op.create_table(
        "verification_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "record_id",
            sa.Integer(),
            sa.ForeignKey("verification_records.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("from_status", sa.String(length=16), nullable=True),
        sa.Column("to_status", sa.String(length=16), nullable=False),
        sa.Column("evidence_type", sa.String(length=30), nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=True),
        sa.Column(
            "actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_verification_events_record_id", "verification_events", ["record_id"])
    op.create_index("ix_verification_events_actor_user_id", "verification_events", ["actor_user_id"])
    op.create_index("ix_verification_events_created_at", "verification_events", ["created_at"])

    op.create_table(
        "assessments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("pass_threshold", sa.Integer(), nullable=False, server_default="80"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("task_count", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_assessments_slug"),
    )
    op.create_index("ix_assessments_slug", "assessments", ["slug"])
    op.create_index("ix_assessments_skill_id", "assessments", ["skill_id"])

    op.create_table(
        "assessment_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "assessment_id",
            sa.Integer(),
            sa.ForeignKey("assessments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column(
            "template_id",
            sa.Integer(),
            sa.ForeignKey("task_templates.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("payload", JSONPayload, nullable=False),
        sa.Column("expected_answer", JSONPayload, nullable=False),
        sa.Column("points", sa.Integer(), nullable=False, server_default="1"),
        *_timestamps(),
        sa.UniqueConstraint("assessment_id", "ordinal", name="uq_assessment_task_ordinal"),
    )
    op.create_index("ix_assessment_tasks_assessment_id", "assessment_tasks", ["assessment_id"])

    op.create_table(
        "assessment_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "assessment_id",
            sa.Integer(),
            sa.ForeignKey("assessments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=True),
    )
    op.create_index("ix_assessment_attempts_assessment_id", "assessment_attempts", ["assessment_id"])
    op.create_index("ix_assessment_attempts_user_id", "assessment_attempts", ["user_id"])

    op.create_table(
        "practical_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("brief_md", sa.Text(), nullable=False, server_default=""),
        sa.Column("rubric", JSONPayload, nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_practical_tasks_slug"),
    )
    op.create_index("ix_practical_tasks_slug", "practical_tasks", ["slug"])
    op.create_index("ix_practical_tasks_skill_id", "practical_tasks", ["skill_id"])

    op.create_table(
        "transcript_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("evidence_type", sa.String(length=30), nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=False),
        sa.Column(
            "occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint(
            "user_id", "kind", "evidence_type", "evidence_id", name="uq_transcript_evidence"
        ),
    )
    op.create_index("ix_transcript_entries_user_id", "transcript_entries", ["user_id"])
    op.create_index("ix_transcript_entries_occurred_at", "transcript_entries", ["occurred_at"])


def downgrade() -> None:
    op.drop_index("ix_transcript_entries_occurred_at", table_name="transcript_entries")
    op.drop_index("ix_transcript_entries_user_id", table_name="transcript_entries")
    op.drop_table("transcript_entries")

    op.drop_index("ix_practical_tasks_skill_id", table_name="practical_tasks")
    op.drop_index("ix_practical_tasks_slug", table_name="practical_tasks")
    op.drop_table("practical_tasks")

    op.drop_index("ix_assessment_attempts_user_id", table_name="assessment_attempts")
    op.drop_index("ix_assessment_attempts_assessment_id", table_name="assessment_attempts")
    op.drop_table("assessment_attempts")

    op.drop_index("ix_assessment_tasks_assessment_id", table_name="assessment_tasks")
    op.drop_table("assessment_tasks")

    op.drop_index("ix_assessments_skill_id", table_name="assessments")
    op.drop_index("ix_assessments_slug", table_name="assessments")
    op.drop_table("assessments")

    op.drop_index("ix_verification_events_created_at", table_name="verification_events")
    op.drop_index("ix_verification_events_actor_user_id", table_name="verification_events")
    op.drop_index("ix_verification_events_record_id", table_name="verification_events")
    op.drop_table("verification_events")

    op.drop_index("ix_verification_records_skill_id", table_name="verification_records")
    op.drop_index("ix_verification_records_user_id", table_name="verification_records")
    op.drop_table("verification_records")
