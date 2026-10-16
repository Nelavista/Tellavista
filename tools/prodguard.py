"""Prod guard for destructive scripts (ADR-0002).

Every seed / maintenance / admin / `--apply` entrypoint imports this and calls
``guard("<action>")`` before doing anything. It:

  1. prints the **masked** database target (password redacted),
  2. detects whether that target is production,
  3. refuses to continue unless the caller explicitly opted in.

Opt-in:
  * CLI flag:  ``--i-know-this-is-production``
  * or env:    ``PRODGUARD_ALLOW=1``

Detection: production if ``APP_ENV == "prod"`` **or** ``DATABASE_URL`` is a
non-SQLite URL whose host is not a local host.

Usage::

    from tools.prodguard import guard
    guard("seed_academia")
    # ... do the destructive thing ...

This module has no third-party dependencies on purpose: it must import in every
environment, including the V1 maintenance scripts.
"""
from __future__ import annotations

import os
import sys
from urllib.parse import urlparse

ALLOW_FLAG = "--i-know-this-is-production"
ALLOW_ENV = "PRODGUARD_ALLOW"

_LOCAL_HOSTS = {
    "localhost", "127.0.0.1", "::1", "0.0.0.0",
    "db", "postgres", "postgresql", "host.docker.internal",
}

REFUSAL = (
    "REFUSED: this script would run against a PRODUCTION database.\n"
    "  If you really mean it, re-run with {flag}  (or set {env}=1).\n"
    "  The target was shown above. Never do this casually."
)


def mask_database_url(database_url: str | None) -> str:
    """Return a printable target with the password removed. Never raises."""
    if not database_url:
        return "(unset -> local sqlite default)"
    if database_url.startswith("sqlite"):
        return database_url
    try:
        parts = urlparse(database_url)
    except Exception:
        return "(unparseable DATABASE_URL)"
    host = parts.hostname or "?"
    dbname = (parts.path or "/").lstrip("/") or "?"
    user = parts.username or "?"
    return f"{parts.scheme}://{user}:***@{host}:{parts.port or '?'}/{dbname}"


def is_production_target(database_url: str | None = None, app_env: str | None = None) -> bool:
    """True when the target looks like production. Conservative on ambiguity."""
    database_url = os.environ.get("DATABASE_URL", "") if database_url is None else database_url
    app_env = (app_env if app_env is not None else os.environ.get("APP_ENV", "")) or ""
    if app_env.strip().lower() in {"prod", "production"}:
        return True
    if not database_url:
        return False                      # unset -> local sqlite file
    if database_url.startswith("sqlite"):
        return False                      # local file
    try:
        host = (urlparse(database_url).hostname or "").lower()
    except Exception:
        return True                       # can't parse a non-sqlite URL -> treat as remote
    return host not in _LOCAL_HOSTS


def guard(action: str, argv: list[str] | None = None, *, database_url: str | None = None,
          app_env: str | None = None) -> None:
    """Enforce the prod guard. Raises SystemExit(3) when refused."""
    argv = list(sys.argv[1:] if argv is None else argv)
    target = mask_database_url(
        database_url if database_url is not None else os.environ.get("DATABASE_URL")
    )
    prod = is_production_target(database_url, app_env)
    allowed = ALLOW_FLAG in argv or os.environ.get(ALLOW_ENV) == "1"

    label = "PRODUCTION" if prod else "non-production"
    sys.stderr.write(f"[prodguard] {action}: target {target} ({label})\n")

    if prod and not allowed:
        sys.stderr.write(REFUSAL.format(flag=ALLOW_FLAG, env=ALLOW_ENV) + "\n")
        raise SystemExit(3)


if __name__ == "__main__":  # tiny self-test / inspection
    print("target:", mask_database_url(os.environ.get("DATABASE_URL")))
    print("production:", is_production_target())
