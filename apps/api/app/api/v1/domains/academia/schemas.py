"""Academia dashboard contract (A3).

The five questions are a fixed shape: each carries a plain-language `answer` and
the rows behind it. Modelling it means the dashboard the web app reads is the
dashboard the API validates, instead of two hand-kept copies.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.api.v1.domains.identity.schemas import EnrolmentOut


class TopicStatOut(BaseModel):
    """Accuracy over practice answers, with the strength/weakness verdict."""

    topic_id: int | None = None
    topic: str
    attempts: int
    correct: int
    accuracy: int
    strength: bool
    weakness: bool


class RecentItemOut(BaseModel):
    kind: str
    title: str
    when: datetime | None = None


class PracticeItemOut(BaseModel):
    topic_id: int | None = None
    topic: str
    accuracy: int | None = None


class NextActionOut(BaseModel):
    """One action, with a destination the client can open and a readable reason."""

    kind: str
    label: str
    reason: str
    topic_id: int | None = None
    lesson_id: int | None = None
    material_id: int | None = None


class StudyingQuestionOut(BaseModel):
    answer: str
    courses: list[EnrolmentOut]


class RecentQuestionOut(BaseModel):
    answer: str
    items: list[RecentItemOut]


class PractiseQuestionOut(BaseModel):
    answer: str
    items: list[PracticeItemOut]


class WeakQuestionOut(BaseModel):
    answer: str
    items: list[TopicStatOut]


class NextQuestionOut(BaseModel):
    answer: str | None = None
    action: NextActionOut


class DashboardQuestionsOut(BaseModel):
    what_am_i_studying: StudyingQuestionOut
    what_did_i_study_recently: RecentQuestionOut
    what_should_i_practise: PractiseQuestionOut
    where_am_i_weak: WeakQuestionOut
    what_should_i_do_next: NextQuestionOut


class DashboardOut(BaseModel):
    questions: DashboardQuestionsOut
    # Course id (as a string, because JSON object keys are strings) → count.
    materials_by_course: dict[str, int]
    enrolment_count: int


__all__ = [
    "DashboardOut",
    "DashboardQuestionsOut",
    "NextActionOut",
    "NextQuestionOut",
    "PracticeItemOut",
    "PractiseQuestionOut",
    "RecentItemOut",
    "RecentQuestionOut",
    "StudyingQuestionOut",
    "TopicStatOut",
    "WeakQuestionOut",
]
