"""Add StudentProject.notebook_cells_json — backs the new 'data' (notebook-style)
project workspace, alongside the existing developer/writer/designer workspaces.

Revision ID: a3f8d2c94e61
Revises: 8f71db33eaa8
Create Date: 2026-08-28 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'a3f8d2c94e61'
down_revision = '8f71db33eaa8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notebook_cells_json', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.drop_column('notebook_cells_json')
