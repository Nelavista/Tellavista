"""Student opportunities (scholarships, fellowships, competitions...): deadline status,
visibility/verification rules, personalisation, save / I-applied / report / share, the
apply hand-off, and the admin publish/verify guards."""
import json
from datetime import date, datetime, timedelta

import pytest

from app.extensions import db
from app.models import (
    StudentOpportunity, StudentOpportunitySave, StudentOpportunityApplication,
    StudentOpportunityEvent, StudentOpportunityReport,
)
from app.services import student_opportunity_service as svc

TODAY = date(2026, 11, 16)


def _opp(**kw):
    base = dict(
        slug=kw.pop('slug', 'org-thing'), title='Thing', organization='Org', category='scholarship',
        location_scope='nigeria', application_mode='EXTERNAL_WEBVIEW', verification_status='verified',
        is_published=True, featured=False, is_rolling=False, is_partner=False, allows_in_app_view=False,
        manually_closed=False, is_archived=False, application_url='https://example.org/apply',
        source_url='https://example.org/news', deadline=TODAY + timedelta(days=30),
        verified_at=datetime.utcnow(), last_checked_at=datetime.utcnow(), published_at=datetime.utcnow(),
    )
    base.update(kw)
    return StudentOpportunity(**base)


def _add(app, **kw):
    with app.app_context():
        o = _opp(**kw)
        db.session.add(o)
        db.session.commit()
        return o.id, o.slug


# ---------------------------------------------------------------- pure status logic

@pytest.mark.parametrize('deadline_offset,key,label', [
    (30, 'open', 'Open'),
    (7, 'closing_soon', 'Closing in 7 days'),
    (3, 'closing_soon', 'Closing in 3 days'),
    (1, 'closing_soon', 'Closes tomorrow'),
    (0, 'closing_soon', 'Closes today'),
    (-1, 'closed', 'Closed'),
])
def test_compute_status_from_deadline(deadline_offset, key, label):
    st = svc.compute_status(_opp(deadline=TODAY + timedelta(days=deadline_offset)), today=TODAY)
    assert st['key'] == key and st['label'] == label


def test_upcoming_manual_close_archive_and_rolling():
    assert svc.compute_status(_opp(opens_at=TODAY + timedelta(days=5)), today=TODAY)['key'] == 'upcoming'
    assert svc.compute_status(_opp(manually_closed=True), today=TODAY)['key'] == 'closed'
    assert svc.compute_status(_opp(is_archived=True), today=TODAY)['key'] == 'closed'
    assert svc.compute_status(_opp(deadline=None, is_rolling=True), today=TODAY)['key'] == 'open'


def test_department_and_level_mapping():
    assert svc.discipline_for_department('Computer Science') == 'computer_science'
    assert svc.discipline_for_department('Mathematics') == 'mathematics'
    assert svc.discipline_for_department('Accounting') == 'accounting'
    assert svc.discipline_for_department('Mass Communication') == 'social_sciences'
    assert svc.level_key_for_user('200 Level') == '200'
    assert svc.level_key_for_user('600') == '500'
    assert svc.level_key_for_user(None) is None


def test_personalisation_widens_but_never_hides_general():
    maths = {'discipline': 'mathematics', 'level': '200', 'university': None}
    finance = _opp(disciplines_json=json.dumps(['finance']))
    ai = _opp(disciplines_json=json.dumps(['computer_science']), tags_json=json.dumps(['AI', 'data']))
    general = _opp(disciplines_json=json.dumps(['all']))
    law = _opp(disciplines_json=json.dumps(['law']))
    final_year_only = _opp(disciplines_json=json.dumps(['all']), levels_json=json.dumps(['final_year']))
    assert svc.is_for_you(finance, maths)          # related discipline
    assert svc.is_for_you(ai, maths)               # AI/data tags
    assert svc.is_for_you(general, maths)          # open to all
    assert not svc.is_for_you(law, maths)
    assert not svc.is_for_you(final_year_only, maths)
    assert svc.relevance_score(general, maths) > 0
    assert svc.relevance_score(finance, maths) > svc.relevance_score(law, maths)


def test_search_and_filters():
    o = _opp(title='Campus Ambassador Programme', organization='Cowrywise', category='campus_ambassador',
             disciplines_json=json.dumps(['finance', 'marketing']), tags_json=json.dumps(['fintech', 'LASU']))
    assert svc.matches_search(o, 'campus ambassador')
    assert svc.matches_search(o, 'cowrywise finance')
    assert svc.matches_search(o, 'lasu')
    assert not svc.matches_search(o, 'hackathon')
    assert svc.apply_filters([o], category='campus_ambassador', today=TODAY) == [o]
    assert svc.apply_filters([o], discipline='law', today=TODAY) == []
    assert svc.apply_filters([o], deadline='week', today=TODAY) == []
    assert svc.apply_filters([o], deadline='month', today=TODAY) == [o]


# ---------------------------------------------------------------- routes

def test_feed_hides_unverified_unpublished_closed(app, client, make_user, login_as):
    user = make_user('opp_feed')
    _add(app, slug='live-one', title='Live Scholarship')
    _add(app, slug='draft-one', title='Draft Thing', is_published=False)
    _add(app, slug='unverified-one', title='Rumour Thing', verification_status='unverified')
    _add(app, slug='closed-one', title='Expired Thing', deadline=date(2020, 1, 1))
    _add(app, slug='archived-one', title='Archived Thing', is_archived=True)
    login_as(client, user)
    html = client.get('/opportunities/discover').get_data(as_text=True)
    assert 'Live Scholarship' in html
    for hidden in ('Draft Thing', 'Rumour Thing', 'Expired Thing', 'Archived Thing'):
        assert hidden not in html
    archive = client.get('/opportunities/discover/archive').get_data(as_text=True)
    assert 'Expired Thing' in archive and 'Draft Thing' not in archive and 'Rumour Thing' not in archive


def test_detail_404_for_unverified_and_view_logged_once(app, client, make_user, login_as):
    user = make_user('opp_detail')
    oid, slug = _add(app, slug='detail-one', title='Detail Scholarship')
    _add(app, slug='secret-one', verification_status='unverified')
    login_as(client, user)
    assert client.get('/opportunities/discover/secret-one').status_code == 404
    res = client.get(f'/opportunities/discover/{slug}')
    html = res.get_data(as_text=True)
    assert res.status_code == 200
    assert 'APPLY NOW' in html and 'Verified by Nelavista' in html
    client.get(f'/opportunities/discover/{slug}')
    with app.app_context():
        assert StudentOpportunityEvent.query.filter_by(opportunity_id=oid, event_type='view').count() == 1


def test_search_and_category_filter_routes(app, client, make_user, login_as):
    user = make_user('opp_search')
    _add(app, slug='hack', title='AI Hackathon', category='hackathon', tags_json=json.dumps(['AI']))
    _add(app, slug='schol', title='Merit Scholarship', category='scholarship')
    login_as(client, user)
    html = client.get('/opportunities/discover?q=hackathon').get_data(as_text=True)
    assert 'AI Hackathon' in html and 'Merit Scholarship' not in html
    html = client.get('/opportunities/discover?category=scholarship').get_data(as_text=True)
    assert 'Merit Scholarship' in html and 'AI Hackathon' not in html


def test_save_applied_and_my_opportunities(app, client, make_user, login_as):
    user = make_user('opp_saver')
    oid, slug = _add(app, slug='save-me', title='Saveable Fellowship', deadline=TODAY + timedelta(days=400))
    login_as(client, user)
    assert client.post(f'/opportunities/discover/{oid}/save', json={'saved': True}).get_json()['saved'] is True
    assert client.post(f'/opportunities/discover/{oid}/save', json={'saved': True}).status_code == 200  # idempotent
    res = client.post(f'/opportunities/discover/{oid}/applied', json={'applied': True}).get_json()
    assert res['applied'] is True and res['applied_label'].startswith('Applied ')
    with app.app_context():
        assert StudentOpportunitySave.query.filter_by(user_id=user.id).count() == 1
        app_row = StudentOpportunityApplication.query.filter_by(user_id=user.id).one()
        assert app_row.source == 'self_reported'
    assert 'Saveable Fellowship' in client.get('/opportunities/discover/mine?tab=saved').get_data(as_text=True)
    applied_html = client.get('/opportunities/discover/mine?tab=applied').get_data(as_text=True)
    assert 'Saveable Fellowship' in applied_html and 'Applied' in applied_html
    client.post(f'/opportunities/discover/{oid}/applied', json={'applied': False})
    client.post(f'/opportunities/discover/{oid}/save', json={'saved': False})
    with app.app_context():
        assert StudentOpportunityApplication.query.count() == 0
        assert StudentOpportunitySave.query.count() == 0
        types = {e.event_type for e in StudentOpportunityEvent.query.all()}
        assert {'save', 'unsave', 'applied', 'unapplied'} <= types


def test_cannot_save_hidden_opportunity(app, client, make_user, login_as):
    user = make_user('opp_hidden')
    oid, _ = _add(app, slug='hidden', is_published=False)
    login_as(client, user)
    assert client.post(f'/opportunities/discover/{oid}/save', json={'saved': True}).status_code == 404


def test_apply_redirects_to_official_url_and_logs_click(app, client, make_user, login_as):
    user = make_user('opp_apply')
    oid, slug = _add(app, slug='apply-me', application_url='https://official.example.org/form')
    login_as(client, user)
    res = client.get(f'/opportunities/discover/{slug}/apply?go=1')
    assert res.status_code == 302 and res.headers['Location'] == 'https://official.example.org/form'
    with app.app_context():
        assert StudentOpportunityEvent.query.filter_by(opportunity_id=oid, event_type='apply_click').count() == 1


def test_in_app_view_frames_official_page(app, client, make_user, login_as):
    user = make_user('opp_frame')
    _, slug = _add(app, slug='frame-me', allows_in_app_view=True, framing_checked_at=datetime.utcnow())
    login_as(client, user)
    html = client.get(f'/opportunities/discover/{slug}/apply').get_data(as_text=True)
    assert '<iframe class="opp-frame" src="https://example.org/apply"' in html
    assert 'Open in browser' in html and 'not run by Nelavista' in html


def test_report_and_share(app, client, make_user, login_as):
    user = make_user('opp_reporter')
    oid, _ = _add(app, slug='report-me')
    login_as(client, user)
    assert client.post(f'/opportunities/discover/{oid}/report', json={'reason': 'bogus'}).status_code == 400
    assert client.post(f'/opportunities/discover/{oid}/report', json={'reason': 'broken_link', 'details': 'dead'}).get_json()['success']
    assert client.post(f'/opportunities/discover/{oid}/share', json={'channel': 'whatsapp'}).get_json()['success']
    with app.app_context():
        assert StudentOpportunityReport.query.filter_by(opportunity_id=oid).one().reason == 'broken_link'
        assert StudentOpportunityEvent.query.filter_by(event_type='share', channel='whatsapp').count() == 1


def test_gig_apply_endpoint_still_works_and_gigs_page_intact(app, client, make_user, login_as):
    """The paid-gig flow kept its URLs when /opportunities/discover became the hub."""
    from app.models import SkillCategory, Skill, Opportunity, OpportunityApplication
    user = make_user('gig_student')
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='gig-cat')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='Gig Skill', slug='gig-skill', is_published=True)
        db.session.add(skill)
        db.session.flush()
        gig = Opportunity(skill_id=skill.id, title='Paid design gig', is_published=True, payment_amount=1000)
        db.session.add(gig)
        db.session.commit()
        gig_id = gig.id
    login_as(client, user)
    assert 'Paid design gig' in client.get('/opportunities/gigs').get_data(as_text=True)
    client.post(f'/opportunities/{gig_id}/apply')
    with app.app_context():
        assert OpportunityApplication.query.filter_by(opportunity_id=gig_id, student_id=user.id).count() == 1


# ---------------------------------------------------------------- admin

def _form(**kw):
    data = {
        'title': 'Test Fellowship', 'organization': 'Test Org', 'category': 'fellowship',
        'summary': 'A fellowship.', 'deadline': (TODAY + timedelta(days=400)).isoformat(),
        'application_url': 'https://test.example.org/apply', 'source_url': 'https://test.example.org/news',
        'official_website': 'https://test.example.org', 'location_scope': 'nigeria',
        'application_mode': 'EXTERNAL_WEBVIEW', 'disciplines': ['all'],
    }
    data.update(kw)
    return data


def test_admin_create_verify_publish_flow(app, client, make_user, login_as):
    admin = make_user('opp_admin', is_admin=True)
    login_as(client, admin)
    res = client.post('/admin/opportunities/new', data=_form())
    assert res.status_code == 302
    with app.app_context():
        opp = StudentOpportunity.query.filter_by(title='Test Fellowship').one()
        oid = opp.id
        assert opp.is_published is False and opp.verification_status == 'unverified'
        assert opp.disciplines == ['all']
    # Publishing before verification is refused server-side.
    client.post(f'/admin/opportunities/{oid}/action', data={'action': 'publish'})
    with app.app_context():
        assert StudentOpportunity.query.get(oid).is_published is False
    client.post(f'/admin/opportunities/{oid}/action', data={'action': 'verify'})
    client.post(f'/admin/opportunities/{oid}/action', data={'action': 'publish'})
    with app.app_context():
        opp = StudentOpportunity.query.get(oid)
        assert opp.is_verified and opp.is_published and opp.verified_by_id == admin.id and opp.published_at
    assert client.get('/admin/opportunities').status_code == 200
    assert client.get(f'/admin/opportunities/{oid}/edit').status_code == 200


def test_admin_cannot_verify_without_source_or_publish_closed(app, client, make_user, login_as):
    admin = make_user('opp_admin2', is_admin=True)
    login_as(client, admin)
    client.post('/admin/opportunities/new', data=_form(title='No Source', source_url=''))
    client.post('/admin/opportunities/new', data=_form(title='Old One', deadline='2020-01-01'))
    with app.app_context():
        no_src = StudentOpportunity.query.filter_by(title='No Source').one().id
        old = StudentOpportunity.query.filter_by(title='Old One').one().id
    client.post(f'/admin/opportunities/{no_src}/action', data={'action': 'verify'})
    client.post(f'/admin/opportunities/{old}/action', data={'action': 'verify'})
    client.post(f'/admin/opportunities/{old}/action', data={'action': 'publish'})
    with app.app_context():
        assert StudentOpportunity.query.get(no_src).verification_status == 'unverified'
        assert StudentOpportunity.query.get(old).is_verified
        assert StudentOpportunity.query.get(old).is_published is False


def test_admin_rejects_partner_mode_without_partnership_and_bad_urls(app, client, make_user, login_as):
    admin = make_user('opp_admin3', is_admin=True)
    login_as(client, admin)
    res = client.post('/admin/opportunities/new', data=_form(application_mode='NELAVISTA_APPLICATION'))
    assert res.status_code == 400 and 'partnered with Nelavista' in res.get_data(as_text=True)
    res = client.post('/admin/opportunities/new', data=_form(application_url='javascript:alert(1)'))
    assert res.status_code == 400
    with app.app_context():
        assert StudentOpportunity.query.count() == 0


def test_partner_mode_without_workflow_still_uses_official_url():
    o = _opp(application_mode='NELAVISTA_APPLICATION', is_partner=True)
    assert svc.effective_application_mode(o) == 'EXTERNAL_WEBVIEW'


def test_admin_delete_blocked_when_students_saved(app, client, make_user, login_as):
    admin = make_user('opp_admin4', is_admin=True)
    student = make_user('opp_student4')
    oid, _ = _add(app, slug='keep-me')
    with app.app_context():
        db.session.add(StudentOpportunitySave(user_id=student.id, opportunity_id=oid))
        db.session.commit()
    login_as(client, admin)
    client.post(f'/admin/opportunities/{oid}/delete')
    with app.app_context():
        assert StudentOpportunity.query.get(oid) is not None


def test_non_admin_cannot_reach_admin(app, client, make_user, login_as):
    user = make_user('opp_nonadmin')
    login_as(client, user)
    res = client.get('/admin/opportunities')
    assert res.status_code in (302, 403)


# ---------------------------------------------------------------- manifest seed

def test_seed_only_verifies_and_publishes_when_rules_pass(app):
    from scripts.seed.seed_student_opportunities import run
    future = (TODAY + timedelta(days=400)).isoformat()
    entries = [
        {'title': 'Checked', 'organization': 'Org A', 'category': 'scholarship', 'deadline': future,
         'application_url': 'https://a.example.org/apply', 'source_url': 'https://a.example.org/news',
         'verified_on': '2026-11-16', 'publish': True, 'disciplines': ['all']},
        {'title': 'Rumour', 'organization': 'Org B', 'deadline': future,
         'application_url': 'https://b.example.org/apply', 'source_url': 'https://b.example.org', 'publish': True},
        {'title': 'Expired', 'organization': 'Org C', 'deadline': '2020-01-01', 'verified_on': '2026-11-16',
         'application_url': 'https://c.example.org/apply', 'source_url': 'https://c.example.org', 'publish': True},
        {'title': 'Bad link', 'organization': 'Org D', 'application_url': 'ftp://nope'},
    ]
    with app.app_context():
        report = run(entries, apply=True)
        assert report['created'] == 3 and report['invalid'] == 1 and report['published'] == 1
        rows = {o.title: o for o in StudentOpportunity.query.all()}
        assert rows['Checked'].is_published and rows['Checked'].is_verified
        assert not rows['Rumour'].is_published and rows['Rumour'].verification_status == 'unverified'
        assert rows['Expired'].is_verified and not rows['Expired'].is_published
        assert run(entries, apply=True)['updated'] == 3  # idempotent upsert


def test_discover_lives_in_the_opportunities_space(app, client, make_user, login_as):
    """Discover uses the Opportunities shell and never shows another space's navigation
    (see tests/test_space_separation.py)."""
    user = make_user('opp_space')
    _, slug = _add(app, slug='space-check', title='Space Check Scholarship')
    login_as(client, user)
    for path in ('/opportunities/discover', f'/opportunities/discover/{slug}', '/opportunities/discover/mine'):
        body = client.get(path).get_data(as_text=True)
        assert '/opportunities/gigs' in body
        for leak in ('/skills/catalog', '/skills/my-learning', '/skills/projects', '/skills/talent', '/dashboard'):
            assert leak not in body, (path, leak)
    assert '/opportunities/discover' in client.get('/opportunities').get_data(as_text=True)


def test_space_nav_order_is_discover_gigs_matched(app, client, make_user, login_as):
    """Product order for the Opportunities space: Discover first, then gigs, then
    matched work, in both the sidebar and the mobile tab bar."""
    user = make_user('opp_nav_order')
    login_as(client, user)
    body = client.get('/opportunities/discover').get_data(as_text=True)
    sidebar, tabbar = body.split('class="mobile-tabbar"', 1)
    for section in (sidebar.split('class="sidebar-nav"', 1)[1], tabbar):
        positions = [section.index(f'href="{href}"')
                     for href in ('/opportunities/discover', '/opportunities/gigs', '/opportunities')]
        assert positions == sorted(positions), positions
