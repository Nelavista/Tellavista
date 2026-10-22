"""Opportunities: managed work and external listings (PRD §6, §7).

`type` is the money switch. A managed opportunity can become a project and a
ledger; an external one never can, and `apply_external` refuses to touch money
even by accident.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User
from app.models.matching import (
    OPPORTUNITY_EXTERNAL,
    OPPORTUNITY_MANAGED,
    OPPORTUNITY_TYPES,
    REQUIREMENT_KINDS,
    Opportunity,
    Requirement,
)
from app.models.talent import (
    APPLICATION_APPLIED,
    OpportunityApplication,
)
from app.services import audit
from app.services.matching import engine

STATUS_DRAFT = "draft"
STATUS_OPEN = "open"
STATUS_CLOSED = "closed"


def _validate_requirements(requirements: list[dict]) -> None:
    for requirement in requirements:
        kind = requirement.get("kind")
        if kind not in REQUIREMENT_KINDS:
            raise ApiError(400, "invalid_requirement", f"Unknown requirement kind: {kind}.")


def create_opportunity(
    db: Session,
    actor: User,
    *,
    type: str,
    slug: str,
    title: str,
    description: str = "",
    client_name: str | None = None,
    department_id: int | None = None,
    headcount: int | None = None,
    quality_standard: str | None = None,
    currency: str | None = None,
    rate_minor: int | None = None,
    starts_on: date | None = None,
    ends_on: date | None = None,
    requirements: list[dict] | None = None,
) -> Opportunity:
    if type not in OPPORTUNITY_TYPES:
        raise ApiError(400, "invalid_opportunity_type", "Use managed or external.")
    if not slug.strip() or not title.strip():
        raise ApiError(400, "invalid_opportunity", "A slug and title are required.")
    if db.scalar(select(Opportunity.id).where(Opportunity.slug == slug)) is not None:
        raise ApiError(409, "opportunity_exists", "That opportunity slug is already used.")
    if type == OPPORTUNITY_MANAGED:
        # G1: an omitted currency means the configured billing currency. A
        # project still records the currency it was priced in, so a later
        # settings change never rewrites an existing contract.
        from app.services.platform import settings as policy

        configured = policy.get_platform_settings(db)
        currency = (currency or configured.billing_currency).upper()
        if currency not in {code.upper() for code in configured.allowed_currencies}:
            raise ApiError(
                400,
                "unsupported_currency",
                "That currency is not enabled for billing.",
                {"allowed": list(configured.allowed_currencies)},
            )
    if currency is not None and len(currency) != 3:
        raise ApiError(400, "invalid_currency", "Use a three-letter currency code.")
    if rate_minor is not None and rate_minor < 0:
        raise ApiError(400, "invalid_rate", "Rate cannot be negative.")
    if type == OPPORTUNITY_MANAGED and rate_minor is None:
        raise ApiError(
            400,
            "managed_money_required",
            "Managed work needs a per-task rate so earnings are explainable.",
        )
    if type == OPPORTUNITY_EXTERNAL and (currency or rate_minor):
        # External opportunities never carry fee logic; a rate here would invite it.
        raise ApiError(
            400,
            "external_has_no_rate",
            "External opportunities do not take a fee and do not need a rate.",
        )
    _validate_requirements(requirements or [])

    opportunity = Opportunity(
        type=type,
        slug=slug.strip()[:120],
        title=title.strip()[:200],
        description=description,
        client_name=client_name,
        department_id=department_id,
        headcount=headcount,
        quality_standard=quality_standard,
        currency=currency.upper() if currency else None,
        rate_minor=rate_minor,
        starts_on=starts_on,
        ends_on=ends_on,
        status=STATUS_DRAFT,
        created_by=actor.id,
    )
    db.add(opportunity)
    db.flush()
    _replace_requirements(db, opportunity, requirements or [])
    audit.record(
        db,
        action="opportunity.created",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="opportunity",
        target_id=opportunity.id,
        context={"type": type, "slug": opportunity.slug},
    )
    return opportunity


def _replace_requirements(db: Session, opportunity: Opportunity, requirements: list[dict]) -> None:
    for existing in db.scalars(
        select(Requirement).where(Requirement.opportunity_id == opportunity.id)
    ):
        db.delete(existing)
    db.flush()
    for item in requirements:
        db.add(
            Requirement(
                opportunity_id=opportunity.id,
                kind=item["kind"],
                skill_id=item.get("skill_id"),
                minimum_value=item.get("minimum_value"),
                is_mandatory=bool(item.get("is_mandatory", True)),
                description=item.get("description"),
            )
        )
    db.flush()


def update_opportunity(
    db: Session,
    actor: User,
    opportunity: Opportunity,
    *,
    title: str | None = None,
    description: str | None = None,
    headcount: int | None = None,
    quality_standard: str | None = None,
    status: str | None = None,
    requirements: list[dict] | None = None,
) -> Opportunity:
    if title is not None:
        opportunity.title = title.strip()[:200]
    if description is not None:
        opportunity.description = description
    if headcount is not None:
        opportunity.headcount = headcount
    if quality_standard is not None:
        opportunity.quality_standard = quality_standard
    if status is not None:
        if status not in {STATUS_DRAFT, STATUS_OPEN, STATUS_CLOSED}:
            raise ApiError(400, "invalid_status", "Unknown opportunity status.")
        if opportunity.type == OPPORTUNITY_MANAGED and status == STATUS_OPEN:
            if opportunity.currency is None or opportunity.rate_minor is None:
                raise ApiError(400, "managed_money_required", "Set the rate before opening.")
        opportunity.status = status
    if requirements is not None:
        _validate_requirements(requirements)
        _replace_requirements(db, opportunity, requirements)
    db.flush()
    audit.record(
        db,
        action="opportunity.updated",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="opportunity",
        target_id=opportunity.id,
        context={"status": opportunity.status},
    )
    return opportunity


def get_opportunity(db: Session, slug: str) -> Opportunity:
    opportunity = db.scalar(select(Opportunity).where(Opportunity.slug == slug))
    if opportunity is None:
        raise ApiError(404, "opportunity_not_found", "That opportunity does not exist.")
    return opportunity


def list_open(db: Session, *, type: str | None = None) -> list[Opportunity]:
    stmt = select(Opportunity).where(Opportunity.status == STATUS_OPEN)
    if type is not None:
        if type not in OPPORTUNITY_TYPES:
            raise ApiError(400, "invalid_opportunity_type", "Use managed or external.")
        stmt = stmt.where(Opportunity.type == type)
    return list(db.scalars(stmt.order_by(Opportunity.id.desc())).all())


def detail_for_user(db: Session, user: User, opportunity: Opportunity) -> dict:
    result = engine.match_user_to_opportunity(db, user, opportunity)
    return {
        "id": opportunity.id,
        "slug": opportunity.slug,
        "type": opportunity.type,
        "title": opportunity.title,
        "description": opportunity.description,
        "client_name": opportunity.client_name if opportunity.type == OPPORTUNITY_MANAGED else None,
        "headcount": opportunity.headcount,
        "status": opportunity.status,
        "currency": opportunity.currency,
        "rate_minor": opportunity.rate_minor,
        "starts_on": opportunity.starts_on,
        "ends_on": opportunity.ends_on,
        "requirements": [
            {
                "id": requirement.id,
                "kind": requirement.kind,
                "skill_id": requirement.skill_id,
                "minimum_value": requirement.minimum_value,
                "is_mandatory": requirement.is_mandatory,
                "description": requirement.description,
            }
            for requirement in db.scalars(
                select(Requirement)
                .where(Requirement.opportunity_id == opportunity.id)
                .order_by(Requirement.id)
            ).all()
        ],
        "match": {
            "eligible": result["eligible"],
            "score": result["score"],
            "explanation": result["explanation"],
            "next_steps": result["next_steps"],
            "qualifies_because": result["qualifies_because"],
        },
    }


def apply_external(
    db: Session, user: User, *, slug: str, note: str | None = None
) -> OpportunityApplication:
    opportunity = get_opportunity(db, slug)
    if opportunity.type != OPPORTUNITY_EXTERNAL:
        raise ApiError(
            400,
            "managed_work_is_invitation_only",
            "Managed work is matched by invitation. Use the opportunity's invitation.",
        )
    if opportunity.status != STATUS_OPEN:
        raise ApiError(409, "opportunity_not_open", "This opportunity is not open.")

    application = db.scalar(
        select(OpportunityApplication).where(
            OpportunityApplication.opportunity_id == opportunity.id,
            OpportunityApplication.user_id == user.id,
        )
    )
    if application is None:
        application = OpportunityApplication(
            opportunity_id=opportunity.id,
            user_id=user.id,
            status=APPLICATION_APPLIED,
            note=(note or None),
        )
        db.add(application)
    else:
        application.status = APPLICATION_APPLIED
        application.note = note or application.note
    db.flush()
    audit.record(
        db,
        action="opportunity.applied",
        actor_user_id=user.id,
        target_type="opportunity",
        target_id=opportunity.id,
    )
    return application


def set_application_status(
    db: Session, actor: User, application_id: int, status: str
) -> OpportunityApplication:
    from app.models.talent import APPLICATION_STATUSES

    if status not in APPLICATION_STATUSES:
        raise ApiError(400, "invalid_application_status", "Unknown application status.")
    application = db.get(OpportunityApplication, application_id)
    if application is None:
        raise ApiError(404, "application_not_found", "That application does not exist.")
    application.status = status
    db.flush()
    audit.record(
        db,
        action="opportunity.application_status",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="opportunity_application",
        target_id=application.id,
        context={"status": status},
    )
    return application


def my_applications(db: Session, user: User) -> list[dict]:
    rows = db.execute(
        select(OpportunityApplication, Opportunity)
        .join(Opportunity, Opportunity.id == OpportunityApplication.opportunity_id)
        .where(OpportunityApplication.user_id == user.id)
        .order_by(OpportunityApplication.id.desc())
    ).all()
    return [
        {
            "id": application.id,
            "status": application.status,
            "note": application.note,
            "opportunity": {
                "id": opportunity.id,
                "slug": opportunity.slug,
                "title": opportunity.title,
                "type": opportunity.type,
            },
        }
        for application, opportunity in rows
    ]
