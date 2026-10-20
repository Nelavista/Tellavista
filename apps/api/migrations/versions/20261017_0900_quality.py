"""quality: standards, reviews, rolling records and consequences

Revision ID: 20261017_0900
Revises: 20261016_1800
Create Date: 2026-10-17

Phase 5. Four new tables, no alterations.

`quality_reviews` is append-only (no updated_at): a reviewer who changes their
mind writes a second review, and the latest one is the current verdict. That is
what keeps "why was this submission paid?" answerable after the fact.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261017_0900"
down_revision: str | None = "20261016_1800"
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
        "quality_standards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("instructions_md", sa.Text(), nullable=False, server_default=""),
        sa.Column("rubric", JSONPayload, nullable=True),
        sa.Column("pass_threshold", sa.Integer(), nullable=False, server_default="80"),
        sa.Column("rules", JSONPayload, nullable=False),
        *_timestamps(),
    )
    op.create_index("ix_quality_standards_project_id", "quality_standards", ["project_id"])

    op.create_table(
        "quality_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "submission_id",
            sa.Integer(),
            sa.ForeignKey("submissions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "reviewer_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("verdict", sa.String(length=16), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_gold", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("gold_correct", sa.Boolean(), nullable=True),
        sa.Column(
            "agrees_with_review_id",
            sa.Integer(),
            sa.ForeignKey("quality_reviews.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_override", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("reason", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_quality_reviews_submission_id", "quality_reviews", ["submission_id"])
    op.create_index("ix_quality_reviews_reviewer_user_id", "quality_reviews", ["reviewer_user_id"])
    op.create_index("ix_quality_reviews_created_at", "quality_reviews", ["created_at"])

    op.create_table(
        "quality_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("reviews_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("approvals", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reworks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rejections", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("average_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gold_tasks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gold_correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("poor_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_review_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("user_id", "project_id", name="uq_quality_record_user_project"),
    )
    op.create_index("ix_quality_records_user_id", "quality_records", ["user_id"])
    op.create_index("ix_quality_records_project_id", "quality_records", ["project_id"])

    op.create_table(
        "quality_consequences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column(
            "quality_record_id",
            sa.Integer(),
            sa.ForeignKey("quality_records.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("lifted_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_quality_consequences_user_id", "quality_consequences", ["user_id"])
    op.create_index("ix_quality_consequences_project_id", "quality_consequences", ["project_id"])


def downgrade() -> None:
    op.drop_index("ix_quality_consequences_project_id", table_name="quality_consequences")
    op.drop_index("ix_quality_consequences_user_id", table_name="quality_consequences")
    op.drop_table("quality_consequences")

    op.drop_index("ix_quality_records_project_id", table_name="quality_records")
    op.drop_index("ix_quality_records_user_id", table_name="quality_records")
    op.drop_table("quality_records")

    op.drop_index("ix_quality_reviews_created_at", table_name="quality_reviews")
    op.drop_index("ix_quality_reviews_reviewer_user_id", table_name="quality_reviews")
    op.drop_index("ix_quality_reviews_submission_id", table_name="quality_reviews")
    op.drop_table("quality_reviews")

    op.drop_index("ix_quality_standards_project_id", table_name="quality_standards")
    op.drop_table("quality_standards")
