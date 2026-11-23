"""Public impact metrics, read from the product database.

The marketing site must not invent reach figures. This service counts what the
platform actually recorded and gives every number a plain-language label and a
definition, so the page can publish a figure without a claim it cannot support.

Rules:

* **Aggregates only.** No student ids, names or addresses leave this module.
* **One read.** Every metric comes from the same transaction, so the page cannot
  show two counts taken at different moments.
* **Published state is a setting.** `impact_metrics_enabled` hides the block
  without deleting the query; the admin preview ignores it.
* **Money is grouped by currency.** Amounts are integer minor units and are
  never summed across currencies.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.academia import Course, University
from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import User
from app.models.ledger import EARNING_PAID, EarningLine
from app.models.matching import Opportunity
from app.models.platform import PlatformSettings
from app.models.skills import Skill
from app.models.verification import (
    VERIFIED,
    AssessmentAttempt,
    PracticalSubmission,
    VerificationRecord,
)
from app.models.work import SUBMISSION_APPROVED, Submission

STATUS_OPEN = "open"


def _count(db: Session, statement) -> int:  # noqa: ANN001 - SQLAlchemy Select
    value = db.scalar(statement)
    return int(value or 0)


def metrics(db: Session) -> list[dict[str, Any]]:
    """The current counts, in display order.

    A metric is included even while its count is zero. Zero is a real, honest
    result and the page says so; hiding it would make the remaining numbers look
    selected.
    """
    student_role_id = db.scalar(select(Role.id).where(Role.code == ROLE_STUDENT))

    students = _count(
        db,
        select(func.count(User.id)).where(
            User.is_deleted.is_(False),
            User.role_id == student_role_id,
        ),
    )
    published_skills = _count(
        db,
        select(func.count(Skill.id)).where(Skill.is_active.is_(True)),
    )
    universities = _count(
        db,
        select(func.count(University.id)).where(University.active.is_(True)),
    )
    courses = _count(db, select(func.count(Course.id)))
    verified_skills = _count(
        db,
        select(func.count(VerificationRecord.id)).where(
            VerificationRecord.status == VERIFIED
        ),
    )
    assessments_passed = _count(
        db,
        select(func.count(AssessmentAttempt.id)).where(
            AssessmentAttempt.passed.is_(True)
        ),
    )
    practical_tasks_passed = _count(
        db,
        select(func.count(PracticalSubmission.id)).where(
            PracticalSubmission.passed.is_(True)
        ),
    )
    work_approved = _count(
        db,
        select(func.count(Submission.id)).where(Submission.status == SUBMISSION_APPROVED),
    )
    open_opportunities = _count(
        db,
        select(func.count(Opportunity.id)).where(Opportunity.status == STATUS_OPEN),
    )

    return [
        {
            "key": "students",
            "label": "Student accounts",
            "value": students,
            "detail": "Accounts created on the platform.",
        },
        {
            "key": "published_skills",
            "label": "Published skills",
            "value": published_skills,
            "detail": "Skills a student can learn and be assessed in.",
        },
        {
            "key": "universities",
            "label": "Universities",
            "value": universities,
            "detail": "Universities with an active campus record.",
        },
        {
            "key": "courses",
            "label": "Courses mapped",
            "value": courses,
            "detail": "Courses carrying a curriculum record.",
        },
        {
            "key": "verified_skills",
            "label": "Verified skills",
            "value": verified_skills,
            "detail": "Skill verifications backed by an assessment or practical task.",
        },
        {
            "key": "assessments_passed",
            "label": "Assessments passed",
            "value": assessments_passed,
            "detail": "Assessment sittings that met the published pass threshold.",
        },
        {
            "key": "practical_tasks_passed",
            "label": "Practical tasks passed",
            "value": practical_tasks_passed,
            "detail": "Practical submissions approved against their rubric.",
        },
        {
            "key": "work_approved",
            "label": "Work approved",
            "value": work_approved,
            "detail": "Paid-work submissions that passed quality review.",
        },
        {
            "key": "open_opportunities",
            "label": "Open opportunities",
            "value": open_opportunities,
            "detail": "Listings currently open to eligible students.",
        },
    ]


def paid_by_currency(db: Session) -> list[dict[str, Any]]:
    """Money actually marked paid, grouped by currency.

    Summing across currencies would be arithmetic nonsense, so the result is a
    short list. An empty list means nothing has been paid yet.
    """
    rows = db.execute(
        select(
            EarningLine.currency,
            func.coalesce(func.sum(EarningLine.amount_minor), 0),
        )
        .where(EarningLine.status == EARNING_PAID)
        .group_by(EarningLine.currency)
        .order_by(EarningLine.currency)
    ).all()
    return [
        {"currency": currency, "amount_minor": int(amount or 0)}
        for currency, amount in rows
    ]


def payload(db: Session, row: PlatformSettings, *, public: bool) -> dict[str, Any]:
    """Build the response.

    A public read with publishing switched off returns the flag and an empty
    metric list: the hidden numbers are not merely left to the client to hide.
    The admin preview passes ``public=False`` and always gets the figures.
    """
    visible = (not public) or bool(row.impact_metrics_enabled)
    return {
        "generated_at": datetime.now(UTC),
        "enabled": bool(row.impact_metrics_enabled),
        "metrics": metrics(db) if visible else [],
        "paid_by_currency": paid_by_currency(db) if visible else [],
    }


__all__ = ["metrics", "paid_by_currency", "payload"]
