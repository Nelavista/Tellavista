"""Onboarding wizard endpoints: taxonomy → enrolment (Phase 1)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.v1.domains.identity.schemas import (
    CourseOut,
    EnrolIn,
    EnrolmentOut,
    MessageOut,
    OnboardingStateOut,
    SemesterOut,
    SubdivisionOut,
    UniversityOut,
    WaitlistIn,
)
from app.core import observability
from app.db.session import get_db
from app.models.identity import User
from app.services.identity import onboarding

router = APIRouter(prefix="/onboarding", tags=["identity"])


@router.get("/universities", response_model=list[UniversityOut])
def universities(db: Session = Depends(get_db)) -> list[UniversityOut]:
    return [
        UniversityOut(id=row.id, name=row.name, slug=row.slug)
        for row in onboarding.list_universities(db)
    ]


@router.get("/universities/{university_id}/faculties", response_model=list[SubdivisionOut])
def faculties(university_id: int, db: Session = Depends(get_db)) -> list[SubdivisionOut]:
    return [
        SubdivisionOut(id=row.id, name=row.name)
        for row in onboarding.list_faculties(db, university_id)
    ]


@router.get("/faculties/{faculty_id}/departments", response_model=list[SubdivisionOut])
def departments(faculty_id: int, db: Session = Depends(get_db)) -> list[SubdivisionOut]:
    return [
        SubdivisionOut(id=row.id, name=row.name)
        for row in onboarding.list_departments(db, faculty_id)
    ]


@router.get("/departments/{department_id}/courses", response_model=list[CourseOut])
def courses(
    department_id: int,
    level: str | None = Query(default=None, max_length=10),
    db: Session = Depends(get_db),
) -> list[CourseOut]:
    return [
        CourseOut(id=row.id, code=row.code, title=row.title, level=row.level)
        for row in onboarding.list_courses(db, department_id, level=level)
    ]


@router.get("/sessions/current", response_model=SemesterOut | None)
def current_semester(db: Session = Depends(get_db)) -> SemesterOut | None:
    row = onboarding.current_session(db)
    if row is None:
        return None
    return SemesterOut(
        id=row.id, name=row.name, ordinal=row.ordinal, session_id=row.session_id
    )


@router.get("/sessions/{session_id}/semesters", response_model=list[SemesterOut])
def semesters(session_id: int, db: Session = Depends(get_db)) -> list[SemesterOut]:
    return [
        SemesterOut(id=row.id, name=row.name, ordinal=row.ordinal, session_id=row.session_id)
        for row in onboarding.list_semesters(db, session_id)
    ]


@router.post("/enrol", response_model=list[EnrolmentOut], status_code=201)
def enrol(
    payload: EnrolIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[EnrolmentOut]:
    onboarding.enrol(
        db,
        user,
        course_ids=payload.course_ids,
        session_id=payload.session_id,
        semester_id=payload.semester_id,
    )
    db.commit()
    rows = onboarding.my_enrolments(db, user)
    observability.capture(
        user.id, observability.EVENTS["enrolled"], {"courses": len(rows)}
    )
    return [EnrolmentOut(**row) for row in rows]


@router.get("/state", response_model=OnboardingStateOut)
def state(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> OnboardingStateOut:
    context = onboarding.academic_context(db, user)
    semester = onboarding.current_session(db)
    rows = onboarding.my_enrolments(db, user)
    return OnboardingStateOut(
        profile_completed=bool(user.profile and user.profile.display_name),
        has_enrolment=bool(rows),
        current_semester=(
            {
                "id": semester.id,
                "name": semester.name,
                "ordinal": semester.ordinal,
                "session_id": semester.session_id,
            }
            if semester
            else None
        ),
        academic=context,
        enrolments=rows,
        next_step=(
            "choose_path"
            if rows and not (user.profile and user.profile.preferred_path)
            else ("enrol" if not rows else "ready")
        ),
    )


@router.post("/waitlist", response_model=MessageOut, status_code=201)
def waitlist(
    payload: WaitlistIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageOut:
    onboarding.join_waitlist(
        db,
        user,
        university_name=payload.university_name,
        email=payload.email,
        note=payload.note,
    )
    db.commit()
    return MessageOut(
        message="You are on the list. We will let you know when your university is covered."
    )
