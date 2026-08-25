from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models import User, EmployerProfile, StudentPrivacySettings, StudentSkill, Skill
from extensions import db
from services.skills_service import get_talent_stats, is_skill_verified

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


@employer_bp.route('/employer/discover')
@employer_required
def discover():
    """Students are discoverable only if they've opted in (profile_visibility in
    'employers'/'public') — an empty result here is the correct, safe default for a class
    with nobody opted in yet, not a bug. Filters and results are built from the same
    get_talent_stats() a student's own Talent Profile uses — an employer sees exactly
    what the student's profile shows, never a separate, richer view."""
    skill_id = request.args.get('skill_id', type=int)
    min_rating = request.args.get('min_rating', type=float)
    verified_only = request.args.get('verified_only') == '1'
    q = request.args.get('q', '').strip()

    query = (
        db.session.query(StudentPrivacySettings, User)
        .join(User, StudentPrivacySettings.student_id == User.id)
        .filter(StudentPrivacySettings.profile_visibility.in_(['employers', 'public']))
    )
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(User.name.ilike(like), User.username.ilike(like), User.university.ilike(like)))
    rows = query.order_by(User.name).all()

    results = []
    for privacy, student in rows:
        if skill_id:
            has_progress = StudentSkill.query.filter_by(student_id=student.id, skill_id=skill_id).first() is not None
            if not has_progress:
                continue
            if verified_only and not is_skill_verified(student.id, skill_id):
                continue
        stats = get_talent_stats(student)
        if verified_only and not skill_id and not stats['verified_skills']:
            continue
        if min_rating and (not stats['avg_rating'] or stats['avg_rating'] < min_rating):
            continue
        results.append({'student': student, 'privacy': privacy, 'stats': stats})

    skills = Skill.query.filter_by(is_published=True).order_by(Skill.name).all()
    return render_template(
        'employer_discover.html', results=results, skills=skills,
        skill_id=skill_id, min_rating=min_rating, verified_only=verified_only, q=q, active_page='discover',
    )


@employer_bp.route('/employer/students/<int:student_id>')
@employer_required
def student_view(student_id):
    """An employer's view of a student is the exact same Talent Profile the student sees
    of themselves — one page, one source of truth, not a separate employer-only template
    that could drift out of sync with what the student thinks they're showing."""
    student = User.query.get_or_404(student_id)
    return redirect(url_for('skills.talent_public', username=student.username))
