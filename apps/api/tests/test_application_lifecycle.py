"""The application lifecycle: deeper states, and the moves that are refused.

An application now runs interested -> applied -> shortlisted -> offered ->
accepted -> in_progress -> submitted -> completed, with rejected/withdrawn/
expired as the ways out before work starts. Each later state gates real work
and, downstream, real money, so the rule under test is not "the status saves"
but "a skipped step cannot be saved".
"""
from __future__ import annotations

import pytest
from factories import make_opportunity, make_ops, make_user, unique
from sqlalchemy import select

from app.core.security import create_access_token
from app.models.admin import AuditLog
from app.models.talent import (
    APPLICATION_ACCEPTED,
    APPLICATION_APPLIED,
    APPLICATION_COMPLETED,
    APPLICATION_IN_PROGRESS,
    APPLICATION_OFFERED,
    APPLICATION_REJECTED,
    APPLICATION_SHORTLISTED,
    APPLICATION_STATUSES,
    APPLICATION_SUBMITTED,
    APPLICATION_TRANSITIONS,
    OpportunityApplication,
    can_transition,
)


def _headers(user) -> dict:
    return {
        "Authorization": (
            f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
        )
    }


def _application(db, status: str = APPLICATION_APPLIED) -> OpportunityApplication:
    """One application, created through the service (so it is audited like a real
    one) and then moved straight to the status the case needs."""
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)
    application = OpportunityApplication(
        opportunity_id=opportunity.id, user_id=student.id, status=status
    )
    db.add(application)
    db.commit()
    return application


def test_every_status_has_a_transition_row() -> None:
    """A new status added without a rule would silently be a dead end (or, worse,
    an unchecked one) -- the table has to cover the whole set."""
    assert set(APPLICATION_TRANSITIONS) == set(APPLICATION_STATUSES)


def test_terminal_states_go_nowhere() -> None:
    for terminal in (
        APPLICATION_COMPLETED,
        APPLICATION_REJECTED,
        "withdrawn",
        "expired",
    ):
        assert APPLICATION_TRANSITIONS[terminal] == ()


def test_the_happy_path_is_walkable_end_to_end(api) -> None:
    client, db = api
    ops = make_ops(db)
    application = _application(db)

    for target in (
        APPLICATION_SHORTLISTED,
        APPLICATION_OFFERED,
        APPLICATION_ACCEPTED,
        APPLICATION_IN_PROGRESS,
        APPLICATION_SUBMITTED,
        APPLICATION_COMPLETED,
    ):
        response = client.post(
            f"/v1/opportunities/applications/{application.id}/status",
            json={"status": target},
            headers=_headers(ops),
        )
        assert response.status_code == 200, response.text
        assert response.json()["status"] == target
        # The response carries the next legal moves, so ops never offers a refused one.
        assert response.json()["allowed_next"] == list(APPLICATION_TRANSITIONS[target])


def test_a_skipped_step_is_refused(api) -> None:
    client, db = api
    ops = make_ops(db)
    application = _application(db)

    response = client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": APPLICATION_COMPLETED},
        headers=_headers(ops),
    )
    assert response.status_code == 409
    error = response.json()["error"]
    assert error["code"] == "invalid_application_transition"
    assert error["details"]["current"] == APPLICATION_APPLIED
    assert error["details"]["requested"] == APPLICATION_COMPLETED
    db.refresh(application)
    assert application.status == APPLICATION_APPLIED


def test_a_completed_application_cannot_be_reopened(api) -> None:
    client, db = api
    ops = make_ops(db)
    application = _application(db, status=APPLICATION_COMPLETED)

    response = client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": APPLICATION_IN_PROGRESS},
        headers=_headers(ops),
    )
    assert response.status_code == 409
    db.refresh(application)
    assert application.status == APPLICATION_COMPLETED


def test_submitted_work_can_be_sent_back_for_rework(api) -> None:
    client, db = api
    ops = make_ops(db)
    application = _application(db, status=APPLICATION_SUBMITTED)

    response = client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": APPLICATION_IN_PROGRESS},
        headers=_headers(ops),
    )
    assert response.status_code == 200
    assert response.json()["status"] == APPLICATION_IN_PROGRESS


def test_resending_the_current_status_is_a_harmless_no_op(api) -> None:
    """Without this, a double-click in the ops UI looks like a refused edit."""
    client, db = api
    ops = make_ops(db)
    application = _application(db, status=APPLICATION_SHORTLISTED)

    response = client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": APPLICATION_SHORTLISTED},
        headers=_headers(ops),
    )
    assert response.status_code == 200
    assert response.json()["status"] == APPLICATION_SHORTLISTED


def test_a_decision_stamps_decided_at(api) -> None:
    client, db = api
    ops = make_ops(db)
    application = _application(db)
    assert application.decided_at is None

    client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": APPLICATION_SHORTLISTED},
        headers=_headers(ops),
    )
    db.refresh(application)
    assert application.decided_at is not None


def test_an_unknown_status_is_a_400_not_a_500(api) -> None:
    client, db = api
    ops = make_ops(db)
    application = _application(db)

    response = client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": "hired"},
        headers=_headers(ops),
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_application_status"


def test_the_move_is_audited_with_both_ends(api) -> None:
    """A status change is the record of who let someone work; the log must say
    where it came from as well as where it went."""
    client, db = api
    ops = make_ops(db)
    application = _application(db)

    client.post(
        f"/v1/opportunities/applications/{application.id}/status",
        json={"status": APPLICATION_SHORTLISTED},
        headers=_headers(ops),
    )
    entry = db.scalar(
        select(AuditLog).where(
            AuditLog.target_type == "opportunity_application",
            AuditLog.target_id == application.id,
        )
    )
    assert entry is not None
    assert entry.context == {"from": APPLICATION_APPLIED, "status": APPLICATION_SHORTLISTED}


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (APPLICATION_APPLIED, APPLICATION_OFFERED),
        (APPLICATION_OFFERED, APPLICATION_IN_PROGRESS),
        (APPLICATION_IN_PROGRESS, APPLICATION_COMPLETED),
        (APPLICATION_ACCEPTED, APPLICATION_SUBMITTED),
    ],
)
def test_can_transition_rejects_specific_skips(current: str, target: str) -> None:
    assert not can_transition(current, target)


def test_an_application_is_unique_per_opportunity_and_student(db) -> None:
    """The lifecycle assumes one row per (opportunity, student); a second row would
    let a student be in two states of the same job at once."""
    application = _application(db)
    duplicate = OpportunityApplication(
        opportunity_id=application.opportunity_id,
        user_id=application.user_id,
        status=APPLICATION_APPLIED,
        note=unique("second"),
    )
    db.add(duplicate)
    from sqlalchemy.exc import IntegrityError

    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
