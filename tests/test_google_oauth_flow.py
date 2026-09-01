"""Regression tests for two Google sign-in bugs reported after the _start_session_for()
fix landed:

1. google_login() never asked Google to show the account picker (no `prompt` param on
   the authorization request), so Google silently reused whichever account was already
   cached in the browser -- someone tapping "Sign Up with Google" with an existing
   Nelavista account already signed into that Google session got silently logged into
   their existing account, with no chance to pick a different one.

2. google_callback() always flashed "Logged in with Google!", even for a genuinely new
   account (which should say something closer to "Account created") and even though the
   real, underlying complaint traced back to bug #1 above (the account picker never
   showing) rather than a callback bug on its own -- fixed anyway so the message is
   accurate regardless of which Google account ends up authenticated.

Both require faking Authlib's oauth.google client rather than a real Google round-trip.
"""
from flask import redirect
from extensions import db
from models import User
import routes.auth_routes as auth_routes


class _FakeGoogleClient:
    def __init__(self, userinfo=None):
        self.authorize_redirect_calls = []
        self._userinfo = userinfo or {}

    def authorize_redirect(self, redirect_uri, **kwargs):
        self.authorize_redirect_calls.append((redirect_uri, kwargs))
        return redirect('https://accounts.google.com/fake-consent-screen')

    def authorize_access_token(self):
        return {'userinfo': self._userinfo}

    def userinfo(self, token=None):
        return self._userinfo


def _enable_google_oauth(monkeypatch, fake_client):
    monkeypatch.setattr(auth_routes, 'GOOGLE_OAUTH_ENABLED', True)
    monkeypatch.setattr(auth_routes.oauth, 'google', fake_client, raising=False)


def test_google_login_forces_the_account_chooser(app, client, monkeypatch):
    fake_client = _FakeGoogleClient()
    _enable_google_oauth(monkeypatch, fake_client)

    client.get('/auth/google')

    assert len(fake_client.authorize_redirect_calls) == 1
    _, kwargs = fake_client.authorize_redirect_calls[0]
    assert kwargs.get('prompt') == 'select_account'


def test_google_callback_new_account_says_account_created(app, client, monkeypatch):
    fake_client = _FakeGoogleClient(userinfo={
        'sub': 'new-google-sub-1', 'email': 'brandnew@example.com', 'email_verified': True,
    })
    _enable_google_oauth(monkeypatch, fake_client)

    res = client.get('/auth/google/callback', follow_redirects=True)
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert 'Account created with Google!' in body
    assert 'Logged in with Google!' not in body

    with app.app_context():
        user = User.query.filter_by(email='brandnew@example.com').first()
        assert user is not None
        assert user.google_sub == 'new-google-sub-1'


def test_google_callback_existing_account_says_logged_in(app, client, monkeypatch, make_user):
    user_ref = make_user('existing_google_user')
    with app.app_context():
        u = User.query.get(user_ref.id)
        u.google_sub = 'existing-google-sub-1'
        db.session.commit()
        user_email = u.email

    fake_client = _FakeGoogleClient(userinfo={
        'sub': 'existing-google-sub-1', 'email': user_email, 'email_verified': True,
    })
    _enable_google_oauth(monkeypatch, fake_client)

    res = client.get('/auth/google/callback', follow_redirects=True)
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert 'Logged in with Google!' in body
    assert 'Account created with Google!' not in body
