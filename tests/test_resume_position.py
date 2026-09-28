"""PRD §5.3 resume position: "Continue learning" must return the student to the exact
material *and* page they left.

Covers the round trip:
  viewer posts {page} -> /api/materials/<id>/view stores it on MaterialView.last_page
  -> /api/continue-studying echoes it back -> course/topic Open links append #page=N
  (app/routes/academia_routes.py's resume_url).

Plus the invariants that keep it honest:
  - a view that reports no page must never CLEAR a previously recorded position
    (re-opening without a position is not "back to page one");
  - garbage page values are rejected, never stored;
  - last_page NULL ("never recorded") stays distinct from page 1.
"""
import pytest

from app.extensions import db
from app.models import Material, MaterialView, User
from app.routes.academia_routes import resume_url
from app.services.progress_service import record_material_view, get_resume_pages


def _make_material(app, title='Data Structures Notes', **kw):
    with app.app_context():
        m = Material(title=title, department='Computer Science', level='200',
                     semester='First Semester', course_code='CSC213',
                     university='Lagos State University', source='uploaded', **kw)
        db.session.add(m)
        db.session.commit()
        return m.id


def test_view_endpoint_stores_and_echoes_page(app, client, make_user, login_as):
    user = make_user('resume1')
    mid = _make_material(app)
    login_as(client, user)

    res = client.post(f'/api/materials/{mid}/view', json={'page': 7})
    assert res.status_code == 200
    assert res.get_json() == {'success': True, 'last_page': 7}

    # And it's really persisted, not just echoed back.
    with app.app_context():
        view = MaterialView.query.filter_by(user_id=user.id, material_id=mid).first()
        assert view is not None
        assert view.last_page == 7


def test_pageless_view_never_clears_a_recorded_position(app, client, make_user, login_as):
    user = make_user('resume2')
    mid = _make_material(app)
    login_as(client, user)

    client.post(f'/api/materials/{mid}/view', json={'page': 12})
    # Older callers (and non-PDF viewers) post no body at all.
    res = client.post(f'/api/materials/{mid}/view')
    assert res.get_json()['last_page'] == 12


@pytest.mark.parametrize('bad_page', [0, -3, 'abc', None, True, 1.5])
def test_invalid_page_values_are_never_stored(app, client, make_user, login_as, bad_page):
    user = make_user(f'resume_bad_{str(bad_page).replace(".", "_")}')
    mid = _make_material(app)
    login_as(client, user)

    res = client.post(f'/api/materials/{mid}/view', json={'page': bad_page})
    # Accepted as a view, but the position stays "never recorded" (None).
    assert res.status_code == 200
    assert res.get_json()['last_page'] is None


def test_continue_studying_returns_the_resume_page(app, client, make_user, login_as):
    user = make_user('resume3')
    mid = _make_material(app)
    login_as(client, user)

    client.post(f'/api/materials/{mid}/view', json={'page': 5})
    res = client.get('/api/continue-studying')
    data = res.get_json()['material']
    assert data['last_page'] == 5
    assert data['material_id'] == mid


def test_get_resume_pages_is_one_lookup_and_skips_unrecorded(app, make_user):
    user = make_user('resume4')
    m1, m2, m3 = _make_material(app, 'A'), _make_material(app, 'B'), _make_material(app, 'C')
    with app.app_context():
        u = User.query.get(user.id)
        record_material_view(u, Material.query.get(m1), page=3)
        record_material_view(u, Material.query.get(m2))          # position never recorded
        record_material_view(u, Material.query.get(m3), page=1)
        pages = get_resume_pages(u, [m1, m2, m3])
    assert pages == {m1: 3, m3: 1}   # m2 absent -> "no position", distinct from page 1
    assert get_resume_pages(u, []) == {}


def test_resume_url_appends_fragment_only_for_pdf_links():
    class _M:
        id = 1
        resolved_url = 'https://res.cloudinary.com/x/notes.pdf'
        external_url = None

    assert resume_url(_M(), {1: 9}) == 'https://res.cloudinary.com/x/notes.pdf#page=9'
    # No recorded position -> unchanged.
    assert resume_url(_M(), {}) == 'https://res.cloudinary.com/x/notes.pdf'
    # Never mangle a URL that already carries a fragment.
    _M.resolved_url = 'https://example.com/doc.pdf#zoom=100'
    assert resume_url(_M(), {1: 9}) == 'https://example.com/doc.pdf#zoom=100'
    # Non-PDF resources never get a page anchor.
    _M.resolved_url = 'https://example.com/lecture.html'
    assert resume_url(_M(), {1: 9}) == 'https://example.com/lecture.html'
    _M.resolved_url = None
    _M.external_url = 'https://files.example.org/past-questions.PDF'
    assert resume_url(_M(), {1: 2}) == 'https://files.example.org/past-questions.PDF#page=2'
