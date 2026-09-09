"""Store password-reset and email-verification tokens as SHA-256 hashes, not raw values

Revision ID: a7f2c9e14b83
Revises: b4d7fa0c25e1
Create Date: 2026-09-08

routes/auth_routes.py generated cryptographically random tokens (secrets.token_urlsafe)
but stored them on User.reset_token / User.email_verify_token in plaintext -- anyone who
could read a DB row (a backup, a replica, a compromised read-only credential) could use
that value directly as a working reset/verification link with no further work, exactly
like storing a password in plaintext. This migration replaces both columns with a hash
column (SHA-256 hex digest, 64 chars); the app now stores only the hash and re-hashes an
incoming token to compare, the same never-store-the-secret-itself pattern already used
for User.password_hash.

Any reset/verification link already in flight at deploy time is invalidated by this
migration (its old plaintext token no longer matches anything) -- acceptable given these
tokens are short-lived (30-60 minutes) and the user can simply request a new one.
"""
from alembic import op
import sqlalchemy as sa

revision = 'a7f2c9e14b83'
down_revision = 'b4d7fa0c25e1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_token_hash', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('email_verify_token_hash', sa.String(length=64), nullable=True))
        batch_op.create_index('ix_user_reset_token_hash', ['reset_token_hash'])
        batch_op.create_index('ix_user_email_verify_token_hash', ['email_verify_token_hash'])
        batch_op.drop_column('reset_token')
        batch_op.drop_column('email_verify_token')


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_token', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('email_verify_token', sa.String(length=200), nullable=True))
        batch_op.drop_index('ix_user_email_verify_token_hash')
        batch_op.drop_index('ix_user_reset_token_hash')
        batch_op.drop_column('email_verify_token_hash')
        batch_op.drop_column('reset_token_hash')
