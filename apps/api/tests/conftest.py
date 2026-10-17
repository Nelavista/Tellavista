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

from app.db.base import Base  # noqa: E402
from app.seed.roles import seed_roles  # noqa: E402


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
