"""Phase 8 — Academia answers five questions, and only its own five.

The dashboard's five questions must have a real answer even when the data is
empty. Study materials and CBT are enrolled-course scoped (another course is a
403, not an empty list), Ask Nelavista declines honestly when it has no grounding,
and a CBT answer saved twice with one client key is stored once.
"""
from __future__ import annotations

import pytest
from factories import make_user, unique
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.academia import (
    AcademicSession,
    Course,
    Department,
    Enrolment,
    Faculty,
    Material,
    MaterialChunk,
    Question,
    Topic,
    University,
)
from app.services.academia import ask, cbt, dashboard, materials


def _course(db: Session, *, code: str = "CSC213"):
    university = University(name=unique("University"), slug=unique("university"))
    db.add(university)
    db.flush()
    faculty = Faculty(university_id=university.id, name="Science")
    db.add(faculty)
    db.flush()
    department = Department(faculty_id=faculty.id, name="Computer Science")
    db.add(department)
    db.flush()
    course = Course(
        department_id=department.id,
        code=code,
        title="Data Structures",
        level="200",
    )
    db.add(course)
    db.flush()
    return university, department, course


def _enrol(db: Session, user, course: Course):
    session = db.scalar(select(AcademicSession).where(AcademicSession.is_current.is_(True)))
    if session is None:
        session = AcademicSession(name=unique("2026"), is_current=True)
        db.add(session)
        db.flush()
    enrolment = Enrolment(
        user_id=user.id, course_id=course.id, session_id=session.id, status="active"
    )
    db.add(enrolment)
    db.flush()
    return enrolment


def test_dashboard_answers_all_five_questions_even_with_no_data(db: Session) -> None:
    student = make_user(db)

    payload = dashboard.dashboard(db, student)

    questions = payload["questions"]
    assert set(questions) == {
        "what_am_i_studying",
        "what_did_i_study_recently",
        "what_should_i_practise",
        "where_am_i_weak",
        "what_should_i_do_next",
    }
    for answer in questions.values():
        assert answer["answer"]  # never an empty string
    assert "onboarding" in questions["what_am_i_studying"]["answer"].lower()
    assert payload["enrolment_count"] == 0


def test_dashboard_uses_the_students_own_courses(db: Session) -> None:
    student = make_user(db)
    _university, _department, course = _course(db)
    _enrol(db, student, course)

    payload = dashboard.dashboard(db, student)

    assert payload["enrolment_count"] == 1
    assert course.code in payload["questions"]["what_am_i_studying"]["answer"]


def test_materials_are_scoped_to_enrolled_courses(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)
    material = Material(course_id=course.id, title="Binary trees notes", file_url="https://x.test/a.pdf")
    db.add(material)
    db.flush()

    listed = materials.my_materials(db, student)
    assert [row["id"] for row in listed] == [material.id]
    assert listed[0]["course"]["code"] == course.code

    # A course the student is not enrolled in is refused, not silently empty.
    _u2, _d2, other_course = _course(db, code="CSC315")
    with pytest.raises(ApiError) as excinfo:
        materials.my_materials(db, student, course_id=other_course.id)
    assert excinfo.value.code == "not_enrolled"


def test_material_search_finds_the_chunk_text(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)
    material = Material(course_id=course.id, title="Algorithms handout")
    db.add(material)
    db.flush()
    db.add(
        MaterialChunk(
            material_id=material.id,
            ordinal=0,
            content="A binary search tree keeps keys ordered so lookup is logarithmic.",
        )
    )
    db.flush()

    results = materials.search_materials(db, student, "binary search")
    assert results and results[0]["material_id"] == material.id
    assert "binary" in results[0]["snippet"].lower()
    assert materials.material_detail(db, student, material.id)["chunks"][0]["ordinal"] == 0


def test_ask_declines_honestly_without_grounding(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)

    result = ask.ask(db, student, question="What is the time complexity of quicksort?", course_id=course.id)

    assert result["declined"] is True
    assert result["citations"] == []
    assert "course materials" in result["answer"].lower()
    assert result["provider"] is None


def test_ask_answers_from_the_students_own_material(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)
    material = Material(course_id=course.id, title="Trees")
    db.add(material)
    db.flush()
    db.add(
        MaterialChunk(
            material_id=material.id,
            ordinal=0,
            content="A binary search tree keeps keys ordered so lookup is logarithmic.",
        )
    )
    db.flush()

    result = ask.ask(
        db, student, question="How does a binary search tree keep lookup fast?", course_id=course.id
    )

    assert result["declined"] is False
    assert result["citations"][0]["material_id"] == material.id
    assert result["citations"][0]["course_code"] == course.code
    assert result["answer"]


def test_ask_refuses_a_course_the_student_does_not_take(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)

    with pytest.raises(ApiError) as excinfo:
        ask.ask(db, student, question="Explain pointers please", course_id=course.id)
    assert excinfo.value.code == "not_enrolled"


def test_a_short_question_is_rejected(db: Session) -> None:
    student = make_user(db)
    with pytest.raises(ApiError) as excinfo:
        ask.ask(db, student, question="why")
    assert excinfo.value.code == "question_too_short"


def _question(db: Session, course: Course, topic: Topic | None, key: str = "A") -> Question:
    question = Question(
        course_id=course.id,
        topic_id=topic.id if topic else None,
        prompt="What is the worst-case lookup in a balanced BST?",
        options=[{"key": "A", "text": "O(log n)"}, {"key": "B", "text": "O(n)"}],
        correct_key=key,
        explanation="A balanced tree halves the search space each step.",
    )
    db.add(question)
    db.flush()
    return question


def test_cbt_scores_strengths_and_weaknesses_by_topic(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)
    strong = Topic(course_id=course.id, title="Trees", ordinal=1)
    weak = Topic(course_id=course.id, title="Graphs", ordinal=2)
    db.add_all([strong, weak])
    db.flush()
    strong_q = _question(db, course, strong, key="A")
    weak_q = _question(db, course, weak, key="A")

    cbt.save_answer(db, student, question_id=strong_q.id, selected_key="A")
    cbt.save_answer(db, student, question_id=weak_q.id, selected_key="B")

    results = cbt.results(db, student, course_id=course.id)
    assert results["strengths"][0]["topic"] == "Trees"
    assert results["weaknesses"][0]["topic"] == "Graphs"
    assert results["weaknesses"][0]["accuracy"] == 0
    assert results["recommendations"][0]["topic"] == "Graphs"


def test_an_answer_saved_twice_is_stored_once(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)
    question = _question(db, course, None)

    first = cbt.save_answer(
        db, student, question_id=question.id, selected_key="A", client_key="cbt-1"
    )
    second = cbt.save_answer(
        db, student, question_id=question.id, selected_key="A", client_key="cbt-1"
    )

    assert first["attempt_id"] == second["attempt_id"]
    stats = cbt.topic_stats(db, student)
    assert len(stats) == 1 and stats[0]["attempts"] == 1


def test_an_answer_must_be_one_of_the_options(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)
    question = _question(db, course, None)

    with pytest.raises(ApiError) as excinfo:
        cbt.save_answer(db, student, question_id=question.id, selected_key="Z")
    assert excinfo.value.code == "invalid_option"


def test_a_quiz_with_no_questions_says_so(db: Session) -> None:
    student = make_user(db)
    _u, _d, course = _course(db)
    _enrol(db, student, course)

    with pytest.raises(ApiError) as excinfo:
        cbt.start_quiz(db, student, course_id=course.id)
    assert excinfo.value.code == "no_questions"
