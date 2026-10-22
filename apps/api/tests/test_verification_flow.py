"""Phase 3 — verification is proof, and every transition names its evidence.

The acceptance rule from the build plan: a student can only become verified by
passing the practical assessment; watching lessons never changes status; the
transcript updates with linked evidence. An ops override is possible, but it is
logged with a mandatory reason.
"""
from __future__ import annotations

import pytest
from factories import make_skill, make_template, make_user, unique
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.skills import STATUS_PUBLISHED, LearningPath, LearningPathStep, Lesson
from app.models.verification import (
    Assessment,
    AssessmentTask,
    TranscriptEntry,
    VerificationEvent,
    VerificationRecord,
)
from app.services.skills import learning
from app.services.verification import assessments, state
from app.services.verification import transcript as transcript_service


def _assessment(db: Session, *, threshold: int = 80):
    skill = make_skill(db)
    template = make_template(
        db,
        skill,
        config={"expected_answer": {"key": "A"}, "gold_expected": {"key": "A"}},
    )
    assessment = Assessment(
        skill_id=skill.id,
        slug=unique("assessment"),
        title="Annotation practical",
        pass_threshold=threshold,
        max_attempts=2,
        task_count=2,
        status=STATUS_PUBLISHED,
    )
    db.add(assessment)
    db.flush()
    db.add_all(
        [
            AssessmentTask(
                assessment_id=assessment.id,
                ordinal=1,
                template_id=template.id,
                payload={"text": "I love this."},
                expected_answer={"key": "A"},
                points=1,
            ),
            AssessmentTask(
                assessment_id=assessment.id,
                ordinal=2,
                template_id=template.id,
                payload={"text": "This is awful."},
                expected_answer={"key": "A"},
                points=1,
            ),
        ]
    )
    db.flush()
    return skill, assessment


def _answer(attempt: dict, key: str) -> dict:
    return {str(task["task_id"]): {"key": key} for task in attempt["tasks"]}


def test_passing_the_assessment_verifies_the_skill(db: Session) -> None:
    skill, assessment = _assessment(db)
    student = make_user(db)

    attempt = assessments.start_attempt(db, student, assessment.slug)
    assert len(attempt["tasks"]) == 2
    result = assessments.submit_attempt(db, student, attempt["attempt_id"], _answer(attempt, "A"))

    assert result["passed"] is True
    assert result["score"] == 100
    assert result["verification_status"] == "verified"
    record = db.scalars(select(VerificationRecord)).one()
    assert record.status == "verified" and record.verified_at is not None

    entry = db.scalars(
        select(TranscriptEntry).where(TranscriptEntry.kind == "proved")
    ).one()
    assert entry.evidence_type == "assessment_attempt"
    assert int(entry.evidence_id) == attempt["attempt_id"]
    assert entry.skill_id == skill.id

    # Starting the sitting is its own, logged transition; passing is the second.
    events = db.scalars(select(VerificationEvent).order_by(VerificationEvent.id)).all()
    assert [event.to_status for event in events] == ["in_progress", "verified"]
    assert events[-1].evidence_type == "assessment"
    assert events[-1].evidence_id == str(attempt["attempt_id"])


def test_a_failed_attempt_leaves_the_student_in_progress(db: Session) -> None:
    _skill, assessment = _assessment(db)
    student = make_user(db)

    attempt = assessments.start_attempt(db, student, assessment.slug)
    result = assessments.submit_attempt(db, student, attempt["attempt_id"], _answer(attempt, "B"))

    assert result["passed"] is False
    assert result["verification_status"] == "in_progress"
    assert db.scalars(select(TranscriptEntry).where(TranscriptEntry.kind == "proved")).all() == []


def test_watching_every_lesson_never_verifies(db: Session) -> None:
    skill = make_skill(db)
    path = LearningPath(
        skill_id=skill.id, slug=unique("path"), title="Annotation", status=STATUS_PUBLISHED
    )
    db.add(path)
    db.flush()
    lesson = Lesson(
        skill_id=skill.id,
        slug=unique("lesson"),
        title="Intro",
        body_md="Read this.",
        status=STATUS_PUBLISHED,
    )
    db.add(lesson)
    db.flush()
    db.add(LearningPathStep(path_id=path.id, ordinal=1, kind="lesson", lesson_id=lesson.id))
    db.flush()
    student = make_user(db)

    learning.complete_lesson(db, student, lesson.id)

    assert db.scalars(select(VerificationRecord)).all() == []
    assert state.status_for(db, student.id, skill.id) == "unverified"


def test_the_attempt_limit_is_enforced(db: Session) -> None:
    _skill, assessment = _assessment(db, threshold=101)
    student = make_user(db)

    first = assessments.start_attempt(db, student, assessment.slug)
    assessments.submit_attempt(db, student, first["attempt_id"], _answer(first, "B"))
    second = assessments.start_attempt(db, student, assessment.slug)
    assessments.submit_attempt(db, student, second["attempt_id"], _answer(second, "B"))

    with pytest.raises(ApiError) as excinfo:
        assessments.start_attempt(db, student, assessment.slug)
    assert excinfo.value.code == "attempt_limit_reached"


def test_an_unsubmitted_attempt_resumes_with_the_same_tasks(db: Session) -> None:
    _skill, assessment = _assessment(db)
    student = make_user(db)

    first = assessments.start_attempt(db, student, assessment.slug)
    again = assessments.start_attempt(db, student, assessment.slug)

    assert first["attempt_id"] == again["attempt_id"]
    assert [task["task_id"] for task in first["tasks"]] == [
        task["task_id"] for task in again["tasks"]
    ]


def test_another_students_attempt_is_not_found(db: Session) -> None:
    _skill, assessment = _assessment(db)
    student = make_user(db)
    intruder = make_user(db)
    attempt = assessments.start_attempt(db, student, assessment.slug)

    with pytest.raises(ApiError) as excinfo:
        assessments.submit_attempt(db, intruder, attempt["attempt_id"], {})
    assert excinfo.value.status_code == 404
    assert excinfo.value.code == "attempt_not_found"


def test_an_attempt_cannot_be_graded_twice(db: Session) -> None:
    _skill, assessment = _assessment(db)
    student = make_user(db)
    attempt = assessments.start_attempt(db, student, assessment.slug)
    assessments.submit_attempt(db, student, attempt["attempt_id"], _answer(attempt, "A"))

    with pytest.raises(ApiError) as excinfo:
        assessments.submit_attempt(db, student, attempt["attempt_id"], _answer(attempt, "A"))
    assert excinfo.value.code == "attempt_already_submitted"


def test_an_override_needs_a_reason_and_is_logged(db: Session) -> None:
    skill = make_skill(db)
    student = make_user(db)
    ops = make_user(db)
    record = state.ensure_record(db, student.id, skill.id)

    with pytest.raises(ApiError) as excinfo:
        state.override(db, record=record, to_status="verified", actor=ops, reason=" ")
    assert excinfo.value.status_code == 400
    assert excinfo.value.code == "override_requires_reason"

    state.override(db, record=record, to_status="verified", actor=ops, reason="gold task mis-scored")

    assert record.status == "verified"
    event = db.scalars(select(VerificationEvent)).one()
    assert event.evidence_type == "manual_override"
    assert event.actor_user_id == ops.id
    assert event.reason == "gold task mis-scored"


def test_an_unknown_verification_status_is_refused(db: Session) -> None:
    skill = make_skill(db)
    record = state.ensure_record(db, make_user(db).id, skill.id)

    with pytest.raises(ApiError):
        state.transition(
            db,
            record,
            to_status="trusted",
            evidence_type="assessment",
            evidence_id=1,
        )


def test_the_transcript_links_every_entry_to_evidence(db: Session) -> None:
    _skill, assessment = _assessment(db)
    student = make_user(db)
    attempt = assessments.start_attempt(db, student, assessment.slug)
    assessments.submit_attempt(db, student, attempt["attempt_id"], _answer(attempt, "A"))

    transcript = transcript_service.get_transcript(db, student)

    assert transcript["entries"]
    for entry in transcript["entries"]:
        assert entry["evidence"]["type"]
        assert entry["evidence"]["id"]
