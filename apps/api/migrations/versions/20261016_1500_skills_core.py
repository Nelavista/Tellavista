"""skills: categories, skills, learning paths, lessons, task templates, progress

Revision ID: 20261016_1500
Revises: 20261016_1400
Create Date: 2026-10-16

Phase 0 PR 0.2b. Pure expansion: seven new tables, nothing altered.

`task_templates` is the one that earns its keep: its instructions, input schema,
answer schema and validator name are data, so the second annotation task type is
seeded content rather than a code path. `version` and `status` are part of the
table from the start because a live cohort must never have its task redefined
underneath it.

Nothing here can verify a student. `lesson_progress` records study; verification
arrives in M3 from assessments with known answers.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261016_1500"
down_revision: str | None = "20261016_1400"
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
        "skill_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("ordinal", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_skill_categories_slug"),
    )
    op.create_index("ix_skill_categories_slug", "skill_categories", ["slug"])

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("skill_categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_skills_slug"),
    )
    op.create_index("ix_skills_slug", "skills", ["slug"])
    op.create_index("ix_skills_category_id", "skills", ["category_id"])

    op.create_table(
        "learning_paths",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "skill_id",
            sa.Integer(),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("level", sa.String(length=20), nullable=False, server_default="beginner"),
        sa.Column("estimated_hours", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_learning_paths_slug"),
    )
    op.create_index("ix_learning_paths_slug", "learning_paths", ["slug"])
    op.create_index("ix_learning_paths_skill_id", "learning_paths", ["skill_id"])

    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "skill_id",
            sa.Integer(),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body_md", sa.Text(), nullable=False, server_default=""),
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_lessons_slug"),
    )
    op.create_index("ix_lessons_slug", "lessons", ["slug"])
    op.create_index("ix_lessons_skill_id", "lessons", ["skill_id"])

    op.create_table(
        "learning_path_steps",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "path_id",
            sa.Integer(),
            sa.ForeignKey("learning_paths.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column(
            "lesson_id", sa.Integer(), sa.ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True
        ),
        *_timestamps(),
        sa.UniqueConstraint("path_id", "ordinal", name="uq_path_step_ordinal"),
    )
    op.create_index("ix_learning_path_steps_path_id", "learning_path_steps", ["path_id"])

    op.create_table(
        "task_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "skill_id",
            sa.Integer(),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("instructions_md", sa.Text(), nullable=False, server_default=""),
        sa.Column("input_schema", JSONPayload, nullable=False),
        sa.Column("answer_schema", JSONPayload, nullable=False),
        sa.Column("validator", sa.String(length=40), nullable=False, server_default="exact_key"),
        sa.Column("config", JSONPayload, nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        *_timestamps(),
        sa.UniqueConstraint("slug", name="uq_task_templates_slug"),
    )
    op.create_index("ix_task_templates_slug", "task_templates", ["slug"])
    op.create_index("ix_task_templates_skill_id", "task_templates", ["skill_id"])

    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="not_started"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_lesson_progress_user_lesson"),
    )
    op.create_index("ix_lesson_progress_user_id", "lesson_progress", ["user_id"])
    op.create_index("ix_lesson_progress_lesson_id", "lesson_progress", ["lesson_id"])


def downgrade() -> None:
    op.drop_index("ix_lesson_progress_lesson_id", table_name="lesson_progress")
    op.drop_index("ix_lesson_progress_user_id", table_name="lesson_progress")
    op.drop_table("lesson_progress")

    op.drop_index("ix_task_templates_skill_id", table_name="task_templates")
    op.drop_index("ix_task_templates_slug", table_name="task_templates")
    op.drop_table("task_templates")

    op.drop_index("ix_learning_path_steps_path_id", table_name="learning_path_steps")
    op.drop_table("learning_path_steps")

    op.drop_index("ix_lessons_skill_id", table_name="lessons")
    op.drop_index("ix_lessons_slug", table_name="lessons")
    op.drop_table("lessons")

    op.drop_index("ix_learning_paths_skill_id", table_name="learning_paths")
    op.drop_index("ix_learning_paths_slug", table_name="learning_paths")
    op.drop_table("learning_paths")

    op.drop_index("ix_skills_category_id", table_name="skills")
    op.drop_index("ix_skills_slug", table_name="skills")
    op.drop_table("skills")

    op.drop_index("ix_skill_categories_slug", table_name="skill_categories")
    op.drop_table("skill_categories")
