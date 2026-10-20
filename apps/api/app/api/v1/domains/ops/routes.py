"""Ops endpoints: V1 import runs, support lookup, audit trail (Phase 1).

These are internal tools, so they are gated by permission rather than a student
feature flag — switching the student flag off must never hide the import history
that proves what was imported.

The import endpoint takes the V1 export as JSON in the request body. Nothing here
reads V1's database: the export is produced elsewhere and handed in, which keeps
the one-way rule (`V1 → V2`, never the reverse) structural.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.v1.domains.ops.schemas import (
    AuditLogListOut,
    CampusCreatedOut,
    ImportListOut,
    ImportReportOut,
    ImportResultOut,
    UserDetailOut,
    UserListOut,
    WaitlistOut,
)
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.core.pagination import paginate
from app.db.session import get_db
from app.models.academia import University
from app.models.admin import AuditLog
from app.models.identity import User
from app.models.ops import IMPORT_APPLY, IMPORT_DRY_RUN, CampusInfo, ImportRun, UniversityWaitlist
from app.services.academia import campus as campus_service
from app.services.imports import v1 as importer

router = APIRouter(prefix="/ops", tags=["ops"])


class ImportIn(BaseModel):
    mode: str = Field(default=IMPORT_DRY_RUN, max_length=10)
    source: str = Field(default="v1_export", max_length=40)
    data: dict
    v1_counts: dict | None = None


class CampusIn(BaseModel):
    university_id: int
    kind: str = Field(default="info", max_length=30)
    title: str = Field(min_length=2, max_length=160)
    body: str = ""
    latitude_micro: int | None = None
    longitude_micro: int | None = None


@router.post("/imports", status_code=201, response_model=ImportResultOut)
def run_import(
    payload: ImportIn,
    actor: User = Depends(require_permission("import.run")),
    db: Session = Depends(get_db),
) -> ImportResultOut:
    """Dry-run by default. An apply run is recorded with its reconciliation."""
    if payload.mode not in {IMPORT_DRY_RUN, IMPORT_APPLY}:
        raise ApiError(400, "invalid_import_mode", "Import mode must be dry_run or apply.")
    run = importer.run_import(
        db,
        data=payload.data,
        mode=payload.mode,
        source=payload.source,
        created_by=actor.id,
    )
    report = importer.reconciliation(run, payload.v1_counts)
    db.commit()
    return ImportResultOut(
        run_id=run.id,
        mode=run.mode,
        status=run.status,
        counts=run.counts,
        errors=run.errors,
        reconciliation=report,
    )


@router.get("/imports", response_model=ImportListOut)
def list_imports(
    limit: int = Query(default=20, ge=1, le=100),
    _actor: User = Depends(require_permission("import.run")),
    db: Session = Depends(get_db),
) -> dict:
    rows = db.scalars(select(ImportRun).order_by(ImportRun.id.desc()).limit(limit)).all()
    return ImportListOut(
        runs=[
            {
                "id": row.id,
                "source": row.source,
                "mode": row.mode,
                "status": row.status,
                "started_at": row.started_at,
                "finished_at": row.finished_at,
                "counts": row.counts,
                "errors": row.errors,
            }
            for row in rows
        ]
    )


@router.get("/imports/{run_id}", response_model=ImportReportOut)
def import_detail(
    run_id: int,
    _actor: User = Depends(require_permission("import.run")),
    db: Session = Depends(get_db),
) -> ImportReportOut:
    run = db.get(ImportRun, run_id)
    if run is None:
        raise ApiError(404, "import_not_found", "That import run does not exist.")
    return ImportReportOut(**importer.reconciliation(run))


@router.get("/users", response_model=UserListOut)
def search_users(
    q: str | None = Query(default=None, min_length=2, max_length=120),
    cursor: str | None = None,
    limit: int | None = None,
    _actor: User = Depends(require_permission("talent.read")),
    db: Session = Depends(get_db),
) -> UserListOut:
    """Support lookup by email, username or name. Never returns a password hash."""
    stmt = select(User).where(User.is_deleted.is_(False))
    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(User.email.ilike(pattern), User.username.ilike(pattern), User.name.ilike(pattern))
        )
    rows, next_cursor = paginate(db, stmt, id_column=User.id, cursor=cursor, limit=limit)
    return UserListOut(
        users=[
            {
                "id": row.id,
                "email": row.email,
                "username": row.username,
                "name": row.name,
                "role": row.role.code if row.role else None,
                "email_verified": row.email_verified,
                "google_linked": bool(row.google_sub),
                "created_at": row.created_at,
            }
            for row in rows
        ],
        next_cursor=next_cursor,
    )


@router.get("/users/{user_id}", response_model=UserDetailOut)
def user_detail(
    user_id: int,
    _actor: User = Depends(require_permission("talent.read")),
    db: Session = Depends(get_db),
) -> UserDetailOut:
    user = db.get(User, user_id)
    if user is None:
        raise ApiError(404, "user_not_found", "That user does not exist.")
    profile = user.profile
    return UserDetailOut(
        id=user.id,
        email=user.email,
        username=user.username,
        name=user.name,
        role=user.role.code if user.role else None,
        email_verified=user.email_verified,
        google_linked=bool(user.google_sub),
        is_deleted=user.is_deleted,
        deleted_at=user.deleted_at,
        profile={
            "display_name": profile.display_name if profile else None,
            "preferred_path": profile.preferred_path if profile else None,
            "onboarding_completed_at": profile.onboarding_completed_at if profile else None,
        },
    )


@router.get("/audit-logs", response_model=AuditLogListOut)
def audit_logs(
    action: str | None = Query(default=None, max_length=80),
    target_type: str | None = Query(default=None, max_length=60),
    limit: int = Query(default=50, ge=1, le=200),
    _actor: User = Depends(require_permission("audit.read")),
    db: Session = Depends(get_db),
) -> AuditLogListOut:
    """Append-only: there is no endpoint that edits or deletes an audit row."""
    stmt = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
    if action:
        stmt = stmt.where(AuditLog.action == action)
    if target_type:
        stmt = stmt.where(AuditLog.target_type == target_type)
    rows = db.scalars(stmt).all()
    return AuditLogListOut(
        logs=[
            {
                "id": row.id,
                "actor_user_id": row.actor_user_id,
                "actor_role_code": row.actor_role_code,
                "action": row.action,
                "target_type": row.target_type,
                "target_id": row.target_id,
                "reason": row.reason,
                "context": row.context,
                "request_id": row.request_id,
                "created_at": row.created_at,
            }
            for row in rows
        ]
    )


@router.get("/waitlist", response_model=WaitlistOut)
def waitlist(
    limit: int = Query(default=100, ge=1, le=500),
    _actor: User = Depends(require_permission("talent.read")),
    db: Session = Depends(get_db),
) -> dict:
    rows = db.scalars(
        select(UniversityWaitlist).order_by(UniversityWaitlist.id.desc()).limit(limit)
    ).all()
    return WaitlistOut(
        waitlist=[
            {
                "id": row.id,
                "user_id": row.user_id,
                "university_name": row.university_name,
                "email": row.email,
                "note": row.note,
                "created_at": row.created_at,
            }
            for row in rows
        ]
    )


@router.post("/campus", status_code=201, response_model=CampusCreatedOut)
def create_campus_info(
    payload: CampusIn,
    _actor: User = Depends(require_permission("project.write")),
    db: Session = Depends(get_db),
) -> dict:
    university = db.get(University, payload.university_id)
    if university is None:
        raise ApiError(404, "university_not_found", "That university does not exist.")
    if payload.kind not in campus_service.MAP_KINDS | {"info"}:
        raise ApiError(400, "invalid_campus_kind", "Unknown campus item kind.")
    row = CampusInfo(
        university_id=university.id,
        kind=payload.kind,
        title=payload.title.strip(),
        body=payload.body,
        latitude_micro=payload.latitude_micro,
        longitude_micro=payload.longitude_micro,
    )
    db.add(row)
    db.commit()
    return CampusCreatedOut(id=row.id, kind=row.kind, title=row.title)


__all__ = ["router"]
