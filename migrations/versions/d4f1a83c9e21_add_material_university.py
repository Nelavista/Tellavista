"""Add Material.university for per-institution content scoping

Revision ID: d4f1a83c9e21
Revises: c3e9f21a6b58
Create Date: 2026-08-06 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'd4f1a83c9e21'
down_revision = 'c3e9f21a6b58'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.add_column(sa.Column('university', sa.String(length=150), nullable=True))


def downgrade():
    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.drop_column('university')
