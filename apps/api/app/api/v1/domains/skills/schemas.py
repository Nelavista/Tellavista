"""Skills contracts (A3).

These models exist so the student journey has one description of each shape: the
routes validate against them, the OpenAPI schema is generated from them, and the
web app imports the generated types instead of a hand-copied interface. A field
that a service stops returning is a 500 in tests, not a silent `undefined` in the
browser.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class SkillOut(BaseModel):
    """One catalog row. `published_paths` is what the student can actually open."""

    id: int
    slug: str
    name: str
    description: str | None = None
    category: str | None = None
    category_slug: str | None = None
    published_paths: int


class SkillsOut(BaseModel):
    skills: list[SkillOut]


class PathSummaryOut(BaseModel):
    id: int
    slug: str
    title: str
    summary: str | None = None
    level: str
    estimated_hours: int | None = None


class SkillDetailOut(BaseModel):
    id: int
    slug: str
    name: str
    description: str | None = None
    paths: list[PathSummaryOut]


class PathStepOut(BaseModel):
    """One position in a path, with the student's own state on it.

    `unlocked` is computed server-side from the steps before this one, so the UI
    never has to re-derive path order (and cannot disagree with the API about it).
    """

    id: int
    ordinal: int
    kind: str
    title: str | None = None
    lesson_id: int | None = None
    # The reader route is slug-addressed, so a step can link into it directly.
    lesson_slug: str | None = None
    task_template_id: int | None = None
    completed: bool
    unlocked: bool
    progress_status: str | None = None
    estimated_minutes: int | None = None


class PathOut(BaseModel):
    id: int
    slug: str
    title: str
    summary: str | None = None
    level: str
    estimated_hours: int | None = None
    skill_id: int
    steps: list[PathStepOut]
    completed_steps: int
    required_steps: int
    percent_complete: int
    next_step: PathStepOut | None = None


class MyLearningOut(BaseModel):
    paths: list[PathOut]


class LessonOut(BaseModel):
    id: int
    slug: str
    title: str
    body_md: str
    estimated_minutes: int | None = None
    skill_id: int
    status: str
    unlocked: bool


class LessonStartedOut(BaseModel):
    lesson_id: int
    status: str


class LessonCompletedOut(BaseModel):
    """Completion is progress. `verified` is always false, and says so out loud."""

    lesson_id: int
    status: str
    completed_at: datetime | None = None
    verified: bool = False
    note: str


class PracticeBriefOut(BaseModel):
    """What the student sees. The expected answer is never part of this shape."""

    template_id: int
    slug: str
    name: str
    instructions_md: str
    input_schema: dict[str, Any]
    answer_schema: dict[str, Any]
    sample: Any | None = None
    version: int


class PracticeResultOut(BaseModel):
    attempt_id: int
    is_correct: bool
    score: int
    feedback: str
    details: dict[str, Any]
    counts_as_verification: bool = False


__all__ = [
    "LessonCompletedOut",
    "LessonOut",
    "LessonStartedOut",
    "MyLearningOut",
    "PathOut",
    "PathStepOut",
    "PathSummaryOut",
    "PracticeBriefOut",
    "PracticeResultOut",
    "SkillDetailOut",
    "SkillOut",
    "SkillsOut",
]
