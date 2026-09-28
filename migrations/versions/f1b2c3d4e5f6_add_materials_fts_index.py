"""Materials full-text search: expression GIN index (gap G7).

On Postgres, search over Materials moves from a sequential `ILIKE '%q%'` scan to a
real full-text query (websearch_to_tsquery against a weighted tsvector -- see
services/search_service.py). The index here is an *expression* index built on exactly
the weighted tsvector expression the service layer compiles into its match/rank
clauses (same functions, same weights, same coalesces, same order) -- Postgres'
expression-index matching works textually, so these queries resolve via the GIN
index with zero schema change to the materials table. Keeping the expression in the
service layer (not a stored column) means ORM behavior, to_dict(), and every other
reader of Material stay untouched.

SQLite (tests, dev) gets nothing -- it has no tsvector, and search_service degrades
to the original ILIKE filter there. The dialect check keeps this migration a no-op
on SQLite, same convention as the material_chunks migration.

Revision ID: f1b2c3d4e5f6
Revises: e6a7b8c9d0e1
Create Date: 2026-09-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'f1b2c3d4e5f6'
down_revision = 'e6a7b8c9d0e1'
branch_labels = None
depends_on = None

_INDEX_NAME = 'ix_materials_fts'

# Must stay byte-equivalent to search_service._material_tsvector() (the
# coalesce/weight order matters for the planner's expression matching).
_FTS_EXPRESSION = """
    setweight(to_tsvector('english', title), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(course_code, '')), 'C')
"""


def upgrade():
    bind = op.get_bind()
    if bind.dialect.name != 'postgresql':
        return

    # GIN over the weighted tsvector expression: title hits, description hits and
    # code hits all resolve via the index instead of scanning 100% of rows per
    # query. IMMEDIATE building is fine at today's material counts; if the table
    # ever grows past millions of rows, switch to CREATE INDEX CONCURRENTLY (needs
    # a non-transactional migration -- alembic op can't emit it directly).
    bind.execute(sa.text(
        f"CREATE INDEX IF NOT EXISTS {_INDEX_NAME} ON materials USING GIN (({_FTS_EXPRESSION}))"
    ))


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name != 'postgresql':
        return
    bind.execute(sa.text(f"DROP INDEX IF EXISTS {_INDEX_NAME}"))
