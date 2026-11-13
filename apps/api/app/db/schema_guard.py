"""Startup guard and free auto-migration.

Production used to rely on an explicit, reviewed ``alembic upgrade head``
(docs/runbooks/deploy-to-prod.md). When that step is skipped, the API boots and
the health check stays green, but the first query touching a new column fails
with ``column courses.semester does not exist`` — a 500 for every student on
that screen, discovered from logs rather than from the deploy.

Two pieces close that gap:

* :func:`upgrade_database` applies pending revisions at boot, serialised with a
  Postgres advisory lock. Render's pre-deploy command is a paid feature, so this
  is the free equivalent: a deploy either migrates or fails.
* :func:`check_schema` then refuses to serve if the database is still behind
  (``AUTO_MIGRATE=0``, or a migration that did not take effect).

The check is deliberately one-directional: migrations are expand-only, so a
*newer* database is safe for older code (that is what makes a code rollback
possible) and must not block one. Only a database that is *behind* the code is
fatal.
"""
from __future__ import annotations

import logging
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

_API_DIR = Path(__file__).resolve().parents[2]
_ALEMBIC_INI = _API_DIR / "alembic.ini"
_MIGRATIONS_DIR = _API_DIR / "migrations"

# Arbitrary but stable: every API/worker boot takes the same lock, so only one
# process runs DDL while the rest wait and then find the schema already current.
_MIGRATION_LOCK_KEY = 0x4E454C41  # "NELA"


class SchemaOutOfDate(RuntimeError):
    """The database is missing a migration this code depends on."""


def _alembic_config() -> Config:
    config = Config(str(_ALEMBIC_INI))
    config.set_main_option("script_location", str(_MIGRATIONS_DIR))
    # `migrations/env.py` reconfigures logging for the CLI; when invoked from a
    # running server that would disable uvicorn's loggers, so it opts out.
    config.attributes["skip_logging_config"] = True
    return config


def _script_directory() -> ScriptDirectory | None:
    if not _ALEMBIC_INI.is_file():
        return None
    return ScriptDirectory.from_config(_alembic_config())


def upgrade_database(engine: Engine, *, settings: Settings | None = None) -> None:
    """Apply pending migrations before serving traffic.

    Skipped locally (SQLite is built from the models) and when ``AUTO_MIGRATE``
    is off. Concurrent boots are serialised with a Postgres advisory lock; the
    waiting processes then see nothing to do. A failure propagates, so the deploy
    fails instead of running against a half-migrated database.
    """
    settings = settings or get_settings()
    if settings.is_local or not getattr(settings, "AUTO_MIGRATE", True):
        return
    if not _ALEMBIC_INI.is_file():
        logger.warning("Alembic config not found at %s; skipping auto-migration.", _ALEMBIC_INI)
        return

    config = _alembic_config()
    # Two connections: one holds the session-level advisory lock, the other runs
    # the DDL (Alembic must own a clean transaction on its connection).
    with engine.connect() as lock_conn:
        locked = engine.dialect.name == "postgresql"
        if locked:
            lock_conn.execute(text("SELECT pg_advisory_lock(:key)"), {"key": _MIGRATION_LOCK_KEY})
            lock_conn.commit()
        try:
            with engine.connect() as migration_conn:
                config.attributes["connection"] = migration_conn
                try:
                    logger.info("Applying database migrations (head).")
                    command.upgrade(config, "head")
                    logger.info("Database migrations are up to date.")
                finally:
                    config.attributes.pop("connection", None)
        finally:
            if locked:
                lock_conn.execute(
                    text("SELECT pg_advisory_unlock(:key)"), {"key": _MIGRATION_LOCK_KEY}
                )
                lock_conn.commit()


def head_revision() -> str | None:
    """The migration head this build expects, or ``None`` when unavailable."""
    script = _script_directory()
    if script is None:
        return None
    heads = script.get_heads()
    # CI enforces a single head; more than one is a merge that must be fixed
    # before anything is deployed, so this guard cannot pick one for you.
    return heads[0] if len(heads) == 1 else None


def current_revisions(engine: Engine) -> list[str]:
    """Revision rows recorded by Alembic. Empty if the table does not exist."""
    if not inspect(engine).has_table("alembic_version"):
        return []
    with engine.connect() as conn:
        return list(conn.execute(text("SELECT version_num FROM alembic_version")).scalars())


def _is_ancestor(script: ScriptDirectory, ancestor: str, descendant: str) -> bool | None:
    """Whether ``ancestor`` is in ``descendant``'s history.

    ``None`` means this build does not know ``descendant`` at all — a database
    migrated by a newer release. That is a code rollback, not drift, so it is
    allowed and only logged.
    """
    try:
        if script.get_revision(descendant) is None:
            return None
        return any(
            rev.revision == ancestor for rev in script.iterate_revisions(descendant, "base")
        )
    except Exception:  # noqa: BLE001 - an unknown revision is data, not a crash
        return None


def check_schema(engine: Engine, *, settings: Settings | None = None) -> None:
    """Raise :class:`SchemaOutOfDate` when the database is behind this build.

    Local runs are skipped: a developer's SQLite file can be created from the
    models directly and has no Alembic row. Anything that goes wrong while
    reading the version (database still starting, for example) is logged and
    ignored, because the health endpoint is intentionally dependency-light.
    """
    settings = settings or get_settings()
    if settings.is_local:
        return

    script = _script_directory()
    if script is None:
        logger.warning("Alembic config not found at %s; skipping the schema check.", _ALEMBIC_INI)
        return

    heads = script.get_heads()
    if len(heads) != 1:
        logger.critical(
            "Expected exactly one Alembic head, found %s (%s). Fix the migration chain.",
            len(heads),
            ", ".join(heads) or "none",
        )
        return
    head = heads[0]

    try:
        current = current_revisions(engine)
    except Exception:  # noqa: BLE001 - a database still starting must not crash boot
        logger.warning("Could not read alembic_version; skipping the schema check.", exc_info=True)
        return

    if not current:
        logger.warning(
            "No Alembic revision recorded; cannot verify the schema. Run `alembic upgrade head`."
        )
        return

    if head in current:
        return

    known = [_is_ancestor(script, head, revision) for revision in current]
    if any(known):
        # The database already contains this build's migration (a rollback).
        return
    if all(ancestor is None for ancestor in known):
        logger.warning(
            "Database revision %s is unknown to this build; assuming a code rollback.",
            ", ".join(current),
        )
        return

    raise SchemaOutOfDate(
        f"Database schema is at {', '.join(current)} but this build expects {head}. "
        "Run `alembic -c apps/api/alembic.ini upgrade head` before deploying."
    )
