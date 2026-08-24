"""Add CBTQuestion/CBTAttempt/CBTAnswer -- persists CBT practice scores/history and a
seedable question bank (mirroring CBT.html's existing hand-authored questions), where
previously CBT scoring/results only ever existed transiently in the browser.

Revision ID: a4e7f2c81d93
Revises: f3a8c1d92b47
Create Date: 2026-08-21 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a4e7f2c81d93'
down_revision = 'f3a8c1d92b47'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cbt_questions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('subject_code', sa.String(length=10), nullable=False),
        sa.Column('question_type', sa.String(length=10), nullable=False, server_default='cbt'),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options_json', sa.Text()),
        sa.Column('correct_index', sa.Integer()),
        sa.Column('explanation', sa.Text()),
        sa.Column('mark_scheme', sa.Text()),
        sa.Column('is_active', sa.Boolean(), server_default=sa.true()),
        sa.Column('created_at', sa.DateTime()),
    )
    op.create_index('ix_cbt_questions_subject_code', 'cbt_questions', ['subject_code'])

    op.create_table(
        'cbt_attempts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('course_code', sa.String(length=20), nullable=False),
        sa.Column('question_type', sa.String(length=10), nullable=False),
        sa.Column('total_questions', sa.Integer(), nullable=False),
        sa.Column('correct_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('score_pct', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('duration_seconds', sa.Integer()),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('submitted_at', sa.DateTime()),
    )
    op.create_index('ix_cbt_attempts_course_code', 'cbt_attempts', ['course_code'])

    op.create_table(
        'cbt_answers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('attempt_id', sa.Integer(), sa.ForeignKey('cbt_attempts.id'), nullable=False),
        sa.Column('question_id', sa.Integer(), sa.ForeignKey('cbt_questions.id'), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('selected_index', sa.Integer()),
        sa.Column('written_answer', sa.Text()),
        sa.Column('is_correct', sa.Boolean()),
    )


def downgrade():
    op.drop_table('cbt_answers')
    op.drop_index('ix_cbt_attempts_course_code', table_name='cbt_attempts')
    op.drop_table('cbt_attempts')
    op.drop_index('ix_cbt_questions_subject_code', table_name='cbt_questions')
    op.drop_table('cbt_questions')
