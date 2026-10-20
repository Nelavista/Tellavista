"""Platform policy endpoints (G1–G5).

The read-only config is public because a signed-out visitor still needs to know
which currency a price is in and what the working-age rules are. Everything that
changes policy requires `settings.write`, which only `super_admin` holds by
default: currency and payout thresholds are not an ops-editor convenience.

Changes are audited with the before/after values. The contributor terms body is
audited by length, never by content, so the audit trail does not become a second
copy of a document that is already in `platform_settings`.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.v1.domains.platform.schemas import (
    EligibilityOut,
    PlatformConfigOut,
    PlatformSettingsIn,
    PlatformSettingsOut,
)
from app.core.authz import require_permission
from app.db.session import get_db
from app.models.identity import User
from app.services.platform import settings as policy

router = APIRouter(prefix="/platform", tags=["platform"])


@router.get("/config", response_model=PlatformConfigOut)
def config(db: Session = Depends(get_db)) -> PlatformConfigOut:
    """Public: the current currency, ages, terms version and curriculum owner."""
    row = policy.get_platform_settings(db)
    db.commit()
    return PlatformConfigOut(**policy.public_config(row))


@router.get("/settings", response_model=PlatformSettingsOut)
def read_settings(
    _actor: User = Depends(require_permission("settings.read")),
    db: Session = Depends(get_db),
) -> PlatformSettingsOut:
    row = policy.get_platform_settings(db)
    db.commit()
    return PlatformSettingsOut(**policy.admin_payload(row))


@router.patch("/settings", response_model=PlatformSettingsOut)
def write_settings(
    payload: PlatformSettingsIn,
    actor: User = Depends(require_permission("settings.write")),
    db: Session = Depends(get_db),
) -> PlatformSettingsOut:
    row = policy.update_platform_settings(db, actor, payload.changes())
    db.commit()
    db.refresh(row)
    return PlatformSettingsOut(**policy.admin_payload(row))


@router.get("/me/eligibility", response_model=EligibilityOut)
def my_eligibility(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> EligibilityOut:
    """What is still missing before this student can accept paid work."""
    result = policy.eligibility(db, user)
    db.commit()
    return EligibilityOut(**result)


__all__ = ["router"]
