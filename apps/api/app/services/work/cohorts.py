"""Projects and cohorts: the managed workforce run by our team (PRD §8).

A managed opportunity becomes exactly one project. Students join a cohort by
invitation, and an invitation is only offered to someone the matcher says is
eligible — the ops screen shows the same explanation the student sees.

Removal is a status change with a reason, never a delete: a replacement decision
has to be explainable, and the removed student's completed work still counts.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.identity import User
from app.models.matching import OPPORTUNITY_MANAGED, Opportunity
from app.models.skills import STATUS_PUBLISHED, TaskTemplate
from app.models.work import (
    ASSIGNMENT_ASSIGNED,
    COHORT_ACTIVE,
    COHORT_CLOSED,
    COHORT_FORMING,
    MEMBER_ACTIVE,
    MEMBER_COMPLETED,
    MEMBER_INVITED,
    MEMBER_REMOVED,
    Assignment,
    Cohort,
    CohortMember,
    Project,
)
from app.services import audit
from app.services.matching import engine
from app.services.notifications import notify

PROJECT_STATUSES = ("draft", "active", "paused", "completed")


def create_project(
    db: Session,
    actor: User,
    *,
    opportunity: Opportunity,
    slug: str,
    title: str,
    starts_on: date | None = None,
    ends_on: date | None = None,
    status: str = "active",
) -> Project:
    if opportunity.type != OPPORTUNITY_MANAGED:
        raise ApiError(
            400,
            "external_has_no_project",
            "External opportunities are not projects and never touch the ledger.",
        )
    if db.scalar(select(Project.id).where(Project.opportunity_id == opportunity.id)) is not None:
        raise ApiError(409, "project_exists", "This opportunity already has a project.")
    if db.scalar(select(Project.id).where(Project.slug == slug)) is not None:
        raise ApiError(409, "project_slug_taken", "That project slug is already used.")
    if status not in PROJECT_STATUSES:
        raise ApiError(400, "invalid_project_status", "Unknown project status.")

    project = Project(
        opportunity_id=opportunity.id,
        slug=slug,
        title=title,
        starts_on=starts_on,
        ends_on=ends_on,
        status=status,
    )
    db.add(project)
    db.flush()
    audit.record(
        db,
        action="project.created",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="project",
        target_id=project.id,
        context={"opportunity_id": opportunity.id},
    )
    return project


def get_project(db: Session, slug: str) -> Project:
    project = db.scalar(select(Project).where(Project.slug == slug))
    if project is None:
        raise ApiError(404, "project_not_found", "That project does not exist.")
    return project


def create_cohort(
    db: Session,
    actor: User,
    *,
    project: Project,
    name: str,
    capacity: int | None = None,
) -> Cohort:
    if capacity is not None and capacity < 1:
        raise ApiError(400, "invalid_capacity", "Capacity must be at least one.")
    cohort = Cohort(project_id=project.id, name=name.strip()[:120], capacity=capacity)
    db.add(cohort)
    db.flush()
    audit.record(
        db,
        action="cohort.created",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="cohort",
        target_id=cohort.id,
    )
    return cohort


def _seat_count(db: Session, cohort_id: int) -> int:
    return (
        db.scalar(
            select(func.count(CohortMember.id)).where(
                CohortMember.cohort_id == cohort_id,
                CohortMember.status.in_([MEMBER_INVITED, MEMBER_ACTIVE]),
            )
        )
        or 0
    )


def invite(
    db: Session,
    actor: User,
    *,
    cohort: Cohort,
    user_ids: list[int],
) -> list[CohortMember]:
    """Invite eligible students. Ineligible students are rejected with the reason."""
    if cohort.status == COHORT_CLOSED:
        raise ApiError(409, "cohort_closed", "This cohort is closed.")
    project = db.get(Project, cohort.project_id)
    opportunity = db.get(Opportunity, project.opportunity_id) if project else None
    if project is None or opportunity is None:
        raise ApiError(404, "project_not_found", "That project does not exist.")

    unique_ids = list(dict.fromkeys(user_ids))
    if cohort.capacity is not None and _seat_count(db, cohort.id) + len(unique_ids) > cohort.capacity:
        raise ApiError(
            409,
            "cohort_full",
            "This cohort does not have that many seats left.",
            {"capacity": cohort.capacity, "seats_used": _seat_count(db, cohort.id)},
        )

    created: list[CohortMember] = []
    for user_id in unique_ids:
        user = db.get(User, user_id)
        if user is None or user.is_deleted:
            raise ApiError(404, "student_not_found", f"Student {user_id} does not exist.")
        existing = db.scalar(
            select(CohortMember).where(
                CohortMember.cohort_id == cohort.id, CohortMember.user_id == user.id
            )
        )
        if existing is not None:
            if existing.status == MEMBER_REMOVED:
                raise ApiError(
                    409,
                    "student_removed",
                    "This student was removed from the cohort; use a replacement.",
                )
            created.append(existing)
            continue

        result = engine.evaluate(db, user, opportunity)
        if not result["eligible"]:
            raise ApiError(
                409,
                "student_not_eligible",
                "That student does not meet the mandatory requirements.",
                {
                    "user_id": user.id,
                    "missing": [
                        {"requirement_id": check["requirement_id"], "detail": check["detail"]}
                        for check in result["missing"]
                    ],
                },
            )

        member = CohortMember(cohort_id=cohort.id, user_id=user.id, status=MEMBER_INVITED)
        db.add(member)
        db.flush()
        from app.core import observability

        observability.capture(
            user.id, observability.EVENTS["matched"], {"opportunity_id": opportunity.id}
        )
        notify(
            db,
            user_id=user.id,
            kind="invite",
            title=f"You are invited to {project.title}",
            body="Open the opportunity to see why you qualify and accept the work.",
            data={"cohort_id": cohort.id, "project_slug": project.slug},
        )
        created.append(member)
    db.flush()
    return created


def respond_invite(db: Session, user: User, cohort_id: int, *, accept: bool) -> CohortMember:
    member = db.scalar(
        select(CohortMember).where(
            CohortMember.cohort_id == cohort_id, CohortMember.user_id == user.id
        )
    )
    if member is None:
        raise ApiError(404, "invite_not_found", "You were not invited to this cohort.")
    if member.status != MEMBER_INVITED:
        raise ApiError(409, "invite_not_pending", "This invitation was already answered.")

    if not accept:
        member.status = MEMBER_REMOVED
        db.flush()
        return member

    cohort = db.get(Cohort, cohort_id)
    if cohort is None:
        raise ApiError(404, "cohort_not_found", "That cohort does not exist.")
    if cohort.capacity is not None:
        active = (
            db.scalar(
                select(func.count(CohortMember.id)).where(
                    CohortMember.cohort_id == cohort.id, CohortMember.status == MEMBER_ACTIVE
                )
            )
            or 0
        )
        if active >= cohort.capacity:
            raise ApiError(409, "cohort_full", "This cohort is already full.")

    member.status = MEMBER_ACTIVE
    member.joined_at = utcnow()
    if cohort.status == COHORT_FORMING and cohort.capacity is not None:
        active = (
            db.scalar(
                select(func.count(CohortMember.id)).where(
                    CohortMember.cohort_id == cohort.id, CohortMember.status == MEMBER_ACTIVE
                )
            )
            or 0
        )
        if active >= cohort.capacity:
            cohort.status = COHORT_ACTIVE
    db.flush()
    return member


def remove_member(
    db: Session,
    actor: User,
    *,
    member_id: int,
    reason: str,
) -> CohortMember:
    if not reason.strip():
        raise ApiError(400, "reason_required", "Removal needs a reason.")
    member = db.get(CohortMember, member_id)
    if member is None:
        raise ApiError(404, "member_not_found", "That cohort member does not exist.")
    if member.status == MEMBER_REMOVED:
        raise ApiError(409, "already_removed", "This student was already removed.")
    member.status = MEMBER_REMOVED
    db.flush()

    cohort = db.get(Cohort, member.cohort_id)
    project = db.get(Project, cohort.project_id) if cohort else None
    audit.record(
        db,
        action="cohort.member_removed",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="cohort_member",
        target_id=member.id,
        reason=reason,
        context={"project_slug": project.slug if project else None},
    )
    notify(
        db,
        user_id=member.user_id,
        kind="system",
        title="Your work on this project has ended",
        body=reason[:200],
        data={"cohort_id": member.cohort_id},
    )
    return member


def replacement_candidates(db: Session, cohort: Cohort, *, limit: int = 20) -> list[dict]:
    """Eligible students who are not already in this cohort."""
    project = db.get(Project, cohort.project_id)
    opportunity = db.get(Opportunity, project.opportunity_id) if project else None
    if project is None or opportunity is None:
        return []
    member_ids = {
        row
        for row in db.scalars(
            select(CohortMember.user_id).where(CohortMember.cohort_id == cohort.id)
        ).all()
    }
    result = []
    for candidate in engine.match_candidates(db, opportunity):
        if candidate["user_id"] in member_ids or not candidate["eligible"]:
            continue
        result.append(
            {
                "user_id": candidate["user_id"],
                "score": candidate["score"],
                "qualifies_because": candidate["qualifies_because"],
                "next_steps": candidate["next_steps"],
            }
        )
        if len(result) >= limit:
            break
    return result


def cohort_detail(db: Session, cohort: Cohort) -> dict:
    members = db.execute(
        select(CohortMember, User)
        .join(User, User.id == CohortMember.user_id)
        .where(CohortMember.cohort_id == cohort.id)
        .order_by(CohortMember.id)
    ).all()
    counts = dict(
        db.execute(
            select(Assignment.status, func.count(Assignment.id))
            .where(Assignment.cohort_id == cohort.id)
            .group_by(Assignment.status)
        ).all()
    )
    return {
        "id": cohort.id,
        "project_id": cohort.project_id,
        "name": cohort.name,
        "capacity": cohort.capacity,
        "status": cohort.status,
        "seats_used": _seat_count(db, cohort.id),
        "members": [
            {
                "member_id": member.id,
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "status": member.status,
                "joined_at": member.joined_at,
            }
            for member, user in members
        ],
        "assignment_counts": counts,
    }


def assign_task(
    db: Session,
    actor: User,
    *,
    project: Project,
    user_id: int,
    title: str,
    template_id: int | None = None,
    cohort_id: int | None = None,
    due_at: datetime | None = None,
) -> Assignment:
    if project.status != "active":
        raise ApiError(409, "project_not_active", "This project is not active.")
    member = db.scalar(
        select(CohortMember)
        .join(Cohort, Cohort.id == CohortMember.cohort_id)
        .where(
            Cohort.project_id == project.id,
            CohortMember.user_id == user_id,
            CohortMember.status == MEMBER_ACTIVE,
        )
    )
    if member is None:
        raise ApiError(
            409,
            "not_active_member",
            "Assign work only to students who accepted a cohort invitation.",
        )
    if template_id is not None:
        template = db.get(TaskTemplate, template_id)
        if template is None or template.status != STATUS_PUBLISHED:
            raise ApiError(404, "task_template_not_found", "That task template is not published.")

    assignment = Assignment(
        project_id=project.id,
        cohort_id=cohort_id or member.cohort_id,
        user_id=user_id,
        template_id=template_id,
        title=title.strip()[:200],
        status=ASSIGNMENT_ASSIGNED,
        due_at=due_at,
    )
    db.add(assignment)
    db.flush()
    notify(
        db,
        user_id=user_id,
        kind="assignment",
        title="New work assigned",
        body=f"{assignment.title} is ready for you.",
        data={"assignment_id": assignment.id, "project_slug": project.slug},
    )
    audit.record(
        db,
        action="assignment.created",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="assignment",
        target_id=assignment.id,
        context={"user_id": user_id, "project_id": project.id},
    )
    return assignment


def my_assignments(db: Session, user: User) -> list[dict]:
    rows = db.execute(
        select(Assignment, Project)
        .join(Project, Project.id == Assignment.project_id)
        .where(Assignment.user_id == user.id)
        .order_by(Assignment.id.desc())
    ).all()
    return [
        {
            "id": assignment.id,
            "title": assignment.title,
            "status": assignment.status,
            "due_at": assignment.due_at,
            "template_id": assignment.template_id,
            "project": {"id": project.id, "slug": project.slug, "title": project.title},
        }
        for assignment, project in rows
    ]


def project_dashboard(db: Session, project: Project) -> dict:
    assignments = dict(
        db.execute(
            select(Assignment.status, func.count(Assignment.id))
            .where(Assignment.project_id == project.id)
            .group_by(Assignment.status)
        ).all()
    )
    cohorts = db.scalars(select(Cohort).where(Cohort.project_id == project.id)).all()
    return {
        "id": project.id,
        "slug": project.slug,
        "title": project.title,
        "status": project.status,
        "starts_on": project.starts_on,
        "ends_on": project.ends_on,
        "cohorts": [cohort_detail(db, cohort) for cohort in cohorts],
        "assignment_counts": assignments,
    }


def complete_member_work(db: Session, member: CohortMember) -> None:
    """Called when every assignment for a member is approved."""
    member.status = MEMBER_COMPLETED
    db.flush()
