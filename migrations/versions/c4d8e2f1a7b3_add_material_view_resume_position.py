"""Add material_views.last_page -- the resume position PRD §5.3's "Continue learning"
acceptance criteria require ("returns to exact material + scroll/page position").

MaterialView previously stored only (user_id, material_id, viewed_at), so reopening a
material could return the student to the right *material* but never the right *page*.
`last_page` is nullable: NULL keeps its existing meaning of "opened, but no page position
ever recorded" (e.g. a non-PDF resource, or a viewer that couldn't report its position),
and must never be confused with page 1.

Purely additive -- no column is dropped, narrowed, or re-typed, so this can be deployed
before any code reads or writes the field.

Revision ID: c4d8e2f1a7b3
Revises: b3f7a91c4e28
Create Date: 2026-09-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c4d8e2f1a7b3'
down_revision = 'b3f7a91c4e28'
branch_labels = None
depends_on = None


def upgrade():
    # Unconstrained (no FK) -- direct ADD COLUMN is safe on both Postgres and SQLite.
    op.add_column('material_views', sa.Column('last_page', sa.Integer(), nullable=True))


def downgrade():
    # batch mode so the SQLite dialect (test suite) can drop the column; on Postgres
    # batch mode takes the direct ALTER PATH.
    with op.batch_alter_table('material_views', schema=None) as batch_op:
        batch_op.drop_column('last_page')
