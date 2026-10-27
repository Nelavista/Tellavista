"""Startup configuration validation — the fail-fast contract (ADR-0002)."""
from __future__ import annotations

import pytest

from app.core.config import Settings


def test_local_gets_a_default_secret() -> None:
    s = Settings(_env_file=None, APP_ENV="local", DATABASE_URL="postgresql://u:p@localhost/db")
    assert s.SECRET_KEY  # local convenience default


def test_prod_requires_secret_key() -> None:
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        Settings(_env_file=None, APP_ENV="prod", DATABASE_URL="postgresql://u:p@host/db", SECRET_KEY="")


def test_dev_requires_secret_key() -> None:
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        Settings(_env_file=None, APP_ENV="dev", DATABASE_URL="postgresql://u:p@host/db", SECRET_KEY="")


def test_local_without_database_url_uses_sqlite() -> None:
    s = Settings(_env_file=None, APP_ENV="local", DATABASE_URL="", SECRET_KEY="x")
    assert s.DATABASE_URL.startswith("sqlite:///")
    assert s.DATABASE_URL.endswith("v2-local.db")


def test_dev_requires_database_url() -> None:
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        Settings(_env_file=None, APP_ENV="dev", DATABASE_URL="", SECRET_KEY="x")


def test_prod_requires_database_url() -> None:
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        Settings(_env_file=None, APP_ENV="prod", DATABASE_URL="", SECRET_KEY="x")


def test_wildcard_cors_rejected_outside_local() -> None:
    with pytest.raises(RuntimeError, match="CORS_ORIGINS"):
        Settings(
            _env_file=None,
            APP_ENV="prod",
            DATABASE_URL="postgresql://u:p@host/db",
            SECRET_KEY="x",
            CORS_ORIGINS="*",
        )


def test_cors_origins_parsed() -> None:
    s = Settings(
        _env_file=None,
        APP_ENV="local",
        DATABASE_URL="postgresql://u:p@localhost/db",
        SECRET_KEY="x",
        CORS_ORIGINS="http://localhost:5173, http://localhost:5174",
    )
    assert s.cors_origins == ["http://localhost:5173", "http://localhost:5174"]
