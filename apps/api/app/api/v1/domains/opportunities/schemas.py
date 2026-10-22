"""Opportunity and matching contracts (B8, C4).

The student screen and the ops candidate list read the same explanation: a
verdict without a reason is a support ticket. `MatchCheckOut` is that reason in
one shape, so "why you qualify" and "what is missing" can never disagree.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class ClosesViaOut(BaseModel):
    learning_path_id: int | None = None
    assessment_id: int | None = None


class RequirementOut(BaseModel):
    id: int
    kind: str
    skill_id: int | None = None
    minimum_value: str | None = None
    is_mandatory: bool
    description: str | None = None


class MatchCheckOut(BaseModel):
    requirement_id: int
    kind: str
    description: str
    skill_id: int | None = None
    mandatory: bool
    met: bool
    detail: str
    closes_via: ClosesViaOut


class NextStepOut(BaseModel):
    requirement_id: int
    detail: str
    closes_via: ClosesViaOut


class MatchOut(BaseModel):
    """One student's verdict on one opportunity, with every requirement.

    `blocked` is not a preference: a quality consequence stops matching and the
    screen must say so instead of showing an empty list.
    """

    opportunity_id: int
    user_id: int
    eligible: bool
    score: int
    blocked: bool = False
    blocked_reason: str | None = None
    explanation: list[MatchCheckOut] = []
    missing: list[MatchCheckOut] = []
    qualifies_because: list[str] = []
    next_steps: list[NextStepOut] = []
    facts: dict[str, Any] = {}


class OpportunityMatchOut(BaseModel):
    """The summary embedded in an opportunity card (a subset of MatchOut)."""

    eligible: bool
    score: int
    explanation: list[MatchCheckOut] = []
    next_steps: list[NextStepOut] = []
    qualifies_because: list[str] = []


class OpportunityOut(BaseModel):
    id: int
    slug: str
    type: str
    title: str
    description: str
    client_name: str | None = None
    headcount: int | None = None
    status: str
    currency: str | None = None
    rate_minor: int | None = None
    starts_on: date | None = None
    ends_on: date | None = None
    requirements: list[RequirementOut]
    match: OpportunityMatchOut


class OpportunityListOut(BaseModel):
    opportunities: list[OpportunityOut]


class MatchListOut(BaseModel):
    matches: list[MatchOut]
    eligible_count: int


class ApplicationOpportunityOut(BaseModel):
    id: int
    slug: str
    title: str
    type: str


class ApplicationOut(BaseModel):
    id: int
    status: str
    note: str | None = None
    opportunity: ApplicationOpportunityOut


class ApplicationListOut(BaseModel):
    applications: list[ApplicationOut]


class ApplyOut(BaseModel):
    id: int
    status: str
    note: str | None = None


class GapOut(BaseModel):
    requirement_id: int
    kind: str
    detail: str
    status: str
    closes_via: ClosesViaOut


class GapListOut(BaseModel):
    gaps: list[GapOut]


class OpportunityRefOut(BaseModel):
    id: int
    slug: str
    title: str | None = None


class ApplicationSummaryOut(BaseModel):
    id: int
    status: str
    user_id: int
    note: str | None = None


class OpportunityApplicationsOut(BaseModel):
    opportunity: OpportunityRefOut
    applications: list[ApplicationSummaryOut]


class ApplicationStatusOut(BaseModel):
    id: int
    status: str


class OpportunityWriteOut(BaseModel):
    id: int
    slug: str
    status: str


class CandidateListOut(BaseModel):
    opportunity: OpportunityRefOut
    # `CandidateOut`, not `MatchOut`: the ops list has to name the student, and a
    # response model that drops the field silently is worse than no model at all.
    # Forward reference: CandidateOut is defined below, so it is rebuilt after.
    candidates: list[CandidateOut]
    eligible_count: int


class OpportunityAdminRowOut(BaseModel):
    """One row for the ops list. Drafts and closed rows are included on purpose."""

    id: int
    slug: str
    type: str
    title: str
    client_name: str | None = None
    status: str
    headcount: int | None = None
    currency: str | None = None
    rate_minor: int | None = None


class OpportunityAdminListOut(BaseModel):
    opportunities: list[OpportunityAdminRowOut]


class CandidateNameOut(BaseModel):
    id: int
    name: str | None = None
    email: str


class CandidateOut(BaseModel):
    """Ops view of one student: the verdict plus who it is about."""

    opportunity_id: int
    user_id: int
    eligible: bool
    score: int
    blocked: bool = False
    blocked_reason: str | None = None
    explanation: list[MatchCheckOut] = []
    missing: list[MatchCheckOut] = []
    qualifies_because: list[str] = []
    next_steps: list[NextStepOut] = []
    facts: dict[str, Any] = {}
    student: CandidateNameOut | None = None
    computed_at: datetime | None = None


CandidateListOut.model_rebuild()


__all__ = [
    "ApplicationListOut",
    "ApplicationOpportunityOut",
    "ApplicationOut",
    "ApplicationStatusOut",
    "ApplicationSummaryOut",
    "ApplyOut",
    "CandidateListOut",
    "CandidateOut",
    "CandidateNameOut",
    "CandidateOut",
    "ClosesViaOut",
    "GapListOut",
    "GapOut",
    "MatchCheckOut",
    "MatchListOut",
    "MatchOut",
    "NextStepOut",
    "OpportunityAdminListOut",
    "OpportunityAdminRowOut",
    "OpportunityApplicationsOut",
    "OpportunityListOut",
    "OpportunityMatchOut",
    "OpportunityOut",
    "OpportunityRefOut",
    "OpportunityWriteOut",
    "RequirementOut",
]
