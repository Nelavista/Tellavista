"""Audit writes (model: app.models.admin.AuditLog).

Append-only by contract: this module only inserts. Every sensitive action —
role changes, verification overrides, payout approvals, account deletion, import
runs — must call `record` in the same transaction as the change it describes, so
an audit row cannot exist without its action, or vice versa.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.request_id import get_request_id
from app.models.admin import AuditLog


def record(
    db: Session,
    *,
    action: str,
    actor_user_id: int | None = None,
    actor_role_code: str | None = None,
    target_type: str | None = None,
    target_id: str | int | None = None,
    reason: str | None = None,
    context: dict[str, Any] | None = None,
) -> AuditLog:
    entry = AuditLog(
        actor_user_id=actor_user_id,
        actor_role_code=actor_role_code,
        action=action,
        target_type=target_type,
        target_id=str(target_id) if target_id is not None else None,
        reason=reason,
        request_id=get_request_id() or None,
        context=context,
    )
    db.add(entry)
    db.flush()
    return entry
