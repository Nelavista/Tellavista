"""Profile, Choose Path and the student's own data (PRD §2, §14; ADR-0009).

One identity means one profile: the path a student picked is a preference, not a
second account. Switching path is allowed at any time and never deletes learning,
verification or earnings.

The data export and deletion hooks here exist because the app stores require
in-app deletion. Deletion itself anonymises in `identity.auth`; this module builds
the export.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.academia import Enrolment
from app.models.identity import Consent, User, UserAvailability, UserLanguage, UserProfile
from app.models.ledger import EarningLine
from app.models.quality import QualityRecord
from app.models.skills import LessonProgress, PracticeAttempt
from app.models.talent import OpportunityApplication, TalentShare
from app.models.verification import (
    AssessmentAttempt,
    PracticalSubmission,
    TranscriptEntry,
    VerificationRecord,
)

PATHS: tuple[str, ...] = ("academia", "skills")
VISIBILITIES: tuple[str, ...] = ("private", "link", "public")
LANGUAGE_LEVELS: tuple[str, ...] = ("basic", "conversational", "fluent", "native")


def get_or_create_profile(db: Session, user: User) -> UserProfile:
    if user.profile is not None:
        return user.profile
    profile = UserProfile(user_id=user.id, display_name=user.name or user.username)
    db.add(profile)
    db.flush()
    return profile


def update_profile(
    db: Session,
    user: User,
    *,
    display_name: str | None = None,
    bio: str | None = None,
    location: str | None = None,
    avatar_url: str | None = None,
    locale: str | None = None,
    timezone: str | None = None,
    notify_email: bool | None = None,
    notify_push: bool | None = None,
    profile_visibility: str | None = None,
    date_of_birth: date | None = None,
) -> UserProfile:
    profile = get_or_create_profile(db, user)

    if profile_visibility is not None:
        if profile_visibility not in VISIBILITIES:
            raise ApiError(400, "invalid_visibility", "Choose private, link or public.")
        profile.profile_visibility = profile_visibility

    if display_name is not None:
        cleaned = display_name.strip()
        if not cleaned:
            raise ApiError(400, "invalid_display_name", "Display name cannot be empty.")
        profile.display_name = cleaned[:150]
    if bio is not None:
        profile.bio = bio.strip()[:500] or None
    if location is not None:
        profile.location = location.strip()[:120] or None
    if avatar_url is not None:
        profile.avatar_url = avatar_url[:1024] or None
    if locale is not None:
        profile.locale = locale[:10]
    if timezone is not None:
        profile.timezone = timezone[:64] or None
    if notify_email is not None:
        profile.notify_email = notify_email
    if notify_push is not None:
        profile.notify_push = notify_push
    if date_of_birth is not None:
        if date_of_birth > utcnow().date():
            raise ApiError(400, "invalid_date_of_birth", "Date of birth cannot be in the future.")
        profile.date_of_birth = date_of_birth

    db.flush()
    return profile


def choose_path(db: Session, user: User, path: str) -> UserProfile:
    """Set or switch the student's path. Switching never deletes anything."""
    if path not in PATHS:
        raise ApiError(400, "invalid_path", "Choose academia or skills.")
    profile = get_or_create_profile(db, user)
    profile.preferred_path = path
    db.flush()
    return profile


def complete_onboarding(db: Session, user: User) -> UserProfile:
    profile = get_or_create_profile(db, user)
    profile.onboarding_completed_at = utcnow()
    db.flush()
    return profile


def set_languages(db: Session, user: User, languages: list[tuple[str, str]]) -> list[UserLanguage]:
    """Replace the student's languages. Duplicates are rejected, not silently merged."""
    seen: set[str] = set()
    cleaned: list[tuple[str, str]] = []
    for language, level in languages:
        name = language.strip()
        if not name:
            raise ApiError(400, "invalid_language", "Language cannot be empty.")
        key = name.lower()
        if key in seen:
            raise ApiError(400, "duplicate_language", f"{name} is listed twice.")
        if level not in LANGUAGE_LEVELS:
            raise ApiError(400, "invalid_language_level", "Unknown language level.")
        seen.add(key)
        cleaned.append((name[:60], level))

    for row in db.scalars(select(UserLanguage).where(UserLanguage.user_id == user.id)):
        db.delete(row)
    db.flush()

    rows = [UserLanguage(user_id=user.id, language=name, level=level) for name, level in cleaned]
    db.add_all(rows)
    db.flush()
    return rows


def set_availability(
    db: Session,
    user: User,
    *,
    hours_per_week: int | None,
    available_from: date | None,
    note: str | None,
) -> UserAvailability:
    if hours_per_week is not None and not (0 <= hours_per_week <= 168):
        raise ApiError(400, "invalid_hours", "Hours per week must be between 0 and 168.")
    row = db.scalar(select(UserAvailability).where(UserAvailability.user_id == user.id))
    if row is None:
        row = UserAvailability(user_id=user.id)
        db.add(row)
    row.hours_per_week = hours_per_week
    row.available_from = available_from
    row.note = (note or "")[:255] or None
    db.flush()
    return row


def export_data(db: Session, user: User) -> dict:
    """Everything V2 holds about one student, for a data export request.

    Money and audit evidence is included because the student is entitled to know
    what was earned and why; other people's notes are never included.
    """
    profile = user.profile
    enrolments = db.scalars(select(Enrolment).where(Enrolment.user_id == user.id)).all()
    lessons = db.scalars(select(LessonProgress).where(LessonProgress.user_id == user.id)).all()
    practice = db.scalars(select(PracticeAttempt).where(PracticeAttempt.user_id == user.id)).all()
    verifications = db.scalars(
        select(VerificationRecord).where(VerificationRecord.user_id == user.id)
    ).all()
    transcript = db.scalars(select(TranscriptEntry).where(TranscriptEntry.user_id == user.id)).all()
    assessments = db.scalars(
        select(AssessmentAttempt).where(AssessmentAttempt.user_id == user.id)
    ).all()
    practicals = db.scalars(
        select(PracticalSubmission).where(PracticalSubmission.user_id == user.id)
    ).all()
    earnings = db.scalars(select(EarningLine).where(EarningLine.user_id == user.id)).all()
    quality = db.scalars(select(QualityRecord).where(QualityRecord.user_id == user.id)).all()
    applications = db.scalars(
        select(OpportunityApplication).where(OpportunityApplication.user_id == user.id)
    ).all()
    consents = db.scalars(select(Consent).where(Consent.user_id == user.id)).all()
    shares = db.scalars(select(TalentShare).where(TalentShare.user_id == user.id)).all()
    languages = db.scalars(select(UserLanguage).where(UserLanguage.user_id == user.id)).all()
    availability = db.scalar(
        select(UserAvailability).where(UserAvailability.user_id == user.id)
    )

    return {
        "account": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "name": user.name,
            "email_verified": user.email_verified,
            "created_at": user.created_at,
        },
        "profile": {
            "display_name": profile.display_name if profile else None,
            "bio": profile.bio if profile else None,
            "location": profile.location if profile else None,
            "locale": profile.locale if profile else None,
            "preferred_path": profile.preferred_path if profile else None,
            "profile_visibility": profile.profile_visibility if profile else "private",
        },
        "languages": [{"language": row.language, "level": row.level} for row in languages],
        "availability": (
            {
                "hours_per_week": availability.hours_per_week,
                "available_from": availability.available_from,
            }
            if availability
            else None
        ),
        "enrolments": [
            {"course_id": row.course_id, "session_id": row.session_id, "status": row.status}
            for row in enrolments
        ],
        "lesson_progress": [
            {"lesson_id": row.lesson_id, "status": row.status, "completed_at": row.completed_at}
            for row in lessons
        ],
        "practice_attempts": [
            {"template_id": row.template_id, "is_correct": row.is_correct} for row in practice
        ],
        "verification": [
            {"skill_id": row.skill_id, "status": row.status, "verified_at": row.verified_at}
            for row in verifications
        ],
        "transcript": [
            {
                "kind": row.kind,
                "title": row.title,
                "skill_id": row.skill_id,
                "occurred_at": row.occurred_at,
            }
            for row in transcript
        ],
        "assessments": [
            {"assessment_id": row.assessment_id, "score": row.score, "passed": row.passed}
            for row in assessments
        ],
        "practical_submissions": [
            {"practical_task_id": row.practical_task_id, "score": row.score, "passed": row.passed}
            for row in practicals
        ],
        "earnings": [
            {
                "project_id": row.project_id,
                "amount_minor": row.amount_minor,
                "currency": row.currency,
                "status": row.status,
            }
            for row in earnings
        ],
        "quality": [
            {
                "project_id": row.project_id,
                "average_score": row.average_score,
                "reviews_count": row.reviews_count,
            }
            for row in quality
        ],
        "applications": [
            {"opportunity_id": row.opportunity_id, "status": row.status} for row in applications
        ],
        "consents": [
            {
                "kind": row.kind,
                "document_version": row.document_version,
                "granted": row.granted,
                "created_at": row.created_at,
            }
            for row in consents
        ],
        "talent_shares": [
            {"label": row.label, "expires_at": row.expires_at, "revoked_at": row.revoked_at}
            for row in shares
        ],
    }
