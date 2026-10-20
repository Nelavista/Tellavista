"""Student-facing surfaces: profile settings, opportunity discovery, invites (Phase 2/4)."""
from __future__ import annotations

from factories import make_opportunity, make_ops, make_project, make_user, unique
from sqlalchemy import select

from app.core.security import create_access_token
from app.models.identity import User
from app.models.work import Cohort

PREFIX = "/v1"


def _headers(user) -> dict:
    return {
        "Authorization": f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
    }


def test_profile_languages_and_availability_round_trip(api) -> None:
    client, db = api
    student = make_user(db)
    headers = _headers(student)

    put_langs = client.put(
        f"{PREFIX}/me/languages",
        json={
            "languages": [
                {"language": "English", "level": "fluent"},
                {"language": "Swahili", "level": "native"},
            ]
        },
        headers=headers,
    )
    assert put_langs.status_code == 200, put_langs.text
    assert {row["language"] for row in put_langs.json()["languages"]} == {"English", "Swahili"}

    got_langs = client.get(f"{PREFIX}/me/languages", headers=headers)
    assert got_langs.status_code == 200
    assert len(got_langs.json()["languages"]) == 2

    put_avail = client.put(
        f"{PREFIX}/me/availability", json={"hours_per_week": 12}, headers=headers
    )
    assert put_avail.status_code == 200, put_avail.text
    assert put_avail.json()["hours_per_week"] == 12

    got_avail = client.get(f"{PREFIX}/me/availability", headers=headers)
    assert got_avail.status_code == 200
    assert got_avail.json()["hours_per_week"] == 12


def test_export_returns_the_account_payload(api) -> None:
    client, db = api
    student = make_user(db, email="export@example.test")

    response = client.get(f"{PREFIX}/me/export", headers=_headers(student))

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["account"]["email"] == "export@example.test"
    assert "profile" in body


def test_deleting_an_account_anonymises_the_row(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.delete(f"{PREFIX}/auth/account", headers=_headers(student))

    assert response.status_code == 200, response.text
    db.expire_all()
    row = db.scalar(select(User).where(User.id == student.id))
    assert row.is_deleted is True
    # The row is anonymised rather than removed: money and audit rows still point at it.
    assert row.email == f"deleted-{student.id}@deleted.invalid"
    assert row.username == f"deleted-{student.id}"
    assert row.name is None


def test_external_opportunity_discovery_and_apply(api) -> None:
    client, db = api
    ops = make_ops(db)
    opportunity = make_opportunity(db, ops, type="external", slug=unique("freelance"))
    student = make_user(db)
    headers = _headers(student)

    listing = client.get(f"{PREFIX}/opportunities", headers=headers)
    assert listing.status_code == 200, listing.text
    slugs = {row["slug"] for row in listing.json()["opportunities"]}
    assert opportunity.slug in slugs

    detail = client.get(f"{PREFIX}/opportunities/{opportunity.slug}", headers=headers)
    assert detail.status_code == 200, detail.text
    assert detail.json()["type"] == "external"
    # The verdict is nested under `match` so a client cannot show eligibility
    # without the reasons that explain it.
    assert detail.json()["match"]["eligible"] is True
    # This fixture has no requirements, so there is nothing to explain; an
    # explanation entry only exists for a requirement that was checked.
    assert detail.json()["match"]["explanation"] == []
    assert detail.json()["match"]["next_steps"] == []

    gaps = client.get(f"{PREFIX}/opportunities/{opportunity.slug}/gaps", headers=headers)
    assert gaps.status_code == 200, gaps.text
    assert "gaps" in gaps.json()

    applied = client.post(
        f"{PREFIX}/opportunities/{opportunity.slug}/apply",
        json={"note": "I would love to help."},
        headers=headers,
    )
    assert applied.status_code == 201, applied.text
    assert applied.json()["status"] == "applied"

    mine = client.get(f"{PREFIX}/opportunities/applications", headers=headers)
    assert mine.status_code == 200
    assert len(mine.json()["applications"]) == 1


def test_managed_opportunity_is_invitation_only(api) -> None:
    client, db = api
    ops = make_ops(db)
    managed = make_opportunity(db, ops)
    student = make_user(db)

    response = client.post(
        f"{PREFIX}/opportunities/{managed.slug}/apply", json={}, headers=_headers(student)
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "managed_work_is_invitation_only"


def test_cohort_invite_accept_flow(api) -> None:
    client, db = api
    ops = make_ops(db)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    cohort = Cohort(project_id=project.id, name=unique("cohort"), capacity=3, status="forming")
    db.add(cohort)
    db.flush()
    student = make_user(db)
    student_headers = _headers(student)
    ops_headers = _headers(ops)

    invite = client.post(
        f"{PREFIX}/work/cohorts/{cohort.id}/invites",
        json={"user_ids": [student.id]},
        headers=ops_headers,
    )
    assert invite.status_code == 201, invite.text
    assert invite.json()["members"][0]["status"] == "invited"

    notifications = client.get(f"{PREFIX}/me/notifications", headers=student_headers)
    assert notifications.status_code == 200
    kinds = [row["kind"] for row in notifications.json()["notifications"]]
    assert "invite" in kinds

    respond = client.post(
        f"{PREFIX}/work/cohorts/{cohort.id}/respond",
        json={"accept": True},
        headers=student_headers,
    )
    assert respond.status_code == 200, respond.text
    assert respond.json()["status"] == "active"

    detail = client.get(f"{PREFIX}/work/cohorts/{cohort.id}", headers=ops_headers)
    assert detail.status_code == 200, detail.text
    assert detail.json()["members"][0]["status"] == "active"


def test_a_closed_cohort_rejects_invites(api) -> None:
    client, db = api
    ops = make_ops(db)
    project = make_project(db, ops, make_opportunity(db, ops))
    cohort = Cohort(project_id=project.id, name=unique("cohort"), status="closed")
    db.add(cohort)
    db.flush()
    student = make_user(db)

    response = client.post(
        f"{PREFIX}/work/cohorts/{cohort.id}/invites",
        json={"user_ids": [student.id]},
        headers=_headers(ops),
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "cohort_closed"
