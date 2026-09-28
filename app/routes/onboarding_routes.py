"""PRD §5.2 sequential academic onboarding -- see services/onboarding_service.py.

One page + four small JSON step endpoints (each filtered by the prior selection) +
the save + waitlist capture. Editable later from profile: /onboarding stays reachable
and pre-fills the student's current context (get_onboarding_options).
"""
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash

from app.models import User
from app.utils.helpers import login_required
from app.services import onboarding_service
from app.services import analytics

onboarding_bp = Blueprint('onboarding', __name__)


def _user():
    return User.query.filter_by(username=session['user']['username']).first()


@onboarding_bp.route('/onboarding')
@login_required
def wizard():
    user = _user()
    if not user:
        return redirect(url_for('auth.login'))
    options = onboarding_service.get_onboarding_options(user)
    return render_template('onboarding.html', user=user, options=options)


@onboarding_bp.route('/api/onboarding/faculties')
@login_required
def api_faculties():
    return jsonify({'faculties': onboarding_service.faculties_for(request.args.get('university', ''))})


@onboarding_bp.route('/api/onboarding/departments')
@login_required
def api_departments():
    return jsonify({'departments': onboarding_service.departments_for(
        request.args.get('university', ''), request.args.get('faculty', ''))})


@onboarding_bp.route('/api/onboarding/sessions')
@login_required
def api_sessions():
    return jsonify({'sessions': onboarding_service.sessions_for(request.args.get('university', ''))})


@onboarding_bp.route('/api/onboarding/courses')
@login_required
def api_courses():
    return jsonify({'courses': onboarding_service.courses_for(
        request.args.get('university', ''),
        request.args.get('department', ''),
        request.args.get('level', ''),
    )})


@onboarding_bp.route('/api/onboarding/enrolled')
@login_required
def api_enrolled():
    user = _user()
    return jsonify({'course_ids': sorted(onboarding_service.already_enrolled_course_ids(user))})


@onboarding_bp.route('/api/onboarding/save', methods=['POST'])
@login_required
def api_save():
    user = _user()
    if not user:
        return jsonify({'success': False, 'error': 'not_found'}), 401
    data = request.get_json(silent=True) or {}
    ok, error = onboarding_service.save_onboarding(user, data)
    if not ok:
        return jsonify({'success': False, 'error': error}), 400
    # PRD §21 activation funnel: wizard *completed* (not merely started), with the
    # enrolled-course count as the activation-depth signal. Best-effort/no-op without
    # POSTHOG_API_KEY -- see services/analytics.py.
    analytics.capture_event_for_user(
        user.username, analytics.EVENT_ONBOARDING_COMPLETED,
        {'courses_enrolled': len(data.get('course_ids') or [])},
    )
    # Keep the session's cached academic snapshot in step with the DB.
    session['user']['preferred_path'] = session['user'].get('preferred_path')
    flash('Academic profile saved!', 'success')
    return jsonify({'success': True, 'redirect': url_for('dashboard.dashboard')})


@onboarding_bp.route('/api/onboarding/waitlist', methods=['POST'])
@login_required
def api_waitlist():
    user = _user()
    data = request.get_json(silent=True) or {}
    result = onboarding_service.save_waitlist(
        user,
        data.get('university', ''),
        data.get('department', ''),
        level=(data.get('level') or '').strip() or None,
    )
    return jsonify({'success': True, **result})
