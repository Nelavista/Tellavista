"""Add 30-Day Skill Class system tables: assignments, grading config, cohorts,
employer profiles, and student privacy settings.

Revision ID: a2f5e8c1b7d3
Revises: d1f6b3c8e4a9
Create Date: 2026-08-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a2f5e8c1b7d3'
down_revision = 'd1f6b3c8e4a9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('instructions', sa.Text()),
        sa.Column('due_offset_hours', sa.Integer(), server_default='48'),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('lesson_id', name='uq_assignment_lesson'),
    )

    op.create_table(
        'assignment_submissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('assignment_id', sa.Integer(), sa.ForeignKey('assignments.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='submitted'),
        sa.Column('review_status', sa.String(length=20), server_default='pending'),
        sa.Column('score', sa.Integer()),
        sa.Column('feedback_json', sa.Text()),
        sa.Column('submitted_at', sa.DateTime()),
        sa.Column('first_submitted_at', sa.DateTime()),
    )

    op.create_table(
        'grade_scales',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('skill_courses.id'), nullable=False),
        sa.Column('grade_letter', sa.String(length=5), nullable=False),
        sa.Column('min_score', sa.Integer(), nullable=False),
        sa.Column('max_score', sa.Integer(), nullable=False),
        sa.Column('grade_point', sa.Float(), nullable=False),
        sa.Column('order', sa.Integer(), server_default='0'),
    )

    op.create_table(
        'grade_weights',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('skill_courses.id'), nullable=False),
        sa.Column('component', sa.String(length=30), nullable=False),
        sa.Column('weight_pct', sa.Integer(), nullable=False, server_default='0'),
        sa.UniqueConstraint('course_id', 'component', name='uq_course_grade_component'),
    )

    op.create_table(
        'cohorts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('skill_courses.id'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date()),
        sa.Column('is_active', sa.Boolean(), server_default=sa.true()),
        sa.Column('created_at', sa.DateTime()),
    )

    op.create_table(
        'cohort_enrollments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('cohort_id', sa.Integer(), sa.ForeignKey('cohorts.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('enrolled_at', sa.DateTime()),
        sa.Column('current_day', sa.Integer(), server_default='1'),
        sa.Column('skill_gpa', sa.Float()),
        sa.Column('gpa_updated_at', sa.DateTime()),
        sa.UniqueConstraint('cohort_id', 'student_id', name='uq_cohort_student'),
    )

    op.create_table(
        'employer_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('company_name', sa.String(length=150), nullable=False),
        sa.Column('company_description', sa.Text()),
        sa.Column('website', sa.String(length=300)),
        sa.Column('industry', sa.String(length=120)),
        sa.Column('logo_url', sa.String(length=500)),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('user_id', name='uq_employer_profile_user'),
    )

    op.create_table(
        'student_privacy_settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('profile_visibility', sa.String(length=20), nullable=False, server_default='private'),
        sa.Column('show_academic_cgpa', sa.Boolean(), server_default=sa.false()),
        sa.Column('show_projects', sa.Boolean(), server_default=sa.true()),
        sa.Column('show_skill_transcript', sa.Boolean(), server_default=sa.true()),
        sa.Column('updated_at', sa.DateTime()),
        sa.UniqueConstraint('student_id', name='uq_privacy_settings_student'),
    )


def downgrade():
    op.drop_table('student_privacy_settings')
    op.drop_table('employer_profiles')
    op.drop_table('cohort_enrollments')
    op.drop_table('cohorts')
    op.drop_table('grade_weights')
    op.drop_table('grade_scales')
    op.drop_table('assignment_submissions')
    op.drop_table('assignments')
