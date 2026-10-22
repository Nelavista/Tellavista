"""Platform policy: read, validate and enforce G1–G5.

The settings row is data, but the *rules* that read it live here so every caller
gets the same answer:

* funding uses the configured billing currency,
* a payout batch above the configured threshold needs a second approver,
* a student cannot accept paid work until their age and the contributor terms
  are on record (guardian consent below the configured age),
* a payout is blocked when the recipient fails the configured identity checks.

Validation is deliberately strict and centralised: the admin form can send any
subset of fields, and an invalid value is rejected with a field name rather than
saved and discovered later by a worker.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.identity import CONSENT_KINDS, Consent, User
from app.models.platform import (
    DEFAULT_ALLOWED_CURRENCIES,
    DEFAULT_BILLING_CURRENCY,
    DEFAULT_CONTRIBUTOR_TERMS,
    DEFAULT_CONTRIBUTOR_TERMS_VERSION,
    DEFAULT_CURRICULUM_LICENSE,
    DEFAULT_CURRICULUM_OWNER,
    DEFAULT_GUARDIAN_CONSENT_BELOW_AGE,
    DEFAULT_MIN_STUDENT_AGE,
    DEFAULT_PAYOUT_CURRENCY,
    DEFAULT_SECOND_APPROVER_THRESHOLD_MINOR,
    DEFAULT_TERMS_VERSION,
    SETTINGS_ID,
    PlatformSettings,
)
from app.services import audit

CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
AUTHORING_MODELS: tuple[str, ...] = ("in_house", "community", "partner")

# The fields an admin may change. Anything else in a PATCH is a mistake, not a
# silent no-op.
EDITABLE_FIELDS: tuple[str, ...] = (
    "billing_currency",
    "payout_currency",
    "allowed_currencies",
    "payout_second_approver_threshold_minor",
    "payout_second_approver_always",
    "payout_require_verified_email",
    "min_student_age",
    "guardian_consent_below_age",
    "terms_version",
    "contributor_terms_version",
    "contributor_terms_body",
    "curriculum_owner",
    "curriculum_license",
    "curriculum_authoring_model",
    "target_launch_date",
)


def _defaults() -> dict[str, Any]:
    return {
        "billing_currency": DEFAULT_BILLING_CURRENCY,
        "payout_currency": DEFAULT_PAYOUT_CURRENCY,
        "allowed_currencies": list(DEFAULT_ALLOWED_CURRENCIES),
        "payout_second_approver_threshold_minor": DEFAULT_SECOND_APPROVER_THRESHOLD_MINOR,
        "payout_second_approver_always": False,
        "payout_require_verified_email": True,
        "min_student_age": DEFAULT_MIN_STUDENT_AGE,
        "guardian_consent_below_age": DEFAULT_GUARDIAN_CONSENT_BELOW_AGE,
        "terms_version": DEFAULT_TERMS_VERSION,
        "contributor_terms_version": DEFAULT_CONTRIBUTOR_TERMS_VERSION,
        "contributor_terms_body": DEFAULT_CONTRIBUTOR_TERMS,
        "curriculum_owner": DEFAULT_CURRICULUM_OWNER,
        "curriculum_license": DEFAULT_CURRICULUM_LICENSE,
        "curriculum_authoring_model": "in_house",
        "target_launch_date": None,
    }


def get_platform_settings(db: Session) -> PlatformSettings:
    """Return the single settings row, creating it with defaults on first read.

    Creating on read (rather than only in a data migration) means a database that
    was restored from before this table existed still boots with the documented
    defaults instead of failing every money and work request.
    """
    row = db.get(PlatformSettings, SETTINGS_ID)
    if row is None:
        row = PlatformSettings(id=SETTINGS_ID, **_defaults())
        db.add(row)
        db.flush()
    return row


def _currency(value: str, field: str) -> str:
    cleaned = (value or "").strip().upper()
    if not CURRENCY_RE.match(cleaned):
        raise ApiError(
            400, "invalid_currency", "Use a three-letter currency code such as NGN.", {"field": field}
        )
    return cleaned


def _validate(changes: dict[str, Any], current: PlatformSettings) -> dict[str, Any]:
    unknown = set(changes) - set(EDITABLE_FIELDS)
    if unknown:
        raise ApiError(
            400, "unknown_setting", "That setting cannot be changed.", {"fields": sorted(unknown)}
        )
    if not changes:
        raise ApiError(400, "no_changes", "Send at least one setting to change.")

    clean: dict[str, Any] = dict(changes)

    allowed = changes.get("allowed_currencies", current.allowed_currencies)
    if not isinstance(allowed, list) or not allowed:
        raise ApiError(
            400,
            "invalid_setting",
            "At least one currency must be allowed.",
            {"field": "allowed_currencies"},
        )
    allowed = [_currency(str(code), "allowed_currencies") for code in allowed]
    allowed = list(dict.fromkeys(allowed))
    if "allowed_currencies" in clean:
        clean["allowed_currencies"] = allowed

    for field in ("billing_currency", "payout_currency"):
        if field in clean:
            clean[field] = _currency(clean[field], field)

    effective_billing = clean.get("billing_currency", current.billing_currency)
    effective_payout = clean.get("payout_currency", current.payout_currency)
    # A currency must be allowed before it can be selected. The error names both
    # fields so the admin can fix the form in one pass.
    missing = [
        code for code in (effective_billing, effective_payout) if code not in allowed
    ]
    if missing:
        raise ApiError(
            400,
            "currency_not_allowed",
            "Add the currency to the allowed list before selecting it.",
            {"currencies": missing, "field": "allowed_currencies"},
        )

    threshold = changes.get(
        "payout_second_approver_threshold_minor",
        current.payout_second_approver_threshold_minor,
    )
    if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 0:
        raise ApiError(
            400,
            "invalid_setting",
            "The second-approver threshold must be zero or more minor units.",
            {"field": "payout_second_approver_threshold_minor"},
        )
    if threshold > 10**12:
        raise ApiError(
            400,
            "invalid_setting",
            "That threshold is larger than the ledger allows.",
            {"field": "payout_second_approver_threshold_minor"},
        )

    min_age = changes.get("min_student_age", current.min_student_age)
    guardian_age = changes.get("guardian_consent_below_age", current.guardian_consent_below_age)
    if not isinstance(min_age, int) or isinstance(min_age, bool) or not 13 <= min_age <= 25:
        raise ApiError(
            400, "invalid_setting", "The minimum age must be between 13 and 25.", {"field": "min_student_age"}
        )
    if (
        not isinstance(guardian_age, int)
        or isinstance(guardian_age, bool)
        or not min_age <= guardian_age <= 25
    ):
        raise ApiError(
            400,
            "invalid_setting",
            "The guardian-consent age must be at or above the minimum age, and at most 25.",
            {"field": "guardian_consent_below_age"},
        )

    for field in ("terms_version", "contributor_terms_version"):
        if field in clean:
            value = str(clean[field]).strip()
            if not 1 <= len(value) <= 20:
                raise ApiError(
                    400, "invalid_setting", "A terms version is 1–20 characters.", {"field": field}
                )
            clean[field] = value

    if "contributor_terms_body" in clean:
        body = str(clean["contributor_terms_body"]).strip()
        if not 20 <= len(body) <= 20_000:
            raise ApiError(
                400,
                "invalid_setting",
                "The contributor terms must be between 20 and 20,000 characters.",
                {"field": "contributor_terms_body"},
            )
        clean["contributor_terms_body"] = body

    for field, max_length in (("curriculum_owner", 160), ("curriculum_license", 80)):
        if field in clean:
            value = str(clean[field]).strip()
            if not 1 <= len(value) <= max_length:
                raise ApiError(
                    400, "invalid_setting", "That value is empty or too long.", {"field": field}
                )
            clean[field] = value

    if "curriculum_authoring_model" in clean and clean["curriculum_authoring_model"] not in AUTHORING_MODELS:
        raise ApiError(
            400,
            "invalid_setting",
            "Choose how the curriculum is authored.",
            {"field": "curriculum_authoring_model", "allowed": list(AUTHORING_MODELS)},
        )

    if "target_launch_date" in clean and clean["target_launch_date"] is not None:
        launch = clean["target_launch_date"]
        if isinstance(launch, date) and not 2000 <= launch.year <= 2100:
            raise ApiError(
                400, "invalid_setting", "That launch date is out of range.", {"field": "target_launch_date"}
            )
        if isinstance(launch, str):
            try:
                clean["target_launch_date"] = date.fromisoformat(launch)
            except ValueError as exc:
                raise ApiError(
                    400, "invalid_setting", "Use an ISO date (YYYY-MM-DD).", {"field": "target_launch_date"}
                ) from exc
    return clean


def update_platform_settings(
    db: Session, actor: User, changes: dict[str, Any]
) -> PlatformSettings:
    """Validate and apply a subset of settings, recording before/after in the audit."""
    row = get_platform_settings(db)
    clean = _validate(changes, row)

    diff: dict[str, dict[str, Any]] = {}
    for field, value in clean.items():
        before = getattr(row, field)
        if before == value:
            continue
        # The terms body is long; the audit stores a length, not the document.
        if field == "contributor_terms_body":
            diff[field] = {"from": len(before or ""), "to": len(value)}
        else:
            diff[field] = {"from": before, "to": value}
        setattr(row, field, value)

    if not diff:
        return row
    row.updated_by = actor.id
    db.flush()
    audit.record(
        db,
        action="platform.settings_updated",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="platform_settings",
        target_id=str(row.id),
        context={"changes": diff},
    )
    return row


def public_config(row: PlatformSettings) -> dict[str, Any]:
    """What every client may read: what money is in, and the rules it is held to."""
    return {
        "billing_currency": row.billing_currency,
        "payout_currency": row.payout_currency,
        "allowed_currencies": list(row.allowed_currencies or []),
        "min_student_age": row.min_student_age,
        "guardian_consent_below_age": row.guardian_consent_below_age,
        "terms_version": row.terms_version,
        "contributor_terms_version": row.contributor_terms_version,
        "contributor_terms_body": row.contributor_terms_body,
        "curriculum_owner": row.curriculum_owner,
        "curriculum_license": row.curriculum_license,
        "curriculum_authoring_model": row.curriculum_authoring_model,
        "target_launch_date": row.target_launch_date,
        "updated_at": row.updated_at,
    }


def admin_payload(row: PlatformSettings) -> dict[str, Any]:
    body = public_config(row)
    body.update(
        {
            "id": row.id,
            "payout_second_approver_threshold_minor": row.payout_second_approver_threshold_minor,
            "payout_second_approver_always": row.payout_second_approver_always,
            "payout_require_verified_email": row.payout_require_verified_email,
            "updated_by": row.updated_by,
        }
    )
    return body


def age_from(date_of_birth: date, *, today: date | None = None) -> int:
    """Whole years, counting a birthday that has not happened yet as next year."""
    day = today or utcnow().date()
    return day.year - date_of_birth.year - (
        (day.month, day.day) < (date_of_birth.month, date_of_birth.day)
    )


def current_consent(
    db: Session, user: User, kind: str, version: str
) -> Consent | None:
    """The latest granted consent at this exact document version.

    A version bump therefore invalidates the old agreement without deleting the
    evidence of it.
    """
    return db.scalar(
        select(Consent)
        .where(
            Consent.user_id == user.id,
            Consent.kind == kind,
            Consent.document_version == version,
            Consent.granted.is_(True),
        )
        .order_by(Consent.id.desc())
        .limit(1)
    )


def consent_version_for(row: PlatformSettings, kind: str) -> str:
    if kind == "contributor_terms":
        return row.contributor_terms_version
    if kind == "guardian_consent":
        return row.contributor_terms_version
    if kind == "terms_of_service":
        return row.terms_version
    return "1"


def eligibility(db: Session, user: User) -> dict[str, Any]:
    """Whether this student may accept paid work, and exactly what is missing.

    `blockers` are stable codes a client can branch on; `reasons` are readable
    sentences. Both are returned so a screen never has to invent copy.
    """
    row = get_platform_settings(db)
    profile = user.profile
    blockers: list[str] = []
    reasons: list[str] = []
    age: int | None = None

    if not user.email_verified:
        blockers.append("email_unverified")
        reasons.append("Confirm your email address before accepting work.")

    if profile is None or profile.date_of_birth is None:
        blockers.append("date_of_birth_missing")
        reasons.append("Add your date of birth in Settings so we can apply the age rules.")
    else:
        age = age_from(profile.date_of_birth)
        if age < row.min_student_age:
            blockers.append("under_minimum_age")
            reasons.append(
                f"Paid work starts at {row.min_student_age}. You can keep learning and practising."
            )
        elif age < row.guardian_consent_below_age and current_consent(
            db, user, "guardian_consent", row.contributor_terms_version
        ) is None:
            blockers.append("guardian_consent_required")
            reasons.append(
                "A parent or guardian needs to agree to the contributor terms before you accept paid work."
            )

    if current_consent(db, user, "contributor_terms", row.contributor_terms_version) is None:
        blockers.append("contributor_terms_required")
        reasons.append("Read and accept the contributor terms before accepting work.")

    return {
        "eligible": not blockers,
        "blockers": blockers,
        "reasons": reasons,
        "age": age,
        "min_student_age": row.min_student_age,
        "guardian_consent_below_age": row.guardian_consent_below_age,
        "contributor_terms_version": row.contributor_terms_version,
        "contributor_terms_body": row.contributor_terms_body,
    }


def ensure_work_eligible(db: Session, user: User) -> None:
    """Gate accepting paid work. Raising here is the only enforcement that counts."""
    result = eligibility(db, user)
    if result["eligible"]:
        return
    raise ApiError(
        403,
        "not_eligible_for_work",
        result["reasons"][0] if result["reasons"] else "You are not eligible for paid work yet.",
        {
            "blockers": result["blockers"],
            "reasons": result["reasons"],
            "min_student_age": result["min_student_age"],
        },
    )


def payout_blockers(db: Session, user: User, row: PlatformSettings) -> list[str]:
    """Identity checks before a student is paid.

    Payout is narrower than work eligibility: it does not ask for the terms again
    (they were accepted to start the work), but it does refuse an unverified
    email and anyone below the minimum age.
    """
    blockers: list[str] = []
    if row.payout_require_verified_email and not user.email_verified:
        blockers.append("email_unverified")
    if user.is_deleted:
        blockers.append("account_deleted")
    profile = user.profile
    if profile and profile.date_of_birth and age_from(profile.date_of_birth) < row.min_student_age:
        blockers.append("under_minimum_age")
    return blockers


def record_consent(
    db: Session, user: User, *, kind: str, document_version: str, granted: bool
) -> Consent:
    """Append a consent row. Never edits an existing one (PRD §13)."""
    if kind not in CONSENT_KINDS:
        raise ApiError(400, "unknown_consent_kind", "Unknown consent kind.")
    row = get_platform_settings(db)
    expected = consent_version_for(row, kind)
    if document_version.strip() != expected:
        raise ApiError(
            409,
            "stale_terms",
            "Those terms have changed. Reload and read the current version.",
            {"expected_version": expected},
        )
    if kind == "guardian_consent" and not granted:
        raise ApiError(
            400, "guardian_consent_required", "Guardian consent must be granted, not declined."
        )
    if kind == "guardian_consent":
        profile = user.profile
        age = age_from(profile.date_of_birth) if profile and profile.date_of_birth else None
        if age is not None and age >= row.guardian_consent_below_age:
            raise ApiError(
                400, "guardian_consent_not_required", "Guardian consent is not required at your age."
            )
    consent = Consent(
        user_id=user.id,
        kind=kind,
        document_version=document_version.strip(),
        granted=granted,
    )
    db.add(consent)
    db.flush()
    audit.record(
        db,
        action="consent.recorded",
        actor_user_id=user.id,
        actor_role_code=user.role.code if user.role else None,
        target_type="consent",
        target_id=consent.id,
        context={"kind": kind, "version": consent.document_version, "granted": granted},
    )
    return consent


__all__ = [
    "AUTHORING_MODELS",
    "CURRENCY_RE",
    "EDITABLE_FIELDS",
    "admin_payload",
    "age_from",
    "consent_version_for",
    "current_consent",
    "eligibility",
    "ensure_work_eligible",
    "get_platform_settings",
    "payout_blockers",
    "public_config",
    "record_consent",
    "update_platform_settings",
]
