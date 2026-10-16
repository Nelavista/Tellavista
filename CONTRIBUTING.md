# Contributing to Nelavista

## The one rule that overrides the others
**V1 is live with real students at `nelavista.com`.** Nothing you do may break it. V1 is frozen for features.

Before and after any change that touches V1 (`app/`, `migrations/`, `scripts/`, `tests/`, V1 config), run and report:

```bash
pytest tests/
python -m scripts.audit.check_template_links
```

Never force-push. Never rewrite git history without the founder's explicit approval. Never delete or untrack `app/static/materials` or `app/static/media`.

## Trunk-based flow

```
feat/xyz  ──PR──▶ develop (integration) ──auto-deploy──▶ DEV
                          │
                          └──PR (manual approval, CI green)──▶ main ──▶ PROD
```

- Short-lived branches: `feat/…`, `fix/…`, `chore/…`, `docs/…`.
- **`develop`** is the integration branch; merging there auto-deploys to `dev.nelavista.com`.
- **`main`** is protected; it deploys to prod only after CI passes **and** a manual approval.
- PRs are small and single-purpose. One owner per area (`CODEOWNERS`).

## Commits
Conventional Commits: `feat(api): …`, `fix(web): …`, `chore: …`, `docs(adr): …`.

## Local setup
`make bootstrap && make up && make seed-local && make dev`. Target: a new developer is running in **under 15 minutes** (web + API). Mobile setup is separate and shorter: `docs/runbooks/mobile-local-setup.md`.

## Path filters
CI and deploys are path-filtered: a change in `apps/v1` (or V1 at root) never rebuilds V2 and vice versa; a web-only change never triggers a mobile build.

## Shared code
Only through **versioned workspace packages** (`packages/api-client`, `packages/contracts`, `packages/design-tokens`, `packages/config`). **No copy-paste** of types or API calls between apps.

## Database rules (multiple developers)
- **Expand/contract** only: add nullable columns → deploy → backfill → remove later.
- **A single Alembic head is enforced in CI.** Two heads fail the build.
- Resolving a conflict: rebase; if two heads remain, `alembic merge -m "merge heads" <rev1> <rev2>`; never edit a merged revision.

## Secrets
- Never commit a secret. `.env.local` is gitignored; real values live in Render/Actions settings only.
- **gitleaks runs in pre-commit and CI.** If it blocks you, that is the intended outcome — talk to the founder, don't bypass it.
- **Never print, copy or commit a secret**, including in a PR description or CI log.

## Feature flags
Anything half-built merges to `develop` **behind a flag** (`packages/config` flags + per-env overrides) so it is invisible in prod until it is done.

## Destructive scripts
Seed/maintenance/admin scripts are **prod-guarded** (`tools/prodguard.py`). They refuse to run against a production database unless `--i-know-this-is-production` is passed, and they always print the masked target first. **Before running any data-touching script, state which `DATABASE_URL` it will hit.**

## Manual steps (never automate)
Changes in Render, DNS, Google Cloud Console (OAuth), Search Console, Apple Developer, Google Play Console or Expo/EAS are **manual** — list them in the PR and wait for confirmation.
