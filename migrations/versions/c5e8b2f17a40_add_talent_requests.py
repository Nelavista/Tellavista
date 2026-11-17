"""Add talent_requests: organisations' requests from /talent/request

Revision ID: c5e8b2f17a40
Revises: a7d2f9c41e83
Create Date: 2026-11-17

Purely additive: one new table. Nothing existing is touched.
"""
from alembic import op
import sqlalchemy as sa

revision = 'c5e8b2f17a40'
down_revision = 'a7d2f9c41e83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'talent_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('contact_name', sa.String(length=120), nullable=False),
        sa.Column('company_name', sa.String(length=150), nullable=False),
        sa.Column('work_email', sa.String(length=200), nullable=False),
        sa.Column('job_title', sa.String(length=120), nullable=True),
        sa.Column('company_website', sa.String(length=300), nullable=True),
        sa.Column('country', sa.String(length=80), nullable=True),
        sa.Column('need_summary', sa.String(length=500), nullable=False),
        sa.Column('category', sa.String(length=60), nullable=True),
        sa.Column('headcount', sa.String(length=20), nullable=True),
        sa.Column('skills', sa.String(length=500), nullable=True),
        sa.Column('engagement_type', sa.String(length=30), nullable=False),
        sa.Column('start_window', sa.String(length=30), nullable=True),
        sa.Column('budget_range', sa.String(length=30), nullable=True),
        sa.Column('timezone', sa.String(length=30), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('profile_ref', sa.String(length=120), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='new'),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_talent_requests_work_email', 'talent_requests', ['work_email'])
    op.create_index('ix_talent_requests_status', 'talent_requests', ['status'])
    op.create_index('ix_talent_requests_created_at', 'talent_requests', ['created_at'])


def downgrade():
    op.drop_index('ix_talent_requests_created_at', table_name='talent_requests')
    op.drop_index('ix_talent_requests_status', table_name='talent_requests')
    op.drop_index('ix_talent_requests_work_email', table_name='talent_requests')
    op.drop_table('talent_requests')
