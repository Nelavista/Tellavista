"""Ops contracts: imports, support lookup, audit (C1–C3).

The import report is the receipt: expected versus actual per section, with the
checksums V2 saw. The admin app renders it without interpreting counts, so a
mismatch is visible rather than a green tick with a caveat.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ImportSectionOut(BaseModel):
    expected: int | None = None
    actual: int
    skipped: int
    errors: int
    matched: bool


class ImportReportOut(BaseModel):
    run_id: int
    mode: str
    source: str
    checksums: dict[str, Any]
    sections: dict[str, ImportSectionOut]
    balanced: bool


class ImportRunOut(BaseModel):
    id: int
    source: str
    mode: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    counts: dict[str, Any] | None = None
    errors: list[Any] | None = None


class ImportListOut(BaseModel):
    runs: list[ImportRunOut]


class ImportResultOut(BaseModel):
    run_id: int
    mode: str
    status: str
    counts: dict[str, Any] | None = None
    errors: list[Any] | None = None
    reconciliation: ImportReportOut


class UserSummaryOut(BaseModel):
    id: int
    email: str
    username: str
    name: str | None = None
    role: str | None = None
    email_verified: bool
    google_linked: bool
    created_at: datetime


class UserListOut(BaseModel):
    users: list[UserSummaryOut]
    next_cursor: str | None = None


class UserProfileOut(BaseModel):
    display_name: str | None = None
    preferred_path: str | None = None
    onboarding_completed_at: datetime | None = None


class UserDetailOut(BaseModel):
    id: int
    email: str
    username: str
    name: str | None = None
    role: str | None = None
    email_verified: bool
    google_linked: bool
    is_deleted: bool
    deleted_at: datetime | None = None
    profile: UserProfileOut


class AuditLogOut(BaseModel):
    id: int
    actor_user_id: int | None = None
    actor_role_code: str | None = None
    action: str
    target_type: str | None = None
    target_id: str | None = None
    reason: str | None = None
    context: dict[str, Any] | None = None
    request_id: str | None = None
    created_at: datetime


class AuditLogListOut(BaseModel):
    logs: list[AuditLogOut]


class WaitlistEntryOut(BaseModel):
    id: int
    user_id: int | None = None
    university_name: str
    email: str | None = None
    note: str | None = None
    created_at: datetime


class WaitlistOut(BaseModel):
    waitlist: list[WaitlistEntryOut]


class CampusCreatedOut(BaseModel):
    id: int
    kind: str
    title: str


__all__ = [
    "AuditLogListOut",
    "AuditLogOut",
    "CampusCreatedOut",
    "ImportListOut",
    "ImportReportOut",
    "ImportResultOut",
    "ImportRunOut",
    "ImportSectionOut",
    "UserDetailOut",
    "UserListOut",
    "UserProfileOut",
    "UserSummaryOut",
    "WaitlistEntryOut",
    "WaitlistOut",
]
