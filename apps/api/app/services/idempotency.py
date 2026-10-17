"""Idempotency store: make every important write safe to retry (ADR-0007).

The client sends a UUIDv4 `Idempotency-Key`. The first request claims the key and
stores its response; a replay with the same key and body returns the stored
response instead of writing again. Three outcomes are distinct on purpose:

* **replay** — same key, same request, already completed: return the old response.
* **in progress** — same key, first attempt has not finished: 409, retry shortly.
  Returning the second write would be the bug this exists to prevent.
* **key reused** — same key, different body: 409, because the client is confused
  and one of the two writes must not happen silently.

The claim is inserted inside a savepoint, so losing a race to a concurrent request
does not roll back the caller's transaction.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import IdempotencyKey

DEFAULT_TTL = timedelta(hours=24)


def _aware(value: datetime) -> datetime:
    """SQLite returns naive datetimes even for timezone-aware columns; normalise."""
    return value if value.tzinfo else value.replace(tzinfo=UTC)


def fingerprint(method: str, path: str, body: Any) -> str:
    """Stable hash of what the request *means*. Key order must not matter."""
    canonical = json.dumps(
        {"method": method.upper(), "path": path, "body": body},
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


@dataclass(frozen=True)
class StoredResponse:
    status_code: int
    body: dict | None


class IdempotencyStore:
    def __init__(
        self,
        db: Session,
        *,
        key: str,
        method: str,
        path: str,
        user_id: int | None = None,
        body: Any = None,
        ttl: timedelta = DEFAULT_TTL,
    ) -> None:
        if not key or len(key) > 64:
            raise ApiError(400, "idempotency.invalid_key", "Idempotency-Key must be 1-64 characters.")
        self.db = db
        self.key = key
        self.user_id = user_id
        self.method = method.upper()
        self.path = path
        self.ttl = ttl
        self._fingerprint = fingerprint(method, path, body)
        self._row: IdempotencyKey | None = None

    def begin(self) -> StoredResponse | None:
        """Return the stored response on replay; claim the key otherwise."""
        row = self.db.scalar(select(IdempotencyKey).where(IdempotencyKey.key == self.key))
        now = datetime.now(UTC)

        if row is not None and _aware(row.expires_at) <= now:
            # Expired rows are not evidence of anything; free the key.
            self.db.delete(row)
            self.db.flush()
            row = None

        if row is None:
            self._insert(now)
            return None

        if row.request_fingerprint != self._fingerprint:
            raise ApiError(
                409,
                "idempotency.key_reused",
                "This Idempotency-Key was already used for a different request.",
            )
        if row.completed_at is None:
            raise ApiError(
                409,
                "idempotency.in_progress",
                "This request is still being processed. Retry in a moment.",
            )
        return StoredResponse(row.response_status or 200, row.response_body)

    def complete(self, status_code: int, body: dict | None = None) -> None:
        row = self._row or self.db.scalar(
            select(IdempotencyKey).where(IdempotencyKey.key == self.key)
        )
        if row is None:  # pragma: no cover - misuse, but fail loudly rather than silently
            raise RuntimeError("complete() called before begin()")
        row.response_status = status_code
        row.response_body = body
        row.completed_at = datetime.now(UTC)
        self.db.flush()

    def _insert(self, now: datetime) -> None:
        row = IdempotencyKey(
            key=self.key,
            user_id=self.user_id,
            method=self.method,
            path=self.path,
            request_fingerprint=self._fingerprint,
            expires_at=now + self.ttl,
        )
        try:
            with self.db.begin_nested():
                self.db.add(row)
                self.db.flush()
        except IntegrityError as exc:
            # Another request claimed the key between our SELECT and INSERT.
            raise ApiError(
                409,
                "idempotency.in_progress",
                "This request is still being processed. Retry in a moment.",
            ) from exc
        self._row = row
