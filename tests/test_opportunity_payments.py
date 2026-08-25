"""Every OpportunityApplication status change (especially marking something 'paid') must
be recorded in OpportunityStatusEvent -- an admin PUT is never just an untraceable flag
flip anymore."""
from extensions import db
from models import Skill, SkillCategory, Opportunity, OpportunityApplication, OpportunityStatusEvent


def _make_opportunity_and_application(app, student_id):
    with app.app_context():
        category = SkillCategory(name='Tech2', slug='tech2', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Backend Dev', slug='backend-dev', is_published=True)
        db.session.add(skill)
        db.session.commit()
        opp = Opportunity(skill_id=skill.id, title='Build an API', payment_amount=50000, is_published=True)
        db.session.add(opp)
        db.session.commit()
        app_row = OpportunityApplication(opportunity_id=opp.id, student_id=student_id, status='accepted')
        db.session.add(app_row)
        db.session.commit()
        return app_row.id


def test_marking_paid_writes_audit_event_and_actor(app, client, make_user, login_as):
    admin = make_user('pay_admin', is_admin=True)
    student = make_user('pay_student')
    application_id = _make_opportunity_and_application(app, student.id)
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                      json={'status': 'paid', 'payout_amount': 45000, 'payment_reference': 'BANK-REF-123'})
    assert res.status_code == 200
    data = res.get_json()['application']
    assert data['payment_reference'] == 'BANK-REF-123'
    assert data['paid_by_admin'] is not None

    with app.app_context():
        events = OpportunityStatusEvent.query.filter_by(application_id=application_id).all()
        assert len(events) == 1
        assert events[0].to_status == 'paid'
        assert events[0].from_status == 'accepted'
        assert events[0].actor_user_id == admin.id


def test_dispute_and_refund_states_are_representable(app, client, make_user, login_as):
    """The audit's business-readiness finding: there was no way to represent a clawback
    at all. Confirms 'disputed' and 'refunded' are now valid, trackable transitions."""
    admin = make_user('dispute_admin', is_admin=True)
    student = make_user('dispute_student')
    application_id = _make_opportunity_and_application(app, student.id)
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}',
                      json={'status': 'disputed', 'dispute_reason': 'Work not delivered as agreed'})
    assert res.status_code == 200
    assert res.get_json()['application']['dispute_reason'] == 'Work not delivered as agreed'

    res2 = client.put(f'/admin/api/opportunity-applications/{application_id}', json={'status': 'refunded'})
    assert res2.status_code == 200
    assert res2.get_json()['application']['refunded_at'] is not None

    with app.app_context():
        events = OpportunityStatusEvent.query.filter_by(application_id=application_id).order_by(OpportunityStatusEvent.id).all()
        assert [e.to_status for e in events] == ['disputed', 'refunded']


def test_invalid_status_rejected(app, client, make_user, login_as):
    admin = make_user('invalid_status_admin', is_admin=True)
    student = make_user('invalid_status_student')
    application_id = _make_opportunity_and_application(app, student.id)
    login_as(client, admin)

    res = client.put(f'/admin/api/opportunity-applications/{application_id}', json={'status': 'made_up_status'})
    assert res.status_code == 400
