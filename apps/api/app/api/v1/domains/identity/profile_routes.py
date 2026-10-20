"""Profile, Choose Path and the student's own data endpoints (Phase 1)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.v1.domains.identity.schemas import (
    AvailabilityIn,
    AvailabilityOut,
    CampusOut,
    LanguagesIn,
    LanguagesOut,
    MessageOut,
    NotificationListOut,
    NotificationReadIn,
    NotificationReadOut,
    PathIn,
    ProfileOut,
    ProfileUpdateIn,
    PushDeviceIn,
    PushDeviceListOut,
    PushDeviceOut,
)
from app.core.errors import ApiError
from app.core.time import utcnow
from app.db.session import get_db
from app.models.engagement import PushDevice
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


@router.get("/languages", response_model=LanguagesOut)
def get_languages(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> LanguagesOut:
    from sqlalchemy import select

    from app.models.identity import UserLanguage

    rows = db.scalars(
        select(UserLanguage).where(UserLanguage.user_id == user.id).order_by(UserLanguage.language)
    ).all()
    return LanguagesOut(
        languages=[{"language": row.language, "level": row.level} for row in rows]
    )


@router.put("/languages", response_model=LanguagesOut)
def set_languages(
    payload: LanguagesIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LanguagesOut:
    rows = profile_service.set_languages(
        db, user, [(item.language, item.level) for item in payload.languages]
    )
    db.commit()
    return LanguagesOut(
        languages=[{"language": row.language, "level": row.level} for row in rows]
    )


@router.get("/availability", response_model=AvailabilityOut)
def get_availability(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> AvailabilityOut:
    from sqlalchemy import select

    from app.models.identity import UserAvailability

    row = db.scalar(select(UserAvailability).where(UserAvailability.user_id == user.id))
    return AvailabilityOut(
        hours_per_week=row.hours_per_week if row else None,
        available_from=row.available_from if row else None,
        note=row.note if row else None,
    )


@router.put("/availability", response_model=AvailabilityOut)
def set_availability(
    payload: AvailabilityIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AvailabilityOut:
    row = profile_service.set_availability(
        db,
        user,
        hours_per_week=payload.hours_per_week,
        available_from=payload.available_from,
        note=payload.note,
    )
    db.commit()
    return AvailabilityOut(
        hours_per_week=row.hours_per_week,
        available_from=row.available_from,
        note=row.note,
    )


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


@router.get("/notifications", response_model=NotificationListOut)
def get_notifications(
    unread_only: bool = False,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NotificationListOut:
    """In-app notifications. Push delivers the same rows; a failed push retries."""
    return NotificationListOut(
        notifications=notifications.list_notifications(db, user, unread_only=unread_only)
    )


@router.post("/notifications/read", response_model=NotificationReadOut)
def read_notifications(
    payload: NotificationReadIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NotificationReadOut:
    updated = notifications.mark_read(db, user, payload.ids)
    db.commit()
    return NotificationReadOut(updated=updated)


@router.get("/push-devices", response_model=PushDeviceListOut)
def list_push_devices(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> PushDeviceListOut:
    from sqlalchemy import select

    rows = db.scalars(
        select(PushDevice)
        .where(PushDevice.user_id == user.id, PushDevice.revoked_at.is_(None))
        .order_by(PushDevice.id)
    ).all()
    return PushDeviceListOut(
        devices=[
            {
                "id": row.id,
                "token": row.token,
                "platform": row.platform,
                "last_seen_at": row.last_seen_at,
            }
            for row in rows
        ]
    )


@router.post("/push-devices", response_model=PushDeviceOut, status_code=201)
def register_push_device(
    payload: PushDeviceIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PushDeviceOut:
    """Register an install. A token that moved accounts is reassigned, never doubled."""
    from sqlalchemy import select

    if payload.platform not in {"ios", "android", "web"}:
        raise ApiError(400, "invalid_platform", "Use ios, android or web.")
    row = db.scalar(select(PushDevice).where(PushDevice.token == payload.token))
    if row is None:
        row = PushDevice(token=payload.token, platform=payload.platform, user_id=user.id)
        db.add(row)
    else:
        # Another account signed in on this phone: delivery follows the newest
        # owner, because the previous owner can no longer read this device.
        row.user_id = user.id
        row.platform = payload.platform
        row.revoked_at = None
    row.last_seen_at = utcnow()
    db.commit()
    return PushDeviceOut(
        id=row.id, token=row.token, platform=row.platform, last_seen_at=row.last_seen_at
    )


@router.delete("/push-devices/{device_id}", response_model=MessageOut)
def unregister_push_device(
    device_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageOut:
    row = db.get(PushDevice, device_id)
    if row is None or row.user_id != user.id:
        raise ApiError(404, "push_device_not_found", "That device is not registered.")
    db.delete(row)
    db.commit()
    return MessageOut(message="This device will no longer receive notifications.")


@router.post("/onboarding/complete", response_model=MessageOut)
def complete_onboarding(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> MessageOut:
    profile_service.complete_onboarding(db, user)
    db.commit()
    return MessageOut(message="Onboarding complete.")
