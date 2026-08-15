"""Add ChallengeSubmission.feedback_json — structured AI feedback on practice submissions.

Revision ID: d1f6b3c8e4a9
Revises: c9e5a2b7d3f8
Create Date: 2026-08-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'd1f6b3c8e4a9'
down_revision = 'c9e5a2b7d3f8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('challenge_submissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback_json', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('challenge_submissions', schema=None) as batch_op:
        batch_op.drop_column('feedback_json')
