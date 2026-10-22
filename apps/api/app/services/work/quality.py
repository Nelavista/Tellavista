"""Quality control: review, gold tasks and consequences (PRD §8).

The review decides approval, rework or rejection. Everything downstream reads from
that decision: the assignment status, the student's earning line, their rolling
quality record, their verification status and — through consequences — whether they
keep matching.

Gold tasks are mixed into live work. Their answer is known, so the reviewer's
verdict and the objective answer can be compared. A gold task that is wrong scores
zero regardless of a lenient reviewer; that is what stops quality drifting.

Consequences are configuration: the thresholds live on the project's standard, and
every consequence row names the rule that fired it.
"""
from __future__ import annotations

import hashlib

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User
from app.models.quality import (
    CONSEQUENCE_KINDS,
    CONSEQUENCE_REMOVE_FROM_PROJECT,
    CONSEQUENCE_REQUIRE_REVERIFICATION,
    CONSEQUENCE_RESTRICT_MATCHING,
    CONSEQUENCE_WARN,
    DEFAULT_RULES,
    VERDICT_APPROVED,
    VERDICT_REJECTED,
    VERDICT_REWORK,
    VERDICTS,
    QualityConsequence,
    QualityRecord,
    QualityReview,
    QualityStandard,
)
from app.models.skills import Skill, TaskTemplate
from app.models.verification import TRANSCRIPT_DELIVERED, Assessment
from app.models.work import (
    ASSIGNMENT_APPROVED,
    ASSIGNMENT_REJECTED,
    ASSIGNMENT_REWORK,
    MEMBER_REMOVED,
    SUBMISSION_APPROVED,
    SUBMISSION_REJECTED,
    SUBMISSION_REWORK,
    SUBMISSION_SUBMITTED,
    Assignment,
    Cohort,
    CohortMember,
    Project,
    Submission,
)
from app.services import audit
from app.services.money.ledger import record_approval_earning
from app.services.notifications import notify
from app.services.skills.tasks import validate
from app.services.verification import state
from app.services.verification.transcript import add_entry


def ensure_standard(db: Session, project: Project) -> QualityStandard:
    standard = db.scalar(
        select(QualityStandard).where(QualityStandard.project_id == project.id)
    )
    if standard is None:
        standard = QualityStandard(
            project_id=project.id,
            name=f"{project.title} quality standard",
            instructions_md="Work must be accurate, complete and follow the task instructions.",
            rubric=[
                {"key": "accuracy", "weight": 60},
                {"key": "completeness", "weight": 30},
                {"key": "instruction_following", "weight": 10},
            ],
            pass_threshold=int(DEFAULT_RULES["pass_threshold"]),
            rules=dict(DEFAULT_RULES),
        )
        db.add(standard)
        db.flush()
    return standard


def set_standard(
    db: Session,
    actor: User,
    project: Project,
    *,
    name: str | None = None,
    instructions_md: str | None = None,
    rubric: list | None = None,
    pass_threshold: int | None = None,
    rules: dict | None = None,
) -> QualityStandard:
    standard = ensure_standard(db, project)
    if pass_threshold is not None and not (0 <= pass_threshold <= 100):
        raise ApiError(400, "invalid_threshold", "Pass threshold must be 0-100.")
    merged = dict(standard.rules or DEFAULT_RULES)
    if rules:
        unknown = set(rules) - set(DEFAULT_RULES)
        if unknown:
            raise ApiError(
                400, "unknown_quality_rule", "Unknown quality rule.", {"rules": sorted(unknown)}
            )
        merged.update(rules)
    if name is not None:
        standard.name = name[:160]
    if instructions_md is not None:
        standard.instructions_md = instructions_md
    if rubric is not None:
        standard.rubric = rubric
    if pass_threshold is not None:
        standard.pass_threshold = pass_threshold
    standard.rules = merged
    db.flush()
    audit.record(
        db,
        action="quality.standard_updated",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="quality_standard",
        target_id=standard.id,
    )
    return standard


def _requires_second_review(submission: Submission, standard: QualityStandard) -> bool:
    rate = int((standard.rules or DEFAULT_RULES).get("double_review_percent", 0))
    if rate <= 0:
        return False
    digest = hashlib.sha256(f"double:{submission.id}".encode()).hexdigest()
    return int(digest[:8], 16) % 100 < rate


def _gold_correct(db: Session, submission: Submission) -> bool | None:
    if not submission.is_gold or submission.gold_expected is None:
        return None
    assignment = db.get(Assignment, submission.assignment_id)
    template = (
        db.get(TaskTemplate, assignment.template_id)
        if assignment and assignment.template_id
        else None
    )
    result = validate(
        template.validator if template else "exact_key",
        submission.payload if isinstance(submission.payload, dict) else {},
        submission.gold_expected,
        template.config if template else {},
    )
    return result.is_correct


def _review_score(verdict: str, score: int | None) -> int:
    if score is not None:
        return max(0, min(100, score))
    return {VERDICT_APPROVED: 100, VERDICT_REWORK: 50, VERDICT_REJECTED: 0}[verdict]


def _reviews(db: Session, submission_id: int) -> list[QualityReview]:
    return list(
        db.scalars(
            select(QualityReview)
            .where(QualityReview.submission_id == submission_id)
            .order_by(QualityReview.id)
        ).all()
    )


def review_submission(
    db: Session,
    reviewer: User,
    *,
    submission_id: int,
    verdict: str,
    score: int | None = None,
    notes: str | None = None,
    is_override: bool = False,
    reason: str | None = None,
) -> QualityReview:
    if verdict not in VERDICTS:
        raise ApiError(400, "invalid_verdict", "Use approved, rework or rejected.")
    if is_override and not (reason or "").strip():
        raise ApiError(400, "reason_required", "An override needs a reason.")

    submission = db.get(Submission, submission_id)
    if submission is None:
        raise ApiError(404, "submission_not_found", "That submission does not exist.")
    assignment = db.get(Assignment, submission.assignment_id)
    project = db.get(Project, assignment.project_id) if assignment else None
    if assignment is None or project is None:
        raise ApiError(404, "assignment_not_found", "That submission has no assignment.")
    standard = ensure_standard(db, project)

    existing = _reviews(db, submission.id)
    second_review = False
    agrees_with: QualityReview | None = None
    if existing and not is_override:
        if any(review.is_override for review in existing):
            raise ApiError(409, "already_overridden", "This submission was already overridden.")
        if len(existing) >= 2:
            raise ApiError(409, "already_reviewed", "This submission was already reviewed twice.")
        if not _requires_second_review(submission, standard):
            raise ApiError(409, "already_reviewed", "This submission was already reviewed.")
        if existing[0].reviewer_user_id == reviewer.id:
            raise ApiError(
                409, "second_reviewer_required", "A second review must come from someone else."
            )
        second_review = True
        agrees_with = existing[0]

    gold_correct = _gold_correct(db, submission)
    final_score = _review_score(verdict, score)
    if gold_correct is not None:
        # The objective answer wins over a lenient reviewer for quality scoring.
        final_score = 100 if gold_correct else 0

    review = QualityReview(
        submission_id=submission.id,
        reviewer_user_id=reviewer.id,
        verdict=verdict,
        score=final_score,
        notes=notes,
        is_gold=gold_correct is not None,
        gold_correct=gold_correct,
        agrees_with_review_id=agrees_with.id if agrees_with else None,
        is_override=is_override,
        reason=reason,
    )
    db.add(review)
    db.flush()

    if not second_review:
        _apply_outcome(db, submission=submission, assignment=assignment, project=project, verdict=verdict)
        record = recompute_record(db, submission.user_id, project_id=project.id, standard=standard)
        overall = recompute_record(db, submission.user_id, project_id=None, standard=standard)
        fired = _apply_consequences(
            db,
            submission=submission,
            assignment=assignment,
            project=project,
            standard=standard,
            record=record,
        )
        _apply_verification_quality(
            db,
            assignment=assignment,
            project_record=record,
            standard=standard,
            # The re-verification consequence already told the student to act;
            # a second notification for the same review would just be noise.
            notify_change=CONSEQUENCE_REQUIRE_REVERIFICATION not in fired,
        )
        _ = overall
    elif agrees_with is not None:
        audit.record(
            db,
            action="quality.second_review",
            actor_user_id=reviewer.id,
            actor_role_code=reviewer.role.code if reviewer.role else None,
            target_type="submission",
            target_id=submission.id,
            context={
                "agrees": review.verdict == agrees_with.verdict,
                "first_review_id": agrees_with.id,
            },
        )

    if is_override:
        audit.record(
            db,
            action="quality.override",
            actor_user_id=reviewer.id,
            actor_role_code=reviewer.role.code if reviewer.role else None,
            target_type="submission",
            target_id=submission.id,
            reason=reason,
            context={"verdict": verdict, "score": final_score},
        )
    db.flush()
    return review


def _apply_outcome(
    db: Session,
    *,
    submission: Submission,
    assignment: Assignment,
    project: Project,
    verdict: str,
) -> None:
    if verdict == VERDICT_APPROVED:
        submission.status = SUBMISSION_APPROVED
        assignment.status = ASSIGNMENT_APPROVED
        db.flush()
        record_approval_earning(db, project=project, submission=submission)
        from app.core import observability

        observability.capture(
            submission.user_id,
            observability.EVENTS["approved"],
            {"submission_id": submission.id, "project_id": project.id},
        )
        add_entry(
            db,
            user_id=submission.user_id,
            kind=TRANSCRIPT_DELIVERED,
            title=assignment.title,
            evidence_type="submission",
            evidence_id=submission.id,
        )
        notify(
            db,
            user_id=submission.user_id,
            kind="review",
            title="Work approved",
            body=f"{assignment.title} was approved and added to your earnings.",
            data={"assignment_id": assignment.id, "submission_id": submission.id},
        )
    elif verdict == VERDICT_REWORK:
        submission.status = SUBMISSION_REWORK
        assignment.status = ASSIGNMENT_REWORK
        db.flush()
        notify(
            db,
            user_id=submission.user_id,
            kind="rework",
            title="Changes requested",
            body=f"{assignment.title} needs another pass. Open it to see the notes.",
            data={"assignment_id": assignment.id},
        )
    else:
        submission.status = SUBMISSION_REJECTED
        assignment.status = ASSIGNMENT_REJECTED
        db.flush()
        notify(
            db,
            user_id=submission.user_id,
            kind="review",
            title="Work not accepted",
            body=f"{assignment.title} was not accepted. Read the review notes before retrying.",
            data={"assignment_id": assignment.id},
        )


def recompute_record(
    db: Session,
    user_id: int,
    *,
    project_id: int | None,
    standard: QualityStandard | None = None,
) -> QualityRecord:
    """Rebuild the rolling record from current reviews. Never trusts a counter."""
    latest_ids = (
        select(func.max(QualityReview.id).label("review_id"))
        .join(Submission, Submission.id == QualityReview.submission_id)
        .where(
            Submission.user_id == user_id,
            QualityReview.agrees_with_review_id.is_(None),
        )
    )
    if project_id is not None:
        latest_ids = latest_ids.where(Submission.assignment_id.in_(
            select(Assignment.id).where(Assignment.project_id == project_id)
        ))
    latest_ids = latest_ids.group_by(QualityReview.submission_id).subquery()
    reviews = list(
        db.scalars(
            select(QualityReview)
            .where(QualityReview.id.in_(select(latest_ids.c.review_id)))
            .order_by(QualityReview.created_at.desc(), QualityReview.id.desc())
        ).all()
    )

    record = db.scalar(
        select(QualityRecord).where(
            QualityRecord.user_id == user_id,
            QualityRecord.project_id == project_id
            if project_id is not None
            else QualityRecord.project_id.is_(None),
        )
    )
    if record is None:
        record = QualityRecord(user_id=user_id, project_id=project_id)
        db.add(record)

    threshold = standard.pass_threshold if standard else 80
    scores = [review.score if review.score is not None else 0 for review in reviews]
    record.reviews_count = len(reviews)
    record.approvals = sum(1 for review in reviews if review.verdict == VERDICT_APPROVED)
    record.reworks = sum(1 for review in reviews if review.verdict == VERDICT_REWORK)
    record.rejections = sum(1 for review in reviews if review.verdict == VERDICT_REJECTED)
    record.average_score = (
        (sum(scores) + len(scores) // 2) // len(scores) if scores else 0
    )
    record.gold_tasks = sum(1 for review in reviews if review.is_gold)
    record.gold_correct = sum(1 for review in reviews if review.gold_correct)
    record.last_review_at = reviews[0].created_at if reviews else None

    poor_streak = 0
    for review in reviews:
        if review.verdict == VERDICT_APPROVED and (review.score or 0) >= threshold:
            break
        poor_streak += 1
    record.poor_streak = poor_streak
    db.flush()
    return record


def _apply_consequences(
    db: Session,
    *,
    submission: Submission,
    assignment: Assignment,
    project: Project,
    standard: QualityStandard,
    record: QualityRecord,
) -> set[str]:
    """Record any consequence the streak has earned. Returns the kinds fired."""
    rules = {**DEFAULT_RULES, **(standard.rules or {})}
    streak = record.poor_streak
    fired: set[str] = set()
    thresholds = [
        (CONSEQUENCE_WARN, int(rules["warn_after"])),
        (CONSEQUENCE_RESTRICT_MATCHING, int(rules["restrict_matching_after"])),
        (CONSEQUENCE_REQUIRE_REVERIFICATION, int(rules["require_reverification_after"])),
        (CONSEQUENCE_REMOVE_FROM_PROJECT, int(rules["remove_from_project_after"])),
    ]
    for kind, threshold in thresholds:
        if streak < threshold:
            continue
        already = db.scalar(
            select(QualityConsequence).where(
                QualityConsequence.user_id == submission.user_id,
                QualityConsequence.project_id == project.id,
                QualityConsequence.kind == kind,
                QualityConsequence.active.is_(True),
            )
        )
        if already is not None:
            continue
        consequence = QualityConsequence(
            user_id=submission.user_id,
            project_id=project.id,
            kind=kind,
            reason=f"{streak} consecutive reviews below the {standard.pass_threshold} quality bar",
            quality_record_id=record.id,
        )
        db.add(consequence)
        db.flush()
        fired.add(kind)
        audit.record(
            db,
            action="quality.consequence",
            target_type="quality_consequence",
            target_id=consequence.id,
            reason=consequence.reason,
            context={"kind": kind, "user_id": submission.user_id, "project_id": project.id},
        )

        if kind == CONSEQUENCE_REMOVE_FROM_PROJECT:
            member = db.scalar(
                select(CohortMember)
                .join(Cohort, Cohort.id == CohortMember.cohort_id)
                .where(
                    Cohort.project_id == project.id,
                    CohortMember.user_id == submission.user_id,
                    CohortMember.status != MEMBER_REMOVED,
                )
                .order_by(CohortMember.id.desc())
                .limit(1)
            )
            if member is not None:
                member.status = MEMBER_REMOVED
            notify(
                db,
                user_id=submission.user_id,
                kind="system",
                title="Removed from the project",
                body="Quality fell below the project standard after several reviews.",
                data={"project_slug": project.slug},
            )
        elif kind == CONSEQUENCE_REQUIRE_REVERIFICATION:
            notify(
                db,
                user_id=submission.user_id,
                kind="verification",
                title="Re-verification required",
                body="Your recent work quality means you need to verify this skill again.",
                data={"project_slug": project.slug},
            )
        elif kind == CONSEQUENCE_RESTRICT_MATCHING:
            notify(
                db,
                user_id=submission.user_id,
                kind="system",
                title="Matching paused",
                body="New opportunities are paused while your quality record recovers.",
            )
        else:
            notify(
                db,
                user_id=submission.user_id,
                kind="system",
                title="Quality warning",
                body="Recent work fell below the project quality standard.",
                data={"project_slug": project.slug},
            )
    db.flush()
    return fired


def _apply_verification_quality(
    db: Session,
    *,
    assignment: Assignment,
    project_record: QualityRecord,
    standard: QualityStandard,
    notify_change: bool = True,
) -> str | None:
    """Move the badge on real work quality and tell the student when it moves.

    A badge that drops to `at_risk` or `suspended` is a prompt, not a silent
    status: the notification names the skill and, when one exists, the assessment
    that earns it back. The prompt is skipped only when the same review already
    sent the re-verification consequence.
    """
    if assignment.template_id is None:
        return None
    template = db.get(TaskTemplate, assignment.template_id)
    if template is None:
        return None
    record = state.ensure_record(db, project_record.user_id, template.skill_id)
    before = record.status
    state.apply_quality(
        db,
        record,
        quality_record_id=project_record.id,
        score=project_record.average_score,
        pass_threshold=standard.pass_threshold,
    )
    if record.status == before or record.status not in {state.AT_RISK, state.SUSPENDED}:
        return record.status

    if notify_change:
        skill = db.get(Skill, template.skill_id)
        assessment = db.scalar(
            select(Assessment)
            .where(Assessment.skill_id == template.skill_id)
            .order_by(Assessment.id)
            .limit(1)
        )
        skill_name = skill.name if skill else "this skill"
        if record.status == state.SUSPENDED:
            title = "Re-verify this skill"
            body = (
                f"Your work quality suspended the {skill_name} badge. "
                "Pass the assessment again to earn it back."
            )
        else:
            title = "Your skill badge is at risk"
            body = (
                f"Recent work quality lowered the {skill_name} badge. "
                "Pass the assessment again to restore it."
            )
        notify(
            db,
            user_id=project_record.user_id,
            kind="verification",
            title=title,
            body=body,
            data={
                "skill_slug": skill.slug if skill else None,
                "assessment_slug": assessment.slug if assessment else None,
                "verification_status": record.status,
            },
        )
    return record.status


def review_queue(db: Session, *, limit: int = 50) -> list[dict]:
    reviewed = select(QualityReview.submission_id)
    rows = db.execute(
        select(Submission, Assignment, Project, User)
        .join(Assignment, Assignment.id == Submission.assignment_id)
        .join(Project, Project.id == Assignment.project_id)
        .join(User, User.id == Submission.user_id)
        .where(Submission.status == SUBMISSION_SUBMITTED, Submission.id.not_in(reviewed))
        .order_by(Submission.id)
        .limit(limit)
    ).all()
    return [
        {
            "submission_id": submission.id,
            "assignment_id": assignment.id,
            "assignment_title": assignment.title,
            "project": {"slug": project.slug, "title": project.title},
            "student": {"id": user.id, "name": user.name, "email": user.email},
            "is_gold": submission.is_gold,
            "submitted_at": submission.submitted_at,
            "payload": submission.payload,
        }
        for submission, assignment, project, user in rows
    ]


def my_quality(db: Session, user: User) -> dict:
    record = db.scalar(
        select(QualityRecord).where(
            QualityRecord.user_id == user.id, QualityRecord.project_id.is_(None)
        )
    )
    consequences = db.scalars(
        select(QualityConsequence)
        .where(QualityConsequence.user_id == user.id, QualityConsequence.active.is_(True))
        .order_by(QualityConsequence.id.desc())
    ).all()
    return {
        "record": (
            {
                "reviews_count": record.reviews_count,
                "approvals": record.approvals,
                "reworks": record.reworks,
                "rejections": record.rejections,
                "average_score": record.average_score,
                "gold_tasks": record.gold_tasks,
                "gold_correct": record.gold_correct,
                "poor_streak": record.poor_streak,
            }
            if record
            else None
        ),
        "consequences": [
            {"kind": row.kind, "reason": row.reason, "created_at": row.created_at}
            for row in consequences
        ],
    }


__all__ = [
    "CONSEQUENCE_KINDS",
    "ensure_standard",
    "my_quality",
    "recompute_record",
    "review_queue",
    "review_submission",
    "set_standard",
]
