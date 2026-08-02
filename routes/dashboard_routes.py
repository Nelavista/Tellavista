from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify
from utils.helpers import login_required, admin_required, check_profile_complete
from models import User, Material
from extensions import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

# NOTE: study-session/exam/user-courses tracking used to be duplicated here (session-backed,
# ephemeral) and in routes/materials_routes.py (DB-backed, persistent). The two silently
# shadowed each other since both registered the same URLs. materials_routes.py's DB-backed
# versions are now the sole implementation — see routes/materials_routes.py.


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
                           show_profile_modal=show_profile_modal)

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