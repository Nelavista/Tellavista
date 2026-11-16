"""Add student opportunities (scholarships, fellowships, competitions, internships...)

Revision ID: e4c9a7b21d50
Revises: d7a3c5e81f42
Create Date: 2026-11-16

Purely additive: five new tables, no change to any existing table. The existing
`opportunities` table (paid gigs, payouts, earnings) is untouched.

Revises: d7a3c5e81f42
"""
from alembic import op
import sqlalchemy as sa

revision = 'e4c9a7b21d50'
down_revision = 'd7a3c5e81f42'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'student_opportunities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('slug', sa.String(length=160), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('organization', sa.String(length=150), nullable=False),
        sa.Column('summary', sa.String(length=300), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('eligibility', sa.Text(), nullable=True),
        sa.Column('benefits', sa.Text(), nullable=True),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('application_steps', sa.Text(), nullable=True),
        sa.Column('eligible_summary', sa.String(length=150), nullable=True),
        sa.Column('category', sa.String(length=40), nullable=False, server_default='other'),
        sa.Column('categories_json', sa.Text(), nullable=True),
        sa.Column('disciplines_json', sa.Text(), nullable=True),
        sa.Column('levels_json', sa.Text(), nullable=True),
        sa.Column('tags_json', sa.Text(), nullable=True),
        sa.Column('location_scope', sa.String(length=20), nullable=False, server_default='nigeria'),
        sa.Column('location', sa.String(length=150), nullable=True),
        sa.Column('delivery_format', sa.String(length=20), nullable=True),
        sa.Column('opens_at', sa.Date(), nullable=True),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('is_rolling', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('deadline_note', sa.String(length=200), nullable=True),
        sa.Column('manually_closed', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('application_mode', sa.String(length=30), nullable=False, server_default='EXTERNAL_WEBVIEW'),
        sa.Column('application_url', sa.String(length=500), nullable=True),
        sa.Column('embed_url', sa.String(length=500), nullable=True),
        sa.Column('allows_in_app_view', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('framing_checked_at', sa.DateTime(), nullable=True),
        sa.Column('official_website', sa.String(length=500), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('is_partner', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('partner_note', sa.String(length=300), nullable=True),
        sa.Column('verification_status', sa.String(length=20), nullable=False, server_default='unverified'),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('verified_by_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('last_checked_at', sa.DateTime(), nullable=True),
        sa.Column('verification_notes', sa.Text(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('featured', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_by_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_student_opportunities_slug', 'student_opportunities', ['slug'], unique=True)
    op.create_index('ix_student_opportunities_category', 'student_opportunities', ['category'])
    op.create_index('ix_student_opportunities_is_published', 'student_opportunities', ['is_published'])

    op.create_table(
        'student_opportunity_saves',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('opportunity_id', sa.Integer(), sa.ForeignKey('student_opportunities.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'opportunity_id', name='uq_student_opp_save'),
    )
    op.create_index('ix_student_opportunity_saves_user_id', 'student_opportunity_saves', ['user_id'])
    op.create_index('ix_student_opportunity_saves_opportunity_id', 'student_opportunity_saves', ['opportunity_id'])

    op.create_table(
        'student_opportunity_applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('opportunity_id', sa.Integer(), sa.ForeignKey('student_opportunities.id'), nullable=False),
        sa.Column('source', sa.String(length=20), nullable=False, server_default='self_reported'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='applied'),
        sa.Column('applied_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'opportunity_id', name='uq_student_opp_application'),
    )
    op.create_index('ix_student_opportunity_applications_user_id', 'student_opportunity_applications', ['user_id'])
    op.create_index('ix_student_opportunity_applications_opportunity_id', 'student_opportunity_applications', ['opportunity_id'])

    op.create_table(
        'student_opportunity_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('opportunity_id', sa.Integer(), sa.ForeignKey('student_opportunities.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('event_type', sa.String(length=20), nullable=False),
        sa.Column('channel', sa.String(length=30), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_student_opportunity_events_opportunity_id', 'student_opportunity_events', ['opportunity_id'])
    op.create_index('ix_student_opportunity_events_user_id', 'student_opportunity_events', ['user_id'])
    op.create_index('ix_student_opportunity_events_event_type', 'student_opportunity_events', ['event_type'])
    op.create_index('ix_student_opportunity_events_created_at', 'student_opportunity_events', ['created_at'])

    op.create_table(
        'student_opportunity_reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('opportunity_id', sa.Integer(), sa.ForeignKey('student_opportunities.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('reason', sa.String(length=30), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('resolved', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_student_opportunity_reports_opportunity_id', 'student_opportunity_reports', ['opportunity_id'])


def downgrade():
    op.drop_table('student_opportunity_reports')
    op.drop_table('student_opportunity_events')
    op.drop_table('student_opportunity_applications')
    op.drop_table('student_opportunity_saves')
    op.drop_table('student_opportunities')
