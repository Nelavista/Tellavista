"""Per-skill practice gates and evidence-backed talent output."""
from __future__ import annotations

import pytest
from factories import make_profile, make_skill, make_template, make_user, unique
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import UserLanguage
from app.models.skills import STATUS_PUBLISHED
from app.models.verification import Assessment, AssessmentTask
from app.services.skills import tasks
from app.services.talent import profile as talent
from app.services.verification import assessments, state, transcript


def _structured_assessment(db: Session):
    skill = make_skill(db)
    template = make_template(
        db,
        skill,
        validator="exact_key",
        config={"expected_answer": {"key": "A"}, "task_spec": {"kind": "labeling"}},
    )
    assessment = Assessment(
        skill_id=skill.id,
        slug=unique("structured-assessment"),
        title="Structured assessment",
        task_count=1,
        status=STATUS_PUBLISHED,
    )
    db.add(assessment)
    db.flush()
    db.add(
        AssessmentTask(
            assessment_id=assessment.id,
            ordinal=1,
            template_id=template.id,
            payload={"text": "A sample"},
            expected_answer={"key": "A"},
            points=1,
        )
    )
    db.flush()
    return skill, template, assessment


def test_structured_assessment_requires_scored_practice_first(db: Session) -> None:
    _skill, template, assessment = _structured_assessment(db)
    student = make_user(db)

    with pytest.raises(ApiError) as excinfo:
        assessments.start_attempt(db, student, assessment.slug)
    assert excinfo.value.code == "practice_prerequisite_incomplete"
    assert excinfo.value.details["missing"] == [template.id]

    tasks.submit_practice(db, student, template_id=template.id, answer={"key": "A"})
    attempt = assessments.start_attempt(db, student, assessment.slug)
    assert attempt["tasks"]

    learned = transcript.get_transcript(db, student)["learned"]
    assert learned[0]["evidence"]["type"] == "practice_attempt"


def test_talent_skill_contains_verification_evidence_and_scoped_context(db: Session) -> None:
    student = make_user(db, university="FUTA", department="Surveying", level="400")
    make_profile(db, student, profile_visibility="public", location="Akure")
    db.add(UserLanguage(user_id=student.id, language="Yoruba", level="fluent"))
    skill = make_skill(db)
    record = state.ensure_record(db, student.id, skill.id)
    state.transition(
        db,
        record,
        to_status=state.IN_PROGRESS,
        evidence_type="assessment",
        evidence_id=101,
        reason="assessment started",
    )
    state.transition(
        db,
        record,
        to_status=state.VERIFIED,
        evidence_type="assessment",
        evidence_id=102,
        reason="assessment passed",
    )

    payload = talent.build_profile(db, student, owner=True)

    assert payload["academic"] == {"university": "FUTA", "department": "Surveying", "level": "400"}
    assert payload["availability"]["languages"] == [{"language": "Yoruba", "level": "fluent"}]
    evidence = payload["verified_skills"][0]["evidence"]
    assert [item["id"] for item in evidence] == ["101", "102"]
    assert evidence[-1]["reason"] == "assessment passed"
