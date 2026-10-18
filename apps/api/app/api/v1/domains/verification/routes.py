"""Verification endpoints: assessments, practical tasks and the transcript (Phase 3)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.api.v1.domains.verification.schemas import (
    AssessmentListOut,
    AttemptOut,
    AttemptResultOut,
    AttemptSubmitIn,
    ReviewOut,
    TranscriptOut,
    VerificationOut,
)
from app.core import flags, observability
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.identity import User
from app.models.skills import Skill
from app.models.verification import VERIFIED, PracticalSubmission, VerificationRecord
from app.services.verification import assessments, state, transcript

router = APIRouter(
    prefix="/verification",
    tags=["verification"],
    dependencies=[Depends(require_flag(flags.SKILLS_JOURNEY))],
)


class PracticalIn(BaseModel):
    payload: dict = Field(default_factory=dict)
    client_key: str | None = Field(default=None, max_length=64)


class PracticalReviewIn(BaseModel):
    score: int = Field(ge=0, le=100)
    passed: bool
    notes: str | None = Field(default=None, max_length=2000)


@router.get("", response_model=VerificationOut)
def my_verification(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    rows = db.execute(
        select(VerificationRecord, Skill)
        .join(Skill, Skill.id == VerificationRecord.skill_id)
        .where(VerificationRecord.user_id == user.id)
        .order_by(Skill.name)
    ).all()
    return {
        "skills": [
            {
                "skill_id": skill.id,
                "skill": skill.name,
                "slug": skill.slug,
                "status": record.status,
                "verified_at": record.verified_at,
                "last_evaluated_at": record.last_evaluated_at,
                "verified": record.status == VERIFIED,
            }
            for record, skill in rows
        ]
    }


@router.get("/transcript", response_model=TranscriptOut)
def my_transcript(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return transcript.get_transcript(db, user)


@router.get("/assessments", response_model=AssessmentListOut)
def list_assessments(
    skill_id: int | None = None,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return {"assessments": assessments.list_assessments(db, skill_id=skill_id)}


@router.post("/assessments/{slug}/start", response_model=AttemptOut)
def start_assessment(
    slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    payload = assessments.start_attempt(db, user, slug)
    db.commit()
    return payload


@router.post("/attempts/{attempt_id}/submit", response_model=AttemptResultOut)
def submit_assessment(
    attempt_id: int,
    payload: AttemptSubmitIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    result = assessments.submit_attempt(db, user, attempt_id, payload.answers)
    db.commit()
    if result.get("passed"):
        observability.capture(
            user.id,
            observability.EVENTS["assessment_passed"],
            {"attempt_id": attempt_id, "score": result["score"]},
        )
    return result


@router.get("/attempts/{attempt_id}", response_model=ReviewOut)
def review_assessment(
    attempt_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return assessments.review_attempt(db, user, attempt_id)


@router.get("/practical")
def list_practical(
    skill_id: int | None = None,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return {"tasks": assessments.list_practical_tasks(db, skill_id=skill_id)}


@router.post("/practical/{slug}", status_code=201)
def submit_practical(
    slug: str,
    payload: PracticalIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = assessments.submit_practical(
        db, user, slug=slug, payload=payload.payload, client_key=payload.client_key
    )
    db.commit()
    return {
        "id": row.id,
        "status": row.status,
        "submitted_at": row.submitted_at,
        "message": "Submitted for review.",
    }


@router.get("/practical/submissions")
def practical_queue(
    status: str = Query(default="submitted", max_length=16),
    limit: int = Query(default=50, ge=1, le=200),
    _staff: User = Depends(require_permission("review.read")),
    db: Session = Depends(get_db),
) -> dict:
    """The practical review queue; students never see other students' work."""
    rows = db.scalars(
        select(PracticalSubmission)
        .where(PracticalSubmission.status == status)
        .order_by(PracticalSubmission.id)
        .limit(limit)
    ).all()
    return {
        "submissions": [
            {
                "id": row.id,
                "practical_task_id": row.practical_task_id,
                "user_id": row.user_id,
                "status": row.status,
                "submitted_at": row.submitted_at,
            }
            for row in rows
        ]
    }


class OverrideIn(BaseModel):
    to_status: str = Field(min_length=5, max_length=16)
    reason: str = Field(min_length=3, max_length=255)


@router.post("/records/{user_id}/{skill_id}/override")
def override_verification(
    user_id: int,
    skill_id: int,
    payload: OverrideIn,
    actor: User = Depends(require_permission("review.write")),
    db: Session = Depends(get_db),
) -> dict:
    """A human override, always logged with its reason (PRD §5)."""
    student = db.get(User, user_id)
    if student is None or student.is_deleted:
        raise ApiError(404, "student_not_found", "That student does not exist.")
    record = state.ensure_record(db, user_id, skill_id)
    event = state.override(
        db, record=record, to_status=payload.to_status, actor=actor, reason=payload.reason
    )
    db.commit()
    return {
        "user_id": user_id,
        "skill_id": skill_id,
        "status": record.status,
        "event_id": event.id,
        "reason": event.reason,
    }


@router.post("/practical/submissions/{submission_id}/review")
def review_practical(
    submission_id: int,
    payload: PracticalReviewIn,
    reviewer: User = Depends(require_permission("review.write")),
    db: Session = Depends(get_db),
) -> dict:
    row = assessments.review_practical(
        db,
        reviewer,
        submission_id=submission_id,
        score=payload.score,
        passed=payload.passed,
        notes=payload.notes,
    )
    db.commit()
    return {
        "id": row.id,
        "status": row.status,
        "score": row.score,
        "passed": row.passed,
    }


__all__ = ["router", "state"]
