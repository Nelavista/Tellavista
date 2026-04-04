from flask import Blueprint, render_template, redirect, url_for, session, flash
from utils.helpers import login_required
from models import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def landing():
    user = session.get('user')
    if user:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('landing.html')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_data = session.get('user')
    if not user_data:
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(username=user_data['username']).first()
    if user and not user.department:
        flash('Please complete your academic profile to continue.', 'warning')
        return redirect(url_for('profile.profile'))
    return render_template('index.html', user=user_data)