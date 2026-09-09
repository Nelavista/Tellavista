from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from datetime import datetime, timedelta
import hashlib
import re
import secrets
from models import User
from routes.dashboard_routes import post_auth_redirect
from extensions import db, mail, limiter, oauth  # Assuming 'mail' is initialized in extensions.py
from flask_mail import Message
from logging_config import logger
from config import GOOGLE_OAUTH_ENABLED
from utils.validation import password_strength_error

auth_bp = Blueprint('auth', __name__)

EMAIL_VERIFY_TOKEN_HOURS = 48
RESET_TOKEN_MINUTES = 30


def _hash_token(token):
    """SHA-256 hex digest of a reset/verification token -- see models.py's
    reset_token_hash / email_verify_token_hash docstrings for why only the hash is ever
    persisted. The raw token itself always comes from secrets.token_urlsafe(32) (256 bits
    of entropy), so a fast, unsalted hash is fine here -- unlike a password, there's no
    realistic low-entropy input for an attacker with DB access to brute force. Hashing
    (rather than e.g. encrypting) also means the lookup stays a plain indexed equality
    query: hash the incoming token and compare, same as before but hashed both sides."""
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def _send_mail_or_raise(msg):
    """Thin wrapper around mail.send() that fails with a specific, actionable message
    when SMTP credentials simply aren't configured, instead of letting Flask-Mail attempt
    a real connection and raise a generic (and, against Gmail, sometimes confusingly
    worded) SMTPAuthenticationError. This is what routes/auth_routes.py's forgot-password
    endpoint was tracing back to: MAIL_USERNAME/MAIL_PASSWORD were unset in production, so
    every send attempt failed the same way and got swallowed into "Unable to send email at
    this time." -- with nothing in the logs to say *why*. Skipped when MAIL_SUPPRESS_SEND
    is on (tests and any deliberate dry-run config) since Flask-Mail itself never opens a
    real connection in that mode either."""
    if not current_app.config.get('MAIL_SUPPRESS_SEND') and not (
        current_app.config.get('MAIL_USERNAME') and current_app.config.get('MAIL_PASSWORD')
    ):
        raise RuntimeError(
            'Email is not configured: MAIL_USERNAME and/or MAIL_PASSWORD environment '
            'variables are not set. See .env.example.'
        )
    mail.send(msg)


# ---------- Email Sending Functions ----------
def send_verification_email(user):
    """Sends (or resends) the email-identity-confirmation link. Generates a fresh,
    single-use, expiring token every time -- a previously issued token stops working the
    moment a new one is requested, same single-active-token pattern as password reset
    below, just a separate token/expiry pair (User.email_verify_token_hash) so verifying
    an email can never be confused with, or substituted for, resetting a password. Only
    the token's hash is persisted (see _hash_token above); the raw token exists only in
    this function's local variable and the outgoing email, never logged or stored."""
    token = secrets.token_urlsafe(32)
    user.email_verify_token_hash = _hash_token(token)
    user.email_verify_token_expiry = datetime.utcnow() + timedelta(hours=EMAIL_VERIFY_TOKEN_HOURS)
    db.session.commit()

    verify_link = f"{request.host_url}verify-email?token={token}"
    html_content = f"""
    <div style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; background: #161b22; color: #f0f3f8; padding: 40px 24px; border-radius: 20px;">
      <h1 style="color: #00d1ff; margin-bottom: 16px;">Confirm your email</h1>
      <p style="color: #b9c3d1; line-height: 1.6; margin-bottom: 24px;">
        Welcome to Nelavista! Confirm this is really your email address to finish setting up your account.
      </p>
      <a href="{verify_link}" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #00d1ff, #007bff); color: white; text-decoration: none; border-radius: 12px; font-weight: 600;">
        Confirm Email →
      </a>
      <p style="color: #b9c3d1; font-size: 0.9rem; margin-top: 32px; line-height: 1.6;">
        This link will expire in {EMAIL_VERIFY_TOKEN_HOURS} hours. If you didn't create a Nelavista account, you can safely ignore this email.
      </p>
      <p style="color: #6b7280; font-size: 0.85rem; margin-top: 24px; border-top: 1px solid #30363d; padding-top: 24px;">
        Or copy this link: <span style="color: #00d1ff;">{verify_link}</span>
      </p>
    </div>
    """
    msg = Message(
        subject="Confirm your Nelavista email",
        recipients=[user.email],
        html=html_content,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@nelavista.com')
    )
    _send_mail_or_raise(msg)


def send_password_reset_email(user_email, reset_link):
    """Send a password reset email with a beautiful HTML template."""
    html_content = f"""
    <div style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; background: #161b22; color: #f0f3f8; padding: 40px 24px; border-radius: 20px;">
      <h1 style="color: #00d1ff; margin-bottom: 16px;">Reset Your Password</h1>
      <p style="color: #b9c3d1; line-height: 1.6; margin-bottom: 24px;">
        You requested to reset your Nelavista password. Click the button below to create a new password:
      </p>
      <a href="{reset_link}" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #00d1ff, #007bff); color: white; text-decoration: none; border-radius: 12px; font-weight: 600;">
        Reset Password →
      </a>
      <p style="color: #b9c3d1; font-size: 0.9rem; margin-top: 32px; line-height: 1.6;">
        This link will expire in 30 minutes. If you didn't request this, you can safely ignore this email.
      </p>
      <p style="color: #6b7280; font-size: 0.85rem; margin-top: 24px; border-top: 1px solid #30363d; padding-top: 24px;">
        Or copy this link: <span style="color: #00d1ff;">{reset_link}</span>
      </p>
    </div>
    """

    msg = Message(
        subject="Reset your Nelavista password",
        recipients=[user_email],
        html=html_content,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@nelavista.com')
    )
    _send_mail_or_raise(msg)


# ---------- Existing Routes ----------
@auth_bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit('10 per hour')
def signup():
    if request.method == 'POST':
        # A flash queued by an earlier, unrelated attempt (e.g. a redirect the browser
        # never finished following -- a flaky mobile connection, a backgrounded tab, a
        # shared/public browser) sits in the session until some page happens to render
        # get_flashed_messages(). Left alone, it would surface here glued onto whatever
        # this attempt flashes, showing an unrelated leftover message next to today's
        # actual result. Every fresh attempt starts from a clean slate.
        session.pop('_flashes', None)
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip() or None
        university = request.form.get('university', '').strip() or None
        faculty = request.form.get('faculty', '').strip() or None
        department = request.form.get('department', '').strip() or None
        level = request.form.get('level', '').strip() or None

        if not username or not email or not password:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('auth.signup'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'error')
            return redirect(url_for('auth.signup'))

        user = User(username=username, email=email, name=name, university=university,
                    faculty=faculty, department=department, level=level)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session.permanent = True
        session['user'] = {
            'username': username,
            'email': email,
            'joined_on': user.joined_on.strftime('%Y-%m-%d'),
            'last_login': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'is_admin': user.is_admin,
            'preferred_path': user.preferred_path
        }

        # Best-effort: a failed verification email must never block account creation or
        # login (the account and session above are already committed) -- the student can
        # always resend it later from the dashboard reminder (see resend_verification_email).
        try:
            send_verification_email(user)
            flash('Account created! Check your email to verify your Nelavista account.', 'success')
        except Exception:
            # logger.exception (not .error(f"...{e}")) captures the full traceback server-
            # side -- e.g. an SMTPAuthenticationError's real cause -- without putting
            # anything sensitive in the user-facing flash below. Never include str(e) in
            # what's shown to the user: some SMTP failures echo back configuration detail.
            logger.exception('Failed to send verification email to new signup %s', user.id)
            flash('Account created successfully! We could not send a verification email '
                  'right now -- you can request one anytime from your dashboard.', 'success')

        # Brand-new account: preferred_path is always unset at this point, so
        # post_auth_redirect() sends them through path selection like any first-ever
        # entry — see its docstring in routes/dashboard_routes.py.
        return post_auth_redirect(user)
    return render_template('signup.html', google_oauth_enabled=GOOGLE_OAUTH_ENABLED)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('15 per 5 minutes')
def login():
    if request.method == 'POST':
        # See the matching comment in signup() above -- a stale flash from an earlier,
        # interrupted attempt (redirect never finished loading) must never bleed into
        # this attempt's result.
        session.pop('_flashes', None)
        login_input = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '').strip()
        if not login_input or not password:
            flash('Please enter username/email and password.', 'error')
            return redirect(url_for('auth.login'))
        user = User.query.filter((User.username == login_input) | (User.email == login_input)).first()
        if user and user.is_deleted:
            flash('This account has been deleted.', 'error')
            return redirect(url_for('auth.login'))
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            session.permanent = True
            session['user'] = {
                'username': user.username,
                'email': user.email,
                'joined_on': user.joined_on.strftime('%Y-%m-%d'),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                'is_admin': user.is_admin,
                'preferred_path': user.preferred_path
            }
            flash('Logged in successfully!', 'success')
            # A first-ever login (no preferred_path saved yet) forks through the
            # Academia/Skills picker; a returning user goes straight back to whichever
            # space they already chose — see post_auth_redirect()'s docstring.
            return post_auth_redirect(user)
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('auth.login'))
    return render_template('login.html', google_oauth_enabled=GOOGLE_OAUTH_ENABLED)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


# ---------- Google Sign-In ----------
def _generate_username_from_email(email):
    """Turns 'jane.doe99@gmail.com' into a free username like 'janedoe99', trying the
    plain slug first and falling back to numeric suffixes -- usernames are required and
    unique, but a Google sign-in never collects one."""
    base = re.sub(r'[^a-z0-9]', '', email.split('@', 1)[0].lower())[:30] or 'user'
    candidate = base
    suffix = 0
    while User.query.filter_by(username=candidate).first() is not None:
        suffix += 1
        candidate = f"{base}{suffix}"
    return candidate


def _start_session_for(user):
    """Same session shape auth.login()/auth.signup() build, factored out so both the
    existing-account and new-account branches of the Google callback below set it
    identically. Returns False (and starts no session) if the account was deleted via
    Settings > Danger Zone -- mirrors the is_deleted check in login() above."""
    if user.is_deleted:
        return False
    user.last_login = datetime.utcnow()
    db.session.commit()
    session.permanent = True
    session['user'] = {
        'username': user.username,
        'email': user.email,
        'joined_on': user.joined_on.strftime('%Y-%m-%d'),
        'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
        'is_admin': user.is_admin,
        'preferred_path': user.preferred_path
    }
    # Without this, the function falls off the end and implicitly returns None -- falsy,
    # so google_callback()'s `if not _start_session_for(user):` was true on EVERY Google
    # sign-in, successful or not. The session above was already built correctly (hence
    # last_login updating and a logged-in user landing on the dashboard if they navigated
    # anywhere else), but the caller still flashed "This account has been deleted." and
    # bounced back to /login regardless, because it never actually got a truthy result to
    # check against.
    return True


@auth_bp.route('/auth/google')
@limiter.limit('20 per hour')
def google_login():
    if not GOOGLE_OAUTH_ENABLED:
        flash('Google sign-in is not available right now.', 'error')
        return redirect(url_for('auth.login'))
    redirect_uri = url_for('auth.google_callback', _external=True)
    # Without this, Google silently reuses whichever Google account is already cached in
    # the browser instead of ever showing the account picker -- someone with more than
    # one Google account (or just wanting to sign up with a different one than they're
    # currently signed into) gets authenticated as whichever account Google already had
    # active, with no chance to choose. select_account forces the picker every time.
    return oauth.google.authorize_redirect(redirect_uri, prompt='select_account')


@auth_bp.route('/auth/google/callback')
@limiter.limit('20 per hour')
def google_callback():
    # See the matching comment in login()/signup() -- a stale flash from an earlier,
    # interrupted attempt must never bleed into this one (OAuth round-trips through
    # Google and back are especially prone to a browser giving up mid-redirect).
    session.pop('_flashes', None)
    if not GOOGLE_OAUTH_ENABLED:
        flash('Google sign-in is not available right now.', 'error')
        return redirect(url_for('auth.login'))

    try:
        # authorize_access_token() validates the id_token's nonce (set during
        # authorize_redirect above, stored server-side in the session by Authlib) and
        # returns the already-verified claims under 'userinfo' -- never parse the id
        # token manually, that's what would skip nonce validation.
        token = oauth.google.authorize_access_token()
        userinfo = token.get('userinfo') or oauth.google.userinfo(token=token)
    except Exception as e:
        logger.error(f"Google OAuth callback failed: {e}")
        flash('Google sign-in failed. Please try again.', 'error')
        return redirect(url_for('auth.login'))

    google_sub = userinfo.get('sub')
    google_email = (userinfo.get('email') or '').strip().lower()
    email_verified_by_google = bool(userinfo.get('email_verified'))

    if not google_sub or not google_email:
        flash('Google did not share the account details we need. Please try again.', 'error')
        return redirect(url_for('auth.login'))

    # 1. Returning Google sign-in -- matched by the stable Google account id.
    user = User.query.filter_by(google_sub=google_sub).first()

    # 2. First-time Google sign-in on an email that already has a password account --
    # link the two rather than creating a duplicate, but only when Google itself vouches
    # for the email (never link on an unverified email claim -- that's how account
    # takeover via a look-alike Google Workspace address would work).
    if not user and email_verified_by_google:
        existing = User.query.filter_by(email=google_email).first()
        if existing:
            existing.google_sub = google_sub
            user = existing

    # 3. Brand new account -- new accounts always start with preferred_path unset, so
    # they land on the Academia/Skills picker below same as a regular signup.
    is_new_account = not user
    if is_new_account:
        username = _generate_username_from_email(google_email)
        user = User(username=username, email=google_email, google_sub=google_sub,
                    name=userinfo.get('name') or None,
                    email_verified=email_verified_by_google)
        db.session.add(user)

    if not _start_session_for(user):
        flash('This account has been deleted.', 'error')
        return redirect(url_for('auth.login'))
    # "Logged in" reads as a mistake to someone who tapped Sign Up and genuinely got a
    # new account, and "Account created" would be just as misleading to someone who
    # already had one -- is_new_account (set above, before the row could match anything
    # existing) tells these apart for real, not by which button the user clicked.
    flash('Account created with Google!' if is_new_account else 'Logged in with Google!', 'success')
    return post_auth_redirect(user)


# ---------- Email Verification Routes ----------
@auth_bp.route('/verify-email')
def verify_email():
    """Renders a dedicated result page (success / expired / invalid) rather than just
    flashing and redirecting -- the old behavior bounced a logged-out visitor straight to
    /login with no context on what happened, and gave no way to request a new link without
    logging in first. The expired/invalid state embeds a resend-by-email form (see
    resend_verification_public below) for exactly that case."""
    token = request.args.get('token')
    logged_in = 'user' in session

    if not token:
        return render_template('verify_email_result.html', status='invalid', logged_in=logged_in)

    user = User.query.filter_by(email_verify_token_hash=_hash_token(token)).first()
    if not user or not user.email_verify_token_expiry or user.email_verify_token_expiry < datetime.utcnow():
        return render_template('verify_email_result.html', status='expired', logged_in=logged_in)

    user.email_verified = True
    user.email_verify_token_hash = None
    user.email_verify_token_expiry = None
    db.session.commit()
    return render_template('verify_email_result.html', status='success', logged_in=logged_in)


@auth_bp.route('/verify-email/resend', methods=['POST'])
@limiter.limit('3 per hour')
def resend_verification_email():
    """Login-required (operates only on the current session's own account) rather than
    taking an email address as input -- sidesteps any 'does this email exist' enumeration
    entirely, since there's nothing to guess: it always targets whoever is already logged
    in. Used by the dashboard's "Resend email" banner. See resend_verification_public
    below for the logged-out equivalent (e.g. from an expired verification link)."""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(username=session['user']['username']).first()
    if not user:
        return redirect(url_for('auth.login'))
    if user.email_verified:
        flash('Your email is already confirmed.', 'success')
        return redirect(request.referrer or url_for('dashboard.dashboard'))
    try:
        send_verification_email(user)
        flash('Verification email sent — check your inbox.', 'success')
    except Exception:
        logger.exception('Failed to resend verification email for user %s', user.id)
        flash('Could not send the email right now — please try again shortly.', 'error')
    return redirect(request.referrer or url_for('dashboard.dashboard'))


@auth_bp.route('/verify-email/resend-public', methods=['POST'])
@limiter.limit('5 per hour')
def resend_verification_public():
    """Same account-enumeration-proof pattern as forgot_password() below (generic
    response regardless of whether the email exists, is already verified, or the send
    itself fails) -- reachable from verify_email_result.html's expired/invalid state for
    someone who isn't (or is no longer) logged in, so "Resend verification email" doesn't
    require signing back in first."""
    email = request.form.get('email', '').strip().lower()
    if email:
        user = User.query.filter_by(email=email).first()
        if user and not user.email_verified:
            try:
                send_verification_email(user)
            except Exception:
                logger.exception('Failed to send verification email via public resend')
    flash("If an account exists with this email and hasn't been verified yet, "
          "we've sent a new verification link.", 'success')
    return redirect(url_for('auth.login'))


# ---------- New Password Reset Routes ----------
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@limiter.limit('5 per hour')
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Please enter your email address.', 'error')
            return redirect(url_for('auth.forgot_password'))

        user = User.query.filter_by(email=email).first()

        if user:
            # Generate secure token and expiry. Only the hash is persisted -- see
            # models.py's reset_token_hash docstring and _hash_token above.
            token = secrets.token_urlsafe(32)
            user.reset_token_hash = _hash_token(token)
            user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_MINUTES)
            db.session.commit()

            # request.host_url reflects whatever Host header this request actually
            # arrived on -- ProxyFix (app.py) trusts Render's X-Forwarded-Proto, so this
            # is 'https://nelavista.com/...' in production and 'http://localhost:5000/...'
            # locally, never a hardcoded domain that could point the wrong way.
            reset_link = f"{request.host_url}reset-password?token={token}"
            try:
                send_password_reset_email(user.email, reset_link)
            except Exception:
                # Logged with full detail server-side (e.g. "MAIL_USERNAME/MAIL_PASSWORD
                # not set", or the real SMTPAuthenticationError) -- but the response to
                # the client below is identical to the "no such account" and "sent fine"
                # cases. Previously this branch returned a distinct "Unable to send email"
                # flash *only* when the account existed, which let anyone probe which
                # emails were registered simply by watching which message they got back
                # while the mail system was down -- exactly the enumeration this endpoint
                # is supposed to prevent.
                logger.exception('Failed to send password reset email for user %s', user.id)

        # Always the same response, regardless of whether the account exists, is
        # unverified, or the email send itself failed -- see the comment above.
        flash("If an account exists with this email, a password reset link has been sent.", 'success')
        return redirect(url_for('auth.login'))

    # GET request
    return render_template('forgot_password.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
@limiter.limit('10 per hour')
def reset_password():
    token = request.args.get('token')
    if not token:
        flash('Reset link is invalid or expired.', 'error')
        return redirect(url_for('auth.forgot_password'))

    # Find user by token and check expiry
    user = User.query.filter_by(reset_token_hash=_hash_token(token)).first()
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        flash('Reset link is invalid or expired.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        errors = []
        strength_error = password_strength_error(password)
        if strength_error:
            errors.append(strength_error)
        if password != confirm:
            errors.append('Passwords do not match.')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('reset_password.html')

        # Update password and invalidate the token so the same link can't be replayed
        user.set_password(password)
        user.reset_token_hash = None
        user.reset_token_expiry = None
        db.session.commit()

        flash('Password reset successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    # GET request: render the form
    return render_template('reset_password.html')