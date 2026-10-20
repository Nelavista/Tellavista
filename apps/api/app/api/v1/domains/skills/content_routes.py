"""Ops content management: paths, lessons and task templates (Phase 2 ops slice).

Content is configuration. These routes are how ops writes it — and they are the
reason skill number two does not need a deploy. A draft is invisible to students
(every student service filters on `status == published`), so content can be staged
safely and published when it is ready.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_flag
from app.api.v1.domains.skills.schemas import (
    ContentLessonListOut,
    ContentPathListOut,
    ContentTemplateListOut,
    ValidatorListOut,
)
from app.core import flags
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.identity import User
from app.models.skills import (
    CONTENT_STATUSES,
    STEP_KINDS,
    LearningPath,
    LearningPathStep,
    Lesson,
    Skill,
    TaskTemplate,
)

router = APIRouter(
    prefix="/skills/content",
    tags=["skills"],
    dependencies=[
        Depends(require_flag(flags.SKILLS_JOURNEY)),
        Depends(require_permission("project.write")),
    ],
)


class LessonIn(BaseModel):
    skill_id: int
    slug: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=2, max_length=200)
    body_md: str = ""
    estimated_minutes: int | None = Field(default=None, ge=1)
    status: str = Field(default="draft", max_length=16)


class LessonPatchIn(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    body_md: str | None = None
    estimated_minutes: int | None = Field(default=None, ge=1)
    status: str | None = Field(default=None, max_length=16)


class PathIn(BaseModel):
    skill_id: int
    slug: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=2, max_length=200)
    summary: str | None = Field(default=None, max_length=500)
    level: str = Field(default="beginner", max_length=20)
    estimated_hours: int | None = Field(default=None, ge=1)
    status: str = Field(default="draft", max_length=16)


class PathPatchIn(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    summary: str | None = Field(default=None, max_length=500)
    level: str | None = Field(default=None, max_length=20)
    estimated_hours: int | None = Field(default=None, ge=1)
    status: str | None = Field(default=None, max_length=16)


class StepIn(BaseModel):
    path_id: int
    ordinal: int = Field(ge=1)
    kind: str = Field(min_length=3, max_length=16)
    title: str | None = Field(default=None, max_length=200)
    lesson_id: int | None = None
    task_template_id: int | None = None


class TemplateIn(BaseModel):
    skill_id: int
    slug: str = Field(min_length=2, max_length=80)
    name: str = Field(min_length=2, max_length=120)
    instructions_md: str = ""
    input_schema: dict = Field(default_factory=dict)
    answer_schema: dict = Field(default_factory=dict)
    validator: str = Field(default="exact_key", max_length=40)
    config: dict | None = None
    status: str = Field(default="draft", max_length=16)


class TemplatePatchIn(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    instructions_md: str | None = None
    input_schema: dict | None = None
    answer_schema: dict | None = None
    validator: str | None = Field(default=None, max_length=40)
    config: dict | None = None
    status: str | None = Field(default=None, max_length=16)


def _status(value: str) -> str:
    if value not in CONTENT_STATUSES:
        raise ApiError(400, "invalid_content_status", "Use draft, published or archived.")
    return value


def _skill(db: Session, skill_id: int) -> Skill:
    skill = db.get(Skill, skill_id)
    if skill is None:
        raise ApiError(404, "skill_not_found", "That skill does not exist.")
    return skill


@router.get("/lessons", response_model=ContentLessonListOut)
def list_lessons(
    skill_id: int | None = None,
    status: str | None = Query(default=None, max_length=16),
    db: Session = Depends(get_db),
) -> ContentLessonListOut:
    """Drafts included: this is the screen ops edits, not the student reader."""
    stmt = select(Lesson).order_by(Lesson.skill_id, Lesson.slug)
    if skill_id is not None:
        stmt = stmt.where(Lesson.skill_id == skill_id)
    if status is not None:
        stmt = stmt.where(Lesson.status == _status(status))
    rows = db.scalars(stmt).all()
    return ContentLessonListOut(
        lessons=[
            {
                "id": row.id,
                "skill_id": row.skill_id,
                "slug": row.slug,
                "title": row.title,
                "body_md": row.body_md,
                "estimated_minutes": row.estimated_minutes,
                "status": row.status,
            }
            for row in rows
        ]
    )


@router.get("/paths", response_model=ContentPathListOut)
def list_paths(
    skill_id: int | None = None,
    status: str | None = Query(default=None, max_length=16),
    db: Session = Depends(get_db),
) -> ContentPathListOut:
    stmt = select(LearningPath).order_by(LearningPath.skill_id, LearningPath.slug)
    if skill_id is not None:
        stmt = stmt.where(LearningPath.skill_id == skill_id)
    if status is not None:
        stmt = stmt.where(LearningPath.status == _status(status))
    rows = db.scalars(stmt).all()
    return ContentPathListOut(
        paths=[
            {
                "id": row.id,
                "skill_id": row.skill_id,
                "slug": row.slug,
                "title": row.title,
                "summary": row.summary,
                "level": row.level,
                "estimated_hours": row.estimated_hours,
                "status": row.status,
                "steps": [
                    {
                        "id": step.id,
                        "ordinal": step.ordinal,
                        "kind": step.kind,
                        "title": step.title,
                        "lesson_id": step.lesson_id,
                        "task_template_id": step.task_template_id,
                    }
                    for step in db.scalars(
                        select(LearningPathStep)
                        .where(LearningPathStep.path_id == row.id)
                        .order_by(LearningPathStep.ordinal)
                    ).all()
                ],
            }
            for row in rows
        ]
    )


@router.get("/tasks", response_model=ContentTemplateListOut)
def list_templates(
    skill_id: int | None = None,
    status: str | None = Query(default=None, max_length=16),
    db: Session = Depends(get_db),
) -> ContentTemplateListOut:
    stmt = select(TaskTemplate).order_by(TaskTemplate.skill_id, TaskTemplate.slug)
    if skill_id is not None:
        stmt = stmt.where(TaskTemplate.skill_id == skill_id)
    if status is not None:
        stmt = stmt.where(TaskTemplate.status == _status(status))
    rows = db.scalars(stmt).all()
    return ContentTemplateListOut(
        templates=[
            {
                "id": row.id,
                "skill_id": row.skill_id,
                "slug": row.slug,
                "name": row.name,
                "instructions_md": row.instructions_md,
                "input_schema": row.input_schema,
                "answer_schema": row.answer_schema,
                "validator": row.validator,
                "config": row.config,
                "status": row.status,
                "version": row.version,
            }
            for row in rows
        ]
    )


@router.get("/validators", response_model=ValidatorListOut)
def list_validators() -> ValidatorListOut:
    """The task engine's registered names, so a template cannot invent one."""
    from app.services.skills.tasks import VALIDATORS

    return ValidatorListOut(validators=sorted(VALIDATORS))


@router.post("/lessons", status_code=201)
def create_lesson(
    payload: LessonIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    _skill(db, payload.skill_id)
    if db.scalar(select(Lesson.id).where(Lesson.slug == payload.slug)) is not None:
        raise ApiError(409, "lesson_exists", "That lesson slug is already used.")
    lesson = Lesson(
        skill_id=payload.skill_id,
        slug=payload.slug,
        title=payload.title,
        body_md=payload.body_md,
        estimated_minutes=payload.estimated_minutes,
        status=_status(payload.status),
    )
    db.add(lesson)
    db.commit()
    return {"id": lesson.id, "slug": lesson.slug, "status": lesson.status}


@router.patch("/lessons/{lesson_id}")
def update_lesson(
    lesson_id: int,
    payload: LessonPatchIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise ApiError(404, "lesson_not_found", "That lesson does not exist.")
    if payload.title is not None:
        lesson.title = payload.title
    if payload.body_md is not None:
        lesson.body_md = payload.body_md
    if payload.estimated_minutes is not None:
        lesson.estimated_minutes = payload.estimated_minutes
    if payload.status is not None:
        lesson.status = _status(payload.status)
    db.commit()
    return {"id": lesson.id, "slug": lesson.slug, "status": lesson.status}


@router.post("/paths", status_code=201)
def create_path(
    payload: PathIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    _skill(db, payload.skill_id)
    if db.scalar(select(LearningPath.id).where(LearningPath.slug == payload.slug)) is not None:
        raise ApiError(409, "path_exists", "That path slug is already used.")
    path = LearningPath(
        skill_id=payload.skill_id,
        slug=payload.slug,
        title=payload.title,
        summary=payload.summary,
        level=payload.level,
        estimated_hours=payload.estimated_hours,
        status=_status(payload.status),
    )
    db.add(path)
    db.commit()
    return {"id": path.id, "slug": path.slug, "status": path.status}


@router.patch("/paths/{path_id}")
def update_path(
    path_id: int,
    payload: PathPatchIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    path = db.get(LearningPath, path_id)
    if path is None:
        raise ApiError(404, "path_not_found", "That learning path does not exist.")
    if payload.title is not None:
        path.title = payload.title
    if payload.summary is not None:
        path.summary = payload.summary
    if payload.level is not None:
        path.level = payload.level
    if payload.estimated_hours is not None:
        path.estimated_hours = payload.estimated_hours
    if payload.status is not None:
        path.status = _status(payload.status)
    db.commit()
    return {"id": path.id, "slug": path.slug, "status": path.status}


@router.post("/paths/{path_id}/steps", status_code=201)
def add_step(
    path_id: int,
    payload: StepIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    if payload.path_id != path_id:
        raise ApiError(400, "path_mismatch", "The step must belong to this path.")
    path = db.get(LearningPath, path_id)
    if path is None:
        raise ApiError(404, "path_not_found", "That learning path does not exist.")
    if payload.kind not in STEP_KINDS:
        raise ApiError(400, "invalid_step_kind", "Use lesson, practice, project or assessment.")
    if db.scalar(
        select(LearningPathStep.id).where(
            LearningPathStep.path_id == path_id, LearningPathStep.ordinal == payload.ordinal
        )
    ) is not None:
        raise ApiError(409, "step_exists", "That ordinal is already used in this path.")
    if payload.lesson_id is not None and db.get(Lesson, payload.lesson_id) is None:
        raise ApiError(404, "lesson_not_found", "That lesson does not exist.")
    if payload.task_template_id is not None and db.get(TaskTemplate, payload.task_template_id) is None:
        raise ApiError(404, "task_not_found", "That task template does not exist.")

    step = LearningPathStep(
        path_id=path_id,
        ordinal=payload.ordinal,
        kind=payload.kind,
        title=payload.title,
        lesson_id=payload.lesson_id,
        task_template_id=payload.task_template_id,
    )
    db.add(step)
    db.commit()
    return {"id": step.id, "ordinal": step.ordinal, "kind": step.kind}


@router.post("/tasks", status_code=201)
def create_template(
    payload: TemplateIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    _skill(db, payload.skill_id)
    if db.scalar(select(TaskTemplate.id).where(TaskTemplate.slug == payload.slug)) is not None:
        raise ApiError(409, "task_exists", "That task slug is already used.")
    template = TaskTemplate(
        skill_id=payload.skill_id,
        slug=payload.slug,
        name=payload.name,
        instructions_md=payload.instructions_md,
        input_schema=payload.input_schema,
        answer_schema=payload.answer_schema,
        validator=payload.validator,
        config=payload.config,
        status=_status(payload.status),
    )
    db.add(template)
    db.commit()
    return {"id": template.id, "slug": template.slug, "status": template.status}


@router.patch("/tasks/{template_id}")
def update_template(
    template_id: int,
    payload: TemplatePatchIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    template = db.get(TaskTemplate, template_id)
    if template is None:
        raise ApiError(404, "task_not_found", "That task template does not exist.")
    if payload.name is not None:
        template.name = payload.name
    if payload.instructions_md is not None:
        template.instructions_md = payload.instructions_md
    if payload.input_schema is not None:
        template.input_schema = payload.input_schema
    if payload.answer_schema is not None:
        template.answer_schema = payload.answer_schema
    if payload.validator is not None:
        template.validator = payload.validator
    if payload.config is not None:
        template.config = payload.config
    if payload.status is not None:
        if payload.status == "published":
            # Publishing an existing template is a new version, so work already
            # submitted keeps pointing at the definition it was graded against.
            template.version = template.version + 1
        template.status = _status(payload.status)
    db.commit()
    return {"id": template.id, "slug": template.slug, "status": template.status, "version": template.version}


__all__ = ["router"]
