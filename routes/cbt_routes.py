from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils.helpers import login_required
from models import User

cbt_bp = Blueprint('cbt', __name__)


@cbt_bp.route('/CBT', methods=['GET'])
@login_required
def CBT():
    """Mock Exam / CBT Practice page"""

    # Get username from session (custom auth)
    username = session.get('user', {}).get('username')
    if not username:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))

    # Query the user from database
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found. Please log in again.', 'error')
        return redirect(url_for('auth.login'))

    return render_template(
        "CBT.html",
        user_dept=user.department or '',
        user_level=user.level or '',
        user_name=user.name or 'Student'
    )
