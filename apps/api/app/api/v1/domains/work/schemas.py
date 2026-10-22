"""Work delivery and quality contracts (B9, C4, C5).

The student screens and the review queue read the same submission: a reviewer
must see exactly what the student sent, and the student must never see the gold
answer. `AssignmentTaskOut` therefore carries the template schemas but no
expected answer — the same rule as a verification sitting.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class ProjectRefOut(BaseModel):
    id: int | None = None
    slug: str
    title: str


class AssignmentOut(BaseModel):
    id: int
    title: str
    status: str
    due_at: datetime | None = None
    template_id: int | None = None
    project: ProjectRefOut


class AssignmentListOut(BaseModel):
    assignments: list[AssignmentOut]


class AssignmentTaskOut(BaseModel):
    template_id: int
    name: str
    instructions_md: str
    input_schema: dict[str, Any]
    answer_schema: dict[str, Any]


class LastSubmissionOut(BaseModel):
    id: int
    status: str
    submitted_at: datetime | None = None


class AssignmentDetailOut(BaseModel):
    id: int
    title: str
    status: str
    due_at: datetime | None = None
    project: ProjectRefOut
    task: AssignmentTaskOut | None = None
    last_submission: LastSubmissionOut | None = None


class AssignmentStateOut(BaseModel):
    id: int
    status: str


class SubmissionResultOut(BaseModel):
    id: int
    status: str
    is_gold: bool
    submitted_at: datetime | None = None
    created: bool
    message: str


class SyncResultOut(BaseModel):
    client_key: str
    status: str
    submission_id: int | None = None
    code: str | None = None
    message: str | None = None


class SyncOut(BaseModel):
    results: list[SyncResultOut]
    applied: int
    failed: int


class SubmissionSummaryOut(BaseModel):
    submission_id: int
    assignment_id: int
    assignment_title: str
    status: str
    is_gold: bool
    submitted_at: datetime | None = None


class SubmissionListOut(BaseModel):
    submissions: list[SubmissionSummaryOut]


class QualityRecordOut(BaseModel):
    reviews_count: int
    approvals: int
    reworks: int
    rejections: int
    average_score: int | None = None
    gold_tasks: int
    gold_correct: int
    poor_streak: int


class ConsequenceOut(BaseModel):
    kind: str
    reason: str | None = None
    created_at: datetime


class QualityOut(BaseModel):
    record: QualityRecordOut | None = None
    consequences: list[ConsequenceOut]


class WorkMessageOut(BaseModel):
    id: int
    body: str
    sender_user_id: int | None = None
    read_at: datetime | None = None
    created_at: datetime


class MessageListOut(BaseModel):
    messages: list[WorkMessageOut]


class InviteResponseOut(BaseModel):
    id: int
    status: str
    joined_at: datetime | None = None


class ProjectWriteOut(BaseModel):
    id: int
    slug: str
    status: str


class CohortWriteOut(BaseModel):
    id: int
    name: str
    capacity: int | None = None
    status: str


class CohortMemberOut(BaseModel):
    member_id: int
    user_id: int
    name: str | None = None
    email: str
    status: str
    joined_at: datetime | None = None


class CohortOut(BaseModel):
    id: int
    project_id: int
    name: str
    capacity: int | None = None
    status: str
    seats_used: int
    members: list[CohortMemberOut]
    assignment_counts: dict[str, int]


class ProjectSummaryOut(BaseModel):
    id: int
    slug: str
    title: str
    status: str
    starts_on: date | None = None
    ends_on: date | None = None


class ProjectListOut(BaseModel):
    projects: list[ProjectSummaryOut]


class ProjectOut(BaseModel):
    id: int
    slug: str
    title: str
    status: str
    starts_on: date | None = None
    ends_on: date | None = None
    cohorts: list[CohortOut]
    assignment_counts: dict[str, int]


class InviteOut(BaseModel):
    id: int
    user_id: int
    status: str


class InviteListOut(BaseModel):
    members: list[InviteOut]


class RemoveOut(BaseModel):
    id: int
    status: str


class ReplacementOut(BaseModel):
    """A replacement suggestion: who, and the evidence behind the pick."""

    user_id: int
    name: str | None = None
    email: str | None = None
    score: int
    eligible: bool = True
    qualifies_because: list[str] = []
    next_steps: list[dict[str, Any]] = []


class ReplacementListOut(BaseModel):
    candidates: list[ReplacementOut]


class AssignOut(BaseModel):
    id: int
    status: str
    due_at: datetime | None = None


class MessageSentOut(BaseModel):
    id: int
    created_at: datetime


class StudentRefOut(BaseModel):
    id: int
    name: str | None = None
    email: str


class ReviewQueueItemOut(BaseModel):
    submission_id: int
    assignment_id: int
    assignment_title: str
    project: ProjectRefOut
    student: StudentRefOut
    is_gold: bool
    submitted_at: datetime | None = None
    payload: dict[str, Any]


class ReviewQueueOut(BaseModel):
    queue: list[ReviewQueueItemOut]


class ReviewOut(BaseModel):
    id: int
    submission_id: int
    verdict: str
    score: int | None = None
    gold_correct: bool | None = None


class StandardOut(BaseModel):
    id: int
    name: str
    pass_threshold: int
    rules: dict[str, Any] | None = None


__all__ = [
    "AssignOut",
    "AssignmentDetailOut",
    "AssignmentListOut",
    "AssignmentOut",
    "AssignmentStateOut",
    "AssignmentTaskOut",
    "CohortMemberOut",
    "CohortOut",
    "CohortWriteOut",
    "ConsequenceOut",
    "InviteListOut",
    "InviteOut",
    "InviteResponseOut",
    "LastSubmissionOut",
    "MessageListOut",
    "MessageSentOut",
    "ProjectListOut",
    "ProjectOut",
    "ProjectRefOut",
    "ProjectSummaryOut",
    "ProjectWriteOut",
    "QualityOut",
    "QualityRecordOut",
    "RemoveOut",
    "ReplacementListOut",
    "ReplacementOut",
    "ReviewOut",
    "ReviewQueueItemOut",
    "ReviewQueueOut",
    "StandardOut",
    "StudentRefOut",
    "SubmissionListOut",
    "SubmissionResultOut",
    "SubmissionSummaryOut",
    "SyncOut",
    "SyncResultOut",
    "WorkMessageOut",
]
