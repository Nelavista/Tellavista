# Runbook — Rollback

## Web / Admin
They are static SPAs: **redeploy the previous build** from Render (Deploys → a previous successful deploy → Redeploy). No database involved.

## API
1. Render → API service → previous successful deploy → **Redeploy**.
2. **Only if the release included a schema change**, run the migration's `downgrade` **or** apply the compensating migration from the same release (ASCII rule: expand/contract, so a code rollback alone is usually safe).
3. Verify `/v1/health` and a login.

## Database
Prefer a **forward fix** over a restore. A restore loses data written since the backup.
- Backups & tested restore: `restore-from-backup.md`.
- Never restore prod from a dev snapshot.

## Mobile
- **JS:** `eas update:rollback`.
- **Native:** promote the previous store build; halt the staged rollout.

## Domain swap
If V2 misbehaves immediately after launch: re-point `nelavista.com` at V1's Render service. With a 60 s TTL this takes minutes; the V2 database is separate so nothing is lost (ADR-0003).

## After any rollback
Write a short incident note: what changed, what rolled back, what the fix will be, and add a test if one was missing.
