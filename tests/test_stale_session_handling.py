"""Regression test for the stale-session crash (P0-1 of the stabilization pass).

login_required() previously only checked `'user' in session` -- never that the DB row
still existed. Settings > Danger Zone anonymizes/renames a deleted account in place
rather than hard-deleting it (models.py's User.is_deleted), so a second tab/device on
the same browser keeps a session for a username that no longer resolves to anything the
moment the first tab deletes the account. Every protected route downstream re-queries
the user with no None-guard and immediately dereferences the result, so the very next
request on that stale session used to 500 instead of bouncing back to login.
"""
from extensions import db
from models import User


def test_stale_session_after_account_deleted_redirects_instead_of_crashing(app, client, make_user, login_as):
    user = make_user('will_be_deleted')
    login_as(client, user)

    # Simulate what settings_routes.py's delete_account() does to the row -- anonymize
    # in place -- without going through the route, so the *other* tab's session (this
    # client) is left pointing at a username that no longer exists.
    with app.app_context():
        u = User.query.get(user.id)
        u.username = f'deleted_user_{u.id}'
        u.is_deleted = True
        db.session.commit()

    # Limited to blueprints the test app fixture actually registers (see conftest.py) --
    # the fix itself lives in the shared login_required() decorator, so these three are
    # representative of every other protected route across the app, not an exhaustive list.
    for path in ('/dashboard', '/CBT/history', '/choose-path'):
        res = client.get(path, follow_redirects=False)
        assert res.status_code == 302, f'{path} should redirect (not crash) on a stale session, got {res.status_code}'
        assert '/login' in res.headers['Location'], f'{path} should redirect to login'


def test_valid_session_still_reaches_protected_routes(app, client, make_user, login_as):
    user = make_user('still_active')
    login_as(client, user)

    res = client.get('/dashboard', follow_redirects=False)
    assert res.status_code == 200


def test_admin_required_already_handled_this_case(app, client, make_user, login_as):
    """admin_required() already re-queries the DB (see utils/helpers.py) -- confirms the
    new login_required check doesn't change its (already-correct) behavior for a deleted
    session hitting an admin-only route."""
    user = make_user('deleted_admin', is_admin=True)
    login_as(client, user)

    with app.app_context():
        u = User.query.get(user.id)
        u.username = f'deleted_user_{u.id}'
        u.is_deleted = True
        db.session.commit()

    res = client.get('/dashboard', follow_redirects=False)
    assert res.status_code == 302
    assert '/login' in res.headers['Location']
