"""Add Lesson.videos_json — cached auto-fetched YouTube results per lesson.

Revision ID: b8d4f1a6c2e7
Revises: a7c3e9f2b4d1
Create Date: 2026-08-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b8d4f1a6c2e7'
down_revision = 'a7c3e9f2b4d1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('videos_json', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        batch_op.drop_column('videos_json')
