"""Add User.bio, User.portfolio_url, User.profile_photo_url — power the "Profile
strength" checklist on the Skills dashboard.

Revision ID: f9b3e6c2a105
Revises: e7c4a19f3d82
Create Date: 2026-08-24 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'f9b3e6c2a105'
down_revision = 'e7c4a19f3d82'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('portfolio_url', sa.String(length=300), nullable=True))
        batch_op.add_column(sa.Column('profile_photo_url', sa.String(length=500), nullable=True))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('profile_photo_url')
        batch_op.drop_column('portfolio_url')
        batch_op.drop_column('bio')
