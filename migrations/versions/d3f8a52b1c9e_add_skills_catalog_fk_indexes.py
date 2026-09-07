"""Add indexes on the Skills catalog's own filter columns

SQLAlchemy/Postgres does not auto-index a foreign key column -- only the primary key it
points at. Six FK columns that the Skills catalog, course listings, and opportunity board
all filter by (skills.category_id, skill_courses.skill_id, challenges.skill_id,
project_templates.skill_id, opportunities.skill_id, career_track_steps.skill_id) never
got an explicit index; confirmed by grepping every prior migration for `create_index`
against these tables -- none exists. Cheap to add now; expensive to retrofit once these
tables have real row counts. Purely additive -- no existing query or constraint changes.

Revision ID: d3f8a52b1c9e
Revises: c4a9f2e871b3
Create Date: 2026-09-05 00:00:00.000000

"""
from alembic import op

revision = 'd3f8a52b1c9e'
down_revision = 'c4a9f2e871b3'
branch_labels = None
depends_on = None

_INDEXES = [
    ('ix_skills_category_id', 'skills', 'category_id'),
    ('ix_skill_courses_skill_id', 'skill_courses', 'skill_id'),
    ('ix_challenges_skill_id', 'challenges', 'skill_id'),
    ('ix_project_templates_skill_id', 'project_templates', 'skill_id'),
    ('ix_opportunities_skill_id', 'opportunities', 'skill_id'),
    ('ix_career_track_steps_skill_id', 'career_track_steps', 'skill_id'),
]


def upgrade():
    for index_name, table, column in _INDEXES:
        op.create_index(index_name, table, [column])


def downgrade():
    for index_name, table, column in _INDEXES:
        op.drop_index(index_name, table_name=table)
