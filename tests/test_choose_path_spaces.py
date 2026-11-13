"""The Choose Your Path picker offers all four student spaces.

V1 originally shipped with only Academia and Skills while V2 had four spaces
(Academia, Skills, Opportunities and Campus). These tests pin the picker, the
saved path, and the redirects so V1 cannot silently fall back to two cards.
"""
import pytest

from app.extensions import db
from app.models import User


SPACES = [
    ('academia', '/dashboard'),
    ('skills', '/skills'),
    ('opportunities', '/opportunities'),
    ('campus', '/campus-map'),
]


def test_picker_lists_all_four_spaces(client, login_as, make_user):
    login_as(client, make_user('four_spaces'))
    res = client.get('/choose-path')
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    for label in ('Academia', 'Skills', 'Opportunities', 'Campus'):
        assert label in body
    for value, _ in SPACES:
        assert f'name="path" value="{value}"' in body


@pytest.mark.parametrize('path,expected', SPACES)
def test_each_space_saves_path_and_redirects(app, client, login_as, make_user, path, expected):
    user = make_user(f'path_{path}')
    login_as(client, user)

    res = client.post('/choose-path', data={'path': path}, follow_redirects=False)
    assert res.status_code == 302
    assert res.headers['Location'] == expected

    with app.app_context():
        assert db.session.get(User, user.id).preferred_path == path
    with client.session_transaction() as sess:
        assert sess['user']['preferred_path'] == path


@pytest.mark.parametrize('path,expected', SPACES)
def test_returning_visit_opens_the_saved_space(client, login_as, make_user, path, expected):
    login_as(client, make_user(f'return_{path}'))
    client.post('/choose-path', data={'path': path}, follow_redirects=False)

    res = client.get('/', follow_redirects=False)
    assert res.status_code == 302
    assert res.headers['Location'] == expected


def test_unknown_path_is_rejected_and_leaves_no_saved_choice(app, client, login_as, make_user):
    user = make_user('bad_path')
    login_as(client, user)

    res = client.post('/choose-path', data={'path': 'employer'}, follow_redirects=True)
    assert res.status_code == 200
    assert 'Please choose a valid path.' in res.get_data(as_text=True)

    with app.app_context():
        assert db.session.get(User, user.id).preferred_path is None
