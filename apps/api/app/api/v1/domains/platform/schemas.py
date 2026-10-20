"""Contracts for the platform settings and work eligibility (G1–G5)."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class PlatformConfigOut(BaseModel):
    """What any signed-in client may read: currency and the rules it enforces."""

    billing_currency: str
    payout_currency: str
    allowed_currencies: list[str]
    min_student_age: int
    guardian_consent_below_age: int
    terms_version: str
    contributor_terms_version: str
    contributor_terms_body: str
    curriculum_owner: str
    curriculum_license: str
    curriculum_authoring_model: str
    target_launch_date: date | None = None
    updated_at: datetime | None = None


class PlatformSettingsOut(PlatformConfigOut):
    """The staff view: adds the payout approval and identity switches."""

    id: int
    payout_second_approver_threshold_minor: int
    payout_second_approver_always: bool
    payout_require_verified_email: bool
    updated_by: int | None = None


class PlatformSettingsIn(BaseModel):
    """A partial update. Validation lives in the service so every caller agrees."""

    billing_currency: str | None = Field(default=None, min_length=3, max_length=3)
    payout_currency: str | None = Field(default=None, min_length=3, max_length=3)
    allowed_currencies: list[str] | None = None
    payout_second_approver_threshold_minor: int | None = Field(default=None, ge=0)
    payout_second_approver_always: bool | None = None
    payout_require_verified_email: bool | None = None
    min_student_age: int | None = Field(default=None, ge=13, le=25)
    guardian_consent_below_age: int | None = Field(default=None, ge=13, le=25)
    terms_version: str | None = Field(default=None, max_length=20)
    contributor_terms_version: str | None = Field(default=None, max_length=20)
    contributor_terms_body: str | None = Field(default=None, max_length=20_000)
    curriculum_owner: str | None = Field(default=None, max_length=160)
    curriculum_license: str | None = Field(default=None, max_length=80)
    curriculum_authoring_model: str | None = Field(default=None, max_length=40)
    target_launch_date: date | None = None

    def changes(self) -> dict:
        """Only the fields the client actually sent (null is meaningful for a date)."""
        return self.model_dump(exclude_unset=True)


class EligibilityOut(BaseModel):
    eligible: bool
    blockers: list[str]
    reasons: list[str]
    age: int | None = None
    min_student_age: int
    guardian_consent_below_age: int
    contributor_terms_version: str
    contributor_terms_body: str


class ConsentIn(BaseModel):
    kind: str = Field(min_length=3, max_length=30)
    document_version: str = Field(min_length=1, max_length=20)
    granted: bool = True


class ConsentOut(BaseModel):
    id: int
    kind: str
    document_version: str
    granted: bool
    created_at: datetime


class ConsentListOut(BaseModel):
    consents: list[ConsentOut]


__all__ = [
    "ConsentIn",
    "ConsentListOut",
    "ConsentOut",
    "EligibilityOut",
    "PlatformConfigOut",
    "PlatformSettingsIn",
    "PlatformSettingsOut",
]
