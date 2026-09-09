"""Add nullable university/faculty/department/course FKs to cbt_questions

Multi-university expansion, step 4. Every existing row stays NULL in all four columns --
NULL means "universal", shown to every school practicing this subject_code, identical to
today's behavior. This just gives a future admin/import the option to tag a question to
one school's own course numbering (see routes/cbt_routes.py's question-selection query)
without touching any existing CBT data.

Revision ID: b4d7fa0c25e1
Revises: a3c6e9b14d70
Create Date: 2026-09-06 00:00:00.000003

"""
from alembic import op
import sqlalchemy as sa

revision = 'b4d7fa0c25e1'
down_revision = 'a3c6e9b14d70'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cbt_questions', sa.Column('university_id', sa.Integer(), nullable=True))
    op.add_column('cbt_questions', sa.Column('faculty_id', sa.Integer(), nullable=True))
    op.add_column('cbt_questions', sa.Column('department_id', sa.Integer(), nullable=True))
    op.add_column('cbt_questions', sa.Column('course_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_cbt_questions_university_id', 'cbt_questions', 'universities', ['university_id'], ['id'])
    op.create_foreign_key('fk_cbt_questions_faculty_id', 'cbt_questions', 'faculties', ['faculty_id'], ['id'])
    op.create_foreign_key('fk_cbt_questions_department_id', 'cbt_questions', 'departments', ['department_id'], ['id'])
    op.create_foreign_key('fk_cbt_questions_course_id', 'cbt_questions', 'courses', ['course_id'], ['id'])
    op.create_index('ix_cbt_questions_university_id', 'cbt_questions', ['university_id'])


def downgrade():
    op.drop_index('ix_cbt_questions_university_id', table_name='cbt_questions')
    op.drop_constraint('fk_cbt_questions_course_id', 'cbt_questions', type_='foreignkey')
    op.drop_constraint('fk_cbt_questions_department_id', 'cbt_questions', type_='foreignkey')
    op.drop_constraint('fk_cbt_questions_faculty_id', 'cbt_questions', type_='foreignkey')
    op.drop_constraint('fk_cbt_questions_university_id', 'cbt_questions', type_='foreignkey')
    op.drop_column('cbt_questions', 'course_id')
    op.drop_column('cbt_questions', 'department_id')
    op.drop_column('cbt_questions', 'faculty_id')
    op.drop_column('cbt_questions', 'university_id')
