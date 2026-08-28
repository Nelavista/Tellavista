"""Finds (and optionally deactivates) approved Material rows whose external URL
(OpenStax/web-search sourced -- source in 'openstax'/'google_auto') is actually dead --
a 404, a redirect to a generic "not found" page, or unreachable. Companion to
audit_broken_material_links.py, which only checks LOCAL static file paths; this checks
the external ones.

Found via a concrete production example: 69 approved materials pointing at the literal
string "https://openstax.org/general/cnx-404" -- OpenStax's own catch-all page for a
book/chapter URL that has since moved or been retired. Those are checked first (exact,
free, no network call needed) before doing live HTTP checks on the rest.

"A broken resource must never reach the student" -- these were showing on course pages
indistinguishable from real content.

Default is a DRY RUN: reports what it would deactivate, changes nothing. Pass --apply
to actually deactivate. Deactivated rows are NOT deleted -- same convention as
audit_broken_material_links.py -- they simply stop showing to students and can be
re-approved later if a URL turns out to be a transient failure.

Usage:
    python audit_broken_external_links.py             # report only
    python audit_broken_external_links.py --apply      # deactivate broken rows
    python audit_broken_external_links.py --apply --full-check   # also live-check
                                                                   # every remaining
                                                                   # external URL over
                                                                   # HTTP, not just the
                                                                   # known cnx-404 pattern
"""
import json
import subprocess
import sys

APPLY = '--apply' in sys.argv
FULL_CHECK = '--full-check' in sys.argv

KNOWN_DEAD_PATTERNS = ('/general/cnx-404',)

# The live-HTTP-check phase deliberately runs in a completely separate subprocess that
# never imports app.py -- app.py's own `import eventlet; eventlet.monkey_patch()` (its
# very first lines) conflicts with a plain blocking `requests` call made later in the
# same process on this stack (Python 3.13 + this eventlet version): a real
# `RecursionError` inside urllib3/ssl was hit running this in-process. A subprocess that
# only ever imports `requests` sidesteps eventlet's monkey-patching entirely.
_CHECKER_SCRIPT = r'''
import json, sys, requests
KNOWN_DEAD_PATTERNS = ("/general/cnx-404",)
def is_known_dead(url):
    return bool(url) and any(p in url for p in KNOWN_DEAD_PATTERNS)
urls = json.loads(sys.stdin.read())
dead = []
for item_id, url in urls:
    try:
        resp = requests.head(url, timeout=8, allow_redirects=True)
        if resp.status_code == 405:
            resp = requests.get(url, timeout=8, allow_redirects=True, stream=True)
        if resp.status_code == 404 or is_known_dead(resp.url):
            dead.append(item_id)
    except requests.RequestException:
        pass  # inconclusive -- never deactivate on a network failure alone
print(json.dumps(dead))
'''


def _is_known_dead(url):
    return bool(url) and any(p in url for p in KNOWN_DEAD_PATTERNS)


def _check_live_batch(id_url_pairs):
    """Runs the live HTTP liveness check for a batch of (id, url) pairs in a clean
    subprocess (see _CHECKER_SCRIPT above). Returns the set of ids found dead."""
    if not id_url_pairs:
        return set()
    result = subprocess.run(
        [sys.executable, '-c', _CHECKER_SCRIPT],
        input=json.dumps(id_url_pairs), capture_output=True, text=True, timeout=1800,
    )
    if result.returncode != 0:
        print(f"[WARN] link-check subprocess failed: {result.stderr[-500:]}")
        return set()
    try:
        return set(json.loads(result.stdout.strip().splitlines()[-1]))
    except (ValueError, IndexError):
        print(f"[WARN] couldn't parse link-check subprocess output: {result.stdout[-500:]}")
        return set()


def main():
    from app import app, db
    from models import Material

    with app.app_context():
        candidates = Material.query.filter(
            Material.is_approved.is_(True),
            Material.source.in_(['openstax', 'google_auto', 'oer_library']),
        ).all()

        known_dead = [m for m in candidates if _is_known_dead(m.external_url) or _is_known_dead(m.file_url)]
        print(f"Checked {len(candidates)} approved OpenStax/Open-Textbook-Library/web-search materials.")
        print(f"Found {len(known_dead)} pointing at the known-dead OpenStax cnx-404 pattern.")

        live_checked_dead = []
        remaining = [m for m in candidates if m not in known_dead]
        if FULL_CHECK:
            pairs = [(m.id, m.external_url or m.file_url) for m in remaining
                     if (m.external_url or m.file_url or '').startswith(('http://', 'https://'))]
            print(f"\n--full-check: live-checking {len(pairs)} URLs over HTTP in batches "
                  "(separate subprocess per batch, this will take a while)...")
            BATCH = 100
            dead_ids = set()
            for start in range(0, len(pairs), BATCH):
                batch = pairs[start:start + BATCH]
                dead_ids |= _check_live_batch(batch)
                print(f"  ...{min(start + BATCH, len(pairs))}/{len(pairs)} checked, {len(dead_ids)} dead so far")
            live_checked_dead = [m for m in remaining if m.id in dead_ids]
            print(f"Live HTTP check found {len(live_checked_dead)} more broken URLs.")

        all_broken = known_dead + live_checked_dead
        print(f"\nTotal to deactivate: {len(all_broken)}")
        for m in all_broken[:15]:
            print(f"  id={m.id:<6} course={m.course_code or '(none)':<10} title={m.title[:60]!r}")
        if len(all_broken) > 15:
            print(f"  ... and {len(all_broken) - 15} more")

        if not APPLY:
            print("\nDry run only -- no changes made. Re-run with --apply to deactivate these rows.")
            return

        for m in all_broken:
            m.is_approved = False
        db.session.commit()
        print(f"\nDeactivated {len(all_broken)} materials. They will no longer show to students.")


if __name__ == '__main__':
    main()
