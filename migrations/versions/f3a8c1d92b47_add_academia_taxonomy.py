"""Add University/Faculty/Department/Course taxonomy tables.

Revision ID: f3a8c1d92b47
Revises: b9e4a7f2c6d8
Create Date: 2026-08-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'f3a8c1d92b47'
down_revision = 'b9e4a7f2c6d8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'universities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('short_name', sa.String(length=20)),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('name', name='uq_university_name'),
    )
    op.create_table(
        'faculties',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('university_id', sa.Integer(), sa.ForeignKey('universities.id'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('university_id', 'name', name='uq_faculty_university_name'),
    )
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('faculty_id', sa.Integer(), sa.ForeignKey('faculties.id'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('faculty_id', 'name', name='uq_department_faculty_name'),
    )
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('department_id', sa.Integer(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('level', sa.String(length=10), nullable=False),
        sa.Column('semester', sa.String(length=20), nullable=True),
        sa.Column('course_type', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('department_id', 'level', 'code', name='uq_course_dept_level_code'),
    )
    op.create_index('ix_courses_code', 'courses', ['code'])


def downgrade():
    op.drop_index('ix_courses_code', table_name='courses')
    op.drop_table('courses')
    op.drop_table('departments')
    op.drop_table('faculties')
    op.drop_table('universities')
