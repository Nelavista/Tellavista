"""Phase 0 PR 0.2b — skills, learning paths, lessons, task templates, progress.

Model-level rules: slugs are unique, path order is enforced, content starts as a
draft, a skill's children disappear with it, and progress is — structurally —
not verification. Uses the shared `db` fixture from conftest.py.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import User
from app.models.skills import (
    STATUS_DRAFT,
    LearningPath,
    LearningPathStep,
    Lesson,
    LessonProgress,
    Skill,
    SkillCategory,
    TaskTemplate,
)

EXPECTED_TABLES = {
    "skill_categories",
    "skills",
    "learning_paths",
    "lessons",
    "learning_path_steps",
    "task_templates",
    "lesson_progress",
}


def _user(db: Session) -> User:
    student = db.scalar(select(Role).where(Role.code == ROLE_STUDENT))
    user = User(
        email=f"u{uuid.uuid4().hex[:8]}@example.test",
        username=f"u{uuid.uuid4().hex[:8]}",
        role_id=student.id if student else None,
    )
    db.add(user)
    db.flush()
    return user


def _skill(db: Session, category: SkillCategory | None = None) -> Skill:
    skill = Skill(
        slug=f"skill-{uuid.uuid4().hex[:8]}",
        name="AI Data Annotation",
        category_id=category.id if category else None,
    )
    db.add(skill)
    db.flush()
    return skill


def _path(db: Session, skill: Skill) -> LearningPath:
    path = LearningPath(slug=f"path-{uuid.uuid4().hex[:8]}", title="Annotate text", skill_id=skill.id)
    db.add(path)
    db.flush()
    return path


def test_tables_exist_and_template_schemas_are_jsonb_on_postgres(db: Session) -> None:
    assert EXPECTED_TABLES <= set(inspect(db.get_bind()).get_table_names())
    for name in ("input_schema", "answer_schema", "config"):
        column = TaskTemplate.__table__.c[name]
        assert isinstance(column.type.dialect_impl(postgresql.dialect()), JSONB)
    assert not TaskTemplate.__table__.c.input_schema.nullable
    assert not TaskTemplate.__table__.c.answer_schema.nullable


def test_slugs_are_unique_across_the_catalogue(db: Session) -> None:
    category = SkillCategory(slug=f"cat-{uuid.uuid4().hex[:8]}", name="AI & Data")
    db.add(category)
    db.flush()
    _skill(db, category)

    db.add(SkillCategory(slug=category.slug, name="Duplicate"))
    with pytest.raises(IntegrityError):
        db.flush()


def test_skill_slug_is_unique(db: Session) -> None:
    skill = _skill(db)
    db.add(Skill(slug=skill.slug, name="Impostor"))
    with pytest.raises(IntegrityError):
        db.flush()


def test_retiring_a_category_keeps_its_skills(db: Session) -> None:
    category = SkillCategory(slug=f"cat-{uuid.uuid4().hex[:8]}", name="AI & Data")
    db.add(category)
    db.flush()
    skill = _skill(db, category)

    db.delete(category)
    db.flush()
    db.expire_all()
    assert db.scalar(select(Skill.slug).where(Skill.id == skill.id)) == skill.slug
    assert db.scalar(select(Skill.category_id).where(Skill.id == skill.id)) is None


def test_path_step_order_is_unique_within_a_path(db: Session) -> None:
    path = _path(db, _skill(db))
    db.add(LearningPathStep(path_id=path.id, ordinal=1, kind="lesson", title="Why labels matter"))
    db.flush()
    db.add(LearningPathStep(path_id=path.id, ordinal=1, kind="practice", title="Duplicate"))
    with pytest.raises(IntegrityError):
        db.flush()


def test_a_deleted_lesson_leaves_the_step_in_place(db: Session) -> None:
    skill = _skill(db)
    path = _path(db, skill)
    lesson = Lesson(slug=f"lesson-{uuid.uuid4().hex[:8]}", title="Introduction", skill_id=skill.id)
    db.add(lesson)
    db.flush()
    step = LearningPathStep(path_id=path.id, ordinal=1, kind="lesson", lesson_id=lesson.id)
    db.add(step)
    db.flush()

    db.delete(lesson)
    db.flush()
    db.expire_all()
    remaining = db.scalars(select(LearningPathStep)).one()
    assert remaining.lesson_id is None and remaining.ordinal == 1


def test_content_starts_as_a_draft_and_templates_are_versioned(db: Session) -> None:
    skill = _skill(db)
    path = _path(db, skill)
    lesson = Lesson(slug=f"lesson-{uuid.uuid4().hex[:8]}", title="Intro", skill_id=skill.id)
    template = TaskTemplate(
        slug=f"task-{uuid.uuid4().hex[:8]}",
        name="Text classification",
        skill_id=skill.id,
        input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
        answer_schema={"type": "object", "properties": {"label": {"type": "string"}}},
        config={"labels": ["positive", "negative", "neutral"]},
    )
    db.add_all([lesson, template])
    db.flush()

    assert path.status == lesson.status == template.status == STATUS_DRAFT
    assert template.version == 1
    assert template.validator == "exact_key"
    assert template.config["labels"] == ["positive", "negative", "neutral"]


def test_deleting_a_skill_removes_its_content_but_not_its_students(db: Session) -> None:
    skill = _skill(db)
    path = _path(db, skill)
    lesson = Lesson(slug=f"lesson-{uuid.uuid4().hex[:8]}", title="Intro", skill_id=skill.id)
    db.add(lesson)
    db.flush()
    db.add(LearningPathStep(path_id=path.id, ordinal=1, kind="lesson", lesson_id=lesson.id))
    user = _user(db)
    db.add(LessonProgress(user_id=user.id, lesson_id=lesson.id))
    db.flush()

    db.delete(skill)
    db.flush()

    assert db.scalars(select(LearningPath)).all() == []
    assert db.scalars(select(LearningPathStep)).all() == []
    assert db.scalars(select(Lesson)).all() == []
    assert db.scalars(select(LessonProgress)).all() == []
    assert db.scalars(select(User).where(User.id == user.id)).one() is not None


def test_progress_is_one_row_per_student_and_lesson(db: Session) -> None:
    skill = _skill(db)
    lesson = Lesson(slug=f"lesson-{uuid.uuid4().hex[:8]}", title="Intro", skill_id=skill.id)
    user = _user(db)
    db.add(lesson)
    db.flush()
    db.add(LessonProgress(user_id=user.id, lesson_id=lesson.id))
    db.flush()
    db.add(LessonProgress(user_id=user.id, lesson_id=lesson.id))
    with pytest.raises(IntegrityError):
        db.flush()


def test_completing_a_lesson_is_progress_and_nothing_more(db: Session) -> None:
    """No column here can verify anyone: that is M3's assessment evidence."""
    assert "verified" not in LessonProgress.__table__.c
    assert "verification" not in EXPECTED_TABLES

    skill = _skill(db)
    lesson = Lesson(slug=f"lesson-{uuid.uuid4().hex[:8]}", title="Intro", skill_id=skill.id)
    user = _user(db)
    db.add(lesson)
    db.flush()
    progress = LessonProgress(user_id=user.id, lesson_id=lesson.id)
    db.add(progress)
    db.flush()
    assert progress.status == "not_started" and progress.completed_at is None

    progress.status = "completed"
    progress.completed_at = datetime.now(UTC)
    db.flush()
    row = db.scalars(select(LessonProgress)).one()
    assert row.status == "completed" and row.completed_at is not None
