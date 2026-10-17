"""Phase 0 PR 0.5 — the API conventions every later endpoint inherits.

Covers the four things clients depend on: one error envelope, a request id
that survives into the error body, keyset pagination that cannot skip rows, and
an idempotency store whose three outcomes (replay, in progress, key reused) are
distinct.
"""
from __future__ import annotations

import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError, register_exception_handlers
from app.core.pagination import decode_cursor, encode_cursor, paginate, resolve_limit
from app.core.request_id import RequestIdMiddleware
from app.main import app as real_app
from app.models.skills import Skill
from app.services.idempotency import IdempotencyStore


def _mini_app() -> FastAPI:
    """A throwaway app: the handlers, not the product, are under test here."""
    api = FastAPI()
    api.add_middleware(RequestIdMiddleware)
    register_exception_handlers(api)

    @api.get("/conflict")
    def conflict() -> dict:
        raise ApiError(409, "conflict.demo", "Nope.", {"why": "test"})

    @api.get("/items/{item_id}")
    def item(item_id: int) -> dict:
        return {"item_id": item_id}

    @api.get("/explode")
    def explode() -> dict:
        raise RuntimeError("kaboom")

    return api


def test_error_envelope_carries_code_details_and_request_id() -> None:
    client = TestClient(_mini_app(), raise_server_exceptions=False)
    response = client.get("/conflict")
    assert response.status_code == 409
    error = response.json()["error"]
    assert error["code"] == "conflict.demo"
    assert error["details"] == {"why": "test"}
    assert error["request_id"] == response.headers["X-Request-ID"]


def test_inbound_request_id_is_echoed_and_malformed_one_replaced() -> None:
    client = TestClient(_mini_app(), raise_server_exceptions=False)
    given = "abc12345-ok"
    echoed = client.get("/conflict", headers={"X-Request-ID": given})
    assert echoed.headers["X-Request-ID"] == given

    hostile = client.get("/conflict", headers={"X-Request-ID": "bad id with spaces"})
    assert hostile.headers["X-Request-ID"] != "bad id with spaces"
    assert len(hostile.headers["X-Request-ID"]) == 32


def test_validation_errors_use_the_same_envelope() -> None:
    client = TestClient(_mini_app(), raise_server_exceptions=False)
    response = client.get("/items/not-an-int")
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    assert error["details"][0]["loc"] == "path.item_id"


def test_unhandled_error_hides_the_exception_text() -> None:
    client = TestClient(_mini_app(), raise_server_exceptions=False)
    response = client.get("/explode")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
    assert "kaboom" not in response.text


def test_real_app_answers_unknown_routes_with_the_envelope() -> None:
    client = TestClient(real_app)
    response = client.get("/v1/does-not-exist")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
    assert response.headers["X-Request-ID"]
    assert response.headers["X-API-Version"]


def test_cursor_round_trip_and_rejection() -> None:
    assert decode_cursor(encode_cursor(42)) == 42
    with pytest.raises(ApiError) as excinfo:
        decode_cursor("not-a-cursor")
    assert excinfo.value.status_code == 400
    assert excinfo.value.code == "pagination.invalid_cursor"


def test_limit_is_bounded() -> None:
    assert resolve_limit(None) == 20
    assert resolve_limit(5) == 5
    assert resolve_limit(10_000) == 100
    with pytest.raises(ApiError):
        resolve_limit(0)


def test_pagination_walks_every_row_once_in_order(db: Session) -> None:
    for i in range(5):
        db.add(Skill(slug=f"walker-{uuid.uuid4().hex[:6]}", name=f"Skill {i}"))
    db.flush()

    seen: list[int] = []
    cursor: str | None = None
    pages = 0
    while True:
        rows, cursor = paginate(
            db, select(Skill), id_column=Skill.id, cursor=cursor, limit=2
        )
        seen.extend(row.id for row in rows)
        pages += 1
        if cursor is None:
            break

    assert pages == 3
    assert seen == sorted(seen)
    assert len(seen) == 5


def _store(db: Session, *, key: str, body: dict) -> IdempotencyStore:
    return IdempotencyStore(db, key=key, method="POST", path="/v1/work/submissions", body=body)


def test_idempotency_replays_the_stored_response(db: Session) -> None:
    key = str(uuid.uuid4())
    body = {"labels": ["positive"]}

    first = _store(db, key=key, body=body)
    assert first.begin() is None
    first.complete(201, {"id": 7})

    replay = _store(db, key=key, body=body)
    stored = replay.begin()
    assert stored is not None
    assert stored.status_code == 201 and stored.body == {"id": 7}


def test_idempotency_rejects_a_second_write_while_in_flight(db: Session) -> None:
    key = str(uuid.uuid4())
    _store(db, key=key, body={"a": 1}).begin()

    with pytest.raises(ApiError) as excinfo:
        _store(db, key=key, body={"a": 1}).begin()
    assert excinfo.value.status_code == 409
    assert excinfo.value.code == "idempotency.in_progress"


def test_idempotency_rejects_the_same_key_with_a_different_body(db: Session) -> None:
    key = str(uuid.uuid4())
    first = _store(db, key=key, body={"a": 1})
    first.begin()
    first.complete(201, {"id": 1})

    with pytest.raises(ApiError) as excinfo:
        _store(db, key=key, body={"a": 2}).begin()
    assert excinfo.value.status_code == 409
    assert excinfo.value.code == "idempotency.key_reused"


def test_idempotency_key_is_validated(db: Session) -> None:
    with pytest.raises(ApiError) as excinfo:
        _store(db, key="", body={})
    assert excinfo.value.code == "idempotency.invalid_key"
