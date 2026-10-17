"""Phase 0 PR 0.2a — academic calendar, enrolment, course breakdown and CBT bank.

Model-level rules only: uniqueness, cascade/set-null behaviour and the shapes the
M1 onboarding wizard and M8 question import will write into. They run on the
shared `db` fixture (in-memory SQLite with foreign keys enabled).
"""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.academia import (
    AcademicSession,
    Course,
    Department,
    Enrolment,
    Faculty,
    Material,
    MaterialChunk,
    Question,
    QuestionAttempt,
    Semester,
    Topic,
    University,
)
from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import User

EXPECTED_TABLES = {
    "academic_sessions",
    "semesters",
    "enrolments",
    "topics",
    "material_chunks",
    "questions",
    "question_attempts",
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


def _course(db: Session) -> Course:
    uni = University(name=f"Uni {uuid.uuid4().hex[:6]}", slug=f"uni-{uuid.uuid4().hex[:6]}")
    db.add(uni)
    db.flush()
    faculty = Faculty(university_id=uni.id, name="Science")
    db.add(faculty)
    db.flush()
    dept = Department(faculty_id=faculty.id, name="Computer Science")
    db.add(dept)
    db.flush()
    course = Course(
        department_id=dept.id,
        code=f"CSC{uuid.uuid4().int % 900 + 100}",
        title="Data Structures",
        level="200",
    )
    db.add(course)
    db.flush()
    return course


def _session(db: Session) -> AcademicSession:
    session = AcademicSession(name=f"20{uuid.uuid4().int % 90 + 10}/20{uuid.uuid4().int % 90 + 11}")
    db.add(session)
    db.flush()
    return session


def test_tables_exist_and_options_are_jsonb_on_postgres(db: Session) -> None:
    assert EXPECTED_TABLES <= set(inspect(db.get_bind()).get_table_names())
    column = Question.__table__.c.options
    assert isinstance(column.type.dialect_impl(postgresql.dialect()), JSONB)
    assert not column.nullable


def test_expand_only_leaves_the_skeleton_columns_alone(db: Session) -> None:
    """M1 backfills these from `enrolments`; until then they must still exist."""
    columns = {c["name"] for c in inspect(db.get_bind()).get_columns("users")}
    assert {"university", "department", "level"} <= columns


def test_session_names_are_unique(db: Session) -> None:
    session = _session(db)
    db.add(AcademicSession(name=session.name))
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_semester_ordinal_is_unique_within_a_session_only(db: Session) -> None:
    first, second = _session(db), _session(db)
    db.add(Semester(session_id=first.id, name="First", ordinal=1))
    db.flush()
    # Same ordinal in another session is fine.
    db.add(Semester(session_id=second.id, name="First", ordinal=1))
    db.flush()
    db.add(Semester(session_id=first.id, name="Second", ordinal=1))
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_enrolment_is_unique_per_student_course_and_session(db: Session) -> None:
    user, course, session = _user(db), _course(db), _session(db)
    db.add(Enrolment(user_id=user.id, course_id=course.id, session_id=session.id))
    db.flush()
    db.add(Enrolment(user_id=user.id, course_id=course.id, session_id=session.id))
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_enrolment_survives_a_deleted_semester_but_not_a_deleted_course(db: Session) -> None:
    user, course, session = _user(db), _course(db), _session(db)
    semester = Semester(session_id=session.id, name="First", ordinal=1)
    db.add(semester)
    db.flush()
    enrolment = Enrolment(
        user_id=user.id, course_id=course.id, session_id=session.id, semester_id=semester.id
    )
    db.add(enrolment)
    db.flush()

    db.delete(semester)
    db.flush()
    db.expire_all()
    assert db.scalar(select(Enrolment.semester_id)) is None

    db.delete(course)
    db.flush()
    assert db.scalars(select(Enrolment)).all() == []


def test_topic_ordinal_is_unique_within_a_course(db: Session) -> None:
    course = _course(db)
    db.add(Topic(course_id=course.id, title="Arrays", ordinal=1))
    db.flush()
    db.add(Topic(course_id=course.id, title="Lists", ordinal=1))
    with pytest.raises(IntegrityError):
        db.flush()


def test_topics_keep_their_teaching_order(db: Session) -> None:
    course = _course(db)
    db.add_all(
        [
            Topic(course_id=course.id, title="Arrays", ordinal=1),
            Topic(course_id=course.id, title="Lists", ordinal=2),
        ]
    )
    db.flush()
    titles = db.scalars(select(Topic.title).order_by(Topic.ordinal)).all()
    assert titles == ["Arrays", "Lists"]


def test_topics_and_chunks_cascade_from_their_parent(db: Session) -> None:
    course = _course(db)
    topic = Topic(course_id=course.id, title="Arrays", ordinal=1)
    material = Material(course_id=course.id, title="Week 1 notes")
    db.add_all([topic, material])
    db.flush()
    db.add(MaterialChunk(material_id=material.id, ordinal=1, content="An array is..."))
    db.flush()

    db.delete(topic)
    db.flush()
    assert db.scalars(select(Topic)).all() == []

    db.delete(material)
    db.flush()
    assert db.scalars(select(MaterialChunk)).all() == []


def test_question_keeps_its_answer_key_and_options(db: Session) -> None:
    course = _course(db)
    question = Question(
        course_id=course.id,
        prompt="What is the time complexity of binary search?",
        options=[{"key": "A", "text": "O(n)"}, {"key": "B", "text": "O(log n)"}],
        correct_key="B",
    )
    db.add(question)
    db.flush()

    stored = db.scalars(select(Question)).one()
    assert stored.correct_key == "B"
    assert [o["key"] for o in stored.options] == ["A", "B"]
    # Defaults are real defaults, so an imported bank needs no boilerplate.
    assert stored.difficulty == "medium" and stored.is_active is True


def test_question_attempt_is_a_record_not_a_verification(db: Session) -> None:
    user, course = _user(db), _course(db)
    question = Question(
        course_id=course.id,
        prompt="Pick one",
        options=[{"key": "A", "text": "yes"}, {"key": "B", "text": "no"}],
        correct_key="A",
    )
    db.add(question)
    db.flush()
    db.add(QuestionAttempt(user_id=user.id, question_id=question.id, selected_key="B", is_correct=False))
    db.flush()
    attempt = db.scalars(select(QuestionAttempt)).one()
    assert attempt.is_correct is False and attempt.answered_at is not None

    db.delete(user)
    db.flush()
    assert db.scalars(select(QuestionAttempt)).all() == []
