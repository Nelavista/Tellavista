"""Skills endpoints: catalog, learning, practice (Phase 2)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.core import flags, observability
from app.db.session import get_db
from app.models.identity import User
from app.services.skills import learning, tasks

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    dependencies=[Depends(require_flag(flags.SKILLS_JOURNEY))],
)


class PracticeIn(BaseModel):
    answer: dict = Field(default_factory=dict)
    duration_ms: int | None = Field(default=None, ge=0)


@router.get("")
def list_skills(
    _user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"skills": learning.list_skills(db)}


@router.get("/my-learning")
def my_learning(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"paths": learning.my_learning(db, user)}


@router.get("/paths/{path_slug}")
def path_detail(
    path_slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    path = learning.get_path(db, path_slug)
    return learning.path_with_progress(db, user, path)


@router.get("/lessons/{lesson_slug}")
def lesson(
    lesson_slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return learning.lesson_detail(db, user, lesson_slug)


@router.post("/lessons/{lesson_id}/start")
def start_lesson(
    lesson_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = learning.start_lesson(db, user, lesson_id)
    db.commit()
    return {"lesson_id": row.lesson_id, "status": row.status}


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = learning.complete_lesson(db, user, lesson_id)
    db.commit()
    observability.capture(
        user.id, observability.EVENTS["lesson_completed"], {"lesson_id": lesson_id}
    )
    return {
        "lesson_id": row.lesson_id,
        "status": row.status,
        "completed_at": row.completed_at,
        "verified": False,
        "note": "Completing a lesson is progress, not verification.",
    }


@router.get("/tasks/{template_id}")
def practice_brief(
    template_id: int,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return tasks.practice_brief(db, template_id)


@router.post("/tasks/{template_id}/practice")
def practice(
    template_id: int,
    payload: PracticeIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    attempt, result = tasks.submit_practice(
        db,
        user,
        template_id=template_id,
        answer=payload.answer,
        duration_ms=payload.duration_ms,
    )
    db.commit()
    return {
        "attempt_id": attempt.id,
        "is_correct": result.is_correct,
        "score": result.score,
        "feedback": result.feedback,
        "details": result.details,
        "counts_as_verification": False,
    }


@router.get("/{skill_slug}")
def skill_detail(
    skill_slug: str,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return learning.get_skill(db, skill_slug)
