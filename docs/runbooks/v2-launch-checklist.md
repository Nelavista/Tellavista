# V2 launch checklist — DEV preview first, then V1 on `v1`, V2 on `nelavista.com`

> **Status:** ready to execute. This is the ordered list of what has to happen, who does it, and
> how to prove each step worked.
>
> **The goal in one line:** get a working V2 preview at a Render URL *this week*, then move V1 to
> `v1.nelavista.com` and put V2 on `nelavista.com` in one short, rehearsed window.
>
> Read `docs/runbooks/domain-switch.md` alongside this file; it is the terse version of Phase E.
> The architecture is in `docs/architecture/03-versioning-and-domains.md`.

**Owner key**

| Tag | Meaning |
|---|---|
| **[YOU]** | Only you can do it: Render dashboard, Namecheap, Google Cloud, provider accounts, approvals. |
| **[ENG]** | Repo/code change. I can do it; it ships as a PR through CI. |
| **[BOTH]** | We do it together in one sitting (usually: I run the command, you confirm the target). |

---

## 0. The seven launch traps (B0–B3 are now fixed)

These are the gaps found while writing the checklist. B0–B3 are implemented; B4 and
the Phase B hardening items are still open.

1. **The web app calls `/api/v1/...` same-origin, but nothing proxies `/api` in a deployed
   environment.** The Vite dev server strips the `/api` prefix locally (`apps/web/vite.config.ts`);
   there is no equivalent on Render. Without a proxy, every browser request to
   `https://nelavista.com/api/...` returns the SPA's `index.html` and the app looks broken.
   *Fix:* a Render static-site rewrite `/api/*` → `<api-host>/*` (server-side proxy), or a tiny
   proxy web service. See **A5**.
2. **A fresh database has no roles.** `roles` is populated only by the local seed and tests
   (`app/seed/roles.py`). After `alembic upgrade head` on a new Postgres, `roles` is empty, so a
   signup gets `role_id = NULL`, permission checks fail, and no one can be staff.
   *Fixed:* migration `20261022_1000` inserts the six roles idempotently; a blank database is
   correct immediately after `upgrade head`.
3. **There is no first-admin path.** Nothing in the API or admin UI promotes a user. The first
   `super_admin` and a second approver have to be created deliberately.
   *Fixed:* `tools/create_staff.py` (Phase B2), prod-guarded and audited. Payouts at or above
   ₦50,000 still need **two** approvers, so create both accounts.
4. **Email cannot authenticate.** `send_email` used `smtplib` with no username/password
   (`app/worker/tasks.py`), and Render's free web services block outbound SMTP ports 25/465/587.
   *Fixed:* `EMAIL_PROVIDER=sendhiiv` uses Sendhiiv's HTTP API (no SMTP port; 202 = queued; only
   HTTP 429 is retried, because a 5xx may already have queued the message). SMTP AUTH
   (`MAIL_USERNAME`/`MAIL_PASSWORD`) exists as a fallback for a relay on a paid instance. In
   non-production, `EMAIL_REDIRECT_TO` funnels every message to one inbox.
5. **There is no production content path.** The only thing that loads the curriculum is
   `tools/seed_local.py`, which also creates fake students and a fake university. Never run it
   against PROD. The V1 importer (`/ops/imports`) is the intended path, but there is no V1 export
   generator in the repo.
   *Fix:* an export tool + a curriculum-only seed (Phase B4).
6. **Only one Render service can own `nelavista.com`.** V1 owns it today. The cutover is therefore a
   **Render custom-domain move**, not just a DNS edit: DNS already points at Render's shared load
   balancer. Expect a short window where the apex has no service until it is on V2 (Phase E).
7. **`alembic -c apps/api/alembic.ini` from the repo root used to resolve V1's `migrations/`**, not
   V2's. `heads` printed V1's head (`f1b2c3d4e5f6`) and `upgrade` died importing Flask — so the
   command in the runbooks was both wrong and misleading. Fixed in #14 (B0). Before that fix, the
   only safe form was `cd apps/api` first.

Two more, lower down but still before the public switch: **local disk storage is ephemeral**
(`STORAGE_BACKEND=local`) and **the PWA caches authenticated API GETs without clearing them on
logout**. Both are Phase B.

---

## 1. Decisions to make before creating anything (30 minutes)

| # | Decision | Recommended | Why |
|---|---|---|---|
| 1 | Render plan | **Paid** instances for API + worker + Postgres | Free web services block SMTP and spin down; the API must send mail and stay warm. Static sites can stay free. |
| 2 | Region | Same region as V1 if it is close to users (e.g. Frankfurt/London) | Keep API, worker and Postgres in one region; the static sites are on the global CDN anyway. |
| 3 | Dev gating | Start on `*.onrender.com` links, unlisted; add basic-auth/Cloudflare before `dev.nelavista.com` is public | Render has no built-in basic auth. A short private preview does not need DNS. |
| 4 | Email provider | **Resend** or **Brevo** SMTP (or SendGrid) | Real deliverability + SPF/DKIM/DMARC; free tiers are enough for launch. |
| 5 | V1 data | **Import V1 users + taxonomy + materials + questions** before cutover | Otherwise existing students lose their accounts and history. Passwords carry over (PBKDF2 → Argon2 on first login). |
| 6 | Mobile at launch | **Web-first**, mobile store release as a separate track | D4 screenshots and D5 device smoke are still owed; the web launch should not wait for store review. |
| 7 | V1 after cutover | Banner + read-only/maintenance at `v1`, kept online | Prevents two live copies of student data diverging. |
| 8 | V1 repo move to `apps/v1` | **Defer** until well after launch | It changes Render's Root Directory non-atomically and adds launch risk for zero user benefit. The domain move does not require it. |

---

## 2. Phase A — V2 DEV preview (no DNS, no apex changes)

Target: a URL you can send to a tester, with signup/login/learning/admin working end-to-end.

### A1 [YOU] Confirm the Render workspace and V1 facts

In the Render dashboard, write these down before touching anything:

- [ ] V1 service name, region, plan, and its **exact custom domains** (primary + aliases).
- [ ] V1's current Root Directory, build command, start command.
- [ ] V1's Postgres name/region (V2 must be a **separate** database).
- [ ] Whether the workspace is Hobby (2 custom domains) or Pro (15). V2 needs about 8 hostnames:
      `nelavista.com`, `www`, `api`, `admin`, `dev`, `api-dev`, `admin-dev`, `v1`.
- [ ] In Namecheap → Domain → **Advanced DNS**, screenshot the current records. Do **not** change
      nameservers. Confirm `@` is an `A` record to `216.24.57.1` (Render's load balancer). If it is
      not, stop and tell me — the cutover plan changes.

### A2 [YOU] Create the DEV Postgres

- Render → **New → Postgres**, name `nelavista-db-dev`, same region, Postgres 16.
- Copy both connection strings:
  - **Internal** for the API and worker (`postgresql://...@dpg-.../nelavista...`).
  - **External** for running migrations and seeds from your laptop (add `?sslmode=require` if the
    dashboard's external URL does not already include it).
- The migrations create the `vector` extension. If `CREATE EXTENSION vector` fails, tell me; do not
  hand-edit the migration.

### A3 [YOU] Create the DEV API web service

Render → **New → Web Service** → the `Nelavista/Tellavista` repo.

| Setting | Value |
|---|---|
| Name | `nelavista-api-dev` |
| Region | same as the database |
| Branch | `develop` |
| Root Directory | *(empty — repo root)* |
| Runtime | Python 3.11 |
| Build Command | `pip install uv && uv sync --frozen --no-dev` |
| Start Command | `uv run --no-sync --package nelavista-api uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir apps/api` |
| Health Check Path | `/v1/health` |
| Instance | paid (Starter is enough to start) |
| Auto-Deploy | Yes (or via the deploy hook in A8) |

Environment (Render → Environment; use an **Environment Group** called `nelavista-dev` so the API
and worker cannot drift):

```text
APP_ENV=dev
API_VERSION=v1
SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_urlsafe(48))">
DATABASE_URL=<DEV Postgres INTERNAL URL>
CORS_ORIGINS=https://<nelavista-web-dev>.onrender.com,https://<nelavista-admin-dev>.onrender.com
WEB_BASE_URL=https://<nelavista-web-dev>.onrender.com
MAIL_FROM=no-reply@nelavista.com
# Sendhiiv in DEV: it delivers for real. Set EMAIL_REDIRECT_TO to your own inbox
# so preview mail cannot reach a real tester. LEAVE SENDHIIV_FROM empty until the
# domain is verified (the shared sender is used instead).
EMAIL_PROVIDER=sendhiiv
SENDHIIV_API_KEY=sh_live_...
SENDHIIV_FROM=
EMAIL_REDIRECT_TO=you@example.com
STORAGE_BACKEND=local                  # dev only; use cloudinary for prod
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4o-mini
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
CLOUDINARY_URL=
SENTRY_DSN=
POSTHOG_API_KEY=
PUSH_ENDPOINT=
FLAG_SKILLS_JOURNEY=1
FLAG_MANAGED_WORKFORCE=1
FLAG_LEDGER=1
FLAG_ACADEMIA_CONNECT=1
FLAG_TALENT_PROFILE=1
FLAG_EXTERNAL_OPPORTUNITIES=1
```

Notes:

- `REDIS_URL` is **not needed**: rate limiting is in-process and jobs are a database table.
  Do not pay for Render Key Value for this launch.
- `SKIP_DB_INIT` appears in the runbooks but is not read by the code. Migrations are always explicit.
- `SECRET_KEY` signs JWTs. Set it once; changing it logs everyone out.
- `WEB_BASE_URL` is what verification and reset emails link to. For the preview it is the web
  service's `onrender.com` URL; later it becomes `https://dev.nelavista.com`.

Before the first deploy succeeds, the service will fail its health check until A7 runs the
migrations. That is expected; deploy, then migrate, then redeploy/restart.

### A4 [YOU] Create the DEV worker

Render → **New → Background Worker**, same repo/branch/region.

| Setting | Value |
|---|---|
| Name | `nelavista-worker-dev` |
| Build Command | `pip install uv && uv sync --frozen --no-dev` |
| Start Command | `uv run --no-sync --package nelavista-api python -m app.worker` |
| Environment | the same `nelavista-dev` group |

The worker drains the durable `jobs` table (`app/worker/`). Without it, verification emails and
pushes are queued forever. It is a database loop, not an ARQ/Redis process.

### A5 [YOU] Create the DEV web static site

Render → **New → Static Site**, same repo, branch `develop`.

| Setting | Value |
|---|---|
| Name | `nelavista-web-dev` |
| Root Directory | *(empty — repo root)* |
| Build Command | `corepack enable && pnpm install --frozen-lockfile && pnpm --filter @nelavista/web build` |
| Publish Directory | `apps/web/dist` |
| Environment | `VITE_API_VERSION=v1` (the built app uses relative `/api`, so no API URL is baked in) |

**Redirects/Rewrites** (order matters — first match wins):

| # | Source | Destination | Action |
|---|---|---|---|
| 1 | `/api/*` | `https://<nelavista-api-dev>.onrender.com/*` | **Rewrite** |
| 2 | `/*` | `/index.html` | **Rewrite** |

The first rule is the proxy. It keeps the browser on the web origin, so the API's host-only
`nv_refresh` cookie and readable `nv_csrf` cookie work exactly as they do locally. Do **not** use a
Redirect here.

**If the proxy misbehaves** (POST body dropped, `Set-Cookie` stripped, or shared caching of an
authenticated GET), fall back to one small Render **Web Service** per frontend that serves the built
`dist/` and reverse-proxies `/api/` to the API (Caddy or nginx in a two-line Dockerfile). A web
service is not CDN-cached, so the auth/caching risk disappears. This is the same origin model, just
with a server we control. Do not switch the frontend to a cross-origin API URL: the CSRF cookie is
host-only on the API, so `document.cookie` on the web origin would not see it.

**Headers** (Settings → Headers):

| Path | Header | Value |
|---|---|---|
| `/*` | `X-Robots-Tag` | `noindex` |
| `/*` | `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `/*` | `X-Content-Type-Options` | `nosniff` |
| `/api/*` | `Cache-Control` | `no-store` (verify it reaches the proxied response; see A9) |

### A6 [YOU] Create the DEV admin static site

Same as A5, with:

| Setting | Value |
|---|---|
| Name | `nelavista-admin-dev` |
| Build Command | `corepack enable && pnpm install --frozen-lockfile && pnpm --filter @nelavista/admin build` |
| Publish Directory | `apps/admin/dist` |
| Rewrite 1 | `/api/*` → `https://<nelavista-api-dev>.onrender.com/*` (Rewrite) |
| Rewrite 2 | `/*` → `/index.html` (Rewrite) |
| Header | `X-Robots-Tag: noindex` |

The admin is already `noindex` in its HTML; the header covers the API responses too.

### A7 [BOTH] Migrate, seed roles, load dev data, create two staff accounts

Run from the repo root on Windows. **Say the target database out loud before each command.**

```powershell
# Point at the DEV database for this shell only.
$env:APP_ENV = "dev"
$env:DATABASE_URL = "<DEV Postgres EXTERNAL URL>"
$env:SECRET_KEY = "<any non-empty value for the CLI>"
# A Render database is not localhost, so the prod guard treats it as production.
# This opt-in is required by seed_local and create_staff; check the printed target
# before each run.
$env:PRODGUARD_ALLOW = "1"

# 1. Schema. Run B0 first: without it this resolves V1's migrations/ and fails
#    (or worse, prints V1's head and looks fine).
apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini upgrade head
apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini heads
#    heads must print exactly one head: 20261022_1000 (head)

# 2. Dev sample data (roles, fake university, curriculum, two sample students)
apps\api\.venv\Scripts\python.exe -m tools.seed_local
```

Then create the two staff accounts. Sign them up as normal accounts in the web UI first (the tool
never creates a password), then promote them:

```powershell
# PRODGUARD_ALLOW is already set above. The guard prints the masked DB target;
# read it before the tool changes anything.
apps\api\.venv\Scripts\python.exe -m tools.create_staff `
  --email you@nelavista.com --role super_admin
apps\api\.venv\Scripts\python.exe -m tools.create_staff `
  --email ops@nelavista.com --role ops_admin
```

The tool verifies the email, sets the role, and writes `audit_logs.action = 'staff.role_granted'`
in the same transaction. Re-running it is safe: it reports `(already set)` and does not duplicate the
audit row.

Why two: the payout guardrail requires a **second approver at ≥ ₦50,000.00**, and the Platform
settings route is super-admin only. A single staff account cannot approve its own payouts (by
design) and leaves you locked out of one of the two roles.

Dev email verification shortcut: signup works and login does **not** require a verified email, so
you can test the whole student journey before email is wired. The banner will keep asking to verify.
With `EMAIL_REDIRECT_TO` set in DEV, the verification link lands in that inbox (the subject names the
real recipient), so you can still click it. To verify a test account without email, run a one-off
`update users set email_verified = true where email = '...';` or promote it with
`tools/create_staff.py`, which sets `email_verified = true`.

### A8 [YOU] Wire the deploy hooks (so `develop` deploys itself)

In Render, copy each service's **Deploy Hook** URL. In GitHub → repo → Settings → Secrets and
variables → Actions, add:

- `RENDER_DEV_API_DEPLOY_HOOK`
- `RENDER_DEV_WEB_DEPLOY_HOOK`
- `RENDER_DEV_ADMIN_DEPLOY_HOOK`

The workflow already reads these three (`.github/workflows/deploy-dev.yml`). It does **not** know
about the worker yet — that is a Phase B change (B9). Until then, redeploy the worker manually when
worker code changes.

### A9 [BOTH] Preview smoke test (the gate)

Do this in a private window, on the `onrender.com` URLs. Tick every line.

**API and proxy**

- [ ] `https://<api-dev>.onrender.com/v1/health` → `{"status":"ok","app_env":"dev",...}`
- [ ] `https://<web-dev>.onrender.com/api/v1/health` → the **same JSON** (proves the rewrite proxy).
- [ ] `POST https://<web-dev>.onrender.com/api/v1/auth/login` with a real account returns 200 and
      `Set-Cookie: nv_refresh=...; Path=/; Secure; HttpOnly; SameSite=lax` plus `nv_csrf=...`.
- [ ] Reload the page: the session survives (refresh cookie rotates once, no 401 loop).
- [ ] Sign out, sign in as the other account: no data from the first account appears.
- [ ] A write (e.g. save a practice answer) succeeds — this proves `X-CSRF-Token` is read from the
      proxied cookie and POST bodies survive the proxy.
- [ ] Response headers for `/api/v1/me` include `cache-control: no-store` (or at least no shared
      cache header). If the CDN caches authenticated GETs, stop: switch to the fallback proxy in A5.

**Student app** (the point of B13/B14 and the journey screens)

- [ ] Landing → Sign up → Login → Onboarding → Home.
- [ ] Academia dashboard: five questions answered, one next action with a reason.
- [ ] Campus, Materials, Material reader, Ask Nelavista (degrades honestly with no API key), CBT.
- [ ] Skills → Skill detail → Path → Lesson → Practice (answer, reload, answer restored: B6).
- [ ] Verification → Assessment sitting → Attempt review → Transcript.
- [ ] Practice task → submit → Verification prompt / re-verification state (B7).
- [ ] Opportunities → detail → Work → Assignment → submit (retry once; one submission).
- [ ] Earnings / ledger (flag on), Talent profile, Shared profile link, Settings (notifications,
      languages, availability, delete account).
- [ ] PWA: install prompt, offline shell, deep-link reload (e.g. `/skills/...` served by rewrite 2).
- [ ] Email link lands on `/auth/verify?token=...` and confirms (needs SMTP; otherwise defer).

**Admin app**

- [ ] Login as `super_admin`; the 2FA enrolment screen appears before any ops screen.
- [ ] Enrol TOTP, save recovery codes, sign out, sign in with the code.
- [ ] Users, Imports (dry-run), Opportunities, Work, Review, Money, Content, Platform, Security, Audit.
- [ ] Platform: change a policy value (e.g. payout threshold), save, reload; the change persists and
      an audit row exists. Change it back.
- [ ] A student account is refused by the admin app.

**Sign-off**

- [ ] You have clicked through the student journey and the admin journey yourself.
- [ ] No 5xx in the Render API logs during the run.
- [ ] Write the date and any exceptions at the bottom of this file.

---

## 3. Phase B — Engineering hardening before the public switch

These are small, feature-flagged PRs. Each has a test. None changes V1.

| # | Gap | Fix | Files |
|---|---|---|---|
| B0 | Root-level Alembic resolves V1's migrations (fixed in #14) | `script_location = %(here)s/migrations`, `prepend_sys_path = %(here)s`. Test: from the repo root, `heads` prints `20261022_1000 (head)` and `upgrade head` runs V2's migrations on a blank DB. | `apps/api/alembic.ini` |
| B1 | Fresh DB has no roles — **done** | `migrations/versions/20261022_1000_seed_roles.py` inserts the six roles idempotently (SQLite + Postgres, offline-safe). Test: upgrade a blank DB and assert the six codes; downgrade is a no-op so reference data is never deleted. | `migrations/versions/20261022_1000_seed_roles.py`, `tests/test_migrations.py` |
| B2 | No first admin — **done** | `tools/create_staff.py --email ... --role super_admin` / `--role ops_admin` (prod-guarded, audited, idempotent, email-verifying). It never creates a password: sign up first. | `tools/create_staff.py`, `tests/test_create_staff.py` |
| B3 | SMTP cannot authenticate — **done** | `EMAIL_PROVIDER=sendhiiv` posts to Sendhiiv's HTTP API (`Authorization: Bearer`; 202 = queued). Retry policy follows the provider: only HTTP 429 rate limits are retried; 4xx and 5xx/transport failures are permanent (a 5xx may already be queued). `EMAIL_REDIRECT_TO` funnels non-prod mail to one inbox. SMTP AUTH (`MAIL_USERNAME`/`MAIL_PASSWORD`, port 587 + STARTTLS, 465 implicit TLS) is the fallback. | `app/core/config.py`, `app/worker/tasks.py`, `app/worker/errors.py`, `app/worker/runner.py`, `tests/test_email_transport.py` |
| B4 | No prod content path | (a) `tools/export_v1.py` that reads V1 **read-only** and writes the importer's JSON shape; (b) `tools/seed_curriculum.py` that runs `app/seed/curriculum.py` for a named department **without** fake students. Both prod-guarded. | `tools/`, `app/seed/curriculum.py` |
| B5 | Local disk storage is ephemeral | Production uses `STORAGE_BACKEND=cloudinary` + `CLOUDINARY_URL`; verify an upload survives a redeploy. | env only |
| B6 | PWA caches authenticated API GETs and never clears on logout | Narrow `runtimeCaching` to catalog/course/material metadata only (exclude `/money/`, `/work/`, `/talent/`, `/me`, `/verification/`), and clear the `nv-api` cache on logout and on sign-in. Test: sign in A, load work, sign out, go offline, confirm A's work is not served. | `apps/web/vite.config.ts`, `apps/web/src/lib/session.tsx` |
| B7 | No `robots.txt`, `sitemap.xml`, or Search Console file in the web build | Copy `google76268f26b118dad1.html` into `apps/web/public/`; add `robots.txt` (allow + sitemap) and a static `sitemap.xml` for the public pages. Dev stays `noindex` via header. | `apps/web/public/` |
| B8 | Sentry is configured but the SDK is not a dependency | Add `sentry-sdk[fastapi]` (lock it) or accept no error tracking. Test: a forced error appears in Sentry dev. | `apps/api/pyproject.toml`, `uv.lock` |
| B9 | Worker deploy hook missing from CI | Add `RENDER_DEV_WORKER_DEPLOY_HOOK` and `RENDER_PROD_WORKER_DEPLOY_HOOK` to the workflows and GitHub secrets. | `.github/workflows/deploy-*.yml` |
| B10 | Web security headers not set for the static sites | Add HSTS, `X-Frame-Options: DENY`, `Permissions-Policy`, and a CSP that allows the PWA's own assets and the API origin only. Do it as Render header rules or `<meta>` + a tested policy. | Render settings / `index.html` |
| B11 | API responses have no explicit cache policy | Add `Cache-Control: no-store` to authenticated API responses (middleware or dependency), so a proxy/CDN cannot serve one student's data to another. | `app/core/`, `app/main.py` |
| B12 | Mobile placeholders | Real EAS project ID and `updates.url` in `apps/mobile/app.config.js`; store URLs in `packages/config/versions.json`; real artwork/screenshots. Only needed if mobile ships at launch. | `apps/mobile/app.config.js`, `packages/config/versions.json`, `apps/mobile/` |

Also decide, per environment, the **flag matrix**. With every flag off, the matching journeys 404 by
design. For the public launch, turn on the journeys you are actually launching; leave external
opportunities off until there are partners to fill them.

---

## 4. Phase C — Put V1 on `v1.nelavista.com` (T‑7 days, no apex traffic change)

This is the "V1 gets its own domain" step. V1 keeps working at `nelavista.com` throughout.

### C1 [YOU] Lower DNS TTL

- Namecheap → Advanced DNS: set the `@` A record and the `www` CNAME TTL to **1 minute**.
- Do this at least one old-TTL period before the cutover (a week is comfortable).

### C2 [YOU] Add the `v1` hostname to Render and DNS

1. Render → V1 service → Settings → Custom Domains → **Add** `v1.nelavista.com`.
2. Namecheap → Advanced DNS → add `CNAME v1 → <v1-service>.onrender.com`, TTL 1 minute.
3. Wait for Render to verify and issue TLS.
4. Visit `https://v1.nelavista.com` — the V1 site must load.

### C3 [ENG + YOU] Make V1 fully work on the new host

- [ ] V1 Render env: add `https://v1.nelavista.com` to `SOCKETIO_CORS_ORIGINS` (comma-separated;
      keep the existing apex entry for now). Redeploy/restart.
- [ ] Google Cloud Console → the V1 OAuth client → **Authorized redirect URIs** → add
      `https://v1.nelavista.com/auth/google/callback` **in addition to** the existing
      `https://nelavista.com/auth/google/callback`. Do not remove the old one yet.
- [ ] Verify on `v1.nelavista.com`: password login, Google login, email verification/reset links,
      materials, realtime (Socket.IO) features, PWA install.
- [ ] Take a fresh V1 database backup (`pg_dump`), even though no schema change is planned.

**Do not remove** the apex domains from V1 yet. That is Phase E.

---

## 5. Phase D — Provision V2 PROD (T‑5 to T‑1, no public traffic)

Repeat Phase A with the prod names and values. Nothing here touches DNS for the apex.

### D1 [YOU] Create the PROD services

| Service | Name | Type | Branch |
|---|---|---|---|
| Database | `nelavista-db` | Postgres 16 | — |
| API | `nelavista-api` | Web Service (paid) | `main` |
| Worker | `nelavista-worker` | Background Worker (paid) | `main` |
| Web | `nelavista-web` | Static Site | `main` |
| Admin | `nelavista-admin` | Static Site | `main` |

Use the same build/start/publish commands as A3–A6. The **only** differences are the environment
values below and the fact that `main` is the deploy branch. First promote the merged V2 work:
open a PR `develop` → `main`, wait for CI, approve the `production` environment, and merge. Until
that happens, `main` does not contain V2.

Also, in GitHub → Settings → Secrets and variables → Actions, add the prod deploy hooks:
`RENDER_PROD_API_DEPLOY_HOOK`, `RENDER_PROD_WEB_DEPLOY_HOOK`, `RENDER_PROD_ADMIN_DEPLOY_HOOK`
(and `RENDER_PROD_WORKER_DEPLOY_HOOK` once B9 ships). Confirm the `production` environment still has
`@hiipraise` as its required reviewer.

**PROD API/worker environment** (Environment Group `nelavista-prod`):

```text
APP_ENV=prod
API_VERSION=v1
SECRET_KEY=<a different, long random value from dev>
DATABASE_URL=<PROD Postgres INTERNAL URL>
CORS_ORIGINS=https://nelavista.com,https://www.nelavista.com,https://admin.nelavista.com
WEB_BASE_URL=https://nelavista.com
MAIL_FROM=no-reply@nelavista.com
EMAIL_PROVIDER=sendhiiv
SENDHIIV_API_KEY=sh_live_...
SENDHIIV_FROM=no-reply@nelavista.com
STORAGE_BACKEND=cloudinary
CLOUDINARY_URL=<prod folder/credentials>
OPENROUTER_API_KEY=<prod key>
OPENROUTER_MODEL=openai/gpt-4o-mini
SENTRY_DSN=<prod project>
POSTHOG_API_KEY=<prod project>
GOOGLE_CLIENT_ID=<prod mobile client>
GOOGLE_CLIENT_SECRET=<prod mobile secret>
PUSH_ENDPOINT=https://exp.host/--/api/v2/push/send
FLAG_SKILLS_JOURNEY=1
FLAG_MANAGED_WORKFORCE=1
FLAG_LEDGER=1
FLAG_ACADEMIA_CONNECT=1
FLAG_TALENT_PROFILE=1
FLAG_EXTERNAL_OPPORTUNITIES=0
```

`CORS_ORIGINS` is belt-and-braces: the web/admin talk to the API through their own `/api` rewrite,
so the browser never makes a cross-origin request. Keep it exact anyway.

### D2 [YOU] Add the non-apex custom domains now

These do not conflict with V1 and can be live before cutover:

- `api.nelavista.com` → `nelavista-api`
- `admin.nelavista.com` → `nelavista-admin`
- `dev.nelavista.com` → `nelavista-web-dev` (after you decide on gating)
- `api-dev.nelavista.com` → `nelavista-api-dev`
- `admin-dev.nelavista.com` → `nelavista-admin-dev`

Namecheap: `CNAME` each host to the service's `onrender.com` hostname, TTL 1 minute. Remove any
`AAAA` records for these hosts. Let Render verify and issue TLS.

Then update the dev environment values and preview URLs from `onrender.com` to the new dev domains:
`WEB_BASE_URL`, `CORS_ORIGINS`, and the *admin* links in emails/tests. The static-site rewrite
destination is still the API's Render host, so it does not change.

### D3 [BOTH] Migrate, seed, create staff, load content

Against the **PROD** database, from your laptop with the external URL:

1. Migrate (B0 makes this the correct V2 path from the repo root):
   ```powershell
   $env:APP_ENV = "prod"
   $env:DATABASE_URL = "<PROD Postgres EXTERNAL URL>"
   $env:SECRET_KEY = "<the same SECRET_KEY the PROD API will use>"
   apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini upgrade head
   apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini heads   # exactly one
   ```
2. Seed roles (after B1).
3. Create two staff accounts (after B2): one `super_admin`, one `ops_admin`; both enrol TOTP.
4. Import content:
   - Export V1 read-only (after B4a).
   - Admin → Imports → **dry run** → review counts → **apply**.
   - Run the curriculum-only seed for the real department (after B4b).
5. Do **not** run `tools/seed_local.py` against PROD. It creates fake students and a fake university.

### D4 [BOTH] Verify PROD before DNS

Use the V2 web service's `onrender.com` URL with the prod config:

- [ ] `/api/v1/health` through the web origin returns `app_env: prod`.
- [ ] Signup → verify email → login; cookies are `Secure`, the CSRF write works.
- [ ] Admin login + 2FA; Platform settings load; payout policy is NGN and ₦50,000.
- [ ] Cloudinary upload survives a redeploy.
- [ ] Sentry receives a forced test error (if B8 done).
- [ ] `alembic heads` is one; a fresh backup exists.

---

## 6. Phase E — Cutover (T‑0, one 45–60 minute window)

Announce a freeze: no merges, no deploys, no seed runs. Have the V1 and V2 Render service pages open
side by side, plus the Namecheap DNS page.

### E1 [YOU] Pre-flight (15 minutes before)

- [ ] V1 is fully working at `https://v1.nelavista.com` (login, Google, materials, PWA).
- [ ] V2 prod is fully working at its `onrender.com` URL (D4 green).
- [ ] Fresh V1 and V2 Postgres backups exist.
- [ ] `@` A record is still `216.24.57.1`; TTL is 1 minute.
- [ ] You know V1's current custom domains (primary + aliases + `www`).
- [ ] Rollback is understood: reverse E2/E3. V1's database is untouched.

### E2 [YOU] Move the apex off V1

1. V1 service → Custom Domains → remove `nelavista.com` **and** `www.nelavista.com`.
   The apex now has no service for a short time. This is the expected gap.
2. **Immediately** go to the V2 web service → Custom Domains → add `nelavista.com`.
   Render will add/redirect `www.nelavista.com` with it.
3. If the Namecheap `www` CNAME points at the **V1 service host**, change it to the **V2 web
   service host** now. The apex `A` record does not change.
4. Wait for Render to verify and issue the apex TLS certificate (usually a minute or two). Refresh
   `https://nelavista.com` until it serves V2.

If Render refuses because the domain is still attached elsewhere, confirm step 1 completed on the
V1 service (including aliases), then retry.

### E3 [BOTH] Post-switch verification (the first 15 minutes)

- [ ] `https://nelavista.com` → V2 landing; `https://www.nelavista.com` → redirects to the apex.
- [ ] `https://api.nelavista.com/v1/health` → ok; `https://admin.nelavista.com` → admin login.
- [ ] `https://nelavista.com/api/v1/health` → ok (the rewrite still works on the apex).
- [ ] Sign up a real test account, verify the email, log in, reload.
- [ ] Open a course, a skill, a practice question; submit one answer; confirm it persists.
- [ ] Admin: login + 2FA; one read and one audited write.
- [ ] A V1 page at `https://v1.nelavista.com` still works; Google login there still works.
- [ ] Check the browser console: no mixed content, no CORS errors, no 404s on assets.
- [ ] Check Render logs for 5xx in the last 10 minutes.
- [ ] Check `Cache-Control`/CDN headers on an authenticated GET; confirm no shared cache.

Two expected, non-bug changes to tell users about:

- **Sessions do not carry over.** V1's session cookie is host-only and V2 uses a different cookie and
  database. Existing users sign in again at the apex. Their V1 account still works at `v1`.
- **Installed V1 PWA.** A device that installed the old app sees a stale shell until the new service
  worker takes over. Test on a browser/profile that installed V1. If it is stuck, clearing site data
  or reopening once usually fixes it; note it in the launch message rather than debugging it live.

### E4 [YOU] Rollback (only if E3 fails badly)

1. V2 web service → Custom Domains → remove `nelavista.com` and `www`.
2. V1 service → add `nelavista.com` and `www.nelavista.com` back.
3. If you changed the `www` CNAME, point it back at the V1 service host.
4. Confirm `https://nelavista.com` serves V1 again. V2 data is untouched; nothing is lost.

A TLS re-issue may add another minute. That is why the window is scheduled, not opportunistic.

---

## 7. Phase F — First 72 hours

- [ ] Search Console: add a **Domain property** for `nelavista.com` (DNS TXT verification at
      Namecheap), submit `https://nelavista.com/sitemap.xml`.
- [ ] Keep V1's apex OAuth redirect URI and CORS entry for **30 days**.
- [ ] Restore normal DNS TTLs (e.g. 1 hour) after a stable week.
- [ ] Put a banner on V1: "This is the old Nelavista. Go to nelavista.com." Decide read-only timing.
- [ ] Monitor: Render 5xx/latency, Sentry, PostHog journey events, signup→verified→onboarded funnel,
      email bounce/complaint rates.
- [ ] Confirm backups are running and do one restore test into a throwaway database.
- [ ] Tag `v1-final` and create `release/v1` (repo bookkeeping; the `apps/v1` move can wait).
- [ ] Top V1 URLs: decide redirects. Old bookmarks like `nelavista.com/course/...` now hit V2 and
      may 404. A small redirect map for the top 20 URLs is worth it.
- [ ] Mobile track separately: EAS project, real store assets/screenshots from a signed build,
      Maestro smoke, TestFlight/internal testing, then store review.

---

## 8. Namecheap DNS — the records we will end with

Use **Advanced DNS**, not a nameserver change. Keep existing MX/TXT records untouched.

| Host | Type | Value | TTL | When |
|---|---|---|---|---|
| `@` | A | `216.24.57.1` | 1 min → 1 hr | already; no change at cutover |
| `www` | CNAME | `<nelavista-web>.onrender.com` | 1 min → 1 hr | E2 (was V1's host) |
| `api` | CNAME | `<nelavista-api>.onrender.com` | 1 min | D2 |
| `admin` | CNAME | `<nelavista-admin>.onrender.com` | 1 min | D2 |
| `dev` | CNAME | `<nelavista-web-dev>.onrender.com` | 1 min | D2 |
| `api-dev` | CNAME | `<nelavista-api-dev>.onrender.com` | 1 min | D2 |
| `admin-dev` | CNAME | `<nelavista-admin-dev>.onrender.com` | 1 min | D2 |
| `v1` | CNAME | `<v1-service>.onrender.com` | 1 min | C2 |

Also:

- Remove `AAAA` records for any host Render serves (Render is IPv4-only).
- Remove Namecheap's default `www` parking/redirect record before adding the CNAME.
- For email: keep the existing MX; add the provider's SPF (merge, do not create a second SPF TXT),
  DKIM, and a DMARC record (`v=DMARC1; p=none; rua=mailto:...` to start).
- For Search Console domain verification: add the `google-site-verification=...` TXT at `@`.

**Custom-domain budget:** this is 8 hostnames. Hobby includes 2; Pro includes 15. If you are on
Hobby, either upgrade or accept $0.25/month per extra domain. Each new hostname also needs its own
TLS certificate (Render issues it automatically).

---

## 9. Render services at a glance

| Env | Service | Type | Branch | Notes |
|---|---|---|---|---|
| dev | `nelavista-db-dev` | Postgres 16 | — | separate from prod, seeded fake data |
| dev | `nelavista-api-dev` | Web Service | `develop` | health `/v1/health` |
| dev | `nelavista-worker-dev` | Background Worker | `develop` | drains jobs/email |
| dev | `nelavista-web-dev` | Static Site | `develop` | `/api/*` rewrite |
| dev | `nelavista-admin-dev` | Static Site | `develop` | `/api/*` rewrite, noindex |
| prod | `nelavista-db` | Postgres 16 | — | real data, backups |
| prod | `nelavista-api` | Web Service | `main` | health `/v1/health` |
| prod | `nelavista-worker` | Background Worker | `main` | must run or email never sends |
| prod | `nelavista-web` | Static Site | `main` | apex + www |
| prod | `nelavista-admin` | Static Site | `main` | admin only, noindex |

The V1 service stays exactly as it is, with `v1.nelavista.com` added in Phase C.

---

## 10. What I need from you (short list)

1. Confirm Render workspace plan/region, and whether you can give me dashboard access or will paste
   the service URLs and deploy-hook names.
2. Pick the email provider and create an API key (Resend/Brevo/SendGrid).
3. Send the current Namecheap Advanced DNS screenshot and V1's custom-domain list.
4. Say **yes/no** to importing V1 users before cutover.
5. Say **web-first** or **mobile at launch**.
6. Give me two staff email addresses for the admin accounts.
7. Confirm you can edit Google Cloud OAuth redirect URIs (for V1 at `v1`).
8. If mobile: Apple/Google developer accounts + EAS access.

## 11. What I will do next (on your go)

In this order, as separate small PRs, each with tests:

1. B1 roles migration + B2 `create_staff` tool.
2. B3 SMTP auth.
3. B4 V1 export + curriculum-only seed.
4. B5–B11 (storage, PWA cache privacy/logout, SEO files, Sentry, worker hooks, headers, no-store).
5. A short `docs/runbooks/deploy-to-dev.md` update with the exact Render settings above, so the
   next environment is one page, not tribal knowledge.

---

## Sign-off log

| Date | What was verified | By | Exceptions |
|---|---|---|---|
| | DEV preview smoke (A9) | | |
| | V1 at `v1.nelavista.com` (C3) | | |
| | PROD pre-DNS (D4) | | |
| | Cutover (E3) | | |
