"""Timezone-safe time helpers.

SQLAlchemy's SQLite dialect returns naive datetimes even for timezone-aware
columns, while Postgres returns aware ones. Comparing the two raises
``TypeError: can't compare offset-naive and offset-aware datetimes`` — a bug that
only shows up in tests using SQLite. Every comparison in a service goes through
``as_utc`` so behaviour is identical on both databases.
"""
from __future__ import annotations

from datetime import UTC, datetime


def utcnow() -> datetime:
    return datetime.now(UTC)


def as_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo else value.replace(tzinfo=UTC)


def is_due(value: datetime | None, *, now: datetime | None = None) -> bool:
    """True when ``value`` is at or before now. A missing value is never due."""
    moment = as_utc(value)
    if moment is None:
        return False
    return moment <= (now or utcnow())
