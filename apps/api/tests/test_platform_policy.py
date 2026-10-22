"""G1–G5: currency, payout guardrails, age rules, terms and curriculum ownership.

Two things are proved for every rule: that the admin can change it without a
deploy, and that the change actually reaches the code path it governs. A setting
that saves but is ignored is worse than no setting.
"""
from __future__ import annotations

import pytest
from factories import (
    make_assignment,
    make_opportunity,
    make_ops,
    make_project,
    make_skill,
    make_template,
    make_user,
)
from sqlalchemy import select

from app.core.errors import ApiError
from app.core.security import create_access_token
from app.models.admin import ROLE_SUPER_ADMIN, AuditLog
from app.models.platform import PlatformSettings
from app.services.money import ledger, payouts
from app.services.platform import settings as policy
from app.services.work import delivery

PREFIX = "/v1"


def _headers(user) -> dict:
    return {
        "Authorization": (
            f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
        )
    }


def test_defaults_are_naira_and_the_documented_guardrails(api) -> None:
    client, db = api

    response = client.get(f"{PREFIX}/platform/config")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["billing_currency"] == "NGN"
    assert body["payout_currency"] == "NGN"
    assert "NGN" in body["allowed_currencies"]
    assert body["min_student_age"] == 16
    assert body["guardian_consent_below_age"] == 18
    assert body["curriculum_owner"] == "Nelavista"
    assert "contributing work" in body["contributor_terms_body"].lower()
    # Reading the config materialised the row exactly once.
    assert len(db.scalars(select(PlatformSettings)).all()) == 1


def test_only_a_super_admin_can_change_platform_settings(api) -> None:
    client, db = api
    ops = make_ops(db)
    super_admin = make_user(db, ROLE_SUPER_ADMIN)

    refused = client.patch(
        f"{PREFIX}/platform/settings",
        json={"payout_currency": "USD"},
        headers=_headers(ops),
    )
    assert refused.status_code == 403

    changed = client.patch(
        f"{PREFIX}/platform/settings",
        json={"billing_currency": "USD", "payout_currency": "USD"},
        headers=_headers(super_admin),
    )
    assert changed.status_code == 200, changed.text
    assert changed.json()["billing_currency"] == "USD"

    # Ops can still read the policy it works under.
    read = client.get(f"{PREFIX}/platform/settings", headers=_headers(ops))
    assert read.status_code == 200
    assert read.json()["payout_currency"] == "USD"

    audit = db.scalar(
        select(AuditLog).where(AuditLog.action == "platform.settings_updated")
    )
    assert audit is not None
    assert audit.actor_user_id == super_admin.id
    assert audit.context["changes"]["billing_currency"] == {"from": "NGN", "to": "USD"}


def test_a_currency_must_be_allowed_before_it_can_be_selected(api) -> None:
    client, db = api
    super_admin = make_user(db, ROLE_SUPER_ADMIN)

    response = client.patch(
        f"{PREFIX}/platform/settings",
        json={"payout_currency": "CHF"},
        headers=_headers(super_admin),
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "currency_not_allowed"


def test_invalid_age_and_terms_settings_are_refused(api) -> None:
    client, db = api
    super_admin = make_user(db, ROLE_SUPER_ADMIN)

    bad_age = client.patch(
        f"{PREFIX}/platform/settings",
        json={"min_student_age": 30},
        headers=_headers(super_admin),
    )
    assert bad_age.status_code == 422 or bad_age.status_code == 400

    inverted = client.patch(
        f"{PREFIX}/platform/settings",
        json={"min_student_age": 20, "guardian_consent_below_age": 18},
        headers=_headers(super_admin),
    )
    assert inverted.status_code == 400
    assert inverted.json()["error"]["code"] == "invalid_setting"


def test_managed_opportunities_default_to_the_configured_currency(db) -> None:
    ops = make_ops(db)

    opportunity = make_opportunity(db, ops, currency=None)

    assert opportunity.currency == "NGN"
    assert opportunity.rate_minor == 1_000


def test_a_lowered_threshold_changes_who_must_approve(db) -> None:
    ops, creator, student, project, line = _payable_setup(db)
    row = policy.get_platform_settings(db)
    row.payout_second_approver_threshold_minor = 500
    db.flush()

    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    with pytest.raises(ApiError) as excinfo:
        payouts.approve_batch(db, creator, batch)
    assert excinfo.value.code == "second_approver_required"
    assert excinfo.value.details["threshold_minor"] == 500


def test_always_second_approver_blocks_self_approval_even_below_the_threshold(db) -> None:
    ops, creator, student, project, line = _payable_setup(db)
    row = policy.get_platform_settings(db)
    row.payout_second_approver_always = True
    db.flush()
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    with pytest.raises(ApiError) as excinfo:
        payouts.approve_batch(db, creator, batch)
    assert excinfo.value.code == "second_approver_required"


def test_an_unverified_recipient_blocks_the_payout_before_any_money_moves(db) -> None:
    ops, creator, student, project, line = _payable_setup(db)
    student.email_verified = False
    db.flush()
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])
    second = make_ops(db)
    payouts.approve_batch(db, second, batch)

    with pytest.raises(ApiError) as excinfo:
        payouts.pay_batch(db, second, batch)

    assert excinfo.value.code == "payout_blocked"
    assert excinfo.value.details["blocked"][str(student.id)] == ["email_unverified"]
    assert batch.status == "approved"


def test_work_eligibility_lists_every_missing_step(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.get(f"{PREFIX}/platform/me/eligibility", headers=_headers(student))

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["eligible"] is False
    assert body["blockers"] == ["date_of_birth_missing", "contributor_terms_required"]

    client.patch(f"{PREFIX}/me", json={"date_of_birth": "2000-01-01"}, headers=_headers(student))
    consent = client.post(
        f"{PREFIX}/me/consents",
        json={"kind": "contributor_terms", "document_version": "2026-10-01"},
        headers=_headers(student),
    )
    assert consent.status_code == 201, consent.text

    ready = client.get(f"{PREFIX}/platform/me/eligibility", headers=_headers(student))
    assert ready.json()["eligible"] is True
    assert ready.json()["age"] >= 18


def test_a_minor_needs_guardian_consent_before_paid_work(api) -> None:
    client, db = api
    student = make_user(db)
    client.patch(f"{PREFIX}/me", json={"date_of_birth": "2010-01-01"}, headers=_headers(student))
    client.post(
        f"{PREFIX}/me/consents",
        json={"kind": "contributor_terms", "document_version": "2026-10-01"},
        headers=_headers(student),
    )

    blocked = client.get(f"{PREFIX}/platform/me/eligibility", headers=_headers(student))
    assert "guardian_consent_required" in blocked.json()["blockers"]

    guardian = client.post(
        f"{PREFIX}/me/consents",
        json={"kind": "guardian_consent", "document_version": "2026-10-01"},
        headers=_headers(student),
    )
    assert guardian.status_code == 201, guardian.text

    allowed = client.get(f"{PREFIX}/platform/me/eligibility", headers=_headers(student))
    assert allowed.json()["eligible"] is True


def test_below_the_minimum_age_paid_work_stays_closed(api) -> None:
    client, db = api
    student = make_user(db)
    client.patch(f"{PREFIX}/me", json={"date_of_birth": "2015-01-01"}, headers=_headers(student))
    client.post(
        f"{PREFIX}/me/consents",
        json={"kind": "contributor_terms", "document_version": "2026-10-01"},
        headers=_headers(student),
    )

    response = client.get(f"{PREFIX}/platform/me/eligibility", headers=_headers(student))

    assert "under_minimum_age" in response.json()["blockers"]
    assert response.json()["eligible"] is False


def test_a_new_terms_version_asks_the_student_again(api) -> None:
    client, db = api
    super_admin = make_user(db, ROLE_SUPER_ADMIN)
    student = make_user(db)
    client.patch(f"{PREFIX}/me", json={"date_of_birth": "2000-01-01"}, headers=_headers(student))
    client.post(
        f"{PREFIX}/me/consents",
        json={"kind": "contributor_terms", "document_version": "2026-10-01"},
        headers=_headers(student),
    )

    bumped = client.patch(
        f"{PREFIX}/platform/settings",
        json={"contributor_terms_version": "2026-11-01"},
        headers=_headers(super_admin),
    )
    assert bumped.status_code == 200, bumped.text

    stale = client.post(
        f"{PREFIX}/me/consents",
        json={"kind": "contributor_terms", "document_version": "2026-10-01"},
        headers=_headers(student),
    )
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "stale_terms"

    status = client.get(f"{PREFIX}/platform/me/eligibility", headers=_headers(student))
    assert "contributor_terms_required" in status.json()["blockers"]


def test_the_funding_currency_falls_back_to_the_configured_billing_currency(db) -> None:
    ops = make_ops(db)
    opportunity = make_opportunity(db, ops, currency=None)
    project = make_project(db, ops, opportunity)
    # Simulate a project created before G1, with no currency of its own.
    opportunity.currency = None
    db.flush()

    transaction, split = ledger.fund_project(db, ops, project=project, total_minor=10_000)

    assert transaction.currency == "NGN"
    assert split.student_pool_minor + split.platform_fee_minor == 10_000


def _payable_setup(db, *, task_count: int = 1):
    ops = make_ops(db)
    creator = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    opportunity = make_opportunity(db, ops, rate_minor=1_000)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student, template=template)
    submission, _ = delivery.submit_work(
        db,
        student,
        assignment_id=assignment.id,
        payload={"label": "positive", "task_count": task_count},
        client_key="policy-1",
    )
    submission.status = "approved"
    db.flush()
    line = ledger.record_approval_earning(db, project=project, submission=submission)
    ledger.mark_payable(db, project)
    return ops, creator, student, project, line
