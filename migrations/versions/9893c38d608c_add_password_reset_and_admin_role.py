"""Add password reset token fields and is_admin role to User

Revision ID: 9893c38d608c
Revises: 9e8af5c916ea
Create Date: 2026-07-31

routes/auth_routes.py's forgot-password/reset-password flow has always read and written
User.reset_token / User.reset_token_expiry, but those columns never existed on the model —
every reset attempt failed at db.session.commit(). This migration adds them.

It also adds User.is_admin to replace two separate, inconsistent hardcoded admin checks that
had grown up independently: routes/video_routes.py used `username == 'admin'`, while
routes/materials_routes.py used `user_level >= 5` (set via the standalone make_admin.py script).
Both are backfilled into the new is_admin column so no existing admin loses access.
"""
from alembic import op
import sqlalchemy as sa


revision = '9893c38d608c'
down_revision = '9e8af5c916ea'
branch_labels = None
depends_on = None


def upgrade():
    # Plain ADD COLUMN (not batch_alter_table/table-recreate) — these are simple additive
    # changes SQLite supports directly, and batch mode's reflect-and-recreate path hits a
    # known Alembic/SQLAlchemy circular-dependency bug on tables with many columns.
    op.add_column('user', sa.Column('reset_token', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('reset_token_expiry', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()))

    # Backfill both of the old ad-hoc admin checks so no existing admin loses access.
    op.execute("UPDATE \"user\" SET is_admin = true WHERE username = 'admin'")

    # user_level is declared as db.Integer in models.py but is ACTUALLY a VARCHAR column in
    # production with real dirty data in it (seen live: '5', '1', '200 Level', NULL — that
    # last one looks like an academic-level value that landed in the wrong column). A blind
    # CAST(user_level AS INTEGER) is fine on SQLite (it just returns 0 for non-numeric input)
    # but PostgreSQL raises InvalidTextRepresentation and rolls back the whole migration. Guard
    # it with a regex check on Postgres so only genuinely-numeric values ever reach the cast —
    # a CASE expression's branches are evaluated lazily, unlike a plain AND in a WHERE clause,
    # so this is safe regardless of query-plan evaluation order.
    if op.get_bind().dialect.name == 'postgresql':
        op.execute(
            "UPDATE \"user\" SET is_admin = true WHERE "
            "CASE WHEN user_level ~ '^[0-9]+$' THEN CAST(user_level AS INTEGER) >= 5 ELSE FALSE END"
        )
    else:
        op.execute("UPDATE \"user\" SET is_admin = true WHERE CAST(user_level AS INTEGER) >= 5")


def downgrade():
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'reset_token_expiry')
    op.drop_column('user', 'reset_token')
