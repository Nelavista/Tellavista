"""Add tables for the Skills product rebuild: project milestones, employer ratings,
competitions, notifications, and in-app messaging.

Revision ID: a5d8c2f61b94
Revises: f9b3e6c2a105
Create Date: 2026-08-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a5d8c2f61b94'
down_revision = 'f9b3e6c2a105'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'project_milestones',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_project_id', sa.Integer(), sa.ForeignKey('student_projects.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.String(length=300)),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('is_done', sa.Boolean(), server_default=sa.false()),
        sa.Column('completed_at', sa.DateTime()),
    )

    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('opportunity_application_id', sa.Integer(), sa.ForeignKey('opportunity_applications.id'), nullable=False),
        sa.Column('employer_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('stars', sa.Integer(), nullable=False),
        sa.Column('comment', sa.String(length=500)),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('opportunity_application_id', name='uq_rating_application'),
    )

    op.create_table(
        'competitions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('prize_amount', sa.Integer(), server_default='0'),
        sa.Column('currency', sa.String(length=10), server_default='NGN'),
        sa.Column('deadline', sa.DateTime()),
        sa.Column('skills_tags_json', sa.Text()),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('slug', name='uq_competition_slug'),
    )

    op.create_table(
        'competition_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('competition_id', sa.Integer(), sa.ForeignKey('competitions.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('submission_url', sa.String(length=500)),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(length=20), server_default='submitted'),
        sa.Column('submitted_at', sa.DateTime()),
        sa.UniqueConstraint('competition_id', 'student_id', name='uq_competition_student'),
    )

    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('type', sa.String(length=40), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('body', sa.String(length=400)),
        sa.Column('link_url', sa.String(length=300)),
        sa.Column('is_read', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime()),
    )

    op.create_table(
        'message_threads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('employer_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('opportunity_application_id', sa.Integer(), sa.ForeignKey('opportunity_applications.id'), nullable=True),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('last_message_at', sa.DateTime()),
        sa.UniqueConstraint('employer_id', 'student_id', name='uq_thread_employer_student'),
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('thread_id', sa.Integer(), sa.ForeignKey('message_threads.id'), nullable=False),
        sa.Column('sender_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('messages')
    op.drop_table('message_threads')
    op.drop_table('notifications')
    op.drop_table('competition_entries')
    op.drop_table('competitions')
    op.drop_table('ratings')
    op.drop_table('project_milestones')
