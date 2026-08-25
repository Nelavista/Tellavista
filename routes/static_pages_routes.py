from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from utils.helpers import login_required

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/about')
def about():
    return render_template('about.html')


@pages_bp.route('/campus-map')
def campus_map():
    return render_template('campus-map.html')


@pages_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@pages_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')


@pages_bp.route('/settings')
@login_required
def settings():
    memory = {
        "traits": session.get('traits', []),
        "more_info": session.get('more_info', ''),
        "enable_memory": session.get('enable_memory', False)
    }
    return render_template('settings.html', memory=memory,
                           theme=session.get('theme'), language=session.get('language'))


@pages_bp.route('/memory', methods=['POST'])
@login_required
def save_memory():
    session['theme'] = request.form.get('theme')
    session['language'] = request.form.get('language')
    session['notifications'] = 'notifications' in request.form
    if 'traits' in request.form:
        session['traits'] = request.form.getlist('traits')
    if 'more_info' in request.form:
        session['more_info'] = request.form.get('more_info')
    if 'enable_memory' in request.form:
        session['enable_memory'] = request.form.get('enable_memory') == 'on'
    if request.form.get('ajax') == '1':
        return {'success': True}
    flash('Settings saved!')
    return redirect(url_for('pages.settings'))


@pages_bp.route("/mat101")
def math101():
    return render_template("mat101.html")
