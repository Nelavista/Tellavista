"""Phase 5 — quality control: the review decides pay, and the record is a projection.

These tests pin the rules the PRD cares about:

* only an approval can earn money, and the earning line says how it was computed;
* a gold task's known answer beats a lenient reviewer;
* poor reviews create consequences from configuration, not hard-coded branches;
* an override is possible, but it needs a reason.
"""
from __future__ import annotations

import pytest
from factories import (
    make_assignment,
    make_opportunity,
    make_ops,
    make_project,
    make_reviewer,
    make_skill,
    make_template,
    make_user,
    unique,
    verify,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.engagement import Notification
from app.models.ledger import EarningLine
from app.models.quality import QualityConsequence, QualityRecord, QualityStandard
from app.models.verification import AT_RISK, SUSPENDED, VERIFIED, Assessment
from app.services.verification import state
from app.services.work import quality


def _setup(db: Session, *, rate_minor: int = 1_000, verified: bool = True):
    ops = make_ops(db)
    reviewer = make_reviewer(db)
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    opportunity = make_opportunity(db, ops, rate_minor=rate_minor)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student, template=template)
    if verified:
        verify(db, student, skill)
    return ops, reviewer, student, skill, project, assignment


def _submit(db: Session, student, assignment, payload: dict, key: str):
    from app.services.work import delivery

    submission, _ = delivery.submit_work(
        db, student, assignment_id=assignment.id, payload=payload, client_key=key
    )
    return submission


def test_approval_creates_one_earning_line_with_its_explanation(db: Session) -> None:
    _ops, reviewer, student, _skill, project, assignment = _setup(db)
    submission = _submit(db, student, assignment, {"label": "positive", "task_count": 3}, "q-1")

    review = quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="approved", score=95
    )

    assert review.verdict == "approved"
    line = db.scalars(select(EarningLine)).one()
    assert line.amount_minor == 3_000
    assert line.rate_minor == 1_000
    assert line.task_count == 3
    assert line.status == "approved"
    assert "3 task(s)" in line.description
    assert submission.status == "approved"
    assert assignment.status == "approved"


def test_rework_earns_nothing_and_warns_once(db: Session) -> None:
    _ops, reviewer, student, _skill, project, assignment = _setup(db)
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-2")

    quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="rework", notes="Fix the labels."
    )

    assert db.scalars(select(EarningLine)).all() == []
    assert submission.status == "rework"
    consequence = db.scalars(select(QualityConsequence)).one()
    assert consequence.kind == "warn"
    assert consequence.user_id == student.id
    assert "quality bar" in consequence.reason

    record = db.scalar(
        select(QualityRecord).where(
            QualityRecord.user_id == student.id, QualityRecord.project_id == project.id
        )
    )
    assert record.reworks == 1 and record.approvals == 0
    assert record.poor_streak == 1


def test_a_gold_task_is_scored_by_its_known_answer(db: Session) -> None:
    _ops, reviewer, student, _skill, _project, assignment = _setup(db)
    submission = _submit(db, student, assignment, {"label": "negative"}, "q-3")
    submission.is_gold = True
    submission.gold_expected = {"label": "positive"}
    db.flush()

    review = quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="approved", score=100
    )

    # The reviewer said 100, but the known answer says the work is wrong.
    assert review.is_gold is True
    assert review.gold_correct is False
    assert review.score == 0


def test_an_override_must_give_a_reason(db: Session) -> None:
    _ops, reviewer, student, _skill, _project, assignment = _setup(db)
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-4")

    with pytest.raises(ApiError) as excinfo:
        quality.review_submission(
            db, reviewer, submission_id=submission.id, verdict="approved", is_override=True
        )
    assert excinfo.value.code == "reason_required"


def test_a_second_reviewer_is_required_for_a_sampled_second_review(db: Session) -> None:
    _ops, reviewer, student, _skill, project, assignment = _setup(db)
    standard = quality.ensure_standard(db, project)
    standard.rules = {**(standard.rules or {}), "double_review_percent": 100}
    db.flush()
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-5")
    quality.review_submission(db, reviewer, submission_id=submission.id, verdict="approved")

    with pytest.raises(ApiError) as excinfo:
        quality.review_submission(
            db, reviewer, submission_id=submission.id, verdict="approved"
        )
    assert excinfo.value.code == "second_reviewer_required"

    other = make_reviewer(db)
    review = quality.review_submission(
        db, other, submission_id=submission.id, verdict="approved"
    )
    assert review.agrees_with_review_id is not None


def test_a_poor_review_moves_a_verified_skill_at_risk(db: Session) -> None:
    _ops, reviewer, student, skill, project, assignment = _setup(db)
    standard = quality.ensure_standard(db, project)
    standard.pass_threshold = 80
    db.flush()
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-6")

    quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="rejected", score=10
    )

    record = db.scalar(
        select(QualityRecord).where(
            QualityRecord.user_id == student.id, QualityRecord.project_id.is_(None)
        )
    )
    assert record is not None and record.average_score == 10
    assert state.status_for(db, student.id, skill.id) == AT_RISK


def test_a_suspended_badge_prompts_the_student_with_the_way_back(db: Session) -> None:
    _ops, reviewer, student, skill, project, assignment = _setup(db)
    standard = quality.ensure_standard(db, project)
    standard.pass_threshold = 80
    assessment = Assessment(
        skill_id=skill.id,
        slug=unique("reverify"),
        title="Annotation practical",
        pass_threshold=80,
        status="published",
    )
    db.add(assessment)
    db.flush()

    # First poor review: verified → at risk. Second: at risk → suspended.
    for key in ("q-8a", "q-8b"):
        submission = _submit(db, student, assignment, {"label": "positive"}, key)
        quality.review_submission(
            db, reviewer, submission_id=submission.id, verdict="rejected", score=10
        )

    assert state.status_for(db, student.id, skill.id) == SUSPENDED

    rows = list(
        db.scalars(
            select(Notification)
            .where(Notification.user_id == student.id, Notification.kind == "verification")
            .order_by(Notification.id)
        ).all()
    )
    # Both transitions are announced, and the prompt names the way back.
    assert [row.data["verification_status"] for row in rows] == [AT_RISK, SUSPENDED]
    assert rows[-1].data["skill_slug"] == skill.slug
    assert rows[-1].data["assessment_slug"] == assessment.slug
    assert "suspended" in rows[-1].body.lower()


def test_quality_can_restore_an_at_risk_skill_but_cannot_verify_an_unproven_one(
    db: Session,
) -> None:
    _ops, reviewer, student, skill, _project, assignment = _setup(db)
    record = state.ensure_record(db, student.id, skill.id)
    record.status = AT_RISK
    db.flush()
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-6b")

    quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="approved", score=95
    )

    assert state.status_for(db, student.id, skill.id) == VERIFIED

    # A different, unproven skill is untouched by good work on this project.
    other_skill = make_skill(db)
    assert state.status_for(db, student.id, other_skill.id) == "unverified"


def test_quality_record_is_recomputed_from_reviews_not_incremented(db: Session) -> None:
    _ops, reviewer, student, _skill, project, assignment = _setup(db)
    first = _submit(db, student, assignment, {"label": "positive"}, "q-7")
    quality.review_submission(db, reviewer, submission_id=first.id, verdict="approved", score=90)

    record = quality.recompute_record(db, student.id, project_id=project.id)
    assert record.reviews_count == 1 and record.average_score == 90

    # Recomputing again from the same reviews changes nothing.
    again = quality.recompute_record(db, student.id, project_id=project.id)
    assert again.id == record.id
    assert again.reviews_count == 1 and again.average_score == 90


def test_only_unreviewed_submissions_are_in_the_queue(db: Session) -> None:
    _ops, reviewer, student, _skill, _project, assignment = _setup(db)
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-8")

    assert [row["submission_id"] for row in quality.review_queue(db)] == [submission.id]
    quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="approved", score=90
    )
    assert quality.review_queue(db) == []


def test_my_quality_explains_the_record_and_active_consequences(db: Session) -> None:
    _ops, reviewer, student, _skill, _project, assignment = _setup(db)
    submission = _submit(db, student, assignment, {"label": "positive"}, "q-9")
    quality.review_submission(
        db, reviewer, submission_id=submission.id, verdict="rework", score=40
    )

    payload = quality.my_quality(db, student)
    assert payload["record"]["reviews_count"] == 1
    assert payload["record"]["average_score"] == 40
    assert payload["consequences"][0]["kind"] == "warn"


def test_standard_rules_are_configuration(db: Session) -> None:
    ops = make_ops(db)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)

    standard = quality.set_standard(
        db,
        ops,
        project,
        pass_threshold=70,
        rules={"warn_after": 3, "gold_rate_percent": 0},
    )

    assert isinstance(standard, QualityStandard)
    assert standard.pass_threshold == 70
    assert standard.rules["warn_after"] == 3
    assert standard.rules["gold_rate_percent"] == 0

    with pytest.raises(ApiError):
        quality.set_standard(db, ops, project, pass_threshold=101)
