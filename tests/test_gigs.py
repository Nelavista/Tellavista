"""Gigs: availability/freshness, pay display, skill match, the provider adapters, the sync
(create/update/close/dedupe/failure isolation), the student feed and detail pages,
save / I-applied / share / apply hand-off, My Opportunities, and the admin guards."""
import json
from datetime import datetime, timedelta

import pytest

from app.extensions import db
from app.models import (
    Gig, GigProvider, GigSyncRun, GigSave, GigApplication, GigEvent,
    SkillCategory, Skill, StudentSkill, Opportunity,
)
from app.services.gigs import core, sync
from app.services.gigs.adapters import JobicyAdapter, JsonFeedAdapter, parse_feed, ProviderError

NOW = datetime(2026, 11, 17, 12, 0, 0)


@pytest.fixture(autouse=True)
def _no_dns(monkeypatch):
    """Adapters refuse private/unresolvable hosts. Tests never touch the network."""
    import app.services.link_fetch_service as lfs
    monkeypatch.setattr(lfs, '_is_safe_url', lambda url: url.startswith('https://'))


def _provider(**kw):
    base = dict(slug='prov', name='Prov', kind='api', adapter='json_feed', enabled=True, redistribution_confirmed=True,
                attribution_text='Prov', redistribution_basis='Terms allow it.', terms_url='https://prov.example/terms',
                api_base_url='https://prov.example/api', auth_method='none', auto_publish=True,
                sync_frequency_minutes=60, stale_after_hours=72, consecutive_failures=0)
    base.update(kw)
    return GigProvider(**base)


def _gig(provider, **kw):
    base = dict(slug=kw.pop('slug', 'react-dev'), provider_id=provider.id, source_gig_id=kw.pop('sid', '1'),
                origin='external', title='React Developer', organization='Acme', category='web_development',
                skills_json=json.dumps(['React', 'JavaScript', 'Git']), pay_min=100000, pay_max=150000,
                currency='NGN', pay_type='fixed', work_type='project', location_type='remote', location='Worldwide',
                application_url='https://acme.example/apply/1', source_url='https://prov.example/jobs/1',
                source_status='OPEN', last_verified_at=datetime.utcnow(), is_published=True, featured=False,
                is_archived=False, allows_in_app_view=False, application_mode='EXTERNAL',
                posted_at=datetime.utcnow() - timedelta(days=2), created_at=datetime.utcnow())
    base.update(kw)
    g = Gig(**base)
    g.provider = provider
    return g


def _setup(app, provider_kw=None, **gig_kw):
    with app.app_context():
        p = _provider(**(provider_kw or {}))
        db.session.add(p)
        db.session.flush()
        g = _gig(p, **gig_kw)
        db.session.add(g)
        db.session.commit()
        return p.id, g.id, g.slug


class FakeResp:
    def __init__(self, payload, status=200):
        self.status_code = status
        self.headers = {}
        self.content = json.dumps(payload).encode() if not isinstance(payload, bytes) else payload

    def close(self):
        pass


class FakeHttp:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params=None, headers=None, timeout=None, stream=False):
        self.calls.append((url, params, headers))
        r = self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]
        if isinstance(r, Exception):
            raise r
        return r


# ---------------------------------------------------------------- status

def test_status_open_closing_closed_expired_unknown():
    p = _provider()
    assert core.compute_status(_gig(p), NOW + timedelta(hours=1)) is not None
    g = _gig(p, last_verified_at=NOW - timedelta(hours=1))
    assert core.compute_status(g, NOW)['key'] == 'OPEN'
    g.deadline = (NOW + timedelta(hours=1) + timedelta(days=2)).date()
    assert core.compute_status(g, NOW)['key'] == 'CLOSING_SOON'
    g.deadline = (NOW - timedelta(days=2)).date()
    assert core.compute_status(g, NOW)['key'] == 'EXPIRED'
    g.deadline = None
    g.source_status = 'CLOSED'
    assert core.compute_status(g, NOW)['key'] == 'CLOSED'
    g.source_status = 'UNKNOWN'
    assert core.compute_status(g, NOW)['key'] == 'UNKNOWN'


def test_stale_open_gig_becomes_unknown_not_open():
    """An old import must not stay "open" forever."""
    p = _provider(stale_after_hours=72)
    g = _gig(p, last_verified_at=NOW - timedelta(hours=73))
    st = core.compute_status(g, NOW)
    assert st['key'] == 'UNKNOWN' and not st['accepting'] and st['label'] == 'Availability unknown'


def test_admin_override_and_manual_recheck_window():
    p = _provider()
    g = _gig(p, source_status='CLOSED', status_override='OPEN', last_verified_at=NOW)
    assert core.compute_status(g, NOW)['key'] == 'OPEN'
    g.status_override = 'CLOSED'
    g.source_status = 'OPEN'
    assert core.compute_status(g, NOW)['key'] == 'CLOSED'
    manual = _gig(p, origin='manual', status_override=None, last_verified_at=NOW - timedelta(days=15))
    assert core.compute_status(manual, NOW)['key'] == 'UNKNOWN'


def test_pay_formatting_never_invents_numbers():
    p = _provider()
    assert core.format_pay(_gig(p)) == '₦100,000–₦150,000'
    assert core.format_pay(_gig(p), compact=True) == '₦100k–₦150k'
    assert core.format_pay(_gig(p, pay_min=25, pay_max=None, currency='USD', pay_type='hourly')) == 'From $25/hr'
    assert core.format_pay(_gig(p, pay_min=None, pay_max=None, pay_text=None)) == 'Pay not stated'
    assert core.format_pay(_gig(p, pay_min=None, pay_max=None, pay_text='Paid per article')) == 'Paid per article'


def test_skill_match_only_with_real_data():
    p = _provider()
    g = _gig(p)
    assert core.skill_match(g, []) is None
    assert core.skill_match(_gig(p, skills_json='[]'), ['React']) is None
    m = core.skill_match(g, ['React Development', 'JavaScript', 'Python'])
    assert m['pct'] == 67 and set(m['matched']) == {'React', 'JavaScript'}
    assert core.skill_match(g, ['Accounting']) is None


def test_open_to_nigeria():
    assert core.open_to_nigeria('Worldwide') is True
    assert core.open_to_nigeria('USA only') is False
    assert core.open_to_nigeria('EMEA') is True
    assert core.open_to_nigeria(None) is True


# ---------------------------------------------------------------- adapters

def _jobicy_job(i, **kw):
    job = {'id': i, 'url': f'https://jobicy.com/jobs/{i}', 'jobTitle': f'Content Writer {i}', 'companyName': 'WriteCo',
           'jobIndustry': ['Copywriting'], 'jobType': ['contract'], 'jobGeo': 'Anywhere',
           'jobExcerpt': 'Write SEO blog posts.', 'jobDescription': '<p>Write <b>SEO</b> posts.</p><script>x()</script>',
           'pubDate': '2026-11-15T10:00:00+00:00', 'salaryMin': 500, 'salaryMax': 900, 'salaryCurrency': 'USD',
           'salaryPeriod': 'monthly'}
    job.update(kw)
    return job


def test_jobicy_normalize_and_filters():
    p = _provider(adapter='jobicy', config_json=json.dumps({}))
    a = JobicyAdapter(p, http=FakeHttp(FakeResp({'jobs': []})))
    ng = a.normalize_gig(_jobicy_job(1))
    assert ng.title == 'Content Writer 1' and ng.organization == 'WriteCo'
    assert ng.application_url == ng.source_url == 'https://jobicy.com/jobs/1'  # canonical Jobicy URL kept
    assert ng.category == 'content' and 'SEO' in ng.skills
    assert ng.pay_min == 500 and ng.currency == 'USD' and ng.pay_type == 'monthly'
    assert '<' not in ng.description and 'x()' not in ng.description
    assert ng.status == 'OPEN' and ng.posted_at == datetime(2026, 11, 15, 10, 0)
    assert a.normalize_gig(_jobicy_job(2, jobType=['full-time'])) is None       # salaried job, not a gig
    assert a.normalize_gig(_jobicy_job(3, jobGeo='USA Only')) is None           # not open to Nigeria
    assert a.normalize_gig(_jobicy_job(4, url='javascript:alert(1)')) is None   # unsafe link


def test_jobicy_status_endpoint_parsing():
    p = _provider(adapter='jobicy', api_base_url='https://jobicy.com/api/jobs')
    http = FakeHttp(FakeResp({'jobs': [{'id': 1, 'status': 'closed'}, {'id': 2, 'status': 'active'}, {'id': 3, 'status': 'unknown'}]}))
    out = JobicyAdapter(p, http=http).get_status(['1', '2', '3', '4'])
    assert out == {'1': 'CLOSED', '2': 'OPEN', '3': 'UNKNOWN', '4': 'UNKNOWN'}
    assert http.calls[0][0] == 'https://jobicy.com/api/jobs/status'


def test_json_feed_mapping_and_credentials_from_env(monkeypatch):
    monkeypatch.setenv('ACME_GIGS_KEY', 's3cret')
    cfg = {'items_path': 'data.gigs', 'fields': {'source_gig_id': 'id', 'title': 'name', 'organization': 'client',
           'application_url': 'apply', 'pay_min': 'budget', 'status': 'state', 'location': 'where', 'skills': 'tags'},
           'status_map': {'live': 'OPEN', 'filled': 'CLOSED'}, 'defaults': {'currency': 'NGN', 'category': 'design'}}
    p = _provider(config_json=json.dumps(cfg), auth_method='bearer', credentials_env='ACME_GIGS_KEY')
    http = FakeHttp(FakeResp({'data': {'gigs': [{'id': 'a1', 'name': 'Flyer design', 'client': 'Shop',
                                                 'apply': 'https://shop.example/a1', 'budget': '30k', 'state': 'live',
                                                 'where': 'Lagos', 'tags': ['Canva']}]}}))
    a = JsonFeedAdapter(p, http=http)
    raws = a.fetch_gigs()
    assert http.calls[0][2]['Authorization'] == 'Bearer s3cret'
    ng = a.normalize_gig(raws[0])
    assert (ng.title, ng.pay_min, ng.currency, ng.category, ng.status, ng.skills) == ('Flyer design', 30000, 'NGN', 'design', 'OPEN', ['Canva'])


def test_missing_credential_is_a_provider_error(monkeypatch):
    monkeypatch.delenv('NOPE_KEY', raising=False)
    p = _provider(auth_method='api_key_header', credentials_env='NOPE_KEY')
    with pytest.raises(ProviderError):
        JsonFeedAdapter(p, http=FakeHttp(FakeResp({}))).fetch_gigs()


def test_rss_parse():
    xml = b"""<?xml version="1.0"?><rss><channel><title>Feed</title>
      <item><title>Data entry project</title><link>https://feed.example/1</link><guid>g1</guid>
      <description>&lt;p&gt;Type up forms&lt;/p&gt;</description><category>Data Entry</category></item></channel></rss>"""
    items = parse_feed(xml)
    assert items[0]['title'] == 'Data entry project' and items[0]['guid'] == 'g1' and items[0]['categories'] == ['Data Entry']


# ---------------------------------------------------------------- sync

def _feed_provider(app, items, **kw):
    cfg = {'items_path': 'gigs', 'absence_means_closed': kw.pop('absence_means_closed', True),
           'fields': {'source_gig_id': 'id', 'title': 'title', 'organization': 'org', 'application_url': 'url',
                      'status': 'status'}}
    with app.app_context():
        p = _provider(config_json=json.dumps(cfg), **kw)
        db.session.add(p)
        db.session.commit()
        return p.id


def test_sync_creates_updates_closes_and_records_run(app):
    items = [{'id': 1, 'title': 'Logo design', 'org': 'A', 'url': 'https://a.example/1'},
             {'id': 2, 'title': 'Blog writer', 'org': 'B', 'url': 'https://b.example/2'}]
    pid = _feed_provider(app, items)
    with app.app_context():
        p = GigProvider.query.get(pid)
        run = sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        assert (run.status, run.fetched, run.created) == ('success', 2, 2)
        g1 = Gig.query.filter_by(source_gig_id='1').one()
        assert g1.is_published and g1.category == 'design' and g1.last_verified_at == NOW
        # Second sync: gig 1 updated, gig 2 gone -> closed (complete feed), gig 3 new.
        later = NOW + timedelta(hours=2)
        items2 = [{'id': 1, 'title': 'Logo design (updated)', 'org': 'A', 'url': 'https://a.example/1'},
                  {'id': 3, 'title': 'Video editor', 'org': 'C', 'url': 'https://c.example/3'}]
        run2 = sync.sync_provider(p, now=later, http=FakeHttp(FakeResp({'gigs': items2})))
        assert (run2.created, run2.updated, run2.closed) == (1, 1, 1)
        assert Gig.query.filter_by(source_gig_id='1').one().title == 'Logo design (updated)'
        gone = Gig.query.filter_by(source_gig_id='2').one()
        assert gone.source_status == 'CLOSED' and core.compute_status(gone, later)['key'] == 'CLOSED'
        assert p.last_status == 'success' and p.consecutive_failures == 0
        assert GigSyncRun.query.count() == 2


def test_sync_status_from_api_closes_gig(app):
    items = [{'id': 1, 'title': 'Social media manager', 'org': 'A', 'url': 'https://a.example/1', 'status': 'open'}]
    pid = _feed_provider(app, items)
    with app.app_context():
        p = GigProvider.query.get(pid)
        p.config_json = json.dumps({**p.config, 'status_map': {'open': 'OPEN', 'closed': 'CLOSED'}})
        sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        items[0]['status'] = 'closed'
        sync.sync_provider(p, now=NOW + timedelta(hours=2), http=FakeHttp(FakeResp({'gigs': items})))
        g = Gig.query.one()
        assert g.source_status == 'CLOSED' and not core.is_active(g, NOW + timedelta(hours=2))


def test_failed_sync_keeps_gigs_and_logs_error(app):
    items = [{'id': 1, 'title': 'Data analyst', 'org': 'A', 'url': 'https://a.example/1'}]
    pid = _feed_provider(app, items)
    with app.app_context():
        p = GigProvider.query.get(pid)
        sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        run = sync.sync_provider(p, now=NOW + timedelta(hours=2), http=FakeHttp(FakeResp({'error': 'x'}, status=503)))
        assert run.status == 'failed' and '503' in run.error
        assert p.last_status == 'failed' and p.consecutive_failures == 1 and p.last_error
        g = Gig.query.one()
        assert g.source_status == 'OPEN' and g.is_published and not g.is_archived
        # Backoff: the first failure retries at the normal interval, then it doubles.
        assert sync.effective_interval(p) == timedelta(minutes=60)
        p.consecutive_failures = 3
        assert sync.effective_interval(p) == timedelta(minutes=240)


def test_empty_fetch_never_mass_closes(app):
    items = [{'id': 1, 'title': 'Research assistant', 'org': 'A', 'url': 'https://a.example/1'}]
    pid = _feed_provider(app, items)
    with app.app_context():
        p = GigProvider.query.get(pid)
        sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        run = sync.sync_provider(p, now=NOW + timedelta(hours=2), http=FakeHttp(FakeResp({'gigs': []})))
        assert run.closed == 0 and 'Kept 1' in run.notes
        assert Gig.query.one().source_status == 'OPEN'


def test_absent_from_recent_feed_uses_status_not_absence(app):
    """Jobicy-style feeds only show recent jobs: absence alone never closes."""
    items = [{'id': 1, 'title': 'Customer support agent', 'org': 'A', 'url': 'https://a.example/1'},
             {'id': 2, 'title': 'Virtual assistant', 'org': 'B', 'url': 'https://b.example/2'}]
    pid = _feed_provider(app, items, absence_means_closed=False)
    with app.app_context():
        p = GigProvider.query.get(pid)
        sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        sync.sync_provider(p, now=NOW + timedelta(hours=2), http=FakeHttp(FakeResp({'gigs': items[:1]})))
        assert Gig.query.filter_by(source_gig_id='2').one().source_status == 'OPEN'


def test_duplicates_across_providers_are_hidden(app):
    items = [{'id': 'x', 'title': 'React Developer', 'org': 'Acme Ltd', 'url': 'https://acme.example/jobs/9?utm_source=a'}]
    pid1 = _feed_provider(app, items)
    with app.app_context():
        p2 = _provider(slug='prov2', name='Prov2', config_json=GigProvider.query.get(pid1).config_json)
        db.session.add(p2)
        db.session.commit()
        sync.sync_provider(GigProvider.query.get(pid1), now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        copy = [{'id': 'y', 'title': 'React developer!', 'org': 'ACME LTD', 'url': 'https://www.acme.example/jobs/9'}]
        run = sync.sync_provider(p2, now=NOW, http=FakeHttp(FakeResp({'gigs': copy})))
        assert run.duplicates == 1
        dup = Gig.query.filter_by(source_gig_id='y').one()
        assert dup.duplicate_of_id and not dup.is_published
        assert core.visible_query().count() == 1


def test_admin_edits_survive_sync_and_disabled_provider_never_syncs(app):
    items = [{'id': 1, 'title': 'Graphic designer', 'org': 'A', 'url': 'https://a.example/1'}]
    pid = _feed_provider(app, items)
    with app.app_context():
        p = GigProvider.query.get(pid)
        sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items})))
        g = Gig.query.one()
        g.title = 'Graphic designer (Canva)'
        g.locked_fields_json = json.dumps(['title'])
        db.session.commit()
        sync.sync_provider(p, now=NOW + timedelta(hours=2), http=FakeHttp(FakeResp({'gigs': items})))
        assert Gig.query.one().title == 'Graphic designer (Canva)'
        p.redistribution_confirmed = False
        db.session.commit()
        assert not sync.is_due(p, NOW + timedelta(days=1))
        assert sync.sync_provider(p, now=NOW, http=FakeHttp(FakeResp({'gigs': items}))).status == 'failed'


def test_provider_problems_require_terms_basis(app):
    with app.app_context():
        p = _provider(redistribution_confirmed=False, redistribution_basis=None, terms_url=None)
        problems = ' '.join(sync.provider_problems(p))
        assert 'terms' in problems.lower() and 'basis' in problems.lower()
        created = sync.ensure_default_providers()
        assert set(created) == {'manual', 'jobicy', 'naijalancers'}
        jobicy = GigProvider.query.filter_by(slug='jobicy').one()
        assert not jobicy.enabled and not jobicy.redistribution_confirmed
        naijalancers = GigProvider.query.filter_by(slug='naijalancers').one()
        assert naijalancers.enabled and naijalancers.kind == 'partner' and naijalancers.adapter == 'manual'
        assert naijalancers.attribution_text == 'Naijalancers'


# ---------------------------------------------------------------- student routes

def test_hub_shows_open_gigs_and_hides_unknown_closed_unpublished(app, client, make_user, login_as):
    user = make_user('gig_hub')
    pid, _, _ = _setup(app, title='React Developer')
    with app.app_context():
        p = GigProvider.query.get(pid)
        db.session.add_all([
            _gig(p, slug='stale', sid='2', title='Stale Gig', last_verified_at=datetime.utcnow() - timedelta(days=5)),
            _gig(p, slug='closed', sid='3', title='Closed Gig', source_status='CLOSED'),
            _gig(p, slug='draft', sid='4', title='Draft Gig', is_published=False),
        ])
        db.session.commit()
    login_as(client, user)
    body = client.get('/opportunities/gigs').get_data(as_text=True)
    assert 'React Developer' in body and '₦100k–₦150k' in body and 'via Prov' in body
    assert '1</strong> open gig' in body
    assert 'Closed Gig' not in body and 'Draft Gig' not in body
    open_part, unknown_part = body.split('Availability unknown <span', 1)
    assert 'Stale Gig' not in open_part and 'Stale Gig' in unknown_part


def test_hub_filters(app, client, make_user, login_as):
    user = make_user('gig_filter')
    pid, _, _ = _setup(app)
    with app.app_context():
        p = GigProvider.query.get(pid)
        db.session.add(_gig(p, slug='writer', sid='2', title='Blog Writer', category='content', skills_json='["SEO"]',
                            pay_min=20000, pay_max=None, location='USA only'))
        db.session.commit()
    login_as(client, user)
    assert 'Blog Writer' not in client.get('/opportunities/gigs?category=web_development').get_data(as_text=True)
    assert 'Blog Writer' in client.get('/opportunities/gigs?skill=seo').get_data(as_text=True)
    assert 'Blog Writer' not in client.get('/opportunities/gigs?min_pay=50000').get_data(as_text=True)
    assert 'Blog Writer' not in client.get('/opportunities/gigs?nigeria=1').get_data(as_text=True)
    assert 'React Developer' in client.get('/opportunities/gigs?q=react').get_data(as_text=True)


def test_nelavista_gigs_live_off_the_hub(app, client, make_user, login_as):
    """Ledger gigs aren't on the Gigs hub; they keep their own list (and Matched work)."""
    user = make_user('gig_nv')
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='gig-nv-cat')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='Gig Skill', slug='gig-nv-skill', is_published=True)
        db.session.add(skill)
        db.session.flush()
        db.session.add(Opportunity(skill_id=skill.id, title='Ledger gig', is_published=True, payment_amount=5000))
        db.session.commit()
    login_as(client, user)
    body = client.get('/opportunities/gigs').get_data(as_text=True)
    assert 'Ledger gig' not in body and 'Nelavista gigs' not in body
    assert 'Ledger gig' in client.get('/opportunities/gigs/nelavista').get_data(as_text=True)
    assert 'Ledger gig' in client.get('/opportunities').get_data(as_text=True)


def test_recommended_uses_tracked_skills_only(app, client, make_user, login_as):
    user = make_user('gig_rec')
    _setup(app)
    login_as(client, user)
    body = client.get('/opportunities/gigs').get_data(as_text=True)
    assert 'skill match' not in body and 'Recommended for you' not in body
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='gig-rec-cat')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='React', slug='gig-rec-react', is_published=True)
        db.session.add(skill)
        db.session.flush()
        db.session.add(StudentSkill(student_id=user.id, skill_id=skill.id, progress_pct=30))
        db.session.commit()
    body = client.get('/opportunities/gigs').get_data(as_text=True)
    assert '33% skill match' in body and 'Recommended for you' in body


def test_detail_view_logged_once_and_source_shown(app, client, make_user, login_as):
    user = make_user('gig_detail')
    _, gid, slug = _setup(app)
    login_as(client, user)
    body = client.get(f'/opportunities/gigs/{slug}').get_data(as_text=True)
    assert 'Currently accepting applications' in body and 'Application handled by Prov' in body
    assert 'This is not a Nelavista gig' in body and 'Apply on Prov' in body
    client.get(f'/opportunities/gigs/{slug}')
    with app.app_context():
        assert GigEvent.query.filter_by(gig_id=gid, event_type='gig_viewed').count() == 1


def test_unpublished_gig_404_for_students_and_disabled_provider_hides(app, client, make_user, login_as):
    user = make_user('gig_404')
    pid, gid, slug = _setup(app, is_published=False)
    login_as(client, user)
    assert client.get(f'/opportunities/gigs/{slug}').status_code == 404
    assert client.post(f'/opportunities/gigs/{gid}/save', json={'saved': True}).status_code == 404
    with app.app_context():
        g = Gig.query.get(gid)
        g.is_published = True
        GigProvider.query.get(pid).enabled = False
        db.session.commit()
    assert client.get(f'/opportunities/gigs/{slug}').status_code == 404


def test_apply_save_applied_share_and_my_opportunities(app, client, make_user, login_as):
    user = make_user('gig_flow')
    _, gid, slug = _setup(app)
    login_as(client, user)
    res = client.get(f'/opportunities/gigs/{slug}/apply?go=1')
    assert res.status_code == 302 and res.headers['Location'] == 'https://acme.example/apply/1'
    assert client.post(f'/opportunities/gigs/{gid}/save', json={'saved': True}).get_json()['saved'] is True
    data = client.post(f'/opportunities/gigs/{gid}/applied', json={'applied': True}).get_json()
    assert data['applied'] and data['applied_label'].startswith('Applied ')
    assert client.post(f'/opportunities/gigs/{gid}/share', json={'channel': 'whatsapp'}).get_json()['success']
    with app.app_context():
        assert GigApplication.query.filter_by(user_id=user.id, gig_id=gid).one().source == 'self_reported'
        assert GigSave.query.filter_by(user_id=user.id, gig_id=gid).count() == 1
        kinds = {e.event_type for e in GigEvent.query.filter_by(gig_id=gid).all()}
        assert {'apply_clicked', 'gig_saved', 'application_marked', 'gig_shared'} <= kinds
    applied = client.get('/opportunities/discover/mine?tab=applied').get_data(as_text=True)
    assert 'React Developer' in applied and 'via Prov' in applied
    assert 'React Developer' in client.get('/opportunities/discover/mine?tab=saved').get_data(as_text=True)
    client.post(f'/opportunities/gigs/{gid}/applied', json={'applied': False})
    with app.app_context():
        assert GigApplication.query.count() == 0


def test_in_app_view_frames_official_page(app, client, make_user, login_as):
    user = make_user('gig_frame')
    _, _, slug = _setup(app, allows_in_app_view=True)
    login_as(client, user)
    body = client.get(f'/opportunities/gigs/{slug}/apply').get_data(as_text=True)
    assert 'iframe' in body and 'https://acme.example/apply/1' in body and 'not run by Nelavista' in body


def test_gigs_stay_in_the_opportunities_space(app, client, make_user, login_as):
    user = make_user('gig_space')
    _, _, slug = _setup(app)
    login_as(client, user)
    for path in ('/opportunities/gigs', f'/opportunities/gigs/{slug}'):
        body = client.get(path).get_data(as_text=True)
        assert '/opportunities/discover' in body
        for leak in ('/skills/catalog', '/skills/my-learning', '/skills/projects', '/skills/talent', '/dashboard'):
            assert leak not in body, (path, leak)
    assert 'href="/opportunities/gigs"' in client.get('/opportunities/discover').get_data(as_text=True)


# ---------------------------------------------------------------- admin

def _admin(make_user):
    return make_user('gig_admin', is_admin=True)


def test_admin_manual_gig_flow(app, client, make_user, login_as):
    admin = _admin(make_user)
    login_as(client, admin)
    form = {'title': 'Event photographer', 'organization': 'Campus Media', 'category': 'design', 'skills': 'Photography, Lightroom',
            'pay_min': '40000', 'pay_max': '', 'currency': 'NGN', 'pay_type': 'fixed', 'work_type': 'project',
            'location_type': 'onsite', 'location': 'Lagos', 'application_url': 'https://campusmedia.example/apply',
            'external_reference': 'Email from hr@campusmedia.example, 2026-11-17'}
    res = client.post('/admin/gigs/new', data=form)
    assert res.status_code == 302
    with app.app_context():
        g = Gig.query.one()
        assert g.origin == 'manual' and g.provider.slug == 'manual' and not g.is_published
        gid = g.id
    client.post(f'/admin/gigs/{gid}/action', data={'action': 'publish'})
    with app.app_context():
        assert Gig.query.get(gid).is_published  # published, but "Availability unknown" until verified
        assert not core.is_active(Gig.query.get(gid))
    client.post(f'/admin/gigs/{gid}/action', data={'action': 'verify'})
    with app.app_context():
        assert core.is_active(Gig.query.get(gid))
    client.post(f'/admin/gigs/{gid}/action', data={'action': 'override', 'value': 'CLOSED'})
    with app.app_context():
        assert core.compute_status(Gig.query.get(gid))['key'] == 'CLOSED'
    assert client.get('/admin/gigs').status_code == 200
    assert client.get(f'/admin/gigs/{gid}/edit').status_code == 200


def test_admin_rejects_bad_urls_and_missing_source(app, client, make_user, login_as):
    admin = _admin(make_user)
    login_as(client, admin)
    res = client.post('/admin/gigs/new', data={'title': 'X', 'organization': 'Y', 'application_url': 'javascript:alert(1)'})
    assert res.status_code == 400
    client.post('/admin/gigs/new', data={'title': 'X', 'organization': 'Y', 'application_url': 'https://y.example/a'})
    with app.app_context():
        gid = Gig.query.one().id
    client.post(f'/admin/gigs/{gid}/action', data={'action': 'publish'})
    with app.app_context():
        assert not Gig.query.get(gid).is_published  # no source URL or reference recorded


def test_admin_provider_cannot_enable_without_terms_and_sync_now(app, client, make_user, login_as, monkeypatch):
    admin = _admin(make_user)
    login_as(client, admin)
    assert client.get('/admin/gigs/providers').status_code == 200
    with app.app_context():
        jid = GigProvider.query.filter_by(slug='jobicy').one().id
    res = client.post(f'/admin/gigs/providers/{jid}', data={'name': 'Jobicy', 'adapter': 'jobicy', 'kind': 'api',
                                                           'terms_url': 'https://jobicy.com/jobs-rss-feed',
                                                           'attribution_text': 'Jobicy', 'enabled': '1',
                                                           'sync_frequency_minutes': '180', 'stale_after_hours': '72'})
    assert res.status_code == 400
    with app.app_context():
        assert not GigProvider.query.get(jid).enabled
    client.post(f'/admin/gigs/providers/{jid}', data={'name': 'Jobicy', 'adapter': 'jobicy', 'kind': 'api',
                                                     'terms_url': 'https://jobicy.com/jobs-rss-feed', 'attribution_text': 'Jobicy',
                                                     'redistribution_basis': 'Fair use allows it with credit.',
                                                     'redistribution_confirmed': '1', 'enabled': '1',
                                                     'sync_frequency_minutes': '5', 'stale_after_hours': '72',
                                                     'config_json': '{"count": 10}', 'credentials_env': ''})
    with app.app_context():
        p = GigProvider.query.get(jid)
        assert p.enabled and p.sync_frequency_minutes == 60  # raised to the terms floor
    import requests
    monkeypatch.setattr(requests.Session, 'get', lambda self, *a, **k: FakeResp({'jobs': [_jobicy_job(7)]}))
    client.post(f'/admin/gigs/providers/{jid}/sync')
    with app.app_context():
        g = Gig.query.filter_by(source_gig_id='7').one()
        assert g.title == 'Content Writer 7' and not g.is_published  # auto_publish off: waits for review


def test_non_admin_blocked_and_metrics(app, client, make_user, login_as):
    user = make_user('gig_nonadmin')
    _, gid, slug = _setup(app)
    login_as(client, user)
    assert client.get('/admin/gigs').status_code in (302, 403)
    client.get(f'/opportunities/gigs/{slug}')
    client.get(f'/opportunities/gigs/{slug}/apply?go=1')
    with app.app_context():
        m = core.dashboard_metrics()
        assert m['students_viewing'] == 1 and m['students_clicking_apply'] == 1 and m['total_active'] == 1
        assert ('React', 4) in m['top_skills']
