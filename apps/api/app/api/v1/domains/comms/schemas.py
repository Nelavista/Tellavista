"""Response contracts for announcements and the newsletter list."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnnouncementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    audience: str
    channel: str
    status: str
    published_at: datetime | None = None
    archived_at: datetime | None = None
    email_sent_at: datetime | None = None
    email_recipient_count: int = 0


class AnnouncementListOut(BaseModel):
    announcements: list[AnnouncementOut]


class NewsletterSubscriberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    source: str
    is_active: bool
    created_at: datetime | None = None
    unsubscribed_at: datetime | None = None


class NewsletterSubscriberListOut(BaseModel):
    subscribers: list[NewsletterSubscriberOut]
    active_count: int
    total_count: int


class NewsletterSubscribeOut(BaseModel):
    subscribed: bool
    email: str
