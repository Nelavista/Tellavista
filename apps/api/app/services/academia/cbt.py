"""CBT: practice, instant feedback and topic insights (PRD §8).

CBT is a practice tool, not verification. An answer is stored on
`QuestionAttempt`, which no verification rule reads. What the results *do* feed is
the dashboard: strengths, weaknesses and what to practise next.

Answers are idempotent by `client_key`, so an offline answer can be synced twice
without inventing a second attempt or skewing the accuracy numbers.
"""
from __future__ import annotations

import random

from sqlalchemy import Integer, func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.academia import (
    Course,
    Question,
    QuestionAttempt,
    Topic,
)
from app.models.identity import User
from app.services.academia.materials import enrolled_course_ids

STRENGTH_THRESHOLD = 75
WEAKNESS_THRESHOLD = 50


def _assert_enrolled(db: Session, user: User, course_id: int) -> None:
    if course_id not in enrolled_course_ids(db, user):
        raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")


def start_quiz(
    db: Session,
    user: User,
    *,
    course_id: int,
    topic_id: int | None = None,
    count: int = 10,
) -> dict:
    _assert_enrolled(db, user, course_id)
    count = max(1, min(count, 50))
    stmt = select(Question).where(Question.course_id == course_id, Question.is_active.is_(True))
    if topic_id is not None:
        stmt = stmt.where(Question.topic_id == topic_id)
    questions = list(db.scalars(stmt).all())
    if not questions:
        raise ApiError(409, "no_questions", "There are no practice questions for this course yet.")

    selected = random.SystemRandom().sample(questions, min(count, len(questions)))
    course = db.get(Course, course_id)
    return {
        "course": {"id": course_id, "code": course.code if course else None},
        "count": len(selected),
        "questions": [
            {
                "id": question.id,
                "topic_id": question.topic_id,
                "prompt": question.prompt,
                "options": question.options,
                "difficulty": question.difficulty,
            }
            for question in selected
        ],
    }


def save_answer(
    db: Session,
    user: User,
    *,
    question_id: int,
    selected_key: str,
    client_key: str | None = None,
    duration_ms: int | None = None,
) -> dict:
    question = db.get(Question, question_id)
    if question is None or not question.is_active:
        raise ApiError(404, "question_not_found", "That question is not available.")
    _assert_enrolled(db, user, question.course_id)

    if client_key:
        existing = db.scalar(
            select(QuestionAttempt).where(QuestionAttempt.client_key == client_key)
        )
        if existing is not None:
            if existing.user_id != user.id:
                raise ApiError(409, "idempotency.key_reused", "This key belongs to another request.")
            return _answer_payload(existing, question)

    option_keys = {
        str(option.get("key"))
        for option in (question.options or [])
        if isinstance(option, dict)
    }
    if selected_key not in option_keys:
        raise ApiError(400, "invalid_option", "That option is not on this question.")

    attempt = QuestionAttempt(
        user_id=user.id,
        question_id=question.id,
        selected_key=selected_key,
        is_correct=selected_key == question.correct_key,
        duration_ms=duration_ms,
        client_key=client_key,
    )
    db.add(attempt)
    db.flush()
    return _answer_payload(attempt, question)


def _answer_payload(attempt: QuestionAttempt, question: Question) -> dict:
    return {
        "attempt_id": attempt.id,
        "question_id": question.id,
        "is_correct": attempt.is_correct,
        "correct_key": question.correct_key,
        "explanation": question.explanation,
    }


def topic_stats(db: Session, user: User, course_id: int | None = None) -> list[dict]:
    stmt = (
        select(
            Question.topic_id,
            Topic.title,
            func.count(QuestionAttempt.id),
            func.sum(func.cast(QuestionAttempt.is_correct, Integer)),
        )
        .join(Question, Question.id == QuestionAttempt.question_id)
        .outerjoin(Topic, Topic.id == Question.topic_id)
        .where(QuestionAttempt.user_id == user.id)
        .group_by(Question.topic_id, Topic.title)
    )
    if course_id is not None:
        stmt = stmt.where(Question.course_id == course_id)

    stats = []
    for topic_id, title, attempts, correct in db.execute(stmt).all():
        correct = int(correct or 0)
        attempts = int(attempts or 1)
        accuracy = round(100 * correct / attempts)
        stats.append(
            {
                "topic_id": topic_id,
                "topic": title or "General",
                "attempts": attempts,
                "correct": correct,
                "accuracy": accuracy,
                "strength": accuracy >= STRENGTH_THRESHOLD,
                "weakness": accuracy < WEAKNESS_THRESHOLD,
            }
        )
    stats.sort(key=lambda item: (item["accuracy"], -item["attempts"]))
    return stats


def results(db: Session, user: User, *, course_id: int) -> dict:
    _assert_enrolled(db, user, course_id)
    stats = topic_stats(db, user, course_id)
    strengths = [item for item in stats if item["strength"]]
    weaknesses = [item for item in stats if item["weakness"]]
    recent = db.execute(
        select(QuestionAttempt, Question)
        .join(Question, Question.id == QuestionAttempt.question_id)
        .where(
            QuestionAttempt.user_id == user.id,
            Question.course_id == course_id,
        )
        .order_by(QuestionAttempt.id.desc())
        .limit(10)
    ).all()
    return {
        "course_id": course_id,
        "topics": stats,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": [
            {
                "topic_id": item["topic_id"],
                "topic": item["topic"],
                "accuracy": item["accuracy"],
                "action": "practise",
            }
            for item in (weaknesses or stats)[:3]
        ],
        "recent": [
            {
                "attempt_id": attempt.id,
                "question_id": question.id,
                "is_correct": attempt.is_correct,
                "answered_at": attempt.answered_at,
            }
            for attempt, question in recent
        ],
    }


def practice_next(db: Session, user: User, *, course_id: int, limit: int = 5) -> dict:
    _assert_enrolled(db, user, course_id)
    stats = topic_stats(db, user, course_id)
    weak_ids = [item["topic_id"] for item in stats if item["weakness"] and item["topic_id"]]
    stmt = select(Question).where(Question.course_id == course_id, Question.is_active.is_(True))
    if weak_ids:
        stmt = stmt.where(Question.topic_id.in_(weak_ids))
    questions = list(db.scalars(stmt).all())
    if not questions:
        questions = list(
            db.scalars(
                select(Question).where(
                    Question.course_id == course_id, Question.is_active.is_(True)
                )
            ).all()
        )
    selected = random.SystemRandom().sample(questions, min(limit, len(questions)))
    return {
        "course_id": course_id,
        "focus_topics": weak_ids,
        "questions": [
            {
                "id": question.id,
                "topic_id": question.topic_id,
                "prompt": question.prompt,
                "options": question.options,
            }
            for question in selected
        ],
    }
