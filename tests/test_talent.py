"""Nelavista Talent (/talent): public pages render, the honesty rules hold (no unverified
figures, samples always labelled and noindex), the Request Talent form validates and
stores leads, and the admin queue is admin-only."""
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
    'category': 'customer-support', 'headcount': '2-5', 'budget_range': 'discuss',
}


# ---------------------------------------------------------------- content rules

def test_hidden_figures_never_render():
    figures = tn.build_figures({'skill_count': 12, 'university_count': 1})
    keys = [f['key'] for f in figures]
    assert 'assessed' not in keys and 'introductions' not in keys   # value None = hidden
    assert all(f['value'] for f in figures)
    assert keys[:2] == ['reached', 'trained_ai']
    assert 'University live on Nelavista' in [f['label'] for f in figures]


def test_live_figures_skipped_when_zero():
    keys = [f['key'] for f in tn.build_figures({'skill_count': 0, 'university_count': 0})]
    assert 'skills' not in keys and 'universities' not in keys


def test_every_public_profile_is_marked_sample():
    assert tn.featured_talent() and all(p['is_sample'] for p in tn.featured_talent())
    for p in tn.SAMPLE_PROFILES:
        assert p['slug'].startswith('sample-')
        assert p['category'] in tn.CATEGORY_BY_SLUG
        assert set(p['checks']) == set(tn.CHECK_LABELS)


def test_no_logos_or_stories_shipped_without_consent():
    # These must only ever be filled with real, permitted material.
    assert tn.CLIENT_LOGOS == [] and tn.STORIES == []


# ---------------------------------------------------------------- pages

def test_home_renders_core_sections(tclient):
    r = tclient.get('/talent')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert '<title>Nelavista Talent | Hire Skilled African Talent</title>' in html
    assert 'Hire skilled African talent, without the hiring headache.' in html
    assert 'These are sample profiles.' in html
    for anchor in ('id="talent"', 'id="categories"', 'id="standard"', 'id="employers"', 'id="how"', 'id="join"'):
        assert anchor in html
    assert '2,500+' in html and '500+' in html
    assert 'Talent assessed' not in html     # unverified figure stays hidden
    assert 'Being added' in html and 'Live on Nelavista' in html


def test_profile_sample_is_noindex_and_labelled(tclient):
    r = tclient.get('/talent/profile/sample-adebayo-o')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'noindex' in html and 'Sample profile.' in html
    assert '/talent/request?profile=sample-adebayo-o' in html


def test_unknown_profile_404(tclient):
    assert tclient.get('/talent/profile/nobody').status_code == 404


def test_join_and_request_pages_render(tclient):
    assert tclient.get('/talent/join').status_code == 200
    r = tclient.get('/talent/request?category=technology')
    assert r.status_code == 200
    assert 'value="technology" selected' in r.get_data(as_text=True)


def test_request_prefills_category_from_profile(tclient):
    html = tclient.get('/talent/request?profile=sample-kwame-a').get_data(as_text=True)
    assert 'About Kwame A. (sample profile)' in html
    assert 'value="technology" selected' in html


def test_logged_in_incomplete_profile_is_not_bounced(tclient, make_user, login_as):
    user = make_user('halfdone', complete_profile=False)
    login_as(tclient, user)
    assert tclient.get('/talent').status_code == 200


# ---------------------------------------------------------------- request form

def test_valid_request_is_stored(tclient, talent_app):
    r = tclient.post('/talent/request', data=dict(VALID, profile_ref='sample-adebayo-o'))
    assert r.status_code == 302 and r.headers['Location'].endswith('/talent/request/received')
    with talent_app.app_context():
        row = TalentRequest.query.one()
        assert row.work_email == 'ada@example.com'
        assert row.status == 'new' and row.engagement_type == 'contract'
        assert row.profile_ref == 'sample-adebayo-o'
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
    r = tclient.get('/admin/talent-requests')
    assert r.status_code in (302, 403)


def test_admin_can_list_and_update(tclient, talent_app, make_user, login_as):
    tclient.post('/talent/request', data=VALID)
    login_as(tclient, make_user('boss', is_admin=True))
    html = tclient.get('/admin/talent-requests').get_data(as_text=True)
    assert 'Example Ltd' in html and 'Two chat support agents' in html
    with talent_app.app_context():
        rid = TalentRequest.query.one().id
    r = tclient.post(f'/admin/talent-requests/{rid}', data={'status': 'contacted', 'admin_notes': 'Called.'})
    assert r.status_code == 302
    with talent_app.app_context():
        row = db.session.get(TalentRequest, rid)
        assert row.status == 'contacted' and row.admin_notes == 'Called.'
