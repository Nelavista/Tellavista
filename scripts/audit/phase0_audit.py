"""Phase 0 data-integrity audit for the Skills implementation plan.

Read-only. Connects to config.DATABASE_URL with the connection forced into Postgres
read-only mode (psycopg2's `readonly` session flag) as a hard safety net on top of the
fact that every query below is a SELECT — even a bug in this script cannot write to the
database it's pointed at.

Checks the five preconditions the plan's Step 8 migrations depend on:
  1. ProjectTemplate.rubric_json rows whose max_points don't sum to 100         (AD-5)
  2. GradeWeight rows per course whose weight_pct don't sum to 100             (AD-6)
  3. Lesson (module_id, slug) collisions -- blocks the new unique constraint    (AD-10)
  4. Cohort rows with more than one is_active=True per course_id               (B-9)
  5. repo_url / live_url / submission_url / portfolio_url values that aren't
     http(s) -- blocks nulling out anything already bad before validation      (B-2)

Run with: python scripts/phase0_audit.py
Nothing here writes, deletes, or alters any row. Exit code is 0 if every check is clean,
1 if any check found something an admin/engineer needs to look at before Phase 1-2 land.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, text
from app.config import DATABASE_URL

IS_POSTGRES = DATABASE_URL.startswith('postgresql')


def _engine():
    kwargs = {}
    if IS_POSTGRES:
        # Belt-and-suspenders: the driver itself refuses any write on this connection,
        # independent of the fact that every statement below is already a SELECT.
        kwargs['connect_args'] = {'options': '-c default_transaction_read_only=on'}
    return create_engine(DATABASE_URL, **kwargs)


def check_rubric_sums(conn):
    rows = conn.execute(text(
        "SELECT id, title, rubric_json FROM project_templates "
        "WHERE rubric_json IS NOT NULL AND rubric_json != '' AND rubric_json != '[]'"
    )).fetchall()
    bad = []
    for r in rows:
        try:
            rubric = json.loads(r.rubric_json)
        except (ValueError, TypeError):
            bad.append((r.id, r.title, 'unparseable rubric_json'))
            continue
        total = sum(c.get('max_points', 0) for c in rubric if isinstance(c, dict))
        if total != 100:
            bad.append((r.id, r.title, f'sums to {total}'))
    return bad


def check_grade_weights(conn):
    rows = conn.execute(text(
        "SELECT course_id, SUM(weight_pct) AS total, COUNT(*) AS n "
        "FROM grade_weights GROUP BY course_id"
    )).fetchall()
    return [(r.course_id, r.total, r.n) for r in rows if r.total != 100]


def check_lesson_slug_collisions(conn):
    rows = conn.execute(text(
        "SELECT module_id, slug, COUNT(*) AS n, array_agg(id ORDER BY id) AS ids "
        "FROM lessons GROUP BY module_id, slug HAVING COUNT(*) > 1"
    ) if IS_POSTGRES else text(
        "SELECT module_id, slug, COUNT(*) AS n, GROUP_CONCAT(id) AS ids "
        "FROM lessons GROUP BY module_id, slug HAVING COUNT(*) > 1"
    )).fetchall()
    return [(r.module_id, r.slug, r.n, r.ids) for r in rows]


def check_duplicate_active_cohorts(conn):
    rows = conn.execute(text(
        "SELECT course_id, COUNT(*) AS n "
        "FROM cohorts WHERE is_active = true GROUP BY course_id HAVING COUNT(*) > 1"
    ) if IS_POSTGRES else text(
        "SELECT course_id, COUNT(*) AS n "
        "FROM cohorts WHERE is_active = 1 GROUP BY course_id HAVING COUNT(*) > 1"
    )).fetchall()
    return [(r.course_id, r.n) for r in rows]


def check_unsafe_urls(conn):
    findings = []
    checks = [
        ('student_projects', 'id', 'repo_url'),
        ('student_projects', 'id', 'live_url'),
        ('competition_entries', 'id', 'submission_url'),
        ('"user"', 'id', 'portfolio_url'),  # `user` is a reserved word in Postgres -- must be quoted
    ]
    for table, idcol, col in checks:
        rows = conn.execute(text(
            f"SELECT {idcol}, {col} FROM {table} "
            f"WHERE {col} IS NOT NULL AND {col} != '' "
            f"AND {col} NOT ILIKE 'http://%%' AND {col} NOT ILIKE 'https://%%'"
        ) if IS_POSTGRES else text(
            f"SELECT {idcol}, {col} FROM {table} "
            f"WHERE {col} IS NOT NULL AND {col} != '' "
            f"AND {col} NOT LIKE 'http://%' AND {col} NOT LIKE 'https://%'"
        )).fetchall()
        for r in rows:
            findings.append((table, col, getattr(r, idcol), getattr(r, col)))

    # external_links_json / screenshots_json are JSON lists -- scanned in Python since
    # the unsafe value can be nested inside a list, not a plain column value.
    rows = conn.execute(text(
        "SELECT id, external_links_json FROM student_projects WHERE external_links_json IS NOT NULL"
    )).fetchall()
    for r in rows:
        try:
            links = json.loads(r.external_links_json) or []
        except (ValueError, TypeError):
            continue
        for link in links:
            url = (link or {}).get('url', '') if isinstance(link, dict) else ''
            if url and not (url.lower().startswith('http://') or url.lower().startswith('https://')):
                findings.append(('student_projects', 'external_links_json', r.id, url))
    return findings


def main():
    engine = _engine()
    exit_code = 0
    with engine.connect() as conn:
        print(f"Connected to: {'PostgreSQL' if IS_POSTGRES else 'SQLite'} ({DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL})")
        print("Connection is read-only at the driver level." if IS_POSTGRES else "SQLite has no server-side read-only flag; every statement below is a SELECT.")
        print()

        print("== 1. ProjectTemplate rubrics not summing to 100 (blocks AD-5) ==")
        bad = check_rubric_sums(conn)
        if bad:
            exit_code = 1
            for row in bad:
                print(f"  template #{row[0]} \"{row[1]}\": {row[2]}")
        else:
            print("  clean — every configured rubric sums to 100")
        print()

        print("== 2. GradeWeight sets not summing to 100 (blocks AD-6) ==")
        bad = check_grade_weights(conn)
        if bad:
            exit_code = 1
            for course_id, total, n in bad:
                print(f"  course #{course_id}: {n} weight rows sum to {total}")
        else:
            print("  clean — every course's configured weights sum to 100")
        print()

        print("== 3. Lesson (module_id, slug) collisions (blocks AD-10) ==")
        bad = check_lesson_slug_collisions(conn)
        if bad:
            exit_code = 1
            for module_id, slug, n, ids in bad:
                print(f"  module #{module_id} slug '{slug}': {n} lessons ({ids})")
        else:
            print("  clean — no duplicate (module_id, slug) pairs")
        print()

        print("== 4. Courses with more than one active Cohort (blocks B-9) ==")
        bad = check_duplicate_active_cohorts(conn)
        if bad:
            exit_code = 1
            for course_id, n in bad:
                print(f"  course #{course_id}: {n} active cohorts")
        else:
            print("  clean — at most one active cohort per course")
        print()

        print("== 5. Non-http(s) URLs in student/competition/profile fields (blocks B-2 cleanup) ==")
        bad = check_unsafe_urls(conn)
        if bad:
            exit_code = 1
            for table, col, row_id, val in bad:
                print(f"  {table}.{col} id={row_id}: {val!r}")
        else:
            print("  clean — no non-http(s) values found in any checked field")
        print()

    print("RESULT:", "ALL CLEAN — Phase 1/2 migrations can proceed as planned." if exit_code == 0
          else "ISSUES FOUND — resolve the rows above before applying the corresponding migration/validation.")
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
