"""Talent profile endpoints (Phase 7 / B13).

The profile is computed from evidence, so there is no "edit my profile" route for
skills or history: a student can change their availability and the scopes they
share, never the proof itself. Share links are the student's consent boundary:
each one is scoped, expiring and revocable, and the token is only ever returned
once, at creation.

Every route now declares its response model (A3). The public share and the
internal ops view use the same shape; only the scopes and `account` differ, so a
screen written against one works for the other.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.api.v1.domains.talent.schemas import (
    ShareCreatedOut,
    ShareIn,
    ShareListOut,
    ShareRevokedOut,
    TalentProfileOut,
    TalentTranscriptOut,
)
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


@router.get("/me", response_model=TalentProfileOut)
def my_profile(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    # `owner=True`: a private profile is still visible to the person deciding
    # what to share. It is the public share that stays blocked.
    return talent.build_profile(db, user, owner=True)


@router.get("/me/transcript", response_model=TalentTranscriptOut)
def my_transcript(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return talent.transcript_only(db, user)


@router.get("/me/shares", response_model=ShareListOut)
def list_shares(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"shares": talent.list_shares(db, user)}


@router.post("/me/shares", status_code=201, response_model=ShareCreatedOut)
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


@router.post("/me/shares/{share_id}/revoke", response_model=ShareRevokedOut)
def revoke_share(
    share_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    share = talent.revoke_share(db, user, share_id)
    db.commit()
    return {"id": share.id, "revoked_at": share.revoked_at}


@router.get("/share/{token}", response_model=TalentProfileOut)
def public_share(token: str, db: Session = Depends(get_db)) -> dict:
    """Public by design: the token is the grant, and it can be revoked or expire."""
    if len(token) < 20 or len(token) > 200:
        raise ApiError(404, "share_not_found", "This link is no longer active.")
    return talent.view_share(db, token)


@router.get("/students/{user_id}", response_model=TalentProfileOut)
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
