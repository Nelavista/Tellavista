"""One error shape for every client (web, iOS, Android, admin).

Every failure is `{"error": {"code", "message", "details", "request_id"}}`.
`code` is machine-readable and stable; `message` is safe to show a student;
`details` is only ever structured data (never a stack trace). The request id ties
a report from a student's phone to one line in the server logs.

Nothing here leaks an exception message on a 500 — the log has the trace, the
client gets `internal_error` and the request id.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.request_id import get_request_id

logger = logging.getLogger(__name__)

_DEFAULT_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    422: "validation_error",
    426: "upgrade_required",
    429: "rate_limited",
    500: "internal_error",
}


class ApiError(Exception):
    """Raise this from services and routes; the handler renders the envelope."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def error_body(code: str, message: str, details: Any | None = None) -> dict:
    payload: dict[str, Any] = {"code": code, "message": message}
    request_id = get_request_id()
    if request_id:
        payload["request_id"] = request_id
    if details is not None:
        payload["details"] = details
    return {"error": payload}


def _validation_details(exc: RequestValidationError) -> list[dict]:
    """Only the serialisable fields: `ctx` can hold exception objects."""
    return [
        {
            "loc": ".".join(str(part) for part in error.get("loc", [])),
            "msg": str(error.get("msg", "")),
            "type": str(error.get("type", "")),
        }
        for error in exc.errors()
    ]


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _handle_api_error(_request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _handle_validation(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_body(
                "validation_error", "The request contains invalid fields.", _validation_details(exc)
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = _DEFAULT_CODES.get(exc.status_code, "http_error")
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
        return JSONResponse(status_code=exc.status_code, content=error_body(code, message))

    @app.exception_handler(Exception)
    async def _handle_unexpected(_request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled error request_id=%s", get_request_id(), exc_info=exc)
        return JSONResponse(
            status_code=500,
            content=error_body("internal_error", "Something went wrong. Please try again."),
        )
