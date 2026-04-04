from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.helpers import login_required
from models import User
from extensions import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        user.name = request.form.get('name', '').strip() or None
        user.university = request.form.get('university', '').strip() or None
        user.faculty = request.form.get('faculty', '').strip() or None
        user.department = request.form.get('department', '').strip() or None
        user.level = request.form.get('level', '').strip() or None
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('profile.html', user=user)