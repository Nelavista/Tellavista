"""Two-factor authentication for staff accounts (F1, C8).

TOTP, RFC 6238, implemented with the standard library. A dependency would add one
more supply-chain surface to a security-critical path, and the algorithm is small
enough to test directly.

The rules the routes depend on:

* a secret is **pending** until the first code is confirmed, so a half-finished
  enrolment cannot lock anyone out;
* recovery codes are hashed at rest and consumed one at a time;
* 2FA is *required* before an admin session is issued for a staff account that
  has it enabled — a password alone is never enough after enrolment.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import struct
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.security import hash_token
from app.core.time import utcnow
from app.models.identity import User

TOTP_DIGITS = 6
TOTP_STEP_SECONDS = 30
# One step either side absorbs a clock that is a few seconds out without widening
# the guessing window beyond the usual 90 seconds.
TOTP_VERIFY_WINDOW = 1
RECOVERY_CODE_COUNT = 10
ISSUER = "Nelavista"


def new_secret() -> str:
    """A fresh base32 secret (160 bits, the RFC-recommended size)."""
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def _counter(at: datetime | None = None) -> int:
    moment = at or utcnow()
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return int(moment.timestamp()) // TOTP_STEP_SECONDS


def code_at(secret: str, at: datetime | None = None, *, offset: int = 0) -> str:
    """The six-digit code for `secret` at a counter offset from now."""
    padded = secret.upper() + "=" * (-len(secret) % 8)
    key = base64.b32decode(padded, casefold=True)
    counter = _counter(at) + offset
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    index = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[index : index + 4])[0] & 0x7FFFFFFF
    return str(value % (10**TOTP_DIGITS)).zfill(TOTP_DIGITS)


def verify_code(secret: str, code: str, at: datetime | None = None) -> bool:
    """True when `code` is valid for the current step (or one step either side)."""
    cleaned = (code or "").strip().replace(" ", "")
    if not secret or not cleaned.isdigit() or len(cleaned) != TOTP_DIGITS:
        return False
    for offset in range(-TOTP_VERIFY_WINDOW, TOTP_VERIFY_WINDOW + 1):
        if hmac.compare_digest(code_at(secret, at, offset=offset), cleaned):
            return True
    return False


def provisioning_uri(secret: str, account_label: str) -> str:
    """The `otpauth://` URI an authenticator app scans."""
    label = f"{ISSUER}:{account_label}".replace(" ", "%20")
    return (
        f"otpauth://totp/{label}?secret={secret}&issuer={ISSUER}"
        f"&algorithm=SHA1&digits={TOTP_DIGITS}&period={TOTP_STEP_SECONDS}"
    )


def is_enabled(user: User) -> bool:
    return user.totp_enabled_at is not None and bool(user.totp_secret)


def is_staff(user: User) -> bool:
    return bool(user.role and user.role.is_staff)


def requires_second_factor(user: User) -> bool:
    """A staff account with 2FA enabled must present a code at login."""
    return is_staff(user) and is_enabled(user)


def _recovery_code() -> str:
    raw = secrets.token_hex(5).upper()
    return f"{raw[:5]}-{raw[5:]}"


def _normalise_recovery(code: str) -> str:
    return (code or "").strip().upper().replace("-", "").replace(" ", "")


def _hash_recovery(code: str) -> str:
    return hash_token(_normalise_recovery(code))


def begin_enrollment(db: Session, user: User) -> tuple[str, str]:
    """Mint a pending secret and return `(secret, otpauth_uri)`.

    Re-enrolling while 2FA is live is refused: disabling first is a deliberate
    step, and it keeps a stolen session from silently replacing the second factor.
    """
    if is_enabled(user):
        raise ApiError(
            409,
            "two_factor_already_enabled",
            "Two-factor is already on. Turn it off before enrolling again.",
        )
    secret = new_secret()
    user.totp_secret = secret
    user.totp_enabled_at = None
    user.totp_recovery_hashes = None
    db.flush()
    return secret, provisioning_uri(secret, user.email)


def confirm_enrollment(db: Session, user: User, code: str) -> list[str]:
    """Confirm the pending secret and return recovery codes exactly once."""
    if not user.totp_secret:
        raise ApiError(400, "two_factor_not_started", "Start two-factor setup first.")
    if not verify_code(user.totp_secret, code):
        raise ApiError(400, "invalid_two_factor_code", "That code is not valid. Try the next one.")

    codes = [_recovery_code() for _ in range(RECOVERY_CODE_COUNT)]
    user.totp_recovery_hashes = [_hash_recovery(item) for item in codes]
    user.totp_enabled_at = utcnow()
    db.flush()
    return codes


def disable(db: Session, user: User, code: str) -> None:
    """Turn 2FA off, but only with a valid code (or a recovery code)."""
    if not is_enabled(user):
        raise ApiError(409, "two_factor_not_enabled", "Two-factor is not on for this account.")
    if not verify_login_code(db, user, code):
        raise ApiError(400, "invalid_two_factor_code", "That code is not valid.")
    user.totp_enabled_at = None
    user.totp_secret = None
    user.totp_recovery_hashes = None
    db.flush()


def verify_login_code(db: Session, user: User, code: str) -> bool:
    """A TOTP code, or a single-use recovery code."""
    if not is_enabled(user):
        return False
    if verify_code(user.totp_secret or "", code):
        return True

    normalised = _normalise_recovery(code)
    if len(normalised) != 10:
        return False
    wanted = _hash_recovery(code)
    hashes = list(user.totp_recovery_hashes or [])
    if wanted not in hashes:
        return False
    hashes.remove(wanted)
    user.totp_recovery_hashes = hashes
    db.flush()
    return True


def remaining_recovery_codes(user: User) -> int:
    return len(user.totp_recovery_hashes or [])


__all__ = [
    "ISSUER",
    "TOTP_DIGITS",
    "TOTP_STEP_SECONDS",
    "begin_enrollment",
    "code_at",
    "confirm_enrollment",
    "disable",
    "is_enabled",
    "is_staff",
    "new_secret",
    "provisioning_uri",
    "remaining_recovery_codes",
    "requires_second_factor",
    "verify_code",
    "verify_login_code",
]
