"""Ask Nelavista: course-aware, material-grounded, honest (PRD §8).

The assistant is not a general chatbot. It retrieves only from the student's own
enrolled courses, and when the material does not support an answer it says so
instead of guessing. That rule lives here, before any provider is called, so it
cannot be softened by changing models.

Every answer stores the chunks it was built from; the student can see the source
material, and a support question ("where did this come from?") has an answer.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.academia import AskMessage, AskSession, Course
from app.models.identity import User
from app.services.academia.materials import enrolled_course_ids, retrieve
from app.services.ai.provider import ExtractiveProvider, ProviderError, get_provider

# Below this lexical relevance the honest answer is "I could not find it".
MIN_SCORE = 0.2

DECLINE_MESSAGE = (
    "I could not find this in your course materials, so I will not guess. "
    "Try asking about a topic from one of your enrolled courses, or open the material directly."
)


def _session(db: Session, user: User, session_id: int | None, course_id: int | None) -> AskSession:
    if session_id is not None:
        row = db.get(AskSession, session_id)
        if row is None or row.user_id != user.id:
            raise ApiError(404, "session_not_found", "That conversation does not exist.")
        return row

    if course_id is not None and course_id not in enrolled_course_ids(db, user):
        raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")
    row = AskSession(user_id=user.id, course_id=course_id)
    db.add(row)
    db.flush()
    return row


def ask(
    db: Session,
    user: User,
    *,
    question: str,
    session_id: int | None = None,
    course_id: int | None = None,
) -> dict:
    cleaned = " ".join(question.split())
    if len(cleaned) < 5:
        raise ApiError(400, "question_too_short", "Ask a little more than that.")
    if len(cleaned) > 1000:
        raise ApiError(400, "question_too_long", "Keep the question under 1000 characters.")

    session = _session(db, user, session_id, course_id)
    effective_course = course_id if course_id is not None else session.course_id

    db.add(AskMessage(session_id=session.id, role="user", content=cleaned))
    db.flush()

    chunks = retrieve(db, user, cleaned, course_id=effective_course, limit=4)
    best = chunks[0][1] if chunks else 0.0
    if not chunks or best < MIN_SCORE:
        message = AskMessage(
            session_id=session.id,
            role="assistant",
            content=DECLINE_MESSAGE,
            citations=[],
            declined=True,
        )
        db.add(message)
        db.flush()
        return {
            "session_id": session.id,
            "answer": DECLINE_MESSAGE,
            "declined": True,
            "citations": [],
            "provider": None,
        }

    context = [chunk for chunk, _score in chunks]
    provider = get_provider()
    provider_name = provider.name
    try:
        answer = provider.answer(cleaned, context)
    except ProviderError:
        # A provider outage must not turn into a hallucination or a 500. The
        # extractive fallback still answers from the same grounded chunks.
        provider_name = "extractive-fallback"
        answer = ExtractiveProvider().answer(cleaned, context)

    citations = [
        {
            "chunk_id": chunk.chunk_id,
            "material_id": chunk.material_id,
            "material_title": chunk.material_title,
            "course_code": chunk.course_code,
            "score": next(score for candidate, score in chunks if candidate.chunk_id == chunk.chunk_id),
        }
        for chunk in context
    ]
    message = AskMessage(
        session_id=session.id,
        role="assistant",
        content=answer,
        citations=citations,
        declined=False,
    )
    db.add(message)
    if session.title is None or effective_course is not None:
        course = db.get(Course, effective_course) if effective_course else None
        session.title = (f"{course.code}: {cleaned[:80]}" if course else cleaned[:120])
    db.flush()
    return {
        "session_id": session.id,
        "answer": answer,
        "declined": False,
        "citations": citations,
        "provider": provider_name,
        "best_score": best,
    }


def list_sessions(db: Session, user: User) -> list[dict]:
    rows = db.scalars(
        select(AskSession)
        .where(AskSession.user_id == user.id)
        .order_by(AskSession.id.desc())
        .limit(100)
    ).all()
    courses = {
        course.id: course
        for course in db.scalars(
            select(Course).where(Course.id.in_([row.course_id for row in rows if row.course_id]))
        ).all()
    }
    return [
        {
            "id": row.id,
            "title": row.title,
            "course": (
                {"id": row.course_id, "code": courses[row.course_id].code}
                if row.course_id in courses
                else None
            ),
            "created_at": row.created_at,
        }
        for row in rows
    ]


def session_messages(db: Session, user: User, session_id: int) -> dict:
    session = db.get(AskSession, session_id)
    if session is None or session.user_id != user.id:
        raise ApiError(404, "session_not_found", "That conversation does not exist.")
    messages = db.scalars(
        select(AskMessage)
        .where(AskMessage.session_id == session.id)
        .order_by(AskMessage.id)
    ).all()
    return {
        "id": session.id,
        "title": session.title,
        "course_id": session.course_id,
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "citations": message.citations or [],
                "declined": message.declined,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }
