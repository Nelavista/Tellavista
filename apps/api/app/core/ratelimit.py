"""Fixed-window rate limiting (ADR-0009: per-user and per-IP on auth routes).

The store is Redis when `REDIS_URL` is configured, so limits are shared across
workers and survive a restart (Render restarts every dyno without warning). With
`REDIS_URL` unset, a process-local counter is used: correct for a single worker
and for tests, but resets on restart and is not shared.

The Redis path is deliberately non-fatal. If Redis is unreachable the limiter
logs and falls back to the in-process store rather than failing every login:
availability wins over a temporarily weakened limit, and the previous behaviour
(per-process limits) is exactly what the fallback gives you.

The limits are deliberately generous: they exist to stop credential stuffing and
mail bombing, not to annoy a student on a slow connection retrying a login.
"""
from __future__ import annotations

import logging
import math
import time
from collections import defaultdict
from dataclasses import dataclass

from app.core.config import get_settings
from app.core.errors import ApiError

logger = logging.getLogger(__name__)

_KEY_PREFIX = "nelavista:ratelimit:"

# One round trip, atomic: increment, set the window on the first hit, and return
# the remaining TTL so a 429 can say exactly how long to wait. PTTL in
# milliseconds avoids rounding a sub-second wait down to zero.
_INCR_SCRIPT = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then
    redis.call('PEXPIRE', KEYS[1], ARGV[1])
end
local ttl = redis.call('PTTL', KEYS[1])
if ttl < 0 then
    redis.call('PEXPIRE', KEYS[1], ARGV[1])
    ttl = tonumber(ARGV[1])
end
return {count, ttl}
"""


@dataclass
class _Window:
    count: int
    resets_at: float


_buckets: dict[str, _Window] = defaultdict(lambda: _Window(0, 0.0))

_client = None
_client_url: str | None = None
_script = None


def _redis() -> tuple[object, object] | tuple[None, None]:
    """The shared Redis client and Lua script, or (None, None) when unconfigured."""
    global _client, _client_url, _script
    url = get_settings().REDIS_URL
    if not url:
        return None, None
    if _client is None or _client_url != url:
        # Imported lazily so the package is only needed where Redis is used; it
        # is a hard dependency in pyproject.toml, but local mode needs no server.
        import redis

        _client = redis.Redis.from_url(
            url,
            decode_responses=True,
            socket_timeout=2,
            socket_connect_timeout=2,
        )
        _script = _client.register_script(_INCR_SCRIPT)
        _client_url = url
    return _client, _script


def _too_many(retry_after: int) -> ApiError:
    return ApiError(
        429,
        "rate_limited",
        "Too many attempts. Please wait and try again.",
        {"retry_after_seconds": retry_after},
    )


def _check_memory(key: str, *, limit: int, window_seconds: int) -> None:
    now = time.monotonic()
    bucket = _buckets[key]
    if bucket.resets_at <= now:
        bucket.count = 0
        bucket.resets_at = now + window_seconds
    bucket.count += 1
    if bucket.count > limit:
        retry_after = max(1, int(bucket.resets_at - now))
        raise _too_many(retry_after)


def reset() -> None:
    """Test hook: clear the in-process counters and any Redis keys for this app."""
    _buckets.clear()
    client, _ = _redis()
    if client is None:
        return
    try:
        keys = list(client.scan_iter(match=f"{_KEY_PREFIX}*", count=500))  # type: ignore[attr-defined]
        if keys:
            client.delete(*keys)  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - reset must never fail a test run
        logger.warning("rate limiter: could not clear Redis keys on reset", exc_info=True)


def check(key: str, *, limit: int, window_seconds: int = 60) -> None:
    """Count one hit for `key`; raise 429 when the window is exhausted."""
    client, script = _redis()
    if client is not None:
        try:
            count, ttl_ms = script(  # type: ignore[misc]
                keys=[f"{_KEY_PREFIX}{key}"],
                args=[window_seconds * 1000],
                client=client,
            )
        except Exception:
            logger.warning(
                "rate limiter: Redis unavailable, using the in-process store", exc_info=True
            )
        else:
            if int(count) > limit:
                raise _too_many(max(1, math.ceil(int(ttl_ms) / 1000)))
            return
    _check_memory(key, limit=limit, window_seconds=window_seconds)
