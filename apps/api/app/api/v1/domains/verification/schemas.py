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
    """One skill's current badge state. `verified` is derived from `status`.

    `status_reason` and `status_changed_at` come from the latest verification
    event, so a suspended or at-risk badge can say *why* and *when* instead of
    only showing a label (B7 re-verification prompt).
    """

    skill_id: int
    skill: str
    slug: str
    status: str
    status_reason: str | None = None
    status_changed_at: datetime | None = None
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


# --- practical tasks (B7 remaining) -----------------------------------------


class PracticalTaskOut(BaseModel):
    """A real brief and its rubric. The rubric is shown, so the standard is public."""

    id: int
    slug: str
    title: str
    brief_md: str
    skill_id: int
    rubric: Any | None = None


class PracticalTaskListOut(BaseModel):
    tasks: list[PracticalTaskOut]


class PracticalSubmissionOut(BaseModel):
    id: int
    status: str
    submitted_at: datetime | None = None
    message: str


class PracticalQueueItemOut(BaseModel):
    id: int
    practical_task_id: int
    user_id: int
    status: str
    submitted_at: datetime | None = None


class PracticalQueueOut(BaseModel):
    submissions: list[PracticalQueueItemOut]


class PracticalReviewOut(BaseModel):
    id: int
    status: str
    score: int | None = None
    passed: bool | None = None


class OverrideOut(BaseModel):
    user_id: int
    skill_id: int
    status: str
    event_id: int
    reason: str | None = None


__all__ = [
    "AssessmentListOut",
    "AssessmentOut",
    "AttemptOut",
    "AttemptResultOut",
    "AttemptResultTaskOut",
    "AttemptSubmitIn",
    "AttemptTaskOut",
    "OverrideOut",
    "PracticalQueueItemOut",
    "PracticalQueueOut",
    "PracticalReviewOut",
    "PracticalSubmissionOut",
    "PracticalTaskListOut",
    "PracticalTaskOut",
    "ReviewOut",
    "ReviewTaskOut",
    "TranscriptCountsOut",
    "TranscriptEntryOut",
    "TranscriptEvidenceOut",
    "TranscriptOut",
    "VerificationOut",
    "VerificationSkillOut",
]
