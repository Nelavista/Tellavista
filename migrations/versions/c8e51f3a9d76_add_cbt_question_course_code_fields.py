"""Add course_code/topic/difficulty/source_note to cbt_questions

Revision ID: c8e51f3a9d76
Revises: a7f2c9e14b83
Create Date: 2026-09-12

CBTQuestion.subject_code was matched by 3-letter prefix only (e.g. "MTH"), so every
course sharing a prefix (MTH101, MTH205, MTH419, ...) drew from one shared bucket
instead of its own course-specific bank -- see app/services/cbt_bank.py, the new
single place that queries the course_code column added here. subject_code is left in
place (still populated, still returned by to_dict()) for backward compatibility; it's
no longer what selects a bank. topic/difficulty/source_note support the content
pipeline's per-question metadata and an internal audit trail of what grounded each
course's bank. All four columns are nullable/additive -- cbt_questions has zero rows in
production at the time of this migration, so there is no backfill to do.

Revises: a7f2c9e14b83
"""
from alembic import op
import sqlalchemy as sa

revision = 'c8e51f3a9d76'
down_revision = 'a7f2c9e14b83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cbt_questions', sa.Column('course_code', sa.String(length=20), nullable=True))
    op.add_column('cbt_questions', sa.Column('topic', sa.String(length=150), nullable=True))
    op.add_column('cbt_questions', sa.Column('difficulty', sa.String(length=10), nullable=True))
    op.add_column('cbt_questions', sa.Column('source_note', sa.Text(), nullable=True))
    op.create_index('ix_cbt_questions_course_code', 'cbt_questions', ['course_code'])


def downgrade():
    op.drop_index('ix_cbt_questions_course_code', table_name='cbt_questions')
    op.drop_column('cbt_questions', 'source_note')
    op.drop_column('cbt_questions', 'difficulty')
    op.drop_column('cbt_questions', 'topic')
    op.drop_column('cbt_questions', 'course_code')
