# Docs index

For the V2 web launch, read these three and ignore the rest:

1. **`RUN-LOCALLY.md`** (repo root) — run V2 on Windows in about 15 minutes.
2. **`docs/runbooks/v2-launch-checklist.md`** — the seven-step launch plan.
3. **`docs/runbooks/domain-switch.md`** — the domain move and rollback in detail.

## Reference (only when a step sends you there)

- **`docs/runbooks/rollback.md`** — put V1 back if the cutover goes wrong.
- **`docs/runbooks/restore-from-backup.md`** — Render Postgres restore drill.
- **`docs/runbooks/rotate-secrets.md`** — key rotation.
- **`docs/architecture/02-environments.md`** — env vars and environments.
- **`docs/architecture/03-versioning-and-domains.md`** — why V1 lives on `v1`.
- **`docs/adr/`** — the decisions behind the architecture.

## Not part of this launch

The mobile app, DEV preview, load-test measurement and Cloudinary material
migration are post-launch. Their runbooks are kept for later but are not steps in
the launch plan.

## Historical, not instructions

`docs/build/`, `docs/MIGRATION_MAP.md`, `docs/architecture/00-audit.md` and the
older architecture notes describe earlier plans (including Sentry and a DEV
environment). They are kept for context only. If a historical page disagrees with
the launch plan, the launch plan wins.
