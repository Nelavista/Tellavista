"""Import student opportunities from a reviewed manifest
(seed_data/opportunities/opportunities.json) into StudentOpportunity rows.

Production Postgres isn't reachable from a dev PC, so listings researched offline
are committed to the manifest and this script is run on the server, the same pipeline as
the other seeds.

Trust rules (the same ones the admin UI enforces; see services/student_opportunity_service.py):
- Every entry goes through the same validation as the admin form (URLs must be real
  http(s) links, NELAVISTA_APPLICATION needs a recorded partnership, ...).
- An entry is marked verified ONLY if it has "verified_on" (the date someone checked the
  official page) plus source_url and application_url. Otherwise it's imported as an
  unverified draft that students never see.
- An entry is published ONLY if it asks to be ("publish": true) AND passes every publish
  check (verified, source, application route, deadline or rolling, not closed). A closed
  programme is never published, whatever the manifest says.
- Upserts by slug (defaults to "<organization> <title>"), so re-running is safe. Rows an
  admin has since edited in the dashboard are skipped unless --overwrite is passed.

Manifest entry (only title + organization are required):
    {
      "title": "...", "organization": "...", "category": "scholarship",
      "categories": ["leadership"], "summary": "...", "eligible_summary": "...",
      "description": "...", "eligibility": "...", "benefits": "...", "requirements": "...",
      "application_steps": "step one\\nstep two",
      "disciplines": ["all"], "levels": ["200", "300"], "tags": ["AI", "data"],
      "location_scope": "nigeria", "location": "...", "delivery_format": "online",
      "opens_at": "2026-11-01", "deadline": "2026-12-15", "is_rolling": false, "deadline_note": "...",
      "application_url": "https://...", "official_website": "https://...", "source_url": "https://...",
      "application_mode": "EXTERNAL_WEBVIEW",
      "verified_on": "2026-11-16", "verification_notes": "...", "publish": true, "featured": false
    }

Default is a DRY RUN; pass --apply to write.

Usage:
    python -m scripts.seed.seed_student_opportunities
    python -m scripts.seed.seed_student_opportunities --apply [--overwrite] [--manifest path.json]
"""
import json
import os
import sys
from datetime import datetime

from app import app, db
from app.models import StudentOpportunity
from app.services import student_opportunity_service as svc

DEFAULT_MANIFEST = os.path.join(os.path.dirname(__file__), '..', '..', 'seed_data', 'opportunities', 'opportunities.json')
SEED_MARKER = '[seed:opportunities]'


class _Form(dict):
    """Adapts a manifest entry to the request.form shape svc.apply_form() reads."""
    def get(self, key, default=None):
        value = super().get(key, default)
        if isinstance(value, bool):
            return '1' if value else ''
        if isinstance(value, list):
            return ', '.join(str(v) for v in value)
        return value

    def getlist(self, key):
        value = super().get(key) or []
        return value if isinstance(value, list) else [value]


def load_manifest(path):
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    return data.get('opportunities', data) if isinstance(data, dict) else data


def run(entries, apply=False, overwrite=False):
    report = {'created': 0, 'updated': 0, 'skipped': 0, 'invalid': 0, 'published': 0, 'drafts': 0}
    for i, entry in enumerate(entries, 1):
        label = f"#{i} {entry.get('organization', '?')}: {entry.get('title', '?')}"
        slug = entry.get('slug') or svc.slugify(f"{entry.get('organization', '')} {entry.get('title', '')}")
        opp = StudentOpportunity.query.filter_by(slug=slug).first()
        is_new = opp is None
        if not is_new and not overwrite and SEED_MARKER not in (opp.verification_notes or ''):
            print(f'  SKIP {label}: exists and was edited in the dashboard (use --overwrite)')
            report['skipped'] += 1
            continue
        if is_new:
            opp = StudentOpportunity(slug=slug, verification_status='unverified', is_published=False,
                                     featured=False, is_rolling=False, is_partner=False, allows_in_app_view=False,
                                     manually_closed=False, is_archived=False)
        form = _Form(entry)
        form['verification_notes'] = f"{SEED_MARKER} {entry.get('verification_notes') or ''}".strip()
        errors = svc.apply_form(opp, form, form.getlist)
        if errors:
            print(f'  INVALID {label}: ' + ' '.join(errors))
            report['invalid'] += 1
            db.session.rollback()
            continue

        verified_on = entry.get('verified_on')
        if verified_on and opp.source_url and (opp.application_url or opp.embed_url):
            checked = datetime.strptime(verified_on, '%Y-%m-%d')
            opp.verification_status = 'verified'
            opp.verified_at = opp.verified_at or checked
            opp.last_checked_at = checked
        else:
            opp.verification_status = 'unverified'
            opp.is_published = False

        problems = svc.publish_problems(opp)
        if entry.get('publish') and not problems:
            opp.is_published = True
            opp.published_at = opp.published_at or datetime.utcnow()
            report['published'] += 1
            state = 'PUBLISH'
        else:
            opp.is_published = False
            report['drafts'] += 1
            state = 'DRAFT' + (f" ({'; '.join(problems)})" if entry.get('publish') and problems else '')
        print(f"  {'NEW ' if is_new else 'UPD '}{state} {label} [{svc.compute_status(opp)['label']}]")
        if is_new:
            db.session.add(opp)
            report['created'] += 1
        else:
            report['updated'] += 1
        if apply:
            db.session.commit()  # per entry, so a later invalid entry's rollback can't undo it
        else:
            db.session.flush()   # catch DB-level problems in the dry run too
    if not apply:
        db.session.rollback()
    return report


def main(argv):
    apply = '--apply' in argv
    overwrite = '--overwrite' in argv
    path = DEFAULT_MANIFEST
    if '--manifest' in argv:
        path = argv[argv.index('--manifest') + 1]
    entries = load_manifest(path)
    print(f"{'APPLYING' if apply else 'DRY RUN'}: {len(entries)} entries from {os.path.abspath(path)}")
    with app.app_context():
        report = run(entries, apply=apply, overwrite=overwrite)
    print(report)
    if not apply:
        print('Nothing written. Re-run with --apply.')


if __name__ == '__main__':
    main(sys.argv[1:])
