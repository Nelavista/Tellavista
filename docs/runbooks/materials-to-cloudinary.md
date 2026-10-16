# Runbook — Materials → Cloudinary, untrack, purge history

> **STATUS: WRITTEN PLAN ONLY. NOT EXECUTED.** Every step below needs explicit founder approval, and step 5 rewrites git history (forbidden without it).

## What the audit found (verify before acting)
- `app/static/materials/` is ~**1.2 GB / 182 files**, tracked through **Git LFS** (pointer blobs in history; 180 files).
- `app/static/media/` is ~**146 MB / 20 files** (15 `.mp4`, 5 `.jpeg`) and is **not LFS-covered** (`.gitattributes` only lists pdf/office). Those are ordinary blobs.
- `.git` is **1.3 GB**.
- A stray tracked file `app/static/materials/accounting/h` (3 bytes) is junk.

## Hard rules
- **Do not delete or untrack `app/static/materials` or `app/static/media`** until the migration below is complete and verified.
- Never force-push; never rewrite history without explicit approval.

## Plan (each step its own PR, smallest first)
1. **Inventory + mapping.** List every tracked file, the `Material` rows referencing it, and the target Cloudinary public id. Output a CSV for review. *No changes.*
2. **Migrate to Cloudinary.** Run `scripts/maintenance/migrate_static_materials_to_cloudinary.py` against **dev first** with a **dev** Cloudinary folder. Verify N uploaded bytes == N expected and every `Material.file_url` resolves. Then prod, in a low-traffic window. (Prod-guarded; state the `DATABASE_URL` first.)
3. **Serve from Cloudinary.** Confirm the app prefers `file_url` over the local static path, and that the RAG/extraction path still works.
4. **Untrack without deleting locally** (approval required):
   ```bash
   git rm --cached -r app/static/materials app/static/media
   # add to .gitignore, commit
   ```
   The files stay on disk; V1 keeps working.
5. **Purge history (SEPARATE, APPROVED OPERATION ONLY).**
   - Media: `git lfs migrate` / `git filter-repo` for the materials paths and the un-LFS'd media.
   - Coordinate all clones and forks; a rewrite invalidates local copies.
   - Announced freeze window; everyone re-clones afterwards.
6. **Verify** fresh clone size, CI still green, V1 still serves every material, and Search Console is unaffected.

## Rollback
Steps 1–4 are reversible (`git restore --staged`, restore `.gitignore`). Step 5 is **not** until everyone re-clones.
