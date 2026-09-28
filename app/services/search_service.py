"""Full-text search across Materials (PRD §5.3, migration-map gap G7).

Postgres (the deploy target) gets a real websearch-style full-text query over a
weighted tsvector: title matches outrank description matches, and the English
dictionary folds word-form noise ("structures" matches "structure") that the old
`ILIKE '%q%'` scan could never do. pg_trgm/unaccent are available on the Render
Postgres instance (migration map Step 2) but this MVP deliberately ships without
them: `websearch_to_tsquery` already handles phrase/AND/OR natural queries, and the
migration's GIN index puts exact-word latency orders of magnitude under the old
sequential ILIKE scan. Trigram fuzzy/typo matching is a straight follow-up (add
pg_trgm GIN indexes, OR an ILIKE arm) without touching call sites.

SQLite (the test suite, and dev without DATABASE_URL) has no tsvector and no
portable websearch parser, so the same public functions degrade to the previous
OR-of-ILIKEs behavior. The dialect split lives here in one place -- exactly like
the embedding split in rag_service.py -- so routes stay dialect-blind.

Escaping note: the SQLite branch escapes LIKE metacharacters (\\ % _) with an
explicit ESCAPE clause, so a query like "50%" finds "50%" rather than every title
ending in "50".
"""
import sqlalchemy as sa

from app.extensions import db
from app.models import Material

# Query row limit stays the routes' concern; nothing here fetches -- everything
# returns a SQLAlchemy clause so existing pagination/scoping composes unchanged.


def _material_tsvector():
    """Weighted search vector: title (A) dominates, description (B) next, course code
    (C) so 'CSC213' hits hard but a bare code in a title still wins. Coalesce keeps
    NULLs from nulling the whole concatenation. This exact expression (same weights,
    same order, same functions) is what migration f1b2c3d4e5f6 builds the GIN index
    on, so these matches resolve via the index on Postgres -- change one, change both."""
    title = Material.title
    description = sa.func.coalesce(Material.description, '')
    course_code = sa.func.coalesce(Material.course_code, '')
    # tsvector concatenation is the '||' operator on Postgres (there is no '+'), and
    # the clause is only ever *compiled* on the Postgres branch -- on SQLite these
    # functions are constructed but never executed (see material_search_filter).
    return sa.func.setweight(sa.func.to_tsvector('english', title), 'A').op('||')(
        sa.func.setweight(sa.func.to_tsvector('english', description), 'B')
    ).op('||')(
        sa.func.setweight(sa.func.to_tsvector('english', course_code), 'C')
    )


def _sqlite_like_filter(q):
    """The pre-FTS behavior, kept byte-for-byte for SQLite: substring match on
    title/description/course_code, with LIKE metacharacters escaped."""
    safe = q.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    like = f'%{safe}%'
    return db.or_(*(
        col.ilike(like, escape='\\')
        for col in (Material.title, Material.description, Material.course_code)
    ))


def material_search_filter(q):
    """A SQLAlchemy filter clause matching Materials for the user query `q`. Dialect-
    aware; composes with the caller's existing scoping (department/university/approved)
    because it returns just the match clause."""
    if db.engine.dialect.name == 'postgresql':
        ts_query = sa.func.websearch_to_tsquery('english', q)
        return _material_tsvector().op('@@')(ts_query)
    return _sqlite_like_filter(q)


def material_search_rank(q):
    """A relevance ordering clause for the same query `q` (title weighted above
    description above course code), for callers that want matches ranked instead of
    purely recency-sorted. None on SQLite, where callers keep their existing
    created_at ordering -- rank without a tsvector isn't a thing."""
    if db.engine.dialect.name != 'postgresql':
        return None
    return sa.func.ts_rank(_material_tsvector(),
                           sa.func.websearch_to_tsquery('english', q)).label('rank')


def material_search_query(query, q):
    """Apply the match filter to an existing Material query. Kept as a helper so the
    two call sites (materials browse + academia search) can't drift apart."""
    return query.filter(material_search_filter(q))
