"""Regression test for routes/auth_routes.py's _start_session_for(): it built the
session correctly (session['user'] set, User.last_login updated, db.session.commit()
called) but never returned a truthy value on that success path -- it fell off the end of
the function, implicitly returning None, which is falsy. google_callback()'s
`if not _start_session_for(user):` was therefore true on EVERY Google sign-in,
successful or not, so it always flashed "This account has been deleted." and redirected
back to /login -- even though the session had already been established correctly (which
is why navigating anywhere else in the same browser landed on the dashboard, logged in).
"""
from flask import session
from extensions import db
from models import User
from routes.auth_routes import _start_session_for


def test_start_session_for_returns_true_and_sets_session_on_success(app, make_user):
    user_ref = make_user('google_signin_user')
    with app.test_request_context():
        user = User.query.get(user_ref.id)
        result = _start_session_for(user)
        assert result is True
        assert session['user']['username'] == 'google_signin_user'

    with app.app_context():
        reloaded = User.query.get(user_ref.id)
        assert reloaded.last_login is not None


def test_start_session_for_returns_false_for_a_genuinely_deleted_account(app, make_user):
    user_ref = make_user('google_deleted_user')
    with app.app_context():
        u = User.query.get(user_ref.id)
        u.is_deleted = True
        db.session.commit()

    with app.test_request_context():
        user = User.query.get(user_ref.id)
        result = _start_session_for(user)
        assert result is False
