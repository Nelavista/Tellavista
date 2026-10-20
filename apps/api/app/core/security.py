"""Password hashing, access tokens and opaque refresh tokens (ADR-0009).

Three rules:
* Passwords are **Argon2id**; a V1 PBKDF2 hash still verifies and is upgraded on
  the first successful login (ADR-0005), without ever seeing a plaintext password
  leave the request.
* Access tokens are short-lived JWTs (15 minutes) and carry only an id and role.
* Refresh tokens are **opaque**, stored only as a SHA-256 hash, single-use, and
  belong to a rotating family. A replayed token revokes the whole family.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from app.core.config import get_settings

ACCESS_TTL = timedelta(minutes=15)
REFRESH_TTL = timedelta(days=30)
EMAIL_TOKEN_TTL = timedelta(hours=24)
RESET_TOKEN_TTL = timedelta(hours=2)
# A second-factor challenge is short: it exists only to carry "password was
# correct" from the login call to the code call.
MFA_TTL = timedelta(minutes=5)

JWT_ALGORITHM = "HS256"
JWT_ISSUER = "nelavista"
JWT_AUDIENCE = "nelavista-api"

MIN_PASSWORD_LENGTH = 10

_hasher = PasswordHasher()  # argon2id defaults


# --- passwords ---------------------------------------------------------------


def hash_password(password: str) -> str:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
    return _hasher.hash(password)


def verify_password(password: str, stored: str | None) -> tuple[bool, bool]:
    """Return (ok, needs_rehash). Never raises on a malformed hash."""
    if not stored:
        return False, False
    try:
        _hasher.verify(stored, password)
        return True, _hasher.check_needs_rehash(stored)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False, False


def is_argon2(stored: str | None) -> bool:
    return bool(stored) and stored.startswith("$argon2")


def verify_legacy_pbkdf2(password: str, stored: str | None) -> bool:
    """Werkzeug-format PBKDF2 (`pbkdf2:sha256:260000$salt$hex`), as V1 stores it.

    Implemented here rather than importing V1 or werkzeug: V2 never imports V1 code
    (brief), and the format is small enough to verify directly.
    """
    if not stored or not stored.startswith("pbkdf2:"):
        return False
    try:
        method, salt, expected = stored.split("$")
        _, digest, iterations = method.split(":")
        if digest != "sha256":
            return False
        computed = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), int(iterations)
        ).hex()
        return hmac.compare_digest(computed, expected)
    except (ValueError, TypeError):
        return False


# --- access tokens -----------------------------------------------------------


def create_access_token(user_id: int, role: str | None) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role or "",
        "iat": now,
        "exp": now + ACCESS_TTL,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "typ": "access",
    }
    return jwt.encode(payload, get_settings().SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Raises jwt.InvalidTokenError (expired, wrong audience, tampered)."""
    payload = jwt.decode(
        token,
        get_settings().SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
        audience=JWT_AUDIENCE,
        issuer=JWT_ISSUER,
    )
    if payload.get("typ") != "access":
        raise jwt.InvalidTokenError("not an access token")
    return payload


def create_mfa_token(user_id: int, platform: str) -> str:
    """A short-lived token that proves the password step only.

    It is a JWT with its own `typ`, so it can never be used as an access token:
    `decode_access_token` rejects it, and the MFA route rejects access tokens.
    """
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "platform": platform,
        "iat": now,
        "exp": now + MFA_TTL,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "typ": "mfa",
    }
    return jwt.encode(payload, get_settings().SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_mfa_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        get_settings().SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
        audience=JWT_AUDIENCE,
        issuer=JWT_ISSUER,
    )
    if payload.get("typ") != "mfa":
        raise jwt.InvalidTokenError("not an MFA token")
    return payload


# --- opaque tokens -----------------------------------------------------------


def new_refresh_token() -> tuple[str, str]:
    """Return (raw token for the client, hash for the database)."""
    raw = secrets.token_urlsafe(48)
    return raw, hash_token(raw)


def new_email_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, hash_token(raw)


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()
