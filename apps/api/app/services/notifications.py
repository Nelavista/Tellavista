"""Notifications that cannot be lost (PRD §8, Phase 5).

The row is written in the caller's transaction and the push is a durable job. If
the push provider is down the job retries; the student still sees the notification
in the app. There is no path that sends a push without a row.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import utcnow
from app.models.engagement import NOTIFY_KINDS, Message, Notification
from app.models.identity import User, UserProfile
from app.services.jobs import enqueue


def notify(
    db: Session,
    *,
    user_id: int,
    kind: str,
    title: str,
    body: str,
    data: dict | None = None,
) -> Notification:
    if kind not in NOTIFY_KINDS:
        raise ValueError(f"unknown notification kind: {kind}")
    row = Notification(
        user_id=user_id,
        kind=kind,
        title=title[:160],
        body=body[:500],
        data=data,
    )
    db.add(row)
    db.flush()

    wants_push = db.scalar(
        select(UserProfile.notify_push).where(UserProfile.user_id == user_id)
    )
    if wants_push is not False:
        enqueue(
            db,
            "send_push",
            {
                "user_id": user_id,
                "notification_id": row.id,
                "title": row.title,
                "body": row.body,
                "data": data or {},
            },
            key=f"push:{row.id}",
        )
    return row


def list_notifications(db: Session, user: User, *, unread_only: bool = False) -> list[dict]:
    stmt = select(Notification).where(Notification.user_id == user.id)
    if unread_only:
        stmt = stmt.where(Notification.read_at.is_(None))
    rows = db.scalars(stmt.order_by(Notification.id.desc()).limit(200)).all()
    return [
        {
            "id": row.id,
            "kind": row.kind,
            "title": row.title,
            "body": row.body,
            "data": row.data,
            "read_at": row.read_at,
            "created_at": row.created_at,
        }
        for row in rows
    ]


def mark_read(db: Session, user: User, notification_ids: list[int]) -> int:
    rows = db.scalars(
        select(Notification).where(
            Notification.user_id == user.id,
            Notification.id.in_(notification_ids),
            Notification.read_at.is_(None),
        )
    ).all()
    now = utcnow()
    for row in rows:
        row.read_at = now
    db.flush()
    return len(rows)


def send_message(
    db: Session,
    *,
    sender: User | None,
    recipient_user_id: int,
    body: str,
    assignment_id: int | None = None,
) -> Message:
    if not body.strip():
        raise ValueError("message body cannot be empty")
    row = Message(
        sender_user_id=sender.id if sender else None,
        recipient_user_id=recipient_user_id,
        assignment_id=assignment_id,
        body=body.strip(),
    )
    db.add(row)
    db.flush()
    notify(
        db,
        user_id=recipient_user_id,
        kind="system",
        title="New message",
        body=body.strip()[:200],
        data={"message_id": row.id, "assignment_id": assignment_id},
    )
    return row
