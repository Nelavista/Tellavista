from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from datetime import datetime, timedelta
import secrets
from models import User
from extensions import db, mail  # Assuming 'mail' is initialized in extensions.py
from flask_mail import Message

auth_bp = Blueprint('auth', __name__)


# ---------- Email Sending Function ----------
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
    mail.send(msg)


# ---------- Existing Routes ----------
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip() or None
        university = request.form.get('university', '').strip() or None
        faculty = request.form.get('faculty', '').strip() or None
        department = request.form.get('department', '').strip() or None
        level = request.form.get('level', '').strip() or None

        if not username or not email or not password:
            flash('Please fill out all fields.')
            return redirect(url_for('auth.signup'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.')
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
        flash('Account created successfully!')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '').strip()
        if not login_input or not password:
            flash('Please enter username/email and password.')
            return redirect(url_for('auth.login'))
        user = User.query.filter((User.username == login_input) | (User.email == login_input)).first()
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
            flash('Logged in successfully!')
            # Skills (and the Employer blueprint) are currently disabled — see app.py —
            # so every login goes straight to Academia.
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


# ---------- New Password Reset Routes ----------
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Please enter your email address.', 'error')
            return redirect(url_for('auth.forgot_password'))

        user = User.query.filter_by(email=email).first()

        if user:
            # Generate secure token and expiry
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()

            # Build reset link
            reset_link = f"{request.host_url}reset-password?token={token}"
            try:
                send_password_reset_email(user.email, reset_link)
            except Exception as e:
                current_app.logger.error(f"Failed to send reset email: {e}")
                flash('Unable to send email at this time. Please try again later.', 'error')
                return redirect(url_for('auth.forgot_password'))

        # Always show the same message (security best practice)
        flash("If that email exists, you'll receive a reset link.", 'success')
        return redirect(url_for('auth.login'))

    # GET request
    return render_template('forgot_password.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    if not token:
        flash('Reset link is invalid or expired.', 'error')
        return redirect(url_for('auth.forgot_password'))

    # Find user by token and check expiry
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        flash('Reset link is invalid or expired.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        errors = []
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if password != confirm:
            errors.append('Passwords do not match.')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('reset_password.html')

        # Update password and clear token
        user.set_password(password)  # using your existing method
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        flash('Password reset successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    # GET request: render the form
    return render_template('reset_password.html')