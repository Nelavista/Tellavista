"""Phase 0 PR 0.1 — the migration itself: run it, reverse it, and check it agrees
with the models.

These run Alembic in a subprocess against a throwaway SQLite file. That executes
the real DDL in both directions (so a broken `downgrade` fails CI, not a
production rollback) and then compares the resulting schema with
`Base.metadata`, so migration and models cannot drift apart silently.

Postgres *execution* arrives with the CI service container in PR 0.14; until
then the Postgres dialect is checked by compiling the migration offline
(`alembic upgrade head --sql`), which catches dialect-specific DDL errors.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect

from app.db.base import Base

API_ROOT = Path(__file__).resolve().parents[1]
POSTGRES_URL = "postgresql://ci:ci@localhost:5432/ci_offline"  # never connected to

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
    assert ACADEMIA_TABLES <= tables and IDENTITY_TABLES <= tables and CREDENTIAL_TABLES <= tables
    assert "role_id" in {c["name"] for c in inspect(engine).get_columns("users")}

    # Walk back one revision at a time. Each downgrade must remove exactly its own
    # revision's tables and leave every earlier one in place (expand-only).
    for removed in (ACADEMIA_TABLES, CREDENTIAL_TABLES, IDENTITY_TABLES):
        down = _alembic("downgrade", "-1", db_url=url)
        assert down.returncode == 0, down.stderr
        tables = set(inspect(engine).get_table_names())
        assert removed.isdisjoint(tables), f"downgrade left {removed & tables} behind"
        assert SKELETON_TABLES <= tables

    assert "role_id" not in {c["name"] for c in inspect(engine).get_columns("users")}

    again = _alembic("upgrade", "head", db_url=url)
    assert again.returncode == 0, again.stderr
    tables = set(inspect(engine).get_table_names())
    assert ACADEMIA_TABLES <= tables and CREDENTIAL_TABLES <= tables


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
    assert "JSONB" in ddl, "JSON payload columns must be JSONB on Postgres"
    assert "SET NOT NULL" in ddl, "the timestamp tightening must reach Postgres"


def test_revision_chain_is_linked() -> None:
    """History must show the new revision on top of the skeleton one."""
    proc = _alembic("history", db_url=POSTGRES_URL)
    assert proc.returncode == 0, proc.stderr
    assert all(
        revision in proc.stdout
        for revision in ("20261016_1400", "20261016_1300", "20261016_1200", "20261016_0000")
    )
