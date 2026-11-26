"""Announcements and the newsletter list.

Two admin surfaces that did not exist: composing a message and sending the
newsletter. What is worth testing is not "the row saves" but the parts that are
irreversible -- a message people already received cannot be rewritten, a double
publish cannot double-mail, and an unsubscribe cannot be silently undone.
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest
from factories import make_ops, make_user, unique
from sqlalchemy import func, select

from app.core import ratelimit
from app.core.security import create_access_token
from app.models.comms import NewsletterSubscriber
from app.models.jobs import Job


@pytest.fixture(autouse=True)
def _reset_rate_limits():
    """This module deliberately hits the public opt-in many times; the IP limit is
    exercised in test_rate_limit_redis.py, not by accumulating across tests."""
    ratelimit.reset()
    yield
    ratelimit.reset()


def _headers(user) -> dict:
    return {
        "Authorization": (
            f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
        )
    }


def _subscriber(db, *, active: bool = True) -> NewsletterSubscriber:
    row = NewsletterSubscriber(
        email=f"{unique('list')}@example.test",
        source="manual",
        is_active=active,
        confirmed_at=datetime.now(UTC),
    )
    db.add(row)
    db.commit()
    return row


def _confirm(client, db, address: str) -> None:
    """Finish the double opt-in the way the reader does: from the emailed link."""
    row = db.scalar(select(NewsletterSubscriber).where(NewsletterSubscriber.email == address))
    assert row is not None and row.confirm_token
    response = client.post("/v1/newsletter/confirm", json={"token": row.confirm_token})
    assert response.status_code == 200, response.text


def test_ops_can_compose_and_publish_an_announcement(api) -> None:
    client, db = api
    ops = make_ops(db)

    created = client.post(
        "/v1/ops/announcements",
        json={"title": "New payout rail", "body": "Payouts now land in 24h.", "audience": "students"},
        headers=_headers(ops),
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["status"] == "draft"
    assert body["published_at"] is None

    published = client.post(
        f"/v1/ops/announcements/{body['id']}/publish", headers=_headers(ops)
    )
    assert published.status_code == 200
    assert published.json()["status"] == "published"
    assert published.json()["published_at"] is not None


def test_a_published_announcement_cannot_be_rewritten(api) -> None:
    client, db = api
    ops = make_ops(db)
    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Maintenance", "body": "Down 2am."},
        headers=_headers(ops),
    ).json()

    draft_edit = client.patch(
        f"/v1/ops/announcements/{created['id']}",
        json={"body": "Down 3am."},
        headers=_headers(ops),
    )
    assert draft_edit.status_code == 200

    client.post(f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops))
    late_edit = client.patch(
        f"/v1/ops/announcements/{created['id']}",
        json={"body": "Never happened."},
        headers=_headers(ops),
    )
    assert late_edit.status_code == 409
    assert late_edit.json()["error"]["code"] == "announcement_not_editable"


def test_publishing_twice_does_not_double_mail(api) -> None:
    client, db = api
    ops = make_ops(db)
    _subscriber(db)
    _subscriber(db)
    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Hello", "body": "First issue", "channel": "email"},
        headers=_headers(ops),
    ).json()

    first = client.post(f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops))
    assert first.json()["email_recipient_count"] == 2

    again = client.post(f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops))
    assert again.status_code == 200
    assert again.json()["email_recipient_count"] == 2

    jobs = db.scalar(select(func.count()).select_from(Job).where(Job.name == "send_email"))
    assert jobs == 2  # one per subscriber, not four


def test_a_platform_only_announcement_sends_no_email(api) -> None:
    client, db = api
    ops = make_ops(db)
    _subscriber(db)
    created = client.post(
        "/v1/ops/announcements",
        json={"title": "In-app notice", "channel": "platform"},
        headers=_headers(ops),
    ).json()

    body = client.post(
        f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops)
    ).json()
    assert body["email_recipient_count"] == 0
    assert db.scalar(select(func.count()).select_from(Job).where(Job.name == "send_email")) == 0


def test_an_unsubscribed_address_is_not_mailed(api) -> None:
    client, db = api
    ops = make_ops(db)
    _subscriber(db)
    _subscriber(db, active=False)
    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Issue two", "channel": "both"},
        headers=_headers(ops),
    ).json()

    body = client.post(
        f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops)
    ).json()
    assert body["email_recipient_count"] == 1


def test_students_read_only_their_audience(api) -> None:
    client, db = api
    ops = make_ops(db)
    student = make_user(db)

    for audience, title in (("students", "For students"), ("staff", "For staff"), ("all", "For all")):
        created = client.post(
            "/v1/ops/announcements",
            json={"title": title, "audience": audience},
            headers=_headers(ops),
        ).json()
        client.post(f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops))

    student_rows = client.get("/v1/announcements", headers=_headers(student)).json()
    staff_rows = client.get("/v1/announcements", headers=_headers(ops)).json()
    student_titles = {row["title"] for row in student_rows["announcements"]}
    staff_titles = {row["title"] for row in staff_rows["announcements"]}

    assert student_titles == {"For students", "For all"}
    assert staff_titles == {"For staff", "For all"}


def test_a_draft_is_not_visible_in_the_product(api) -> None:
    client, db = api
    ops = make_ops(db)
    client.post(
        "/v1/ops/announcements",
        json={"title": "Not yet"},
        headers=_headers(ops),
    )
    assert client.get("/v1/announcements", headers=_headers(ops)).json()["announcements"] == []


def test_archiving_removes_an_announcement_from_the_product(api) -> None:
    client, db = api
    ops = make_ops(db)
    created = client.post(
        "/v1/ops/announcements", json={"title": "Temporary"}, headers=_headers(ops)
    ).json()
    client.post(f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops))

    archived = client.post(
        f"/v1/ops/announcements/{created['id']}/archive", headers=_headers(ops)
    )
    assert archived.json()["status"] == "archived"
    assert client.get("/v1/announcements", headers=_headers(ops)).json()["announcements"] == []


def test_a_student_cannot_publish_an_announcement(api) -> None:
    client, db = api
    response = client.post(
        "/v1/ops/announcements",
        json={"title": "Fake notice"},
        headers=_headers(make_user(db)),
    )
    assert response.status_code == 403


def test_the_public_can_subscribe_once(api) -> None:
    client, db = api
    address = f"{unique('public')}@example.test"

    first = client.post("/v1/newsletter/subscribe", json={"email": address})
    second = client.post("/v1/newsletter/subscribe", json={"email": address.upper()})

    assert first.status_code == 201 and second.status_code == 201
    rows = db.scalars(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == address)
    ).all()
    assert len(rows) == 1
    # Double opt-in: submitting starts the row but does not finish it.
    assert rows[0].is_active
    assert rows[0].confirmed_at is None
    assert rows[0].confirm_token

    _confirm(client, db, address)
    db.refresh(rows[0])
    assert rows[0].confirmed_at is not None


def test_subscribing_emails_one_confirmation_link_and_does_not_spam(api) -> None:
    client, db = api
    address = f"{unique('confirmmail')}@example.test"

    client.post("/v1/newsletter/subscribe", json={"email": address})
    client.post("/v1/newsletter/subscribe", json={"email": address})

    jobs = db.scalars(select(Job).where(Job.name == "send_email")).all()
    assert len(jobs) == 1  # the second submit reused the pending job key
    body = jobs[0].payload["body"]
    row = db.scalar(select(NewsletterSubscriber).where(NewsletterSubscriber.email == address))
    assert f"/newsletter/confirm?token={row.confirm_token}" in body
    assert address not in body


def test_a_pending_address_is_not_mailed_an_issue(api) -> None:
    client, db = api
    ops = make_ops(db)
    address = f"{unique('pending')}@example.test"
    client.post("/v1/newsletter/subscribe", json={"email": address})

    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Too early", "channel": "email"},
        headers=_headers(ops),
    ).json()
    body = client.post(
        f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops)
    ).json()
    assert body["email_recipient_count"] == 0

    _confirm(client, db, address)
    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Now welcome", "channel": "email"},
        headers=_headers(ops),
    ).json()
    body = client.post(
        f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops)
    ).json()
    assert body["email_recipient_count"] == 1


def test_a_confirmation_click_is_idempotent_and_reports_the_state(api) -> None:
    client, db = api
    address = f"{unique('clicktwice')}@example.test"
    client.post("/v1/newsletter/subscribe", json={"email": address})
    row = db.scalar(select(NewsletterSubscriber).where(NewsletterSubscriber.email == address))

    first = client.post("/v1/newsletter/confirm", json={"token": row.confirm_token})
    second = client.post("/v1/newsletter/confirm", json={"token": row.confirm_token})

    assert first.json() == {"subscribed": True, "pending": False, "email": address}
    # A second click is not an error, and does not change the timestamp.
    assert second.json() == first.json()


def test_an_unknown_confirmation_token_is_refused(api) -> None:
    client, _db = api
    response = client.post("/v1/newsletter/confirm", json={"token": "x" * 40})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "confirm_link_invalid"


def test_the_public_cannot_probe_whether_an_address_is_subscribed(api) -> None:
    """The answer is the same for a new, a pending and a confirmed address, so the
    endpoint cannot be used to test who is on the list."""
    client, db = api
    address = f"{unique('probe')}@example.test"
    fresh = client.post("/v1/newsletter/subscribe", json={"email": address})
    again = client.post("/v1/newsletter/subscribe", json={"email": address})
    _confirm(client, db, address)
    confirmed = client.post("/v1/newsletter/subscribe", json={"email": address})

    expected = {"subscribed": False, "pending": True, "email": address}
    assert fresh.json() == again.json() == confirmed.json() == expected


def test_a_signed_in_person_can_subscribe_and_leave_from_settings(api) -> None:
    client, db = api
    student = make_user(db)

    initial = client.get("/v1/me/newsletter", headers=_headers(student))
    assert initial.json() == {"email": student.email, "subscribed": False, "pending": False}

    started = client.post("/v1/me/newsletter", headers=_headers(student))
    assert started.json() == {"email": student.email, "subscribed": False, "pending": True}
    _confirm(client, db, student.email)

    active = client.get("/v1/me/newsletter", headers=_headers(student))
    assert active.json() == {"email": student.email, "subscribed": True, "pending": False}

    left = client.delete("/v1/me/newsletter", headers=_headers(student))
    assert left.json() == {"email": student.email, "subscribed": False, "pending": False}
    # Leaving twice is not an error.
    again = client.delete("/v1/me/newsletter", headers=_headers(student))
    assert again.json() == left.json()


def test_unsubscribing_keeps_the_row_and_can_be_undone(api) -> None:
    client, db = api
    ops = make_ops(db)
    row = _subscriber(db)

    removed = client.delete(
        f"/v1/ops/newsletter/subscribers/{row.id}", headers=_headers(ops)
    )
    assert removed.status_code == 200
    assert removed.json()["is_active"] is False

    # The row survives, so an import cannot silently re-add it as active.
    db.refresh(row)
    assert row.unsubscribed_at is not None

    again = client.post(
        "/v1/newsletter/subscribe", json={"email": row.email}
    )
    assert again.status_code == 201
    db.refresh(row)
    # Re-subscribing starts a new opt-in: the row is active again but pending
    # confirmation, so an old unsubscribe cannot be silently bypassed.
    assert row.is_active and row.unsubscribed_at is None
    assert row.confirmed_at is None
    _confirm(client, db, row.email)
    db.refresh(row)
    assert row.confirmed_at is not None


def test_the_subscriber_list_reports_real_counts(api) -> None:
    client, db = api
    ops = make_ops(db)
    _subscriber(db)
    _subscriber(db, active=False)

    body = client.get(
        "/v1/ops/newsletter/subscribers", headers=_headers(ops)
    ).json()
    assert body["total_count"] == 2
    assert body["active_count"] == 1
    assert len(body["subscribers"]) == 2


def test_every_email_carries_the_subscribers_own_unsubscribe_link(api) -> None:
    """The link is the only way out for someone who is not signed in, so it has
    to be in the message itself -- and it must carry the token, never the address."""
    client, db = api
    ops = make_ops(db)
    address = f"{unique('optout')}@example.test"
    client.post("/v1/newsletter/subscribe", json={"email": address})
    _confirm(client, db, address)
    row = db.scalar(select(NewsletterSubscriber).where(NewsletterSubscriber.email == address))
    assert row is not None and row.unsubscribe_token

    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Issue three", "body": "Hello there.", "channel": "email"},
        headers=_headers(ops),
    ).json()
    client.post(f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops))

    job = db.scalar(
        select(Job).where(Job.name == "send_email", Job.idempotency_key.like("announcement:%"))
    )
    body = job.payload["body"]
    assert "Hello there." in body
    assert f"/newsletter/unsubscribe?token={row.unsubscribe_token}" in body
    # The address is in the To field, not in a URL anyone could guess.
    assert address not in body


def test_the_unsubscribe_link_works_and_cannot_be_undone_by_accident(api) -> None:
    client, db = api
    ops = make_ops(db)
    address = f"{unique('leave')}@example.test"
    client.post("/v1/newsletter/subscribe", json={"email": address})
    _confirm(client, db, address)
    row = db.scalar(select(NewsletterSubscriber).where(NewsletterSubscriber.email == address))

    first = client.post(
        "/v1/newsletter/unsubscribe", json={"token": row.unsubscribe_token}
    )
    assert first.status_code == 200
    assert first.json() == {"subscribed": False, "pending": False, "email": address}
    db.refresh(row)
    assert row.is_active is False and row.unsubscribed_at is not None

    # A second click (or a mail client prefetch) is not an error.
    again = client.post("/v1/newsletter/unsubscribe", json={"token": row.unsubscribe_token})
    assert again.status_code == 200
    assert again.json()["subscribed"] is False

    # And the next issue skips the address.
    created = client.post(
        "/v1/ops/announcements",
        json={"title": "Issue four", "channel": "email"},
        headers=_headers(ops),
    ).json()
    body = client.post(
        f"/v1/ops/announcements/{created['id']}/publish", headers=_headers(ops)
    ).json()
    assert body["email_recipient_count"] == 0


def test_an_unknown_unsubscribe_token_is_refused(api) -> None:
    client, _db = api
    missing = client.post("/v1/newsletter/unsubscribe", json={"token": "x" * 40})
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "unsubscribe_link_invalid"

    # Too short to be a token at all: refused as a bad request, not looked up.
    truncated = client.post("/v1/newsletter/unsubscribe", json={"token": "abc"})
    assert truncated.status_code == 422


def test_the_subscriber_list_never_returns_unsubscribe_tokens(api) -> None:
    """A list of tokens would let ops -- or anyone who reads that response -- opt
    out every subscriber. The token belongs only in that subscriber's email."""
    client, db = api
    ops = make_ops(db)
    address = f"{unique('listtoken')}@example.test"
    client.post("/v1/newsletter/subscribe", json={"email": address})

    body = client.get("/v1/ops/newsletter/subscribers", headers=_headers(ops)).json()
    assert body["subscribers"]
    for subscriber in body["subscribers"]:
        assert "unsubscribe_token" not in subscriber


def test_an_invalid_email_is_refused(api) -> None:
    client, db = api
    response = client.post("/v1/newsletter/subscribe", json={"email": "not-an-email"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_email"
