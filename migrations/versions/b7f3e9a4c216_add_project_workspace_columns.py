"""Add project-workspace columns to student_projects: screenshots, AI review, and
Talent Profile visibility.

Revision ID: b7f3e9a4c216
Revises: a5d8c2f61b94
Create Date: 2026-08-24 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'b7f3e9a4c216'
down_revision = 'a5d8c2f61b94'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('screenshots_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('ai_feedback_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('verification_status', sa.String(length=20), server_default='none'))
        batch_op.add_column(sa.Column('is_public', sa.Boolean(), server_default=sa.true()))


def downgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.drop_column('is_public')
        batch_op.drop_column('verification_status')
        batch_op.drop_column('ai_feedback_json')
        batch_op.drop_column('screenshots_json')
