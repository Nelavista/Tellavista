# V2 launch — the simple plan

**What this is:** V2 is built. This plan puts it on Render, brings V1's people and
content across, checks it on a Render URL, then moves `nelavista.com` from V1 to V2.

**Not in this plan:** the mobile app, Sentry, a DEV preview, or `dev` subdomains.
They are not needed for this launch.

**Already done:** V1 is live at `https://v1.nelavista.com`; V2 builds and its tests
pass; the database schema, roles, staff tool, email transport, PWA cache fix,
robots/sitemap, no-store API headers, worker deploy hooks, V1 exporter and
curriculum seeder are in the repo. The rest is deployment and data.

If you only want to see V2 on your own machine first, follow **`RUN-LOCALLY.md`**
and come back here when it runs.

---

## The seven steps

| # | Who      | Step                                                           |
| - | -------- | -------------------------------------------------------------- |
| 1 | Me + you | Merge `develop` into `main` (the code that Render deploys) |
| 2 | You      | Create the PROD services and data stores on Render             |
| 3 | You      | Prepare the PROD database                                      |
| 4 | You      | Create the two staff accounts                                  |
| 5 | You      | Export V1, import it, seed the curriculum                      |
| 6 | You      | Check V2 on its `onrender.com` URLs                          |
| 7 | You      | Move `nelavista.com` to V2                                   |

Do them in this order. Steps 1 and 2 can happen on the same day; step 7 is the only
one users will notice.

---

## 1. Merge `develop` into `main`

I open the PR, CI runs, and you approve the `production` environment if GitHub asks.
Merge with a merge commit. Render deploys `main`; `develop` stops being the source
of truth at that point.

Do not create a release tag or change V1.

---

## 2. Create the PROD services and data stores on Render

Use the **same region** for everything. Choose paid instances: Render's free web
services spin down and free Postgres expires. No `render.yaml` is used; create
everything in the dashboard.

| Service              | Render type                | Branch   | Build command                                                                                 | Start command                                                                                                    |
| -------------------- | -------------------------- | -------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `nelavista-db`     | Postgres                   | —       | —                                                                                            | —                                                                                                               |
| `nelavista-redis`  | Key Value                  | —       | —                                                                                            | —                                                                                                               |
| `nelavista-api`    | Web Service (Python)       | `main` | `pip install uv && uv sync --frozen --no-dev --all-packages`                                | `uv run --no-sync --package nelavista-api uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir apps/api` |
| `nelavista-worker` | Background Worker (Python) | `main` | same as API                                                                                   | `cd apps/api && uv run --no-sync --package nelavista-api python -m app.worker`                                 |
| `nelavista-web`    | Static Site                | `main` | `corepack enable && pnpm install --frozen-lockfile && pnpm --filter @nelavista/web build`   | — (publish `apps/web/dist`)                                                                                   |
| `nelavista-admin`  | Static Site                | `main` | `corepack enable && pnpm install --frozen-lockfile && pnpm --filter @nelavista/admin build` | — (publish `apps/admin/dist`)                                                                                 |

That is four application services plus Postgres and Redis.

Generate the API secret once, in your terminal:

```powershell
apps\api\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

**API and worker environment** (copy the same values into both):

```dotenv
APP_ENV=prod
API_VERSION=v1
PYTHON_VERSION=3.11
SECRET_KEY=<the value from the command above>
DATABASE_URL=<Render Postgres INTERNAL URL>
REDIS_URL=<Render Key Value INTERNAL URL>
CORS_ORIGINS=https://nelavista.com,https://www.nelavista.com,https://admin.nelavista.com
WEB_BASE_URL=https://nelavista.com
MAIL_FROM=no-reply@nelavista.com

EMAIL_PROVIDER=sendhiiv
SENDHIIV_API_KEY=<your live Sendhiiv key>
SENDHIIV_FROM=
# Leave SENDHIIV_FROM empty until Sendhiiv verifies nelavista.com. The shared
# sender works meanwhile, but mail is more likely to land in spam.

FLAG_SKILLS_JOURNEY=1
FLAG_MANAGED_WORKFORCE=1
FLAG_LEDGER=1
FLAG_ACADEMIA_CONNECT=1
FLAG_TALENT_PROFILE=1
FLAG_EXTERNAL_OPPORTUNITIES=0
```

Optional, leave empty if you do not have them: `OPENROUTER_API_KEY`,
`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `POSTHOG_API_KEY`.

On the two static sites, set `NODE_VERSION=20` if Render does not read `.nvmrc` automatically.

**API health check path:** `/v1/health`.

**Static site rewrites** (both web and admin, in this order). Open the static
site → **Settings** → **Redirects/Rewrites** → **Add Rule**:

| Source     | Destination                              | Action            |
| ---------- | ---------------------------------------- | ----------------- |
| `/api/*` | `https://nelavista-api.onrender.com/*` | **Rewrite** |
| `/*`     | `/index.html`                          | **Rewrite** |

The first rule is the proxy that keeps the login cookie on the same origin. Do not
use a Redirect. Use the exact API host Render shows (it may have a suffix such as
`nelavista-api-a1b2.onrender.com`). If Render's rewrite ever drops a POST body or
`Set-Cookie`, tell me and we replace it with a tiny proxy service; do not switch the
frontends to a different API hostname.

**Static site headers** (open the static site → **Settings** → **Headers** → **Add
Header**, path `/*`):

| Header                        | Value                                                                                                                                                                                                                                                    |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains`                                                                                                                                                                                                                  |
| `X-Frame-Options`           | `DENY`                                                                                                                                                                                                                                                 |
| `X-Content-Type-Options`    | `nosniff`                                                                                                                                                                                                                                              |
| `Referrer-Policy`           | `strict-origin-when-cross-origin`                                                                                                                                                                                                                      |
| `Permissions-Policy`        | `camera=(), microphone=(), geolocation=()`                                                                                                                                                                                                             |
| `Content-Security-Policy`   | `default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; font-src 'self' data:; manifest-src 'self'; worker-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'` |

Add `X-Robots-Tag: noindex` to **admin only**. Never add it to the student web app.

**Custom domains now (before cutover):**

- `api.nelavista.com` → `nelavista-api`
- `admin.nelavista.com` → `nelavista-admin`

Do **not** add `nelavista.com` or `www.nelavista.com` to V2 yet. They still belong
to V1 until step 7.

---

## 3. Prepare the PROD database

Use the **external** database URL for this terminal only. Never commit it.

```powershell
$env:APP_ENV = "prod"
$env:DATABASE_URL = "<PROD Postgres EXTERNAL URL>"
$env:SECRET_KEY = "<any non-empty value for the CLI>"
$env:PRODGUARD_ALLOW = "1"

apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini upgrade head
apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini heads
```

`heads` must print exactly one head: `20261022_1000 (head)`. If it prints more than
one, stop and tell me.

Do **not** run `tools.seed_local` against this database. It creates fake students.

---

## 4. Create the two staff accounts

1. Sign up normally at `https://nelavista-web.onrender.com` with
   `info.praisechinedu@gmail.com` and `tellaafeezadewale@gmail.com`. Use a real
   password you control.
2. Promote them against the PROD database:

```powershell
# Same shell as step 3, still pointed at the PROD external URL.
apps\api\.venv\Scripts\python.exe -m tools.create_staff `
  --email info.praisechinedu@gmail.com --role super_admin

apps\api\.venv\Scripts\python.exe -m tools.create_staff `
  --email tellaafeezadewale@gmail.com --role ops_admin
```

The tool verifies the email, grants the role, and writes an audit row. It never
creates or prints a password. Re-running it is safe.

Why two: payouts of ₦50,000.00 or more need a second approver. A single account
cannot approve its own payout, and `super_admin` is the only role that can change
platform policy.

---

## 5. Bring V1's content and people across

### 5.1 Export V1 (read-only)

In Render: open the **V1 Postgres** database → **Connections** → copy the
**External Database URL**. Keep it in your terminal; do not paste it in chat.

```powershell
$env:V1_DATABASE_URL = "<V1 external Postgres URL>"
$env:PRODGUARD_ALLOW = "1"

apps\api\.venv\Scripts\python.exe -m tools.export_v1 --out v1-export.json
```

The exporter only reads V1. It prints counts for users, taxonomy, materials,
questions and skills. Open the JSON and check those numbers look like your site.

V1 keeps taking new signups and uploads until the domain moves. If you verify V2
on Render before cutover day, run 5.1 and 5.2 again on cutover day so those late
rows come across. The import is idempotent, so a second run is safe.

If the V1 database is not on Render, use whatever Postgres URL V1 uses. If you
cannot get any database URL, tell me before launch: we can launch V2 with fresh
content, but V1 accounts will not carry over.

### 5.2 Import it in the admin app

1. Open `https://nelavista-admin.onrender.com` and sign in as
   `info.praisechinedu@gmail.com`.
2. Enrol 2FA when asked. Save the recovery codes.
3. Go to **Import runs** → choose `v1-export.json` → **Dry run**.
4. Read the report. Each section should say `match` (or explain what it skipped).
5. Choose **Apply** and run it once.
6. After it succeeds, delete `v1-export.json` from your machine. It contains real
   student data.

The import is idempotent: running it again updates or skips, it does not duplicate.
It brings across people, taxonomy, approved materials, CBT questions and skill
lesson text. V1 enrolments, learning progress, challenges, project submissions and
lesson videos/resources do not come across; students confirm their course during
onboarding. V1 accounts that only used Google have no password and can set one
with **Forgot your password?** on the V2 login page.
Seeded PDFs that lived under V1's `/static/materials` are rewritten to
`https://v1.nelavista.com/static/...`, so keep V1 running until those files are
moved to Cloudinary.

### 5.3 Seed the curriculum

Use the real university/faculty/department that will receive the first students.

```powershell
# Still pointed at the PROD external URL.
apps\api\.venv\Scripts\python.exe -m tools.seed_curriculum `
  --university "<university name>" `
  --faculty "<faculty name>" `
  --department "<department name>"
```

That creates the AI Data Annotation skill, its path and lessons, the assessment and
the practical task, plus the AID301 course. It creates no students. Re-running is
safe.

---

## 6. Check V2 on the Render URLs

Use a private browser window. Do not use the apex yet.

**API and proxy**

- [ ] `https://nelavista-api.onrender.com/v1/health` returns `{"status":"ok",...}`.
- [ ] `https://nelavista-web.onrender.com/api/v1/health` returns the same JSON.
- [ ] Sign up at `https://nelavista-web.onrender.com`; the session survives a reload.
- [ ] A write works (save a practice answer, then reload).
- [ ] `/api/v1/me` response has `cache-control: no-store`.
- [ ] Sign out; no data from the previous account appears.

**Student app**

- [ ] Landing → Sign up → Login → Onboarding → Home.
- [ ] Academia, Materials, Material reader, CBT.
- [ ] Skills → Path → Lesson → Practice; reload restores the answer.
- [ ] Verification → Assessment → Attempt review → Transcript.
- [ ] Opportunities → Work → Assignment → submit once.
- [ ] Earnings, Talent profile, Settings.
- [ ] Install the PWA; a deep link reloads correctly.

**Admin app**

- [ ] `https://nelavista-admin.onrender.com` → login → 2FA.
- [ ] Import history shows your run and its report.
- [ ] Users, Opportunities, Work, Review, Money, Content, Platform, Security, Audit.
- [ ] Change one policy value, save, reload; the audit row exists. Change it back.
- [ ] A student account is refused.

**Logs**

- [ ] No 5xx in the API or worker logs during the whole run.

Email links use `WEB_BASE_URL`. While verifying before cutover, set it to
`https://nelavista-web.onrender.com` on both the API and worker, then redeploy.
Otherwise verification and password-reset links open V1 at `nelavista.com` and
return 404. Change it back to `https://nelavista.com` in step 7.

---

## 7. Move the domain

### Before the window

- [ ] Lower the Namecheap TTL on `@` and `www` to 5 minutes at least 24 hours ahead.
- [ ] Re-run 5.1 and 5.2 if V1 has taken any signups or uploads since the last import.
- [ ] Set `WEB_BASE_URL=https://nelavista.com` on both the V2 API and worker, then
      redeploy them.
- [ ] `https://v1.nelavista.com` still loads and you can log in. If Google login
  fails, add `https://v1.nelavista.com/auth/google/callback` (or the redirect
  URI V1 prints) in Google Cloud.
- [ ] Keep this page open. The rollback is at the bottom.

### The switch (10–15 minutes)

1. V1 service → **Custom Domains** → remove `nelavista.com` **and**
   `www.nelavista.com`. A short gap is expected.
2. Immediately: V2 **web** service → **Custom Domains** → add `nelavista.com`.
   Render adds `www.nelavista.com` with it.
3. In Namecheap, change the `www` CNAME target from the V1 host to the V2 web host
   Render shows. The apex `A` record stays `216.24.57.1`.
4. Wait for Render to verify and issue the apex certificate. Refresh
   `https://nelavista.com` until V2 loads.

### Verify

- [ ] `https://nelavista.com` → V2 landing.
- [ ] `https://www.nelavista.com` → redirects to the apex.
- [ ] `https://api.nelavista.com/v1/health` → ok.
- [ ] `https://admin.nelavista.com` → admin login.
- [ ] `https://nelavista.com/api/v1/health` → ok.
- [ ] Sign in, reload, and complete one write on the real domain.
- [ ] A verification email link opens the V2 verify page.

### Rollback (if V2 is broken)

1. V2 web → Custom Domains → remove `nelavista.com` and `www.nelavista.com`.
2. V1 service → Custom Domains → add `nelavista.com` and `www.nelavista.com` back.
3. Point the `www` CNAME back at the V1 host.
4. Wait for TLS, then confirm `https://nelavista.com` is V1 again.

Keep the V1 service and database running for at least 30 days after cutover. Do not
delete anything on the V1 side during the launch window.

---

## DNS summary (Namecheap)

| Host      | Type  | Value                     | When                                             |
| --------- | ----- | ------------------------- | ------------------------------------------------ |
| `@`     | A     | `216.24.57.1`           | unchanged; Render switches which service owns it |
| `www`   | CNAME | V2 web host from Render   | at cutover                                       |
| `api`   | CNAME | V2 API host from Render   | now                                              |
| `admin` | CNAME | V2 admin host from Render | now                                              |
| `v1`    | CNAME | V1 host from Render       | already done                                     |

Only these records. Do not add `dev`, `api-dev` or `admin-dev`.

---

## After launch (first week)

- [ ] Render Postgres backups are on; do one restore drill using
  `docs/runbooks/restore-from-backup.md`.
- [ ] Add `nelavista.com` to Google Search Console and submit `/sitemap.xml`.
- [ ] Check the API and worker logs once a day for 5xx or failed jobs.
- [ ] Rotate the Sendhiiv key and Render/GitHub secrets if anyone else saw them.
- [ ] Leave V1 at `v1.nelavista.com` and keep its rollback path for 30 days.
  Keep it longer if imported PDFs still point at `v1.nelavista.com/static/...`.
  Do not share the `v1` URL with students after cutover; it is for rollback only.

## Sign-off

- Date:
- Cutover by:
- Exceptions:
