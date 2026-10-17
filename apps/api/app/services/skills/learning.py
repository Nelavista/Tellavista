"""Learn → Practise → Build: catalog, sequential progress and My Learning (PRD §4).

Two honesty rules are enforced here, not in the UI:

* A lesson can only be completed after the steps before it. Progress is real
  sequential progress, not a list of visited pages.
* Completing a lesson writes `LessonProgress` and **nothing else**. Verification is
  a separate module with different evidence; no function in this module can set a
  verification status.
"""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.identity import User
from app.models.skills import (
    COMPLETED,
    IN_PROGRESS,
    STATUS_PUBLISHED,
    LearningPath,
    LearningPathStep,
    Lesson,
    LessonProgress,
    PracticeAttempt,
    Skill,
    SkillCategory,
)


def list_skills(db: Session) -> list[dict]:
    categories = {row.id: row for row in db.scalars(select(SkillCategory)).all()}
    skills = db.scalars(select(Skill).where(Skill.is_active.is_(True)).order_by(Skill.name)).all()
    path_counts = dict(
        db.execute(
            select(LearningPath.skill_id, func.count(LearningPath.id))
            .where(LearningPath.status == STATUS_PUBLISHED)
            .group_by(LearningPath.skill_id)
        ).all()
    )
    result: list[dict] = []
    for skill in skills:
        category = categories.get(skill.category_id)
        result.append(
            {
                "id": skill.id,
                "slug": skill.slug,
                "name": skill.name,
                "description": skill.description,
                "category": category.name if category else None,
                "category_slug": category.slug if category else None,
                "published_paths": path_counts.get(skill.id, 0),
            }
        )
    return result


def get_skill(db: Session, slug: str) -> dict:
    skill = db.scalar(select(Skill).where(Skill.slug == slug, Skill.is_active.is_(True)))
    if skill is None:
        raise ApiError(404, "skill_not_found", "That skill does not exist.")
    paths = db.scalars(
        select(LearningPath)
        .where(LearningPath.skill_id == skill.id, LearningPath.status == STATUS_PUBLISHED)
        .order_by(LearningPath.title)
    ).all()
    return {
        "id": skill.id,
        "slug": skill.slug,
        "name": skill.name,
        "description": skill.description,
        "paths": [
            {
                "id": path.id,
                "slug": path.slug,
                "title": path.title,
                "summary": path.summary,
                "level": path.level,
                "estimated_hours": path.estimated_hours,
            }
            for path in paths
        ],
    }


def get_path(db: Session, path_slug: str) -> LearningPath:
    path = db.scalar(select(LearningPath).where(LearningPath.slug == path_slug))
    if path is None or path.status != STATUS_PUBLISHED:
        raise ApiError(404, "path_not_found", "That learning path is not available.")
    return path


def _steps(db: Session, path_id: int) -> list[LearningPathStep]:
    return list(
        db.scalars(
            select(LearningPathStep)
            .where(LearningPathStep.path_id == path_id)
            .order_by(LearningPathStep.ordinal)
        ).all()
    )


def _progress_map(db: Session, user: User) -> dict[int, LessonProgress]:
    return {
        row.lesson_id: row
        for row in db.scalars(
            select(LessonProgress).where(LessonProgress.user_id == user.id)
        ).all()
    }


def _practice_template_ids(db: Session, user: User) -> set[int]:
    return {
        row
        for row in db.scalars(
            select(PracticeAttempt.template_id).where(
                PracticeAttempt.user_id == user.id, PracticeAttempt.is_correct.is_(True)
            )
        ).all()
        if row is not None
    }


def _step_done(step: LearningPathStep, progress: dict[int, LessonProgress], practice: set[int]) -> bool:
    if step.kind == "lesson" and step.lesson_id is not None:
        row = progress.get(step.lesson_id)
        return row is not None and row.status == COMPLETED
    if step.kind == "practice" and step.task_template_id is not None:
        return step.task_template_id in practice
    # Project and assessment steps are shown but do not lock the next lesson:
    # a project can take days and must not stall learning.
    return False


def path_with_progress(db: Session, user: User, path: LearningPath) -> dict:
    progress = _progress_map(db, user)
    practice = _practice_template_ids(db, user)
    steps = _steps(db, path.id)

    lessons = {
        lesson.id: lesson
        for lesson in db.scalars(
            select(Lesson).where(Lesson.id.in_([s.lesson_id for s in steps if s.lesson_id]))
        ).all()
    }

    completed_count = 0
    payload: list[dict] = []
    previous_done = True
    for step in steps:
        done = _step_done(step, progress, practice)
        completed_count += int(done)
        lesson = lessons.get(step.lesson_id) if step.lesson_id else None
        step_progress = progress.get(step.lesson_id) if step.lesson_id else None
        payload.append(
            {
                "id": step.id,
                "ordinal": step.ordinal,
                "kind": step.kind,
                "title": step.title or (lesson.title if lesson else None),
                "lesson_id": step.lesson_id,
                "task_template_id": step.task_template_id,
                "completed": done,
                "unlocked": previous_done,
                "progress_status": step_progress.status if step_progress else None,
                "estimated_minutes": lesson.estimated_minutes if lesson else None,
            }
        )
        # Only a lesson or practice step gates the one after it.
        if step.kind in {"lesson", "practice"}:
            previous_done = done

    total = sum(1 for step in steps if step.kind in {"lesson", "practice"})
    percent = round(100 * min(completed_count, total) / total) if total else 0
    next_step = next((step for step in payload if not step["completed"] and step["unlocked"]), None)
    return {
        "id": path.id,
        "slug": path.slug,
        "title": path.title,
        "summary": path.summary,
        "level": path.level,
        "estimated_hours": path.estimated_hours,
        "skill_id": path.skill_id,
        "steps": payload,
        "completed_steps": completed_count,
        "required_steps": total,
        "percent_complete": percent,
        "next_step": next_step,
    }


def lesson_detail(db: Session, user: User, lesson_slug: str) -> dict:
    lesson = db.scalar(select(Lesson).where(Lesson.slug == lesson_slug))
    if lesson is None or lesson.status != STATUS_PUBLISHED:
        raise ApiError(404, "lesson_not_found", "That lesson is not available.")

    # Which path(s) contain this lesson, and is the student allowed to finish it?
    steps = db.scalars(
        select(LearningPathStep).where(LearningPathStep.lesson_id == lesson.id)
    ).all()
    unlocked = True
    for step in steps:
        path = db.get(LearningPath, step.path_id)
        if path is None or path.status != STATUS_PUBLISHED:
            continue
        progress = _progress_map(db, user)
        practice = _practice_template_ids(db, user)
        for earlier in _steps(db, path.id):
            if earlier.ordinal >= step.ordinal:
                break
            if earlier.kind in {"lesson", "practice"} and not _step_done(earlier, progress, practice):
                unlocked = False
                break
        if not unlocked:
            break

    row = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id
        )
    )
    return {
        "id": lesson.id,
        "slug": lesson.slug,
        "title": lesson.title,
        "body_md": lesson.body_md,
        "estimated_minutes": lesson.estimated_minutes,
        "skill_id": lesson.skill_id,
        "status": row.status if row else "not_started",
        "unlocked": unlocked,
    }


def start_lesson(db: Session, user: User, lesson_id: int) -> LessonProgress:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None or lesson.status != STATUS_PUBLISHED:
        raise ApiError(404, "lesson_not_found", "That lesson is not available.")
    row = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_id
        )
    )
    if row is None:
        row = LessonProgress(
            user_id=user.id, lesson_id=lesson_id, status=IN_PROGRESS, started_at=utcnow()
        )
        db.add(row)
        db.flush()
    elif row.status == "not_started":
        row.status = IN_PROGRESS
        row.started_at = utcnow()
        db.flush()
    return row


def complete_lesson(db: Session, user: User, lesson_id: int) -> LessonProgress:
    """Mark a lesson complete, enforcing path order. Idempotent.

    Completing an already-completed lesson returns the existing row; a retry from
    an offline client different with ``started_at`` still succeeds.
    """
    lesson = db.get(Lesson, lesson_id)
    if lesson is None or lesson.status != STATUS_PUBLISHED:
        raise ApiError(404, "lesson_not_found", "That lesson is not available.")

    row = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_id
        )
    )
    if row is not None and row.status == COMPLETED:
        return row

    steps = db.scalars(
        select(LearningPathStep).where(LearningPathStep.lesson_id == lesson.id)
    ).all()
    progress = _progress_map(db, user)
    practice = _practice_template_ids(db, user)
    for step in steps:
        path = db.get(LearningPath, step.path_id)
        if path is None or path.status != STATUS_PUBLISHED:
            continue
        for earlier in _steps(db, path.id):
            if earlier.ordinal >= step.ordinal:
                break
            if earlier.kind in {"lesson", "practice"} and not _step_done(earlier, progress, practice):
                raise ApiError(
                    409,
                    "step_locked",
                    "Finish the previous step first.",
                    {"path_slug": path.slug, "step_ordinal": earlier.ordinal},
                )

    if row is None:
        row = LessonProgress(user_id=user.id, lesson_id=lesson_id, status=COMPLETED)
        db.add(row)
    row.status = COMPLETED
    row.started_at = row.started_at or utcnow()
    row.completed_at = utcnow()
    db.flush()

    # A transcript "learned" line, linked to this exact progress row. It is a
    # record of learning, never of proof; only verification adds "proved".
    from app.models.verification import TRANSCRIPT_LEARNED
    from app.services.verification.transcript import add_entry

    add_entry(
        db,
        user_id=user.id,
        kind=TRANSCRIPT_LEARNED,
        title=lesson.title,
        evidence_type="lesson_progress",
        evidence_id=row.id,
        skill_id=lesson.skill_id,
    )
    return row


def my_learning(db: Session, user: User) -> list[dict]:
    """Every path the student has touched, with honest progress."""
    started_lesson_ids = {
        row.lesson_id
        for row in db.scalars(select(LessonProgress).where(LessonProgress.user_id == user.id)).all()
    }
    if not started_lesson_ids:
        return []

    paths = db.scalars(
        select(LearningPath)
        .join(LearningPathStep, LearningPathStep.path_id == LearningPath.id)
        .where(
            LearningPathStep.lesson_id.in_(started_lesson_ids),
            LearningPath.status == STATUS_PUBLISHED,
        )
        .distinct()
    ).all()
    return [path_with_progress(db, user, path) for path in paths]
