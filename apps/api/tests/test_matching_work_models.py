"""Phase 0 PR 0.3b — matching and work delivery shapes.

Product rules under test: one stored verdict per student per opportunity, every
gap points back into learning or verification, a project has exactly one
opportunity, and a retried submission records once because its idempotency key is
unique. Uses the shared `db` fixture.
"""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import User
from app.models.matching import (
    GAP_MISSING,
    OPPORTUNITY_EXTERNAL,
    OPPORTUNITY_MANAGED,
    MatchResult,
    Opportunity,
    Requirement,
    SkillGap,
)
from app.models.skills import LearningPath, Skill
from app.models.verification import Assessment
from app.models.work import (
    Assignment,
    Cohort,
    CohortMember,
    Project,
    Submission,
)

EXPECTED_TABLES = {
    "opportunities",
    "requirements",
    "match_results",
    "skill_gaps",
    "projects",
    "cohorts",
    "cohort_members",
    "assignments",
    "submissions",
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


def _opportunity(db: Session, **overrides) -> Opportunity:
    data = {
        "slug": f"opp-{uuid.uuid4().hex[:8]}",
        "title": "Annotate 5,000 records",
        "type": OPPORTUNITY_MANAGED,
    }
    data.update(overrides)
    opportunity = Opportunity(**data)
    db.add(opportunity)
    db.flush()
    return opportunity


def test_tables_exist(db: Session) -> None:
    assert EXPECTED_TABLES <= set(inspect(db.get_bind()).get_table_names())


def test_opportunity_type_is_the_fee_switch(db: Session) -> None:
    managed = _opportunity(db)
    external = _opportunity(db, type=OPPORTUNITY_EXTERNAL, title="Scholarship")
    assert managed.type == "managed" and external.type == "external"
    # Currency and rate are per row and optional: an external listing has neither.
    assert external.currency is None and external.rate_minor is None


def test_requirement_can_point_at_a_skill_or_a_value(db: Session) -> None:
    opportunity, skill = _opportunity(db), _skill(db)
    db.add_all(
        [
            Requirement(opportunity_id=opportunity.id, kind="skill", skill_id=skill.id),
            Requirement(
                opportunity_id=opportunity.id,
                kind="verification",
                skill_id=skill.id,
                minimum_value="verified",
            ),
        ]
    )
    db.flush()
    kinds = db.scalars(select(Requirement.kind).order_by(Requirement.id)).all()
    assert kinds == ["skill", "verification"]
    assert db.scalar(select(Requirement.is_mandatory).limit(1)) is True


def test_one_match_verdict_per_student_and_opportunity(db: Session) -> None:
    opportunity, user = _opportunity(db), _user(db)
    db.add(MatchResult(opportunity_id=opportunity.id, user_id=user.id, explanation=[]))
    db.flush()
    db.add(MatchResult(opportunity_id=opportunity.id, user_id=user.id))
    with pytest.raises(IntegrityError):
        db.flush()


def test_every_gap_points_back_into_learning_or_verification(db: Session) -> None:
    opportunity, user, skill = _opportunity(db), _user(db), _skill(db)
    requirement = Requirement(opportunity_id=opportunity.id, kind="verification", skill_id=skill.id)
    path = LearningPath(slug=f"p-{uuid.uuid4().hex[:8]}", title="Annotate", skill_id=skill.id)
    assessment = Assessment(slug=f"a-{uuid.uuid4().hex[:8]}", title="Assess", skill_id=skill.id)
    db.add_all([requirement, path, assessment])
    db.flush()

    gap = SkillGap(
        user_id=user.id,
        opportunity_id=opportunity.id,
        requirement_id=requirement.id,
        closes_via_learning_path_id=path.id,
        closes_via_assessment_id=assessment.id,
    )
    db.add(gap)
    db.flush()
    assert gap.status == GAP_MISSING
    assert gap.closes_via_assessment_id == assessment.id

    db.add(
        SkillGap(user_id=user.id, opportunity_id=opportunity.id, requirement_id=requirement.id)
    )
    with pytest.raises(IntegrityError):
        db.flush()


def test_project_is_one_to_one_with_its_opportunity(db: Session) -> None:
    opportunity = _opportunity(db)
    db.add(Project(opportunity_id=opportunity.id, slug="proj-a", title="Project A"))
    db.flush()
    db.add(Project(opportunity_id=opportunity.id, slug="proj-b", title="Project B"))
    with pytest.raises(IntegrityError):
        db.flush()


def test_cohort_membership_is_unique_and_removal_is_a_status(db: Session) -> None:
    opportunity, user = _opportunity(db), _user(db)
    project = Project(opportunity_id=opportunity.id, slug="proj", title="Project")
    db.add(project)
    db.flush()
    cohort = Cohort(project_id=project.id, name="Lagos batch 1")
    db.add(cohort)
    db.flush()
    member = CohortMember(cohort_id=cohort.id, user_id=user.id)
    db.add(member)
    db.flush()
    assert member.status == "invited" and member.joined_at is None

    member.status = "removed"
    db.flush()
    db.add(CohortMember(cohort_id=cohort.id, user_id=user.id))
    with pytest.raises(IntegrityError):
        db.flush()


def test_a_retried_submission_records_once(db: Session) -> None:
    opportunity, user = _opportunity(db), _user(db)
    project = Project(opportunity_id=opportunity.id, slug="proj", title="Project")
    db.add(project)
    db.flush()
    assignment = Assignment(project_id=project.id, user_id=user.id, title="Annotate 10")
    db.add(assignment)
    db.flush()

    key = str(uuid.uuid4())
    db.add(
        Submission(
            assignment_id=assignment.id,
            user_id=user.id,
            payload={"labels": ["positive"]},
            idempotency_key=key,
        )
    )
    db.flush()
    db.add(
        Submission(
            assignment_id=assignment.id,
            user_id=user.id,
            payload={"labels": ["positive"]},
            idempotency_key=key,
        )
    )
    with pytest.raises(IntegrityError):
        db.flush()


def test_deleting_a_project_removes_its_cohorts_and_assignments(db: Session) -> None:
    opportunity, user = _opportunity(db), _user(db)
    project = Project(opportunity_id=opportunity.id, slug="proj", title="Project")
    db.add(project)
    db.flush()
    cohort = Cohort(project_id=project.id, name="Batch")
    db.add(cohort)
    db.flush()
    db.add(CohortMember(cohort_id=cohort.id, user_id=user.id))
    db.add(Assignment(project_id=project.id, user_id=user.id, title="Annotate"))
    db.flush()

    db.delete(project)
    db.flush()
    assert db.scalars(select(Cohort)).all() == []
    assert db.scalars(select(CohortMember)).all() == []
    assert db.scalars(select(Assignment)).all() == []
