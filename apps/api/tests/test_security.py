"""Phase 0 PR 0.8 — hashing and tokens.

Written now, run with the rest of the suite in the verification pass.
"""
from __future__ import annotations

import hashlib

import jwt
import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    hash_token,
    is_argon2,
    new_refresh_token,
    verify_legacy_pbkdf2,
    verify_legacy_werkzeug,
    verify_password,
)


def test_argon2_hash_round_trip_and_rehash_flag() -> None:
    stored = hash_password("correct horse battery")
    assert is_argon2(stored)
    ok, needs_rehash = verify_password("correct horse battery", stored)
    assert ok is True and needs_rehash is False

    wrong, _ = verify_password("wrong password", stored)
    assert wrong is False


def test_malformed_or_missing_hash_never_raises() -> None:
    assert verify_password("x", None) == (False, False)
    assert verify_password("x", "not-a-hash") == (False, False)


def test_short_password_is_refused() -> None:
    with pytest.raises(ValueError):
        hash_password("short")


def test_v1_pbkdf2_hash_verifies_and_wrong_password_does_not() -> None:
    salt = "abc123"
    iterations = 260000
    digest = hashlib.pbkdf2_hmac("sha256", b"v1-password", salt.encode(), iterations).hex()
    stored = f"pbkdf2:sha256:{iterations}${salt}${digest}"

    assert verify_legacy_pbkdf2("v1-password", stored) is True
    assert verify_legacy_pbkdf2("nope", stored) is False
    assert verify_legacy_pbkdf2("v1-password", None) is False
    assert verify_legacy_werkzeug("v1-password", stored) is True


def test_v1_werkzeug_scrypt_hash_verifies_and_wrong_password_does_not() -> None:
    salt = "abc123"
    n, r, p = 2**14, 8, 1
    digest = hashlib.scrypt(
        b"v1-password", salt=salt.encode(), n=n, r=r, p=p, maxmem=132 * n * r * p
    ).hex()
    stored = f"scrypt:{n}:{r}:{p}${salt}${digest}"

    assert verify_legacy_werkzeug("v1-password", stored) is True
    assert verify_legacy_werkzeug("nope", stored) is False
    assert verify_legacy_werkzeug("v1-password", "scrypt:bad") is False
    assert verify_legacy_werkzeug("v1-password", f"scrypt:999999999:8:1${salt}${digest}") is False


def test_access_token_round_trip_and_tamper_detection() -> None:
    token = create_access_token(7, "student")
    payload = decode_access_token(token)
    assert payload["sub"] == "7" and payload["role"] == "student"

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token + "x")


def test_refresh_tokens_are_random_and_only_stored_hashed() -> None:
    first_raw, first_hash = new_refresh_token()
    second_raw, _ = new_refresh_token()
    assert first_raw != second_raw
    assert first_hash == hash_token(first_raw)
    assert first_raw not in first_hash
