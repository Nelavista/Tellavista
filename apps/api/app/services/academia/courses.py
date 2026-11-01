"""Course and topic detail for the student's own enrolments.

Materials and CBT answers are already scoped per student. This module adds the
one read the course screen was missing: the course's topics, the material
attached to it, and the practice record that belongs to the signed-in student.
It never exposes the CBT answer key except through the attempt-history endpoint,
where the student is reviewing answers they already submitted.
"""

from __future__ import annotations

from sqlalchemy import Integer, func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.academia import (
    AcademicSession,
    Course,
    Department,
    Enrolment,
    Faculty,
    Question,
    QuestionAttempt,
    Semester,
    Topic,
    University,
)
from app.models.identity import User
from app.services.academia import cbt, materials


def _assert_enrolled(db: Session, user: User, course: Course) -> Enrolment:
    enrolment = db.scalar(
        select(Enrolment)
        .where(
            Enrolment.user_id == user.id,
            Enrolment.course_id == course.id,
            Enrolment.status == "active",
        )
        .order_by(Enrolment.id.desc())
    )
    if enrolment is None:
        raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")
    return enrolment


def _course_context(db: Session, course: Course) -> tuple[str, str, str]:
    department = db.get(Department, course.department_id)
    faculty = db.get(Faculty, department.faculty_id) if department else None
    university = db.get(University, faculty.university_id) if faculty else None
    return (
        department.name if department else "Not recorded",
        faculty.name if faculty else "Not recorded",
        university.name if university else "Not recorded",
    )


def _stats_for(db: Session, user: User, course_id: int) -> dict[int | None, dict]:
    return {item["topic_id"]: item for item in cbt.topic_stats(db, user, course_id)}


def _question_counts(db: Session, course_id: int) -> dict[int | None, int]:
    return dict(
        db.execute(
            select(Question.topic_id, func.count(Question.id))
            .where(Question.course_id == course_id, Question.is_active.is_(True))
            .group_by(Question.topic_id)
        ).all()
    )


def _topic_payload(topic: Topic, stats: dict[int | None, dict], counts: dict[int | None, int]) -> dict:
    stat = stats.get(topic.id) or {}
    return {
        "id": topic.id,
        "title": topic.title,
        "ordinal": topic.ordinal,
        "summary": topic.summary,
        "question_count": int(counts.get(topic.id, 0)),
        "attempts": int(stat.get("attempts", 0)),
        "correct": int(stat.get("correct", 0)),
        "accuracy": stat.get("accuracy"),
        "strength": bool(stat.get("strength", False)),
        "weakness": bool(stat.get("weakness", False)),
    }


def course_detail(db: Session, user: User, course_id: int) -> dict:
    course = db.get(Course, course_id)
    if course is None:
        raise ApiError(404, "course_not_found", "That course does not exist.")
    enrolment = _assert_enrolled(db, user, course)

    session_row = db.get(AcademicSession, enrolment.session_id)
    semester = db.get(Semester, enrolment.semester_id) if enrolment.semester_id else None
    department, faculty, university = _course_context(db, course)
    stats = _stats_for(db, user, course.id)
    counts = _question_counts(db, course.id)

    topics = db.scalars(
        select(Topic).where(Topic.course_id == course.id).order_by(Topic.ordinal, Topic.id)
    ).all()
    attempts = sum(int(item.get("attempts", 0)) for item in stats.values())
    correct = sum(int(item.get("correct", 0)) for item in stats.values())

    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "level": course.level,
        "department": department,
        "faculty": faculty,
        "university": university,
        "enrolment_id": enrolment.id,
        "session_id": enrolment.session_id,
        "session_name": session_row.name if session_row else None,
        "semester_id": enrolment.semester_id,
        "semester_name": semester.name if semester else None,
        "status": enrolment.status,
        "topics": [_topic_payload(topic, stats, counts) for topic in topics],
        "materials": materials.my_materials(db, user, course_id=course.id),
        "practice": {
            "attempts": attempts,
            "correct": correct,
            "accuracy": round(100 * correct / attempts) if attempts else 0,
        },
    }


def topic_detail(db: Session, user: User, topic_id: int) -> dict:
    topic = db.get(Topic, topic_id)
    if topic is None:
        raise ApiError(404, "topic_not_found", "That topic does not exist.")
    course = db.get(Course, topic.course_id)
    if course is None:
        raise ApiError(404, "course_not_found", "That course does not exist.")
    _assert_enrolled(db, user, course)

    stats = _stats_for(db, user, course.id)
    counts = _question_counts(db, course.id)
    payload = _topic_payload(topic, stats, counts)
    return {
        "id": topic.id,
        "title": topic.title,
        "ordinal": topic.ordinal,
        "summary": topic.summary,
        "course": {"id": course.id, "code": course.code, "title": course.title},
        "question_count": payload["question_count"],
        "attempts": payload["attempts"],
        "correct": payload["correct"],
        "accuracy": payload["accuracy"],
        "strength": payload["strength"],
        "weakness": payload["weakness"],
        "materials": materials.my_materials(db, user, course_id=course.id),
    }


def my_cbt_history(db: Session, user: User, *, course_id: int | None = None, limit: int = 100) -> dict:
    if course_id is not None and course_id not in materials.enrolled_course_ids(db, user):
        raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")

    conditions = [QuestionAttempt.user_id == user.id]
    if course_id is not None:
        conditions.append(Question.course_id == course_id)

    # Summary counts cover every recorded answer, not only the page below.
    total, correct = db.execute(
        select(
            func.count(QuestionAttempt.id),
            func.sum(func.cast(QuestionAttempt.is_correct, Integer)),
        )
        .join(Question, Question.id == QuestionAttempt.question_id)
        .where(*conditions)
    ).one()
    total = int(total or 0)
    correct = int(correct or 0)

    rows = db.execute(
        select(QuestionAttempt, Question, Course, Topic)
        .join(Question, Question.id == QuestionAttempt.question_id)
        .join(Course, Course.id == Question.course_id)
        .outerjoin(Topic, Topic.id == Question.topic_id)
        .where(*conditions)
        .order_by(QuestionAttempt.id.desc())
        .limit(limit)
    ).all()
    return {
        "items": [
            {
                "attempt_id": attempt.id,
                "course_id": course.id,
                "course_code": course.code,
                "topic_id": topic.id if topic else None,
                "topic": topic.title if topic else None,
                "question_id": question.id,
                "prompt": question.prompt,
                "selected_key": attempt.selected_key,
                "correct_key": question.correct_key,
                "is_correct": attempt.is_correct,
                "explanation": question.explanation,
                "duration_ms": attempt.duration_ms,
                "answered_at": attempt.answered_at,
            }
            for attempt, question, course, topic in rows
        ],
        "attempts": total,
        "correct": correct,
        "accuracy": round(100 * correct / total) if total else 0,
    }


__all__ = ["course_detail", "my_cbt_history", "topic_detail"]
