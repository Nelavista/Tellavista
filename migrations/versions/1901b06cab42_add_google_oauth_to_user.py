"""Add Google sign-in support to User: password_hash becomes nullable (a Google-only
account never sets one -- see models.py's check_password()) and a new unique google_sub
column stores the Google account's stable OIDC "sub" claim, used to recognize a returning
Google sign-in and to link onto an existing password account with a matching, Google-
verified email (see routes/auth_routes.py).

Revision ID: 1901b06cab42
Revises: e2f7c5b830a4
Create Date: 2026-08-25 00:00:00.000004

"""
from alembic import op
import sqlalchemy as sa

revision = '1901b06cab42'
down_revision = 'e2f7c5b830a4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash', existing_type=sa.String(200), nullable=True)
        batch_op.add_column(sa.Column('google_sub', sa.String(64), nullable=True))
        batch_op.create_unique_constraint('uq_user_google_sub', ['google_sub'])
        batch_op.create_index('ix_user_google_sub', ['google_sub'])


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_google_sub')
        batch_op.drop_constraint('uq_user_google_sub', type_='unique')
        batch_op.drop_column('google_sub')
        batch_op.alter_column('password_hash', existing_type=sa.String(200), nullable=False)
