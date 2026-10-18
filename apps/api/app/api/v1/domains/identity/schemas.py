"""Identity contracts (the shapes the typed client is generated from)."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

PLATFORMS = ("web", "ios", "android", "admin")


class SignupIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    username: str = Field(min_length=3, max_length=40, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=10, max_length=200)
    name: str | None = Field(default=None, max_length=150)
    accept_terms: bool = False
    platform: str = "web"

    @field_validator("email")
    @classmethod
    def _looks_like_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("Enter a valid email address.")
        return value

    @field_validator("platform")
    @classmethod
    def _known_platform(cls, value: str) -> str:
        if value not in PLATFORMS:
            raise ValueError("Unknown platform.")
        return value


class LoginIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=200)
    platform: str = "web"

    @field_validator("platform")
    @classmethod
    def _known_platform(cls, value: str) -> str:
        if value not in PLATFORMS:
            raise ValueError("Unknown platform.")
        return value


class RefreshIn(BaseModel):
    # Native clients send the token; web and admin rely on the httpOnly cookie.
    refresh_token: str | None = Field(default=None, max_length=200)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    # Absent for cookie clients (web, admin): the token is in an httpOnly cookie.
    refresh_token: str | None = None


class MeOut(BaseModel):
    id: int
    email: str
    username: str
    name: str | None = None
    email_verified: bool
    role: str | None = None
    preferred_path: str | None = None


class VerifyEmailIn(BaseModel):
    token: str = Field(min_length=10, max_length=200)


class ResetRequestIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)


class ResetPasswordIn(BaseModel):
    token: str = Field(min_length=10, max_length=200)
    password: str = Field(min_length=10, max_length=200)


class GoogleIn(BaseModel):
    id_token: str = Field(min_length=10)
    platform: str = "ios"

    @field_validator("platform")
    @classmethod
    def _known_platform(cls, value: str) -> str:
        if value not in PLATFORMS:
            raise ValueError("Unknown platform.")
        return value


class ConsentIn(BaseModel):
    kind: str = Field(min_length=3, max_length=30)
    document_version: str = Field(min_length=1, max_length=20)
    granted: bool = True


class MessageOut(BaseModel):
    message: str


# --- profile, choose path and onboarding -------------------------------------


class ProfileUpdateIn(BaseModel):
    display_name: str | None = Field(default=None, max_length=150)
    bio: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=120)
    avatar_url: str | None = Field(default=None, max_length=1024)
    locale: str | None = Field(default=None, max_length=10)
    timezone: str | None = Field(default=None, max_length=64)
    notify_email: bool | None = None
    notify_push: bool | None = None
    profile_visibility: str | None = Field(default=None, max_length=16)
    date_of_birth: date | None = None


class ProfileOut(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    location: str | None = None
    avatar_url: str | None = None
    locale: str
    timezone: str | None = None
    preferred_path: str | None = None
    notify_email: bool
    notify_push: bool
    profile_visibility: str
    date_of_birth: date | None = None
    onboarding_completed_at: datetime | None = None


class PathIn(BaseModel):
    path: str = Field(min_length=5, max_length=16)


class LanguageIn(BaseModel):
    language: str = Field(min_length=1, max_length=60)
    level: str = Field(default="fluent", max_length=20)


class LanguagesIn(BaseModel):
    languages: list[LanguageIn] = Field(default_factory=list, max_length=20)


class AvailabilityIn(BaseModel):
    hours_per_week: int | None = Field(default=None, ge=0, le=168)
    available_from: date | None = None
    note: str | None = Field(default=None, max_length=255)


class EnrolIn(BaseModel):
    course_ids: list[int] = Field(min_length=1, max_length=30)
    session_id: int
    semester_id: int | None = None


class WaitlistIn(BaseModel):
    university_name: str = Field(min_length=2, max_length=200)
    email: str | None = Field(default=None, max_length=255)
    note: str | None = Field(default=None, max_length=500)


class UniversityOut(BaseModel):
    id: int
    name: str
    slug: str


class SubdivisionOut(BaseModel):
    id: int
    name: str


class CourseOut(BaseModel):
    id: int
    code: str
    title: str
    level: str


class SemesterOut(BaseModel):
    id: int
    name: str
    ordinal: int
    session_id: int


class EnrolmentOut(BaseModel):
    enrolment_id: int
    course_id: int
    code: str
    title: str
    level: str
    session_id: int
    semester_id: int | None
    status: str
    department: str
    faculty: str
    university: str


class OnboardingStateOut(BaseModel):
    profile_completed: bool
    has_enrolment: bool
    current_semester: SemesterOut | None = None
    academic: dict


# --- campus ----------------------------------------------------------------


class CampusUniversityOut(BaseModel):
    id: int
    name: str
    slug: str


class CampusItemOut(BaseModel):
    """A campus fact or map point. Coordinates are decimal degrees or absent."""

    id: int
    kind: str
    title: str
    body: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class CampusOut(BaseModel):
    university: CampusUniversityOut | None = None
    info: list[CampusItemOut]
    map: list[CampusItemOut]
