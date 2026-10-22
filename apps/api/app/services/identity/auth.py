"""Identity service: registration, login, sessions and recovery (ADR-0009).

Everything a client can do to an account lives here so the routes stay thin and
the rules are testable without HTTP. The security-critical parts:

* login accepts a V1 PBKDF2 hash and **upgrades it to Argon2id** on first success;
* a refresh token is single-use, rotation keeps the family, and presenting a used
  token revokes the whole family (reuse detection) and is audited;
* email/reset tokens are stored hashed, expire, and are single-use;
* account deletion anonymises and deactivates, never hard-deletes, because money
  and audit rows must stay explainable.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import ApiError
from app.core.security import (
    EMAIL_TOKEN_TTL,
    REFRESH_TTL,
    RESET_TOKEN_TTL,
    create_access_token,
    hash_password,
    hash_token,
    is_argon2,
    new_email_token,
    new_refresh_token,
    verify_legacy_werkzeug,
    verify_password,
)
from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import (
    CONSENT_KINDS,
    EMAIL_TOKEN_PURPOSES,
    REVOKE_ACCOUNT_DELETED,
    REVOKE_LOGOUT,
    REVOKE_PASSWORD_RESET,
    REVOKE_REUSE_DETECTED,
    REVOKE_ROTATED,
    Consent,
    EmailToken,
    RefreshToken,
    User,
    UserProfile,
)
from app.services import audit
from app.services.jobs import enqueue

TERMS_VERSION = "1.0"


# --- helpers -----------------------------------------------------------------


def normalise_email(email: str) -> str:
    return email.strip().lower()


def _student_role_id(db: Session) -> int | None:
    return db.scalar(select(Role.id).where(Role.code == ROLE_STUDENT))


def _hash_password(password: str) -> str:
    """Hash, converting the length rule into a client-facing 400."""
    try:
        return hash_password(password)
    except ValueError as exc:
        raise ApiError(400, "weak_password", "Use at least 10 characters for your password.") from exc


def _issue_access(user: User) -> str:
    return create_access_token(user.id, user.role.code if user.role else None)


def _new_refresh_row(
    db: Session, *, user_id: int, platform: str, family_id: str, expires_at: datetime
) -> tuple[str, RefreshToken]:
    raw, token_hash = new_refresh_token()
    row = RefreshToken(
        user_id=user_id,
        family_id=family_id,
        token_hash=token_hash,
        platform=platform,
        expires_at=expires_at,
    )
    db.add(row)
    db.flush()
    return raw, row


def _revoke(db: Session, token: RefreshToken, reason: str) -> None:
    if token.revoked_at is None:
        token.revoked_at = datetime.now(UTC)
        token.revoked_reason = reason


# --- registration and login --------------------------------------------------


def register(
    db: Session,
    *,
    email: str,
    username: str,
    password: str,
    name: str | None = None,
    accept_terms: bool = False,
    platform: str = "web",
) -> tuple[User, str, str, datetime]:
    email = normalise_email(email)
    if db.scalar(select(User.id).where(User.email == email)) is not None:
        raise ApiError(409, "email_taken", "An account with this email already exists.")
    if db.scalar(select(User.id).where(User.username == username)) is not None:
        raise ApiError(409, "username_taken", "That username is taken. Try another.")

    user = User(
        email=email,
        username=username,
        password_hash=_hash_password(password),
        name=name,
        email_verified=False,
        role_id=_student_role_id(db),
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError as exc:  # lost a race on the unique constraints
        raise ApiError(409, "email_taken", "An account with this email already exists.") from exc

    db.add(UserProfile(user_id=user.id, display_name=name or username))
    if accept_terms:
        db.add(
            Consent(
                user_id=user.id,
                kind="terms_of_service",
                document_version=TERMS_VERSION,
                granted=True,
            )
        )

    _send_verification(db, user)
    audit.record(
        db, action="account.created", actor_user_id=user.id, target_type="user", target_id=user.id
    )
    access, refresh, expires = issue_session(db, user, platform=platform)
    return user, access, refresh, expires


def web_link(path: str) -> str:
    """An absolute link into the web app. Relative paths cannot be clicked in mail."""
    return f"{get_settings().WEB_BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def _send_verification(db: Session, user: User) -> None:
    raw, token_hash = new_email_token()
    db.add(
        EmailToken(
            user_id=user.id,
            purpose="verify_email",
            token_hash=token_hash,
            expires_at=datetime.now(UTC) + EMAIL_TOKEN_TTL,
        )
    )
    db.flush()
    enqueue(
        db,
        "send_email",
        {
            "to": user.email,
            "subject": "Verify your Nelavista email",
            "body": f"Verify your email: {web_link(f'/auth/verify?token={raw}')}",
        },
    )


def authenticate(db: Session, *, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == normalise_email(email)))
    # One message for unknown user and wrong password: no account enumeration.
    if user is None or user.is_deleted:
        raise ApiError(401, "invalid_credentials", "Email or password is incorrect.")

    if is_argon2(user.password_hash):
        ok, needs_rehash = verify_password(password, user.password_hash)
    else:
        # V1 account: verify its Werkzeug hash (PBKDF2 or scrypt), then upgrade
        # to Argon2id silently.
        ok = verify_legacy_werkzeug(password, user.password_hash)
        needs_rehash = ok

    if not ok:
        raise ApiError(401, "invalid_credentials", "Email or password is incorrect.")

    if needs_rehash:
        user.password_hash = _hash_password(password)
        audit.record(
            db, action="password.rehashed", actor_user_id=user.id, target_type="user",
            target_id=user.id,
        )

    user.last_login = datetime.now(UTC)
    db.flush()
    return user


def issue_session(
    db: Session, user: User, *, platform: str = "web"
) -> tuple[str, str, datetime]:
    family_id = str(uuid.uuid4())
    expires_at = datetime.now(UTC) + REFRESH_TTL
    raw, _row = _new_refresh_row(
        db, user_id=user.id, platform=platform, family_id=family_id, expires_at=expires_at
    )
    return _issue_access(user), raw, expires_at


# --- refresh rotation --------------------------------------------------------


def rotate(db: Session, *, raw_token: str) -> tuple[str, str, datetime]:
    """Rotate a refresh token. A replayed token revokes its whole family."""
    token = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw_token)))
    if token is None:
        raise ApiError(401, "invalid_refresh_token", "Please sign in again.")
    # Reuse detection comes before the revocation check on purpose: a rotated
    # token is revoked as well as used, and replaying it is exactly the signal
    # that the family must die. Checking revocation first would swallow that.
    if token.used_at is not None:
        # Reuse detection: somebody replayed a token that was already exchanged.
        _revoke_family(db, token.family_id, REVOKE_REUSE_DETECTED)
        audit.record(
            db,
            action="auth.refresh_reuse",
            target_type="refresh_token",
            target_id=token.id,
            reason="replayed a used refresh token",
        )
        raise ApiError(401, "refresh_token_reused", "Please sign in again on this device.")
    if token.revoked_at is not None:
        raise ApiError(401, "invalid_refresh_token", "Please sign in again.")
    if token.expires_at.replace(tzinfo=token.expires_at.tzinfo or UTC) <= datetime.now(UTC):
        _revoke(db, token, "expired")
        raise ApiError(401, "invalid_refresh_token", "Please sign in again.")

    user = db.get(User, token.user_id)
    if user is None or user.is_deleted:
        raise ApiError(401, "invalid_refresh_token", "Please sign in again.")

    token.used_at = datetime.now(UTC)
    expires_at = datetime.now(UTC) + REFRESH_TTL
    raw, replacement = _new_refresh_row(
        db,
        user_id=user.id,
        platform=token.platform,
        family_id=token.family_id,
        expires_at=expires_at,
    )
    token.replaced_by_id = replacement.id
    _revoke(db, token, REVOKE_ROTATED)
    db.flush()
    return _issue_access(user), raw, expires_at


def _revoke_family(db: Session, family_id: str, reason: str) -> None:
    for token in db.scalars(
        select(RefreshToken).where(
            RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None)
        )
    ):
        _revoke(db, token, reason)
    db.flush()


def revoke_all(db: Session, user_id: int, reason: str) -> None:
    for token in db.scalars(
        select(RefreshToken).where(
            RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None)
        )
    ):
        _revoke(db, token, reason)
    db.flush()


def logout(db: Session, *, raw_token: str) -> None:
    token = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw_token)))
    if token is not None:
        _revoke_family(db, token.family_id, REVOKE_LOGOUT)


# --- email verification and password reset ----------------------------------


def resend_verification(db: Session, *, user: User) -> None:
    """Send a fresh verification link, invalidating any earlier one.

    A resend means the previous email never arrived, so the old link must stop
    working: two live links would let a stale mailbox confirm an address the
    student no longer controls.
    """
    if user.email_verified:
        raise ApiError(409, "already_verified", "Your email is already confirmed.")
    db.execute(
        update(EmailToken)
        .where(
            EmailToken.user_id == user.id,
            EmailToken.purpose == "verify_email",
            EmailToken.used_at.is_(None),
        )
        .values(used_at=datetime.now(UTC))
    )
    _send_verification(db, user)


def verify_email(db: Session, *, raw_token: str) -> User:
    token = _consume_email_token(db, raw_token, purpose="verify_email")
    user = db.get(User, token.user_id)
    if user is None:
        raise ApiError(400, "invalid_token", "This link is no longer valid.")
    user.email_verified = True
    db.flush()
    audit.record(db, action="email.verified", target_type="user", target_id=user.id)
    return user


def request_password_reset(db: Session, *, email: str) -> None:
    """Always silent: a different response would reveal whether an account exists."""
    user = db.scalar(select(User).where(User.email == normalise_email(email)))
    if user is None or user.is_deleted:
        return
    raw, token_hash = new_email_token()
    db.add(
        EmailToken(
            user_id=user.id,
            purpose="reset_password",
            token_hash=token_hash,
            expires_at=datetime.now(UTC) + RESET_TOKEN_TTL,
        )
    )
    db.flush()
    enqueue(
        db,
        "send_email",
        {
            "to": user.email,
            "subject": "Reset your Nelavista password",
            "body": f"Reset your password: {web_link(f'/auth/reset?token={raw}')}",
        },
    )


def reset_password(db: Session, *, raw_token: str, new_password: str) -> User:
    token = _consume_email_token(db, raw_token, purpose="reset_password")
    user = db.get(User, token.user_id)
    if user is None or user.is_deleted:
        raise ApiError(400, "invalid_token", "This link is no longer valid.")
    user.password_hash = _hash_password(new_password)
    revoke_all(db, user.id, REVOKE_PASSWORD_RESET)
    db.flush()
    audit.record(db, action="password.reset", target_type="user", target_id=user.id)
    return user


def _consume_email_token(db: Session, raw_token: str, *, purpose: str) -> EmailToken:
    if purpose not in EMAIL_TOKEN_PURPOSES:
        raise ValueError(f"unknown email token purpose: {purpose}")
    token = db.scalar(select(EmailToken).where(EmailToken.token_hash == hash_token(raw_token)))
    if token is None or token.purpose != purpose or token.used_at is not None:
        raise ApiError(400, "invalid_token", "This link is no longer valid.")
    expires_at = token.expires_at if token.expires_at.tzinfo else token.expires_at.replace(tzinfo=UTC)
    if expires_at <= datetime.now(UTC):
        raise ApiError(400, "invalid_token", "This link has expired. Request a new one.")
    token.used_at = datetime.now(UTC)
    db.flush()
    return token


# --- Google ------------------------------------------------------------------


def login_with_google(
    db: Session, *, id_token: str, platform: str = "ios"
) -> tuple[User, str, str, datetime]:
    """Verify a Google ID token, then link or create the account by `google_sub`.

    Verification is server-side against Google's tokeninfo endpoint, which checks
    signature, issuer and expiry. The email is trusted only because Google has
    already verified it — the same rule as V1's OAuth callback.
    """
    claims = verify_google_id_token(id_token)
    sub = claims["sub"]
    email = normalise_email(claims["email"])

    user = db.scalar(select(User).where(User.google_sub == sub))
    if user is None:
        user = db.scalar(select(User).where(User.email == email))
        if user is not None and user.google_sub not in (None, sub):
            raise ApiError(409, "account_conflict", "This email is linked to another sign-in method.")
        if user is None:
            user = User(
                email=email,
                username=_unique_username(db, email),
                google_sub=sub,
                name=claims.get("name"),
                email_verified=True,
                role_id=_student_role_id(db),
            )
            db.add(user)
            db.flush()
            db.add(UserProfile(user_id=user.id, display_name=claims.get("name") or user.username))
            audit.record(
                db, action="account.created_google", target_type="user", target_id=user.id
            )
        else:
            user.google_sub = sub
            user.email_verified = True
    user.last_login = datetime.now(UTC)
    db.flush()
    access, refresh, expires = issue_session(db, user, platform=platform)
    return user, access, refresh, expires


def _unique_username(db: Session, email: str) -> str:
    base = email.split("@")[0][:60] or "student"
    candidate = base
    suffix = 0
    while db.scalar(select(User.id).where(User.username == candidate)) is not None:
        suffix += 1
        candidate = f"{base}{suffix}"
    return candidate


def verify_google_id_token(id_token: str) -> dict[str, Any]:
    import httpx

    settings = get_settings()
    if not settings.GOOGLE_CLIENT_ID:
        raise ApiError(503, "google_disabled", "Google sign-in is not configured.")
    try:
        response = httpx.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
            timeout=5.0,
        )
    except httpx.HTTPError as exc:
        raise ApiError(503, "google_unavailable", "Google sign-in is unavailable.") from exc
    if response.status_code != 200:
        raise ApiError(401, "invalid_google_token", "Google sign-in failed. Try again.")
    claims = response.json()
    if claims.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise ApiError(401, "invalid_google_token", "Google sign-in failed. Try again.")
    if claims.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
        raise ApiError(401, "invalid_google_token", "Google sign-in failed. Try again.")
    if claims.get("email_verified") not in {"true", True} or not claims.get("email"):
        raise ApiError(401, "google_email_unverified", "Verify your Google email first.")
    return claims


# --- deletion ----------------------------------------------------------------


def delete_account(db: Session, *, user: User, reason: str | None = None) -> None:
    """Anonymise and deactivate. Rows that explain money or audit stay."""
    now = datetime.now(UTC)
    revoke_all(db, user.id, REVOKE_ACCOUNT_DELETED)
    user.is_deleted = True
    user.deleted_at = now
    user.email = f"deleted-{user.id}@deleted.invalid"
    user.username = f"deleted-{user.id}"
    user.name = None
    user.google_sub = None
    user.password_hash = None
    db.flush()
    audit.record(
        db,
        action="account.deleted",
        actor_user_id=user.id,
        target_type="user",
        target_id=user.id,
        reason=reason,
    )


# --- consent -----------------------------------------------------------------


def record_consent(
    db: Session, *, user: User, kind: str, document_version: str, granted: bool
) -> Consent:
    if kind not in CONSENT_KINDS:
        raise ApiError(400, "unknown_consent", "Unknown consent kind.")
    consent = Consent(
        user_id=user.id, kind=kind, document_version=document_version, granted=granted
    )
    db.add(consent)
    db.flush()
    return consent
