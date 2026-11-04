"""African Languages Lab catalogue metadata and career tracks.

Revision ID: 20261104_2100
Revises: 20261022_1000
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261104_2100"
down_revision: str | None = "20261022_1000"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")


def upgrade() -> None:
    op.add_column(
        "skill_categories",
        sa.Column("program", sa.String(length=40), nullable=False, server_default="core"),
    )
    op.create_index("ix_skill_categories_program", "skill_categories", ["program"])
    op.add_column("skills", sa.Column("language", sa.String(length=60), nullable=True))
    op.add_column("skills", sa.Column("tags", JSONPayload, nullable=True))
    op.create_index("ix_skills_language", "skills", ["language"])

    op.create_table(
        "career_tracks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("tagline", sa.String(length=500), nullable=True),
        sa.Column("icon", sa.String(length=80), nullable=True),
        sa.Column("color", sa.String(length=20), nullable=True),
        sa.Column("program", sa.String(length=40), nullable=False, server_default="core"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="published"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("slug", name="uq_career_tracks_slug"),
    )
    op.create_index("ix_career_tracks_slug", "career_tracks", ["slug"])
    op.create_index("ix_career_tracks_program", "career_tracks", ["program"])
    op.create_table(
        "career_track_steps",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "track_id",
            sa.Integer(),
            sa.ForeignKey("career_tracks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "skill_id",
            sa.Integer(),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("track_id", "ordinal", name="uq_career_track_step_ordinal"),
        sa.UniqueConstraint("track_id", "skill_id", name="uq_career_track_step_skill"),
    )
    op.create_index("ix_career_track_steps_track_id", "career_track_steps", ["track_id"])
    op.create_index("ix_career_track_steps_skill_id", "career_track_steps", ["skill_id"])


def downgrade() -> None:
    op.drop_index("ix_career_track_steps_skill_id", table_name="career_track_steps")
    op.drop_index("ix_career_track_steps_track_id", table_name="career_track_steps")
    op.drop_table("career_track_steps")
    op.drop_index("ix_career_tracks_program", table_name="career_tracks")
    op.drop_index("ix_career_tracks_slug", table_name="career_tracks")
    op.drop_table("career_tracks")
    op.drop_index("ix_skills_language", table_name="skills")
    op.drop_column("skills", "tags")
    op.drop_column("skills", "language")
    op.drop_index("ix_skill_categories_program", table_name="skill_categories")
    op.drop_column("skill_categories", "program")
