"""Add courses.source.

Distinguishes a department's own registrar-verified course codes (NULL) from rows seeded
from the NUC's national core curriculum (CCMAS) for schools with no school-specific
catalog yet (see seed_ccmas_core.py). NOTE: courses.description is NOT added here --
b6d94f0e2a17 (the previous migration) already adds it; an earlier draft of this migration
duplicated that column before this was caught.

Revision ID: c8f4a1e93b56
Revises: b6d94f0e2a17
Create Date: 2026-08-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c8f4a1e93b56'
down_revision = 'b6d94f0e2a17'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('courses', sa.Column('source', sa.String(length=30), nullable=True))


def downgrade():
    op.drop_column('courses', 'source')
