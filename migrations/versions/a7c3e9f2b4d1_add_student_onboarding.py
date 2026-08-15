"""Add student_onboarding — first-visit Skills questionnaire responses.

Revision ID: a7c3e9f2b4d1
Revises: f1a2b3c4d5e6
Create Date: 2026-08-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a7c3e9f2b4d1'
down_revision = 'f1a2b3c4d5e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'student_onboarding',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('interest_text', sa.String(length=200), nullable=False),
        sa.Column('interested_skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=True),
        sa.Column('experience_level', sa.String(length=20), nullable=False),
        sa.Column('goal', sa.String(length=30)),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('student_id', name='uq_student_onboarding_student'),
    )


def downgrade():
    op.drop_table('student_onboarding')
