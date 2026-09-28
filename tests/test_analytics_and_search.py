"""PRD §21 observability batch: PostHog product analytics (gap G5) and Postgres
full-text search over Materials (gap G7).

Analytics contract: without POSTHOG_API_KEY every capture is a no-op that must never
raise into the route it measures (same best-effort bar as ai_monitoring.log_ai_usage);
with a key the event goes out on the client with the route-owned properties. The
client is faked at the module boundary (app.services.analytics.capture) so no test
ever touches the network.

Search contract: on SQLite (this suite's dialect) material_search_filter is the
original OR-of-ILIKEs byte-for-byte -- same matches as before the FTS work, plus
LIKE-metacharacter escaping. Postgres-only behavior (weights, websearch syntax,
rank ordering) is enforced by the migration + service staying textually in sync and
is not exercised here.
"""
import pytest

from app.extensions import db
from app.models import Material
from app.services import analytics, search_service


# ---------------------------------------------------------------- analytics --

@pytest.fixture(autouse=True)
def _reset_analytics_state():
    """Isolate the module-level lazy client between tests (init happens once per
    process; a key flipped mid-suite must still re-evaluate)."""
    analytics._client = None
    analytics._initialized = False
    yield
    analytics._client = None
    analytics._initialized = False


def test_capture_is_noop_without_key(monkeypatch):
    """The env-gating contract: no key -> no client, no call, no raise."""
    monkeypatch.setattr(analytics, 'POSTHOG_API_KEY', None)
    analytics.capture('user:x', analytics.EVENT_SIGNUP)  # must not raise
    assert analytics._get_client() is None


def test_capture_never_raises_with_client(monkeypatch):
    """A exploding PostHog client must never break the route that called it."""
    monkeypatch.setattr(analytics, 'POSTHOG_API_KEY', 'phc_test')
    # _initialized=False so _get_client() actually builds a client through the faked
    # posthog module below, and capture() exercises the real call-and-swallow path.
    analytics._initialized = False
    analytics._client = None

    import sys
    class _Boom:
        def capture(self, *a, **k):
            raise RuntimeError('posthog down')
    monkeypatch.setitem(sys.modules, 'posthog',
                        type('m', (), {'Posthog': lambda *a, **k: _Boom()}))
    analytics.capture('user:x', analytics.EVENT_CBT_SUBMITTED, {'score_pct': 80})


def test_signup_emits_event(client, monkeypatch):
    """Route wiring: a real password signup emits user_signup with method=password,
    carrying countable properties but never the password."""
    monkeypatch.setattr(analytics, 'POSTHOG_API_KEY', 'phc_test')
    captured = []
    monkeypatch.setattr(analytics, 'capture',
                        lambda did, ev, props=None: captured.append((did, ev, props)))

    res = client.post('/signup', data={
        'username': 'funneluser', 'email': 'funneluser@example.com',
        'password': 'Passw0rd123', 'name': 'Funnel User',
        'university': 'Lagos State University', 'faculty': 'Science',
        'department': 'Computer Science', 'level': '200',
    }, follow_redirects=True)
    assert res.status_code == 200

    events = [c for c in captured if c[1] == analytics.EVENT_SIGNUP]
    assert len(events) == 1
    did, _, props = events[0]
    assert did == 'user:funneluser'
    assert props == {'method': 'password'}


def test_cbt_submit_emits_scored_event(app, client, make_user, login_as, monkeypatch):
    """Route wiring: an auto-scored submit emits cbt_submitted with the score."""
    from datetime import datetime
    import json as _json
    from app.models import CBTAttempt, CBTQuestion

    user = make_user('cbtfunnel')
    login_as(client, user)

    with app.app_context():
        q = CBTQuestion(subject_code='CSC', course_code='CSC213', question_type='cbt',
                        question_text='2+2=?', options_json=_json.dumps(['3', '4', '5', '6']),
                        correct_index=1, explanation='basic')
        db.session.add(q)
        db.session.flush()
        attempt = CBTAttempt(user_id=user.id, course_code='CSC213', question_type='cbt',
                             total_questions=1, correct_count=0, score_pct=0)
        attempt.issued_question_ids = [q.id]
        db.session.add(attempt)
        db.session.commit()
        attempt_id, qid = attempt.id, q.id

    monkeypatch.setattr(analytics, 'POSTHOG_API_KEY', 'phc_test')
    captured = []
    monkeypatch.setattr(analytics, 'capture',
                        lambda did, ev, props=None: captured.append((did, ev, props)))

    res = client.post(f'/CBT/submit/{attempt_id}',
                      json={'answers': {str(qid): 1}, 'duration_seconds': 45})
    assert res.status_code == 200

    events = [c for c in captured if c[1] == analytics.EVENT_CBT_SUBMITTED]
    assert len(events) == 1
    did, _, props = events[0]
    assert did == 'user:cbtfunnel'
    assert props['question_type'] == 'cbt'
    assert props['score_pct'] == 100


def test_ai_usage_mirror_emits_event(app, monkeypatch):
    """ai_provider's best-effort hook mirrors each AI call into analytics: with an app
    context, _log_usage both writes the DB usage row and emits the ai_call event with
    aggregate properties only."""
    from app.models import AIUsageLog
    from app.services.ai_provider import OpenRouterProvider as AIProvider

    monkeypatch.setattr(analytics, 'POSTHOG_API_KEY', 'phc_test')
    captured = []
    monkeypatch.setattr(analytics, 'capture',
                        lambda did, ev, props=None: captured.append((did, ev, props)))

    with app.app_context():
        AIProvider._log_usage(user_id=42, feature='tutor_chat', model='test-model',
                              prompt_tokens=11, completion_tokens=7, ok=True)
        assert AIUsageLog.query.count() == 1  # the DB-side log still runs

    assert len(captured) == 1
    did, ev, props = captured[0]
    assert (did, ev) == ('user:42', analytics.EVENT_AI_CALL)
    assert props == {'feature': 'tutor_chat', 'model': 'test-model', 'ok': True}


# ------------------------------------------------------------------- search --

@pytest.fixture
def seeded_materials(app):
    """Three approved materials in one department + one unapproved (search must
    respect the caller's is_approved scoping -- the filter only narrows)."""
    with app.app_context():
        rows = [
            Material(title='Data Structures Handbook', department='Computer Science',
                     level='200', semester='First Semester', is_approved=True,
                     course_code='CSC213', description='Trees, graphs and complexity'),
            Material(title='Organic Chemistry Notes', department='Computer Science',
                     level='200', semester='First Semester', is_approved=True,
                     course_code='CHM101', description='Benzene rings'),
            Material(title='Hidden Gem', department='Computer Science',
                     level='200', semester='First Semester', is_approved=False,
                     course_code='CSC213', description='Data structures galore'),
        ]
        db.session.add_all(rows)
        db.session.commit()
        return [r.id for r in rows]


def test_sqlite_filter_matches_like_behavior(app, seeded_materials):
    """On this suite's SQLite dialect the FTS filter degrades to the original
    OR-of-ILIKEs: same three-column matching, applied as a composable clause."""
    with app.app_context():
        query = Material.query.filter_by(is_approved=True)
        hits = search_service.material_search_query(query, 'structures').all()
        titles = {m.title for m in hits}
        assert titles == {'Data Structures Handbook'}  # unapproved row stays out


def test_sqlite_filter_matches_description(app, seeded_materials):
    with app.app_context():
        query = Material.query.filter_by(is_approved=True)
        hits = search_service.material_search_query(query, 'benzene').all()
        assert [m.title for m in hits] == ['Organic Chemistry Notes']


def test_sqlite_filter_escapes_like_metacharacters(app, seeded_materials):
    """'50%' must not match everything (old code treated % as a wildcard); and a
    bare underscore/percent query matches nothing rather than every row."""
    with app.app_context():
        query = Material.query.filter_by(is_approved=True)
        assert search_service.material_search_query(query, '100%').count() == 0
        assert search_service.material_search_query(query, '_').count() == 0


def test_rank_is_none_on_sqlite(app):
    """No tsvector on SQLite -> no rank clause; callers keep created_at ordering."""
    with app.app_context():
        assert search_service.material_search_rank('anything') is None


def test_route_search_still_works_end_to_end(app, client, make_user, login_as,
                                             seeded_materials):
    """The /api/fetch-materials q= path keeps working through the new filter."""
    user = make_user('searcher', department='Computer Science', level='200')
    login_as(client, user)
    res = client.get('/api/fetch-materials?q=structures')
    assert res.status_code == 200
    body = res.get_json()
    assert body['success'] is True
    assert [m['title'] for m in body['materials']] == ['Data Structures Handbook']
