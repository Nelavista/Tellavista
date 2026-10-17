"""Academia endpoints: dashboard, materials, Ask Nelavista and CBT (Phase 8).

The five dashboard questions are answered by `dashboard.dashboard`; it returns a
plain-language answer next to every section, so an empty state is still a real
answer rather than a spinner. Nothing here reads another student's rows: every
service call is scoped by the authenticated user, and an unenrolled course is a
403 rather than an empty list.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.core import flags
from app.db.session import get_db
from app.models.identity import User
from app.services.academia import ask as ask_service
from app.services.academia import cbt, dashboard, materials

router = APIRouter(
    prefix="/academia",
    tags=["academia"],
    dependencies=[Depends(require_flag(flags.ACADEMIA_CONNECT))],
)


class AskIn(BaseModel):
    question: str = Field(min_length=5, max_length=1000)
    session_id: int | None = None
    course_id: int | None = None


class QuizIn(BaseModel):
    course_id: int
    topic_id: int | None = None
    count: int = Field(default=10, ge=1, le=50)


class AnswerIn(BaseModel):
    question_id: int
    selected_key: str = Field(min_length=1, max_length=8)
    client_key: str | None = Field(default=None, max_length=64)
    duration_ms: int | None = Field(default=None, ge=0)


@router.get("/dashboard")
def get_dashboard(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """The existing dashboard, answering its five questions and nothing else."""
    return dashboard.dashboard(db, user)


@router.get("/materials")
def list_materials(
    course_id: int | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Notes, textbooks and past questions for the student's own courses."""
    return {"materials": materials.my_materials(db, user, course_id=course_id)}


@router.get("/materials/search")
def search_materials(
    q: str = Query(min_length=2, max_length=120),
    limit: int = Query(default=20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return {"query": q, "results": materials.search_materials(db, user, q, limit=limit)}


@router.get("/materials/{material_id}")
def material_detail(
    material_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return materials.material_detail(db, user, material_id)


@router.post("/ask")
def ask(
    payload: AskIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Course-aware and material-aware. Declines honestly when nothing matches."""
    result = ask_service.ask(
        db,
        user,
        question=payload.question,
        session_id=payload.session_id,
        course_id=payload.course_id,
    )
    db.commit()
    return result


@router.get("/ask/sessions")
def ask_sessions(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"sessions": ask_service.list_sessions(db, user)}


@router.get("/ask/sessions/{session_id}")
def ask_session(
    session_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return ask_service.session_messages(db, user, session_id)


@router.post("/cbt/quiz", status_code=201)
def start_quiz(
    payload: QuizIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    quiz = cbt.start_quiz(
        db, user, course_id=payload.course_id, topic_id=payload.topic_id, count=payload.count
    )
    db.commit()
    return quiz


@router.post("/cbt/answer")
def save_answer(
    payload: AnswerIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Save one answer immediately: a dropped connection never loses it."""
    result = cbt.save_answer(
        db,
        user,
        question_id=payload.question_id,
        selected_key=payload.selected_key,
        client_key=payload.client_key,
        duration_ms=payload.duration_ms,
    )
    db.commit()
    return result


@router.get("/cbt/results")
def cbt_results(
    course_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return cbt.results(db, user, course_id=course_id)


@router.get("/cbt/practice-next")
def practice_next(
    course_id: int,
    limit: int = Query(default=5, ge=1, le=20),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return cbt.practice_next(db, user, course_id=course_id, limit=limit)


__all__ = ["router"]
