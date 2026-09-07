"""Add grading_events -- an append-only audit trail for every AI grading attempt

Part of the Skills implementation plan's grading-integrity redesign (Step 4): one row per
grading ATTEMPT (including failed/malformed ones, not just successes) across every scored
Skills evaluator -- challenge feedback, assignment grading, ordinary project review, and
final-project rubric scoring. Nothing writes here yet; services/ai_grading.py (added in a
later phase) is the one call path that will. Purely additive -- no existing table changes.

Revision ID: b58e1c7f4a29
Revises: a92f6d3e8b41
Create Date: 2026-09-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b58e1c7f4a29'
down_revision = 'a92f6d3e8b41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'grading_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('submission_type', sa.String(length=30), nullable=False),
        sa.Column('submission_id', sa.Integer(), nullable=False),
        sa.Column('triggered_by', sa.String(length=20), nullable=False, server_default='student'),
        sa.Column('model', sa.String(length=80), nullable=True),
        sa.Column('prompt_version', sa.String(length=40), nullable=True),
        sa.Column('raw_scores_json', sa.Text(), nullable=True),
        sa.Column('final_scores_json', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='ok'),
        sa.Column('error_detail', sa.String(length=300), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_grading_events_submission_type', 'grading_events', ['submission_type'])
    op.create_index('ix_grading_events_submission_id', 'grading_events', ['submission_id'])
    op.create_index('ix_grading_events_created_at', 'grading_events', ['created_at'])


def downgrade():
    op.drop_index('ix_grading_events_created_at', table_name='grading_events')
    op.drop_index('ix_grading_events_submission_id', table_name='grading_events')
    op.drop_index('ix_grading_events_submission_type', table_name='grading_events')
    op.drop_table('grading_events')
