"""Admin management of student opportunities. Registered on admin_skills_bp (imported at
the bottom of routes/admin_skills_routes.py). The paid-gig admin is still at
/admin/skills/opportunities, now labelled "Gigs" in the admin nav.

Server-side rules (services/student_opportunity_service.py):
- "verified" needs a source URL and an official application URL;
- publishing needs verified + source + application route + a deadline or "rolling",
  and is refused for closed or archived listings;
- NELAVISTA_APPLICATION is refused unless the listing records a real partnership.
"""
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, session

from app.extensions import db
from app.models import User, StudentOpportunity, StudentOpportunityReport, StudentOpportunityEvent
from app.routes.admin_skills_routes import admin_skills_bp
from app.utils.helpers import login_required, admin_required
from app.services import student_opportunity_service as svc


def _admin():
    return User.query.filter_by(username=session['user']['username']).first()


def _form_context(opp, errors=None):
    return dict(
        opp=opp, errors=errors or [], categories=svc.CATEGORIES, disciplines=svc.DISCIPLINES, levels=svc.LEVELS,
        location_scopes=svc.LOCATION_SCOPES, formats=svc.DELIVERY_FORMATS, modes=svc.APPLICATION_MODES,
        mode_labels=svc.APPLICATION_MODE_LABELS, status=svc.compute_status(opp) if opp.title else None,
        publish_problems=svc.publish_problems(opp) if opp.id else [], needs_recheck=svc.needs_recheck(opp) if opp.id else False,
        stats=(svc.analytics_for([opp.id]).get(opp.id, {}) if opp.id else {}),
        reports=(opp.reports.order_by(StudentOpportunityReport.created_at.desc()).all() if opp.id else []),
        active_page='student_opportunities',
    )


@admin_skills_bp.route('/admin/opportunities')
@login_required
@admin_required
def admin_student_opportunities():
    view = request.args.get('view', 'all')
    q = (request.args.get('q') or '').strip().lower()
    today = svc.today_wat()
    all_opps = StudentOpportunity.query.order_by(StudentOpportunity.updated_at.desc()).all()
    open_reports = {}
    for r in StudentOpportunityReport.query.filter_by(resolved=False).all():
        open_reports[r.opportunity_id] = open_reports.get(r.opportunity_id, 0) + 1

    def bucket(o):
        st = svc.compute_status(o, today)['key']
        if o.is_archived:
            return 'archived'
        if o.is_published and o.is_verified and st in ('open', 'closing_soon', 'upcoming'):
            return 'live'
        if st == 'closed':
            return 'closed'
        return 'drafts'

    counts = {'all': 0, 'live': 0, 'drafts': 0, 'closed': 0, 'archived': 0, 'recheck': 0, 'reported': 0}
    rows = []
    for o in all_opps:
        b = bucket(o)
        recheck = o.is_published and svc.needs_recheck(o)
        counts['all'] += 1 if b != 'archived' else 0
        counts[b] += 1
        counts['recheck'] += 1 if recheck else 0
        counts['reported'] += 1 if open_reports.get(o.id) else 0
        if view == 'recheck' and not recheck:
            continue
        if view == 'reported' and not open_reports.get(o.id):
            continue
        if view in ('live', 'drafts', 'closed', 'archived') and b != view:
            continue
        if view == 'all' and b == 'archived':
            continue
        if q and q not in f'{o.title} {o.organization}'.lower():
            continue
        rows.append({'o': o, 'bucket': b, 'status': svc.compute_status(o, today), 'recheck': recheck,
                     'reports': open_reports.get(o.id, 0)})

    stats = svc.analytics_for([r['o'].id for r in rows])
    since = datetime.utcnow() - timedelta(days=30)
    totals = dict(db.session.query(StudentOpportunityEvent.event_type, db.func.count(StudentOpportunityEvent.id))
                  .filter(StudentOpportunityEvent.created_at >= since)
                  .group_by(StudentOpportunityEvent.event_type).all())
    return render_template('admin_student_opportunities.html', rows=rows, counts=counts, view=view, q=q,
                           stats=stats, totals=totals, labels=svc.CATEGORY_SINGULAR, active_page='student_opportunities')


@admin_skills_bp.route('/admin/opportunities/new', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_student_opportunity_new():
    opp = StudentOpportunity(category='scholarship', location_scope='nigeria', application_mode='EXTERNAL_WEBVIEW',
                             verification_status='unverified', is_published=False, featured=False, is_rolling=False,
                             is_partner=False, allows_in_app_view=False, manually_closed=False, is_archived=False)
    if request.method == 'POST':
        errors = svc.apply_form(opp, request.form, request.form.getlist)
        if errors:
            return render_template('admin_student_opportunity_edit.html', **_form_context(opp, errors)), 400
        opp.created_by_id = _admin().id
        db.session.add(opp)
        db.session.commit()
        flash('Saved as a draft. Verify it against the official source, then publish.')
        return redirect(url_for('admin_skills.admin_student_opportunity_edit', opportunity_id=opp.id))
    return render_template('admin_student_opportunity_edit.html', **_form_context(opp))


@admin_skills_bp.route('/admin/opportunities/<int:opportunity_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_student_opportunity_edit(opportunity_id):
    opp = StudentOpportunity.query.get_or_404(opportunity_id)
    if request.method == 'POST':
        was_published = opp.is_published
        errors = svc.apply_form(opp, request.form, request.form.getlist)
        if errors:
            # Render with what the admin typed, then throw the unsaved changes away.
            html = render_template('admin_student_opportunity_edit.html', **_form_context(opp, errors))
            db.session.rollback()
            return html, 400
        db.session.commit()
        if was_published and not opp.is_published:
            flash('Saved, and unpublished: it no longer passes the publish checks.')
        else:
            flash('Saved.')
        return redirect(url_for('admin_skills.admin_student_opportunity_edit', opportunity_id=opp.id))
    return render_template('admin_student_opportunity_edit.html', **_form_context(opp))


@admin_skills_bp.route('/admin/opportunities/<int:opportunity_id>/action', methods=['POST'])
@login_required
@admin_required
def admin_student_opportunity_action(opportunity_id):
    opp = StudentOpportunity.query.get_or_404(opportunity_id)
    ok, message = svc.admin_action(opp, request.form.get('action', ''), _admin())
    if ok:
        db.session.commit()
    else:
        db.session.rollback()
    flash(message)
    return redirect(request.form.get('next') or url_for('admin_skills.admin_student_opportunity_edit', opportunity_id=opp.id))


@admin_skills_bp.route('/admin/opportunities/<int:opportunity_id>/check-framing', methods=['POST'])
@login_required
@admin_required
def admin_student_opportunity_check_framing(opportunity_id):
    opp = StudentOpportunity.query.get_or_404(opportunity_id)
    result = svc.check_framing(opp.application_url)
    if result is None:
        flash("Couldn't reach the application URL to check it. In-app view stays off.")
        opp.allows_in_app_view = False
        opp.framing_checked_at = None
    elif result:
        opp.framing_checked_at = datetime.utcnow()
        flash('The site doesn\'t block framing. You can now tick "Show in-app" and save. '
              'Test it yourself first: login-protected portals may still not load in a frame.')
    else:
        opp.allows_in_app_view = False
        opp.framing_checked_at = None
        flash('The site blocks framing. Students will open it over Nelavista instead (new tab / in-app browser).')
    db.session.commit()
    return redirect(url_for('admin_skills.admin_student_opportunity_edit', opportunity_id=opp.id))


@admin_skills_bp.route('/admin/opportunities/<int:opportunity_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_student_opportunity_delete(opportunity_id):
    opp = StudentOpportunity.query.get_or_404(opportunity_id)
    if opp.applications.first() or opp.saves.first():
        flash('Students have saved or applied to this. Archive it instead, so their history stays intact.')
        return redirect(url_for('admin_skills.admin_student_opportunity_edit', opportunity_id=opp.id))
    db.session.delete(opp)
    db.session.commit()
    flash('Deleted.')
    return redirect(url_for('admin_skills.admin_student_opportunities'))


@admin_skills_bp.route('/admin/opportunities/reports/<int:report_id>/resolve', methods=['POST'])
@login_required
@admin_required
def admin_student_opportunity_resolve_report(report_id):
    report = StudentOpportunityReport.query.get_or_404(report_id)
    report.resolved = True
    report.resolved_at = datetime.utcnow()
    db.session.commit()
    flash('Report resolved.')
    return redirect(url_for('admin_skills.admin_student_opportunity_edit', opportunity_id=report.opportunity_id))
