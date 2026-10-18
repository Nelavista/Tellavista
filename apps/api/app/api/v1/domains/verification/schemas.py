"""Verification contracts (B7).

The student journey reads these shapes: current verification state, a sitting,
the graded result, the post-submission review and the transcript. The models are
the contract — a service that stops returning a field fails in tests instead of
rendering `undefined` in the browser.

Two rules are visible in the shapes themselves:

* `AttemptTaskOut` carries the template's `input_schema`/`answer_schema`, so the
  web app renders the same generated control it uses for practice — but never the
  expected answer.
* `expected_answer` appears only on `ReviewTaskOut`, which the route refuses to
  serve before submission. The type system should not make the leak look normal.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class VerificationSkillOut(BaseModel):
    """One skill's current badge state. `verified` is derived from `status`."""

    skill_id: int
    skill: str
    slug: str
    status: str
    verified_at: datetime | None = None
    last_evaluated_at: datetime | None = None
    verified: bool


class VerificationOut(BaseModel):
    skills: list[VerificationSkillOut]


class TranscriptEvidenceOut(BaseModel):
    """Every transcript line names the row it came from. There is no free text."""

    type: str
    id: str


class TranscriptEntryOut(BaseModel):
    id: int
    kind: str
    title: str
    skill: str | None = None
    skill_slug: str | None = None
    evidence: TranscriptEvidenceOut
    occurred_at: datetime


class TranscriptCountsOut(BaseModel):
    learned: int
    proved: int
    delivered: int


class TranscriptOut(BaseModel):
    entries: list[TranscriptEntryOut]
    learned: list[TranscriptEntryOut]
    proved: list[TranscriptEntryOut]
    delivered: list[TranscriptEntryOut]
    counts: TranscriptCountsOut


class AssessmentOut(BaseModel):
    id: int
    slug: str
    title: str
    skill_id: int
    pass_threshold: int
    max_attempts: int
    task_count: int


class AssessmentListOut(BaseModel):
    assessments: list[AssessmentOut]


class AttemptTaskOut(BaseModel):
    """What the student is shown. The expected answer is deliberately absent."""

    task_id: int
    ordinal: int
    payload: dict[str, Any]
    points: int
    template_id: int | None = None
    input_schema: dict[str, Any] | None = None
    answer_schema: dict[str, Any] | None = None


class AttemptOut(BaseModel):
    attempt_id: int
    assessment_id: int
    started_at: datetime
    expires_at: datetime
    tasks: list[AttemptTaskOut]


class AttemptSubmitIn(BaseModel):
    answers: dict[str, Any] = Field(default_factory=dict)


class AttemptResultTaskOut(BaseModel):
    task_id: int
    ordinal: int
    correct: bool
    points: int
    max_points: int
    feedback: str | None = None


class AttemptResultOut(BaseModel):
    """The graded sitting. An expired attempt is a real result, not an error."""

    attempt_id: int
    score: int
    passed: bool
    expired: bool
    pass_threshold: int | None = None
    verification_status: str | None = None
    message: str | None = None
    tasks: list[AttemptResultTaskOut]


class ReviewTaskOut(BaseModel):
    task_id: int
    ordinal: int
    payload: dict[str, Any]
    answer: Any | None = None
    expected_answer: Any | None = None
    correct: bool
    feedback: str | None = None


class ReviewOut(BaseModel):
    attempt_id: int
    score: int | None = None
    passed: bool | None = None
    submitted_at: datetime | None = None
    tasks: list[ReviewTaskOut]


__all__ = [
    "AssessmentListOut",
    "AssessmentOut",
    "AttemptOut",
    "AttemptResultOut",
    "AttemptResultTaskOut",
    "AttemptSubmitIn",
    "AttemptTaskOut",
    "ReviewOut",
    "ReviewTaskOut",
    "TranscriptCountsOut",
    "TranscriptEntryOut",
    "TranscriptEvidenceOut",
    "TranscriptOut",
    "VerificationOut",
    "VerificationSkillOut",
]
