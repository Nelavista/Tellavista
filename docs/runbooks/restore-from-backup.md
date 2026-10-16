# Runbook — Backup and restore

**A backup you have never restored is not a backup.** Test the restore before every schema change to prod.

## What is backed up
Each environment's Render Postgres (dev and prod are separate — ADR-0002/0005). Backups contain **real student PII** and are never committed (`.gitignore` blocks `backups/`, `*.dump`).

## Take a manual backup (before a schema change)
```bash
pg_dump "$PROD_DATABASE_URL" --format=custom --no-owner --file "backups/prod-$(date +%Y%m%d%H%M).dump"
```
`backups/` is gitignored. Store copies in the platform's managed backup, not just locally.

## Test a restore (on a throwaway database — never prod)
```bash
createdb nelavista_restore_test
pg_restore --dbname nelavista_restore_test --no-owner --clean backups/<file>.dump
# sanity checks
psql nelavista_restore_test -c "select count(*) from users;"
```
Record the date and outcome. **Only then** proceed with the prod schema change.

## Restore prod (last resort)
1. Put the app in maintenance / stop writes.
2. `pg_restore --dbname "$PROD_DATABASE_URL" --no-owner --clean <file>.dump`.
3. Verify health + a login + a recent record.
4. Resume. Write an incident note.

## Rules
- **Never** restore a dev snapshot into prod.
- **Never** run a destructive script without the prod-guard flag (`tools/prodguard.py`).
- State which `DATABASE_URL` a restore targets **before** running it.
