"""Assessments: gold-standard tasks, randomised sittings, honest grading (PRD §5).

Rules that make the badge mean something:

* The tasks are gold-standard: each one has an expected answer, so scoring is
  deterministic and never depends on how long a lesson was watched.
* A sitting draws a random subset and **freezes** the selection, so a retry grades
  the same tasks rather than a fresh (easier) draw.
* The attempt limit and pass threshold are configuration on the assessment.
* Expected answers and explanations are never sent before submission; a client
  cannot open devtools and read the answers.
* Time is bounded, but generous: the assessment respects low-bandwidth users. An
  attempt that expires is failed and counted, not silently ignored.
"""
from __future__ import annotations

import random
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import as_utc, utcnow
from app.models.identity import User
from app.models.skills import Skill, TaskTemplate
from app.models.verification import (
    EVIDENCE_ASSESSMENT,
    EVIDENCE_PRACTICAL_TASK,
    TRANSCRIPT_PROVED,
    UNVERIFIED,
    Assessment,
    AssessmentAttempt,
    AssessmentTask,
    PracticalSubmission,
    PracticalTask,
)
from app.services import audit
from app.services.skills.tasks import validate
from app.services.verification import state
from app.services.verification.transcript import add_entry

ATTEMPT_TTL = timedelta(hours=24)


def list_assessments(db: Session, *, skill_id: int | None = None) -> list[dict]:
    stmt = select(Assessment).where(Assessment.status == "published")
    if skill_id is not None:
        stmt = stmt.where(Assessment.skill_id == skill_id)
    rows = db.scalars(stmt.order_by(Assessment.title)).all()
    return [
        {
            "id": row.id,
            "slug": row.slug,
            "title": row.title,
            "skill_id": row.skill_id,
            "pass_threshold": row.pass_threshold,
            "max_attempts": row.max_attempts,
            "task_count": row.task_count,
        }
        for row in rows
    ]


def _assessment(db: Session, slug: str) -> Assessment:
    assessment = db.scalar(select(Assessment).where(Assessment.slug == slug))
    if assessment is None or assessment.status != "published":
        raise ApiError(404, "assessment_not_found", "That assessment is not available.")
    return assessment


def _attempt_payload(
    attempt: AssessmentAttempt,
    tasks: list[AssessmentTask],
    templates: dict[int, TaskTemplate] | None = None,
) -> dict:
    """The sitting as the student sees it: inputs and schemas, never answers.

    The template's own schemas travel with the task so the client can render the
    same generated control it uses for practice, without a second round trip per
    task. A task with no template still carries its `payload`; the client says
    plainly that it cannot render it rather than guessing a form.
    """
    templates = templates or {}
    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "started_at": attempt.started_at,
        "expires_at": as_utc(attempt.started_at) + ATTEMPT_TTL,
        "tasks": [
            {
                "task_id": task.id,
                "ordinal": task.ordinal,
                "payload": task.payload,
                "points": task.points,
                "template_id": task.template_id,
                "input_schema": (
                    templates[task.template_id].input_schema
                    if task.template_id in templates
                    else None
                ),
                "answer_schema": (
                    templates[task.template_id].answer_schema
                    if task.template_id in templates
                    else None
                ),
            }
            for task in tasks
        ],
    }


def start_attempt(db: Session, user: User, slug: str) -> dict:
    assessment = _assessment(db, slug)

    existing = db.scalar(
        select(AssessmentAttempt)
        .where(
            AssessmentAttempt.assessment_id == assessment.id,
            AssessmentAttempt.user_id == user.id,
            AssessmentAttempt.submitted_at.is_(None),
        )
        .order_by(AssessmentAttempt.id.desc())
        .limit(1)
    )
    all_tasks = list(
        db.scalars(
            select(AssessmentTask)
            .where(AssessmentTask.assessment_id == assessment.id)
            .order_by(AssessmentTask.ordinal)
        ).all()
    )
    if existing is not None:
        # Resume, do not redraw: the student may have lost connection mid-sitting.
        selected = [task for task in all_tasks if task.id in (existing.presented_task_ids or [])]
        return _attempt_payload(existing, selected, _templates(db, selected))

    attempts = db.scalar(
        select(func.count(AssessmentAttempt.id)).where(
            AssessmentAttempt.assessment_id == assessment.id,
            AssessmentAttempt.user_id == user.id,
        )
    ) or 0
    if attempts >= assessment.max_attempts:
        raise ApiError(
            409,
            "attempt_limit_reached",
            "You have used all attempts for this assessment.",
            {"max_attempts": assessment.max_attempts},
        )
    if not all_tasks:
        raise ApiError(409, "assessment_empty", "This assessment has no tasks yet.")

    count = max(1, min(assessment.task_count, len(all_tasks)))
    selected = random.SystemRandom().sample(all_tasks, count)
    selected.sort(key=lambda task: task.ordinal)

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        user_id=user.id,
        presented_task_ids=[task.id for task in selected],
    )
    db.add(attempt)
    db.flush()

    record = state.ensure_record(db, user.id, assessment.skill_id)
    if record.status == UNVERIFIED:
        state.transition(
            db, record, to_status=state.IN_PROGRESS,
            evidence_type=EVIDENCE_ASSESSMENT, evidence_id=attempt.id,
            reason="assessment started",
        )
    elif record.status == state.SUSPENDED:
        # Starting a new sitting is the re-verification step after a suspension.
        state.transition(
            db, record, to_status=state.IN_PROGRESS,
            evidence_type=EVIDENCE_ASSESSMENT, evidence_id=attempt.id,
            reason="re-verification started",
        )
    return _attempt_payload(attempt, selected, _templates(db, selected))


def _templates(db: Session, tasks: list[AssessmentTask]) -> dict[int, TaskTemplate]:
    ids = {task.template_id for task in tasks if task.template_id}
    if not ids:
        return {}
    return {row.id: row for row in db.scalars(select(TaskTemplate).where(TaskTemplate.id.in_(ids)))}


def _grade(
    tasks: list[AssessmentTask],
    answers: dict,
    templates: dict[int, TaskTemplate] | None = None,
) -> tuple[int, int, list[dict]]:
    earned = 0
    total = 0
    detail: list[dict] = []
    templates = templates or {}
    for task in tasks:
        total += task.points
        answer = answers.get(str(task.id)) or answers.get(task.id) or {}
        if not isinstance(answer, dict):
            answer = {}
        template = templates.get(task.template_id) if task.template_id else None
        result = validate(
            template.validator if template else "exact_key",
            answer,
            task.expected_answer,
            template.config if template else {},
        )
        points = task.points if result.is_correct else 0
        earned += points
        detail.append(
            {
                "task_id": task.id,
                "ordinal": task.ordinal,
                "correct": result.is_correct,
                "points": points,
                "max_points": task.points,
                "feedback": result.feedback,
            }
        )
    return earned, total, detail


def submit_attempt(db: Session, user: User, attempt_id: int, answers: dict) -> dict:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if attempt is None or attempt.user_id != user.id:
        # Object-level authorisation: another student's attempt is indistinguishable
        # from a missing one.
        raise ApiError(404, "attempt_not_found", "That attempt does not exist.")
    if attempt.submitted_at is not None:
        raise ApiError(409, "attempt_already_submitted", "This attempt was already submitted.")

    assessment = db.get(Assessment, attempt.assessment_id)
    if assessment is None:
        raise ApiError(404, "assessment_not_found", "That assessment does not exist.")

    tasks = list(
        db.scalars(
            select(AssessmentTask).where(
                AssessmentTask.id.in_(attempt.presented_task_ids or [])
            )
        ).all()
    )
    record = state.ensure_record(db, user.id, assessment.skill_id)

    if as_utc(attempt.started_at) + ATTEMPT_TTL <= utcnow():
        attempt.submitted_at = utcnow()
        attempt.score = 0
        attempt.passed = False
        attempt.answers = answers
        state.apply_assessment(db, record, attempt.id, passed=False)
        db.flush()
        return {
            "attempt_id": attempt.id,
            "score": 0,
            "passed": False,
            "expired": True,
            "message": "This attempt expired. Start a new one.",
            "tasks": [],
        }

    earned, total, detail = _grade(tasks, answers, _templates(db, tasks))
    score = (100 * earned + total // 2) // total if total else 0
    passed = score >= assessment.pass_threshold

    attempt.answers = answers
    attempt.submitted_at = utcnow()
    attempt.score = score
    attempt.passed = passed
    db.flush()

    state.apply_assessment(db, record, attempt.id, passed=passed)
    if passed:
        add_entry(
            db,
            user_id=user.id,
            kind=TRANSCRIPT_PROVED,
            title=assessment.title,
            evidence_type="assessment_attempt",
            evidence_id=attempt.id,
            skill_id=assessment.skill_id,
        )
    db.flush()

    return {
        "attempt_id": attempt.id,
        "score": score,
        "passed": passed,
        "expired": False,
        "pass_threshold": assessment.pass_threshold,
        "verification_status": record.status,
        "tasks": detail,
    }


def review_attempt(db: Session, user: User, attempt_id: int) -> dict:
    """Post-submission review: now the expected answers may be shown."""
    attempt = db.get(AssessmentAttempt, attempt_id)
    if attempt is None or attempt.user_id != user.id:
        raise ApiError(404, "attempt_not_found", "That attempt does not exist.")
    if attempt.submitted_at is None:
        raise ApiError(409, "attempt_not_submitted", "Submit this attempt first.")
    tasks = list(
        db.scalars(
            select(AssessmentTask).where(
                AssessmentTask.id.in_(attempt.presented_task_ids or [])
            )
        ).all()
    )
    template_ids = {task.template_id for task in tasks if task.template_id}
    templates = (
        {row.id: row for row in db.scalars(select(TaskTemplate).where(TaskTemplate.id.in_(template_ids)))}
        if template_ids
        else {}
    )
    answers = attempt.answers or {}
    payload = []
    for task in tasks:
        answer = answers.get(str(task.id)) or answers.get(task.id) or {}
        template = templates.get(task.template_id)
        result = validate(
            template.validator if template else "exact_key",
            answer if isinstance(answer, dict) else {},
            task.expected_answer,
            template.config if template else {},
        )
        payload.append(
            {
                "task_id": task.id,
                "ordinal": task.ordinal,
                "payload": task.payload,
                "answer": answer,
                "expected_answer": task.expected_answer,
                "correct": result.is_correct,
                "feedback": result.feedback,
            }
        )
    return {
        "attempt_id": attempt.id,
        "score": attempt.score,
        "passed": attempt.passed,
        "submitted_at": attempt.submitted_at,
        "tasks": payload,
    }


# --- practical tasks ---------------------------------------------------------


def list_practical_tasks(db: Session, *, skill_id: int | None = None) -> list[dict]:
    stmt = select(PracticalTask).where(PracticalTask.status == "published")
    if skill_id is not None:
        stmt = stmt.where(PracticalTask.skill_id == skill_id)
    rows = db.scalars(stmt.order_by(PracticalTask.title)).all()
    return [
        {
            "id": row.id,
            "slug": row.slug,
            "title": row.title,
            "brief_md": row.brief_md,
            "skill_id": row.skill_id,
            "rubric": row.rubric,
        }
        for row in rows
    ]


def submit_practical(
    db: Session,
    user: User,
    *,
    slug: str,
    payload: dict,
    client_key: str | None = None,
) -> PracticalSubmission:
    task = db.scalar(select(PracticalTask).where(PracticalTask.slug == slug))
    if task is None or task.status != "published":
        raise ApiError(404, "practical_task_not_found", "That practical task is not available.")
    if not isinstance(payload, dict) or not payload:
        raise ApiError(400, "empty_submission", "Submit your work before sending it.")

    if client_key:
        existing = db.scalar(
            select(PracticalSubmission).where(PracticalSubmission.client_key == client_key)
        )
        if existing is not None:
            if existing.user_id != user.id:
                raise ApiError(409, "idempotency.key_reused", "This key belongs to another request.")
            return existing

    row = PracticalSubmission(
        practical_task_id=task.id,
        user_id=user.id,
        payload=payload,
        client_key=client_key,
    )
    db.add(row)
    db.flush()
    return row


def review_practical(
    db: Session,
    reviewer: User,
    *,
    submission_id: int,
    score: int,
    passed: bool,
    notes: str | None = None,
) -> PracticalSubmission:
    submission = db.get(PracticalSubmission, submission_id)
    if submission is None:
        raise ApiError(404, "submission_not_found", "That submission does not exist.")
    if not (0 <= score <= 100):
        raise ApiError(400, "invalid_score", "Score must be between 0 and 100.")
    if submission.status == "reviewed":
        raise ApiError(409, "already_reviewed", "This submission was already reviewed.")

    task = db.get(PracticalTask, submission.practical_task_id)
    if task is None:
        raise ApiError(404, "practical_task_not_found", "That practical task does not exist.")

    submission.status = "reviewed"
    submission.score = score
    submission.passed = passed
    submission.reviewed_by = reviewer.id
    submission.review_notes = notes
    db.flush()

    if passed:
        record = state.ensure_record(db, submission.user_id, task.skill_id)
        state.apply_practical(db, record, submission.id, passed=True)
        add_entry(
            db,
            user_id=submission.user_id,
            kind=TRANSCRIPT_PROVED,
            title=task.title,
            evidence_type="practical_submission",
            evidence_id=submission.id,
            skill_id=task.skill_id,
        )
    audit.record(
        db,
        action="practical.reviewed",
        actor_user_id=reviewer.id,
        actor_role_code=reviewer.role.code if reviewer.role else None,
        target_type="practical_submission",
        target_id=submission.id,
        reason=notes,
        context={"score": score, "passed": passed},
    )
    db.flush()
    return submission


# Re-exported so callers can check skill existence without importing two modules.
__all__ = [
    "ATTEMPT_TTL",
    "EVIDENCE_PRACTICAL_TASK",
    "EVIDENCE_ASSESSMENT",
    "Skill",
    "list_assessments",
    "list_practical_tasks",
    "review_attempt",
    "review_practical",
    "start_attempt",
    "submit_attempt",
    "submit_practical",
]
