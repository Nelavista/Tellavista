"""Work delivery and quality-control endpoints (Phase 5).

Two audiences, one module, because the work and its review must agree:

* **Students** see only their own assignments and submissions. Object-level
  authorisation is enforced in `delivery._assignment_for`, so another student's
  assignment id is a 404, not a 403 that confirms it exists.
* **Reviewers and ops** run cohorts, assign work and review submissions. Their
  routes sit behind `review.write` or `project.write`.

Every submission carries a client-generated idempotency key, accepted either in
the `Idempotency-Key` header or the body, so an offline retry stores one row.
"""
from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, Header, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.core import flags, observability
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.engagement import Message
from app.models.identity import User
from app.models.work import Assignment, Cohort
from app.services import notifications
from app.services.matching import opportunities
from app.services.work import cohorts, delivery
from app.services.work import quality as quality_service

router = APIRouter(
    prefix="/work",
    tags=["work"],
    dependencies=[Depends(require_flag(flags.MANAGED_WORKFORCE))],
)


class SubmissionIn(BaseModel):
    payload: dict = Field(default_factory=dict)
    client_key: str | None = Field(default=None, max_length=64)


class SyncItem(BaseModel):
    assignment_id: int
    payload: dict = Field(default_factory=dict)
    client_key: str = Field(min_length=1, max_length=64)


class SyncIn(BaseModel):
    items: list[SyncItem] = Field(default_factory=list, max_length=50)


class ProjectIn(BaseModel):
    opportunity_slug: str
    slug: str = Field(min_length=2, max_length=120)
    title: str = Field(min_length=2, max_length=200)
    starts_on: date | None = None
    ends_on: date | None = None
    status: str = Field(default="active", max_length=16)


class CohortIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    capacity: int | None = Field(default=None, ge=1)


class InviteIn(BaseModel):
    user_ids: list[int] = Field(min_length=1, max_length=500)


class RespondIn(BaseModel):
    accept: bool


class RemoveIn(BaseModel):
    member_id: int
    reason: str = Field(min_length=3, max_length=255)


class AssignmentIn(BaseModel):
    user_id: int
    title: str = Field(min_length=2, max_length=200)
    template_id: int | None = None
    cohort_id: int | None = None
    due_at: datetime | None = None


class ReviewIn(BaseModel):
    verdict: str = Field(min_length=6, max_length=16)
    score: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=4000)
    is_override: bool = False
    reason: str | None = Field(default=None, max_length=255)


class StandardIn(BaseModel):
    name: str | None = Field(default=None, max_length=160)
    instructions_md: str | None = None
    rubric: list | None = None
    pass_threshold: int | None = Field(default=None, ge=0, le=100)
    rules: dict | None = None


# --- student -----------------------------------------------------------------


@router.get("/assignments")
def my_assignments(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"assignments": cohorts.my_assignments(db, user)}


@router.get("/assignments/{assignment_id}")
def assignment_detail(
    assignment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return delivery.assignment_detail(db, user, assignment_id)


@router.post("/assignments/{assignment_id}/start")
def start_assignment(
    assignment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = delivery.start_assignment(db, user, assignment_id)
    db.commit()
    return {"id": row.id, "status": row.status}


@router.post("/assignments/{assignment_id}/submissions", status_code=201)
def submit_work(
    assignment_id: int,
    payload: SubmissionIn,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Submit once. A retry with the same key returns the stored submission."""
    row, created = delivery.submit_work(
        db,
        user,
        assignment_id=assignment_id,
        payload=payload.payload,
        client_key=idempotency_key or payload.client_key or "",
    )
    db.commit()
    if created:
        observability.capture(
            user.id,
            observability.EVENTS["task_submitted"],
            {"assignment_id": assignment_id, "submission_id": row.id},
        )
    return {
        "id": row.id,
        "status": row.status,
        "is_gold": row.is_gold,
        "submitted_at": row.submitted_at,
        "created": created,
        "message": "Submitted for review." if created else "This work was already submitted.",
    }


@router.post("/submissions/sync")
def sync_offline(
    payload: SyncIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Apply a queued batch. One bad item never discards the rest."""
    results = delivery.sync_offline(db, user, [item.model_dump() for item in payload.items])
    db.commit()
    return {
        "results": results,
        "applied": sum(1 for item in results if item.get("ok")),
        "failed": sum(1 for item in results if not item.get("ok")),
    }


@router.get("/submissions")
def my_submissions(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"submissions": delivery.my_submissions(db, user)}


@router.get("/quality")
def my_quality(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """The student's own quality record: what it is, and what produced it."""
    return quality_service.my_quality(db, user)


class MessageIn(BaseModel):
    body: str = Field(min_length=1, max_length=4000)


@router.get("/assignments/{assignment_id}/messages")
def my_messages(
    assignment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Work messages only: a message exists to move a task forward."""
    assignment = db.get(Assignment, assignment_id)
    if assignment is None or assignment.user_id != user.id:
        raise ApiError(404, "assignment_not_found", "That assignment does not exist.")
    rows = db.scalars(
        select(Message)
        .where(Message.assignment_id == assignment.id, Message.recipient_user_id == user.id)
        .order_by(Message.id)
    ).all()
    return {
        "messages": [
            {
                "id": row.id,
                "body": row.body,
                "sender_user_id": row.sender_user_id,
                "read_at": row.read_at,
                "created_at": row.created_at,
            }
            for row in rows
        ]
    }


@router.post("/cohorts/{cohort_id}/respond")
def respond_invite(
    cohort_id: int,
    payload: RespondIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    member = cohorts.respond_invite(db, user, cohort_id, accept=payload.accept)
    db.commit()
    return {"id": member.id, "status": member.status, "joined_at": member.joined_at}


# --- ops ---------------------------------------------------------------------


ops = APIRouter(tags=["work"], dependencies=[Depends(require_permission("project.write"))])


def _cohort(db: Session, cohort_id: int) -> Cohort:
    row = db.get(Cohort, cohort_id)
    if row is None:
        raise ApiError(404, "cohort_not_found", "That cohort does not exist.")
    return row


@ops.post("/projects", status_code=201)
def create_project(
    payload: ProjectIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    opportunity = opportunities.get_opportunity(db, payload.opportunity_slug)
    project = cohorts.create_project(
        db,
        actor,
        opportunity=opportunity,
        slug=payload.slug,
        title=payload.title,
        starts_on=payload.starts_on,
        ends_on=payload.ends_on,
        status=payload.status,
    )
    db.commit()
    return {"id": project.id, "slug": project.slug, "status": project.status}


@ops.get("/projects/{slug}")
def project_detail(
    slug: str,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    return cohorts.project_dashboard(db, project)


@ops.post("/projects/{slug}/cohorts", status_code=201)
def create_cohort(
    slug: str,
    payload: CohortIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    row = cohorts.create_cohort(db, actor, project=project, name=payload.name, capacity=payload.capacity)
    db.commit()
    return {"id": row.id, "name": row.name, "capacity": row.capacity, "status": row.status}


@ops.get("/cohorts/{cohort_id}")
def cohort_detail(
    cohort_id: int,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    return cohorts.cohort_detail(db, _cohort(db, cohort_id))


@ops.post("/cohorts/{cohort_id}/invites", status_code=201)
def invite(
    cohort_id: int,
    payload: InviteIn,
    actor: User = Depends(require_permission("cohort.write")),
    db: Session = Depends(get_db),
) -> dict:
    members = cohorts.invite(db, actor, cohort=_cohort(db, cohort_id), user_ids=payload.user_ids)
    db.commit()
    return {
        "members": [
            {"id": member.id, "user_id": member.user_id, "status": member.status}
            for member in members
        ]
    }


@ops.post("/cohorts/{cohort_id}/remove")
def remove_member(
    cohort_id: int,
    payload: RemoveIn,
    actor: User = Depends(require_permission("cohort.write")),
    db: Session = Depends(get_db),
) -> dict:
    member = cohorts.remove_member(db, actor, member_id=payload.member_id, reason=payload.reason)
    db.commit()
    return {"id": member.id, "status": member.status}


@ops.get("/cohorts/{cohort_id}/replacements")
def replacement_candidates(
    cohort_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    _actor: User = Depends(require_permission("cohort.write")),
    db: Session = Depends(get_db),
) -> dict:
    return {
        "candidates": cohorts.replacement_candidates(db, _cohort(db, cohort_id), limit=limit)
    }


@ops.post("/projects/{slug}/assignments", status_code=201)
def assign_task(
    slug: str,
    payload: AssignmentIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    row = cohorts.assign_task(
        db,
        actor,
        project=project,
        user_id=payload.user_id,
        title=payload.title,
        template_id=payload.template_id,
        cohort_id=payload.cohort_id,
        due_at=payload.due_at,
    )
    db.commit()
    return {"id": row.id, "status": row.status, "due_at": row.due_at}


@ops.post("/assignments/{assignment_id}/messages", status_code=201)
def send_message(
    assignment_id: int,
    payload: MessageIn,
    actor: User = Depends(require_permission("review.write")),
    db: Session = Depends(get_db),
) -> dict:
    assignment = db.get(Assignment, assignment_id)
    if assignment is None:
        raise ApiError(404, "assignment_not_found", "That assignment does not exist.")
    row = notifications.send_message(
        db,
        sender=actor,
        recipient_user_id=assignment.user_id,
        body=payload.body,
        assignment_id=assignment.id,
    )
    db.commit()
    return {"id": row.id, "created_at": row.created_at}


@ops.get("/review-queue")
def review_queue(
    limit: int = Query(default=50, ge=1, le=200),
    _actor: User = Depends(require_permission("review.read")),
    db: Session = Depends(get_db),
) -> dict:
    return {"queue": quality_service.review_queue(db, limit=limit)}


@ops.post("/submissions/{submission_id}/review")
def review_submission(
    submission_id: int,
    payload: ReviewIn,
    reviewer: User = Depends(require_permission("review.write")),
    db: Session = Depends(get_db),
) -> dict:
    review = quality_service.review_submission(
        db,
        reviewer,
        submission_id=submission_id,
        verdict=payload.verdict,
        score=payload.score,
        notes=payload.notes,
        is_override=payload.is_override,
        reason=payload.reason,
    )
    db.commit()
    return {
        "id": review.id,
        "submission_id": review.submission_id,
        "verdict": review.verdict,
        "score": review.score,
        "gold_correct": review.gold_correct,
    }


@ops.put("/projects/{slug}/quality-standard")
def set_standard(
    slug: str,
    payload: StandardIn,
    actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    standard = quality_service.set_standard(
        db,
        actor,
        project,
        name=payload.name,
        instructions_md=payload.instructions_md,
        rubric=payload.rubric,
        pass_threshold=payload.pass_threshold,
        rules=payload.rules,
    )
    db.commit()
    return {
        "id": standard.id,
        "name": standard.name,
        "pass_threshold": standard.pass_threshold,
        "rules": standard.rules,
    }


router.include_router(ops)

__all__ = ["router"]
