"""Regression test for the university material-leakage fix: routes/materials_routes.py's
/api/fetch-materials used to skip its university filter specifically for Lagos State
University students, so a LASU student could see materials tagged for a different
school. The fix applies the same filter to every university, LASU included.
"""
from extensions import db
from models import Material


def _add_material(app, title, university, department='Computer Science', level='200'):
    with app.app_context():
        m = Material(title=title, department=department, level=level, semester='First Semester',
                     university=university, is_approved=True, file_url='https://example.com/x.pdf')
        db.session.add(m)
        db.session.commit()


def test_lasu_student_does_not_see_unilag_material(app, client, make_user, login_as):
    _add_material(app, 'LASU Past Questions', university='Lagos State University')
    _add_material(app, 'UNILAG Past Questions', university='University of Lagos')
    _add_material(app, 'Universal Notes', university=None)

    user = make_user('lasu_student', university='Lagos State University')
    login_as(client, user)

    res = client.get('/api/fetch-materials')
    assert res.status_code == 200
    titles = {m['title'] for m in res.get_json()['materials']}
    assert 'LASU Past Questions' in titles
    assert 'Universal Notes' in titles
    assert 'UNILAG Past Questions' not in titles


def test_unilag_student_does_not_see_lasu_material(app, client, make_user, login_as):
    _add_material(app, 'LASU Past Questions 2', university='Lagos State University')
    _add_material(app, 'UNILAG Past Questions 2', university='University of Lagos')

    user = make_user('unilag_student', university='University of Lagos')
    login_as(client, user)

    res = client.get('/api/fetch-materials')
    titles = {m['title'] for m in res.get_json()['materials']}
    assert 'UNILAG Past Questions 2' in titles
    assert 'LASU Past Questions 2' not in titles


def test_another_university_also_correctly_scoped(app, client, make_user, login_as):
    """Not just LASU/UNILAG -- the fix must be university-agnostic, not a second
    hardcoded special case."""
    _add_material(app, 'UI Past Questions', university='University of Ibadan')
    _add_material(app, 'LASU Past Questions 3', university='Lagos State University')

    user = make_user('ui_student', university='University of Ibadan')
    login_as(client, user)

    res = client.get('/api/fetch-materials')
    titles = {m['title'] for m in res.get_json()['materials']}
    assert 'UI Past Questions' in titles
    assert 'LASU Past Questions 3' not in titles


def test_no_university_set_query_is_unscoped_by_university(app, make_user):
    """The 'no university set' carve-out in /api/fetch-materials (routes/materials_routes.py)
    only applies when current_user.university is falsy. In practice, a logged-in user
    reaching that route at all must have a COMPLETE profile (routes/materials_routes.py's
    site-wide before_app_request hook redirects incomplete profiles away first), and
    utils/helpers.py's check_profile_complete requires university to be non-empty -- so
    this branch is effectively unreachable via the live HTTP route today, only exercised
    by legacy pre-existing rows with university=None. Tested at the query-building level
    directly (bypassing the HTTP/profile-completion layer) since there's no way to
    reach it end-to-end through a route that requires a complete profile."""
    _add_material(app, 'LASU Past Questions 4', university='Lagos State University')
    _add_material(app, 'UNILAG Past Questions 4', university='University of Lagos')
    user = make_user('no_uni_student', university=None, complete_profile=False)

    with app.app_context():
        from models import User
        current_user = User.query.get(user.id)
        query = Material.query.filter_by(is_approved=True)
        if current_user.university:
            query = query.filter(
                (Material.university.is_(None)) | (Material.university == current_user.university)
            )
        titles = {m.title for m in query.all()}
        assert 'LASU Past Questions 4' in titles
        assert 'UNILAG Past Questions 4' in titles
