"""Nelavista Talent: the employer-facing talent network.

/talent                       homepage (employers first, with a path for talent)
/talent/profile/<slug>        a talent profile (labelled previews today, noindex)
/talent/request               "Request Talent" qualification form (no account needed)
/talent/request/received      confirmation after a request
/talent/join                  the talent-side entry point
/admin/talent-requests        admin: work incoming requests

All copy-level claims (metrics, vetting status, previews, photography) come from
services/talent_network.py. Read its docstring before changing what the pages claim.
"""
import re
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from app.extensions import db, limiter
from app.models import User, TalentRequest
from app.services import talent_network as tn
from app.utils.helpers import admin_required

talent_bp = Blueprint('talent', __name__)

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
FIELD_LIMITS = {
    'contact_name': 120, 'company_name': 150, 'work_email': 200, 'job_title': 120,
    'company_website': 300, 'country': 80, 'need_summary': 500, 'skills': 500, 'details': 4000,
}


def _assessment_tracks():
    """Published skills that have at least one published assessment, counted live. A
    failure here must never take the sales page down: the band simply hides."""
    try:
        from app.models import Challenge, Skill
        return (db.session.query(db.func.count(db.distinct(Challenge.skill_id)))
                .join(Skill, Skill.id == Challenge.skill_id)
                .filter(Challenge.is_assessment.is_(True), Challenge.is_published.is_(True),
                        Skill.is_published.is_(True)).scalar()) or 0
    except Exception:
        db.session.rollback()
        return 0


def _base_context():
    return {'tn': tn, 'categories': tn.CATEGORIES, 'now_year': datetime.utcnow().year,
            'whatsapp_url': tn.whatsapp_url()}


@talent_bp.route('/talent')
def home():
    return render_template(
        'talent/home.html', metrics=tn.build_metrics(_assessment_tracks()),
        talent=tn.featured_talent(), **_base_context(),
    )


@talent_bp.route('/talent/profile/<slug>')
def profile(slug):
    p = tn.get_profile(slug)
    if not p:
        abort(404)
    category = tn.CATEGORY_BY_SLUG.get(p['category'])
    related = [t for t in tn.featured_talent() if t['category'] == p['category'] and t['slug'] != slug][:2] \
        or [t for t in tn.featured_talent() if t['slug'] != slug][:2]
    return render_template('talent/profile.html', p=p, category=category, related=related, **_base_context())


def _clean(form):
    data = {}
    for key, limit in FIELD_LIMITS.items():
        data[key] = (form.get(key) or '').strip()[:limit]
    data['work_email'] = data['work_email'].lower()
    for key, options in (('category', [(c['slug'], c['name']) for c in tn.CATEGORIES] + [('other', 'Other')]),
                         ('headcount', tn.HEADCOUNTS), ('engagement_type', tn.ENGAGEMENT_TYPES),
                         ('start_window', tn.START_WINDOWS), ('budget_range', tn.BUDGET_RANGES),
                         ('timezone', tn.TIMEZONES)):
        value = (form.get(key) or '').strip()
        data[key] = value if value in dict(options) else ''
    ref = (form.get('profile_ref') or '').strip()
    data['profile_ref'] = ref if ref in tn.PREVIEW_BY_SLUG else ''
    return data


def _validate(data):
    errors = {}
    if not data['contact_name']:
        errors['contact_name'] = 'Tell us who we should speak to.'
    if not data['company_name']:
        errors['company_name'] = 'Add your company or organisation name.'
    if not EMAIL_RE.match(data['work_email']):
        errors['work_email'] = 'Enter an email address we can reply to.'
    if len(data['need_summary']) < 10:
        errors['need_summary'] = 'A sentence or two is enough, e.g. "Two chat support agents for our Lagos store."'
    if not data['engagement_type']:
        errors['engagement_type'] = 'Choose how you want to engage. "Not sure yet" is fine.'
    return errors


@talent_bp.route('/talent/request', methods=['GET', 'POST'])
@limiter.limit('8 per hour', methods=['POST'])
def request_talent():
    form_options = dict(engagement_types=tn.ENGAGEMENT_TYPES, headcounts=tn.HEADCOUNTS,
                        start_windows=tn.START_WINDOWS, budget_ranges=tn.BUDGET_RANGES, timezones=tn.TIMEZONES)
    if request.method == 'POST':
        # Honeypot: a hidden field people never fill in. Pretend success to bots.
        if request.form.get('company_fax'):
            return redirect(url_for('talent.request_received'))
        data = _clean(request.form)
        errors = _validate(data)
        if errors:
            return render_template('talent/request.html', data=data, errors=errors,
                                   ref_profile=tn.get_profile(data['profile_ref']), **form_options,
                                   **_base_context()), 400
        user = None
        if 'user' in session:
            user = User.query.filter_by(username=session['user'].get('username')).first()
        # Required fields are non-empty after _validate; optional blanks are stored as NULL.
        row = TalentRequest(**{k: (v or None) for k, v in data.items()}, status='new',
                            user_id=user.id if user else None)
        db.session.add(row)
        db.session.commit()
        # Saved first, then announced: an email failure is logged, never lost or shown.
        from app.services.talent_notify import send_request_alert
        send_request_alert(row)
        session['talent_request_name'] = data['contact_name'].split(' ')[0]
        return redirect(url_for('talent.request_received'))

    data = {'category': request.args.get('category', ''), 'profile_ref': request.args.get('profile', '')}
    if data['category'] not in tn.CATEGORY_BY_SLUG:
        data['category'] = ''
    ref_profile = tn.get_profile(data['profile_ref'])
    if ref_profile and not data['category']:
        data['category'] = ref_profile['category']
    return render_template('talent/request.html', data=data, errors={}, ref_profile=ref_profile,
                           **form_options, **_base_context())


@talent_bp.route('/talent/request/received')
def request_received():
    return render_template('talent/request_received.html', first_name=session.pop('talent_request_name', None),
                           **_base_context())


@talent_bp.route('/talent/join')
def join():
    logged_in = 'user' in session
    return render_template('talent/join.html', logged_in=logged_in, **_base_context())


# ── Admin ────────────────────────────────────────────────────────────────────────────────

@talent_bp.route('/admin/talent-requests')
@admin_required
def admin_requests():
    status = request.args.get('status', '')
    q = TalentRequest.query
    if status in dict(tn.REQUEST_STATUSES):
        q = q.filter_by(status=status)
    rows = q.order_by(TalentRequest.created_at.desc()).limit(300).all()
    counts = dict(db.session.query(TalentRequest.status, db.func.count(TalentRequest.id))
                  .group_by(TalentRequest.status).all())
    return render_template('admin_talent_requests.html', rows=rows, status=status, counts=counts,
                           tn=tn, active_page='talent_requests')


@talent_bp.route('/admin/talent-requests/<int:request_id>', methods=['POST'])
@admin_required
def admin_request_update(request_id):
    row = TalentRequest.query.get_or_404(request_id)
    new_status = request.form.get('status', '')
    if new_status in dict(tn.REQUEST_STATUSES):
        row.status = new_status
    if 'admin_notes' in request.form:
        row.admin_notes = request.form.get('admin_notes', '').strip()[:4000] or None
    db.session.commit()
    flash(f'Updated request from {row.company_name}.')
    return redirect(url_for('talent.admin_requests', status=request.args.get('status', '')))
