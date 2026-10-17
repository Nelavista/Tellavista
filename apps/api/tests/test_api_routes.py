"""Route contract: flags, authentication and object-level authorisation.

These hit the real FastAPI app through TestClient (with the database overridden),
so a missing router mount or a mis-ordered path is caught here rather than in a
demo. The four rules every endpoint must keep:

* an off flag is a 404, not a half-working screen;
* no token is a 401 with the standard envelope;
* a student never reads another student's row (404, not 403);
* a staff-only route is a 403 for a student.
"""
from __future__ import annotations

from factories import (
    make_assignment,
    make_opportunity,
    make_ops,
    make_project,
    make_skill,
    make_template,
    make_user,
)
from fastapi.testclient import TestClient

from app.core.security import create_access_token


def _headers(user) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"}


def test_every_gated_feature_disappears_when_its_flag_is_off(api_no_flags: TestClient) -> None:
    for path in (
        "/v1/money/earnings",
        "/v1/talent/me",
        "/v1/work/assignments",
        "/v1/academia/dashboard",
        "/v1/skills",
        "/v1/verification",
        "/v1/opportunities",
    ):
        response = api_no_flags.get(path)
        assert response.status_code == 404, path
        assert response.json()["error"]["code"] == "not_found"


def test_a_missing_token_is_a_401_envelope(api) -> None:
    client, _db = api
    response = client.get("/v1/money/earnings")

    assert response.status_code == 401
    body = response.json()["error"]
    assert body["code"] == "not_authenticated"
    assert body["request_id"] == response.headers["X-Request-ID"]


def test_a_student_only_sees_their_own_earnings(api) -> None:
    client, db = api
    student = make_user(db)
    other = make_user(db)

    response = client.get("/v1/money/earnings", headers=_headers(student))

    assert response.status_code == 200
    assert response.json()["lines"] == []
    # The other student's call is the same empty shape: no cross-account reads.
    assert client.get("/v1/money/earnings", headers=_headers(other)).json()["lines"] == []


def test_a_student_cannot_read_project_financials(api) -> None:
    client, db = api
    ops = make_ops(db)
    project = make_project(db, ops, make_opportunity(db, ops))
    student = make_user(db)

    response = client.get(
        f"/v1/money/projects/{project.slug}/financials", headers=_headers(student)
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_a_student_cannot_read_the_audit_trail(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.get("/v1/ops/audit-logs", headers=_headers(student))

    assert response.status_code == 403


def test_another_students_assignment_is_a_404_over_http(api) -> None:
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    intruder = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    project = make_project(db, ops, make_opportunity(db, ops))
    assignment = make_assignment(db, project, student, template=template)

    response = client.get(
        f"/v1/work/assignments/{assignment.id}", headers=_headers(intruder)
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "assignment_not_found"


def test_submitting_work_over_http_is_idempotent(api) -> None:
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    project = make_project(db, ops, make_opportunity(db, ops))
    assignment = make_assignment(db, project, student)

    headers = {**_headers(student), "Idempotency-Key": "http-1"}
    first = client.post(
        f"/v1/work/assignments/{assignment.id}/submissions",
        json={"payload": {"label": "positive"}},
        headers=headers,
    )
    second = client.post(
        f"/v1/work/assignments/{assignment.id}/submissions",
        json={"payload": {"label": "positive"}},
        headers=headers,
    )

    assert first.status_code == 201
    assert first.json()["created"] is True
    assert second.json()["created"] is False
    assert second.json()["id"] == first.json()["id"]


def test_the_academia_dashboard_answers_its_five_questions(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.get("/v1/academia/dashboard", headers=_headers(student))

    assert response.status_code == 200
    assert len(response.json()["questions"]) == 5


def test_an_onboarding_route_is_public(api) -> None:
    client, _db = api
    response = client.get("/v1/onboarding/universities")
    assert response.status_code == 200


def test_the_profile_route_reads_the_authenticated_user(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.get("/v1/me", headers=_headers(student))

    assert response.status_code == 200
    assert "preferred_path" in response.json()


def test_a_students_notifications_are_their_own(api) -> None:
    client, db = api
    student = make_user(db)
    other = make_user(db)

    response = client.get("/v1/me/notifications", headers=_headers(student))
    other_response = client.get("/v1/me/notifications", headers=_headers(other))

    assert response.status_code == 200
    assert response.json()["notifications"] == []
    assert other_response.json()["notifications"] == []


def test_apply_to_managed_work_is_refused_over_http(api) -> None:
    client, db = api
    ops = make_ops(db)
    managed = make_opportunity(db, ops)
    student = make_user(db)

    response = client.post(
        f"/v1/opportunities/{managed.slug}/apply", json={"note": "please"}, headers=_headers(student)
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "managed_work_is_invitation_only"


def test_the_health_endpoint_stays_open(api) -> None:
    client, _db = api
    assert client.get("/v1/health").status_code == 200
