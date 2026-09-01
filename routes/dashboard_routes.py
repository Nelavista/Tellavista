from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, request
from utils.helpers import login_required, admin_required, check_profile_complete
from models import User, Material
from extensions import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

# The two top-level experiences a user's single Nelavista account can enter. Kept as a
# module constant so choose_path() and the redirects in auth_routes.py can't drift apart.
VALID_PATHS = {'academia': 'dashboard.dashboard', 'skills': 'skills.home'}

# NOTE: study-session/exam/user-courses tracking used to be duplicated here (session-backed,
# ephemeral) and in routes/materials_routes.py (DB-backed, persistent). The two silently
# shadowed each other since both registered the same URLs. materials_routes.py's DB-backed
# versions are now the sole implementation — see routes/materials_routes.py.


def post_auth_redirect(user):
    """Where a user lands right after authenticating -- login(), signup(), and
    google_callback() in routes/auth_routes.py all call this so the three entry points
    can never drift apart on this decision. Deliberately always the Choose Your Path
    picker for a non-employer account, on every login/signup, regardless of any saved
    preferred_path: the product decision is that authenticating is itself the moment to
    choose Academia or Skills, not something to skip based on last time's pick. (This
    briefly went the other way -- skipping the picker when preferred_path was already
    set -- before being reverted back to always-show here; landing() below is a
    different case (a still-active session revisiting '/', not a fresh authentication)
    and keeps respecting the saved path, untouched by this)."""
    if user.is_employer:
        # Employers have their own separate experience entirely — no Academia/Skills
        # picker for them, since that fork doesn't apply to an employer account.
        return redirect(url_for('employer.dashboard'))
    return redirect(url_for('dashboard.choose_path'))


@dashboard_bp.route('/')
def landing():
    user_data = session.get('user')
    if user_data:
        # Academia and Skills are two separate destinations, not one merged dashboard.
        # First-ever entry (no preferred_path set yet) forks through the Choose Your Path
        # picker so the student makes a deliberate choice; every entry after that goes
        # straight to whichever space they're in — the picker no longer stands between a
        # returning user and their own dashboard. The sidebar wordmark in both shells still
        # links back to /choose-path, which remains how someone switches spaces on purpose.
        preferred_path = user_data.get('preferred_path')
        if preferred_path in VALID_PATHS:
            return redirect(url_for(VALID_PATHS[preferred_path]))
        user = User.query.filter_by(username=user_data.get('username')).first()
        if user and user.preferred_path in VALID_PATHS:
            return redirect(url_for(VALID_PATHS[user.preferred_path]))
        return redirect(url_for('dashboard.choose_path'))
    return render_template('landing.html')


@dashboard_bp.route('/choose-path', methods=['GET', 'POST'])
@login_required
def choose_path():
    """'Choose Your Path' screen — the deliberate fork between Academia and Skills. Shown
    on every login/signup/Google sign-in (post_auth_redirect() above, unconditionally,
    for a non-employer account) and on landing() ('/') only for a session with no saved
    preferred_path yet -- a still-active session revisiting '/' goes straight to its
    saved space instead. Also reachable anytime via the sidebar wordmark, for switching
    spaces on purpose without re-authenticating."""
    user_data = session.get('user')
    user = User.query.filter_by(username=user_data['username']).first()
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('auth.login'))
    if user.is_employer:
        # Employers have no Academia/Skills fork to choose between — straight to their
        # own dashboard, same as auth.login already does for them.
        return redirect(url_for('employer.dashboard'))

    if request.method == 'POST':
        path = request.form.get('path')
        if path not in VALID_PATHS:
            flash('Please choose a valid path.')
            return redirect(url_for('dashboard.choose_path'))
        user.preferred_path = path
        db.session.commit()
        session['user']['preferred_path'] = path
        session.modified = True
        return redirect(url_for(VALID_PATHS[path]))

    if user.name:
        first_name = user.name.strip().split()[0]
    else:
        first_name = None
    return render_template('choose_path.html', user=user_data, first_name=first_name)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_data = session.get('user')
    if not user_data:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=user_data['username']).first()
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('auth.login'))

    # Determine if profile completion modal should be shown
    show_profile_modal = not check_profile_complete(user)

    if user and user.name:
        first_name = user.name.strip().split()[0]
    else:
        first_name = user_data.get('username', 'Student')

    exam_key = f"exams_{user_data.get('username')}"
    exams_list = session.get(exam_key, [])
    upcoming = [
        e for e in exams_list
        if e.get('date') and e['date'] >= datetime.now().strftime('%Y-%m-%d')
    ]
    exam_count = len(upcoming)

    return render_template('dashboard.html',
                           user=user_data,
                           first_name=first_name,
                           exam_count=exam_count,
                           show_profile_modal=show_profile_modal,
                           email_verified=user.email_verified)

@dashboard_bp.route('/api/debug-courses')
@login_required
@admin_required
def debug_courses():
    user_data = session.get('user')
    user = User.query.filter_by(username=user_data.get('username')).first()
    user_info = {
        'level': user.level,
        'semester': user.semester,
        'department': user.department
    }
    all_materials = Material.query.limit(10).all()
    materials_info = [{
        'course': c.course,
        'level': c.level,
        'semester': c.semester,
        'is_approved': c.is_approved
    } for c in all_materials]
    return jsonify({
        'user': user_info,
        'all_materials_in_db': materials_info,
        'total_materials': len(materials_info)
    })


@dashboard_bp.route('/api/debug-all')
@login_required
@admin_required
def debug_all():
    from models import Video, Material
    all_videos = Video.query.limit(10).all()
    videos_info = [{
        'course': v.course,
        'level': v.level,
        'semester': v.semester,
        'department': v.department,
        'is_approved': v.is_approved
    } for v in all_videos]
    all_materials = Material.query.limit(10).all()
    materials_info = [{
        'course': c.course,
        'level': c.level,
        'semester': c.semester,
        'is_approved': c.is_approved
    } for c in all_materials]
    return jsonify({
        'videos_in_db': videos_info,
        'total_videos': len(videos_info),
        'materials_in_db': materials_info,
        'total_materials': len(materials_info)
    })


@dashboard_bp.route('/api/debug-tables')
@login_required
@admin_required
def debug_tables():
    from sqlalchemy import inspect, text
    with db.engine.connect() as conn:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        table_counts = {}
        for table in tables:
            try:
                result = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                count = result.scalar()
                table_counts[table] = count
            except Exception:
                table_counts[table] = 'error'
    return jsonify({
        'all_tables': tables,
        'row_counts': table_counts
    })