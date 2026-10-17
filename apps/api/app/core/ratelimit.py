"""Fixed-window rate limiting (ADR-0009: per-user and per-IP on auth routes).

In-process by design for Phase 0: one process, one counter, no infrastructure.
The interface (`check`) is what the routes depend on, so swapping the store for
Redis when the API runs more than one instance is a single-file change.

The limits are deliberately generous: they exist to stop credential stuffing and
mail bombing, not to annoy a student on a slow connection retrying a login.
"""
from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass

from app.core.errors import ApiError


@dataclass
class _Window:
    count: int
    resets_at: float


_buckets: dict[str, _Window] = defaultdict(lambda: _Window(0, 0.0))


def reset() -> None:
    """Test hook: clear all counters."""
    _buckets.clear()


def check(key: str, *, limit: int, window_seconds: int = 60) -> None:
    """Count one hit for `key`; raise 429 when the window is exhausted."""
    now = time.monotonic()
    bucket = _buckets[key]
    if bucket.resets_at <= now:
        bucket.count = 0
        bucket.resets_at = now + window_seconds
    bucket.count += 1
    if bucket.count > limit:
        retry_after = max(1, int(bucket.resets_at - now))
        raise ApiError(
            429,
            "rate_limited",
            "Too many attempts. Please wait and try again.",
            {"retry_after_seconds": retry_after},
        )
