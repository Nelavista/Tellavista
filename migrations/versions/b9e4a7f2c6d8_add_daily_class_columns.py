"""Add columns for the 30-Day Skill Class system to existing tables: User (employer flag,
self-reported academic CGPA), SkillCourse (daily-class flag), Lesson (day/week sequencing),
ProjectTemplate (final-project rubric), StudentProject (rubric evaluation results).

Revision ID: b9e4a7f2c6d8
Revises: a2f5e8c1b7d3
Create Date: 2026-08-14 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'b9e4a7f2c6d8'
down_revision = 'a2f5e8c1b7d3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_employer', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('academic_cgpa', sa.Float(), nullable=True))

    with op.batch_alter_table('skill_courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_daily_class', sa.Boolean(), server_default=sa.false()))
        batch_op.add_column(sa.Column('duration_days', sa.Integer(), nullable=True))

    with op.batch_alter_table('lessons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('day_number', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('week_number', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('week_title', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('learning_objective', sa.String(length=300), nullable=True))

    with op.batch_alter_table('project_templates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.Integer(), sa.ForeignKey('skill_courses.id'), nullable=True))
        batch_op.add_column(sa.Column('is_final_project', sa.Boolean(), server_default=sa.false()))
        batch_op.add_column(sa.Column('rubric_json', sa.Text(), nullable=True))

    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rubric_scores_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('ai_overall_score', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.drop_column('ai_overall_score')
        batch_op.drop_column('rubric_scores_json')

    with op.batch_alter_table('project_templates', schema=None) as batch_op:
        batch_op.drop_column('rubric_json')
        batch_op.drop_column('is_final_project')
        batch_op.drop_column('course_id')

    with op.batch_alter_table('lessons', schema=None) as batch_op:
        batch_op.drop_column('learning_objective')
        batch_op.drop_column('week_title')
        batch_op.drop_column('week_number')
        batch_op.drop_column('day_number')

    with op.batch_alter_table('skill_courses', schema=None) as batch_op:
        batch_op.drop_column('duration_days')
        batch_op.drop_column('is_daily_class')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('academic_cgpa')
        batch_op.drop_column('is_employer')
