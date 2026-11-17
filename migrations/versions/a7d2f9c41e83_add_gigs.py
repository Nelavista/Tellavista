"""Add gigs: providers, sync runs, normalised gigs, saves, self-reported applications, events

Revision ID: a7d2f9c41e83
Revises: e4c9a7b21d50
Create Date: 2026-11-17

Purely additive: six new tables. The existing `opportunities` table (Nelavista's own paid
gigs, payouts, earnings) and the student_opportunities tables are untouched.
"""
from alembic import op
import sqlalchemy as sa

revision = 'a7d2f9c41e83'
down_revision = 'e4c9a7b21d50'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gig_providers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('slug', sa.String(length=60), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('kind', sa.String(length=20), nullable=False, server_default='api'),
        sa.Column('adapter', sa.String(length=40), nullable=False, server_default='manual'),
        sa.Column('api_base_url', sa.String(length=500), nullable=True),
        sa.Column('auth_method', sa.String(length=20), nullable=False, server_default='none'),
        sa.Column('auth_param', sa.String(length=60), nullable=True),
        sa.Column('credentials_env', sa.String(length=80), nullable=True),
        sa.Column('config_json', sa.Text(), nullable=True),
        sa.Column('website_url', sa.String(length=500), nullable=True),
        sa.Column('terms_url', sa.String(length=500), nullable=True),
        sa.Column('redistribution_basis', sa.Text(), nullable=True),
        sa.Column('redistribution_confirmed', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('attribution_text', sa.String(length=200), nullable=True),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('auto_publish', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('sync_frequency_minutes', sa.Integer(), nullable=False, server_default='360'),
        sa.Column('stale_after_hours', sa.Integer(), nullable=False, server_default='72'),
        sa.Column('last_sync_at', sa.DateTime(), nullable=True),
        sa.Column('last_success_at', sa.DateTime(), nullable=True),
        sa.Column('last_status', sa.String(length=20), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('consecutive_failures', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_gig_providers_slug', 'gig_providers', ['slug'], unique=True)

    op.create_table(
        'gig_sync_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('provider_id', sa.Integer(), sa.ForeignKey('gig_providers.id'), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='running'),
        sa.Column('triggered_by', sa.String(length=60), nullable=True),
        sa.Column('fetched', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('updated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('closed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('skipped', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('duplicates', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('errors', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
    )
    op.create_index('ix_gig_sync_runs_provider_id', 'gig_sync_runs', ['provider_id'])
    op.create_index('ix_gig_sync_runs_started_at', 'gig_sync_runs', ['started_at'])

    op.create_table(
        'gigs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('slug', sa.String(length=180), nullable=False),
        sa.Column('provider_id', sa.Integer(), sa.ForeignKey('gig_providers.id'), nullable=False),
        sa.Column('source_gig_id', sa.String(length=120), nullable=True),
        sa.Column('origin', sa.String(length=20), nullable=False, server_default='external'),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('organization', sa.String(length=150), nullable=False),
        sa.Column('organization_logo_url', sa.String(length=500), nullable=True),
        sa.Column('summary', sa.String(length=300), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('eligibility', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=40), nullable=False, server_default='other'),
        sa.Column('skills_json', sa.Text(), nullable=True),
        sa.Column('pay_min', sa.Integer(), nullable=True),
        sa.Column('pay_max', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=True),
        sa.Column('pay_type', sa.String(length=20), nullable=False, server_default='not_stated'),
        sa.Column('pay_text', sa.String(length=120), nullable=True),
        sa.Column('work_type', sa.String(length=20), nullable=True),
        sa.Column('location_type', sa.String(length=20), nullable=False, server_default='remote'),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('application_url', sa.String(length=500), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('application_mode', sa.String(length=30), nullable=False, server_default='EXTERNAL'),
        sa.Column('allows_in_app_view', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('external_reference', sa.String(length=200), nullable=True),
        sa.Column('posted_at', sa.DateTime(), nullable=True),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('source_status', sa.String(length=20), nullable=False, server_default='UNKNOWN'),
        sa.Column('status_override', sa.String(length=20), nullable=True),
        sa.Column('last_verified_at', sa.DateTime(), nullable=True),
        sa.Column('last_synced_at', sa.DateTime(), nullable=True),
        sa.Column('last_seen_at', sa.DateTime(), nullable=True),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.Column('dedupe_key', sa.String(length=64), nullable=True),
        sa.Column('duplicate_of_id', sa.Integer(), sa.ForeignKey('gigs.id'), nullable=True),
        sa.Column('locked_fields_json', sa.Text(), nullable=True),
        sa.Column('raw_json', sa.Text(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('featured', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('removed_reason', sa.String(length=200), nullable=True),
        sa.Column('verified_by_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('created_by_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('provider_id', 'source_gig_id', name='uq_gig_provider_source'),
    )
    op.create_index('ix_gigs_slug', 'gigs', ['slug'], unique=True)
    op.create_index('ix_gigs_provider_id', 'gigs', ['provider_id'])
    op.create_index('ix_gigs_category', 'gigs', ['category'])
    op.create_index('ix_gigs_dedupe_key', 'gigs', ['dedupe_key'])
    op.create_index('ix_gigs_duplicate_of_id', 'gigs', ['duplicate_of_id'])
    op.create_index('ix_gigs_is_published', 'gigs', ['is_published'])
    op.create_index('ix_gigs_created_at', 'gigs', ['created_at'])

    op.create_table(
        'gig_saves',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('gig_id', sa.Integer(), sa.ForeignKey('gigs.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'gig_id', name='uq_gig_save'),
    )
    op.create_index('ix_gig_saves_user_id', 'gig_saves', ['user_id'])
    op.create_index('ix_gig_saves_gig_id', 'gig_saves', ['gig_id'])

    op.create_table(
        'gig_applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('gig_id', sa.Integer(), sa.ForeignKey('gigs.id'), nullable=False),
        sa.Column('source', sa.String(length=20), nullable=False, server_default='self_reported'),
        sa.Column('applied_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'gig_id', name='uq_gig_application'),
    )
    op.create_index('ix_gig_applications_user_id', 'gig_applications', ['user_id'])
    op.create_index('ix_gig_applications_gig_id', 'gig_applications', ['gig_id'])

    op.create_table(
        'gig_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('gig_id', sa.Integer(), sa.ForeignKey('gigs.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('event_type', sa.String(length=30), nullable=False),
        sa.Column('channel', sa.String(length=30), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_gig_events_gig_id', 'gig_events', ['gig_id'])
    op.create_index('ix_gig_events_user_id', 'gig_events', ['user_id'])
    op.create_index('ix_gig_events_event_type', 'gig_events', ['event_type'])
    op.create_index('ix_gig_events_created_at', 'gig_events', ['created_at'])


def downgrade():
    op.drop_table('gig_events')
    op.drop_table('gig_applications')
    op.drop_table('gig_saves')
    op.drop_table('gigs')
    op.drop_table('gig_sync_runs')
    op.drop_table('gig_providers')
