"""Ops surfaces: content publishing, the ledger explorer, imports and overrides.

These are the internal tools the managed workforce runs on. Each one is tested for
both halves of its contract: the staff action succeeds and is auditable, and a
student is refused. Content also proves the student-facing rule — a draft is
invisible until it is published.
"""
from __future__ import annotations

from factories import make_opportunity, make_ops, make_project, make_reviewer, make_skill, make_user
from sqlalchemy import select

from app.core.security import create_access_token
from app.models.admin import AuditLog
from app.models.identity import User
from app.models.matching import Opportunity
from app.services.money import ledger
from app.services.skills import learning


def _headers(user) -> dict:
    return {
        "Authorization": (
            f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
        )
    }


def test_content_is_invisible_until_it_is_published(api) -> None:
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)

    created = client.post(
        "/v1/skills/content/paths",
        json={
            "skill_id": skill.id,
            "slug": "annotation-draft",
            "title": "Annotation draft",
            "status": "draft",
        },
        headers=_headers(ops),
    )
    assert created.status_code == 201
    path_id = created.json()["id"]

    assert learning.get_skill(db, skill.slug)["paths"] == []

    published = client.patch(
        f"/v1/skills/content/paths/{path_id}",
        json={"status": "published"},
        headers=_headers(ops),
    )
    assert published.json()["status"] == "published"
    assert [row["slug"] for row in learning.get_skill(db, skill.slug)["paths"]] == [
        "annotation-draft"
    ]


def test_content_management_is_staff_only(api) -> None:
    client, db = api
    student = make_user(db)
    skill = make_skill(db)

    response = client.post(
        "/v1/skills/content/lessons",
        json={"skill_id": skill.id, "slug": "sneaky", "title": "Sneaky lesson"},
        headers=_headers(student),
    )

    assert response.status_code == 403


def test_a_duplicate_slug_is_a_409(api) -> None:
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)
    body = {"skill_id": skill.id, "slug": "same-slug", "title": "First"}

    assert client.post("/v1/skills/content/lessons", json=body, headers=_headers(ops)).status_code == 201
    second = client.post("/v1/skills/content/lessons", json=body, headers=_headers(ops))
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "lesson_exists"


def test_an_unknown_step_kind_is_refused(api) -> None:
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)
    path = client.post(
        "/v1/skills/content/paths",
        json={"skill_id": skill.id, "slug": "path-x", "title": "Path"},
        headers=_headers(ops),
    ).json()

    response = client.post(
        f"/v1/skills/content/paths/{path['id']}/steps",
        json={"path_id": path["id"], "ordinal": 1, "kind": "video"},
        headers=_headers(ops),
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_step_kind"


def test_publishing_a_template_bumps_its_version(api) -> None:
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)
    created = client.post(
        "/v1/skills/content/tasks",
        json={
            "skill_id": skill.id,
            "slug": "sentiment-v2",
            "name": "Sentiment",
            "input_schema": {"text": "string"},
            "answer_schema": {"label": "string"},
        },
        headers=_headers(ops),
    ).json()

    published = client.patch(
        f"/v1/skills/content/tasks/{created['id']}",
        json={"status": "published"},
        headers=_headers(ops),
    )

    assert published.status_code == 200
    assert published.json()["version"] == 2


def test_the_ledger_explorer_lists_the_rows_behind_a_balance(api) -> None:
    client, db = api
    ops = make_ops(db)
    project = make_project(db, ops, make_opportunity(db, ops))
    ledger.fund_project(db, ops, project=project, total_minor=1_000_000)

    response = client.get(f"/v1/money/projects/{project.slug}/ledger", headers=_headers(ops))

    assert response.status_code == 200
    payload = response.json()
    assert payload["transactions"][0]["kind"] == "project_funding"
    assert len(payload["transactions"][0]["entries"]) == 4
    accounts = {entry["account"] for entry in payload["transactions"][0]["entries"]}
    assert accounts == {
        "project_escrow",
        "student_payable",
        "platform_revenue",
        "department_payable",
    }


def test_the_ledger_export_is_a_csv(api) -> None:
    client, db = api
    ops = make_ops(db)
    project = make_project(db, ops, make_opportunity(db, ops))
    ledger.fund_project(db, ops, project=project, total_minor=100_000)

    response = client.get(
        f"/v1/money/projects/{project.slug}/ledger/export", headers=_headers(ops)
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert response.text.splitlines()[0].startswith("transaction_id,kind,account")


def test_a_dry_run_import_over_http_creates_no_account(api) -> None:
    client, db = api
    ops = make_ops(db)

    response = client.post(
        "/v1/ops/imports",
        json={
            "mode": "dry_run",
            "data": {
                "users": [
                    {
                        "email": "v1user@example.test",
                        "username": "v1user",
                        "name": "V1 User",
                    }
                ]
            },
        },
        headers=_headers(ops),
    )

    assert response.status_code == 201
    assert response.json()["counts"]["users"]["created"] == 1
    assert response.json()["reconciliation"]["balanced"] is True
    assert db.scalars(select(User).where(User.email == "v1user@example.test")).all() == []


def test_imports_require_the_import_permission(api) -> None:
    client, db = api
    student = make_user(db)
    response = client.post(
        "/v1/ops/imports", json={"mode": "dry_run", "data": {}}, headers=_headers(student)
    )
    assert response.status_code == 403


def test_an_override_is_logged_and_staff_only(api) -> None:
    client, db = api
    reviewer = make_reviewer(db)
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)

    refused = client.post(
        f"/v1/verification/records/{student.id}/{skill.id}/override",
        json={"to_status": "verified", "reason": "gold task mis-scored"},
        headers=_headers(student),
    )
    assert refused.status_code == 403

    accepted = client.post(
        f"/v1/verification/records/{student.id}/{skill.id}/override",
        json={"to_status": "verified", "reason": "gold task mis-scored"},
        headers=_headers(reviewer),
    )
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "verified"

    rows = db.scalars(select(AuditLog).where(AuditLog.action == "verification.override")).all()
    assert rows and rows[0].reason == "gold task mis-scored"
    assert rows[0].actor_user_id == reviewer.id

    # The ops dashboard sees the audit row too.
    logs = client.get("/v1/ops/audit-logs?action=verification.override", headers=_headers(ops))
    assert logs.status_code == 200
    assert logs.json()["logs"][0]["reason"] == "gold task mis-scored"


def test_the_opportunity_ops_routes_stay_shut_for_students(api) -> None:
    client, db = api
    student = make_user(db)
    response = client.post(
        "/v1/opportunities",
        json={
            "type": "managed",
            "slug": "sneaky-project",
            "title": "Sneaky",
            "currency": "USD",
            "rate_minor": 100,
        },
        headers=_headers(student),
    )
    assert response.status_code == 403
    assert db.scalars(select(Opportunity)).all() == []
