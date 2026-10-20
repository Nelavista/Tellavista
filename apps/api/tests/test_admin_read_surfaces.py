"""Admin read surfaces and the practical-task route (B7, C4, C7).

These are the endpoints the ops screens call. They exist for staff, and each one
must refuse a student — an ops list that leaks drafts or another student's work
is the same class of bug as a missing permission check.
"""
from __future__ import annotations

from factories import make_opportunity, make_ops, make_skill, make_template, make_user, unique
from sqlalchemy import select

from app.core.security import create_access_token
from app.models.academia import Course, Department, Faculty, University
from app.models.skills import STATUS_PUBLISHED, LearningPath, Lesson, TaskTemplate
from app.models.verification import PracticalSubmission, PracticalTask


def _headers(user) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"}


def test_the_ops_opportunity_list_includes_drafts_and_refuses_a_student(api) -> None:
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)

    as_ops = client.get("/v1/opportunities/admin/all", headers=_headers(ops))
    assert as_ops.status_code == 200
    slugs = [row["slug"] for row in as_ops.json()["opportunities"]]
    assert opportunity.slug in slugs

    as_student = client.get("/v1/opportunities/admin/all", headers=_headers(student))
    assert as_student.status_code == 403


def test_work_project_list_is_staff_only(api) -> None:
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)

    created = client.post(
        "/v1/work/projects",
        json={"opportunity_slug": opportunity.slug, "slug": unique("project"), "title": "Pilot"},
        headers=_headers(ops),
    )
    assert created.status_code == 201

    listing = client.get("/v1/work/projects", headers=_headers(ops))
    assert listing.status_code == 200
    assert any(row["slug"] == created.json()["slug"] for row in listing.json()["projects"])

    assert client.get("/v1/work/projects", headers=_headers(student)).status_code == 403


def test_content_lists_show_drafts_and_the_validator_catalog(api) -> None:
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)
    lesson = Lesson(
        skill_id=skill.id,
        slug=unique("lesson"),
        title="Draft lesson",
        body_md="# Hello",
        status="draft",
    )
    path = LearningPath(skill_id=skill.id, slug=unique("path"), title="Draft path", status="draft")
    template = make_template(db, skill, status="draft")
    db.add_all([lesson, path])
    db.flush()

    lessons = client.get("/v1/skills/content/lessons", headers=_headers(ops))
    assert lessons.status_code == 200
    assert any(row["id"] == lesson.id and row["status"] == "draft" for row in lessons.json()["lessons"])

    paths = client.get("/v1/skills/content/paths", headers=_headers(ops))
    assert paths.status_code == 200
    assert any(row["id"] == path.id for row in paths.json()["paths"])

    tasks = client.get("/v1/skills/content/tasks", headers=_headers(ops))
    assert tasks.status_code == 200
    assert any(row["id"] == template.id for row in tasks.json()["templates"])

    validators = client.get("/v1/skills/content/validators", headers=_headers(ops))
    assert validators.status_code == 200
    assert validators.json()["validators"] == [
        "exact_key",
        "label_set",
        "numeric_tolerance",
        "ranking",
        "span_overlap",
    ]


def test_the_course_list_can_be_filtered_by_level(api) -> None:
    _client, db = api
    university = University(name=unique("University"), slug=unique("university"))
    db.add(university)
    db.flush()
    faculty = Faculty(university_id=university.id, name="Science")
    db.add(faculty)
    db.flush()
    department = Department(faculty_id=faculty.id, name="Computer Science")
    db.add(department)
    db.flush()
    db.add_all(
        [
            Course(department_id=department.id, code="CSC213", title="Data structures", level="200"),
            Course(department_id=department.id, code="CSC315", title="Systems", level="300"),
        ]
    )
    db.flush()

    from app.services.identity import onboarding

    all_levels = onboarding.list_courses(db, department.id)
    only_200 = onboarding.list_courses(db, department.id, level="200")
    assert len(all_levels) == 2
    assert [row.level for row in only_200] == ["200"]


def test_practical_submission_route_grades_and_writes_proof(api) -> None:
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    task = PracticalTask(
        skill_id=skill.id,
        slug=unique("practical"),
        title="Annotate ten rows",
        brief_md="Label each row.",
        rubric=[{"name": "Accuracy", "description": "Every label matches the brief."}],
        status=STATUS_PUBLISHED,
    )
    db.add(task)
    db.commit()

    listed = client.get("/v1/verification/practical", headers=_headers(student))
    assert listed.status_code == 200
    assert listed.json()["tasks"][0]["rubric"][0]["name"] == "Accuracy"

    submitted = client.post(
        f"/v1/verification/practical/{task.slug}",
        json={"payload": {"summary": "I labelled all ten rows."}},
        headers=_headers(student),
    )
    assert submitted.status_code == 201
    submission_id = submitted.json()["id"]

    # The same client key must not create a second submission.
    again = client.post(
        f"/v1/verification/practical/{task.slug}",
        json={"payload": {"summary": "retry"}, "client_key": "same-key"},
        headers=_headers(student),
    )
    assert again.status_code == 201
    retried = client.post(
        f"/v1/verification/practical/{task.slug}",
        json={"payload": {"summary": "retry"}, "client_key": "same-key"},
        headers=_headers(student),
    )
    assert retried.json()["id"] == again.json()["id"]

    queue = client.get("/v1/verification/practical/submissions", headers=_headers(ops))
    assert queue.status_code == 200
    assert any(row["id"] == submission_id for row in queue.json()["submissions"])

    reviewed = client.post(
        f"/v1/verification/practical/submissions/{submission_id}/review",
        json={"score": 90, "passed": True, "notes": "Good work."},
        headers=_headers(ops),
    )
    assert reviewed.status_code == 200, reviewed.text
    assert reviewed.json()["passed"] is True

    row = db.scalar(select(PracticalSubmission).where(PracticalSubmission.id == submission_id))
    assert row is not None
    assert row.passed is True
    assert row.status == "reviewed"
    assert row.reviewed_by == ops.id


def test_a_student_cannot_read_the_review_queue(api) -> None:
    client, db = api
    student = make_user(db)
    assert client.get("/v1/work/review-queue", headers=_headers(student)).status_code == 403
    assert client.get("/v1/verification/practical/submissions", headers=_headers(student)).status_code == 403


def test_two_factor_was_added_without_touching_the_user_shape(api) -> None:
    """Every read model keeps working: the new columns are optional."""
    client, db = api
    user = make_user(db)
    me = client.get("/v1/auth/me", headers=_headers(user))
    assert me.status_code == 200
    assert me.json()["mfa_enabled"] is False

    status = client.get("/v1/auth/2fa", headers=_headers(user))
    assert status.status_code == 200
    body = status.json()
    assert body["enabled"] is False
    assert body["remaining_recovery_codes"] == 0


def test_publishing_a_template_is_a_new_version(api) -> None:
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)
    template = make_template(db, skill, status="draft")
    before = template.version

    response = client.patch(
        f"/v1/skills/content/tasks/{template.id}", json={"status": "published"}, headers=_headers(ops)
    )
    assert response.status_code == 200
    assert response.json()["version"] == before + 1


def test_editing_a_template_does_not_silently_reversion_it(api) -> None:
    """Only publishing re-versions, so submitted work keeps the definition it used."""
    client, db = api
    ops = make_ops(db)
    skill = make_skill(db)
    template = make_template(db, skill, status=STATUS_PUBLISHED)
    before = template.version

    client.patch(
        f"/v1/skills/content/tasks/{template.id}",
        json={"instructions_md": "Updated instructions"},
        headers=_headers(ops),
    )
    stored = db.get(TaskTemplate, template.id)
    assert stored is not None
    assert stored.instructions_md == "Updated instructions"
    assert stored.version == before


def test_the_transcript_counts_only_real_evidence(api) -> None:
    client, db = api
    student = make_user(db)
    response = client.get("/v1/verification/transcript", headers=_headers(student))
    assert response.status_code == 200
    body = response.json()
    assert body["counts"] == {"learned": 0, "proved": 0, "delivered": 0}
    assert body["entries"] == []
