"""Shared factories for service-level tests.

Kept deliberately small: the factories build *valid rows* and never assert. A test
that needs a different state (an external opportunity, a reworked submission)
changes one field rather than copying 30 lines of setup.

`db` is the in-memory session from `conftest.py`; nothing here commits, so the
fixture's rollback always leaves a clean database for the next test.
"""
from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.admin import (
    ROLE_OPS_ADMIN,
    ROLE_REVIEWER,
    ROLE_STUDENT,
    Role,
)
from app.models.identity import User, UserProfile
from app.models.matching import Opportunity
from app.models.skills import Skill, TaskTemplate
from app.models.verification import VERIFIED, VerificationRecord
from app.models.work import (
    MEMBER_ACTIVE,
    Assignment,
    Cohort,
    CohortMember,
    Project,
)
from app.services.matching import opportunities
from app.services.work import cohorts


def unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def make_user(db: Session, role_code: str = ROLE_STUDENT, **overrides) -> User:
    role = db.scalar(select(Role).where(Role.code == role_code))
    suffix = uuid.uuid4().hex[:8]
    data = {
        "email": f"u{suffix}@example.test",
        "username": f"u{suffix}",
        "name": "Test Student",
        "email_verified": True,
        "password_hash": hash_password("correct-horse-battery"),
        "role_id": role.id if role else None,
    }
    data.update(overrides)
    user = User(**data)
    db.add(user)
    db.flush()
    return user


def make_ops(db: Session, **overrides) -> User:
    return make_user(db, ROLE_OPS_ADMIN, **overrides)


def make_reviewer(db: Session, **overrides) -> User:
    return make_user(db, ROLE_REVIEWER, **overrides)


def make_profile(db: Session, user: User, **overrides) -> UserProfile:
    data = {"user_id": user.id, "display_name": user.name or user.username}
    data.update(overrides)
    profile = UserProfile(**data)
    db.add(profile)
    db.flush()
    return profile


def make_skill(db: Session, **overrides) -> Skill:
    suffix = uuid.uuid4().hex[:8]
    data = {
        "slug": f"ai-data-annotation-{suffix}",
        "name": f"AI Data Annotation {suffix}",
        "is_active": True,
    }
    data.update(overrides)
    skill = Skill(**data)
    db.add(skill)
    db.flush()
    return skill


def make_template(db: Session, skill: Skill, **overrides) -> TaskTemplate:
    data = {
        "skill_id": skill.id,
        "slug": unique("template"),
        "name": "Sentiment label",
        "instructions_md": "Label the text positive or negative.",
        "input_schema": {"type": "object", "required": ["text"]},
        "answer_schema": {"type": "object", "required": ["label"]},
        "validator": "exact_key",
        "config": {"gold_expected": {"label": "positive"}},
        "status": "published",
    }
    data.update(overrides)
    template = TaskTemplate(**data)
    db.add(template)
    db.flush()
    return template


def verify(db: Session, user: User, skill: Skill, status: str = VERIFIED) -> VerificationRecord:
    record = VerificationRecord(user_id=user.id, skill_id=skill.id, status=status)
    db.add(record)
    db.flush()
    return record


def make_opportunity(
    db: Session,
    actor: User,
    *,
    type: str = "managed",
    requirements: list[dict] | None = None,
    currency: str | None = "USD",
    rate_minor: int | None = 1_000,
    department_id: int | None = None,
    **overrides,
) -> Opportunity:
    data = {
        "slug": unique("opportunity"),
        "title": "Managed annotation project",
        "client_name": "Example Client",
        "department_id": department_id,
        "headcount": 10,
        "requirements": requirements if requirements is not None else [],
    }
    if type == "external":
        currency = None
        rate_minor = None
        data["title"] = "External internship"
        data["client_name"] = "External employer"
    data.update(overrides)
    return opportunities.create_opportunity(
        db,
        actor,
        type=type,
        currency=currency,
        rate_minor=rate_minor,
        **data,
    )


def make_project(
    db: Session,
    actor: User,
    opportunity: Opportunity,
    *,
    status: str = "active",
    starts_on: date | None = None,
    **overrides,
) -> Project:
    data = {
        "slug": unique("project"),
        "title": "Annotation pilot",
        "status": status,
        "starts_on": starts_on,
    }
    data.update(overrides)
    return cohorts.create_project(db, actor, opportunity=opportunity, **data)


def make_member(db: Session, project: Project, student: User, *, status: str = MEMBER_ACTIVE):
    """An accepted cohort member, built directly: invitation rules are tested separately."""
    cohort = db.scalar(select(Cohort).where(Cohort.project_id == project.id))
    if cohort is None:
        cohort = Cohort(project_id=project.id, name=unique("cohort"), status="active")
        db.add(cohort)
        db.flush()
    member = CohortMember(cohort_id=cohort.id, user_id=student.id, status=status)
    db.add(member)
    db.flush()
    return member


def make_assignment(
    db: Session,
    project: Project,
    student: User,
    *,
    template: TaskTemplate | None = None,
    title: str = "Label 10 rows",
    status: str = "assigned",
    **overrides,
) -> Assignment:
    data = {
        "project_id": project.id,
        "user_id": student.id,
        "template_id": template.id if template else None,
        "title": title,
        "status": status,
    }
    data.update(overrides)
    assignment = Assignment(**data)
    db.add(assignment)
    db.flush()
    return assignment


__all__ = [
    "make_assignment",
    "make_member",
    "make_opportunity",
    "make_ops",
    "make_profile",
    "make_project",
    "make_reviewer",
    "make_skill",
    "make_template",
    "make_user",
    "unique",
    "verify",
]
