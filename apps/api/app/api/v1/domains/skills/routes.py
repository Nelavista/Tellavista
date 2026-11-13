"""Skills endpoints: catalog, learning, practice (Phase 2)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.api.v1.domains.skills.schemas import (
    CareerTrackListOut,
    LessonCompletedOut,
    LessonOut,
    LessonStartedOut,
    MyLearningOut,
    PathOut,
    PracticeBriefOut,
    PracticeResultOut,
    SkillDetailOut,
    SkillsOut,
)
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


@router.get("", response_model=SkillsOut)
def list_skills(
    q: str | None = Query(default=None, max_length=120),
    program: str | None = Query(default=None, max_length=40),
    category: str | None = Query(default=None, max_length=80),
    language: str | None = Query(default=None, max_length=60),
    tag: str | None = Query(default=None, max_length=60),
    level: str | None = Query(default=None, max_length=20),
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return {
        "skills": learning.list_skills(
            db,
            q=q,
            program=program,
            category=category,
            language=language,
            tag=tag,
            level=level,
        )
    }


@router.get("/career-tracks", response_model=CareerTrackListOut)
def career_tracks(
    program: str | None = Query(default=None, max_length=40),
    q: str | None = Query(default=None, max_length=120),
    language: str | None = Query(default=None, max_length=60),
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return {
        "tracks": learning.list_career_tracks(db, program=program, q=q, language=language)
    }


@router.get("/my-learning", response_model=MyLearningOut)
def my_learning(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return {"paths": learning.my_learning(db, user)}


@router.get("/paths/{path_slug}", response_model=PathOut)
def path_detail(
    path_slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    path = learning.get_path(db, path_slug)
    return learning.path_with_progress(db, user, path)


@router.get("/lessons/{lesson_slug}", response_model=LessonOut)
def lesson(
    lesson_slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return learning.lesson_detail(db, user, lesson_slug)


@router.post("/lessons/{lesson_id}/start", response_model=LessonStartedOut)
def start_lesson(
    lesson_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = learning.start_lesson(db, user, lesson_id)
    db.commit()
    return {"lesson_id": row.lesson_id, "status": row.status}


@router.post("/lessons/{lesson_id}/complete", response_model=LessonCompletedOut)
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


@router.get("/tasks/{template_id}", response_model=PracticeBriefOut)
def practice_brief(
    template_id: int,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return tasks.practice_brief(db, template_id)


@router.post("/tasks/{template_id}/practice", response_model=PracticeResultOut)
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


@router.get("/{skill_slug}", response_model=SkillDetailOut)
def skill_detail(
    skill_slug: str,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return learning.get_skill(db, skill_slug)
