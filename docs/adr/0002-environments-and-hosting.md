# ADR-0002 — LOCAL / DEV / PROD separation, hosting, secrets, prod-guard

**Status:** Accepted · **Date:** 2026-10-16

## Context

Today there is **one** environment. `.env` + `app/config.py`, one database, one set of paid third-party credentials, no `APP_ENV`, no CI, no staging. A developer's laptop can therefore point at production's Google OAuth client, Cloudinary account or database. Every script in `scripts/` except `check_template_links` imports the app and hits whatever `DATABASE_URL` resolves to, with no guard.

## Decision

### Three environments, one switch

- **`APP_ENV` ∈ {`local`, `dev`, `prod`}** drives all behaviour. Config is **environment variables only**, validated at startup with **pydantic-settings**; a missing/invalid required variable **fails fast** with a readable message. `.env.local` is gitignored; `.env.example` per app holds names + safe placeholders only.
- **Mobile gets its environment from build profiles**, never runtime guessing (ADR-0009/0010).

### Subdomain naming (deliberately not confusable with version subdomains)

| Env | Web | API | Admin |
|---|---|---|---|
| prod | `nelavista.com` | `api.nelavista.com` | `admin.nelavista.com` |
| dev | `dev.nelavista.com` | `api-dev.nelavista.com` | `admin-dev.nelavista.com` |

Version subdomains stay `v1.`, `v2.`, … The **`-dev` suffix** (not a `dev-` prefix, not `v1`/`v2` shapes) makes an environment name look nothing like a version name.

### Hosting

| Service | Host | Why |
|---|---|---|
| V1 (until launch) | Render — **unchanged** | It is live; do not move it. |
| API (dev + prod) | Render web service + **Render Key Value (Redis)** + background worker (ARQ) | Same platform V1 already uses; one dashboard; Redis and workers are first-class. |
| Web + Admin | Render Static Sites (or any static host) | They are static SPAs; no server needed. |
| Postgres (dev + prod) | **One Render Postgres per environment** | Isolation is the whole point; dev must not touch prod data. |

### Secrets

- **Real secrets live only in the hosting platform's environment settings** (Render) and in **GitHub Actions secrets** for CI. Never in the repo, never in a mobile binary (anything in an app bundle is public).
- **gitleaks** runs in pre-commit and in CI (Phase 3a).
- `docs/SECRETS_ROTATION.md` stays the source of truth for what must be rotated; the audit (§8.1) flags that `.env` is not in *this* repo's history but the credentials were exposed historically and must still be rotated.

### Per-environment third-party credentials (dev ≠ prod)

dev gets its **own** Google OAuth client (dev redirect URIs), its own Sentry environment, its own PostHog project, its own Cloudinary folder, a test mail sender, and (later) sandbox payment keys.

### Data rules

- dev is **seeded with the same fake sample data as local** (`make seed-local`), **never a prod copy**.
- **If production-like data is ever needed, it must be anonymised first.** This rule is written here and in `docs/architecture/02-environments.md`.

### Prod-guard for destructive scripts

A shared guard (`tools/prodguard.py`) is imported by every seed/maintenance/admin/`--apply` entrypoint. It **refuses to run** when it detects a production target **unless** `--i-know-this-is-production` (or `PRODGUARD_ALLOW=1`) is passed, and it prints the **masked** target first. Production is detected from `APP_ENV=prod` **or** a non-SQLite `DATABASE_URL` whose host is not `localhost/127.0.0.1`.

## Options considered
- **Two environments** (local + prod): cheap, but QA/preview has nowhere to run — rejected.
- **A `dev-` prefix** (`dev.nelavista.com`): the brief's own suggestion, but `dev-` and `v1-` are visually similar at a glance. `-dev` suffix chosen instead.
- **Separate infra per env on different clouds**: unnecessary moving parts for a 3-person team.

## Reversibility
- **High.** Subdomains are DNS + host config. Secrets are re-pointable. The guard is one module.
- **Low** risk to V1: nothing here changes V1's runtime.

## Team cost
- ~0.5 day to provision dev (Render service + Redis + DB + Google OAuth client + Sentry/PostHog projects). Then it removes an entire class of "I pointed my laptop at prod" incidents.

## Manual steps (do not automate — see runbooks)
Render service/DB/Redis creation, DNS records, Google Cloud dev OAuth client, Sentry/PostHog dev projects, Cloudinary folder, mail sender.
