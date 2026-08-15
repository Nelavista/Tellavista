from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models import User, EmployerProfile, StudentPrivacySettings, CohortEnrollment, Cohort, SkillCourse, Skill, StudentProject
from extensions import db
from services.gpa_service import compute_skill_gpa, get_cohort_rank
from services.daily_class_service import get_class_progress_pct

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
    with nobody opted in yet, not a bug."""
    skill_id = request.args.get('skill_id', type=int)
    min_gpa = request.args.get('min_gpa', type=float)
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
        enrollments = CohortEnrollment.query.filter_by(student_id=student.id).all()
        best = None
        matched_skill = False
        for enrollment in enrollments:
            course = enrollment.cohort.course
            if skill_id and course.skill_id != skill_id:
                continue
            if skill_id:
                matched_skill = True
            gpa_data = compute_skill_gpa(enrollment)
            if gpa_data['gpa'] is not None and (best is None or gpa_data['gpa'] > best['gpa_data']['gpa']):
                rank, total = get_cohort_rank(enrollment)
                best = {'course': course, 'gpa_data': gpa_data, 'rank': rank, 'cohort_total': total}
        if skill_id and not matched_skill:
            continue
        if min_gpa and (not best or best['gpa_data']['gpa'] is None or best['gpa_data']['gpa'] < min_gpa):
            continue
        results.append({'student': student, 'privacy': privacy, 'best': best})

    skills = Skill.query.filter_by(is_published=True).order_by(Skill.name).all()
    return render_template(
        'employer_discover.html', results=results, skills=skills,
        skill_id=skill_id, min_gpa=min_gpa, q=q, active_page='discover',
    )


@employer_bp.route('/employer/students/<int:student_id>')
@employer_required
def student_view(student_id):
    student = User.query.get_or_404(student_id)
    privacy = StudentPrivacySettings.query.filter_by(student_id=student.id).first()
    if not privacy or privacy.profile_visibility not in ('employers', 'public'):
        flash("This student's profile isn't available.")
        return redirect(url_for('employer.discover'))

    rows = []
    if privacy.show_skill_transcript:
        for enrollment in CohortEnrollment.query.filter_by(student_id=student.id).all():
            course = enrollment.cohort.course
            gpa_data = compute_skill_gpa(enrollment)
            rank, total = get_cohort_rank(enrollment)
            rows.append({
                'course': course, 'skill': course.skill, 'gpa_data': gpa_data,
                'rank': rank, 'cohort_total': total, 'pct': get_class_progress_pct(course, enrollment),
            })

    projects = []
    if privacy.show_projects:
        projects = StudentProject.query.filter_by(student_id=student.id, status='completed').all()

    return render_template(
        'employer_student_view.html', student=student, privacy=privacy, rows=rows,
        projects=projects, active_page='discover',
    )
