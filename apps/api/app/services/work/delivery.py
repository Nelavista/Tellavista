"""Work delivery: idempotent, offline-first submissions (PRD §8, ADR-0007).

A submission is keyed by a client-generated idempotency key. The mobile app saves
work locally first, then syncs; a retry after a dropped connection returns the
first submission instead of creating a duplicate. `sync_offline` accepts a batch so
a phone that was offline for an hour catches up in one request.

Gold tasks are chosen here, deterministically from the submission id, at the rate
configured on the project's quality standard. The expected answer is stored on the
submission for the reviewer and never returned to the student.
"""
from __future__ import annotations

import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User
from app.models.quality import DEFAULT_RULES
from app.models.skills import STATUS_PUBLISHED, TaskTemplate
from app.models.work import (
    ASSIGNMENT_APPROVED,
    ASSIGNMENT_IN_PROGRESS,
    ASSIGNMENT_SUBMITTED,
    SUBMISSION_SUBMITTED,
    Assignment,
    Project,
    Submission,
)
from app.services.notifications import notify
from app.services.work.quality import ensure_standard


def _assignment_for(db: Session, user: User, assignment_id: int) -> tuple[Assignment, Project]:
    assignment = db.get(Assignment, assignment_id)
    if assignment is None or assignment.user_id != user.id:
        # Another student's assignment is indistinguishable from a missing one.
        raise ApiError(404, "assignment_not_found", "That assignment does not exist.")
    project = db.get(Project, assignment.project_id)
    if project is None:
        raise ApiError(404, "project_not_found", "That project does not exist.")
    return assignment, project


def _should_be_gold(db: Session, project: Project, submission_id: int) -> bool:
    standard = ensure_standard(db, project)
    rate = int((standard.rules or DEFAULT_RULES).get("gold_rate_percent", 0))
    if rate <= 0:
        return False
    digest = hashlib.sha256(f"gold:{submission_id}".encode()).hexdigest()
    return int(digest[:8], 16) % 100 < rate


def submit_work(
    db: Session,
    user: User,
    *,
    assignment_id: int,
    payload: dict,
    client_key: str,
) -> tuple[Submission, bool]:
    """Submit once. Returns (submission, created)."""
    if not client_key or len(client_key) > 64:
        raise ApiError(
            400, "idempotency_key_required", "Include a 1-64 character idempotency key."
        )
    if not isinstance(payload, dict) or not payload:
        raise ApiError(400, "empty_submission", "Your work is empty; nothing was saved.")

    existing = db.scalar(
        select(Submission).where(Submission.idempotency_key == client_key)
    )
    if existing is not None:
        if existing.user_id != user.id:
            raise ApiError(409, "idempotency.key_reused", "This key belongs to another request.")
        return existing, False

    assignment, project = _assignment_for(db, user, assignment_id)
    if project.status != "active":
        raise ApiError(409, "project_not_active", "This project is not accepting work.")
    if assignment.status == ASSIGNMENT_APPROVED:
        raise ApiError(409, "already_approved", "This assignment is already approved.")

    submission = Submission(
        assignment_id=assignment.id,
        user_id=user.id,
        payload=payload,
        status=SUBMISSION_SUBMITTED,
        idempotency_key=client_key,
    )
    db.add(submission)
    db.flush()

    template = db.get(TaskTemplate, assignment.template_id) if assignment.template_id else None
    if template is not None and _should_be_gold(db, project, submission.id):
        expected = (template.config or {}).get("gold_expected") or (
            template.config or {}
        ).get("expected_answer")
        if isinstance(expected, dict):
            submission.is_gold = True
            submission.gold_expected = expected

    assignment.status = ASSIGNMENT_SUBMITTED
    db.flush()

    notify(
        db,
        user_id=user.id,
        kind="system",
        title="Work saved",
        body=f"{assignment.title} was submitted for review.",
        data={"assignment_id": assignment.id, "submission_id": submission.id},
    )
    return submission, True


def sync_offline(db: Session, user: User, items: list[dict]) -> list[dict]:
    """Apply a batch of offline submissions. One bad item never discards the rest."""
    if len(items) > 50:
        raise ApiError(400, "batch_too_large", "Sync at most 50 submissions at a time.")
    results: list[dict] = []
    for item in items:
        key = item.get("client_key") or ""
        try:
            submission, created = submit_work(
                db,
                user,
                assignment_id=int(item.get("assignment_id") or 0),
                payload=item.get("payload") or {},
                client_key=key,
            )
            results.append(
                {
                    "client_key": key,
                    "status": "saved" if created else "already_saved",
                    "submission_id": submission.id,
                }
            )
        except ApiError as exc:
            results.append(
                {
                    "client_key": key,
                    "status": "rejected",
                    "code": exc.code,
                    "message": exc.message,
                }
            )
        except (TypeError, ValueError):
            results.append(
                {
                    "client_key": key,
                    "status": "rejected",
                    "code": "invalid_item",
                    "message": "This queued item is malformed.",
                }
            )
    db.flush()
    return results


def start_assignment(db: Session, user: User, assignment_id: int) -> Assignment:
    assignment, _project = _assignment_for(db, user, assignment_id)
    if assignment.status == "assigned":
        assignment.status = ASSIGNMENT_IN_PROGRESS
        db.flush()
    return assignment


def my_submissions(db: Session, user: User) -> list[dict]:
    rows = db.execute(
        select(Submission, Assignment)
        .join(Assignment, Assignment.id == Submission.assignment_id)
        .where(Submission.user_id == user.id)
        .order_by(Submission.id.desc())
    ).all()
    return [
        {
            "submission_id": submission.id,
            "assignment_id": assignment.id,
            "assignment_title": assignment.title,
            "status": submission.status,
            "is_gold": submission.is_gold,
            "submitted_at": submission.submitted_at,
        }
        for submission, assignment in rows
    ]


def assignment_detail(db: Session, user: User, assignment_id: int) -> dict:
    assignment, project = _assignment_for(db, user, assignment_id)
    template = db.get(TaskTemplate, assignment.template_id) if assignment.template_id else None
    if template is not None and template.status != STATUS_PUBLISHED:
        template = None
    submission = db.scalar(
        select(Submission)
        .where(Submission.assignment_id == assignment.id, Submission.user_id == user.id)
        .order_by(Submission.id.desc())
        .limit(1)
    )
    return {
        "id": assignment.id,
        "title": assignment.title,
        "status": assignment.status,
        "due_at": assignment.due_at,
        "project": {"slug": project.slug, "title": project.title},
        "task": (
            {
                "template_id": template.id,
                "name": template.name,
                "instructions_md": template.instructions_md,
                "input_schema": template.input_schema,
                "answer_schema": template.answer_schema,
            }
            if template
            else None
        ),
        # Gold is not disclosed while work is in flight: the student must not know
        # which task is being used to check the reviewer.
        "last_submission": (
            {
                "id": submission.id,
                "status": submission.status,
                "submitted_at": submission.submitted_at,
            }
            if submission
            else None
        ),
    }
