"""web push subscriptions

Revision ID: 20261121_1200
Revises: 20261119_1200
Create Date: 2026-11-21

Browsers do not mint a provider token the way APNs and FCM do. A browser install
is addressed by its Service Worker PushSubscription: an endpoint URL plus the two
keys needed to encrypt a payload. The endpoint goes in `token` (it is the unique
address, exactly like a native token), and `subscription` keeps the whole object
so the delivery job does not have to rebuild it.

`token` widens to 512 because a subscription endpoint is a URL and some push
services produce ones longer than the 255 a native token needed. `subscription`
is nullable: every existing row is a native install and must keep working
unchanged.

Safe on SQLite and Postgres: one nullable column add plus one length change, done
through batch mode so SQLite can recreate the table.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261121_1200"
down_revision: str | None = "20261119_1200"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("push_devices") as batch:
        batch.add_column(sa.Column("subscription", sa.JSON(), nullable=True))
        batch.alter_column(
            "token", existing_type=sa.String(length=255), type_=sa.String(length=512)
        )


def downgrade() -> None:
    # A web subscription endpoint may not fit in 255; dropping push rows for web
    # installs is better than truncating an address, because a truncated endpoint
    # delivers to nobody and can never be recovered by the client.
    op.execute("DELETE FROM push_devices WHERE platform = 'web'")
    with op.batch_alter_table("push_devices") as batch:
        batch.alter_column(
            "token", existing_type=sa.String(length=512), type_=sa.String(length=255)
        )
        batch.drop_column("subscription")
