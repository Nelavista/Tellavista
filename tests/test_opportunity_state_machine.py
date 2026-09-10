"""Regression tests for services/opportunity_service.py's transition_application() and
its use in routes/admin_skills_routes.py's update_opportunity_application/delete_opportunity.

Before this existed, any status in _APPLICATION_STATUSES was accepted as a legal next
value from ANY current status -- a single PUT could take a brand-new 'applied' row
straight to 'paid' with payout_amount taken from the request body with no bound on it,
and deleting an Opportunity with existing applications had no guard at all.
"""
from app.extensions import db
from app.models import Skill, SkillCategory, Opportunity, OpportunityApplication, OpportunityStatusEvent


def _make_opportunity_and_application(student_id, status='applied', payment_amount=50000):
    category = SkillCategory(name='OppCat', slug='opp-cat', order=0)
    db.session.add(category)
    db.session.commit()
    skill = Skill(category_id=category.id, name='Opp Skill', slug='opp-skill', is_published=True)
    db.session.add(skill)
    db.session.commit()
    opp = Opportunity(skill_id=skill.id, title='Build an API', payment_amount=payment_amount, is_published=True)
    db.session.add(opp)
    db.session.commit()
    app_row = OpportunityApplication(opportunity_id=opp.id, student_id=student_id, status=status)
    db.session.add(app_row)
    db.session.commit()
    return opp.id, app_row.id


def test_applied_cannot_jump_straight_to_paid(app, client, make_user, login_as):
    admin = make_user('opp_sm_admin1', is_admin=True)
    student = make_user('opp_sm_student1')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='applied')
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                      json={'status': 'paid', 'payout_amount': 50000})
    assert res.status_code == 400

    with app.app_context():
        application = OpportunityApplication.query.get(application_id)
        assert application.status == 'applied'
        assert application.payout_amount is None
        assert OpportunityStatusEvent.query.filter_by(application_id=application_id).count() == 0


def test_applied_cannot_jump_straight_to_completed(app, client, make_user, login_as):
    admin = make_user('opp_sm_admin2', is_admin=True)
    student = make_user('opp_sm_student2')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='applied')
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}', json={'status': 'completed'})
    assert res.status_code == 400


def test_full_legal_chain_applied_to_accepted_to_completed_to_paid(app, client, make_user, login_as):
    admin = make_user('opp_sm_admin3', is_admin=True)
    student = make_user('opp_sm_student3')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='applied', payment_amount=50000)
    login_as(client, admin)

    for status in ('accepted', 'completed', 'paid'):
        res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                          json={'status': status, 'payout_amount': 50000})
        assert res.status_code == 200, f'transition to {status} should succeed'

    with app.app_context():
        events = OpportunityStatusEvent.query.filter_by(application_id=application_id).order_by(
            OpportunityStatusEvent.id).all()
        assert [e.to_status for e in events] == ['accepted', 'completed', 'paid']


def test_accepted_can_go_straight_to_paid(app, client, make_user, login_as):
    """Deliberately still allowed -- unlike skipping straight past 'accepted', this is an
    admin's real one-click 'the gig is done and I already paid them' workflow, not the
    vulnerability the state machine exists to close."""
    admin = make_user('opp_sm_admin4', is_admin=True)
    student = make_user('opp_sm_student4')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='accepted', payment_amount=50000)
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                      json={'status': 'paid', 'payout_amount': 30000})
    assert res.status_code == 200


def test_payout_amount_cannot_exceed_listed_amount(app, client, make_user, login_as):
    admin = make_user('opp_sm_admin5', is_admin=True)
    student = make_user('opp_sm_student5')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='completed', payment_amount=50000)
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                      json={'status': 'paid', 'payout_amount': 999999})
    assert res.status_code == 400

    with app.app_context():
        application = OpportunityApplication.query.get(application_id)
        assert application.status == 'completed'
        assert application.payout_amount is None


def test_payout_amount_cannot_be_negative(app, client, make_user, login_as):
    admin = make_user('opp_sm_admin6', is_admin=True)
    student = make_user('opp_sm_student6')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='completed', payment_amount=50000)
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                      json={'status': 'paid', 'payout_amount': -5000})
    assert res.status_code == 400


def test_terminal_statuses_reject_further_transitions(app, client, make_user, login_as):
    admin = make_user('opp_sm_admin7', is_admin=True)
    student = make_user('opp_sm_student7')
    with app.app_context():
        _, application_id = _make_opportunity_and_application(student.id, status='rejected')
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}', json={'status': 'accepted'})
    assert res.status_code == 400


def test_delete_opportunity_blocked_when_applications_exist(app, client, make_user, login_as):
    admin = make_user('opp_del_admin1', is_admin=True)
    student = make_user('opp_del_student1')
    with app.app_context():
        opp_id, application_id = _make_opportunity_and_application(student.id, status='paid', payment_amount=50000)
    login_as(client, admin)

    res = client.delete(f'/admin/api/opportunities/{opp_id}')
    assert res.status_code == 400

    with app.app_context():
        assert Opportunity.query.get(opp_id) is not None
        assert OpportunityApplication.query.get(application_id) is not None


def test_delete_opportunity_with_no_applications_still_succeeds(app, client, make_user, login_as):
    admin = make_user('opp_del_admin2', is_admin=True)
    with app.app_context():
        category = SkillCategory(name='OppDelCat', slug='opp-del-cat', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Opp Del Skill', slug='opp-del-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        opp = Opportunity(skill_id=skill.id, title='Clean Gig', payment_amount=1000, is_published=True)
        db.session.add(opp)
        db.session.commit()
        opp_id = opp.id
    login_as(client, admin)

    res = client.delete(f'/admin/api/opportunities/{opp_id}')
    assert res.status_code == 200
    with app.app_context():
        assert Opportunity.query.get(opp_id) is None
