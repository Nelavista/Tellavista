from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.models import User, EmployerProfile, StudentPrivacySettings, Skill
from app.extensions import db
from app.services.talent_search_service import search_talent, language_options, STATUS_FILTERS
from app.services.language_profile_service import language_label

employer_bp = Blueprint('employer', __name__)


def employer_required(f):
    """Sibling to admin_required in utils/helpers.py — gates a route to logged-in
    employer accounts specifically, checked against the live DB."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        user = User.query.filter_by(username=session['user']['username']).first()
        if not user or not user.is_employer:
            flash('That page is only available to employer accounts.')
            return redirect(url_for('dashboard.choose_path'))
        return f(*args, **kwargs)
    return decorated


def _current_employer():
    return User.query.filter_by(username=session['user']['username']).first()


@employer_bp.route('/employer/signup', methods=['GET', 'POST'])
def employer_signup():
    """Creates a genuine third account type (User.is_employer=True) through the exact
    same auth system as students/admins — no parallel login, no separate password store."""
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        contact_name = request.form.get('contact_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        industry = request.form.get('industry', '').strip() or None
        website = request.form.get('website', '').strip() or None

        if not company_name or not username or not email or not password:
            flash('Please fill out all required fields.')
            return redirect(url_for('employer.employer_signup'))

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            flash('Username or email already exists.')
            return redirect(url_for('employer.employer_signup'))

        user = User(username=username, email=email, name=contact_name or None, is_employer=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = EmployerProfile(
            user_id=user.id, company_name=company_name, industry=industry, website=website,
        )
        db.session.add(profile)
        db.session.commit()

        session.permanent = True
        session['user'] = {
            'username': user.username, 'email': user.email,
            'joined_on': user.joined_on.strftime('%Y-%m-%d'),
            'last_login': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'is_admin': False, 'preferred_path': None,
        }
        flash('Employer account created!')
        return redirect(url_for('employer.dashboard'))

    return render_template('employer_signup.html')


@employer_bp.route('/employer/dashboard')
@employer_required
def dashboard():
    user = _current_employer()
    profile = user.employer_profile
    discoverable_count = StudentPrivacySettings.query.filter(
        StudentPrivacySettings.profile_visibility.in_(['employers', 'public'])
    ).count()
    return render_template('employer_dashboard.html', profile=profile, discoverable_count=discoverable_count, active_page='dashboard')


def talent_viewer_required(f):
    """Employer accounts, plus Nelavista admins (who run the talent pipeline before any
    partner organisation has an employer account). Students never pass."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        user = User.query.filter_by(username=session['user']['username']).first()
        if not user or not (user.is_employer or user.is_admin):
            flash('That page is only available to employer accounts.')
            return redirect(url_for('dashboard.choose_path'))
        return f(*args, **kwargs)
    return decorated


@employer_bp.route('/employer/discover')
@talent_viewer_required
def discover():
    """Students are discoverable only if they've opted in (profile_visibility in
    'employers'/'public') — an empty result here is the correct, safe default for a class
    with nobody opted in yet, not a bug. Filters and results are built from the same
    records a student's own Skill Transcript and Talent Profile use (see
    services/talent_search_service.py) — an employer sees exactly what the student's
    profile shows, never a separate, richer view."""
    level = request.args.get('level', '').strip()
    status = request.args.get('status', '').strip()
    filters = {
        'q': request.args.get('q', '').strip(),
        'skill_id': request.args.get('skill_id', type=int),
        'language': request.args.get('language', '').strip(),
        'level': level if level in ('beginner', 'intermediate', 'advanced') else '',
        'status': status if status in STATUS_FILTERS else '',
        'practical_done': request.args.get('practical_done') == '1',
        'background': request.args.get('background', '').strip(),
        'min_rating': request.args.get('min_rating', type=float),
        'verified_only': request.args.get('verified_only') == '1',
    }
    results = search_talent(**filters)
    skills = Skill.query.filter_by(is_published=True).order_by(Skill.name).all()
    return render_template(
        'employer_discover.html', results=results, skills=skills, filters=filters,
        language_options=language_options(), status_options=STATUS_FILTERS, language_label=language_label,
        skill_id=filters['skill_id'], min_rating=filters['min_rating'], verified_only=filters['verified_only'],
        q=filters['q'], active_page='discover',
    )


@employer_bp.route('/employer/students/<int:student_id>')
@talent_viewer_required
def student_view(student_id):
    """An employer's view of a student is the exact same Talent Profile the student sees
    of themselves — one page, one source of truth, not a separate employer-only template
    that could drift out of sync with what the student thinks they're showing."""
    student = User.query.get_or_404(student_id)
    return redirect(url_for('skills.talent_public', username=student.username))
