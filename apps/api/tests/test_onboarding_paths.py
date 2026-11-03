"""Four spaces are a product decision, so they get route-level coverage."""

from __future__ import annotations

from factories import make_profile, make_user

from app.core.security import create_access_token
from app.models.academia import University


def _headers(user) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"}


def test_all_four_paths_are_stored_and_unknown_values_are_rejected(api) -> None:
    client, db = api
    student = make_user(db)
    make_profile(db, student)
    headers = _headers(student)

    for path in ("academia", "skills", "opportunities", "campus"):
        response = client.post("/v1/me/path", json={"path": path}, headers=headers)
        assert response.status_code == 200, response.text
        assert response.json()["preferred_path"] == path

    rejected = client.post("/v1/me/path", json={"path": "unknown"}, headers=headers)
    assert rejected.status_code == 400
    assert rejected.json()["error"]["code"] == "invalid_path"


def test_skills_and_opportunities_do_not_require_an_enrolment(api) -> None:
    client, db = api
    student = make_user(db)
    make_profile(db, student)
    headers = _headers(student)

    no_path = client.get("/v1/onboarding/state", headers=headers)
    assert no_path.status_code == 200
    assert no_path.json()["next_step"] == "choose_path"

    for path in ("skills", "opportunities"):
        client.post("/v1/me/path", json={"path": path}, headers=headers)
        state = client.get("/v1/onboarding/state", headers=headers)
        assert state.json()["next_step"] == "ready", path

    client.post("/v1/me/path", json={"path": "academia"}, headers=headers)
    state = client.get("/v1/onboarding/state", headers=headers)
    assert state.json()["next_step"] == "enrol"


def test_campus_needs_a_university_not_a_course_list(api) -> None:
    client, db = api
    student = make_user(db)
    make_profile(db, student)
    headers = _headers(student)
    university = University(name="Example University", slug="example-university")
    db.add(university)
    db.flush()

    client.post("/v1/me/path", json={"path": "campus"}, headers=headers)
    before = client.get("/v1/onboarding/state", headers=headers)
    assert before.json()["next_step"] == "enrol"

    chosen = client.put(
        "/v1/onboarding/university",
        json={"university_id": university.id},
        headers=headers,
    )
    assert chosen.status_code == 200, chosen.text
    assert university.name in chosen.json()["message"]

    after = client.get("/v1/onboarding/state", headers=headers)
    assert after.json()["next_step"] == "ready"

    campus = client.get("/v1/me/campus", headers=headers)
    assert campus.status_code == 200
    assert campus.json()["university"]["name"] == university.name

    missing = client.put(
        "/v1/onboarding/university",
        json={"university_id": 999_999},
        headers=headers,
    )
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "university_not_found"
