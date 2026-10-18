"""Identity routes (ADR-0009).

Web and admin authenticate with **cookies** (httpOnly refresh + CSRF pair);
native clients authenticate with **bearer tokens** (refresh in secure storage).
The same service serves both, so the rules cannot drift between platforms.
"""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.v1.domains.identity.schemas import (
    ConsentIn,
    GoogleIn,
    LoginIn,
    MeOut,
    MessageOut,
    RefreshIn,
    ResetPasswordIn,
    ResetRequestIn,
    SignupIn,
    TokenOut,
    VerifyEmailIn,
)
from app.core import ratelimit
from app.core.config import get_settings
from app.core.errors import ApiError
from app.core.security import REFRESH_TTL
from app.db.session import get_db
from app.models.identity import User
from app.services.identity import auth

router = APIRouter(prefix="/auth", tags=["identity"])

REFRESH_COOKIE = "nv_refresh"
CSRF_COOKIE = "nv_csrf"
COOKIE_PATH = "/"


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _set_cookies(response: Response, refresh_token: str) -> None:
    settings = get_settings()
    secure = not settings.is_local
    max_age = int(REFRESH_TTL.total_seconds())
    response.set_cookie(
        REFRESH_COOKIE,
        refresh_token,
        max_age=max_age,
        httponly=True,
        secure=secure,
        samesite="lax",
        path=COOKIE_PATH,
    )
    # Double-submit CSRF: readable by the app, required as a header on refresh.
    response.set_cookie(
        CSRF_COOKIE,
        secrets.token_urlsafe(24),
        max_age=max_age,
        httponly=False,
        secure=secure,
        samesite="lax",
        path=COOKIE_PATH,
    )


def _clear_cookies(response: Response) -> None:
    response.delete_cookie(REFRESH_COOKIE, path=COOKIE_PATH)
    response.delete_cookie(CSRF_COOKIE, path=COOKIE_PATH)


def _session_response(
    user: User, access: str, refresh: str, expires_at, platform: str, response: Response
) -> TokenOut:
    if platform in {"web", "admin"}:
        _set_cookies(response, refresh)
        return TokenOut(access_token=access, expires_at=expires_at)
    return TokenOut(access_token=access, refresh_token=refresh, expires_at=expires_at)


@router.post("/signup", response_model=TokenOut, status_code=201)
def signup(
    payload: SignupIn, request: Request, response: Response, db: Session = Depends(get_db)
) -> TokenOut:
    ratelimit.check(f"signup:{_client_ip(request)}", limit=5, window_seconds=60)
    user, access, refresh, expires = auth.register(
        db,
        email=payload.email,
        username=payload.username,
        password=payload.password,
        name=payload.name,
        accept_terms=payload.accept_terms,
        platform=payload.platform,
    )
    db.commit()
    return _session_response(user, access, refresh, expires, payload.platform, response)


@router.post("/login", response_model=TokenOut)
def login(
    payload: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)
) -> TokenOut:
    ratelimit.check(f"login:{_client_ip(request)}", limit=10, window_seconds=60)
    user = auth.authenticate(db, email=payload.email, password=payload.password)
    access, refresh, expires = auth.issue_session(db, user, platform=payload.platform)
    db.commit()
    return _session_response(user, access, refresh, expires, payload.platform, response)


@router.post("/refresh", response_model=TokenOut)
def refresh(
    payload: RefreshIn, request: Request, response: Response, db: Session = Depends(get_db)
) -> TokenOut:
    cookie_flow = payload.refresh_token is None
    raw = payload.refresh_token or request.cookies.get(REFRESH_COOKIE)
    if not raw:
        raise ApiError(401, "not_authenticated", "Sign in to continue.")
    if cookie_flow:
        header = request.headers.get("X-CSRF-Token")
        if not header or header != request.cookies.get(CSRF_COOKIE):
            raise ApiError(403, "csrf_failed", "Refresh the page and try again.")

    access, new_refresh, expires = auth.rotate(db, raw_token=raw)
    db.commit()
    if cookie_flow:
        _set_cookies(response, new_refresh)
        return TokenOut(access_token=access, expires_at=expires)
    return TokenOut(access_token=access, refresh_token=new_refresh, expires_at=expires)


@router.post("/logout", response_model=MessageOut)
def logout(
    payload: RefreshIn, request: Request, response: Response, db: Session = Depends(get_db)
) -> MessageOut:
    raw = payload.refresh_token or request.cookies.get(REFRESH_COOKIE)
    if raw:
        auth.logout(db, raw_token=raw)
        db.commit()
    _clear_cookies(response)
    return MessageOut(message="Signed out.")


@router.get("/me", response_model=MeOut)
def me(user: User = Depends(get_current_user)) -> MeOut:
    return MeOut(
        id=user.id,
        email=user.email,
        username=user.username,
        name=user.name,
        email_verified=user.email_verified,
        role=user.role.code if user.role else None,
        preferred_path=user.profile.preferred_path if user.profile else None,
    )


@router.post("/email/verify", response_model=MeOut)
def verify_email(payload: VerifyEmailIn, db: Session = Depends(get_db)) -> MeOut:
    user = auth.verify_email(db, raw_token=payload.token)
    db.commit()
    return MeOut(
        id=user.id,
        email=user.email,
        username=user.username,
        name=user.name,
        email_verified=user.email_verified,
        role=user.role.code if user.role else None,
        preferred_path=user.profile.preferred_path if user.profile else None,
    )


@router.post("/email/verify/resend", response_model=MessageOut)
def resend_verification(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> MessageOut:
    """Authenticated on purpose: no address in the body, so no enumeration and
    no way to mail someone who did not ask. Rate-limited per account."""
    ratelimit.check(f"verify-resend:{user.id}", limit=3, window_seconds=300)
    auth.resend_verification(db, user=user)
    db.commit()
    return MessageOut(message="Verification email sent. Check your inbox.")


@router.post("/password/reset-request", response_model=MessageOut)
def request_password_reset(
    payload: ResetRequestIn, request: Request, db: Session = Depends(get_db)
) -> MessageOut:
    ratelimit.check(f"reset:{_client_ip(request)}", limit=5, window_seconds=300)
    auth.request_password_reset(db, email=payload.email)
    db.commit()
    # Always the same answer, whatever the email is.
    return MessageOut(message="If that email has an account, a reset link is on its way.")


@router.post("/password/reset", response_model=MessageOut)
def reset_password(payload: ResetPasswordIn, db: Session = Depends(get_db)) -> MessageOut:
    auth.reset_password(db, raw_token=payload.token, new_password=payload.password)
    db.commit()
    return MessageOut(message="Password updated. Sign in with your new password.")


@router.post("/google", response_model=TokenOut)
def google(
    payload: GoogleIn, response: Response, db: Session = Depends(get_db)
) -> TokenOut:
    user, access, refresh, expires = auth.login_with_google(
        db, id_token=payload.id_token, platform=payload.platform
    )
    db.commit()
    return _session_response(user, access, refresh, expires, payload.platform, response)


@router.post("/consent", response_model=MessageOut)
def consent(
    payload: ConsentIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> MessageOut:
    auth.record_consent(
        db,
        user=user,
        kind=payload.kind,
        document_version=payload.document_version,
        granted=payload.granted,
    )
    db.commit()
    return MessageOut(message="Consent recorded.")


@router.delete("/account", response_model=MessageOut)
def delete_account(
    response: Response,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageOut:
    auth.delete_account(db, user=user)
    db.commit()
    _clear_cookies(response)
    return MessageOut(message="Your account has been deleted.")
