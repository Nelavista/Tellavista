"""The verification state machine (PRD §5).

A student is verified because **evidence** says so. This module is the only place
that changes `VerificationRecord.status`, and every change writes a
`VerificationEvent` in the same transaction naming the evidence.

Allowed transitions:

    unverified  → in_progress        (an assessment attempt started)
    in_progress → verified           (assessment passed, practical task passed)
    in_progress → unverified         (attempt abandoned / failed out)
    verified    → at_risk            (quality on real work dropped)
    verified    → suspended          (severe quality failure)
    at_risk     → verified           (quality recovered)
    at_risk     → suspended          (quality failed again)
    at_risk     → in_progress        (re-verification required)
    suspended   → in_progress        (student may re-verify)
    suspended   → verified           (manual override only)

Anything else is a bug and raises. A manual override is allowed to any state but
requires an actor and a reason, and is audited.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.identity import User
from app.models.verification import (
    AT_RISK,
    EVIDENCE_ASSESSMENT,
    EVIDENCE_OVERRIDE,
    EVIDENCE_PRACTICAL_TASK,
    EVIDENCE_QUALITY_RECORD,
    EVIDENCE_TYPES,
    IN_PROGRESS,
    SUSPENDED,
    UNVERIFIED,
    VERIFICATION_STATUSES,
    VERIFIED,
    VerificationEvent,
    VerificationRecord,
)
from app.services import audit

TRANSITIONS: dict[str, frozenset[str]] = {
    UNVERIFIED: frozenset({IN_PROGRESS}),
    IN_PROGRESS: frozenset({VERIFIED, UNVERIFIED}),
    VERIFIED: frozenset({AT_RISK, SUSPENDED}),
    AT_RISK: frozenset({VERIFIED, SUSPENDED, IN_PROGRESS}),
    SUSPENDED: frozenset({IN_PROGRESS, VERIFIED}),
}


def ensure_record(db: Session, user_id: int, skill_id: int) -> VerificationRecord:
    record = db.scalar(
        select(VerificationRecord).where(
            VerificationRecord.user_id == user_id, VerificationRecord.skill_id == skill_id
        )
    )
    if record is None:
        record = VerificationRecord(user_id=user_id, skill_id=skill_id, status=UNVERIFIED)
        db.add(record)
        db.flush()
    return record


def _assert_transition(
    record: VerificationRecord,
    to_status: str,
    *,
    evidence_type: str,
    actor_user_id: int | None,
    reason: str | None,
) -> None:
    if to_status not in VERIFICATION_STATUSES:
        raise ApiError(400, "invalid_verification_status", "Unknown verification status.")
    if evidence_type not in EVIDENCE_TYPES:
        raise ApiError(400, "invalid_evidence", "Unknown verification evidence.")
    if record.status == to_status:
        return
    if evidence_type == EVIDENCE_OVERRIDE:
        if actor_user_id is None or not (reason or "").strip():
            raise ApiError(
                400,
                "override_requires_reason",
                "A manual override needs a reviewer and a reason.",
            )
        return
    if to_status not in TRANSITIONS.get(record.status, frozenset()):
        raise ApiError(
            409,
            "invalid_verification_transition",
            f"Cannot move verification from {record.status} to {to_status}.",
        )


def transition(
    db: Session,
    record: VerificationRecord,
    *,
    to_status: str,
    evidence_type: str,
    evidence_id: str | int,
    reason: str | None = None,
    actor_user_id: int | None = None,
) -> VerificationEvent:
    """Move the record and append the evidence event. Idempotent on no-op."""
    _assert_transition(
        record,
        to_status,
        evidence_type=evidence_type,
        actor_user_id=actor_user_id,
        reason=reason,
    )
    if record.status == to_status:
        # Re-applying the same evidence must not create a second event, but a
        # fresh successful assessment should refresh `last_evaluated_at`.
        record.last_evaluated_at = utcnow()
        db.flush()
        existing = db.scalar(
            select(VerificationEvent).where(
                VerificationEvent.record_id == record.id,
                VerificationEvent.to_status == to_status,
                VerificationEvent.evidence_type == evidence_type,
                VerificationEvent.evidence_id == str(evidence_id),
            )
        )
        if existing is not None:
            return existing

    from_status = record.status
    record.status = to_status
    record.last_evaluated_at = utcnow()
    if to_status == VERIFIED:
        record.verified_at = utcnow()
    event = VerificationEvent(
        record_id=record.id,
        from_status=from_status,
        to_status=to_status,
        evidence_type=evidence_type,
        evidence_id=str(evidence_id),
        reason=reason,
        actor_user_id=actor_user_id,
    )
    db.add(event)
    db.flush()
    return event


def apply_assessment(db: Session, record: VerificationRecord, attempt_id: int, passed: bool) -> None:
    if not passed:
        # A failed sitting does not punish a verified student; it only leaves them
        # where they are. It does move a first attempt to "in progress".
        if record.status == UNVERIFIED:
            transition(
                db, record, to_status=IN_PROGRESS,
                evidence_type=EVIDENCE_ASSESSMENT, evidence_id=attempt_id,
                reason="assessment attempted",
            )
        return

    if record.status == SUSPENDED:
        # Passing an assessment is not enough on its own after a suspension; the
        # state machine requires re-verification to start first.
        raise ApiError(
            409,
            "reverification_required",
            "Start re-verification before taking the assessment again.",
        )
    transition(
        db, record, to_status=VERIFIED,
        evidence_type=EVIDENCE_ASSESSMENT, evidence_id=attempt_id,
        reason="assessment passed",
    )


def apply_practical(db: Session, record: VerificationRecord, submission_id: int, passed: bool) -> None:
    if passed:
        # Passing the practical is itself the engagement that starts verification:
        # a student who never opened an assessment can still earn proof by doing
        # the task. The state machine requires unverified → in_progress → verified,
        # so record the submission as the start before recording the pass.
        if record.status == UNVERIFIED:
            transition(
                db, record, to_status=IN_PROGRESS,
                evidence_type=EVIDENCE_PRACTICAL_TASK, evidence_id=submission_id,
                reason="practical task submitted",
            )
        transition(
            db, record, to_status=VERIFIED,
            evidence_type=EVIDENCE_PRACTICAL_TASK, evidence_id=submission_id,
            reason="practical task passed",
        )


def apply_quality(
    db: Session,
    record: VerificationRecord,
    *,
    quality_record_id: int,
    score: int,
    pass_threshold: int,
) -> None:
    """Quality on real work strengthens or weakens verification.

    `score >= threshold` moves at-risk back to verified. Below threshold moves
    verified to at-risk; a score more than 20 points below suspends. Nothing here
    can verify an unverified student: only assessment or practical evidence can.
    """
    if record.status in {UNVERIFIED, IN_PROGRESS}:
        return
    if score >= pass_threshold:
        if record.status == AT_RISK:
            transition(
                db, record, to_status=VERIFIED,
                evidence_type=EVIDENCE_QUALITY_RECORD, evidence_id=quality_record_id,
                reason=f"quality recovered to {score}",
            )
        return
    if record.status == VERIFIED:
        transition(
            db, record, to_status=AT_RISK,
            evidence_type=EVIDENCE_QUALITY_RECORD, evidence_id=quality_record_id,
            reason=f"quality dropped to {score}",
        )
    elif record.status == AT_RISK and score < pass_threshold - 20:
        transition(
            db, record, to_status=SUSPENDED,
            evidence_type=EVIDENCE_QUALITY_RECORD, evidence_id=quality_record_id,
            reason=f"quality remained low at {score}",
        )


def override(
    db: Session,
    *,
    record: VerificationRecord,
    to_status: str,
    actor: User,
    reason: str,
) -> VerificationEvent:
    event = transition(
        db, record, to_status=to_status,
        evidence_type=EVIDENCE_OVERRIDE, evidence_id=record.id,
        reason=reason, actor_user_id=actor.id,
    )
    audit.record(
        db,
        action="verification.override",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="verification_record",
        target_id=record.id,
        reason=reason,
        context={"to": to_status, "user_id": record.user_id, "skill_id": record.skill_id},
    )
    return event


def status_for(db: Session, user_id: int, skill_id: int) -> str:
    record = db.scalar(
        select(VerificationRecord).where(
            VerificationRecord.user_id == user_id, VerificationRecord.skill_id == skill_id
        )
    )
    return record.status if record else UNVERIFIED


def verified_skill_ids(db: Session, user_id: int) -> set[int]:
    return {
        row
        for row in db.scalars(
            select(VerificationRecord.skill_id).where(
                VerificationRecord.user_id == user_id,
                VerificationRecord.status.in_([VERIFIED, AT_RISK]),
            )
        ).all()
    }


def last_evaluated(record: VerificationRecord) -> datetime | None:
    return record.last_evaluated_at
