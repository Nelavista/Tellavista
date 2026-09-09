"""Add University.active/slug/location/logo_url -- multi-university expansion, step 1

Part of expanding Nelavista from LASU-only to a 10-university platform. `active` lets a
school be hidden from the student-facing picker without deleting its row (and everything
hanging off it). `slug` is a URL/localStorage-safe identifier, backfilled from `name`
here, used by the campus map's per-university localStorage key prefix. `location`/
`logo_url` are added nullable and left blank -- no fabricated city/state or logo data is
inserted; an admin fills these in later via /admin/academia with real, sourced values.

Revision ID: e1a4c7f92b58
Revises: b58e1c7f4a29
Create Date: 2026-09-06 00:00:00.000000

"""
import re

from alembic import op
import sqlalchemy as sa

revision = 'e1a4c7f92b58'
down_revision = 'b58e1c7f4a29'
branch_labels = None
depends_on = None


def _slugify(name):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return s or 'university'


def upgrade():
    op.add_column('universities', sa.Column('active', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('universities', sa.Column('slug', sa.String(length=160), nullable=True))
    op.add_column('universities', sa.Column('location', sa.String(length=150), nullable=True))
    op.add_column('universities', sa.Column('logo_url', sa.String(length=500), nullable=True))

    conn = op.get_bind()
    rows = conn.execute(sa.text('SELECT id, name FROM universities')).fetchall()
    seen = set()
    for uni_id, name in rows:
        base = _slugify(name)
        slug = base
        n = 2
        while slug in seen:
            slug = f'{base}-{n}'
            n += 1
        seen.add(slug)
        conn.execute(sa.text('UPDATE universities SET slug = :slug WHERE id = :id'), {'slug': slug, 'id': uni_id})

    op.create_unique_constraint('uq_universities_slug', 'universities', ['slug'])


def downgrade():
    op.drop_constraint('uq_universities_slug', 'universities', type_='unique')
    op.drop_column('universities', 'logo_url')
    op.drop_column('universities', 'location')
    op.drop_column('universities', 'slug')
    op.drop_column('universities', 'active')
