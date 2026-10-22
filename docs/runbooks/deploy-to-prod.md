# Runbook — Deploy to PROD

PROD is live with real students. Nothing here is routine.

## Preconditions (all must be true)
- [ ] CI green on the exact commit/tag.
- [ ] Change is reviewed and approved (CODEOWNERS).
- [ ] **If a schema change:** a **fresh backup exists** and a **restore has been tested** (`restore-from-backup.md`).
- [ ] Rollback plan written (`rollback.md`).
- [ ] Feature-flagged if the work is unfinished.
- [ ] Any manual step (Render/DNS/Google/Apple/Play) listed and confirmed.

## Trigger
Push to **`main`** or a version tag → `.github/workflows/deploy-prod.yml` → `environment: production` **requires manual approval** in GitHub.

**PROD deploy approver: `@hiipraise`** (confirmed 2026-10-16). This is enforced by the GitHub **Environment `production` → Required reviewers** setting, which must list `@hiipraise` — that is a **manual GitHub setting**, not repo code. Only an approved reviewer can release a PROD deploy.

## Order of operations
1. **Approve** the `production` environment gate.
2. **Migrations (explicit, ordered):** `APP_ENV=prod` + the prod `DATABASE_URL`, `SKIP_DB_INIT=1`:
   ```
   alembic -c apps/api/alembic.ini upgrade head
   ```
   Expand-only first; contract in a later release (ADR/`04-v1-to-v2-migration.md`).
3. **Deploy API**, then **web/admin** (hooks).
4. **Verify:** `/v1/health`, a login, one read, one write. Check PostHog (if configured) and the API logs for errors.
5. **Announce** what changed.

## After
- Watch error rate and latency for 30 minutes.
- If anything regresses → `rollback.md`.

## Secrets
Only in Render's environment settings. Never in the repo, never in logs, never in a mobile binary.
