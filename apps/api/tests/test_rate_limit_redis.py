"""Redis path of the rate limiter: shared counts, sane retry_after, safe fallback."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core import ratelimit
from app.core.errors import ApiError


class _FakeScript:
    """Counts hits in a dict, standing in for the Lua script's return value."""

    def __init__(self, store: dict[str, int], ttl_ms: int = 60_000) -> None:
        self.store = store
        self.ttl_ms = ttl_ms

    def __call__(self, *, keys, args, client) -> list[int]:  # noqa: ANN001
        key = keys[0]
        count = self.store.get(key, 0) + 1
        self.store[key] = count
        return [count, self.ttl_ms]


def _fake_client() -> SimpleNamespace:
    return SimpleNamespace(scan_iter=lambda **_kwargs: [], delete=lambda *_args: None)


def test_redis_store_shares_counts_and_reports_retry(monkeypatch) -> None:
    store: dict[str, int] = {}
    script = _FakeScript(store, ttl_ms=700)
    monkeypatch.setattr(ratelimit, "_redis", lambda: (_fake_client(), script))
    ratelimit.reset()

    ratelimit.check("login:1.2.3.4", limit=2, window_seconds=60)
    ratelimit.check("login:1.2.3.4", limit=2, window_seconds=60)
    with pytest.raises(ApiError) as excinfo:
        ratelimit.check("login:1.2.3.4", limit=2, window_seconds=60)

    assert excinfo.value.status_code == 429
    assert excinfo.value.details["retry_after_seconds"] == 1  # ceil(0.7s)
    assert list(store) == [f"{ratelimit._KEY_PREFIX}login:1.2.3.4"]


def test_redis_failure_falls_back_to_the_process_store(monkeypatch) -> None:
    def _boom(**_kwargs):
        raise ConnectionError("redis is down")

    ratelimit._buckets.clear()
    monkeypatch.setattr(ratelimit, "_redis", lambda: (_fake_client(), _boom))

    ratelimit.check("verify-resend:42", limit=1, window_seconds=60)
    with pytest.raises(ApiError):
        ratelimit.check("verify-resend:42", limit=1, window_seconds=60)
