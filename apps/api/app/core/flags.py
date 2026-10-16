"""Server-side feature flags.

Anything half-built merges behind a flag so it can reach `develop`/`main`
without being visible in prod. A flag is enabled when ``FLAG_<NAME>`` is set to
1/true/yes/on. Flags are read from the environment per deployment — never guessed.

Usage::

    from app.core.flags import is_enabled
    if is_enabled("ledger"):
        ...
"""
from __future__ import annotations

import os

_TRUTHY = {"1", "true", "yes", "on"}


def is_enabled(name: str, default: bool = False) -> bool:
    """True when FLAG_<NAME> is truthy. Unset falls back to ``default``."""
    key = "FLAG_" + "".join(c if c.isalnum() else "_" for c in name.upper())
    raw = os.environ.get(key)
    if raw is None:
        return default
    return raw.strip().lower() in _TRUTHY


# Server-side flag names. Keep in sync with packages/config/src/flags.ts.
SKILLS_JOURNEY = "skills_journey"
MANAGED_WORKFORCE = "managed_workforce"
LEDGER = "ledger"
