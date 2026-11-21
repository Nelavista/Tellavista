"""Background synchronisation of external gig providers.

For each enabled provider that is due: fetch, normalise, create new gigs, update
existing ones, detect closed ones, record the run, and log failures. Rules:

- A failed fetch changes no gig. The last good data stays, the error is recorded on the
  provider and the run, and the provider backs off. Gigs it can no longer confirm drop
  to "Availability unknown" on their own once they pass the provider's stale window
  (core.compute_status), so nothing is deleted and nothing is falsely shown as open.
- A provider that suddenly returns zero gigs is treated as suspect: nothing is closed.
- Absence from a fetch closes a gig only when the adapter says its feed is complete.
  Otherwise the adapter's get_status() decides, and 'UNKNOWN' never closes anything.
- Admin-edited fields (Gig.locked_fields) are never overwritten by a sync.

Runs from three places: the in-process scheduler (GIG_SYNC_ENABLED=1), the CLI
(`flask --app wsgi gigs-sync`, e.g. from a Render cron job), and the admin "Sync now"
button.
"""
import json
import logging
import os
from datetime import datetime, timedelta

from app.extensions import db
from app.models import Gig, GigProvider, GigSyncRun
from app.services.gigs import core
from app.services.gigs.adapters import get_adapter, ProviderError, trim_raw, ADAPTERS

logger = logging.getLogger('nelavista.gigs.sync')

SCHEDULER_TICK_SECONDS = 600
MAX_BACKOFF_MINUTES = 24 * 60
SYNC_FIELDS = ['title', 'organization', 'organization_logo_url', 'summary', 'description', 'requirements',
               'eligibility', 'category', 'skills_json', 'pay_min', 'pay_max', 'currency', 'pay_type', 'pay_text',
               'work_type', 'location_type', 'location', 'application_url', 'source_url', 'posted_at', 'deadline',
               'external_reference']


# ---------------------------------------------------------------- providers

JOBICY_BASIS = (
    "Jobicy's public API documentation has a Fair Use section: listings may be used in your own products "
    "without individual permission, data may be stored, cached and redistributed, as long as Jobicy is clearly "
    "credited as the source and the canonical Jobicy job URL is kept. Automated polling no more than once per "
    "hour. Re-read the terms before enabling: https://jobicy.com/jobs-rss-feed"
)


NAIJALANCERS_BASIS = (
    "Naijalancers is a Nelavista partner. Gigs are added by Nelavista admins only after checking the listing "
    "with Naijalancers, and every gig keeps its Naijalancers attribution and official listing URL. No page is "
    "scraped; there is no sync until Naijalancers provides an official API or feed."
)


def ensure_default_providers():
    """Creates the built-in providers if missing. 'manual' (Nelavista) and 'naijalancers'
    are enabled manual sources. 'jobicy' is created DISABLED: an admin must read the
    terms, confirm, then enable."""
    created = []
    if not GigProvider.query.filter_by(slug='manual').first():
        db.session.add(GigProvider(
            slug='manual', name='Nelavista', kind='manual', adapter='manual', enabled=True,
            redistribution_confirmed=True, attribution_text='Nelavista',
            redistribution_basis='Gigs added by Nelavista admins after checking them directly.',
            sync_frequency_minutes=0, stale_after_hours=core.MANUAL_RECHECK_DAYS * 24,
        ))
        created.append('manual')
    if not GigProvider.query.filter_by(slug='jobicy').first():
        db.session.add(GigProvider(
            slug='jobicy', name='Jobicy', kind='api', adapter='jobicy', api_base_url='https://jobicy.com/api/jobs',
            website_url='https://jobicy.com', terms_url='https://jobicy.com/jobs-rss-feed',
            redistribution_basis=JOBICY_BASIS, redistribution_confirmed=False, attribution_text='Jobicy',
            enabled=False, auto_publish=False, sync_frequency_minutes=180, stale_after_hours=72,
            config_json=json.dumps({'count': 100, 'nigeria_eligible_only': True}),
        ))
        created.append('jobicy')
    if not GigProvider.query.filter_by(slug='naijalancers').first():
        db.session.add(GigProvider(
            slug='naijalancers', name='Naijalancers', kind='partner', adapter='manual', enabled=True,
            redistribution_confirmed=True, attribution_text='Naijalancers',
            redistribution_basis=NAIJALANCERS_BASIS,
            sync_frequency_minutes=0, stale_after_hours=core.MANUAL_RECHECK_DAYS * 24,
        ))
        created.append('naijalancers')
    if created:
        db.session.commit()
    return created


def manual_provider():
    p = GigProvider.query.filter_by(slug='manual').first()
    if not p:
        ensure_default_providers()
        p = GigProvider.query.filter_by(slug='manual').first()
    return p


def provider_problems(provider):
    """Why this provider can't be enabled (empty = it can)."""
    problems = []
    if provider.adapter not in ADAPTERS:
        problems.append('Pick an adapter.')
    if provider.adapter != 'manual':
        if not provider.redistribution_confirmed:
            problems.append("Confirm that the provider's terms permit showing their listings in Nelavista.")
        if not (provider.redistribution_basis or '').strip():
            problems.append('Record the terms basis (what the terms say and where).')
        if not provider.terms_url:
            problems.append('Add the terms / API documentation URL.')
        if not provider.api_base_url and provider.adapter != 'jobicy':
            problems.append('Add the API / feed URL.')
        if not provider.attribution_text:
            problems.append('Add the attribution students will see (e.g. "Jobicy").')
    return problems


def effective_interval(provider):
    adapter_cls = ADAPTERS.get(provider.adapter)
    floor = adapter_cls.min_interval_minutes if adapter_cls else 60
    minutes = max(provider.sync_frequency_minutes or 0, floor)
    if provider.consecutive_failures:
        minutes = min(minutes * (2 ** min(provider.consecutive_failures - 1, 6)), MAX_BACKOFF_MINUTES)
    return timedelta(minutes=minutes)


def is_due(provider, now=None):
    now = now or datetime.utcnow()
    cls = ADAPTERS.get(provider.adapter)
    if not provider.enabled or not provider.redistribution_confirmed or not cls or not cls.syncable:
        return False
    return provider.last_sync_at is None or now - provider.last_sync_at >= effective_interval(provider)


# ---------------------------------------------------------------- upsert & dedupe

def find_duplicate(gig):
    """Another live gig that is the same job: same title + organisation, or the same
    application URL. The first one Nelavista saw stays; later copies hide behind it."""
    canon = core.canonical_url(gig.application_url)
    q = Gig.query.filter(Gig.is_archived.is_(False), Gig.duplicate_of_id.is_(None))
    if gig.id:
        q = q.filter(Gig.id != gig.id)
    if gig.dedupe_key:
        hit = q.filter(Gig.dedupe_key == gig.dedupe_key).order_by(Gig.id).first()
        if hit:
            return hit
    if canon:
        host = canon.split('/')[2] if '//' in canon else ''
        for cand in q.filter(Gig.application_url.ilike(f'%{host.split(":")[0]}%')).limit(200).all():
            if core.canonical_url(cand.application_url) == canon:
                return cand
    return None


def upsert_gig(provider, ng, now, adapter=None):
    """Creates or updates one gig from a NormalizedGig. Returns 'created', 'updated' or
    'duplicate'. Caller commits."""
    gig = Gig.query.filter_by(provider_id=provider.id, source_gig_id=ng.source_gig_id).first()
    fields = ng.as_fields()
    fields['category'] = fields.get('category') if fields.get('category') in core.CATEGORY_KEYS else 'other'
    fields['pay_type'] = fields.get('pay_type') if fields.get('pay_type') in core.PAY_TYPE_KEYS else 'not_stated'
    fields['location_type'] = fields.get('location_type') if fields.get('location_type') in core.LOCATION_TYPE_KEYS else 'remote'
    created = gig is None
    if created:
        gig = Gig(provider_id=provider.id, source_gig_id=ng.source_gig_id, origin='external', created_at=now,
                  is_published=False, featured=False, is_archived=False, allows_in_app_view=False,
                  application_mode='EXTERNAL', source_status='UNKNOWN')
        # provider_id only: assigning gig.provider would cascade the half-built row into
        # the session and autoflush it (without a slug) on the next query.
        locked = set()
    else:
        locked = gig.locked_fields
    for name in SYNC_FIELDS:
        if name in fields and name not in locked:
            setattr(gig, name, fields[name])
    gig.raw_json = trim_raw(ng.raw) if ng.raw is not None else gig.raw_json
    gig.last_seen_at = now
    gig.last_synced_at = now
    _apply_source_status(gig, ng.status, now)
    gig.dedupe_key = core.dedupe_key_for(gig.title, gig.organization)

    result = 'created' if created else 'updated'
    if created:
        gig.slug = core.unique_slug(core.slugify(f'{gig.title} {gig.organization}'))
        db.session.add(gig)
        db.session.flush()
    if 'duplicate_of_id' not in locked and (created or gig.duplicate_of_id is None):
        dup = find_duplicate(gig)
        if dup and dup.id < gig.id:
            gig.duplicate_of_id = dup.id
            gig.is_published = False
            result = 'duplicate'
    if created and result == 'created' and provider.auto_publish and not core.publish_problems(gig, now):
        gig.is_published = True
        gig.published_at = now
    return result


def _apply_source_status(gig, status, now):
    status = status if status in core.SOURCE_STATUSES else 'UNKNOWN'
    gig.source_status = status
    if status == 'OPEN':
        gig.last_verified_at = now
        gig.closed_at = None
    elif status == 'CLOSED':
        gig.closed_at = gig.closed_at or now


# ---------------------------------------------------------------- one provider

def sync_provider(provider, triggered_by='schedule', now=None, http=None):
    """Synchronises one provider. Always returns the GigSyncRun (or None when the
    provider isn't syncable). Never raises for provider-side problems."""
    now = now or datetime.utcnow()
    cls = ADAPTERS.get(provider.adapter)
    if not cls or not cls.syncable:
        return None
    run = GigSyncRun(provider_id=provider.id, started_at=now, status='running', triggered_by=(triggered_by or '')[:60])
    db.session.add(run)
    if not provider.enabled or not provider.redistribution_confirmed:
        run.status = 'failed'
        run.error = 'Provider is disabled or its redistribution terms are not confirmed.'
        run.finished_at = datetime.utcnow()
        db.session.commit()
        return run
    db.session.flush()

    try:
        adapter = get_adapter(provider, http=http)
        raws = adapter.fetch_gigs()
    except Exception as e:  # ProviderError or anything unexpected: keep all data, record it
        msg = str(e) if isinstance(e, ProviderError) else f'{e.__class__.__name__}: {e}'
        logger.warning('Gig sync failed for %s: %s', provider.slug, msg)
        run.status = 'failed'
        run.error = msg[:2000]
        run.finished_at = datetime.utcnow()
        provider.last_sync_at = now
        provider.last_status = 'failed'
        provider.last_error = msg[:2000]
        provider.consecutive_failures = (provider.consecutive_failures or 0) + 1
        db.session.commit()
        return run

    run.fetched = len(raws)
    seen = set()
    notes = []
    for raw in raws:
        try:
            ng = adapter.normalize_gig(raw)
        except Exception:
            logger.exception('normalize_gig failed for %s', provider.slug)
            run.errors += 1
            continue
        if ng is None or not ng.source_gig_id:
            run.skipped += 1
            continue
        if ng.source_gig_id in seen:
            run.duplicates += 1
            continue
        seen.add(ng.source_gig_id)
        try:
            with db.session.begin_nested():
                result = upsert_gig(provider, ng, now, adapter)
        except Exception:
            logger.exception('upsert failed for %s/%s', provider.slug, ng.source_gig_id)
            run.errors += 1
            continue
        if result == 'created':
            run.created += 1
        elif result == 'updated':
            run.updated += 1
        else:
            run.created += 1
            run.duplicates += 1

    # Gigs this provider had that weren't in this fetch.
    missing = (Gig.query.filter(Gig.provider_id == provider.id, Gig.is_archived.is_(False),
                                Gig.source_status != 'CLOSED')
               .filter(~Gig.source_gig_id.in_(list(seen) or ['__none__'])).all())
    if missing and not raws:
        notes.append(f'Provider returned no gigs. Kept {len(missing)} existing gig(s) unchanged.')
    elif missing and adapter.absence_means_closed:
        for gig in missing:
            _apply_source_status(gig, 'CLOSED', now)
            gig.last_synced_at = now
            run.closed += 1
    elif missing:
        try:
            statuses = adapter.get_status([g.source_gig_id for g in missing])
        except Exception as e:
            statuses = {}
            notes.append(f'Status check failed: {e.__class__.__name__}')
        for gig in missing:
            st = statuses.get(gig.source_gig_id, 'UNKNOWN')
            gig.last_synced_at = now
            if st == 'CLOSED':
                _apply_source_status(gig, 'CLOSED', now)
                run.closed += 1
            elif st == 'OPEN':
                _apply_source_status(gig, 'OPEN', now)
            # UNKNOWN: leave it. It ages into "Availability unknown" by itself.

    run.status = 'partial' if run.errors else 'success'
    run.notes = ' '.join(notes)[:2000] or None
    run.finished_at = datetime.utcnow()
    provider.last_sync_at = now
    provider.last_success_at = now
    provider.last_status = run.status
    provider.last_error = None if not run.errors else f'{run.errors} item(s) failed to import.'
    provider.consecutive_failures = 0
    db.session.commit()
    logger.info('Gig sync %s: fetched=%s created=%s updated=%s closed=%s skipped=%s dup=%s errors=%s',
                provider.slug, run.fetched, run.created, run.updated, run.closed, run.skipped, run.duplicates, run.errors)
    return run


def sync_due_providers(now=None, triggered_by='schedule', http=None, force=False):
    """Syncs every provider that is due. One provider failing never stops the others."""
    now = now or datetime.utcnow()
    runs = []
    for provider in GigProvider.query.order_by(GigProvider.id).all():
        if not (force and provider.enabled and provider.redistribution_confirmed) and not is_due(provider, now):
            continue
        try:
            run = sync_provider(provider, triggered_by=triggered_by, now=now, http=http)
            if run:
                runs.append(run)
        except Exception:
            logger.exception('Unexpected error syncing provider %s', provider.slug)
            db.session.rollback()
    return runs


def recent_errors(limit=20):
    return (GigSyncRun.query.filter(GigSyncRun.status.in_(['failed', 'partial']))
            .order_by(GigSyncRun.started_at.desc()).limit(limit).all())


# ---------------------------------------------------------------- scheduler & CLI

_scheduler_started = False


def start_scheduler(app):
    """Opt-in in-process loop (GIG_SYNC_ENABLED=1). Uses socketio's background task so it
    cooperates with the eventlet worker the app already runs under. Checks every 10
    minutes which providers are due; each provider's own frequency (and its terms'
    minimum interval) decides whether it is actually called."""
    global _scheduler_started
    if _scheduler_started or os.environ.get('GIG_SYNC_ENABLED') != '1' or app.config.get('TESTING'):
        return False
    from app.extensions import socketio
    _scheduler_started = True

    def loop():
        socketio.sleep(90)
        while True:
            with app.app_context():
                try:
                    sync_due_providers(triggered_by='schedule')
                except Exception:
                    logger.exception('Gig scheduler tick failed')
                    db.session.rollback()
                finally:
                    db.session.remove()
            socketio.sleep(SCHEDULER_TICK_SECONDS)

    socketio.start_background_task(loop)
    logger.info('Gig sync scheduler started (tick every %ss).', SCHEDULER_TICK_SECONDS)
    return True


def register_cli(app):
    import click

    @app.cli.command('gigs-sync')
    @click.option('--provider', 'slug', default=None, help='Only this provider slug.')
    @click.option('--force', is_flag=True, help='Ignore the schedule (terms floors still apply to the scheduler).')
    def gigs_sync(slug, force):
        """Synchronise external gig providers."""
        ensure_default_providers()
        if slug:
            provider = GigProvider.query.filter_by(slug=slug).first()
            if not provider:
                raise click.ClickException(f'No provider {slug!r}.')
            runs = [r for r in [sync_provider(provider, triggered_by='cli')] if r]
        else:
            runs = sync_due_providers(triggered_by='cli', force=force)
        if not runs:
            click.echo('Nothing to sync (no enabled provider is due).')
        for r in runs:
            click.echo(f'{r.provider.slug}: {r.status} fetched={r.fetched} created={r.created} updated={r.updated} '
                       f'closed={r.closed} skipped={r.skipped} duplicates={r.duplicates} errors={r.errors}'
                       + (f' error={r.error}' if r.error else ''))

    @app.cli.command('gigs-seed-providers')
    def gigs_seed_providers():
        """Create the built-in providers (manual; Jobicy, disabled)."""
        click.echo(f'Created: {", ".join(ensure_default_providers()) or "nothing (already there)"}')
