"""Nelavista Talent (/talent): public pages render, the honesty rules hold (no invented
metrics, anonymous labelled previews, badges only for live checks, no student framing),
the Request Talent form validates and stores leads, and the admin queue is admin-only."""
import pytest

from app.extensions import db, limiter
from app.models import TalentRequest
from app.services import talent_network as tn


@pytest.fixture
def talent_app(app):
    from app.routes.talent_routes import talent_bp
    app.register_blueprint(talent_bp, url_prefix='/')
    try:
        limiter.reset()
    except Exception:
        pass
    return app


@pytest.fixture
def tclient(talent_app):
    return talent_app.test_client()


VALID = {
    'contact_name': 'Ada Okafor', 'company_name': 'Example Ltd', 'work_email': 'Ada@Example.com',
    'need_summary': 'Two chat support agents for evening cover.', 'engagement_type': 'contract',
    'category': 'customer-experience', 'headcount': '2-5', 'budget_range': 'discuss',
}


# ---------------------------------------------------------------- content rules

def test_metrics_hidden_until_enough_real_numbers(monkeypatch):
    assert all(m['value'] is None for m in tn.METRICS)       # nothing invented ships
    assert tn.build_metrics(None) == [] and tn.build_metrics(12) == []
    monkeypatch.setattr(tn, 'METRICS', [{'key': 'talent', 'label': 'Professionals', 'value': '120'}])
    keys = [m['key'] for m in tn.build_metrics(12)]
    assert keys == ['talent', 'categories', 'tracks']


def test_previews_are_anonymous_and_labelled():
    talent = tn.featured_talent()
    assert talent and all(p['is_preview'] for p in talent)
    for p in tn.PREVIEW_PROFILES:
        assert p['slug'].startswith('preview-')
        assert 'name' not in p and 'photo' not in p            # no invented people
        assert p['category'] in tn.CATEGORY_BY_SLUG


def test_badges_only_for_live_verified_layers():
    live = {layer['key'] for layer in tn.VETTING_LAYERS if layer['status'] == 'live'}
    for p in tn.PREVIEW_PROFILES:
        assert {b['key'] for b in tn.badges(p)} <= live
    fake = {'checks': {'identity': 'verified', 'skills': 'verified', 'practical': 'pending', 'profile': 'verified'}}
    keys = [b['key'] for b in tn.badges(fake)]
    assert 'identity' not in keys                              # rolling out: never a badge
    assert keys == ['skills', 'profile'] and not tn.is_vetted(fake)


def test_no_unconsented_proof_ships():
    assert tn.CLIENT_LOGOS == [] and tn.TESTIMONIALS == [] and tn.CASE_STUDIES == []


def test_whatsapp_link():
    assert tn.whatsapp_url().startswith('https://wa.me/2347087896654?text=')


# ---------------------------------------------------------------- pages

def test_home_renders_core_sections(tclient):
    r = tclient.get('/talent')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert '<title>Nelavista Talent | Hire Skilled African Talent</title>' in html
    assert 'Hire skilled African talent for the work that matters.' in html
    assert 'Not every profile makes the network.' in html
    assert 'Illustrative previews, not live candidates' in html
    for anchor in ('id="talent"', 'id="categories"', 'id="vetted"', 'id="employers"', 'id="how"', 'id="join"', 'id="about"'):
        assert anchor in html
    assert 'wa.me/2347087896654' in html
    assert 'images.unsplash.com' in html and 'srcset=' in html
    assert 'Rolling out' in html


def test_home_has_no_student_framing(tclient):
    html = tclient.get('/talent').get_data(as_text=True).lower()
    for word in ('student', 'universit', 'campus', '2,500'):
        assert word not in html


def test_profile_preview_is_noindex_and_labelled(tclient):
    r = tclient.get('/talent/profile/preview-frontend-developer')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'noindex' in html and 'Profile preview.' in html
    assert '/talent/request?profile=preview-frontend-developer' in html
    assert 'Rolling out across the network' in html            # identity shown honestly


def test_unknown_profile_404(tclient):
    assert tclient.get('/talent/profile/nobody').status_code == 404


def test_join_and_request_pages_render(tclient):
    assert tclient.get('/talent/join').status_code == 200
    r = tclient.get('/talent/request?category=technology')
    assert r.status_code == 200
    assert 'value="technology" selected' in r.get_data(as_text=True)


def test_request_prefills_category_from_profile(tclient):
    html = tclient.get('/talent/request?profile=preview-product-designer').get_data(as_text=True)
    assert 'Product Designer (UI/UX), Nigeria' in html
    assert 'value="design" selected' in html


def test_logged_in_incomplete_profile_is_not_bounced(tclient, make_user, login_as):
    login_as(tclient, make_user('halfdone', complete_profile=False))
    assert tclient.get('/talent').status_code == 200


# ---------------------------------------------------------------- request form

def test_valid_request_is_stored(tclient, talent_app):
    r = tclient.post('/talent/request', data=dict(VALID, profile_ref='preview-frontend-developer'))
    assert r.status_code == 302 and r.headers['Location'].endswith('/talent/request/received')
    with talent_app.app_context():
        row = TalentRequest.query.one()
        assert row.work_email == 'ada@example.com'
        assert row.status == 'new' and row.engagement_type == 'contract'
        assert row.category == 'customer-experience'
        assert row.profile_ref == 'preview-frontend-developer'
        assert row.timezone is None   # blank optional fields stored as NULL
    assert 'Thanks, Ada.' in tclient.get('/talent/request/received').get_data(as_text=True)


def test_invalid_request_shows_errors_and_saves_nothing(tclient, talent_app):
    r = tclient.post('/talent/request', data={'contact_name': 'X', 'work_email': 'not-an-email',
                                              'engagement_type': 'bogus', 'category': 'made-up'})
    assert r.status_code == 400
    html = r.get_data(as_text=True)
    assert 'Enter an email address we can reply to.' in html
    assert 'Choose how you want to engage.' in html
    with talent_app.app_context():
        assert TalentRequest.query.count() == 0


def test_honeypot_drops_bots_silently(tclient, talent_app):
    r = tclient.post('/talent/request', data=dict(VALID, company_fax='555-0100'))
    assert r.status_code == 302
    with talent_app.app_context():
        assert TalentRequest.query.count() == 0


# ---------------------------------------------------------------- admin

def test_admin_queue_is_admin_only(tclient, make_user, login_as):
    login_as(tclient, make_user('plainstudent'))
    assert tclient.get('/admin/talent-requests').status_code in (302, 403)


def test_admin_can_list_and_update(tclient, talent_app, make_user, login_as):
    tclient.post('/talent/request', data=VALID)
    login_as(tclient, make_user('boss', is_admin=True))
    html = tclient.get('/admin/talent-requests').get_data(as_text=True)
    assert 'Example Ltd' in html and 'Customer Experience' in html
    with talent_app.app_context():
        rid = TalentRequest.query.one().id
    r = tclient.post(f'/admin/talent-requests/{rid}', data={'status': 'contacted', 'admin_notes': 'Called.'})
    assert r.status_code == 302
    with talent_app.app_context():
        row = db.session.get(TalentRequest, rid)
        assert row.status == 'contacted' and row.admin_notes == 'Called.'


# ---------------------------------------------------------------- email alert

def test_new_request_emails_hello(tclient, talent_app):
    from app.extensions import mail
    with mail.record_messages() as outbox:
        r = tclient.post('/talent/request', data=dict(VALID, details='<b>Evenings</b> only'))
    assert r.status_code == 302
    assert len(outbox) == 1
    msg = outbox[0]
    assert msg.recipients == ['hello@nelavista.com']
    assert msg.reply_to == 'ada@example.com'                  # replying answers the employer
    assert msg.subject == 'New talent request: Example Ltd (Customer Experience)'
    assert 'Two chat support agents for evening cover.' in msg.body
    assert '/admin/talent-requests' in msg.body
    assert '&lt;b&gt;Evenings&lt;/b&gt;' in msg.html and '<b>Evenings</b>' not in msg.html  # user input escaped


def test_email_failure_never_loses_the_request(tclient, talent_app, monkeypatch):
    from app.extensions import mail

    def boom(_msg):
        raise OSError('SMTP down')
    monkeypatch.setattr(mail, 'send', boom)
    r = tclient.post('/talent/request', data=VALID)
    assert r.status_code == 302 and r.headers['Location'].endswith('/talent/request/received')
    with talent_app.app_context():
        assert TalentRequest.query.count() == 1


def test_honeypot_sends_no_email(tclient):
    from app.extensions import mail
    with mail.record_messages() as outbox:
        tclient.post('/talent/request', data=dict(VALID, company_fax='x'))
    assert outbox == []
