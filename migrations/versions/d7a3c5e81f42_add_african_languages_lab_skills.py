"""Add African Languages Lab (ALL) skill support: programme/language/tag fields,
structured scored tasks + assessments on challenges, and the student language profile

Revision ID: d7a3c5e81f42
Revises: f1b2c3d4e5f6
Create Date: 2026-10-30

Everything is additive and nullable (or server-defaulted), so every existing Skill,
Challenge and ChallengeSubmission keeps behaving exactly as before:
- skill_categories.program groups categories into a programme hub ('all').
- skills.language / skills.tags_json power language-specific skills and catalog filters.
- challenges.task_spec_json / is_assessment / pass_score turn a challenge into an
  auto-scored practical task (services/language_task_service.py), and an assessment
  into one that must be passed, not just attempted.
- challenge_submissions.score / result_json store that deterministic score.
- student_languages + user.language_background are the self-reported language profile.
Content itself is seeded separately by scripts/seed/seed_all_skills.py.

Revises: f1b2c3d4e5f6
"""
from alembic import op
import sqlalchemy as sa

revision = 'd7a3c5e81f42'
down_revision = 'f1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('skill_categories', sa.Column('program', sa.String(length=30), nullable=True))
    op.create_index('ix_skill_categories_program', 'skill_categories', ['program'])

    op.add_column('skills', sa.Column('language', sa.String(length=40), nullable=True))
    op.add_column('skills', sa.Column('tags_json', sa.Text(), nullable=True))
    op.create_index('ix_skills_language', 'skills', ['language'])

    op.add_column('challenges', sa.Column('task_spec_json', sa.Text(), nullable=True))
    op.add_column('challenges', sa.Column('is_assessment', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('challenges', sa.Column('pass_score', sa.Integer(), nullable=True))

    op.add_column('challenge_submissions', sa.Column('score', sa.Integer(), nullable=True))
    op.add_column('challenge_submissions', sa.Column('result_json', sa.Text(), nullable=True))

    op.add_column('user', sa.Column('language_background', sa.Text(), nullable=True))

    op.create_table(
        'student_languages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('language', sa.String(length=40), nullable=False),
        sa.Column('dialect', sa.String(length=80), nullable=True),
        sa.Column('proficiency', sa.String(length=20), nullable=False, server_default='conversational'),
        sa.Column('can_speak', sa.Boolean(), nullable=True),
        sa.Column('can_read', sa.Boolean(), nullable=True),
        sa.Column('can_write', sa.Boolean(), nullable=True),
        sa.Column('can_transcribe', sa.Boolean(), nullable=True),
        sa.Column('can_translate', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('student_id', 'language', name='uq_student_language'),
    )
    op.create_index('ix_student_languages_student_id', 'student_languages', ['student_id'])


def downgrade():
    op.drop_index('ix_student_languages_student_id', table_name='student_languages')
    op.drop_table('student_languages')
    op.drop_column('user', 'language_background')
    op.drop_column('challenge_submissions', 'result_json')
    op.drop_column('challenge_submissions', 'score')
    op.drop_column('challenges', 'pass_score')
    op.drop_column('challenges', 'is_assessment')
    op.drop_column('challenges', 'task_spec_json')
    op.drop_index('ix_skills_language', table_name='skills')
    op.drop_column('skills', 'tags_json')
    op.drop_column('skills', 'language')
    op.drop_index('ix_skill_categories_program', table_name='skill_categories')
    op.drop_column('skill_categories', 'program')
