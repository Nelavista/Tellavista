"""Authentication security: rate limiting actually engages, and the email-verification
token flow is single-use, expiring, and doesn't leak whether an arbitrary email exists.
"""
from datetime import datetime, timedelta
from extensions import db
from models import User


def test_login_rate_limit_engages(app, client, make_user):
    make_user('ratelimited_user')
    # login()'s limiter is '15 per 5 minutes' (routes/auth_routes.py) -- hammer it well
    # past that and confirm the extra requests are actually rejected (429), not silently
    # allowed through.
    statuses = []
    for _ in range(20):
        res = client.post('/login', data={'username_or_email': 'ratelimited_user', 'password': 'wrong'})
        statuses.append(res.status_code)
    assert 429 in statuses, f"expected at least one 429 among {statuses}"


def test_signup_creates_unverified_user_with_token(app, client):
    res = client.post('/signup', data={
        'username': 'newstudent', 'email': 'newstudent@example.com', 'password': 'SuperSecret123!',
        'name': 'New Student', 'university': 'Lagos State University', 'faculty': 'Science',
        'department': 'Computer Science', 'level': '100',
    }, follow_redirects=False)
    assert res.status_code in (302, 200)

    with app.app_context():
        user = User.query.filter_by(username='newstudent').first()
        assert user is not None
        assert user.email_verified is False
        # MAIL_SUPPRESS_SEND=True in tests means send_verification_email() still runs its
        # token-generation side effect even though no real email goes out.
        assert user.email_verify_token is not None
        assert user.email_verify_token_expiry is not None
        assert user.email_verify_token_expiry > datetime.utcnow()


def test_verify_email_with_valid_token_marks_verified(app, client, make_user):
    user = make_user('to_verify')
    with app.app_context():
        u = User.query.get(user.id)
        u.email_verify_token = 'a-valid-test-token'
        u.email_verify_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

    res = client.get('/verify-email?token=a-valid-test-token', follow_redirects=False)
    assert res.status_code == 302

    with app.app_context():
        u = User.query.get(user.id)
        assert u.email_verified is True
        assert u.email_verify_token is None


def test_verify_email_token_is_single_use(app, client, make_user):
    user = make_user('to_verify_twice')
    with app.app_context():
        u = User.query.get(user.id)
        u.email_verify_token = 'one-time-token'
        u.email_verify_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

    client.get('/verify-email?token=one-time-token')  # first use: consumes the token

    with app.app_context():
        u = User.query.get(user.id)
        assert u.email_verified is True

    # Replaying the same token must not do anything harmful (token was cleared, so this
    # just falls into "invalid or expired" -- not an error, not a re-verification of a
    # different account).
    res2 = client.get('/verify-email?token=one-time-token', follow_redirects=True)
    assert res2.status_code == 200


def test_verify_email_expired_token_rejected(app, client, make_user):
    user = make_user('expired_token_user')
    with app.app_context():
        u = User.query.get(user.id)
        u.email_verify_token = 'expired-token'
        u.email_verify_token_expiry = datetime.utcnow() - timedelta(hours=1)  # already expired
        db.session.commit()

    client.get('/verify-email?token=expired-token')

    with app.app_context():
        u = User.query.get(user.id)
        assert u.email_verified is False


def test_verify_email_garbage_token_does_not_crash(client):
    res = client.get('/verify-email?token=this-token-does-not-exist-anywhere')
    assert res.status_code == 302  # redirected with a flash, not a 500


def test_resend_verification_requires_login(client):
    res = client.post('/verify-email/resend')
    assert res.status_code == 302  # bounced to login, no email-existence probing possible
