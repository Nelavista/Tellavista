"""Rules-based matching with an explanation for every result (PRD §6).

Matching is not a job board, so a "no" is never a dead end. For every requirement
the engine records whether it is met and, when it is not, the learning path or
assessment that closes it. A mandatory miss makes the student ineligible; an
optional miss only lowers the score.

The candidate facts are real rows, not profile claims:

* verification status per skill (`verification_records`, only `verified` counts),
* languages and availability the student entered,
* university and department from their enrolments,
* rolling quality from `quality_records`, which is itself a projection of reviews.

Nothing here reads `LessonProgress`: watching lessons does not make anyone eligible.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import utcnow
from app.models.identity import User, UserAvailability, UserLanguage
from app.models.matching import (
    GAP_MISSING,
    OPPORTUNITY_MANAGED,
    REQUIREMENT_AVAILABILITY,
    REQUIREMENT_LANGUAGE,
    REQUIREMENT_LOCATION,
    REQUIREMENT_SKILL,
    REQUIREMENT_UNIVERSITY,
    REQUIREMENT_VERIFICATION,
    MatchResult,
    Opportunity,
    Requirement,
    SkillGap,
)
from app.models.quality import (
    CONSEQUENCE_REMOVE_FROM_PROJECT,
    CONSEQUENCE_RESTRICT_MATCHING,
    QualityConsequence,
    QualityRecord,
)
from app.models.skills import STATUS_PUBLISHED, LearningPath
from app.models.verification import (
    AT_RISK,
    VERIFIED,
    Assessment,
    VerificationRecord,
)
from app.services.identity.onboarding import academic_context

WEIGHT_MANDATORY = 2
WEIGHT_OPTIONAL = 1


def _norm(value: str | None) -> str:
    return (value or "").strip().lower()


def candidate_facts(db: Session, user: User) -> dict:
    records = db.scalars(
        select(VerificationRecord).where(VerificationRecord.user_id == user.id)
    ).all()
    statuses = {row.skill_id: row.status for row in records}
    languages = [
        _norm(row.language)
        for row in db.scalars(select(UserLanguage).where(UserLanguage.user_id == user.id)).all()
    ]
    availability = db.scalar(
        select(UserAvailability).where(UserAvailability.user_id == user.id)
    )
    quality = db.scalar(
        select(QualityRecord).where(
            QualityRecord.user_id == user.id, QualityRecord.project_id.is_(None)
        )
    )
    restriction = db.scalar(
        select(QualityConsequence)
        .where(
            QualityConsequence.user_id == user.id,
            QualityConsequence.active.is_(True),
            QualityConsequence.kind.in_(
                [CONSEQUENCE_RESTRICT_MATCHING, CONSEQUENCE_REMOVE_FROM_PROJECT]
            ),
        )
        .order_by(QualityConsequence.id.desc())
        .limit(1)
    )
    return {
        "user_id": user.id,
        "verification": statuses,
        "verified_skills": {sid for sid, status in statuses.items() if status == VERIFIED},
        "languages": set(languages),
        "hours_per_week": availability.hours_per_week if availability else None,
        "academic": academic_context(db, user),
        "location": _norm(user.profile.location if user.profile else None),
        "quality_score": quality.average_score if quality else None,
        "quality_reviewed": bool(quality and quality.reviews_count),
        "restricted": restriction is not None,
        "restriction_reason": restriction.reason if restriction else None,
    }


def _close_via(db: Session, skill_id: int | None) -> dict:
    if skill_id is None:
        return {}
    path = db.scalar(
        select(LearningPath)
        .where(LearningPath.skill_id == skill_id, LearningPath.status == STATUS_PUBLISHED)
        .order_by(LearningPath.id)
        .limit(1)
    )
    assessment = db.scalar(
        select(Assessment)
        .where(Assessment.skill_id == skill_id, Assessment.status == "published")
        .order_by(Assessment.id)
        .limit(1)
    )
    return {
        "learning_path_id": path.id if path else None,
        "learning_path_slug": path.slug if path else None,
        "assessment_id": assessment.id if assessment else None,
        "assessment_slug": assessment.slug if assessment else None,
    }


def evaluate_requirement(db: Session, facts: dict, requirement: Requirement) -> dict:
    kind = requirement.kind
    met = False
    detail = ""
    closes: dict = {}

    if kind == REQUIREMENT_SKILL:
        met = requirement.skill_id in facts["verified_skills"]
        detail = (
            "Skill verified."
            if met
            else "This skill is not verified yet."
        )
        closes = _close_via(db, requirement.skill_id)
    elif kind == REQUIREMENT_VERIFICATION:
        required = _norm(requirement.minimum_value) or VERIFIED
        current = facts["verification"].get(requirement.skill_id)
        met = current == VERIFIED or (required == AT_RISK and current in {VERIFIED, AT_RISK})
        detail = (
            f"Verification is {current}."
            if current
            else "No verification record for this skill yet."
        )
        closes = _close_via(db, requirement.skill_id)
    elif kind == REQUIREMENT_LANGUAGE:
        wanted = _norm(requirement.minimum_value)
        met = bool(wanted) and wanted in facts["languages"]
        detail = (
            f"Works in {requirement.minimum_value}."
            if met
            else f"Add {requirement.minimum_value} to your languages."
        )
    elif kind == REQUIREMENT_UNIVERSITY:
        wanted = _norm(requirement.minimum_value)
        current = _norm(facts["academic"].get("university"))
        met = bool(wanted) and wanted == current
        detail = (
            "University matches."
            if met
            else f"This opportunity is for {requirement.minimum_value} students."
        )
    elif kind == REQUIREMENT_AVAILABILITY:
        try:
            wanted_hours = int(requirement.minimum_value or 0)
        except (TypeError, ValueError):
            wanted_hours = 0
        have = facts["hours_per_week"]
        met = have is not None and have >= wanted_hours
        detail = (
            f"{have} hours a week available."
            if met
            else f"Set at least {wanted_hours} hours a week in your availability."
        )
    elif kind == REQUIREMENT_LOCATION:
        wanted = _norm(requirement.minimum_value)
        met = bool(wanted) and wanted in facts["location"]
        detail = (
            "Location matches."
            if met
            else f"This opportunity is based in {requirement.minimum_value}."
        )
    else:
        detail = "Unknown requirement."

    return {
        "requirement_id": requirement.id,
        "kind": kind,
        "description": requirement.description or requirement.minimum_value or kind,
        "skill_id": requirement.skill_id,
        "mandatory": requirement.is_mandatory,
        "met": met,
        "detail": detail,
        "closes_via": closes,
    }


def evaluate(db: Session, user: User, opportunity: Opportunity) -> dict:
    facts = candidate_facts(db, user)
    requirements = list(
        db.scalars(
            select(Requirement)
            .where(Requirement.opportunity_id == opportunity.id)
            .order_by(Requirement.id)
        ).all()
    )
    checks = [evaluate_requirement(db, facts, requirement) for requirement in requirements]

    mandatory = [check for check in checks if check["mandatory"]]
    eligible = all(check["met"] for check in mandatory)
    # A quality consequence is a block, not a preference: a student restricted from
    # matching must see why, not an empty list of opportunities.
    if facts["restricted"]:
        eligible = False

    weighted_total = sum(
        WEIGHT_MANDATORY if check["mandatory"] else WEIGHT_OPTIONAL for check in checks
    )
    weighted_met = sum(
        (WEIGHT_MANDATORY if check["mandatory"] else WEIGHT_OPTIONAL)
        for check in checks
        if check["met"]
    )
    base = round(100 * weighted_met / weighted_total) if weighted_total else 100

    # Quality is a matching factor, but it is never the only one: an unproven
    # student is not penalised for having no work history yet.
    if facts["quality_reviewed"] and facts["quality_score"] is not None:
        base = round(base * (0.7 + 0.3 * facts["quality_score"] / 100))
    score = max(0, min(100, base))

    missing = [check for check in checks if not check["met"]]
    return {
        "opportunity_id": opportunity.id,
        "user_id": user.id,
        "eligible": eligible,
        "score": score,
        "blocked": facts["restricted"],
        "blocked_reason": facts["restriction_reason"],
        "explanation": checks,
        "missing": missing,
        "qualifies_because": [check["detail"] for check in checks if check["met"]],
        "next_steps": [
            {
                "requirement_id": check["requirement_id"],
                "detail": check["detail"],
                "closes_via": check["closes_via"],
            }
            for check in missing
        ],
        "facts": {
            "university": facts["academic"].get("university"),
            "verified_skills": sorted(facts["verified_skills"]),
            "quality_score": facts["quality_score"],
        },
    }


def persist(db: Session, result: dict) -> MatchResult:
    row = db.scalar(
        select(MatchResult).where(
            MatchResult.opportunity_id == result["opportunity_id"],
            MatchResult.user_id == result["user_id"],
        )
    )
    if row is None:
        row = MatchResult(
            opportunity_id=result["opportunity_id"], user_id=result["user_id"]
        )
        db.add(row)
    row.eligible = result["eligible"]
    row.score = result["score"]
    row.explanation = result["explanation"]
    row.computed_at = utcnow()
    db.flush()

    for check in result["explanation"]:
        gap = db.scalar(
            select(SkillGap).where(
                SkillGap.user_id == result["user_id"],
                SkillGap.requirement_id == check["requirement_id"],
            )
        )
        if check["met"]:
            if gap is not None:
                db.delete(gap)
            continue
        closes = check["closes_via"] or {}
        if gap is None:
            gap = SkillGap(
                user_id=result["user_id"],
                opportunity_id=result["opportunity_id"],
                requirement_id=check["requirement_id"],
                status=GAP_MISSING,
            )
            db.add(gap)
        gap.status = GAP_MISSING
        gap.detail = check["detail"][:255]
        gap.closes_via_learning_path_id = closes.get("learning_path_id")
        gap.closes_via_assessment_id = closes.get("assessment_id")
    db.flush()
    return row


def match_user_to_opportunity(db: Session, user: User, opportunity: Opportunity) -> dict:
    result = evaluate(db, user, opportunity)
    persist(db, result)
    return result


def list_matches(db: Session, user: User) -> list[dict]:
    """Every open opportunity, evaluated for this student, with its reasons."""
    opportunities = db.scalars(
        select(Opportunity)
        .where(Opportunity.status == "open")
        .order_by(Opportunity.id.desc())
    ).all()
    results = [match_user_to_opportunity(db, user, opportunity) for opportunity in opportunities]
    results.sort(key=lambda item: (item["eligible"], item["score"]), reverse=True)
    return results


def match_candidates(db: Session, opportunity: Opportunity, *, limit: int = 200) -> list[dict]:
    """The ops view: who qualifies, and exactly why the rest do not."""
    users = db.scalars(
        select(User).where(User.is_deleted.is_(False)).order_by(User.id).limit(limit)
    ).all()
    results = []
    for user in users:
        result = evaluate(db, user, opportunity)
        if not result["explanation"]:
            # No requirements means everyone trivially qualifies; only include
            # students who have at least one piece of matching evidence.
            continue
        persist(db, result)
        results.append(result)
    results.sort(key=lambda item: (item["eligible"], item["score"]), reverse=True)
    return results


def gaps_for_user(db: Session, user_id: int, opportunity_id: int) -> list[dict]:
    rows = db.execute(
        select(SkillGap, Requirement)
        .join(Requirement, Requirement.id == SkillGap.requirement_id)
        .where(SkillGap.user_id == user_id, SkillGap.opportunity_id == opportunity_id)
        .order_by(SkillGap.id)
    ).all()
    return [
        {
            "requirement_id": requirement.id,
            "kind": requirement.kind,
            "detail": gap.detail,
            "status": gap.status,
            "closes_via": {
                "learning_path_id": gap.closes_via_learning_path_id,
                "assessment_id": gap.closes_via_assessment_id,
            },
        }
        for gap, requirement in rows
    ]


def is_managed(opportunity: Opportunity) -> bool:
    """The fee switch: only managed work can ever produce a ledger entry."""
    return opportunity.type == OPPORTUNITY_MANAGED


__all__ = [
    "candidate_facts",
    "evaluate",
    "gaps_for_user",
    "is_managed",
    "list_matches",
    "match_candidates",
    "match_user_to_opportunity",
    "persist",
]
