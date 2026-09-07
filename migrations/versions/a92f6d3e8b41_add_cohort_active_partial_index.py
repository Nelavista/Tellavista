"""Add partial unique index: at most one active Cohort per course

get_or_create_active_cohort() (services/daily_class_service.py) has a check-then-insert
with no isolation of its own. Two students triggering the very first enrollment in a
freshly-published daily class near-simultaneously (realistic at a launch/marketing push)
can each create a distinct "cohort" row for the same course before either commits. This
doesn't crash -- it silently forks the leaderboard: get_cohort_rank()
(services/gpa_service.py) only ever ranks within one cohort, so exactly the students who
started closest together end up split across two rosters, which is the one thing Cohort
exists to prevent (see its own docstring in models.py).

Partial, not a plain unique constraint on course_id, because a course legitimately
accumulates many past (closed, is_active=False) cohorts over time -- only "more than one
CURRENTLY ACTIVE at once" is the bug this closes.

IMPORTANT -- read before running against production: if any course already has more than
one is_active=True cohort, `upgrade()` below will fail with a unique-violation error.
This migration deliberately does not decide which of the two to deactivate -- that's a
judgment call (which one has real enrollments, which one is the accidental duplicate),
not something to automate. Run this diagnostic query against the production database
FIRST (also run by scripts/phase0_audit.py, check #4):

    SELECT course_id, COUNT(*)
    FROM cohorts
    WHERE is_active = true
    GROUP BY course_id
    HAVING COUNT(*) > 1;

If it returns zero rows, this migration is safe to run as-is. Confirmed clean against
production on 2026-09-05 (Phase 0 of the Skills implementation plan) -- re-run the query
above before applying if any time has passed since.

Revision ID: a92f6d3e8b41
Revises: e6b4c8f21a07
Create Date: 2026-09-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a92f6d3e8b41'
down_revision = 'e6b4c8f21a07'
branch_labels = None
depends_on = None


def upgrade():
    # Both dialect-specific `where` kwargs are always passed -- SQLAlchemy's DDL compiler
    # only emits the one matching whatever dialect is actually connected (matches the
    # Cohort model's own Index() definition in models.py).
    op.create_index(
        'uq_cohort_active_per_course', 'cohorts', ['course_id'], unique=True,
        postgresql_where=sa.text('is_active = true'),
        sqlite_where=sa.text('is_active = 1'),
    )


def downgrade():
    op.drop_index('uq_cohort_active_per_course', table_name='cohorts')
