"""Onboarding and academic context (PRD §3, Phase 1).

The wizard writes real `enrolments`, not free-string profile fields. Everything
downstream — Study Materials, CBT, Ask Nelavista, and the university requirement in
matching — reads those rows, so "my courses" means the same thing everywhere.

Enrolment is upsert-shaped and therefore safe to retry from a flaky connection:
the unique key is (user, course, session), and enrolling twice changes nothing.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.academia import (
    AcademicSession,
    Course,
    Department,
    Enrolment,
    Faculty,
    Semester,
    University,
)
from app.models.identity import User
from app.models.ops import UniversityWaitlist


def list_universities(db: Session, *, include_inactive: bool = False) -> list[University]:
    stmt = select(University).order_by(University.name)
    if not include_inactive:
        stmt = stmt.where(University.active.is_(True))
    return list(db.scalars(stmt).all())


def list_faculties(db: Session, university_id: int) -> list[Faculty]:
    return list(
        db.scalars(
            select(Faculty).where(Faculty.university_id == university_id).order_by(Faculty.name)
        ).all()
    )


def list_departments(db: Session, faculty_id: int) -> list[Department]:
    return list(
        db.scalars(
            select(Department)
            .where(Department.faculty_id == faculty_id)
            .order_by(Department.name)
        ).all()
    )


def list_courses(db: Session, department_id: int, *, level: str | None = None) -> list[Course]:
    stmt = select(Course).where(Course.department_id == department_id)
    if level:
        stmt = stmt.where(Course.level == level)
    return list(db.scalars(stmt.order_by(Course.level, Course.code)).all())


def current_session(db: Session) -> Semester | None:
    """The semester the wizard preselects. Exactly one session is current."""
    session = db.scalar(select(AcademicSession).where(AcademicSession.is_current.is_(True)))
    if session is None:
        return None
    return db.scalar(
        select(Semester)
        .where(Semester.session_id == session.id)
        .order_by(Semester.ordinal)
        .limit(1)
    )


def list_semesters(db: Session, session_id: int) -> list[Semester]:
    return list(
        db.scalars(
            select(Semester).where(Semester.session_id == session_id).order_by(Semester.ordinal)
        ).all()
    )


def enrol(
    db: Session,
    user: User,
    *,
    course_ids: list[int],
    session_id: int,
    semester_id: int | None = None,
) -> list[Enrolment]:
    """Register the student for courses in one session. Idempotent per course.

    A course from another student's department is not rejected outright: students
    take electives. It must still exist, and the semester must belong to the
    session, which is the part a client can get wrong.
    """
    if not course_ids:
        raise ApiError(400, "no_courses", "Choose at least one course.")
    if len(set(course_ids)) != len(course_ids):
        raise ApiError(400, "duplicate_course", "A course is listed twice.")

    session = db.get(AcademicSession, session_id)
    if session is None:
        raise ApiError(404, "session_not_found", "That academic session does not exist.")
    if semester_id is not None:
        semester = db.get(Semester, semester_id)
        if semester is None or semester.session_id != session_id:
            raise ApiError(400, "invalid_semester", "That semester is not in this session.")

    courses = db.scalars(select(Course).where(Course.id.in_(course_ids))).all()
    found = {course.id for course in courses}
    missing = [str(cid) for cid in course_ids if cid not in found]
    if missing:
        raise ApiError(
            404, "course_not_found", "One of the selected courses does not exist.",
            {"course_ids": missing},
        )

    existing = {
        row.course_id: row
        for row in db.scalars(
            select(Enrolment).where(
                Enrolment.user_id == user.id,
                Enrolment.session_id == session_id,
                Enrolment.course_id.in_(course_ids),
            )
        ).all()
    }

    rows: list[Enrolment] = []
    for course_id in course_ids:
        row = existing.get(course_id)
        if row is None:
            row = Enrolment(
                user_id=user.id,
                course_id=course_id,
                session_id=session_id,
                semester_id=semester_id,
                status="active",
            )
            db.add(row)
        elif row.status != "active":
            row.status = "active"
        rows.append(row)
    db.flush()
    return rows


def my_enrolments(db: Session, user: User) -> list[dict]:
    rows = db.execute(
        select(Enrolment, Course, Department, Faculty, University)
        .join(Course, Course.id == Enrolment.course_id)
        .join(Department, Department.id == Course.department_id)
        .join(Faculty, Faculty.id == Department.faculty_id)
        .join(University, University.id == Faculty.university_id)
        .where(Enrolment.user_id == user.id)
        .order_by(Course.level, Course.code)
    ).all()
    return [
        {
            "enrolment_id": enrolment.id,
            "course_id": course.id,
            "code": course.code,
            "title": course.title,
            "level": course.level,
            "session_id": enrolment.session_id,
            "semester_id": enrolment.semester_id,
            "status": enrolment.status,
            "department": department.name,
            "faculty": faculty.name,
            "university": university.name,
        }
        for enrolment, course, department, faculty, university in rows
    ]


def academic_context(db: Session, user: User) -> dict:
    """The student's current university/department/level, derived from enrolments.

    Falls back to the skeleton free-string columns for imported V1 accounts that
    have not been through the wizard yet.
    """
    context = my_enrolments(db, user)
    if context:
        first = context[0]
        levels = sorted({row["level"] for row in context if row["level"]})
        return {
            "university": first["university"],
            "department": first["department"],
            "level": levels[-1] if levels else None,
            "course_ids": [row["course_id"] for row in context],
            "source": "enrolment",
        }
    return {
        "university": user.university,
        "department": user.department,
        "level": user.level,
        "course_ids": [],
        "source": "profile" if (user.university or user.department) else "none",
    }


def join_waitlist(
    db: Session,
    user: User | None,
    *,
    university_name: str,
    email: str | None = None,
    note: str | None = None,
) -> UniversityWaitlist:
    name = university_name.strip()
    if not name:
        raise ApiError(400, "invalid_university", "Enter your university name.")
    row = db.scalar(
        select(UniversityWaitlist).where(
            UniversityWaitlist.user_id == (user.id if user else None),
            UniversityWaitlist.university_name == name,
        )
    )
    if row is not None:
        return row
    row = UniversityWaitlist(
        user_id=user.id if user else None,
        university_name=name[:200],
        email=(email or (user.email if user else None)),
        note=(note or "")[:500] or None,
    )
    db.add(row)
    db.flush()
    return row
