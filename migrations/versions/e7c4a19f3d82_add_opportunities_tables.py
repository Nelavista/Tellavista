"""Add Opportunities (paid gigs) and OpportunityApplication tables — the "Earn" phase
of Learn -> Practice -> Build -> Verify -> Earn.

Revision ID: e7c4a19f3d82
Revises: c8f4a1e93b56
Create Date: 2026-08-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'e7c4a19f3d82'
down_revision = 'c8f4a1e93b56'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'opportunities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('location', sa.String(length=50), server_default='Remote'),
        sa.Column('payment_amount', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(length=10), server_default='NGN'),
        sa.Column('due_date', sa.Date()),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime()),
    )

    op.create_table(
        'opportunity_applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('opportunity_id', sa.Integer(), sa.ForeignKey('opportunities.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='applied'),
        sa.Column('applied_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.Column('paid_at', sa.DateTime()),
        sa.Column('payout_amount', sa.Integer()),
        sa.UniqueConstraint('opportunity_id', 'student_id', name='uq_opportunity_student'),
    )


def downgrade():
    op.drop_table('opportunity_applications')
    op.drop_table('opportunities')
