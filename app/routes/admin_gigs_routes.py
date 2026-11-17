"""Admin: gigs and gig providers. Registered on admin_skills_bp (imported at the bottom of
routes/admin_skills_routes.py).

/admin/gigs                     gig list: search, filter by provider/state, metrics
/admin/gigs/new                 add a gig by hand (same Gig model, provider 'manual')
/admin/gigs/<id>/edit           edit metadata (locks edited fields against sync)
/admin/gigs/<id>/action         publish, unpublish, verify, override status, feature,
                                archive, mark-not-duplicate
/admin/gigs/<id>/delete         remove a bad gig (archived instead if students saved it)
/admin/gigs/providers           providers: status, last sync, active gigs, errors
/admin/gigs/providers/<id>      edit a provider (enable only with confirmed terms)
/admin/gigs/providers/<id>/sync "Sync now"

The paid-gig ledger (Nelavista's own gigs with payouts) stays at /admin/skills/opportunities.
"""
import json
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, session

from app.extensions import db
from app.models import User, Gig, GigProvider, GigSyncRun
from app.routes.admin_skills_routes import admin_skills_bp
from app.utils.helpers import login_required, admin_required
from app.utils.validation import safe_external_url
from app.services.gigs import core, sync
from app.services.gigs.adapters import ADAPTERS


def _admin():
    return User.query.filter_by(username=session['user']['username']).first()


def _bucket(gig, status):
    if gig.is_archived:
        return 'archived'
    if gig.duplicate_of_id:
        return 'duplicates'
    if not gig.is_published:
        return 'drafts'
    if status['accepting']:
        return 'live'
    if status['key'] == 'UNKNOWN':
        return 'unknown'
    return 'closed'


@admin_skills_bp.route('/admin/gigs')
@login_required
@admin_required
def admin_gigs():
    sync.ensure_default_providers()
    view = request.args.get('view', 'all')
    q = (request.args.get('q') or '').strip().lower()
    provider_id = request.args.get('provider', type=int)
    now = datetime.utcnow()
    providers = GigProvider.query.order_by(GigProvider.name).all()
    query = Gig.query
    if provider_id:
        query = query.filter_by(provider_id=provider_id)
    counts = {k: 0 for k in ('all', 'live', 'unknown', 'drafts', 'closed', 'duplicates', 'archived')}
    rows = []
    for g in query.order_by(Gig.updated_at.desc()).limit(2000).all():
        st = core.compute_status(g, now)
        b = _bucket(g, st)
        counts[b] += 1
        if b != 'archived':
            counts['all'] += 1
        if view == 'all' and b == 'archived':
            continue
        if view != 'all' and b != view:
            continue
        if q and q not in f'{g.title} {g.organization} {g.source_gig_id or ""}'.lower():
            continue
        rows.append({'g': g, 'status': st, 'bucket': b})
    rows = rows[:300]
    stats = core.gig_stats([r['g'].id for r in rows])
    return render_template('admin_gigs.html', rows=rows, counts=counts, view=view, q=q, providers=providers,
                           provider_id=provider_id, stats=stats, metrics=core.dashboard_metrics(),
                           errors=sync.recent_errors(5), labels=core.CATEGORY_LABELS, ui=core.ui_helpers(),
                           active_page='gigs_feed')


def _form_context(gig, errors=None):
    return dict(
        gig=gig, errors=errors or [], categories=core.CATEGORIES, pay_types=core.PAY_TYPES, work_types=core.WORK_TYPES,
        location_types=core.LOCATION_TYPES, status=core.compute_status(gig) if gig.title else None,
        publish_problems=core.publish_problems(gig) if gig.id else [],
        stats=(core.gig_stats([gig.id]).get(gig.id, {}) if gig.id else {}), ui=core.ui_helpers(),
        raw_pretty=_pretty(gig.raw_json), active_page='gigs_feed',
    )


def _pretty(raw):
    if not raw:
        return None
    try:
        return json.dumps(json.loads(raw), indent=2)[:4000]
    except (TypeError, ValueError):
        return raw[:4000]


@admin_skills_bp.route('/admin/gigs/new', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_gig_new():
    provider = sync.manual_provider()
    gig = Gig(provider_id=provider.id, origin='manual', currency='NGN', pay_type='fixed', location_type='remote',
              application_mode='EXTERNAL', source_status='UNKNOWN', is_published=False, featured=False,
              is_archived=False, allows_in_app_view=False)
    # Not gig.provider = provider: that would cascade the unsaved gig into the session.
    if request.method == 'POST':
        errors = core.apply_form(gig, request.form)
        if errors:
            html = render_template('admin_gig_edit.html', **_form_context(gig, errors))
            db.session.rollback()
            return html, 400
        admin = _admin()
        gig.created_by_id = admin.id
        gig.dedupe_key = core.dedupe_key_for(gig.title, gig.organization)
        db.session.add(gig)
        db.session.flush()
        dup = sync.find_duplicate(gig)
        if request.form.get('verified_now'):
            core.admin_action(gig, 'verify', admin)
        db.session.commit()
        flash('Saved as a draft.' + (f' Heads up: it looks like a duplicate of "{dup.title}" (#{dup.id}).' if dup else '')
              + ' Verify it is open, then publish.')
        return redirect(url_for('admin_skills.admin_gig_edit', gig_id=gig.id))
    return render_template('admin_gig_edit.html', **_form_context(gig))


@admin_skills_bp.route('/admin/gigs/<int:gig_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_gig_edit(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    if request.method == 'POST':
        was_published = gig.is_published
        errors = core.apply_form(gig, request.form)
        if errors:
            html = render_template('admin_gig_edit.html', **_form_context(gig, errors))
            db.session.rollback()
            return html, 400
        gig.dedupe_key = core.dedupe_key_for(gig.title, gig.organization)
        db.session.commit()
        flash('Saved, and unpublished: it no longer passes the publish checks.' if was_published and not gig.is_published
              else 'Saved.' + (' Edited fields are locked so the next sync keeps your changes.' if gig.is_external else ''))
        return redirect(url_for('admin_skills.admin_gig_edit', gig_id=gig.id))
    return render_template('admin_gig_edit.html', **_form_context(gig))


@admin_skills_bp.route('/admin/gigs/<int:gig_id>/action', methods=['POST'])
@login_required
@admin_required
def admin_gig_action(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    ok, message = core.admin_action(gig, request.form.get('action', ''), _admin(), value=request.form.get('value'))
    if ok:
        db.session.commit()
    else:
        db.session.rollback()
    flash(message)
    return redirect(request.form.get('next') or url_for('admin_skills.admin_gig_edit', gig_id=gig.id))


@admin_skills_bp.route('/admin/gigs/<int:gig_id>/check-framing', methods=['POST'])
@login_required
@admin_required
def admin_gig_check_framing(gig_id):
    from app.services.student_opportunity_service import check_framing
    gig = Gig.query.get_or_404(gig_id)
    result = check_framing(gig.application_url)
    if result:
        flash("The site doesn't block framing. You can tick \"Show in-app\" and save. Test it yourself first.")
    else:
        gig.allows_in_app_view = False
        db.session.commit()
        flash("The site blocks framing (or couldn't be reached). Students open it in a new tab / in-app browser.")
    return redirect(url_for('admin_skills.admin_gig_edit', gig_id=gig.id))


@admin_skills_bp.route('/admin/gigs/<int:gig_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_gig_delete(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    reason = (request.form.get('reason') or 'Removed by an admin').strip()[:200]
    if gig.saves.first() or gig.applications.first() or gig.is_external:
        # Keep students' history, and keep external gigs as archived tombstones so the
        # next sync doesn't re-import a gig an admin removed.
        gig.is_archived = True
        gig.is_published = False
        gig.removed_reason = reason
        locked = gig.locked_fields | {'is_archived'}
        gig.locked_fields_json = json.dumps(sorted(locked))
        db.session.commit()
        flash('Removed from students and archived (kept so it is not re-imported, and so saved/applied history stays).')
        return redirect(url_for('admin_skills.admin_gigs'))
    db.session.delete(gig)
    db.session.commit()
    flash('Deleted.')
    return redirect(url_for('admin_skills.admin_gigs'))


# ---------------------------------------------------------------- providers

@admin_skills_bp.route('/admin/gigs/providers')
@login_required
@admin_required
def admin_gig_providers():
    sync.ensure_default_providers()
    now = datetime.utcnow()
    providers = GigProvider.query.order_by(GigProvider.id).all()
    active = {}
    for g in core.visible_query().all():
        if core.is_active(g, now):
            active[g.provider_id] = active.get(g.provider_id, 0) + 1
    totals = dict(db.session.query(Gig.provider_id, db.func.count(Gig.id)).group_by(Gig.provider_id).all())
    runs = GigSyncRun.query.order_by(GigSyncRun.started_at.desc()).limit(30).all()
    return render_template('admin_gig_providers.html', providers=providers, active=active, totals=totals, runs=runs,
                           adapters=ADAPTERS, problems={p.id: sync.provider_problems(p) for p in providers},
                           due={p.id: sync.is_due(p, now) for p in providers}, ui=core.ui_helpers(),
                           active_page='gigs_feed')


@admin_skills_bp.route('/admin/gigs/providers/new', methods=['GET', 'POST'])
@admin_skills_bp.route('/admin/gigs/providers/<int:provider_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_gig_provider_edit(provider_id=None):
    provider = GigProvider.query.get_or_404(provider_id) if provider_id else GigProvider(
        kind='api', adapter='json_feed', auth_method='none', enabled=False, redistribution_confirmed=False,
        auto_publish=False, sync_frequency_minutes=360, stale_after_hours=72, consecutive_failures=0)
    errors = []
    if request.method == 'POST':
        f = request.form
        if not provider.id:
            slug = core.slugify(f.get('slug') or f.get('name') or '')[:60]
            if GigProvider.query.filter_by(slug=slug).first():
                errors.append('That slug is taken.')
            provider.slug = slug
        provider.name = (f.get('name') or '').strip()[:120]
        if not provider.name:
            errors.append('Name is required.')
        if provider.slug != 'manual':
            adapter = f.get('adapter')
            provider.adapter = adapter if adapter in ADAPTERS and adapter != 'manual' else provider.adapter
            provider.kind = f.get('kind') if f.get('kind') in ('api', 'feed', 'partner') else 'api'
        for field in ('api_base_url', 'website_url', 'terms_url'):
            raw = (f.get(field) or '').strip()
            clean = safe_external_url(raw)
            if raw and not clean:
                errors.append(f'{field.replace("_", " ")} must be a full http(s) link.')
            setattr(provider, field, clean)
        provider.auth_method = f.get('auth_method') if f.get('auth_method') in ('none', 'api_key_header', 'bearer', 'query_param') else 'none'
        provider.auth_param = (f.get('auth_param') or '').strip()[:60] or None
        env_name = (f.get('credentials_env') or '').strip()[:80]
        if env_name and not env_name.replace('_', '').isalnum():
            errors.append('Credentials env var must be an environment variable NAME (letters, digits, _), not the key itself.')
        provider.credentials_env = env_name or None
        raw_config = (f.get('config_json') or '').strip()
        if raw_config:
            try:
                parsed = json.loads(raw_config)
                if not isinstance(parsed, dict):
                    raise ValueError
                provider.config_json = json.dumps(parsed)
            except ValueError:
                errors.append('Adapter config must be a JSON object.')
        else:
            provider.config_json = None
        provider.redistribution_basis = (f.get('redistribution_basis') or '').strip() or None
        provider.redistribution_confirmed = bool(f.get('redistribution_confirmed'))
        provider.attribution_text = (f.get('attribution_text') or '').strip()[:200] or None
        provider.auto_publish = bool(f.get('auto_publish'))
        try:
            provider.sync_frequency_minutes = max(0, int(f.get('sync_frequency_minutes') or 360))
            provider.stale_after_hours = max(1, int(f.get('stale_after_hours') or 72))
        except ValueError:
            errors.append('Sync frequency and stale threshold must be whole numbers.')
        floor = ADAPTERS[provider.adapter].min_interval_minutes if provider.adapter in ADAPTERS else 60
        if provider.adapter != 'manual' and provider.sync_frequency_minutes < floor:
            provider.sync_frequency_minutes = floor
            flash(f"Sync frequency raised to {floor} minutes: this adapter's terms don't allow polling more often.")
        want_enabled = bool(f.get('enabled'))
        if want_enabled:
            problems = sync.provider_problems(provider)
            if problems:
                errors.extend(['Not enabled: ' + p for p in problems])
                want_enabled = False
        was_enabled = provider.enabled
        provider.enabled = want_enabled
        if errors:
            html = render_template('admin_gig_provider_edit.html', provider=provider, errors=errors, adapters=ADAPTERS,
                                   active_page='gigs_feed')
            db.session.rollback()
            return html, 400
        if not provider.id:
            db.session.add(provider)
        db.session.commit()
        if was_enabled and not provider.enabled:
            flash('Saved. Provider disabled: its gigs are hidden from students until it is enabled again.')
        else:
            flash('Saved.')
        return redirect(url_for('admin_skills.admin_gig_providers'))
    return render_template('admin_gig_provider_edit.html', provider=provider, errors=errors, adapters=ADAPTERS,
                           active_page='gigs_feed')


@admin_skills_bp.route('/admin/gigs/providers/<int:provider_id>/sync', methods=['POST'])
@login_required
@admin_required
def admin_gig_provider_sync(provider_id):
    provider = GigProvider.query.get_or_404(provider_id)
    if not provider.enabled:
        flash('Enable the provider first (its terms must be confirmed).')
        return redirect(url_for('admin_skills.admin_gig_providers'))
    cls = ADAPTERS.get(provider.adapter)
    if provider.last_sync_at and cls and (datetime.utcnow() - provider.last_sync_at).total_seconds() < cls.min_interval_minutes * 60 \
            and not request.form.get('confirm_terms_floor'):
        flash(f"Last sync was under {cls.min_interval_minutes} minutes ago, the most often this provider's terms allow. Try later.")
        return redirect(url_for('admin_skills.admin_gig_providers'))
    run = sync.sync_provider(provider, triggered_by=f'admin:{_admin().username}'[:60])
    if run is None:
        flash('This provider has nothing to sync.')
    elif run.status == 'failed':
        flash(f'Sync failed: {run.error}. Existing gigs were kept unchanged.')
    else:
        flash(f'Synced: {run.fetched} fetched, {run.created} new, {run.updated} updated, {run.closed} closed, '
              f'{run.skipped} skipped, {run.duplicates} duplicates, {run.errors} errors.')
    return redirect(url_for('admin_skills.admin_gig_providers'))
