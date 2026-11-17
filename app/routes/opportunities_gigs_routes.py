"""Gigs: paid work and projects, in the Opportunities space at /opportunities/gigs.

Registered on opportunities_bp (imported at the bottom of routes/opportunities_routes.py),
so these pages use the Opportunities shell and its stale-session guard.

The hub shows two kinds of gig side by side:
- Gig rows (services/gigs/): external gigs synced from providers whose terms allow it,
  plus gigs Nelavista admins add. Students apply on the official listing; "I applied"
  is their own record.
- Opportunity rows (the existing ledger): Nelavista's own gigs, applied to here and
  paid through Earnings. Their full list moved to /opportunities/gigs/nelavista.

Everything students see comes from Nelavista's database. No page calls a provider.
"""
import logging

from flask import render_template, request, jsonify, redirect, url_for, flash, abort, session
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db, limiter
from app.models import Gig, Opportunity, OpportunityApplication, StudentSkill
from app.routes.opportunities_routes import opportunities_bp, _current_user
from app.utils.helpers import login_required
from app.services.gigs import core

logger = logging.getLogger('nelavista.gigs')


def _wants_json():
    return request.is_json or 'application/json' in (request.headers.get('Accept') or '')


def _nelavista_gig_rows(user, limit=6):
    """The ledger's published gigs for the hub's "Apply on Nelavista" rail."""
    progress = {s.skill_id: s.progress_pct for s in StudentSkill.query.filter_by(student_id=user.id).all()}
    apps = {a.opportunity_id: a for a in OpportunityApplication.query.filter_by(student_id=user.id).all()}
    opps = Opportunity.query.filter_by(is_published=True).order_by(Opportunity.created_at.desc()).limit(50).all()
    rows = [{'opportunity': o, 'application': apps.get(o.id), 'match_pct': progress.get(o.skill_id, 0)} for o in opps]
    rows.sort(key=lambda r: -r['match_pct'])
    return rows[:limit], len(opps)


def _get_visible(gig_id, user):
    gig = Gig.query.get_or_404(gig_id)
    if not core.can_view(gig, user):
        abort(404)
    return gig


@opportunities_bp.route('/opportunities/gigs')
@login_required
def gigs():
    user = _current_user()
    nv_rows, nv_total = _nelavista_gig_rows(user)
    try:
        feed = core.build_feed(user, request.args)
        shown = {g.id for key in ('results', 'unknown', 'open_gigs', 'new', 'closing_soon', 'recommended') for g in feed[key]}
        state = core.user_state(user, shown)
        unavailable = False
    except SQLAlchemyError:
        # The gig tables not existing yet (migration not run) must not break the space.
        logger.exception('Gig feed unavailable')
        db.session.rollback()
        feed = {'filters': core.parse_filters({}), 'filtering': False, 'sort': 'best', 'results': [], 'unknown': [],
                'total_open': 0, 'statuses': {}, 'matches': {}, 'open_gigs': [], 'new': [], 'closing_soon': [],
                'recommended': [], 'user_skills': [], 'has_skill_data': False}
        state, unavailable = {}, True

    def filter_url(**overrides):
        params = {k: v for k, v in feed['filters'].items() if v}
        if feed['sort'] != 'best':
            params['sort'] = feed['sort']
        params.update(overrides)
        return url_for('opportunities.gigs', **{k: v for k, v in params.items() if v})

    return render_template(
        'opportunities_gigs_hub.html', feed=feed, state=state, ui=core.ui_helpers(), active_page='gigs',
        filter_url=filter_url, categories=core.CATEGORIES, location_types=core.LOCATION_TYPES,
        deadline_filters=core.DEADLINE_FILTERS, posted_filters=core.POSTED_FILTERS, sorts=core.SORTS,
        nv_rows=nv_rows, nv_total=nv_total, unavailable=unavailable,
    )


@opportunities_bp.route('/opportunities/gigs/<slug>')
@login_required
def gig_detail(slug):
    user = _current_user()
    gig = Gig.query.filter_by(slug=slug).first_or_404()
    if not core.can_view(gig, user):
        abort(404)
    viewed = session.get('gig_viewed', [])
    if gig.id not in viewed and gig.is_published:
        core.log_event(gig, user, core.EVENT_VIEWED, channel=(request.args.get('from') or '')[:30] or None)
        db.session.commit()
        session['gig_viewed'] = (viewed + [gig.id])[-60:]
    state = core.user_state(user, [gig.id]).get(gig.id, {'saved': False, 'applied_at': None})
    related = core.related_gigs(gig)
    return render_template(
        'opportunities_gig_detail.html', gig=gig, status=core.compute_status(gig), state=state, ui=core.ui_helpers(),
        match=core.skill_match(gig, core.user_skill_names(user)), related=related,
        related_state=core.user_state(user, [g.id for g in related]),
        share_url=url_for('opportunities.gig_detail', slug=gig.slug, _external=True), active_page='gigs',
    )


@opportunities_bp.route('/opportunities/gigs/<slug>/apply')
@login_required
def gig_apply(slug):
    """Logs the Apply click, then shows the official listing in the Nelavista frame (only
    when an admin enabled it after a framing check) or hands off to the official URL.
    Nelavista never alters or proxies the provider's page."""
    user = _current_user()
    gig = Gig.query.filter_by(slug=slug).first_or_404()
    if not core.can_view(gig, user):
        abort(404)
    if not gig.application_url:
        flash('This gig has no application link.')
        return redirect(url_for('opportunities.gig_detail', slug=gig.slug))
    in_app = gig.allows_in_app_view and not request.args.get('go')
    if gig.is_published:
        core.log_event(gig, user, core.EVENT_APPLY_CLICKED, channel='in_app' if in_app else 'external')
        db.session.commit()
    if in_app:
        state = core.user_state(user, [gig.id]).get(gig.id, {'saved': False, 'applied_at': None})
        return render_template('opportunities_gig_apply.html', gig=gig, state=state, ui=core.ui_helpers())
    return redirect(gig.application_url)


@opportunities_bp.route('/opportunities/gigs/<int:gig_id>/save', methods=['POST'])
@login_required
def gig_save(gig_id):
    user = _current_user()
    gig = _get_visible(gig_id, user)
    data = request.get_json(silent=True) or request.form
    if 'saved' in data:
        saved = str(data.get('saved')).lower() in ('1', 'true', 'yes', 'on')
    else:
        saved = not core.user_state(user, [gig.id]).get(gig.id, {}).get('saved', False)
    core.set_saved(gig, user, saved)
    db.session.commit()
    if _wants_json():
        return jsonify({'success': True, 'saved': saved})
    flash('Saved to My Opportunities.' if saved else 'Removed from saved.')
    return redirect(request.referrer or url_for('opportunities.gig_detail', slug=gig.slug))


@opportunities_bp.route('/opportunities/gigs/<int:gig_id>/applied', methods=['POST'])
@login_required
def gig_applied(gig_id):
    user = _current_user()
    gig = _get_visible(gig_id, user)
    data = request.get_json(silent=True) or request.form
    applied = str(data.get('applied', '1')).lower() in ('1', 'true', 'yes', 'on')
    record = core.set_applied(gig, user, applied)
    db.session.commit()
    at = record.applied_at if record else None
    if _wants_json():
        return jsonify({'success': True, 'applied': applied,
                        'applied_label': (f"Applied {at.strftime('%b')} {at.day}, {at.year}" if at else None)})
    flash('Added to My Opportunities → Applied. Good luck!' if applied else 'Removed from your applications.')
    return redirect(request.referrer or url_for('opportunities.gig_detail', slug=gig.slug))


@opportunities_bp.route('/opportunities/gigs/<int:gig_id>/share', methods=['POST'])
@login_required
@limiter.limit('60 per hour')
def gig_share(gig_id):
    user = _current_user()
    gig = _get_visible(gig_id, user)
    data = request.get_json(silent=True) or {}
    channel = data.get('channel') if data.get('channel') in ('native', 'whatsapp', 'copy', 'x', 'telegram') else 'other'
    core.log_event(gig, user, core.EVENT_SHARED, channel=channel)
    db.session.commit()
    return jsonify({'success': True})
