# Runbook — Deploy to DEV

DEV (`dev.nelavista.com`, `api-dev.nelavista.com`, `admin-dev.nelavista.com`) is the shared, non-production environment. It is where PR previews and QA happen.

## Trigger
Merge to **`develop`** → `.github/workflows/deploy-dev.yml` fires (path-filtered) → Render deploy hooks run. **No manual approval** for DEV.

## What DEV is
- **Gated + `noindex`.** Basic-auth or an IP allowlist in front of it; `X-Robots-Tag: noindex` and a `robots.txt` that disallows all. The public and search engines must not reach it.
- **Its own everything:** Render Postgres, Render Key Value (Redis), Google OAuth client (dev redirect URIs), Sentry environment, PostHog project, Cloudinary folder, test mail sender, sandbox payments later.
- **Seeded with the same fake data as local** (`make seed-local`). **Never a copy of production.**

## Deploying manually (if the hook is not wired yet)
1. Confirm CI is green on `develop`.
2. Render → the dev API service → **Manual Deploy** (or POST the deploy hook).
3. Run migrations as an explicit step: `make db-upgrade` with `APP_ENV=dev` and the dev `DATABASE_URL` — **state the target out loud first**.
4. Smoke test: `https://api-dev.nelavista.com/v1/health` → `{"status":"ok"}`.

## Production-like data
**Never copy prod into dev.** If production-like data is needed, **anonymise it first** (names, emails, phones, OAuth subs, material metadata) and use a committed anonymisation script.
