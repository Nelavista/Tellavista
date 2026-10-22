"""Academia dashboard contract (A3).

The five questions are a fixed shape: each carries a plain-language `answer` and
the rows behind it. Modelling it means the dashboard the web app reads is the
dashboard the API validates, instead of two hand-kept copies.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

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


# --- Materials (B14) ---------------------------------------------------------


class MaterialCourseOut(BaseModel):
    """The course a material belongs to. `title` is omitted in search results."""

    id: int | None = None
    code: str | None = None
    title: str | None = None


class MaterialOut(BaseModel):
    id: int
    title: str
    file_url: str | None = None
    source: str | None = None
    course: MaterialCourseOut | None = None


class MaterialListOut(BaseModel):
    materials: list[MaterialOut]


class MaterialSearchResultOut(BaseModel):
    material_id: int
    title: str
    course: MaterialCourseOut | None = None
    snippet: str
    score: float


class MaterialSearchOut(BaseModel):
    query: str
    results: list[MaterialSearchResultOut]


class MaterialChunkOut(BaseModel):
    id: int
    ordinal: int
    content: str


class MaterialDetailOut(BaseModel):
    id: int
    title: str
    file_url: str | None = None
    course: MaterialCourseOut | None = None
    chunks: list[MaterialChunkOut]


# --- Ask Nelavista (B14) ----------------------------------------------------


class AskCitationOut(BaseModel):
    """Every answer names the chunks it was built from, so it can be checked."""

    chunk_id: int
    material_id: int
    material_title: str
    course_code: str
    score: float


class AskAnswerOut(BaseModel):
    session_id: int
    answer: str
    declined: bool
    citations: list[AskCitationOut]
    # Null on an honest decline: no provider was asked.
    provider: str | None = None
    best_score: float | None = None


class AskCourseRefOut(BaseModel):
    id: int
    code: str | None = None


class AskSessionSummaryOut(BaseModel):
    id: int
    title: str | None = None
    course: AskCourseRefOut | None = None
    created_at: datetime


class AskSessionListOut(BaseModel):
    sessions: list[AskSessionSummaryOut]


class AskMessageOut(BaseModel):
    id: int
    role: str
    content: str
    citations: list[AskCitationOut]
    declined: bool
    created_at: datetime


class AskSessionOut(BaseModel):
    id: int
    title: str | None = None
    course_id: int | None = None
    messages: list[AskMessageOut]


# --- CBT (B14) ---------------------------------------------------------------


class CbtCourseRefOut(BaseModel):
    id: int
    code: str | None = None


class CbtQuestionOut(BaseModel):
    """A practice question. `correct_key` is never part of this shape."""

    id: int
    topic_id: int | None = None
    prompt: str
    options: list[dict[str, Any]]
    difficulty: str | None = None


class CbtQuizOut(BaseModel):
    course: CbtCourseRefOut
    count: int
    questions: list[CbtQuestionOut]


class CbtAnswerOut(BaseModel):
    attempt_id: int
    question_id: int
    is_correct: bool
    correct_key: str | None = None
    explanation: str | None = None


class CbtRecentOut(BaseModel):
    attempt_id: int
    question_id: int
    is_correct: bool
    answered_at: datetime | None = None


class CbtRecommendationOut(BaseModel):
    topic_id: int | None = None
    topic: str
    accuracy: int
    action: str


class CbtResultsOut(BaseModel):
    course_id: int
    topics: list[TopicStatOut]
    strengths: list[TopicStatOut]
    weaknesses: list[TopicStatOut]
    recommendations: list[CbtRecommendationOut]
    recent: list[CbtRecentOut]


class CbtPracticeQuestionOut(BaseModel):
    id: int
    topic_id: int | None = None
    prompt: str
    options: list[dict[str, Any]]


class CbtPracticeNextOut(BaseModel):
    course_id: int
    focus_topics: list[int | None]
    questions: list[CbtPracticeQuestionOut]


__all__ = [
    "AskAnswerOut",
    "AskCitationOut",
    "AskCourseRefOut",
    "AskMessageOut",
    "AskSessionListOut",
    "AskSessionOut",
    "AskSessionSummaryOut",
    "CbtAnswerOut",
    "CbtCourseRefOut",
    "CbtPracticeNextOut",
    "CbtPracticeQuestionOut",
    "CbtQuestionOut",
    "CbtQuizOut",
    "CbtRecentOut",
    "CbtRecommendationOut",
    "CbtResultsOut",
    "DashboardOut",
    "DashboardQuestionsOut",
    "NextActionOut",
    "MaterialChunkOut",
    "MaterialCourseOut",
    "MaterialDetailOut",
    "MaterialListOut",
    "MaterialOut",
    "MaterialSearchOut",
    "MaterialSearchResultOut",
    "NextQuestionOut",
    "PracticeItemOut",
    "PractiseQuestionOut",
    "RecentItemOut",
    "RecentQuestionOut",
    "StudyingQuestionOut",
    "TopicStatOut",
    "WeakQuestionOut",
]
