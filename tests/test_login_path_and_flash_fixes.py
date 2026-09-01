"""Regression tests for two auth-flow fixes:

1. login()/signup()/google_callback() previously always forced the choose-path picker,
   ignoring any already-saved User.preferred_path -- contradicting landing() ('/'), which
   already respected it. post_auth_redirect() (routes/dashboard_routes.py) now backs all
   three so a returning user with a saved path goes straight there.

2. A flash message queued by an earlier, interrupted request (redirect never followed to
   completion -- flaky network, backgrounded tab, shared browser) used to sit in the
   session and surface glued onto the next unrelated request's own flash. login()/
   signup()/google_callback() now discard any stale flash queue before adding their own.
"""
from extensions import db
from models import User


def test_login_with_saved_path_skips_picker(app, client, make_user):
    user = make_user('pathed_user')
    with app.app_context():
        u = User.query.filter_by(username='pathed_user').first()
        u.preferred_path = 'skills'
        db.session.commit()

    res = client.post('/login', data={'username_or_email': 'pathed_user', 'password': 'TestPass123!'},
                       follow_redirects=False)
    assert res.status_code == 302
    assert '/choose-path' not in res.headers['Location']


def test_login_without_saved_path_shows_picker(app, client, make_user):
    make_user('freshpath_user')
    res = client.post('/login', data={'username_or_email': 'freshpath_user', 'password': 'TestPass123!'},
                       follow_redirects=False)
    assert res.status_code == 302
    assert '/choose-path' in res.headers['Location']


def test_stale_flash_does_not_leak_into_successful_login(app, client, make_user):
    make_user('cleanslate_user')
    # Simulate an earlier request (e.g. a failed login against a genuinely deleted test
    # account, or any other flow) whose redirect the browser never finished following --
    # the flash it queued is still sitting in the session cookie.
    with client.session_transaction() as sess:
        sess['_flashes'] = [('message', 'This account has been deleted.')]

    res = client.post('/login', data={'username_or_email': 'cleanslate_user', 'password': 'TestPass123!'},
                       follow_redirects=True)
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert 'This account has been deleted.' not in body


def test_genuinely_deleted_account_still_blocked(app, client, make_user):
    make_user('to_be_deleted_user')
    with app.app_context():
        u = User.query.filter_by(username='to_be_deleted_user').first()
        u.is_deleted = True
        db.session.commit()

    res = client.post('/login', data={'username_or_email': 'to_be_deleted_user', 'password': 'TestPass123!'},
                       follow_redirects=True)
    assert res.status_code == 200
    assert 'This account has been deleted.' in res.get_data(as_text=True)
