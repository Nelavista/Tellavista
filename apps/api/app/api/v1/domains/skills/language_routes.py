"""Language profile endpoints (African Languages Lab).

The profile is the student's self-reported claim, plus the capabilities their
verified skills actually back. This router is mounted before the `/skills/{slug}`
catalog route so `/skills/languages` is not read as a skill slug.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.api.v1.domains.skills.schemas import (
    LanguageProfileInList,
    LanguageProfileListOut,
)
from app.core import flags
from app.db.session import get_db
from app.models.identity import User
from app.services.skills import language_profile

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    dependencies=[Depends(require_flag(flags.SKILLS_JOURNEY))],
)


def _payload(db: Session, user: User) -> dict:
    return {
        "languages": language_profile.get_language_profile(db, user),
        "capabilities": [
            {"key": key, "label": label}
            for key, label in language_profile.CAPABILITIES
        ],
        "catalog": language_profile.catalog(),
    }


@router.get("/languages", response_model=LanguageProfileListOut)
def get_profile(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return _payload(db, user)


@router.put("/languages", response_model=LanguageProfileListOut)
def set_profile(
    payload: LanguageProfileInList,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    language_profile.set_language_profile(
        db, user, [entry.model_dump() for entry in payload.languages]
    )
    db.commit()
    return _payload(db, user)
