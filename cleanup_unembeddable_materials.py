"""Audits Material rows with an external_url (oer_library / google_auto / openstax --
uploaded/static materials use Cloudinary or same-origin /static/ URLs and are skipped,
matching the precedent set in commit 711f0cc) against their REAL X-Frame-Options / CSP
frame-ancestors response headers -- the actual browser-enforced mechanism behind
"This content is blocked. Contact the site owner to fix the issue." -- and deletes the
ones that genuinely refuse to be framed by a different origin, or are unreachable.

Materials.html loads every material in an <iframe>, no exceptions (see that commit) --
so a material whose host blocks cross-origin framing is not a "sometimes works" material,
it's permanently broken for every student, every time. There's no partial credit for
being real-but-unembeddable; it has to come out.

Usage:
    python cleanup_unembeddable_materials.py [--dry-run]
"""
import sys
import time
import json
import os
# `from app import app` must come before `import requests` -- app.py's eventlet
# monkey-patch has to run before anything else touches ssl/socket, or requests'
# underlying urllib3/ssl machinery ends up in a corrupted, recursively-patched state
# (observed directly: every HTTPS request raised RecursionError in ssl.SSLContext
# .minimum_version once `import requests` ran first).
from app import app, db
import requests
from models import Material

DRY_RUN = '--dry-run' in sys.argv

# Persists confirmed-embeddable URLs across process restarts. The remote DB
# connection has proven to drop every 10-20 minutes (observed repeatedly), so this
# script is designed to be killed and re-run many times -- but without this cache,
# every restart re-verifies every already-confirmed-good material from scratch before
# ever reaching new ground, since "kept" materials are never deleted and the DB itself
# has nowhere to record "already checked". A local file survives across restarts
# even though nothing in Postgres does.
_CACHE_PATH = os.path.join(os.path.dirname(__file__), '.embeddable_cache.json')


def _load_verified_cache():
    try:
        with open(_CACHE_PATH, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except (FileNotFoundError, ValueError):
        return set()


def _save_verified_cache(verified_urls):
    with open(_CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(sorted(verified_urls), f)


def _fetch(url, timeout, retries=2):
    """A single failed connection attempt is not evidence a site is down -- transient
    network blips (seen directly: a whole run's tail turned into spurious
    ConnectionErrors on URLs that curl fetched fine seconds later) must not get
    confused with a real, deliberate X-Frame-Options/CSP block. Retries with backoff
    before giving up; only a response that actually came back gets judged.

    stream=True + immediate .close() is required, not cosmetic: only the response
    HEADERS are needed here, but a plain requests.get() downloads the full body before
    returning -- a large/slowly-served PDF (some of these external_urls are direct PDF
    links) can then block far longer than `timeout` suggests, since requests' timeout
    is a per-read timeout, not a total-request-time cap: a server trickling bytes
    slowly enough never trips it. Observed directly: a run hung with zero progress for
    20+ minutes on exactly this. Streaming and closing before any body read avoids
    downloading the body at all."""
    last_exc = None
    for attempt in range(retries):
        resp = None
        try:
            resp = requests.get(url, timeout=timeout, allow_redirects=True, stream=True,
                                 headers={'User-Agent': 'Mozilla/5.0 (compatible; NelavistaBot/1.0)'})
            resp.close()
            return resp
        except Exception as e:
            if resp is not None:
                resp.close()
            last_exc = e
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise last_exc


def is_embeddable(url, timeout=8):
    """Returns (embeddable: bool, reason: str). Mirrors the check from commit 711f0cc:
    X-Frame-Options DENY/SAMEORIGIN blocks cross-origin framing (our own SAMEORIGIN
    header on same-origin /static/ files is the one case that's NOT actually blocked --
    but those aren't checked here at all, see module docstring). A CSP frame-ancestors
    directive that doesn't allow our origin/'*' also blocks. No such headers -> allowed
    by default, matching real browser behavior."""
    try:
        resp = _fetch(url, timeout)
    except Exception as e:
        return False, f'unreachable after retries: {e.__class__.__name__}'

    if resp.status_code >= 400:
        return False, f'http {resp.status_code}'

    xfo = (resp.headers.get('X-Frame-Options') or '').strip().upper()
    if xfo in ('DENY', 'SAMEORIGIN'):
        return False, f'X-Frame-Options: {xfo}'

    csp = resp.headers.get('Content-Security-Policy') or ''
    for directive in csp.split(';'):
        directive = directive.strip()
        if directive.lower().startswith('frame-ancestors'):
            values = directive.split()[1:]
            if not any(v in ("'self'", '*') for v in values):
                return False, f'CSP frame-ancestors: {directive}'

    return True, 'ok'


def cleanup():
    verified_cache = _load_verified_cache()
    print(f"Loaded {len(verified_cache)} previously-verified-embeddable URLs from cache.")

    with app.app_context():
        materials = Material.query.filter(
            Material.source.in_(['oer_library', 'google_auto', 'openstax']),
            Material.external_url.isnot(None),
        ).all()
        print(f"Auditing {len(materials)} externally-hosted materials "
              f"({sum(1 for m in materials if m.external_url in verified_cache)} already cached as good)...")

        removed = kept = skipped_cached = 0
        consecutive_unreachable = 0
        for i, m in enumerate(materials):
            if m.external_url in verified_cache:
                skipped_cached += 1
                kept += 1
                continue

            embeddable, reason = is_embeddable(m.external_url)
            if embeddable:
                verified_cache.add(m.external_url)

            if reason.startswith('unreachable'):
                consecutive_unreachable += 1
                # A real, isolated dead link is one thing; 8 "unreachable" results in a
                # row -- across unrelated hosts that have no reason to all be down at
                # once -- is what a systemic network problem on OUR end looks like
                # (observed directly earlier). Stop rather than mass-delete good
                # materials because of a local blip.
                if consecutive_unreachable >= 8:
                    print(f"\nABORTING: {consecutive_unreachable} consecutive 'unreachable' results -- "
                          "this looks like a network problem on our end, not real link rot. "
                          "No further deletions this run; already-committed batches stand.")
                    if not DRY_RUN:
                        db.session.commit()
                    _save_verified_cache(verified_cache)
                    return
            else:
                consecutive_unreachable = 0

            if not embeddable:
                print(f"  REMOVE [{m.source}] {m.course_code} \"{m.title[:60]}\" -> {reason}")
                if not DRY_RUN:
                    db.session.delete(m)
                removed += 1
            else:
                kept += 1

            if not DRY_RUN and (i + 1) % 50 == 0:
                db.session.commit()  # commit in batches -- same rationale as the seed
                                      # scripts: a dropped remote-DB connection should
                                      # only cost this batch, not the whole audit.
                _save_verified_cache(verified_cache)  # save alongside the DB commit so a
                                                       # crash right after still keeps
                                                       # this batch's newly-verified URLs
                print(f"[{i+1}/{len(materials)}] removed={removed} kept={kept} "
                      f"(skipped via cache: {skipped_cached})")

            time.sleep(0.1)

        if not DRY_RUN:
            db.session.commit()
        _save_verified_cache(verified_cache)

        print(f"\nDONE. Removed: {removed}   Kept (verified embeddable): {kept}"
              + ("  [DRY RUN -- nothing actually deleted]" if DRY_RUN else ""))


if __name__ == '__main__':
    cleanup()
