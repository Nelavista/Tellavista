"""Talent profile contracts (B13).

The profile is evidence, so every section names the row it came from rather than
accepting free text. Sections are optional because a share token is scoped: a
company that was not granted `quality` must not receive an empty object that
looks like "no quality history".

`headline` is present but always null until evidence supports one; keeping it in
the contract now means adding it later is not a breaking change.
"""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field

from app.api.v1.domains.verification.schemas import TranscriptOut
from app.services.talent.profile import DEFAULT_TTL_DAYS, MAX_TTL_DAYS


class TalentSkillOut(BaseModel):
    """One skill's evidence state. `current` means verified right now."""

    skill_id: int
    skill: str | None = None
    slug: str | None = None
    status: str
    verified_at: datetime | None = None
    at_risk: bool
    current: bool


class TalentAccountOut(BaseModel):
    """Internal ops view only; never part of a public share."""

    id: int
    email: str


class TalentAcademicOut(BaseModel):
    university: str | None = None
    department: str | None = None
    level: str | None = None


class TalentQualityOverallOut(BaseModel):
    reviews_count: int
    approvals: int
    average_score: int | None = None
    gold_tasks: int
    gold_correct: int


class TalentQualityProjectOut(BaseModel):
    project_id: int | None = None
    reviews_count: int
    average_score: int | None = None


class TalentQualityOut(BaseModel):
    overall: TalentQualityOverallOut | None = None
    by_project: list[TalentQualityProjectOut]


class TalentProjectRefOut(BaseModel):
    slug: str
    title: str


class TalentWorkEvidenceOut(BaseModel):
    type: str
    id: str


class TalentWorkHistoryOut(BaseModel):
    submission_id: int
    assignment: str
    project: TalentProjectRefOut
    approved_at: datetime | None = None
    evidence: TalentWorkEvidenceOut


class TalentProjectSummaryOut(BaseModel):
    project_id: int
    title: str
    slug: str
    approved_tasks: int


class TalentLanguageOut(BaseModel):
    language: str
    level: str


class TalentAvailabilityOut(BaseModel):
    hours_per_week: int | None = None
    available_from: date | None = None
    languages: list[TalentLanguageOut]
    location: str | None = None


class TalentProfileOut(BaseModel):
    """The evidence-only profile. Scoped sections are omitted, not blanked."""

    display_name: str | None = None
    headline: str | None = None
    visibility: str
    verified_skills: list[TalentSkillOut]
    all_skills: list[TalentSkillOut] | None = None
    evidence_only: bool
    account: TalentAccountOut | None = None
    transcript: TranscriptOut | None = None
    academic: TalentAcademicOut | None = None
    quality: TalentQualityOut | None = None
    work_history: list[TalentWorkHistoryOut] | None = None
    projects: list[TalentProjectSummaryOut] | None = None
    availability: TalentAvailabilityOut | None = None


class TalentTranscriptOut(BaseModel):
    transcript: TranscriptOut
    verified_skills: list[TalentSkillOut]


class ShareIn(BaseModel):
    label: str | None = Field(default=None, max_length=120)
    scopes: list[str] | None = None
    ttl_days: int = Field(default=DEFAULT_TTL_DAYS, ge=1, le=MAX_TTL_DAYS)


class ShareOut(BaseModel):
    id: int
    label: str | None = None
    scopes: list[str]
    expires_at: datetime
    revoked_at: datetime | None = None
    active: bool


class ShareListOut(BaseModel):
    shares: list[ShareOut]


class ShareCreatedOut(BaseModel):
    id: int
    label: str | None = None
    scopes: list[str]
    expires_at: datetime
    # Returned exactly once; only the hash is stored.
    token: str


class ShareRevokedOut(BaseModel):
    id: int
    revoked_at: datetime | None = None


__all__ = [
    "ShareCreatedOut",
    "ShareIn",
    "ShareListOut",
    "ShareOut",
    "ShareRevokedOut",
    "TalentAcademicOut",
    "TalentAccountOut",
    "TalentAvailabilityOut",
    "TalentLanguageOut",
    "TalentProfileOut",
    "TalentProjectRefOut",
    "TalentProjectSummaryOut",
    "TalentQualityOut",
    "TalentQualityOverallOut",
    "TalentQualityProjectOut",
    "TalentSkillOut",
    "TalentTranscriptOut",
    "TalentWorkEvidenceOut",
    "TalentWorkHistoryOut",
]
