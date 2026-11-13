"""The startup schema guard: a skipped migration must fail the deploy, not every request."""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from app.db.schema_guard import (
    SchemaOutOfDate,
    check_schema,
    current_revisions,
    head_revision,
    upgrade_database,
)

PROD = SimpleNamespace(is_local=False, AUTO_MIGRATE=True)
LOCAL = SimpleNamespace(is_local=True, AUTO_MIGRATE=True)


def _engine(version: str | None, *, with_table: bool = True) -> Engine:
    engine = create_engine("sqlite://")
    with engine.begin() as conn:
        if with_table:
            conn.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"))
            if version is not None:
                conn.execute(text("INSERT INTO alembic_version VALUES (:v)"), {"v": version})
    return engine


def test_local_skips_the_check() -> None:
    # A developer's zero-config SQLite file is created from the models and has no
    # Alembic row; it must never block `make api-dev`.
    check_schema(_engine("20261022_1000"), settings=LOCAL)


def test_auto_migration_is_skipped_locally() -> None:
    upgrade_database(_engine(None, with_table=False), settings=LOCAL)


def test_auto_migration_can_be_disabled() -> None:
    # Once migrations are run by the platform, AUTO_MIGRATE=0 keeps boot read-only.
    settings = SimpleNamespace(is_local=False, AUTO_MIGRATE=False)
    upgrade_database(_engine(None, with_table=False), settings=settings)


def test_database_behind_the_code_fails_fast() -> None:
    """The production incident: code expects 1300, database is still at an earlier head."""
    with pytest.raises(SchemaOutOfDate, match="20261108_1300"):
        check_schema(_engine("20261022_1000"), settings=PROD)


def test_database_at_the_head_passes() -> None:
    head = head_revision()
    assert head is not None, "the repository must expose exactly one Alembic head"
    check_schema(_engine(head), settings=PROD)


def test_unknown_revision_is_treated_as_a_rollback() -> None:
    # A database migrated by a newer release (rollback) is expand-only safe.
    check_schema(_engine("20990101_0000"), settings=PROD)


def test_missing_version_table_only_warns() -> None:
    check_schema(_engine(None, with_table=False), settings=PROD)


def test_empty_version_table_only_warns() -> None:
    check_schema(_engine(None), settings=PROD)


def test_auto_migration_brings_an_empty_database_to_head(tmp_path) -> None:
    """The free replacement for a Render pre-deploy step: boot applies migrations."""
    url = f"sqlite:///{(tmp_path / 'boot.db').as_posix()}"
    engine = create_engine(url)
    settings = SimpleNamespace(is_local=False, AUTO_MIGRATE=True)

    upgrade_database(engine, settings=settings)

    head = head_revision()
    assert head is not None
    assert current_revisions(engine) == [head]
    check_schema(engine, settings=settings)

    course_columns = {column["name"] for column in inspect(engine).get_columns("courses")}
    assert {"semester", "course_type", "description", "source"} <= course_columns
