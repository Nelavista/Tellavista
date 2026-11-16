"""Discover: third-party student opportunities (scholarships, fellowships, competitions,
internships, ambassador and leadership programmes) inside the Opportunities space.

Registered on opportunities_bp (imported at the bottom of routes/opportunities_routes.py),
so these pages use the Opportunities shell and its stale-session guard, at
/opportunities/discover/... The space's other pages are untouched: matched work
(/opportunities), open gigs and earnings. They're the paid-gig ledger (the Opportunity
model), a different thing from these externally run programmes.

Boundary note (see opportunities_routes.py): the "competitions" listed here are external
programmes run by other organisations (Hult Prize, CFA Research Challenge...). Nelavista's
own skill-showcase Competitions stay in Skills.

All the rules are in services/student_opportunity_service.py. In particular, students
only ever see published + verified + not-archived listings, and "I applied" is the
student's own record. Nelavista can't see whether the external application went through.
"""
from datetime import datetime
from flask import render_template, request, jsonify, redirect, url_for, flash, abort, session

from app.extensions import db, limiter
from app.models import StudentOpportunity
from app.routes.opportunities_routes import opportunities_bp, _current_user
from app.utils.helpers import login_required
from app.services import student_opportunity_service as svc


def _wants_json():
    return request.is_json or 'application/json' in (request.headers.get('Accept') or '')


def _ui():
    """Helpers every Discover template uses (labels, status, deadline formatting)."""
    return {
        'status': svc.compute_status,
        'deadline': svc.format_deadline,
        'category_labels': svc.CATEGORY_LABELS,
        'category_singular': svc.CATEGORY_SINGULAR,
        'category_icons': svc.CATEGORY_ICONS,
        'discipline_labels': svc.DISCIPLINE_LABELS,
        'level_labels': svc.LEVEL_LABELS,
        'location_labels': svc.LOCATION_SCOPE_LABELS,
        'mode': svc.effective_application_mode,
    }


def _get_visible(opportunity_id, user):
    opp = StudentOpportunity.query.get_or_404(opportunity_id)
    if not svc.can_view(opp, user):
        abort(404)
    return opp


@opportunities_bp.route('/opportunities/discover')
@login_required
def discover():
    user = _current_user()
    feed = svc.build_feed(user, request.args)
    shown = feed['results'] + feed['closing_soon'] + feed['featured'] + feed['new'] + feed['for_you'] + feed['upcoming']
    state = svc.user_state(user, {o.id for o in shown})

    def filter_url(**overrides):
        params = {k: v for k, v in feed['filters'].items() if v}
        if feed['sort'] != 'relevance':
            params['sort'] = feed['sort']
        params.update(overrides)
        return url_for('opportunities.discover', **{k: v for k, v in params.items() if v})

    return render_template(
        'opportunities_discover.html', feed=feed, state=state, ui=_ui(), active_page='discover',
        filter_url=filter_url,
        chip_categories=[(k, svc.CATEGORY_LABELS[k], svc.CATEGORY_ICONS[k]) for k in svc.FILTER_CHIP_CATEGORIES],
        all_categories=svc.CATEGORIES, disciplines=svc.DISCIPLINES, levels=svc.LEVELS,
        location_scopes=svc.LOCATION_SCOPES, deadline_filters=svc.DEADLINE_FILTERS,
    )


@opportunities_bp.route('/opportunities/discover/mine')
@login_required
def discover_mine():
    user = _current_user()
    data = svc.my_opportunities(user)
    tab = request.args.get('tab') if request.args.get('tab') in ('saved', 'applied', 'closing', 'recommended') else 'saved'
    ids = {o.id for o in data['saved'] + data['closing'] + data['recommended']} | {a.opportunity_id for a in data['applied']}
    return render_template('opportunities_discover_mine.html', data=data, tab=tab, state=svc.user_state(user, ids),
                           ui=_ui(), active_page='discover_mine')


@opportunities_bp.route('/opportunities/discover/archive')
@login_required
def discover_archive():
    user = _current_user()
    today = svc.today_wat()
    closed = [o for o in svc.visible_query().all() if svc.compute_status(o, today)['key'] == 'closed']
    closed.sort(key=lambda o: o.deadline or datetime.min.date(), reverse=True)
    return render_template('opportunities_discover_archive.html', closed=closed[:100],
                           state=svc.user_state(user, {o.id for o in closed[:100]}), ui=_ui(), active_page='discover')


@opportunities_bp.route('/opportunities/discover/<slug>')
@login_required
def discover_detail(slug):
    user = _current_user()
    opp = StudentOpportunity.query.filter_by(slug=slug).first_or_404()
    if not svc.can_view(opp, user):
        abort(404)
    # One 'view' per student per listing per session: a refresh isn't a new view.
    viewed = session.get('opp_viewed', [])
    if opp.id not in viewed and opp.is_published:
        svc.log_event(opp, user, 'view', channel=(request.args.get('from') or '')[:30] or None)
        db.session.commit()
        session['opp_viewed'] = (viewed + [opp.id])[-60:]
    state = svc.user_state(user, [opp.id]).get(opp.id, {'saved': False, 'applied_at': None})
    profile = svc.profile_for(user)
    related = [o for o in svc.active_opportunities() if o.id != opp.id
               and (o.category == opp.category or svc.is_for_you(o, profile))]
    related.sort(key=lambda o: (o.category != opp.category, -svc.relevance_score(o, profile)))
    return render_template(
        'opportunities_discover_detail.html', opp=opp, status=svc.compute_status(opp), state=state,
        mode=svc.effective_application_mode(opp), related=related[:3],
        related_state=svc.user_state(user, [o.id for o in related[:3]]), ui=_ui(),
        report_reasons=svc.REPORT_REASONS, needs_recheck=svc.needs_recheck(opp),
        share_url=url_for('opportunities.discover_detail', slug=opp.slug, _external=True),
        active_page='discover',
    )


@opportunities_bp.route('/opportunities/discover/<slug>/apply')
@login_required
def discover_apply(slug):
    """The Apply button. Logs the click, then either shows the official page inside the
    Nelavista frame (only when an admin enabled it after a framing check), or hands off to
    the official URL. Nelavista never alters or proxies the organisation's page."""
    user = _current_user()
    opp = StudentOpportunity.query.filter_by(slug=slug).first_or_404()
    if not svc.can_view(opp, user):
        abort(404)
    if not opp.application_url:
        flash('This listing has no application link yet.')
        return redirect(url_for('opportunities.discover_detail', slug=opp.slug))
    in_app = opp.allows_in_app_view and not request.args.get('go')
    if opp.is_published:
        svc.log_event(opp, user, 'apply_click', channel='in_app' if in_app else 'external')
        db.session.commit()
    if in_app:
        state = svc.user_state(user, [opp.id]).get(opp.id, {'saved': False, 'applied_at': None})
        return render_template('opportunities_discover_apply.html', opp=opp, state=state, ui=_ui())
    return redirect(opp.application_url)


@opportunities_bp.route('/opportunities/discover/<int:opportunity_id>/save', methods=['POST'])
@login_required
def discover_save(opportunity_id):
    user = _current_user()
    opp = _get_visible(opportunity_id, user)
    data = request.get_json(silent=True) or request.form
    if 'saved' in data:
        saved = str(data.get('saved')).lower() in ('1', 'true', 'yes', 'on')
    else:
        saved = not svc.user_state(user, [opp.id]).get(opp.id, {}).get('saved', False)
    svc.set_saved(opp, user, saved)
    db.session.commit()
    if _wants_json():
        return jsonify({'success': True, 'saved': saved})
    flash('Saved to My Opportunities.' if saved else 'Removed from saved.')
    return redirect(request.referrer or url_for('opportunities.discover_detail', slug=opp.slug))


@opportunities_bp.route('/opportunities/discover/<int:opportunity_id>/applied', methods=['POST'])
@login_required
def discover_applied(opportunity_id):
    user = _current_user()
    opp = _get_visible(opportunity_id, user)
    data = request.get_json(silent=True) or request.form
    applied = str(data.get('applied', '1')).lower() in ('1', 'true', 'yes', 'on')
    record = svc.set_applied(opp, user, applied)
    db.session.commit()
    applied_at = record.applied_at if record else None
    if _wants_json():
        return jsonify({'success': True, 'applied': applied,
                        'applied_label': (f"Applied {applied_at.strftime('%b')} {applied_at.day}, {applied_at.year}" if applied_at else None)})
    flash('Added to your applications. Good luck!' if applied else 'Removed from your applications.')
    return redirect(request.referrer or url_for('opportunities.discover_detail', slug=opp.slug))


@opportunities_bp.route('/opportunities/discover/<int:opportunity_id>/share', methods=['POST'])
@login_required
@limiter.limit('60 per hour')
def discover_share(opportunity_id):
    user = _current_user()
    opp = _get_visible(opportunity_id, user)
    data = request.get_json(silent=True) or {}
    channel = data.get('channel') if data.get('channel') in ('native', 'whatsapp', 'copy', 'x', 'telegram') else 'other'
    svc.log_event(opp, user, 'share', channel=channel)
    db.session.commit()
    return jsonify({'success': True})


@opportunities_bp.route('/opportunities/discover/<int:opportunity_id>/report', methods=['POST'])
@login_required
@limiter.limit('10 per hour')
def discover_report(opportunity_id):
    user = _current_user()
    opp = _get_visible(opportunity_id, user)
    data = request.get_json(silent=True) or request.form
    try:
        svc.create_report(opp, user, data.get('reason'), data.get('details'))
    except ValueError as e:
        if _wants_json():
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(str(e))
        return redirect(url_for('opportunities.discover_detail', slug=opp.slug))
    db.session.commit()
    if _wants_json():
        return jsonify({'success': True})
    flash('Thanks. The Nelavista team will check this listing.')
    return redirect(url_for('opportunities.discover_detail', slug=opp.slug))
