"""Add material_views table, Course.description, and Material's extracted-text cache
columns -- closes the loop between the academic taxonomy and real per-student progress/
AI-retrieval, where previously nothing tracked what a student had actually studied.

Revision ID: b6d94f0e2a17
Revises: a4e7f2c81d93
Create Date: 2026-08-21 00:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b6d94f0e2a17'
down_revision = 'a4e7f2c81d93'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'material_views',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('material_id', sa.Integer(), sa.ForeignKey('materials.id'), nullable=False),
        sa.Column('viewed_at', sa.DateTime()),
        sa.UniqueConstraint('user_id', 'material_id', name='uq_material_view_user_material'),
    )
    op.add_column('courses', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('materials', sa.Column('extracted_text', sa.Text(), nullable=True))
    op.add_column('materials', sa.Column('extracted_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('materials', 'extracted_at')
    op.drop_column('materials', 'extracted_text')
    op.drop_column('courses', 'description')
    op.drop_table('material_views')
