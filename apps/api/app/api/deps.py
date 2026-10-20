"""Shared API dependencies.

`get_current_user` is the only supported way to identify a caller. It reads a
bearer access token, rejects anything expired or malformed with the standard
envelope, and returns a live (non-deleted) user with its role loaded.
"""
from __future__ import annotations

import jwt
from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core import flags, ratelimit
from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.identity import User


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise ApiError(401, "not_authenticated", "Sign in to continue.")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError as exc:
        raise ApiError(401, "invalid_token", "Your session has expired. Sign in again.") from exc

    try:
        user_id = int(payload.get("sub", ""))
    except (TypeError, ValueError) as exc:
        raise ApiError(401, "invalid_token", "Your session has expired. Sign in again.") from exc

    user = db.get(User, user_id)
    if user is None or user.is_deleted:
        raise ApiError(401, "invalid_token", "Your session has expired. Sign in again.")
    return user


def require_flag(name: str):
    """Gate a whole router behind a server-side flag (unfinished features)."""

    def _guard() -> None:
        if not flags.is_enabled(name):
            raise ApiError(404, "not_found", "This feature is not available.")

    return _guard


def rate_limit(scope: str, *, limit: int, window_seconds: int = 60):
    """Per-user fixed-window limit for expensive or abusable routes (F5).

    Auth routes limit by IP in their handlers; a signed-in route knows the user,
    so the counter follows the account even when the address changes.
    """

    def _guard(user: User = Depends(get_current_user)) -> None:
        ratelimit.check(f"{scope}:{user.id}", limit=limit, window_seconds=window_seconds)

    return _guard


def require_any_flag(*names: str):
    """Gate a router behind at least one flag.

    Opportunities serve two flags: managed work and external listings. A student
    route should exist while either is on, and disappear only when both are off.
    """

    def _guard() -> None:
        if not any(flags.is_enabled(name) for name in names):
            raise ApiError(404, "not_found", "This feature is not available.")

    return _guard
