"""Phase 0 PR 0.1 — the migration itself: run it, reverse it, and check it agrees
with the models.

These run Alembic in a subprocess against a throwaway SQLite file. That executes
the real DDL in both directions (so a broken `downgrade` fails CI, not a
production rollback) and then compares the resulting schema with
`Base.metadata`, so migration and models cannot drift apart silently.

Postgres *execution* runs when `POSTGRES_TEST_URL` is set — the CI job starts a
service container and exports it, so the suite applies the real DDL to Postgres
and reverses it. Locally the Postgres dialect is still checked by compiling the
migration offline (`alembic upgrade head --sql`).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from app.db.base import Base
from app.models.admin import SEED_ROLES
from sqlalchemy import create_engine, inspect, text

API_ROOT = Path(__file__).resolve().parents[1]
POSTGRES_URL = "postgresql://ci:ci@localhost:5432/ci_offline"  # never connected to
# Set by ci-api.yml's `migrations-postgres` job; unset locally, where the suite
# skips the execution test rather than failing on a database that is not there.
POSTGRES_TEST_URL = os.environ.get("POSTGRES_TEST_URL")

# Added by 20261020_1000 (G1–G5). One row of policy, created on first read.
PLATFORM_TABLES = {"platform_settings"}
# Added by 20261018_0900 (F1/C8, F4/D1). The columns are nullable and expand-only.
TWO_FACTOR_COLUMNS = {"totp_secret", "totp_enabled_at", "totp_recovery_hashes"}
PUSH_TABLES = {"push_devices"}
# Added by 20261017_1300 (gold tasks). No new tables: two columns on submissions.
GOLD_TASK_COLUMNS = {"is_gold", "gold_expected"}
# Added by 20261017_1200 (Phase 7/8 extensions).
TALENT_EXTENSION_TABLES = {
    "user_languages",
    "user_availability",
    "talent_shares",
    "opportunity_applications",
    "practice_attempts",
    "practical_submissions",
    "ask_sessions",
    "ask_messages",
}
# Added by 20261017_1100 (engagement and ops).
ENGAGEMENT_OPS_TABLES = {
    "notifications",
    "messages",
    "import_runs",
    "campus_info",
    "university_waitlist",
}
# Added by 20261017_1000 (money).
LEDGER_TABLES = {
    "ledger_transactions",
    "ledger_entries",
    "earning_lines",
    "department_shares",
    "payout_batches",
    "payout_items",
    "exchange_rate_snapshots",
    "reconciliation_runs",
}
# Added by 20261017_0900 (quality).
QUALITY_TABLES = {
    "quality_standards",
    "quality_reviews",
    "quality_records",
    "quality_consequences",
}
# Added by 20261016_1800 (PR 0.6).
JOBS_TABLES = {"jobs"}
# Added by 20261016_1700 (PR 0.3b).
MATCHING_WORK_TABLES = {
    "opportunities",
    "requirements",
    "match_results",
    "skill_gaps",
    "projects",
    "cohorts",
    "cohort_members",
    "assignments",
    "submissions",
}
# Added by 20261016_1600 (PR 0.3a).
VERIFICATION_TABLES = {
    "verification_records",
    "verification_events",
    "assessments",
    "assessment_tasks",
    "assessment_attempts",
    "practical_tasks",
    "transcript_entries",
}
# Added by 20261016_1500 (PR 0.2b).
SKILLS_TABLES = {
    "skill_categories",
    "skills",
    "learning_paths",
    "lessons",
    "learning_path_steps",
    "task_templates",
    "lesson_progress",
}
# Added by 20261016_1400 (PR 0.2a).
ACADEMIA_TABLES = {
    "academic_sessions",
    "semesters",
    "enrolments",
    "topics",
    "material_chunks",
    "questions",
    "question_attempts",
}
# Added by 20261016_1300 (PR 0.1b).
CREDENTIAL_TABLES = {"refresh_tokens", "email_tokens", "consents", "idempotency_keys"}
# Added by 20261016_1200 (PR 0.1a).
IDENTITY_TABLES = {"roles", "user_profiles", "audit_logs"}
# Skeleton tables from 20261016_0000: present at every revision.
SKELETON_TABLES = {"users", "universities", "faculties", "departments", "courses", "materials"}


def _alembic(*args: str, db_url: str) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "NELAVISTA_SKIP_ENV_FILE": "1",
        "APP_ENV": "local",
        "DATABASE_URL": db_url,
        "SECRET_KEY": "test-secret-key-for-pytest-only",
        "CORS_ORIGINS": "http://localhost:5173",
    }
    return subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", *args],
        cwd=API_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def _sqlite_url(tmp_path: Path) -> str:
    return f"sqlite:///{(tmp_path / 'migration.db').as_posix()}"


def test_upgrade_downgrade_upgrade_round_trip(tmp_path: Path) -> None:
    url = _sqlite_url(tmp_path)
    engine = create_engine(url)

    up = _alembic("upgrade", "head", db_url=url)
    assert up.returncode == 0, up.stderr
    tables = set(inspect(engine).get_table_names())
    assert JOBS_TABLES <= tables and MATCHING_WORK_TABLES <= tables
    assert VERIFICATION_TABLES <= tables and SKILLS_TABLES <= tables
    assert ACADEMIA_TABLES <= tables and IDENTITY_TABLES <= tables
    assert CREDENTIAL_TABLES <= tables and QUALITY_TABLES <= tables
    assert LEDGER_TABLES <= tables and ENGAGEMENT_OPS_TABLES <= tables
    assert TALENT_EXTENSION_TABLES <= tables and PUSH_TABLES <= tables
    assert PLATFORM_TABLES <= tables
    user_columns = {c["name"] for c in inspect(engine).get_columns("users")}
    assert "role_id" in user_columns
    assert TWO_FACTOR_COLUMNS <= user_columns
    submission_columns = {c["name"] for c in inspect(engine).get_columns("submissions")}
    assert GOLD_TASK_COLUMNS <= submission_columns

    # 20261022_1000 is data-only: every fresh database must have the six roles,
    # not just the databases that ran the local seed.
    with engine.connect() as conn:
        seeded = {row[0] for row in conn.execute(text("SELECT code FROM roles"))}
    assert seeded == {code for code, _name, _is_staff in SEED_ROLES}

    # Walk back one revision at a time. Each downgrade must remove exactly its own
    # revision's tables and leave every earlier one in place (expand-only).
    # The seed revision is data-only, so unwind it first: it removes no tables.
    seed_down = _alembic("downgrade", "-1", db_url=url)
    assert seed_down.returncode == 0, seed_down.stderr
    assert PLATFORM_TABLES <= set(inspect(engine).get_table_names())

    for removed in (
        PLATFORM_TABLES,
        PUSH_TABLES,
        GOLD_TASK_COLUMNS,
        TALENT_EXTENSION_TABLES,
        ENGAGEMENT_OPS_TABLES,
        LEDGER_TABLES,
        QUALITY_TABLES,
        JOBS_TABLES,
        MATCHING_WORK_TABLES,
        VERIFICATION_TABLES,
        SKILLS_TABLES,
        ACADEMIA_TABLES,
        CREDENTIAL_TABLES,
        IDENTITY_TABLES,
    ):
        down = _alembic("downgrade", "-1", db_url=url)
        assert down.returncode == 0, down.stderr
        tables = set(inspect(engine).get_table_names())
        if removed is PUSH_TABLES:
            # 20261018_0900 also adds the 2FA columns; its downgrade removes both.
            assert removed.isdisjoint(tables), f"downgrade left {removed & tables} behind"
            assert TWO_FACTOR_COLUMNS.isdisjoint(
                {c["name"] for c in inspect(engine).get_columns("users")}
            )
        elif removed is GOLD_TASK_COLUMNS:
            # 1300 only adds columns; its downgrade removes those.
            assert removed.isdisjoint(
                {c["name"] for c in inspect(engine).get_columns("submissions")}
            )
        else:
            assert removed.isdisjoint(tables), f"downgrade left {removed & tables} behind"
        assert SKELETON_TABLES <= tables

    assert "role_id" not in {c["name"] for c in inspect(engine).get_columns("users")}
    assert TWO_FACTOR_COLUMNS.isdisjoint(
        {c["name"] for c in inspect(engine).get_columns("users")}
    )

    again = _alembic("upgrade", "head", db_url=url)
    assert again.returncode == 0, again.stderr
    tables = set(inspect(engine).get_table_names())
    assert JOBS_TABLES <= tables and MATCHING_WORK_TABLES <= tables
    assert ACADEMIA_TABLES <= tables and CREDENTIAL_TABLES <= tables
    with engine.connect() as conn:
        seeded = {row[0] for row in conn.execute(text("SELECT code FROM roles"))}
    assert seeded == {code for code, _name, _is_staff in SEED_ROLES}


def test_single_head() -> None:
    proc = _alembic("heads", db_url=POSTGRES_URL)
    assert proc.returncode == 0, proc.stderr
    heads = [line for line in proc.stdout.splitlines() if line.strip()]
    assert len(heads) == 1, f"expected exactly one Alembic head, got: {heads}"


def test_migrated_schema_matches_the_models(tmp_path: Path) -> None:
    url = _sqlite_url(tmp_path)
    proc = _alembic("upgrade", "head", db_url=url)
    assert proc.returncode == 0, proc.stderr

    inspector = inspect(create_engine(url))
    db_tables = set(inspector.get_table_names()) - {"alembic_version"}
    assert db_tables == set(Base.metadata.tables), "migration and models define different tables"

    for table in sorted(Base.metadata.tables):
        db_columns = {c["name"]: bool(c["nullable"]) for c in inspector.get_columns(table)}
        model_columns = {c.name: bool(c.nullable) for c in Base.metadata.tables[table].columns}
        assert db_columns == model_columns, f"{table}: columns/nullability differ from the models"


def test_postgres_ddl_compiles(tmp_path: Path) -> None:
    """Offline compile against the Postgres dialect: no connection is made."""
    proc = _alembic("upgrade", "head", "--sql", db_url=POSTGRES_URL)
    assert proc.returncode == 0, proc.stderr
    ddl = proc.stdout.upper()
    assert "CREATE TABLE ROLES" in ddl
    assert "CREATE TABLE IDEMPOTENCY_KEYS" in ddl
    assert "CREATE TABLE ENROLMENTS" in ddl
    assert "CREATE TABLE TASK_TEMPLATES" in ddl
    assert "CREATE TABLE VERIFICATION_EVENTS" in ddl
    assert "CREATE TABLE SUBMISSIONS" in ddl
    assert "CREATE TABLE JOBS" in ddl
    assert "CREATE TABLE PLATFORM_SETTINGS" in ddl
    assert "JSONB" in ddl, "JSON payload columns must be JSONB on Postgres"
    assert "SET NOT NULL" in ddl, "the timestamp tightening must reach Postgres"


@pytest.mark.skipif(
    not POSTGRES_TEST_URL, reason="POSTGRES_TEST_URL is unset; CI's service container sets it"
)
def test_migrations_execute_on_postgres() -> None:
    """Apply the real DDL to Postgres, reverse it, and apply it again (F2).

    SQLite's round trip cannot catch a Postgres-only failure — a bad JSONB
    default, an index on an expression, a constraint name that is too long. This
    runs the same migrations against the database production actually uses.
    """
    assert POSTGRES_TEST_URL is not None
    engine = create_engine(POSTGRES_TEST_URL)
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()

    up = _alembic("upgrade", "head", db_url=POSTGRES_TEST_URL)
    assert up.returncode == 0, up.stderr
    tables = set(inspect(engine).get_table_names())
    assert JOBS_TABLES <= tables and MATCHING_WORK_TABLES <= tables
    assert LEDGER_TABLES <= tables and PUSH_TABLES <= tables
    assert PLATFORM_TABLES <= tables
    user_columns = {c["name"] for c in inspect(engine).get_columns("users")}
    assert TWO_FACTOR_COLUMNS <= user_columns

    down = _alembic("downgrade", "base", db_url=POSTGRES_TEST_URL)
    assert down.returncode == 0, down.stderr
    remaining = set(inspect(engine).get_table_names()) - {"alembic_version"}
    assert remaining == set(), f"downgrade to base left {remaining} behind"

    again = _alembic("upgrade", "head", db_url=POSTGRES_TEST_URL)
    assert again.returncode == 0, again.stderr
    assert PUSH_TABLES <= set(inspect(engine).get_table_names())


def test_revision_chain_is_linked() -> None:
    """History must show the new revision on top of the skeleton one."""
    proc = _alembic("history", db_url=POSTGRES_URL)
    assert proc.returncode == 0, proc.stderr
    assert all(
        revision in proc.stdout
        for revision in (
            "20261022_1000",
            "20261020_1000",
            "20261018_0900",
            "20261016_1800",
            "20261016_1700",
            "20261016_1600",
            "20261016_1500",
            "20261016_1400",
            "20261016_1300",
            "20261016_1200",
            "20261016_0000",
        )
    )
