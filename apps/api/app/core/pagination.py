"""Cursor pagination (ADR-0007: no offset paging on large sets).

A cursor is the id of the last row the client already has, base64url-encoded so
clients treat it as opaque. The query fetches `limit + 1` rows: seeing one extra
is how we know there is another page without a COUNT.

Offset paging breaks when rows are inserted between requests; keyset paging on a
monotonic id does not, which matters for a queue of submissions arriving on bad
networks.
"""
from __future__ import annotations

import base64
import binascii
import json
from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import Session

from app.core.errors import ApiError

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def encode_cursor(value: int | str) -> str:
    raw = json.dumps({"v": value}, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def decode_cursor(cursor: str) -> int:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded.encode()))
        value = payload["v"]
        if not isinstance(value, int):
            raise ValueError("cursor value is not an integer id")
        return value
    except (binascii.Error, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ApiError(
            400, "pagination.invalid_cursor", "This page link is invalid. Start from the first page."
        ) from exc


def resolve_limit(limit: int | None, *, default: int = DEFAULT_LIMIT, maximum: int = MAX_LIMIT) -> int:
    if limit is None:
        return default
    if limit < 1:
        raise ApiError(400, "pagination.invalid_limit", "limit must be at least 1.")
    return min(limit, maximum)


def paginate(
    db: Session,
    stmt: Select,
    *,
    id_column: Any,
    cursor: str | None = None,
    limit: int | None = None,
) -> tuple[list, str | None]:
    """Return one page of rows and the cursor for the next page (or None)."""
    page_size = resolve_limit(limit)
    query = stmt
    if cursor:
        query = query.where(id_column > decode_cursor(cursor))

    rows = list(db.scalars(query.order_by(id_column).limit(page_size + 1)).all())
    has_more = len(rows) > page_size
    rows = rows[:page_size]
    next_cursor = encode_cursor(rows[-1].id) if has_more and rows else None
    return rows, next_cursor
