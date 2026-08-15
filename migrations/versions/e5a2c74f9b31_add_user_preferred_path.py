"""Add User.preferred_path for Academia / Tech & Skills path selection

Revision ID: e5a2c74f9b31
Revises: d4f1a83c9e21
Create Date: 2026-08-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'e5a2c74f9b31'
down_revision = 'd4f1a83c9e21'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preferred_path', sa.String(length=20), nullable=True))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('preferred_path')
