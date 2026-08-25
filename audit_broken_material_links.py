"""Finds (and optionally deactivates) Material rows whose file_url points at a local
static file that does not exist on disk -- the root cause behind the Level 1 audit's
"~88% of seeded material links are broken" finding. The seed scripts themselves
(seed_materials.py, seed_100_level_science_500.py, seed_200_to_400_COMPLETE.py,
seed_200_to_400_level_science.py, seed_30_courses.py) were fixed separately to stop
CREATING new dead-link rows going forward -- this script is for cleaning up rows that
were already seeded into a real database before that fix existed.

This does NOT touch Cloudinary-hosted uploads (file_url starting with http(s)://) or
external/auto-ingested materials (external_url set) -- only rows whose file_url is a
bare local /static/materials/... path that genuinely doesn't exist on this machine's
checkout. Run this on the same machine/deployment whose filesystem actually holds (or
is missing) static/materials/ -- a path this script can't find locally but that exists
on the real deployment would be a false positive, so double-check the sample output
before using --apply on a database you don't fully control.

Default is a DRY RUN: it only reports what it would change. Nothing is modified unless
you pass --apply. Deactivated rows (is_approved=False) are NOT deleted -- they simply
stop showing up to students, same as an unapproved upload, and can be re-approved later
if the file turns out to exist after all (e.g. it just needs re-uploading).

Usage:
    python audit_broken_material_links.py            # report only, changes nothing
    python audit_broken_material_links.py --apply     # actually deactivate broken rows
"""
import sys
import os
from app import app, db
from models import Material

APPLY = '--apply' in sys.argv


def _is_broken_local_path(file_url):
    if not file_url:
        return False
    if file_url.startswith(('http://', 'https://', '//')):
        return False  # Cloudinary or another absolute URL -- not what this script checks
    local_path = file_url.lstrip('/')
    if not local_path.startswith('static/'):
        return False
    return not os.path.exists(local_path)


def main():
    with app.app_context():
        candidates = Material.query.filter(
            Material.is_approved.is_(True),
            Material.file_url.isnot(None),
        ).all()

        broken = [m for m in candidates if _is_broken_local_path(m.file_url)]

        print(f"Checked {len(candidates)} approved materials with a file_url set.")
        print(f"Found {len(broken)} pointing at a local file that does not exist on this machine.\n")

        if not broken:
            print("Nothing to do.")
            return

        print("Sample (first 20):")
        for m in broken[:20]:
            print(f"  id={m.id:<6} course={m.course_code or '(none)':<10} title={m.title[:60]!r}  ->  {m.file_url}")
        if len(broken) > 20:
            print(f"  ... and {len(broken) - 20} more")

        if not APPLY:
            print(f"\nDry run only -- no changes made. Re-run with --apply to deactivate these {len(broken)} rows.")
            return

        for m in broken:
            m.is_approved = False
        db.session.commit()
        print(f"\nDeactivated {len(broken)} materials (is_approved=False). They will no longer show to students.")


if __name__ == '__main__':
    main()
