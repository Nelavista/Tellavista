"""Authentication security: rate limiting actually engages, the email-verification and
password-reset token flows are single-use, expiring, and store only a token hash, and
neither endpoint leaks whether an arbitrary email exists.
"""
from datetime import datetime, timedelta
from extensions import db
from models import User
from routes.auth_routes import _hash_token


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
        assert user.email_verify_token_hash is not None
        assert user.email_verify_token_expiry is not None
        assert user.email_verify_token_expiry > datetime.utcnow()


def test_verify_email_with_valid_token_marks_verified(app, client, make_user):
    user = make_user('to_verify')
    with app.app_context():
        u = User.query.get(user.id)
        u.email_verify_token_hash = _hash_token('a-valid-test-token')
        u.email_verify_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

    res = client.get('/verify-email?token=a-valid-test-token', follow_redirects=False)
    assert res.status_code == 200
    assert b'confirmed' in res.data.lower()

    with app.app_context():
        u = User.query.get(user.id)
        assert u.email_verified is True
        assert u.email_verify_token_hash is None


def test_verify_email_token_is_single_use(app, client, make_user):
    user = make_user('to_verify_twice')
    with app.app_context():
        u = User.query.get(user.id)
        u.email_verify_token_hash = _hash_token('one-time-token')
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
    assert b'expired' in res2.data.lower() or b'invalid' in res2.data.lower()


def test_verify_email_expired_token_rejected(app, client, make_user):
    user = make_user('expired_token_user')
    with app.app_context():
        u = User.query.get(user.id)
        u.email_verify_token_hash = _hash_token('expired-token')
        u.email_verify_token_expiry = datetime.utcnow() - timedelta(hours=1)  # already expired
        db.session.commit()

    client.get('/verify-email?token=expired-token')

    with app.app_context():
        u = User.query.get(user.id)
        assert u.email_verified is False


def test_verify_email_garbage_token_does_not_crash(client):
    res = client.get('/verify-email?token=this-token-does-not-exist-anywhere')
    assert res.status_code == 200  # renders the invalid/expired result page, not a 500


def test_resend_verification_requires_login(client):
    res = client.post('/verify-email/resend')
    assert res.status_code == 302  # bounced to login, no email-existence probing possible


def test_resend_verification_public_never_reveals_existence(app, client, make_user):
    """/verify-email/resend-public must respond identically whether the email belongs to
    a real, unverified account or doesn't exist at all -- the whole point of a logged-out
    resend path is that it can't be used to enumerate accounts."""
    make_user('has_account', email='hasaccount@example.com')

    res_real = client.post('/verify-email/resend-public',
                            data={'email': 'hasaccount@example.com'}, follow_redirects=True)
    res_fake = client.post('/verify-email/resend-public',
                            data={'email': 'doesnotexist@example.com'}, follow_redirects=True)

    assert res_real.status_code == res_fake.status_code == 200
    assert res_real.data == res_fake.data


def test_verify_email_blocked_by_profile_completion_gate_regression(app, client):
    """Regression test: a fresh signup is logged in immediately but has NOT necessarily
    finished the profile-completion modal (signup doesn't collect 'semester' -- see
    utils/helpers.py's check_profile_complete). Before routes/materials_routes.py's
    enforce_profile_completion hook exempted auth.verify_email, clicking the emailed link
    at this point got silently redirected to /dashboard and the account was NEVER marked
    verified. materials_bp (which owns that hook) is already registered by the `app`
    fixture in conftest.py, so this exercises the real site-wide hook, not a mock of it."""
    client.post('/signup', data={
        'username': 'incomplete_profile_user', 'email': 'incomplete@example.com',
        'password': 'SuperSecret123!', 'name': 'Incomplete User',
        'university': 'Lagos State University', 'faculty': 'Science',
        'department': 'Computer Science', 'level': '100',
        # No 'semester' -- matches what the real signup form actually collects.
    })

    with app.app_context():
        user = User.query.filter_by(username='incomplete_profile_user').first()
        from utils.helpers import check_profile_complete
        assert check_profile_complete(user) is False  # confirms the scenario is real
        token = 'incomplete-user-verify-token'
        user.email_verify_token_hash = _hash_token(token)
        user.email_verify_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

    res = client.get(f'/verify-email?token={token}')
    assert res.status_code == 200
    assert b'confirmed' in res.data.lower()

    with app.app_context():
        user = User.query.filter_by(username='incomplete_profile_user').first()
        assert user.email_verified is True


def test_forgot_password_generic_response_for_unknown_email(client):
    res = client.post('/forgot-password', data={'email': 'nobody@example.com'}, follow_redirects=True)
    assert res.status_code == 200
    assert b'password reset link has been sent' in res.data.lower()


def test_forgot_password_same_response_when_email_send_fails(app, client, make_user):
    """The critical enumeration fix: if the account exists but the email fails to send
    (e.g. SMTP misconfigured, matching the real "Unable to send email" bug this app
    shipped with), the response must be byte-identical to the unknown-email case --
    previously this branch flashed a distinct "Unable to send email" error only when the
    account existed, which let anyone learn which emails were registered simply by
    watching for that message while mail was down."""
    make_user('willbreak', email='willbreak@example.com')
    app.config['MAIL_SUPPRESS_SEND'] = False  # force _send_mail_or_raise's config check to fire
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None

    res_real = client.post('/forgot-password', data={'email': 'willbreak@example.com'}, follow_redirects=True)
    res_fake = client.post('/forgot-password', data={'email': 'stillnobody@example.com'}, follow_redirects=True)

    assert res_real.status_code == res_fake.status_code == 200
    assert res_real.data == res_fake.data


def test_forgot_password_sets_hashed_token_not_raw(app, client, make_user):
    make_user('resetme', email='resetme@example.com')
    client.post('/forgot-password', data={'email': 'resetme@example.com'})

    with app.app_context():
        u = User.query.filter_by(username='resetme').first()
        assert u.reset_token_hash is not None
        assert len(u.reset_token_hash) == 64  # sha256 hex digest
        assert u.reset_token_expiry > datetime.utcnow()


def test_reset_password_full_flow_and_token_single_use(app, client, make_user):
    user = make_user('fullflow', email='fullflow@example.com')
    with app.app_context():
        u = User.query.get(user.id)
        u.reset_token_hash = _hash_token('flow-token')
        u.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()

    res = client.post('/reset-password?token=flow-token',
                       data={'password': 'NewSecure123', 'confirm_password': 'NewSecure123'},
                       follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        u = User.query.get(user.id)
        assert u.check_password('NewSecure123') is True
        assert u.reset_token_hash is None

    # The same link must not work a second time.
    res2 = client.get('/reset-password?token=flow-token', follow_redirects=True)
    assert b'invalid or expired' in res2.data.lower()


def test_reset_password_rejects_weak_password(app, client, make_user):
    user = make_user('weakpw', email='weakpw@example.com')
    with app.app_context():
        u = User.query.get(user.id)
        u.reset_token_hash = _hash_token('weak-token')
        u.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()

    res = client.post('/reset-password?token=weak-token',
                       data={'password': 'alllower', 'confirm_password': 'alllower'},
                       follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        u = User.query.get(user.id)
        assert u.check_password('alllower') is False  # rejected: no digit


def test_reset_password_rejects_mismatched_confirmation(app, client, make_user):
    user = make_user('mismatch', email='mismatch@example.com')
    with app.app_context():
        u = User.query.get(user.id)
        u.reset_token_hash = _hash_token('mismatch-token')
        u.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()

    client.post('/reset-password?token=mismatch-token',
                data={'password': 'GoodPass123', 'confirm_password': 'Different123'})

    with app.app_context():
        u = User.query.get(user.id)
        assert u.check_password('GoodPass123') is False
