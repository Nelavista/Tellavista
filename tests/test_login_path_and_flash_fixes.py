"""Regression tests for auth-flow fixes:

1. post_auth_redirect() (routes/dashboard_routes.py) backs login()/signup()/
   google_callback() so all three entry points agree on where a user lands. Product
   decision: every login/signup always shows the Choose Your Path picker for a
   non-employer account, regardless of any already-saved User.preferred_path -- this
   briefly skipped the picker for a returning user with a saved path (a since-reverted
   change), so the "shows picker" case below is the one that matters going forward; the
   "even with a saved path" test guards specifically against that skip-picker behavior
   coming back. landing() ('/') is intentionally different -- a still-active session
   revisiting the root URL, not a fresh authentication -- and keeps going straight to
   the saved space, untouched by this.

2. A flash message queued by an earlier, interrupted request (redirect never followed to
   completion -- flaky network, backgrounded tab, shared browser) used to sit in the
   session and surface glued onto the next unrelated request's own flash. login()/
   signup()/google_callback() now discard any stale flash queue before adding their own.
"""
from extensions import db
from models import User


def test_login_always_shows_picker_even_with_a_saved_path(app, client, make_user):
    user = make_user('pathed_user')
    with app.app_context():
        u = User.query.filter_by(username='pathed_user').first()
        u.preferred_path = 'skills'
        db.session.commit()

    res = client.post('/login', data={'username_or_email': 'pathed_user', 'password': 'TestPass123!'},
                       follow_redirects=False)
    assert res.status_code == 302
    assert '/choose-path' in res.headers['Location']


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
