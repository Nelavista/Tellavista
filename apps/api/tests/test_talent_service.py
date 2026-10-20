"""Phase 7 — the Talent profile is evidence, and sharing is the student's decision.

Nothing here can add a skill by hand: the profile reads verification, transcript,
approved work and quality. Privacy is opt-in (the default is private), and a share
link is scoped, expiring and revocable, stored only as a hash.
"""
from __future__ import annotations

from datetime import timedelta

import pytest
from factories import (
    make_assignment,
    make_opportunity,
    make_ops,
    make_profile,
    make_project,
    make_skill,
    make_user,
    verify,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.talent import TalentShare
from app.services.talent import profile as talent
from app.services.work import delivery


def _student_with_evidence(db: Session):
    ops = make_ops(db)
    student = make_user(db)
    make_profile(db, student, display_name="Ada", profile_visibility="private")
    skill = make_skill(db)
    verify(db, student, skill)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student)
    submission, _ = delivery.submit_work(
        db, student, assignment_id=assignment.id, payload={"label": "positive"}, client_key="t-1"
    )
    submission.status = "approved"
    db.flush()
    return student, skill, project, submission


def test_a_private_profile_has_no_external_view(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)

    with pytest.raises(ApiError) as excinfo:
        talent.build_profile(db, student)
    assert excinfo.value.status_code == 403
    assert excinfo.value.code == "profile_private"


def test_the_internal_view_works_regardless_of_visibility(db: Session) -> None:
    student, skill, _project, _submission = _student_with_evidence(db)

    payload = talent.build_profile(db, student, internal=True)

    assert payload["evidence_only"] is True
    assert payload["account"]["id"] == student.id
    assert payload["verified_skills"][0]["skill_id"] == skill.id
    assert payload["all_skills"][0]["status"] == "verified"


def test_approved_work_appears_as_history_not_as_a_claim(db: Session) -> None:
    student, _skill, project, submission = _student_with_evidence(db)

    payload = talent.build_profile(db, student, internal=True)

    assert payload["work_history"][0]["submission_id"] == submission.id
    assert payload["projects"][0]["project_id"] == project.id
    assert payload["projects"][0]["approved_tasks"] == 1
    assert payload["verified_skills"][0]["status"] == "verified"


def test_a_share_link_is_scoped_expiring_and_hashed(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)

    share, token = talent.create_share(db, student, label="Recruiter", scopes=["transcript"])

    assert token not in (share.token_hash or "")
    assert len(share.token_hash) == 64
    stored = db.scalars(select(TalentShare)).one()
    assert stored.token_hash == share.token_hash

    payload = talent.view_share(db, token)
    assert "transcript" in payload
    assert "quality" not in payload
    assert "work_history" not in payload
    assert payload["verified_skills"][0]["skill_id"] is not None


def test_a_share_link_works_even_when_the_profile_is_private(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)
    _share, token = talent.create_share(db, student, label=None, scopes=None)

    payload = talent.view_share(db, token)

    # The link is the consent: it is scoped, not a switch that publishes everything.
    assert payload["visibility"] == "private"
    assert payload["evidence_only"] is True
    assert db.scalars(select(TalentShare)).one().last_viewed_at is not None


def test_an_expired_share_is_gone(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)
    share, token = talent.create_share(db, student, label=None, scopes=None)
    share.expires_at = utcnow() - timedelta(minutes=1)
    db.flush()

    with pytest.raises(ApiError) as excinfo:
        talent.view_share(db, token)
    assert excinfo.value.status_code == 410
    assert excinfo.value.code == "share_expired"


def test_revoking_a_share_kills_it(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)
    share, token = talent.create_share(db, student, label=None, scopes=None)

    talent.revoke_share(db, student, share.id)

    with pytest.raises(ApiError) as excinfo:
        talent.view_share(db, token)
    assert excinfo.value.code == "share_not_found"


def test_another_student_cannot_revoke_someone_elses_share(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)
    share, _token = talent.create_share(db, student, label=None, scopes=None)
    intruder = make_user(db)

    with pytest.raises(ApiError) as excinfo:
        talent.revoke_share(db, intruder, share.id)
    assert excinfo.value.code == "share_not_found"


def test_unknown_scopes_are_refused(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)

    with pytest.raises(ApiError) as excinfo:
        talent.create_share(db, student, label=None, scopes=["salary"])
    assert excinfo.value.code == "unknown_scope"

    with pytest.raises(ApiError):
        talent.create_share(db, student, label=None, scopes=None, ttl_days=365)


def test_transcript_only_never_includes_quality(db: Session) -> None:
    student, _skill, _project, _submission = _student_with_evidence(db)

    payload = talent.transcript_only(db, student)

    assert set(payload) == {"transcript", "verified_skills"}
    assert payload["verified_skills"][0]["status"] == "verified"
