"""Phase 4 — matching explains itself, and a "no" always has a next step.

The product rule under test: every result says why the student qualifies or exactly
what is missing, and every gap points back into learning or verification. A
quality consequence blocks matching but never hides the reason.
"""
from __future__ import annotations

import pytest
from factories import make_opportunity, make_ops, make_skill, make_user, verify
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import UserLanguage
from app.models.matching import SkillGap
from app.models.quality import CONSEQUENCE_RESTRICT_MATCHING, QualityConsequence
from app.models.skills import STATUS_PUBLISHED, LearningPath
from app.models.verification import Assessment
from app.services.matching import engine, opportunities


def _published_path(db: Session, skill_id: int) -> LearningPath:
    path = LearningPath(
        skill_id=skill_id,
        slug="ai-data-annotation-path",
        title="AI Data Annotation",
        status=STATUS_PUBLISHED,
    )
    db.add(path)
    db.flush()
    return path


def _published_assessment(db: Session, skill_id: int) -> Assessment:
    assessment = Assessment(
        skill_id=skill_id,
        slug="ai-data-annotation-assessment",
        title="Annotation practical",
        status=STATUS_PUBLISHED,
    )
    db.add(assessment)
    db.flush()
    return assessment


def test_unverified_student_sees_the_exact_gap_and_how_to_close_it(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    path = _published_path(db, skill.id)
    assessment = _published_assessment(db, skill.id)
    opportunity = make_opportunity(
        db,
        ops,
        requirements=[{"kind": "skill", "skill_id": skill.id, "is_mandatory": True}],
    )

    result = engine.evaluate(db, student, opportunity)

    assert result["eligible"] is False
    assert result["missing"][0]["kind"] == "skill"
    assert "not verified" in result["missing"][0]["detail"]
    step = result["next_steps"][0]
    assert step["closes_via"]["learning_path_id"] == path.id
    assert step["closes_via"]["learning_path_slug"] == path.slug
    assert step["closes_via"]["assessment_id"] == assessment.id
    assert step["closes_via"]["assessment_slug"] == assessment.slug


def test_verified_skill_makes_the_student_eligible_and_says_why(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    verify(db, student, skill)
    opportunity = make_opportunity(
        db, ops, requirements=[{"kind": "skill", "skill_id": skill.id}]
    )

    result = engine.evaluate(db, student, opportunity)

    assert result["eligible"] is True
    assert result["score"] == 100
    assert result["qualifies_because"] == ["Skill verified."]
    assert result["missing"] == []


def test_persist_writes_a_gap_row_and_clears_it_when_met(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    opportunity = make_opportunity(
        db, ops, requirements=[{"kind": "skill", "skill_id": skill.id}]
    )

    engine.match_user_to_opportunity(db, student, opportunity)
    gap = db.scalars(select(SkillGap)).one()
    assert gap.status == "missing" and gap.user_id == student.id
    assert engine.gaps_for_user(db, student.id, opportunity.id)[0]["detail"]

    verify(db, student, skill)
    engine.match_user_to_opportunity(db, student, opportunity)
    assert db.scalars(select(SkillGap)).all() == []


def test_language_requirement_names_the_language_to_add(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(
        db, ops, requirements=[{"kind": "language", "minimum_value": "Hausa"}]
    )

    missing = engine.evaluate(db, student, opportunity)["missing"][0]
    assert missing["met"] is False
    assert "Hausa" in missing["detail"]

    db.add(UserLanguage(user_id=student.id, language="Hausa", level="fluent"))
    db.flush()
    assert engine.evaluate(db, student, opportunity)["eligible"] is True


def test_optional_requirement_does_not_block_eligibility(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(
        db,
        ops,
        requirements=[
            {"kind": "language", "minimum_value": "Yoruba", "is_mandatory": False}
        ],
    )

    result = engine.evaluate(db, student, opportunity)
    assert result["eligible"] is True
    assert result["score"] == 0  # nothing met, but nothing mandatory either
    assert result["next_steps"][0]["detail"]


def test_quality_restriction_blocks_matching_with_a_visible_reason(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)
    db.add(
        QualityConsequence(
            user_id=student.id,
            kind=CONSEQUENCE_RESTRICT_MATCHING,
            reason="three consecutive reviews below the bar",
            active=True,
        )
    )
    db.flush()

    result = engine.evaluate(db, student, opportunity)

    assert result["eligible"] is False
    assert result["blocked"] is True
    assert result["blocked_reason"] == "three consecutive reviews below the bar"


def test_only_managed_opportunities_can_earn(db: Session) -> None:
    ops = make_ops(db)
    managed = make_opportunity(db, ops)
    external = make_opportunity(db, ops, type="external")

    assert engine.is_managed(managed) is True
    assert engine.is_managed(external) is False


def test_external_opportunity_cannot_carry_a_rate(db: Session) -> None:
    ops = make_ops(db)
    with pytest.raises(ApiError) as excinfo:
        opportunities.create_opportunity(
            db,
            ops,
            type="external",
            slug="external-with-rate",
            title="Internship",
            currency="USD",
            rate_minor=100,
        )
    assert excinfo.value.status_code == 400
    assert excinfo.value.code == "external_has_no_rate"


def test_student_cannot_apply_to_managed_work(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    managed = make_opportunity(db, ops)

    with pytest.raises(ApiError) as excinfo:
        opportunities.apply_external(db, student, slug=managed.slug)
    assert excinfo.value.code == "managed_work_is_invitation_only"


def test_external_application_is_idempotent(db: Session) -> None:
    ops = make_ops(db)
    student = make_user(db)
    external = make_opportunity(db, ops, type="external")
    opportunities.update_opportunity(db, ops, external, status="open")

    first = opportunities.apply_external(db, student, slug=external.slug, note="Keen")
    second = opportunities.apply_external(db, student, slug=external.slug, note="Keen again")

    assert first.id == second.id
    assert len(opportunities.my_applications(db, student)) == 1
