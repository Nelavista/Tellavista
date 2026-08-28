"""Fixes the ROOT CAUSE behind the historical "~88% of seeded material links are
broken" finding (see audit_broken_material_links.py's docstring), instead of just
re-running that cleanup script forever. The root cause: seeded Material rows pointing
at a local static/materials/... path assume that file still exists on disk at request
time -- true on a developer's machine, false on Render's ephemeral filesystem after any
redeploy/restart that doesn't happen to carry that exact file along.

Cloudinary is already this project's real, persistent file store (every student upload
already goes there -- see routes/materials_routes.py::upload_material). This script
migrates every local-static Material row onto Cloudinary too, so "local static file
path stored in the database" stops being a supported state for materials going
forward -- there is one storage strategy, not two.

For each approved Material whose file_url is a bare local static/... path:
  - If the file exists on disk (this machine's checkout): upload it to Cloudinary,
    rewrite file_url to the returned secure_url, keep everything else unchanged.
  - If the file does NOT exist on disk: deactivate it (is_approved=False), same
    conservative behavior as audit_broken_material_links.py -- there is nothing to
    migrate, and a student must never see a dead link.

Default is a DRY RUN: reports what it would do, changes nothing. Pass --apply to
actually upload files and update rows. Idempotent -- a row whose file_url is already an
http(s) URL (already migrated, or never local to begin with) is skipped.

Usage:
    python migrate_static_materials_to_cloudinary.py            # report only
    python migrate_static_materials_to_cloudinary.py --apply     # upload + rewrite
"""
import os
import sys

import cloudinary
import cloudinary.uploader

from app import app, db
from models import Material

APPLY = '--apply' in sys.argv

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True,
)


def _local_static_candidates():
    return Material.query.filter(
        Material.is_approved.is_(True),
        Material.file_url.isnot(None),
        ~Material.file_url.ilike('http%'),
    ).all()


def main():
    with app.app_context():
        candidates = [m for m in _local_static_candidates() if (m.file_url or '').lstrip('/').startswith('static/')]

        existing_on_disk, missing = [], []
        for m in candidates:
            local_path = m.file_url.lstrip('/')
            (existing_on_disk if os.path.exists(local_path) else missing).append(m)

        print(f"Found {len(candidates)} approved materials with a local static file_url.")
        print(f"  {len(existing_on_disk)} exist on this machine's checkout -- would migrate to Cloudinary.")
        print(f"  {len(missing)} do not exist here -- would deactivate (dead link, nothing to migrate).")

        if not APPLY:
            print("\nDry run only -- no uploads, no changes. Re-run with --apply.")
            return

        migrated = failed = 0
        for m in existing_on_disk:
            local_path = m.file_url.lstrip('/')
            try:
                public_id = f"nelavista_materials_migrated/{m.course_code or 'general'}_{m.id}"
                result = cloudinary.uploader.upload(
                    local_path, resource_type='raw', public_id=public_id, overwrite=True,
                )
                url = result.get('secure_url')
                if not url:
                    raise Exception('no secure_url returned')
                m.file_url = url
                db.session.commit()
                migrated += 1
            except Exception as e:
                db.session.rollback()
                print(f"[FAIL] material id={m.id} ({local_path}): {e}")
                failed += 1

        for m in missing:
            m.is_approved = False
        db.session.commit()

        print(f"\nMigrated {migrated} to Cloudinary ({failed} failed -- left untouched, re-run to retry).")
        print(f"Deactivated {len(missing)} dead links.")


if __name__ == '__main__':
    main()
