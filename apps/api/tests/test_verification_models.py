"""Phase 0 PR 0.3a — verification, evidence and the Skill Transcript.

The product rule under test: a state change must name its evidence, an attempt is
a sitting rather than a proof, and a transcript line cannot exist twice for the
same evidence. Uses the shared `db` fixture (in-memory SQLite, foreign keys on).
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import User
from app.models.skills import Skill
from app.models.verification import (
    EVIDENCE_ASSESSMENT,
    UNVERIFIED,
    VERIFIED,
    Assessment,
    AssessmentAttempt,
    AssessmentTask,
    PracticalTask,
    TranscriptEntry,
    VerificationEvent,
    VerificationRecord,
)

EXPECTED_TABLES = {
    "verification_records",
    "verification_events",
    "assessments",
    "assessment_tasks",
    "assessment_attempts",
    "practical_tasks",
    "transcript_entries",
}


def _user(db: Session) -> User:
    student = db.scalar(select(Role).where(Role.code == ROLE_STUDENT))
    user = User(
        email=f"u{uuid.uuid4().hex[:8]}@example.test",
        username=f"u{uuid.uuid4().hex[:8]}",
        role_id=student.id if student else None,
    )
    db.add(user)
    db.flush()
    return user


def _skill(db: Session) -> Skill:
    skill = Skill(slug=f"skill-{uuid.uuid4().hex[:8]}", name="AI Data Annotation")
    db.add(skill)
    db.flush()
    return skill


def test_tables_exist(db: Session) -> None:
    assert EXPECTED_TABLES <= set(inspect(db.get_bind()).get_table_names())


def test_one_verification_record_per_student_and_skill(db: Session) -> None:
    user, skill = _user(db), _skill(db)
    db.add(VerificationRecord(user_id=user.id, skill_id=skill.id))
    db.flush()
    db.add(VerificationRecord(user_id=user.id, skill_id=skill.id))
    with pytest.raises(IntegrityError):
        db.flush()


def test_record_starts_unverified(db: Session) -> None:
    user, skill = _user(db), _skill(db)
    record = VerificationRecord(user_id=user.id, skill_id=skill.id)
    db.add(record)
    db.flush()
    assert record.status == UNVERIFIED and record.verified_at is None


def test_every_transition_names_its_evidence(db: Session) -> None:
    assert "updated_at" not in VerificationEvent.__table__.c, "events are append-only"
    assert "evidence_type" in VerificationEvent.__table__.c
    assert "evidence_id" in VerificationEvent.__table__.c

    user, skill = _user(db), _skill(db)
    record = VerificationRecord(user_id=user.id, skill_id=skill.id)
    db.add(record)
    db.flush()

    record.status = VERIFIED
    record.verified_at = datetime.now(UTC)
    db.add(
        VerificationEvent(
            record_id=record.id,
            from_status=UNVERIFIED,
            to_status=VERIFIED,
            evidence_type=EVIDENCE_ASSESSMENT,
            evidence_id="attempt-42",
            reason="passed gold-standard assessment",
        )
    )
    db.flush()

    event = db.scalars(select(VerificationEvent)).one()
    assert event.evidence_id == "attempt-42"
    assert event.actor_user_id is None  # system-graded, no human acted

    db.delete(record)
    db.flush()
    assert db.scalars(select(VerificationEvent)).all() == []


def test_assessment_carries_its_gold_answers(db: Session) -> None:
    skill = _skill(db)
    assessment = Assessment(slug=f"a-{uuid.uuid4().hex[:8]}", title="Annotate text", skill_id=skill.id)
    db.add(assessment)
    db.flush()
    task = AssessmentTask(
        assessment_id=assessment.id,
        ordinal=1,
        payload={"text": "I love this"},
        expected_answer={"label": "positive"},
    )
    db.add(task)
    db.flush()

    assert assessment.pass_threshold == 80 and assessment.max_attempts == 3
    stored = db.scalars(select(AssessmentTask)).one()
    assert stored.expected_answer["label"] == "positive" and stored.points == 1

    db.add(
        AssessmentTask(
            assessment_id=assessment.id,
            ordinal=1,
            payload={"text": "duplicate ordinal"},
            expected_answer={"label": "neutral"},
        )
    )
    with pytest.raises(IntegrityError):
        db.flush()


def test_retiring_a_template_keeps_the_graded_task(db: Session) -> None:
    skill = _skill(db)
    assessment = Assessment(slug=f"a-{uuid.uuid4().hex[:8]}", title="Annotate", skill_id=skill.id)
    db.add(assessment)
    db.flush()
    task = AssessmentTask(
        assessment_id=assessment.id,
        ordinal=1,
        payload={"text": "sample"},
        expected_answer={"label": "positive"},
    )
    db.add(task)
    db.flush()
    task.template_id = None  # simulating SET NULL on a retired template
    db.flush()
    assert db.scalars(select(AssessmentTask)).one().expected_answer == {"label": "positive"}


def test_attempts_are_sittings_not_uniqueness_constraints(db: Session) -> None:
    user, skill = _user(db), _skill(db)
    assessment = Assessment(slug=f"a-{uuid.uuid4().hex[:8]}", title="Annotate", skill_id=skill.id)
    db.add(assessment)
    db.flush()
    for _ in range(2):
        db.add(AssessmentAttempt(assessment_id=assessment.id, user_id=user.id))
    db.flush()
    attempts = db.scalars(select(AssessmentAttempt).order_by(AssessmentAttempt.id)).all()
    assert len(attempts) == 2
    assert attempts[0].passed is None and attempts[0].score is None

    attempts[0].score = 90
    attempts[0].passed = True
    db.flush()
    assert db.scalar(select(AssessmentAttempt.passed)) is True


def test_practical_task_keeps_its_rubric(db: Session) -> None:
    skill = _skill(db)
    task = PracticalTask(
        slug=f"p-{uuid.uuid4().hex[:8]}",
        title="Annotate 50 items",
        skill_id=skill.id,
        rubric={"criteria": [{"name": "accuracy", "weight": 70}]},
    )
    db.add(task)
    db.flush()
    assert db.scalars(select(PracticalTask)).one().rubric["criteria"][0]["weight"] == 70


def test_transcript_line_cannot_be_duplicated_for_the_same_evidence(db: Session) -> None:
    user = _user(db)
    entry = TranscriptEntry(
        user_id=user.id,
        kind="proved",
        title="Passed the AI Data Annotation assessment",
        evidence_type=EVIDENCE_ASSESSMENT,
        evidence_id="attempt-42",
    )
    db.add(entry)
    db.flush()
    db.add(
        TranscriptEntry(
            user_id=user.id,
            kind="proved",
            title="Duplicate projection",
            evidence_type=EVIDENCE_ASSESSMENT,
            evidence_id="attempt-42",
        )
    )
    with pytest.raises(IntegrityError):
        db.flush()
