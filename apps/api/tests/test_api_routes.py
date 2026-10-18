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
    unique,
)
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.models.skills import (
    STATUS_PUBLISHED,
    LearningPath,
    LearningPathStep,
    Lesson,
)
from app.models.verification import Assessment, AssessmentTask


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
    body = response.json()
    # The response model is the contract: a new or renamed question fails here.
    assert set(body["questions"]) == {
        "what_am_i_studying",
        "what_did_i_study_recently",
        "what_should_i_practise",
        "where_am_i_weak",
        "what_should_i_do_next",
    }
    assert body["materials_by_course"] == {}
    assert body["enrolment_count"] == 0
    # With no data the dashboard still recommends a real next step.
    assert body["questions"]["what_should_i_do_next"]["action"]["kind"] == "onboarding"


def test_campus_serialises_its_contract(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.get("/v1/me/campus", headers=_headers(student))

    assert response.status_code == 200
    assert response.json() == {"university": None, "info": [], "map": []}


def test_the_skills_journey_matches_its_response_models(api) -> None:
    """One walk through Learn → Practise against the modelled shapes.

    Every call here would fail with a 500 if a service returned a shape the
    response model does not describe, so this is the drift check for the skills
    contract as well as a journey test.
    """
    client, db = api
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill, config={"expected_answer": {"key": "positive"}})
    path = LearningPath(
        skill_id=skill.id, slug=unique("path"), title="Annotation basics", status=STATUS_PUBLISHED
    )
    db.add(path)
    db.flush()
    lesson = Lesson(
        skill_id=skill.id,
        slug=unique("lesson"),
        title="What annotation is",
        body_md="Annotation turns raw data into labels.",
        estimated_minutes=10,
        status=STATUS_PUBLISHED,
    )
    db.add(lesson)
    db.flush()
    db.add_all(
        [
            LearningPathStep(path_id=path.id, ordinal=1, kind="lesson", lesson_id=lesson.id),
            LearningPathStep(
                path_id=path.id, ordinal=2, kind="practice", task_template_id=template.id
            ),
        ]
    )
    db.flush()
    headers = _headers(student)

    catalog = client.get("/v1/skills", headers=headers)
    assert catalog.status_code == 200
    assert skill.slug in [row["slug"] for row in catalog.json()["skills"]]

    detail = client.get(f"/v1/skills/{skill.slug}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["paths"][0]["slug"] == path.slug

    journey = client.get(f"/v1/skills/paths/{path.slug}", headers=headers)
    assert journey.status_code == 200
    body = journey.json()
    assert body["required_steps"] == 2
    assert body["percent_complete"] == 0
    assert [step["unlocked"] for step in body["steps"]] == [True, False]
    assert body["next_step"]["kind"] == "lesson"

    brief = client.get(f"/v1/skills/tasks/{template.id}", headers=headers)
    assert brief.status_code == 200
    assert brief.json()["template_id"] == template.id
    # The expected answer is configuration and never reaches the student.
    assert "expected_answer" not in brief.text

    reader = client.get(f"/v1/skills/lessons/{lesson.slug}", headers=headers)
    assert reader.status_code == 200
    assert reader.json()["unlocked"] is True
    assert reader.json()["body_md"] == "Annotation turns raw data into labels."

    started = client.post(f"/v1/skills/lessons/{lesson.id}/start", headers=headers)
    assert started.json() == {"lesson_id": lesson.id, "status": "in_progress"}

    completed = client.post(f"/v1/skills/lessons/{lesson.id}/complete", headers=headers)
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"
    # Completing a lesson is progress, never proof.
    assert completed.json()["verified"] is False

    halfway = client.get(f"/v1/skills/paths/{path.slug}", headers=headers)
    assert halfway.json()["completed_steps"] == 1
    assert halfway.json()["percent_complete"] == 50
    # One lesson done unlocks the practice step behind it.
    assert halfway.json()["steps"][1]["unlocked"] is True
    assert halfway.json()["next_step"]["kind"] == "practice"

    practice = client.post(
        f"/v1/skills/tasks/{template.id}/practice",
        json={"answer": {"key": "positive"}},
        headers=headers,
    )
    assert practice.status_code == 200
    assert practice.json()["is_correct"] is True
    assert practice.json()["counts_as_verification"] is False

    finished = client.get(f"/v1/skills/paths/{path.slug}", headers=headers)
    assert finished.json()["percent_complete"] == 100
    assert finished.json()["next_step"] is None

    learning = client.get("/v1/skills/my-learning", headers=headers)
    assert learning.status_code == 200
    assert [row["slug"] for row in learning.json()["paths"]] == [path.slug]


def test_the_verification_journey_matches_its_response_models(api) -> None:
    """Sit an assessment end to end against the modelled shapes (B7).

    The response models are the contract: a service that stops returning a field
    or renames one fails here. The two product rules that matter are asserted in
    words as well — the expected answer never reaches a sitting, and a pass writes
    a `proved` line to the transcript.
    """
    client, db = api
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    assessment = Assessment(
        skill_id=skill.id,
        slug=unique("assessment"),
        title="Annotation check",
        status=STATUS_PUBLISHED,
        pass_threshold=80,
        max_attempts=3,
        task_count=2,
    )
    db.add(assessment)
    db.flush()
    db.add_all(
        [
            AssessmentTask(
                assessment_id=assessment.id,
                ordinal=1,
                template_id=template.id,
                payload={"text": "I love it"},
                expected_answer={"key": "positive"},
            ),
            AssessmentTask(
                assessment_id=assessment.id,
                ordinal=2,
                template_id=template.id,
                payload={"text": "I hate it"},
                expected_answer={"key": "negative"},
            ),
        ]
    )
    db.flush()
    headers = _headers(student)

    status = client.get("/v1/verification", headers=headers)
    assert status.status_code == 200
    assert status.json() == {"skills": []}

    catalog = client.get("/v1/verification/assessments", headers=headers)
    assert catalog.status_code == 200
    assert [row["slug"] for row in catalog.json()["assessments"]] == [assessment.slug]

    started = client.post(
        f"/v1/verification/assessments/{assessment.slug}/start", headers=headers
    )
    assert started.status_code == 200
    sitting = started.json()
    assert len(sitting["tasks"]) == 2
    # The template's own schemas ride along so the client renders a real control.
    assert sitting["tasks"][0]["answer_schema"]["required"] == ["label"]
    assert "expected_answer" not in started.text

    answers = {
        str(task["task_id"]): {
            "key": "positive" if task["payload"]["text"] == "I love it" else "negative"
        }
        for task in sitting["tasks"]
    }
    graded = client.post(
        f"/v1/verification/attempts/{sitting['attempt_id']}/submit",
        json={"answers": answers},
        headers=headers,
    )
    assert graded.status_code == 200
    result = graded.json()
    assert result["score"] == 100
    assert result["passed"] is True
    assert result["verification_status"] == "verified"
    assert all(task["correct"] for task in result["tasks"])

    review = client.get(
        f"/v1/verification/attempts/{sitting['attempt_id']}", headers=headers
    )
    assert review.status_code == 200
    # Only now may the expected answers be shown.
    assert review.json()["tasks"][0]["expected_answer"] == {"key": "positive"}

    transcript = client.get("/v1/verification/transcript", headers=headers)
    assert transcript.status_code == 200
    body = transcript.json()
    assert body["counts"]["proved"] == 1
    assert body["proved"][0]["title"] == assessment.title
    assert body["proved"][0]["evidence"]["type"] == "assessment_attempt"


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


def test_resend_verification_needs_a_session_and_respects_verification_state(api) -> None:
    client, db = api
    unverified = make_user(db, email_verified=False)
    verified = make_user(db)

    assert client.post("/v1/auth/email/verify/resend").status_code == 401

    sent = client.post("/v1/auth/email/verify/resend", headers=_headers(unverified))
    assert sent.status_code == 200
    assert "verification email" in sent.json()["message"].lower()

    already = client.post("/v1/auth/email/verify/resend", headers=_headers(verified))
    assert already.status_code == 409
    assert already.json()["error"]["code"] == "already_verified"
