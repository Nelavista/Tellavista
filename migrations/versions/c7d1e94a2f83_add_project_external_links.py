"""Add StudentProject.external_links_json — generic labeled links (Figma, Notion, a
staging URL, anything) beyond the existing repo_url/live_url fields.

Revision ID: c7d1e94a2f83
Revises: a3f8d2c94e61
Create Date: 2026-08-29 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'c7d1e94a2f83'
down_revision = 'a3f8d2c94e61'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('external_links_json', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.drop_column('external_links_json')
