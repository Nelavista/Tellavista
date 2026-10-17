"""Opportunity and matching endpoints (Phases 4 and 7).

Student routes are gated by either the managed-work or external-opportunity flag,
because the model serves both and an unanswered "why don't I qualify" is the same
question in each. Ops routes sit behind the managed-work flag and `project.write`:
managed work is invitation-only, so a student never creates or edits an
opportunity, and external listings are moderated by our team.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_any_flag, require_flag
from app.core import flags
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.identity import User
from app.models.matching import OPPORTUNITY_TYPES
from app.models.talent import OpportunityApplication
from app.services.matching import engine, opportunities

router = APIRouter(
    prefix="/opportunities",
    tags=["opportunities"],
    dependencies=[Depends(require_any_flag(flags.MANAGED_WORKFORCE, flags.EXTERNAL_OPPORTUNITIES))],
)


class RequirementIn(BaseModel):
    kind: str
    skill_id: int | None = None
    minimum_value: str | None = Field(default=None, max_length=120)
    is_mandatory: bool = True
    description: str | None = Field(default=None, max_length=255)


class OpportunityIn(BaseModel):
    type: str
    slug: str = Field(min_length=2, max_length=120)
    title: str = Field(min_length=2, max_length=200)
    description: str = ""
    client_name: str | None = Field(default=None, max_length=200)
    department_id: int | None = None
    headcount: int | None = Field(default=None, ge=1)
    quality_standard: str | None = Field(default=None, max_length=200)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    rate_minor: int | None = Field(default=None, ge=0)
    starts_on: date | None = None
    ends_on: date | None = None
    requirements: list[RequirementIn] = Field(default_factory=list)


class OpportunityPatchIn(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    headcount: int | None = Field(default=None, ge=1)
    quality_standard: str | None = Field(default=None, max_length=200)
    status: str | None = Field(default=None, max_length=16)
    requirements: list[RequirementIn] | None = None


class ApplyIn(BaseModel):
    note: str | None = Field(default=None, max_length=1000)


class ApplicationStatusIn(BaseModel):
    status: str = Field(min_length=3, max_length=20)


def _requirements(items: list[RequirementIn]) -> list[dict]:
    return [item.model_dump() for item in items]


# --- student -----------------------------------------------------------------


@router.get("")
def list_opportunities(
    type: str | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Open opportunities with this student's own verdict on each."""
    rows = opportunities.list_open(db, type=type)
    return {"opportunities": [opportunities.detail_for_user(db, user, row) for row in rows]}


@router.get("/matches")
def my_matches(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """Eligible first, then by score; every row carries its reasons."""
    results = engine.list_matches(db, user)
    db.commit()
    return {
        "matches": results,
        "eligible_count": sum(1 for item in results if item["eligible"]),
    }


@router.get("/applications")
def my_applications(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"applications": opportunities.my_applications(db, user)}


@router.get("/{slug}")
def opportunity_detail(
    slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Includes "why you qualify" or exactly what is missing, with the closing step."""
    row = opportunities.get_opportunity(db, slug)
    detail = opportunities.detail_for_user(db, user, row)
    db.commit()
    return detail


@router.get("/{slug}/gaps")
def opportunity_gaps(
    slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = opportunities.get_opportunity(db, slug)
    return {"gaps": engine.gaps_for_user(db, user.id, row.id)}


@router.post("/{slug}/apply", status_code=201)
def apply_to_external(
    slug: str,
    payload: ApplyIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Only external opportunities accept an application; managed work is invited."""
    application = opportunities.apply_external(db, user, slug=slug, note=payload.note)
    db.commit()
    return {
        "id": application.id,
        "status": application.status,
        "note": application.note,
    }


# --- ops ---------------------------------------------------------------------


# Ops routes live on the same router (one prefix, no path ambiguity) and carry
# their guard on each decorator. The flag keeps half-built admin screens out of
# prod; the permission keeps students out of them.
OPS_GUARD = [
    Depends(require_flag(flags.MANAGED_WORKFORCE)),
    Depends(require_permission("project.write")),
]


@router.get("/{slug}/applications", dependencies=OPS_GUARD)
def list_applications(
    slug: str,
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    _staff: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    opportunity = opportunities.get_opportunity(db, slug)
    stmt = (
        select(OpportunityApplication)
        .where(OpportunityApplication.opportunity_id == opportunity.id)
        .order_by(OpportunityApplication.id.desc())
        .limit(limit)
    )
    if status is not None:
        stmt = stmt.where(OpportunityApplication.status == status)
    rows = db.scalars(stmt).all()
    return {
        "opportunity": {"id": opportunity.id, "slug": opportunity.slug},
        "applications": [
            {
                "id": application.id,
                "status": application.status,
                "user_id": application.user_id,
                "note": application.note,
            }
            for application in rows
        ],
    }


@router.post("/applications/{application_id}/status", dependencies=OPS_GUARD)
def set_application_status(
    application_id: int,
    payload: ApplicationStatusIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    application = opportunities.set_application_status(db, actor, application_id, payload.status)
    db.commit()
    return {"id": application.id, "status": application.status}


@router.post("", status_code=201, dependencies=OPS_GUARD)
def create_opportunity(
    payload: OpportunityIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    if payload.type not in OPPORTUNITY_TYPES:
        raise ApiError(400, "invalid_opportunity_type", "Use managed or external.")
    row = opportunities.create_opportunity(
        db,
        actor,
        type=payload.type,
        slug=payload.slug,
        title=payload.title,
        description=payload.description,
        client_name=payload.client_name,
        department_id=payload.department_id,
        headcount=payload.headcount,
        quality_standard=payload.quality_standard,
        currency=payload.currency,
        rate_minor=payload.rate_minor,
        starts_on=payload.starts_on,
        ends_on=payload.ends_on,
        requirements=_requirements(payload.requirements),
    )
    db.commit()
    return {"id": row.id, "slug": row.slug, "status": row.status}


@router.patch("/{slug}", dependencies=OPS_GUARD)
def update_opportunity(
    slug: str,
    payload: OpportunityPatchIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    row = opportunities.get_opportunity(db, slug)
    opportunities.update_opportunity(
        db,
        actor,
        row,
        title=payload.title,
        description=payload.description,
        headcount=payload.headcount,
        quality_standard=payload.quality_standard,
        status=payload.status,
        requirements=(
            _requirements(payload.requirements) if payload.requirements is not None else None
        ),
    )
    db.commit()
    return {"id": row.id, "slug": row.slug, "status": row.status}


@router.get("/{slug}/candidates", dependencies=OPS_GUARD)
def match_candidates(
    slug: str,
    limit: int = Query(default=200, ge=1, le=500),
    _staff: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    """Who qualifies, and exactly why the rest do not."""
    row = opportunities.get_opportunity(db, slug)
    results = engine.match_candidates(db, row, limit=limit)
    db.commit()
    return {
        "opportunity": {"id": row.id, "slug": row.slug, "title": row.title},
        "candidates": results,
        "eligible_count": sum(1 for item in results if item["eligible"]),
    }


__all__ = ["router"]
