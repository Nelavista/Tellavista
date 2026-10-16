# 02 — LOCAL / DEV / PROD

One switch: **`APP_ENV` ∈ {`local`,`dev`,`prod`}**. Config is env-var-only, validated at startup (pydantic-settings), failing fast with a readable message.

## Matrix

| | **LOCAL** | **DEV** (staging) | **PROD** |
|---|---|---|---|
| **Web** | `http://localhost:5173` | `https://dev.nelavista.com` | `https://nelavista.com` |
| **API** | `http://localhost:8000` | `https://api-dev.nelavista.com` | `https://api.nelavista.com` |
| **Admin** | `http://localhost:5174` | `https://admin-dev.nelavista.com` | `https://admin.nelavista.com` |
| **V1 (Flask)** | `http://localhost:5000` *(confirmed default)* | — (V1 has no dev) | `https://nelavista.com` → `v1.nelavista.com` at launch |
| **Mail UI** | `http://localhost:8025` (Mailpit) | test sender (provider sandbox) | real transactional sender |
| **Database** | Postgres 16 + pgvector in Docker | Render Postgres (own instance) | Render Postgres (own instance) |
| **Redis** | Docker | Render Key Value | Render Key Value |
| **Credentials** | none — all integrations mocked/disabled | **separate** dev OAuth client, Sentry env, PostHog project, Cloudinary folder, test mail, sandbox payments | real, in Render secret settings only |
| **Data** | `make seed-local` (fake) | `make seed-local` (same fake data) | real |
| **Deploy trigger** | n/a | auto-deploy from integration branch `develop` | manual approval, from protected `main`/tags after CI |
| **Access** | developer | gated + `noindex` | public |
| **Mobile ID** | dev client (Expo Go / dev build) | `.dev` suffix bundle ID + package name | store IDs |
| **Mobile distribution** | Expo Go / EAS dev build / Android APK | TestFlight (iOS) + internal testing track / APK (Android) | App Store + Google Play, staged rollout |
| **Money** | mocked | sandbox | real |

> **dev/prod must share NOTHING secret-bearing.** The only shared thing is code.

**PROD deploy approver: `@hiipraise`** (confirmed 2026-10-16) — the sole required reviewer on the GitHub `production` environment (manual GitHub setting; see `docs/runbooks/deploy-to-prod.md`).

**Integration branch: `develop`** (created 2026-10-16 from `main`). Feature branches PR into `develop`, which auto-deploys to DEV; `develop` → `main` promotes to PROD with the approval above.

## Data rules
- dev is seeded with the **same fake sample data as local** — **never** a copy of production.
- **If production-like data is ever needed, it must be anonymised first** (names, emails, phone, OAuth subs, materials metadata scrubbed) and the anonymisation script committed. This rule is binding.

## Config & secrets design
- **`APP_ENV`** selects a settings class; every value comes from the environment.
- Per app: **`.env.example`** committed (names + safe placeholders), **`.env.local`** gitignored.
- **Real dev/prod secrets live only in Render's environment settings** (and GitHub Actions secrets for CI). **Nothing secret ships in a mobile binary** — an app bundle is public.
- **No hardcoded domains/URLs/keys.** Base URLs, cookie domain, CORS origins and OAuth redirect URIs are all derived from config. (V1 has ~20 hardcoded `HTTP-Referer: https://nelavista.com` strings — V2 must not repeat this.)
- **gitleaks** in pre-commit and CI. `.env` is **not** tracked in this repo's current history; the credentials listed in `docs/SECRETS_ROTATION.md` were exposed historically and **must be rotated** (audit §8.1).
- **Feature flags** for anything half-built (`packages/config/flags` + per-user/per-env overrides) so unfinished work merges to `develop` behind a flag and is invisible in prod.

## Prod-guard design (destructive scripts)
`tools/prodguard.py` exposes `guard(action)`:
- Detects a production target via `APP_ENV=prod` **or** a non-SQLite `DATABASE_URL` host that is not `localhost`/`127.0.0.1`.
- Refuses unless `--i-know-this-is-production` **or** `PRODGUARD_ALLOW=1`.
- **Always prints the masked target** (host + db name, password redacted) before doing anything.
- Applied to: `tools/seed_local.py` and **every** V1 `scripts/seed/*`, `scripts/maintenance/*`, `scripts/admin/*` and `scripts/audit/*--apply` entrypoint.
