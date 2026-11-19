"""Announcements and the newsletter: admin, in-product read and public opt-in.

Three surfaces, one domain, because they are the same message seen from three
sides: ops composes and publishes, a signed-in person reads what is published to
their audience, and anyone can add their address to the newsletter list.

The admin writes sit behind `comms.write` (ops and super admin). The in-product
read is audience-filtered in the service, never in the route. The public opt-in
and opt-out are unauthenticated but rate-limited by IP, since they are the two
endpoints here an outsider can hit in a loop. Opting out needs only the token
from the email: no session, no address in the URL, and no way to unsubscribe
someone else.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.v1.domains.comms.schemas import (
    AnnouncementListOut,
    AnnouncementOut,
    NewsletterSubscribeOut,
    NewsletterSubscriberListOut,
    NewsletterSubscriberOut,
)
from app.core import ratelimit
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.comms import Announcement, NewsletterSubscriber
from app.models.identity import User
from app.services.comms import announcements as comms

public_router = APIRouter(tags=["comms"])


class SubscribeIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    source: str = Field(default="public", max_length=40)


class UnsubscribeIn(BaseModel):
    token: str = Field(min_length=20, max_length=128)


class AnnouncementIn(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    body: str = ""
    audience: str = Field(default="all", max_length=16)
    channel: str = Field(default="platform", max_length=16)


class AnnouncementPatchIn(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    body: str | None = None
    audience: str | None = Field(default=None, max_length=16)
    channel: str | None = Field(default=None, max_length=16)


class SubscriberIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    source: str = Field(default="manual", max_length=40)


# --- public / signed-in -----------------------------------------------------


@public_router.post(
    "/newsletter/subscribe",
    status_code=201,
    response_model=NewsletterSubscribeOut,
)
def subscribe_to_newsletter(
    payload: SubscribeIn,
    request: Request,
    db: Session = Depends(get_db),
) -> NewsletterSubscribeOut:
    """Anyone can subscribe; the answer never says whether the address was new,
    so the endpoint cannot be used to test whether someone is on the list.

    Limited by IP inside the handler rather than with the per-user `rate_limit`
    dependency: there is no signed-in user here to key the counter on, which is
    exactly the case the auth routes already handle this way.
    """
    ratelimit.check(
        f"newsletter-subscribe:{_client_ip(request)}", limit=10, window_seconds=60
    )
    row = comms.subscribe(db, email=payload.email, source=payload.source)
    db.commit()
    return NewsletterSubscribeOut(subscribed=True, email=row.email)


@public_router.post("/newsletter/unsubscribe", response_model=NewsletterSubscribeOut)
def unsubscribe_from_newsletter(
    payload: UnsubscribeIn,
    request: Request,
    db: Session = Depends(get_db),
) -> NewsletterSubscribeOut:
    """Leave the list from the link in the email.

    The token is the whole authorisation, which is why it is never returned by a
    list endpoint: holding it means the reader received that issue. The answer is
    the same on a second click -- an unsubscribe that errors on repeat is how a
    reader ends up believing they are still subscribed.
    """
    ratelimit.check(
        f"newsletter-unsubscribe:{_client_ip(request)}", limit=20, window_seconds=60
    )
    row = comms.unsubscribe_by_token(db, payload.token)
    if row is None:
        raise ApiError(
            404,
            "unsubscribe_link_invalid",
            "That unsubscribe link is not valid. Use the link in the most recent email.",
        )
    db.commit()
    return NewsletterSubscribeOut(subscribed=False, email=row.email)


@public_router.get("/announcements", response_model=AnnouncementListOut)
def read_announcements(
    limit: int = Query(default=20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnnouncementListOut:
    return AnnouncementListOut(announcements=comms.visible_to(db, user, limit=limit))


# --- ops --------------------------------------------------------------------


@public_router.get("/ops/announcements", response_model=AnnouncementListOut)
def list_announcements(
    status: str | None = Query(default=None, max_length=16),
    limit: int = Query(default=100, ge=1, le=200),
    _staff: User = Depends(require_permission("comms.read")),
    db: Session = Depends(get_db),
) -> AnnouncementListOut:
    """Drafts and archives included: this is the screen ops works on."""
    stmt = select(Announcement).order_by(Announcement.id.desc()).limit(limit)
    if status is not None:
        stmt = stmt.where(Announcement.status == status)
    return AnnouncementListOut(announcements=list(db.scalars(stmt).all()))


@public_router.post("/ops/announcements", status_code=201, response_model=AnnouncementOut)
def create_announcement(
    payload: AnnouncementIn,
    actor: User = Depends(require_permission("comms.write")),
    db: Session = Depends(get_db),
) -> Announcement:
    row = comms.create_announcement(
        db,
        actor,
        title=payload.title,
        body=payload.body,
        audience=payload.audience,
        channel=payload.channel,
    )
    db.commit()
    return row


@public_router.patch("/ops/announcements/{announcement_id}", response_model=AnnouncementOut)
def update_announcement(
    announcement_id: int,
    payload: AnnouncementPatchIn,
    actor: User = Depends(require_permission("comms.write")),
    db: Session = Depends(get_db),
) -> Announcement:
    row = _announcement(db, announcement_id)
    comms.update_announcement(
        db,
        actor,
        row,
        title=payload.title,
        body=payload.body,
        audience=payload.audience,
        channel=payload.channel,
    )
    db.commit()
    return row


@public_router.post(
    "/ops/announcements/{announcement_id}/publish", response_model=AnnouncementOut
)
def publish_announcement(
    announcement_id: int,
    actor: User = Depends(require_permission("comms.write")),
    db: Session = Depends(get_db),
) -> Announcement:
    row = comms.publish_announcement(db, actor, _announcement(db, announcement_id))
    db.commit()
    return row


@public_router.post(
    "/ops/announcements/{announcement_id}/archive", response_model=AnnouncementOut
)
def archive_announcement(
    announcement_id: int,
    actor: User = Depends(require_permission("comms.write")),
    db: Session = Depends(get_db),
) -> Announcement:
    row = comms.archive_announcement(db, actor, _announcement(db, announcement_id))
    db.commit()
    return row


@public_router.get("/ops/newsletter/subscribers", response_model=NewsletterSubscriberListOut)
def list_subscribers(
    active_only: bool = Query(default=False),
    limit: int = Query(default=200, ge=1, le=500),
    _staff: User = Depends(require_permission("comms.read")),
    db: Session = Depends(get_db),
) -> NewsletterSubscriberListOut:
    stmt = select(NewsletterSubscriber).order_by(NewsletterSubscriber.id.desc()).limit(limit)
    if active_only:
        stmt = stmt.where(NewsletterSubscriber.is_active.is_(True))
    counts = comms.subscriber_counts(db)
    return NewsletterSubscriberListOut(
        subscribers=list(db.scalars(stmt).all()),
        active_count=counts["active"],
        total_count=counts["total"],
    )


@public_router.post(
    "/ops/newsletter/subscribers", status_code=201, response_model=NewsletterSubscriberOut
)
def add_subscriber(
    payload: SubscriberIn,
    _staff: User = Depends(require_permission("comms.write")),
    db: Session = Depends(get_db),
) -> NewsletterSubscriber:
    """Adding an address ops collected elsewhere is the same opt-in path as the
    public form, so the consent rules cannot diverge between the two."""
    row = comms.subscribe(db, email=payload.email, source=payload.source)
    db.commit()
    return row


@public_router.delete(
    "/ops/newsletter/subscribers/{subscriber_id}", response_model=NewsletterSubscriberOut
)
def unsubscribe_subscriber(
    subscriber_id: int,
    _staff: User = Depends(require_permission("comms.write")),
    db: Session = Depends(get_db),
) -> NewsletterSubscriber:
    """Deactivates rather than deletes: a removed row could be re-added by the
    next import, which would re-subscribe someone who opted out."""
    row = db.get(NewsletterSubscriber, subscriber_id)
    if row is None:
        raise ApiError(404, "subscriber_not_found", "That subscriber does not exist.")
    comms.unsubscribe(db, row)
    db.commit()
    return row


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _announcement(db: Session, announcement_id: int) -> Announcement:
    row = db.get(Announcement, announcement_id)
    if row is None:
        raise ApiError(404, "announcement_not_found", "That announcement does not exist.")
    return row


__all__ = ["public_router"]
