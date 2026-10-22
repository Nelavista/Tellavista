"""matching and work: opportunities, requirements, gaps, projects, cohorts, submissions

Revision ID: 20261016_1700
Revises: 20261016_1600
Create Date: 2026-10-16

Phase 0 PR 0.3b. Nine new tables, nothing altered.

Two constraints carry product rules rather than just data hygiene:
* `match_results` is unique per (opportunity, student) — one verdict, recomputed.
* `submissions.idempotency_key` is unique, so a retry from a dropped connection
  records one submission. Nullable, because ops may create rows without a key.

`opportunities.type` (managed | external) is the fee switch the money module
reads; no ledger entry may be created for an external opportunity.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261016_1700"
down_revision: str | None = "20261016_1600"
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
        "opportunities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("type", sa.String(length=16), nullable=False, server_default="managed"),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("client_name", sa.String(length=200), nullable=True),
        sa.Column(
            "department_id",
            sa.Integer(),
            sa.ForeignKey("departments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("headcount", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        sa.Column("quality_standard", sa.String(length=200), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.Column("rate_minor", sa.Integer(), nullable=True),
        sa.Column("starts_on", sa.Date(), nullable=True),
        sa.Column("ends_on", sa.Date(), nullable=True),
        sa.Column(
            "created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_opportunities_slug"),
    )
    op.create_index("ix_opportunities_slug", "opportunities", ["slug"])
    op.create_index("ix_opportunities_department_id", "opportunities", ["department_id"])

    op.create_table(
        "requirements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "opportunity_id",
            sa.Integer(),
            sa.ForeignKey("opportunities.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column(
            "skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("minimum_value", sa.String(length=120), nullable=True),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("description", sa.String(length=255), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_requirements_opportunity_id", "requirements", ["opportunity_id"])
    op.create_index("ix_requirements_skill_id", "requirements", ["skill_id"])

    op.create_table(
        "match_results",
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
        sa.Column("eligible", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("explanation", JSONPayload, nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("opportunity_id", "user_id", name="uq_match_opportunity_user"),
    )
    op.create_index("ix_match_results_opportunity_id", "match_results", ["opportunity_id"])
    op.create_index("ix_match_results_user_id", "match_results", ["user_id"])

    op.create_table(
        "skill_gaps",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "opportunity_id",
            sa.Integer(),
            sa.ForeignKey("opportunities.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "requirement_id",
            sa.Integer(),
            sa.ForeignKey("requirements.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="missing"),
        sa.Column("detail", sa.String(length=255), nullable=True),
        sa.Column(
            "closes_via_learning_path_id",
            sa.Integer(),
            sa.ForeignKey("learning_paths.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "closes_via_assessment_id",
            sa.Integer(),
            sa.ForeignKey("assessments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        *_timestamps(),
        sa.UniqueConstraint("user_id", "requirement_id", name="uq_gap_user_requirement"),
    )
    op.create_index("ix_skill_gaps_user_id", "skill_gaps", ["user_id"])
    op.create_index("ix_skill_gaps_opportunity_id", "skill_gaps", ["opportunity_id"])
    op.create_index("ix_skill_gaps_requirement_id", "skill_gaps", ["requirement_id"])

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "opportunity_id",
            sa.Integer(),
            sa.ForeignKey("opportunities.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        sa.Column("starts_on", sa.Date(), nullable=True),
        sa.Column("ends_on", sa.Date(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_projects_slug"),
    )
    op.create_index("ix_projects_slug", "projects", ["slug"])

    op.create_table(
        "cohorts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="forming"),
        *_timestamps(),
    )
    op.create_index("ix_cohorts_project_id", "cohorts", ["project_id"])

    op.create_table(
        "cohort_members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "cohort_id", sa.Integer(), sa.ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="invited"),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("cohort_id", "user_id", name="uq_cohort_member"),
    )
    op.create_index("ix_cohort_members_cohort_id", "cohort_members", ["cohort_id"])
    op.create_index("ix_cohort_members_user_id", "cohort_members", ["user_id"])

    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "cohort_id", sa.Integer(), sa.ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "template_id",
            sa.Integer(),
            sa.ForeignKey("task_templates.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="assigned"),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_assignments_project_id", "assignments", ["project_id"])
    op.create_index("ix_assignments_cohort_id", "assignments", ["cohort_id"])
    op.create_index("ix_assignments_user_id", "assignments", ["user_id"])

    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "assignment_id",
            sa.Integer(),
            sa.ForeignKey("assignments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("payload", JSONPayload, nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="submitted"),
        sa.Column(
            "submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("idempotency_key", sa.String(length=64), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("idempotency_key", name="uq_submissions_idempotency_key"),
    )
    op.create_index("ix_submissions_assignment_id", "submissions", ["assignment_id"])
    op.create_index("ix_submissions_user_id", "submissions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_submissions_user_id", table_name="submissions")
    op.drop_index("ix_submissions_assignment_id", table_name="submissions")
    op.drop_table("submissions")

    op.drop_index("ix_assignments_user_id", table_name="assignments")
    op.drop_index("ix_assignments_cohort_id", table_name="assignments")
    op.drop_index("ix_assignments_project_id", table_name="assignments")
    op.drop_table("assignments")

    op.drop_index("ix_cohort_members_user_id", table_name="cohort_members")
    op.drop_index("ix_cohort_members_cohort_id", table_name="cohort_members")
    op.drop_table("cohort_members")

    op.drop_index("ix_cohorts_project_id", table_name="cohorts")
    op.drop_table("cohorts")

    op.drop_index("ix_projects_slug", table_name="projects")
    op.drop_table("projects")

    op.drop_index("ix_skill_gaps_requirement_id", table_name="skill_gaps")
    op.drop_index("ix_skill_gaps_opportunity_id", table_name="skill_gaps")
    op.drop_index("ix_skill_gaps_user_id", table_name="skill_gaps")
    op.drop_table("skill_gaps")

    op.drop_index("ix_match_results_user_id", table_name="match_results")
    op.drop_index("ix_match_results_opportunity_id", table_name="match_results")
    op.drop_table("match_results")

    op.drop_index("ix_requirements_skill_id", table_name="requirements")
    op.drop_index("ix_requirements_opportunity_id", table_name="requirements")
    op.drop_table("requirements")

    op.drop_index("ix_opportunities_department_id", table_name="opportunities")
    op.drop_index("ix_opportunities_slug", table_name="opportunities")
    op.drop_table("opportunities")
