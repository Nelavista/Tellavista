"""Profile, Choose Path and the student's own data endpoints (Phase 1)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.v1.domains.identity.schemas import (
    AvailabilityIn,
    CampusOut,
    LanguagesIn,
    MessageOut,
    PathIn,
    ProfileOut,
    ProfileUpdateIn,
)
from app.db.session import get_db
from app.models.identity import User
from app.services import notifications
from app.services.academia import campus
from app.services.identity import profile as profile_service

router = APIRouter(prefix="/me", tags=["identity"])


def _profile_out(user: User) -> ProfileOut:
    row = user.profile
    return ProfileOut(
        display_name=row.display_name if row else None,
        bio=row.bio if row else None,
        location=row.location if row else None,
        avatar_url=row.avatar_url if row else None,
        locale=row.locale if row else "en",
        timezone=row.timezone if row else None,
        preferred_path=row.preferred_path if row else None,
        notify_email=row.notify_email if row else True,
        notify_push=row.notify_push if row else True,
        profile_visibility=row.profile_visibility if row else "private",
        date_of_birth=row.date_of_birth if row else None,
        onboarding_completed_at=row.onboarding_completed_at if row else None,
    )


@router.get("", response_model=ProfileOut)
def get_profile(user: User = Depends(get_current_user)) -> ProfileOut:
    return _profile_out(user)


@router.patch("", response_model=ProfileOut)
def update_profile(
    payload: ProfileUpdateIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileOut:
    profile_service.update_profile(
        db,
        user,
        display_name=payload.display_name,
        bio=payload.bio,
        location=payload.location,
        avatar_url=payload.avatar_url,
        locale=payload.locale,
        timezone=payload.timezone,
        notify_email=payload.notify_email,
        notify_push=payload.notify_push,
        profile_visibility=payload.profile_visibility,
        date_of_birth=payload.date_of_birth,
    )
    db.commit()
    db.refresh(user)
    return _profile_out(user)


@router.post("/path", response_model=ProfileOut)
def choose_path(
    payload: PathIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileOut:
    """Set or switch path. Switching never deletes learning, proof or earnings."""
    profile_service.choose_path(db, user, payload.path)
    db.commit()
    db.refresh(user)
    return _profile_out(user)


@router.get("/languages")
def get_languages(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    from sqlalchemy import select

    from app.models.identity import UserLanguage

    rows = db.scalars(
        select(UserLanguage).where(UserLanguage.user_id == user.id).order_by(UserLanguage.language)
    ).all()
    return {"languages": [{"language": row.language, "level": row.level} for row in rows]}


@router.put("/languages")
def set_languages(
    payload: LanguagesIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    rows = profile_service.set_languages(
        db, user, [(item.language, item.level) for item in payload.languages]
    )
    db.commit()
    return {"languages": [{"language": row.language, "level": row.level} for row in rows]}


@router.get("/availability")
def get_availability(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    from sqlalchemy import select

    from app.models.identity import UserAvailability

    row = db.scalar(select(UserAvailability).where(UserAvailability.user_id == user.id))
    return {
        "hours_per_week": row.hours_per_week if row else None,
        "available_from": row.available_from if row else None,
        "note": row.note if row else None,
    }


@router.put("/availability")
def set_availability(
    payload: AvailabilityIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = profile_service.set_availability(
        db,
        user,
        hours_per_week=payload.hours_per_week,
        available_from=payload.available_from,
        note=payload.note,
    )
    db.commit()
    return {
        "hours_per_week": row.hours_per_week,
        "available_from": row.available_from,
        "note": row.note,
    }


@router.get("/campus", response_model=CampusOut)
def get_campus(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return campus.campus_for(db, user)


@router.get("/export")
def export_data(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """Data export hook required by the app stores (ADR-0009)."""
    return profile_service.export_data(db, user)


@router.get("/notifications")
def get_notifications(
    unread_only: bool = False,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """In-app notifications. Push delivers the same rows; a failed push retries."""
    return {"notifications": notifications.list_notifications(db, user, unread_only=unread_only)}


class NotificationReadIn(BaseModel):
    ids: list[int] = Field(min_length=1, max_length=200)


@router.post("/notifications/read")
def read_notifications(
    payload: NotificationReadIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    updated = notifications.mark_read(db, user, payload.ids)
    db.commit()
    return {"updated": updated}


@router.post("/onboarding/complete", response_model=MessageOut)
def complete_onboarding(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> MessageOut:
    profile_service.complete_onboarding(db, user)
    db.commit()
    return MessageOut(message="Onboarding complete.")
