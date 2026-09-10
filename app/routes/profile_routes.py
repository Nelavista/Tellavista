from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.helpers import login_required
from app.models import User, University, Faculty, Department, Course
from app.extensions import db
from app.services.academic_context import sync_user_university

profile_bp = Blueprint('profile', __name__)


def _has_curriculum(user):
    """True once the real University -> Faculty -> Department -> Course taxonomy has any
    course row for this student's own university -- drives the profile page's "View
    Curriculum" card. Data-driven (not hardcoded to any one school) so it correctly turns
    on for every university that actually has course data and off for one that doesn't."""
    if not user.university_id:
        return False
    return db.session.query(Course.id).join(Department).join(Faculty).filter(
        Faculty.university_id == user.university_id
    ).first() is not None


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
        sync_user_university(user, request.form.get('university', '').strip())
        user.faculty = request.form.get('faculty', '').strip() or None
        user.department = request.form.get('department', '').strip() or None

        level = request.form.get('user_level') or request.form.get('level', '')
        user.level = level.strip() or None

        user.semester = request.form.get('semester', '').strip() or None

        db.session.commit()

        if session.get('user'):
            session['user']['name'] = user.name
            session['user']['username'] = user.username
            session['user']['semester'] = user.semester
            session['user']['level'] = user.level
            session.modified = True

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile'))

    universities = University.query.filter_by(active=True).order_by(University.name).all()
    return render_template('profile.html', user=user, universities=universities, has_curriculum=_has_curriculum(user))