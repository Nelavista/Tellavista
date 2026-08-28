"""Add TopicProgress (basic per-student topic completion tracking)

Revision ID: 8f71db33eaa8
Revises: d00f3200eb0b
Create Date: 2026-08-28 00:00:00.000000

Adds `topic_progress` -- deliberately minimal (row exists = the student marked that
topic complete; no partial states, no streaks) per the product principle that this is
basic completion tracking, not another statistics dashboard. Purely additive: a new
table only, nothing existing touched.
"""
from alembic import op
import sqlalchemy as sa

revision = '8f71db33eaa8'
down_revision = 'd00f3200eb0b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'topic_progress',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('topic_id', sa.Integer(), sa.ForeignKey('topics.id'), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'topic_id', name='uq_topic_progress_user_topic'),
    )
    op.create_index('ix_topic_progress_user_id', 'topic_progress', ['user_id'])
    op.create_index('ix_topic_progress_topic_id', 'topic_progress', ['topic_id'])


def downgrade():
    op.drop_index('ix_topic_progress_topic_id', table_name='topic_progress')
    op.drop_index('ix_topic_progress_user_id', table_name='topic_progress')
    op.drop_table('topic_progress')
