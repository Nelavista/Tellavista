"""The dashboard answers five questions, and nothing else (PRD §8).

1. What am I studying?
2. What did I study recently?
3. What should I practise?
4. Where am I weak?
5. What should I do next?

Every answer is data-backed. "What should I do next" is one action with a real
destination, derived from weak topics, an unfinished lesson, or the student's own
material — never a generic prompt.
"""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.academia import Material, Question, QuestionAttempt, Topic
from app.models.identity import User
from app.models.skills import IN_PROGRESS, Lesson, LessonProgress
from app.services.academia.cbt import topic_stats
from app.services.academia.materials import enrolled_course_ids
from app.services.identity.onboarding import my_enrolments


def _studying(db: Session, user: User) -> tuple[list[dict], str]:
    courses = my_enrolments(db, user)
    if not courses:
        return [], "You are not enrolled in any courses yet. Finish onboarding to add yours."
    names = ", ".join(f"{row['code']} {row['title']}" for row in courses[:3])
    extra = "" if len(courses) <= 3 else f" and {len(courses) - 3} more"
    return courses, f"You are studying {names}{extra}."


def _recent(db: Session, user: User) -> tuple[list[dict], str]:
    lessons = db.execute(
        select(LessonProgress, Lesson)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .where(LessonProgress.user_id == user.id, LessonProgress.completed_at.is_not(None))
        .order_by(LessonProgress.completed_at.desc())
        .limit(3)
    ).all()
    in_progress = db.execute(
        select(LessonProgress, Lesson)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .where(LessonProgress.user_id == user.id, LessonProgress.status == IN_PROGRESS)
        .order_by(LessonProgress.updated_at.desc())
        .limit(3)
    ).all()
    items = [
        {
            "kind": "lesson_completed",
            "title": lesson.title,
            "when": progress.completed_at,
        }
        for progress, lesson in lessons
    ]
    # In-progress lessons are shown once: a lesson that was just completed is
    # already above, and repeating it would make "what did I just do" ambiguous.
    items += [
        {
            "kind": "lesson_in_progress",
            "title": lesson.title,
            "when": progress.updated_at,
        }
        for progress, lesson in in_progress
        if all(item["title"] != lesson.title for item in items)
    ]
    if not items:
        return [], "Nothing yet. Open a course material or a skills lesson to start."
    return items, f"You last worked on {items[0]['title']}."


def _topic_names(db: Session, topic_ids: list[int]) -> dict[int, str]:
    if not topic_ids:
        return {}
    return {
        row.id: row.title
        for row in db.scalars(select(Topic).where(Topic.id.in_(topic_ids))).all()
    }


def _practise(db: Session, user: User) -> tuple[list[dict], str]:
    stats = topic_stats(db, user)
    weak = [item for item in stats if item["weakness"]][:3]
    course_ids = enrolled_course_ids(db, user)

    attempted_topics = (
        select(Question.topic_id)
        .join(QuestionAttempt, QuestionAttempt.question_id == Question.id)
        .where(
            QuestionAttempt.user_id == user.id,
            Question.topic_id.is_not(None),
        )
    )
    unattempted = db.execute(
        select(Topic.id, Topic.title)
        .where(
            Topic.course_id.in_(course_ids),
            Topic.id.not_in(attempted_topics),
        )
        .order_by(Topic.course_id, Topic.ordinal)
        .limit(3)
    ).all()

    items = [
        {"topic_id": item["topic_id"], "topic": item["topic"], "accuracy": item["accuracy"]}
        for item in weak
    ]
    if not items:
        items = [
            {"topic_id": topic_id, "topic": title, "accuracy": None}
            for topic_id, title in unattempted
        ]
    if not items:
        return [], "Practise any topic from your courses to see where you stand."
    return items, f"Start with {items[0]['topic']}."


def _weak(db: Session, user: User) -> tuple[list[dict], str]:
    stats = topic_stats(db, user)
    weaknesses = [item for item in stats if item["weakness"]]
    if not weaknesses:
        return [], (
            "No weak topics yet. Take a few CBT questions and this will fill in."
            if not stats
            else "No topic is below 50% right now."
        )
    top = weaknesses[0]
    return weaknesses, f"{top['topic']} is your weakest topic at {top['accuracy']}%."


def _next_action(db: Session, user: User, weak: list[dict]) -> dict:
    if weak:
        return {
            "kind": "practise",
            "label": f"Practise {weak[0]['topic']}",
            "topic_id": weak[0]["topic_id"],
            "reason": "It is your weakest topic.",
        }

    in_progress = db.execute(
        select(LessonProgress, Lesson)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .where(LessonProgress.user_id == user.id, LessonProgress.status == IN_PROGRESS)
        .order_by(LessonProgress.updated_at.desc())
        .limit(1)
    ).first()
    if in_progress is not None:
        progress, lesson = in_progress
        return {
            "kind": "lesson",
            "label": f"Continue {lesson.title}",
            "lesson_id": lesson.id,
            "reason": "You have a lesson in progress.",
        }

    course_ids = enrolled_course_ids(db, user)
    if course_ids:
        material = db.scalar(
            select(Material)
            .where(Material.course_id.in_(course_ids))
            .order_by(Material.id)
            .limit(1)
        )
        if material is not None:
            return {
                "kind": "material",
                "label": f"Open {material.title}",
                "material_id": material.id,
                "reason": "Your course material is the best place to start.",
            }

    return {
        "kind": "onboarding",
        "label": "Add your courses",
        "reason": "The dashboard needs your courses to be useful.",
    }


def dashboard(db: Session, user: User) -> dict:
    courses, studying_answer = _studying(db, user)
    recent, recent_answer = _recent(db, user)
    practise, practise_answer = _practise(db, user)
    weak, weak_answer = _weak(db, user)
    action = _next_action(db, user, weak)

    course_ids = enrolled_course_ids(db, user)
    material_counts = (
        dict(
            db.execute(
                select(Material.course_id, func.count(Material.id))
                .where(Material.course_id.in_(course_ids))
                .group_by(Material.course_id)
            ).all()
        )
        if course_ids
        else {}
    )

    return {
        "questions": {
            "what_am_i_studying": {"answer": studying_answer, "courses": courses},
            "what_did_i_study_recently": {"answer": recent_answer, "items": recent},
            "what_should_i_practise": {"answer": practise_answer, "items": practise},
            "where_am_i_weak": {"answer": weak_answer, "items": weak},
            "what_should_i_do_next": {"answer": action.get("label"), "action": action},
        },
        "materials_by_course": material_counts,
        "enrolment_count": len(courses),
    }


__all__ = ["dashboard"]
