"""Request correlation id.

Every request gets an id, returned as `X-Request-ID` and embedded in the error
envelope, so a student's screenshot of an error is enough to find the log line.
An inbound id is honoured only if it is short and well-formed — it ends up in
logs, so it must not be attacker-controlled text.
"""
from __future__ import annotations

import re
import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_HEADER = "X-Request-ID"
_VALID = re.compile(r"^[A-Za-z0-9._-]{8,64}$")

_request_id: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return _request_id.get()


def set_request_id(value: str) -> object:
    """Set for the current context. Returns the token for `reset`."""
    return _request_id.set(value)


def reset_request_id(token: object) -> None:
    _request_id.reset(token)  # type: ignore[arg-type]


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        inbound = request.headers.get(_HEADER) or ""
        request_id = inbound if _VALID.match(inbound) else uuid.uuid4().hex
        token = set_request_id(request_id)
        try:
            response = await call_next(request)
            response.headers[_HEADER] = request_id
            return response
        finally:
            reset_request_id(token)
