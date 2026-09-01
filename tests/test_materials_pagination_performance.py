"""Regression tests for the P2 performance fix: fetch_materials() (routes/materials_routes.py)
previously ran `.all()` and sliced in Python for EVERY request, loading and serializing
every matching row just to discard all but `per_page` of them. The common (no type filter)
path now uses real DB-level OFFSET/LIMIT; the type-filter path (which needs a Python
heuristic for legacy NULL-material_type rows) is unchanged. Both must produce identical,
correct pagination results to before.
"""
from extensions import db
from models import Material


def _make_materials(n, department='Computer Science', level='200', material_type='lecture_note'):
    for i in range(n):
        db.session.add(Material(
            title=f'Material {i}', department=department, level=level,
            semester='First Semester', is_approved=True, material_type=material_type,
        ))
    db.session.commit()


def test_pagination_covers_every_material_exactly_once(app, client, make_user, login_as):
    user = make_user('materials_page_student', department='Computer Science', level='200')
    with app.app_context():
        _make_materials(15)

    login_as(client, user)

    seen_titles = set()
    page = 1
    while True:
        res = client.get(f'/api/fetch-materials?page={page}&per_page=5')
        assert res.status_code == 200
        body = res.get_json()
        assert body['total'] == 15
        for m in body['materials']:
            assert m['title'] not in seen_titles, 'duplicate across pages -- pagination is broken'
            seen_titles.add(m['title'])
        if not body['has_more']:
            break
        page += 1

    assert len(seen_titles) == 15


def test_last_page_has_more_is_false(app, client, make_user, login_as):
    user = make_user('materials_lastpage_student', department='Computer Science', level='200')
    with app.app_context():
        _make_materials(7)

    login_as(client, user)
    res = client.get('/api/fetch-materials?page=1&per_page=5')
    body = res.get_json()
    assert body['total'] == 7
    assert len(body['materials']) == 5
    assert body['has_more'] is True

    res2 = client.get('/api/fetch-materials?page=2&per_page=5')
    body2 = res2.get_json()
    assert len(body2['materials']) == 2
    assert body2['has_more'] is False


def test_type_filter_path_still_includes_legacy_null_type_row(app, client, make_user, login_as):
    """The type-filter branch is unchanged by this fix -- proves the Python-heuristic
    fallback for legacy (material_type=NULL) rows still works after the refactor."""
    user = make_user('materials_typefilter_student', department='Computer Science', level='200')
    with app.app_context():
        db.session.add(Material(
            title='2023 Past Question Paper', department='Computer Science', level='200',
            semester='First Semester', is_approved=True, material_type=None,  # legacy row
        ))
        db.session.add(Material(
            title='Some Lecture Notes', department='Computer Science', level='200',
            semester='First Semester', is_approved=True, material_type='lecture_note',
        ))
        db.session.commit()

    login_as(client, user)
    res = client.get('/api/fetch-materials?type=past_question')
    body = res.get_json()
    assert body['total'] == 1
    assert body['materials'][0]['title'] == '2023 Past Question Paper'
