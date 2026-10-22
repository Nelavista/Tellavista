"""Test environment for apps/api.

Sets safe defaults BEFORE importing the app, and tells settings not to read a
developer's local .env file. CI sets these too; this keeps bare `pytest` working.

Also provides the `db` fixture: an in-memory SQLite schema built from the models
with roles seeded. Tests that assert on real DDL use `test_migrations.py`
instead; this one is for model-level rules and constraints.
"""
from __future__ import annotations

import os
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

# apps/api on the path so `import app` resolves to this package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("NELAVISTA_SKIP_ENV_FILE", "1")
os.environ.setdefault("APP_ENV", "local")
os.environ.setdefault("DATABASE_URL", "postgresql://nelavista:nelavista@localhost:5432/nelavista_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")

import pytest  # noqa: E402
from sqlalchemy import create_engine, event  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.seed.roles import seed_roles  # noqa: E402

if TYPE_CHECKING:  # the client is only named in fixture annotations
    from fastapi.testclient import TestClient


@pytest.fixture()
def db() -> Iterator[Session]:
    """A fresh in-memory database per test, with reference data and FK enforcement."""
    engine = create_engine("sqlite://")  # in-memory

    # SQLite ignores foreign keys unless asked: without this, ON DELETE CASCADE /
    # SET NULL look like they work and the tests prove nothing.
    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _record) -> None:  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_roles(session)
        yield session
        session.rollback()


@pytest.fixture()
def api(monkeypatch) -> Iterator[tuple[TestClient, Session]]:
    """A TestClient wired to an in-memory database, with every feature flag on.

    A shared connection (`StaticPool` + `check_same_thread=False`) is required
    because FastAPI runs sync endpoints in a worker thread while the test builds
    its rows on the main one. Each test gets a fresh database and its own env.
    """
    from fastapi.testclient import TestClient

    from app.api.deps import get_current_user  # noqa: F401  (import for side effects)
    from app.db.session import get_db
    from app.main import app as fastapi_app

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _record) -> None:  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    session = Session(engine, expire_on_commit=False)
    seed_roles(session)

    for name in (
        "SKILLS_JOURNEY",
        "MANAGED_WORKFORCE",
        "LEDGER",
        "ACADEMIA_CONNECT",
        "TALENT_PROFILE",
        "EXTERNAL_OPPORTUNITIES",
    ):
        monkeypatch.setenv(f"FLAG_{name}", "1")

    def _override() -> Iterator[Session]:
        yield session

    fastapi_app.dependency_overrides[get_db] = _override
    try:
        with TestClient(fastapi_app) as client:
            yield client, session
    finally:
        fastapi_app.dependency_overrides.clear()
        session.close()


@pytest.fixture()
def api_no_flags(monkeypatch) -> Iterator[TestClient]:
    """A client with every V2 feature flag off, to prove the routes disappear."""
    from fastapi.testclient import TestClient

    from app.db.session import get_db
    from app.main import app as fastapi_app

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    seed_roles(session)

    for name in (
        "SKILLS_JOURNEY",
        "MANAGED_WORKFORCE",
        "LEDGER",
        "ACADEMIA_CONNECT",
        "TALENT_PROFILE",
        "EXTERNAL_OPPORTUNITIES",
    ):
        monkeypatch.delenv(f"FLAG_{name}", raising=False)

    def _override() -> Iterator[Session]:
        yield session

    fastapi_app.dependency_overrides[get_db] = _override
    try:
        with TestClient(fastapi_app) as client:
            yield client
    finally:
        fastapi_app.dependency_overrides.clear()
        session.close()
