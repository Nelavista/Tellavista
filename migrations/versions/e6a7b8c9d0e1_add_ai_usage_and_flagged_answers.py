"""Add ai_usage_log (G6) and flagged_ai_answers (G10).

ai_usage_log: one row per AI feature call -- per-user, per-feature token counters
(PRD §21's AI usage monitoring). Aggregate counters only, never prompt/response
content, per §7's data-minimal-retention rule.

flagged_ai_answers: the destination for student-reported incorrect AI answers --
PRD §6's "log AI responses flagged incorrect by students to build an accuracy
feedback loop", which until now had no storage at all (migration-map gap G10) and is
also the moderation queue §9 asks admins to review.

Both are standalone tables, no existing column is touched.

Revision ID: e6a7b8c9d0e1
Revises: d5e9f0a1b2c3
Create Date: 2026-09-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'e6a7b8c9d0e1'
down_revision = 'd5e9f0a1b2c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ai_usage_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('feature', sa.String(length=40), nullable=False),
        sa.Column('model', sa.String(length=120), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=True),
        sa.Column('completion_tokens', sa.Integer(), nullable=True),
        sa.Column('ok', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime()),
    )
    op.create_index('ix_ai_usage_log_user_id', 'ai_usage_log', ['user_id'])
    op.create_index('ix_ai_usage_log_feature', 'ai_usage_log', ['feature'])
    op.create_index('ix_ai_usage_log_created_at', 'ai_usage_log', ['created_at'])

    op.create_table(
        'flagged_ai_answers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('feature', sa.String(length=40), nullable=False),
        sa.Column('reference_id', sa.Integer(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='open'),
        sa.Column('resolution_note', sa.Text(), nullable=True),
        sa.Column('resolved_by', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('resolved_at', sa.DateTime()),
    )
    op.create_index('ix_flagged_ai_answers_user_id', 'flagged_ai_answers', ['user_id'])
    op.create_index('ix_flagged_ai_answers_status', 'flagged_ai_answers', ['status'])


def downgrade():
    op.drop_index('ix_flagged_ai_answers_status', table_name='flagged_ai_answers')
    op.drop_index('ix_flagged_ai_answers_user_id', table_name='flagged_ai_answers')
    op.drop_table('flagged_ai_answers')
    op.drop_index('ix_ai_usage_log_created_at', table_name='ai_usage_log')
    op.drop_index('ix_ai_usage_log_feature', table_name='ai_usage_log')
    op.drop_index('ix_ai_usage_log_user_id', table_name='ai_usage_log')
    op.drop_table('ai_usage_log')
