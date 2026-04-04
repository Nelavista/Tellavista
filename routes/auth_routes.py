from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from models import User
from extensions import db
from utils.helpers import login_required

auth_bp = Blueprint('auth', __name__)

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

        user = User(username=username, email=email, name=name, university=university, faculty=faculty, department=department, level=level)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user'] = {
            'username': username,
            'email': email,
            'joined_on': user.joined_on.strftime('%Y-%m-%d'),
            'last_login': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
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
            session['user'] = {
                'username': user.username,
                'email': user.email,
                'joined_on': user.joined_on.strftime('%Y-%m-%d'),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S')
            }
            flash('Logged in successfully!')
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