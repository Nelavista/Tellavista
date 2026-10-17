"""Talent profile endpoints (Phase 7).

The profile is computed from evidence, so there is no "edit my profile" route for
skills or history: a student can change their availability and the scopes they
share, never the proof itself. Share links are the student's consent boundary:
each one is scoped, expiring and revocable, and the token is only ever returned
once, at creation.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.core import flags
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.identity import User
from app.services.talent import profile as talent

router = APIRouter(
    prefix="/talent",
    tags=["talent"],
    dependencies=[Depends(require_flag(flags.TALENT_PROFILE))],
)


class ShareIn(BaseModel):
    label: str | None = Field(default=None, max_length=120)
    scopes: list[str] | None = None
    ttl_days: int = Field(default=talent.DEFAULT_TTL_DAYS, ge=1, le=talent.MAX_TTL_DAYS)


@router.get("/me")
def my_profile(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return talent.build_profile(db, user)


@router.get("/me/transcript")
def my_transcript(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return talent.transcript_only(db, user)


@router.get("/me/shares")
def list_shares(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"shares": talent.list_shares(db, user)}


@router.post("/me/shares", status_code=201)
def create_share(
    payload: ShareIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    share, token = talent.create_share(
        db, user, label=payload.label, scopes=payload.scopes, ttl_days=payload.ttl_days
    )
    db.commit()
    return {
        "id": share.id,
        "label": share.label,
        "scopes": share.scopes,
        "expires_at": share.expires_at,
        # Shown once. Only the hash is stored, so it cannot be recovered later.
        "token": token,
    }


@router.post("/me/shares/{share_id}/revoke")
def revoke_share(
    share_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    share = talent.revoke_share(db, user, share_id)
    db.commit()
    return {"id": share.id, "revoked_at": share.revoked_at}


@router.get("/share/{token}")
def public_share(token: str, db: Session = Depends(get_db)) -> dict:
    """Public by design: the token is the grant, and it can be revoked or expire."""
    if len(token) < 20 or len(token) > 200:
        raise ApiError(404, "share_not_found", "This link is no longer active.")
    return talent.view_share(db, token)


@router.get("/students/{user_id}")
def student_profile(
    user_id: int,
    _staff: User = Depends(require_permission("talent.read")),
    db: Session = Depends(get_db),
) -> dict:
    """The internal ops view: same evidence, with the private context included."""
    user = db.get(User, user_id)
    if user is None or user.is_deleted:
        raise ApiError(404, "student_not_found", "That student does not exist.")
    return talent.build_profile(db, user, internal=True)


__all__ = ["router"]
