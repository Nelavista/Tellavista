"""Talent profile: evidence, not claims (PRD §7).

The profile is computed on read from rows that already carry evidence:

* `verification_records` — which skills are verified, and current state,
* `transcript_entries` — what was learned, proved and delivered,
* approved `submissions` — work history, each tied to a project and review,
* `quality_records` — the rolling quality history,
* enrolments, languages and availability — academic context and capacity.

A student can publish it to a company through a scoped, expiring, revocable link.
Only a hash of the link token is stored. Visibility is opt-in: `private` means no
external view exists at all.
"""
from __future__ import annotations

import secrets
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.security import hash_token
from app.core.time import as_utc, utcnow
from app.models.identity import User, UserAvailability, UserLanguage
from app.models.quality import QualityRecord
from app.models.skills import Skill
from app.models.talent import TalentShare
from app.models.verification import (
    AT_RISK,
    VERIFIED,
    VerificationRecord,
)
from app.models.work import (
    SUBMISSION_APPROVED,
    Assignment,
    Project,
    Submission,
)
from app.services import audit
from app.services.identity.onboarding import academic_context
from app.services.verification.transcript import get_transcript

DEFAULT_TTL_DAYS = 30
MAX_TTL_DAYS = 90
SHARE_SCOPES: tuple[str, ...] = (
    "academic",
    "transcript",
    "quality",
    "work_history",
    "availability",
)


def _skills(db: Session) -> dict[int, Skill]:
    return {skill.id: skill for skill in db.scalars(select(Skill)).all()}


def _verification(db: Session, user_id: int, skills: dict[int, Skill]) -> list[dict]:
    rows = db.scalars(
        select(VerificationRecord)
        .where(VerificationRecord.user_id == user_id)
        .order_by(VerificationRecord.id)
    ).all()
    return [
        {
            "skill_id": row.skill_id,
            "skill": skills[row.skill_id].name if row.skill_id in skills else None,
            "slug": skills[row.skill_id].slug if row.skill_id in skills else None,
            "status": row.status,
            "verified_at": row.verified_at,
            "at_risk": row.status == AT_RISK,
            "current": row.status == VERIFIED,
        }
        for row in rows
    ]


def _work_history(db: Session, user_id: int) -> list[dict]:
    rows = db.execute(
        select(Submission, Assignment, Project)
        .join(Assignment, Assignment.id == Submission.assignment_id)
        .join(Project, Project.id == Assignment.project_id)
        .where(Submission.user_id == user_id, Submission.status == SUBMISSION_APPROVED)
        .order_by(Submission.id.desc())
    ).all()
    return [
        {
            "submission_id": submission.id,
            "assignment": assignment.title,
            "project": {"slug": project.slug, "title": project.title},
            "approved_at": submission.updated_at,
            "evidence": {"type": "submission", "id": submission.id},
        }
        for submission, assignment, project in rows
    ]


def _quality(db: Session, user_id: int) -> dict:
    rows = db.scalars(
        select(QualityRecord)
        .where(QualityRecord.user_id == user_id)
        .order_by(QualityRecord.project_id.is_(None).desc(), QualityRecord.id)
    ).all()
    overall = next((row for row in rows if row.project_id is None), None)
    return {
        "overall": (
            {
                "reviews_count": overall.reviews_count,
                "approvals": overall.approvals,
                "average_score": overall.average_score,
                "gold_tasks": overall.gold_tasks,
                "gold_correct": overall.gold_correct,
            }
            if overall
            else None
        ),
        "by_project": [
            {
                "project_id": row.project_id,
                "reviews_count": row.reviews_count,
                "average_score": row.average_score,
            }
            for row in rows
            if row.project_id is not None
        ],
    }


def _availability(db: Session, user: User) -> dict:
    row = db.scalar(select(UserAvailability).where(UserAvailability.user_id == user.id))
    languages = db.scalars(
        select(UserLanguage).where(UserLanguage.user_id == user.id).order_by(UserLanguage.language)
    ).all()
    return {
        "hours_per_week": row.hours_per_week if row else None,
        "available_from": row.available_from if row else None,
        "languages": [{"language": item.language, "level": item.level} for item in languages],
        "location": user.profile.location if user.profile else None,
    }


def build_profile(
    db: Session,
    user: User,
    *,
    scopes: list[str] | None = None,
    internal: bool = False,
    via_share: bool = False,
) -> dict:
    """Compose the profile from evidence.

    `via_share` is the consent exception: a live, scoped share token *is* the
    student's permission, so it works even while the general profile visibility is
    `private` (the student shared one link, not their whole profile).
    """
    chosen = set(scopes or SHARE_SCOPES)
    unknown = chosen - set(SHARE_SCOPES)
    if unknown:
        raise ApiError(400, "unknown_scope", "Unknown profile scope.", {"scopes": sorted(unknown)})

    skills = _skills(db)
    profile = user.profile
    visibility = profile.profile_visibility if profile else "private"
    if not internal and not via_share and visibility == "private":
        raise ApiError(403, "profile_private", "This student has not shared their profile.")

    body: dict = {
        "display_name": profile.display_name if profile else None,
        "headline": None,
        "visibility": visibility,
        "verified_skills": [
            item
            for item in _verification(db, user.id, skills)
            if item["status"] in {VERIFIED, AT_RISK}
        ],
        "all_skills": _verification(db, user.id, skills) if internal else None,
        "evidence_only": True,
    }
    if internal:
        body["account"] = {"id": user.id, "email": user.email}

    if "transcript" in chosen:
        body["transcript"] = get_transcript(db, user)
    if "academic" in chosen:
        context = academic_context(db, user)
        # The internal view may include contact details; an external one only the
        # academic facts the student agreed to share.
        body["academic"] = {
            "university": context["university"],
            "department": context["department"],
            "level": context["level"],
        }
    if "quality" in chosen:
        body["quality"] = _quality(db, user.id)
    if "work_history" in chosen:
        body["work_history"] = _work_history(db, user.id)
        body["projects"] = _project_summary(db, user.id)
    if "availability" in chosen:
        body["availability"] = _availability(db, user)
    return body


def _project_summary(db: Session, user_id: int) -> list[dict]:
    rows = db.execute(
        select(Project.id, Project.title, Project.slug, func.count(Submission.id))
        .join(Assignment, Assignment.project_id == Project.id)
        .join(Submission, Submission.assignment_id == Assignment.id)
        .where(Submission.user_id == user_id, Submission.status == SUBMISSION_APPROVED)
        .group_by(Project.id, Project.title, Project.slug)
        .order_by(Project.id.desc())
    ).all()
    return [
        {"project_id": project_id, "title": title, "slug": slug, "approved_tasks": count}
        for project_id, title, slug, count in rows
    ]


def create_share(
    db: Session,
    user: User,
    *,
    label: str | None,
    scopes: list[str] | None,
    ttl_days: int = DEFAULT_TTL_DAYS,
) -> tuple[TalentShare, str]:
    if not (1 <= ttl_days <= MAX_TTL_DAYS):
        raise ApiError(400, "invalid_ttl", f"Share links last 1-{MAX_TTL_DAYS} days.")
    chosen = scopes or list(SHARE_SCOPES)
    unknown = set(chosen) - set(SHARE_SCOPES)
    if unknown:
        raise ApiError(400, "unknown_scope", "Unknown profile scope.", {"scopes": sorted(unknown)})

    raw = secrets.token_urlsafe(32)
    share = TalentShare(
        user_id=user.id,
        token_hash=hash_token(raw),
        label=(label or "")[:120] or None,
        scopes=chosen,
        expires_at=utcnow() + timedelta(days=ttl_days),
    )
    db.add(share)
    db.flush()
    audit.record(
        db,
        action="talent.share_created",
        actor_user_id=user.id,
        target_type="talent_share",
        target_id=share.id,
        context={"scopes": chosen, "expires_at": share.expires_at.isoformat()},
    )
    return share, raw


def revoke_share(db: Session, user: User, share_id: int) -> TalentShare:
    share = db.get(TalentShare, share_id)
    if share is None or share.user_id != user.id:
        raise ApiError(404, "share_not_found", "That share link does not exist.")
    if share.revoked_at is None:
        share.revoked_at = utcnow()
        db.flush()
        audit.record(
            db,
            action="talent.share_revoked",
            actor_user_id=user.id,
            target_type="talent_share",
            target_id=share.id,
        )
    return share


def view_share(db: Session, raw_token: str) -> dict:
    share = db.scalar(select(TalentShare).where(TalentShare.token_hash == hash_token(raw_token)))
    if share is None or share.revoked_at is not None:
        raise ApiError(404, "share_not_found", "This link is no longer active.")
    if as_utc(share.expires_at) <= utcnow():
        raise ApiError(410, "share_expired", "This link has expired.")
    user = db.get(User, share.user_id)
    if user is None or user.is_deleted:
        raise ApiError(404, "share_not_found", "This link is no longer active.")
    share.last_viewed_at = utcnow()
    db.flush()
    return build_profile(db, user, scopes=share.scopes, via_share=True)


def list_shares(db: Session, user: User) -> list[dict]:
    rows = db.scalars(
        select(TalentShare)
        .where(TalentShare.user_id == user.id)
        .order_by(TalentShare.id.desc())
    ).all()
    return [
        {
            "id": row.id,
            "label": row.label,
            "scopes": row.scopes,
            "expires_at": row.expires_at,
            "revoked_at": row.revoked_at,
            "active": row.revoked_at is None and as_utc(row.expires_at) > utcnow(),
        }
        for row in rows
    ]


def transcript_only(db: Session, user: User) -> dict:
    return {
        "transcript": get_transcript(db, user),
        "verified_skills": [
            item
            for item in _verification(db, user.id, _skills(db))
            if item["status"] == VERIFIED
        ],
    }


__all__ = [
    "DEFAULT_TTL_DAYS",
    "MAX_TTL_DAYS",
    "SHARE_SCOPES",
    "build_profile",
    "create_share",
    "list_shares",
    "revoke_share",
    "transcript_only",
    "view_share",
]
