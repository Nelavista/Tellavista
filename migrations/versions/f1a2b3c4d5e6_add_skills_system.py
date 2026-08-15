"""Add Skills system: catalog, learning paths, courses, lessons, quizzes,
challenges, projects, and student progress tracking.

Revision ID: f1a2b3c4d5e6
Revises: e5a2c74f9b31
Create Date: 2026-08-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'f1a2b3c4d5e6'
down_revision = 'e5a2c74f9b31'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'skill_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('icon', sa.String(length=10)),
        sa.Column('description', sa.String(length=300)),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('is_active', sa.Boolean(), server_default=sa.true()),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('slug', name='uq_skill_category_slug'),
    )

    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('skill_categories.id'), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('slug', sa.String(length=120), nullable=False),
        sa.Column('tagline', sa.String(length=200)),
        sa.Column('description', sa.Text()),
        sa.Column('level', sa.String(length=20), server_default='beginner'),
        sa.Column('icon', sa.String(length=10)),
        sa.Column('color', sa.String(length=20), server_default='#3b82f6'),
        sa.Column('estimated_hours', sa.Integer(), server_default='0'),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('slug', name='uq_skill_slug'),
    )

    op.create_table(
        'skill_courses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('level', sa.String(length=20), server_default='beginner'),
        sa.Column('estimated_hours', sa.Integer(), server_default='0'),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('skill_id', 'slug', name='uq_skill_course_slug'),
    )

    op.create_table(
        'course_modules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('skill_courses.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('order', sa.Integer(), server_default='0'),
    )

    op.create_table(
        'lessons',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('course_modules.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('content', sa.Text()),
        sa.Column('video_url', sa.String(length=500)),
        sa.Column('duration_minutes', sa.Integer(), server_default='10'),
        sa.Column('resources_json', sa.Text()),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime()),
    )

    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=False),
        sa.Column('title', sa.String(length=150), server_default='Check your understanding'),
        sa.Column('questions_json', sa.Text()),
        sa.UniqueConstraint('lesson_id', name='uq_quiz_lesson'),
    )

    op.create_table(
        'challenges',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('description', sa.String(length=300)),
        sa.Column('challenge_type', sa.String(length=20), server_default='coding'),
        sa.Column('difficulty', sa.String(length=20), server_default='beginner'),
        sa.Column('instructions', sa.Text()),
        sa.Column('estimated_minutes', sa.Integer(), server_default='30'),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('skill_id', 'slug', name='uq_challenge_slug'),
    )

    op.create_table(
        'project_templates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('skills_demonstrated_json', sa.Text()),
        sa.Column('difficulty', sa.String(length=20), server_default='beginner'),
        sa.Column('estimated_hours', sa.Integer(), server_default='0'),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('skill_id', 'slug', name='uq_project_template_slug'),
    )

    op.create_table(
        'learning_paths',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('skill_id', name='uq_learning_path_skill'),
    )

    op.create_table(
        'learning_path_steps',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('path_id', sa.Integer(), sa.ForeignKey('learning_paths.id'), nullable=False),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('step_type', sa.String(length=20), nullable=False, server_default='course'),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.String(length=300)),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('skill_courses.id'), nullable=True),
        sa.Column('challenge_id', sa.Integer(), sa.ForeignKey('challenges.id'), nullable=True),
        sa.Column('project_template_id', sa.Integer(), sa.ForeignKey('project_templates.id'), nullable=True),
    )

    op.create_table(
        'challenge_submissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('challenge_id', sa.Integer(), sa.ForeignKey('challenges.id'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='submitted'),
        sa.Column('created_at', sa.DateTime()),
    )

    op.create_table(
        'student_projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('project_template_id', sa.Integer(), sa.ForeignKey('project_templates.id'), nullable=True),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(length=20), server_default='in_progress'),
        sa.Column('progress_pct', sa.Integer(), server_default='0'),
        sa.Column('repo_url', sa.String(length=500)),
        sa.Column('live_url', sa.String(length=500)),
        sa.Column('skills_demonstrated_json', sa.Text()),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
    )

    op.create_table(
        'student_skills',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='in_progress'),
        sa.Column('progress_pct', sa.Integer(), server_default='0'),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('last_activity_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.UniqueConstraint('student_id', 'skill_id', name='uq_student_skill'),
    )

    op.create_table(
        'student_lesson_progress',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=False),
        sa.Column('completed_at', sa.DateTime()),
        sa.UniqueConstraint('student_id', 'lesson_id', name='uq_student_lesson'),
    )

    op.create_table(
        'student_quiz_attempts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('quiz_id', sa.Integer(), sa.ForeignKey('quizzes.id'), nullable=False),
        sa.Column('answers_json', sa.Text()),
        sa.Column('score', sa.Integer()),
        sa.Column('completed_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('student_quiz_attempts')
    op.drop_table('student_lesson_progress')
    op.drop_table('student_skills')
    op.drop_table('student_projects')
    op.drop_table('challenge_submissions')
    op.drop_table('learning_path_steps')
    op.drop_table('learning_paths')
    op.drop_table('project_templates')
    op.drop_table('challenges')
    op.drop_table('quizzes')
    op.drop_table('lessons')
    op.drop_table('course_modules')
    op.drop_table('skill_courses')
    op.drop_table('skills')
    op.drop_table('skill_categories')
