# Nelavista V1 — Phase 0 Audit

**Status:** read-only audit. **No files were changed to produce this** (verified with `git status --porcelain` — clean). No scripts were run against any database. No dependencies were upgraded.
**Date:** 2026-10-16
**Scope:** audit the current codebase and deployment so V2 can be planned without breaking live V1.
**Method:** direct inspection of the working tree, `git` metadata, `migrations/versions`, `app/`, `scripts/`, `tests/`, templates and static assets. Anything not directly confirmed in code is explicitly marked **[assumption]**.

> Facts below were read from the code, not from the README. Where the README disagrees, §7 lists it.

---

## 1. Real repository structure

### 1.1 Top-level (as it exists today)

| Path | Type | What it is | Belongs where (proposal) |
|---|---|---|---|
| `app/` | dir | The entire Flask app (20,309 LOC Python; 106 templates; static assets incl. LFS-tracked course files). | Keep — becomes `apps/v1/` at relocation time (§ADR-d). |
| `migrations/` | dir | Alembic env + 50 revisions under `versions/`. **Single head: `f1b2c3d4e5f6`.** | Keep with the V1 app. |
| `scripts/` | dir | `admin/`, `audit/`, `maintenance/`, `seed/`. **Nothing in `app/` imports them.** | Keep with V1; each needs a prod-guard later. |
| `tests/` | dir | 49 test modules + `conftest.py` (isolated throwaway SQLite app). | Keep with V1. |
| `docs/` | dir | `MIGRATION_MAP.md`, `SECRETS_ROTATION.md`, `TEMPLATE_CLASSIFICATION.md`, `product/Nelavista_V2_PRD.pdf`. | Becomes `docs/` at monorepo root; product docs → `docs/product/`; new audits → `docs/architecture/`. |
| `data/` | dir | 371 tracked files: 369 files in `cbt_question_banks/` (JSON/markdown question banks), `Nelavista_Course_Codes.csv`, and a file literally named `cbt questions` (953 KB UTF-8 text, **a file, not a directory**). These are *seed inputs* read by `scripts/seed/*`. | Move to `data/seed-inputs/`; rename `cbt questions` → `cbt_questions.txt`; keep tracked (seeders + CBT bank read them). |
| `seed_data/` | dir | `career_skills/` — 20 Python modules that *are* seed payload (career-skill definitions), sitting outside `scripts/seed/`. | Fold into `scripts/seed/data/career_skills/` (it is seed payload, not runtime data). |
| `uploads/` | dir | Empty, gitignored, created at boot by `create_app` (`app.config['UPLOAD_FOLDER']`). Runtime artifact. | Keep; document as ephemeral; object storage in V2. |
| `extracted_images/` | dir | Empty, gitignored, created at boot (`IMAGE_FOLDER`). Runtime artifact. | Keep; document as ephemeral. |
| `instance/` | dir | Contains `tellavista.db` (local SQLite file from the pre-rename product name). Gitignored. | Keep; runtime artifact. |
| `google76268f26b118dad1.html` | file | Google Search Console verification file (content: `google-site-verification: google76268f26b118dad1.html`). **Not served by any route and not under `app/static/` → not reachable in production today** (see §5). | Keep, but serve it deliberately (route or `static` root) on whichever host is the current property. |
| `.env` | file | Present on disk, **gitignored and NOT tracked**; contains local secrets. | Never committed; local only. |
| `.env.example` | file | Authoritative list of every env var the app reads. | Rename/expand to per-app `.env.example` files in V2. |
| `.gitattributes` | file | Declares Git LFS for `pdf/pptx/ppt/docx/doc`. | Review: media (`.mp4/.jpeg`) is **not** covered (see §8.2). |
| `.gitignore` | file | Ignores `.env`, DB files, `uploads/`, `extracted_images/`, `backups/`, `node_modules/`, `.freebuff/`, etc. | Expand for monorepo (multiple apps, multiple `.env.*`). |
| `Procfile` / `runtime.txt` | files | `web: gunicorn --worker-class eventlet -w 1 wsgi:app`; `python-3.11.9`. | Moves with the V1 app. |
| `wsgi.py` | file | Prod + local entry point (`socketio.run`, default port 5000). | Moves with V1. |
| `README.md`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini` | files | Docs + deps + test config. | Monorepo root / app root per ADR. |
| `.freebuff/` | dir | Agent session metadata, gitignored. | Leave; never commit. |

### 1.2 Repo-size reality (important, and half-true in the README)

- `app/static/materials/` — **1.2 GB working tree, 182 files**, tracked. `git cat-file -s` on a sample blob = 132 bytes and `.git/lfs/objects` is populated → **these are Git LFS objects, not raw blobs in history** (180 files listed by `git lfs ls-files`).
- `app/static/media/` — **146 MB, 20 files** (15 `.mp4`, 5 `.jpeg`). LFS filters in `.gitattributes` cover neither extension, so **[assumption]** these are ordinary blobs in history (the largest single contributor to the 1.3 GB `.git`).
- Stray tracked file: `app/static/materials/accounting/h` — 3 bytes of text. Junk from an accidental commit.
- So "≈1.2 GB of course files tracked in git" is imprecise: it is LFS-tracked content plus ~146 MB of un-LFS'd media. History-purge planning must account for the LFS store and any forks/clones.

---

## 2. Code inventory

### 2.1 App shell

- `app/__init__.py` — `create_app()`: extensions, security headers, CSP, CORS, error handlers, registers **25 blueprints**. Runs `eventlet.monkey_patch()` at import. Module-level `app = create_app()` then `init_database(app)` **unless `SKIP_DB_INIT=1`**, and `create_default_user()` (hardcoded `test`/`test123`) when `DEBUG_MODE`.
- `app/extensions.py` — `db`, `socketio` (eventlet, `cors_allowed_origins` from config), `mail`, `csrf`, `limiter` (per-user key, Redis-or-memory), `oauth`.
- `app/config.py` — env-driven. `SECRET_KEY` **required** outside debug. `DATABASE_URL` defaults to `sqlite:///tellavista.db`. `ENVIRONMENT` (production|development) exists; **`APP_ENV` does not exist anywhere** (the brief's requested variable is new).
- `app/database.py` — `init_database()`: creates the DB if missing (Postgres), runs `create_all()` + `stamp()` only when `alembic_version` is absent, then legacy `ALTER TABLE` bridges. Refuses to boot against a failed non-SQLite `DATABASE_URL` (good).
- `app/logging_config.py` — structured stdout logging; Sentry activates on `SENTRY_DSN` (env label from `ENVIRONMENT`).
- `app/events.py`, `app/community_events.py` — Socket.IO handlers (live classes, community chat), session-cookie authenticated.

### 2.2 Blueprints / routes (302 `@route` decorators across 25 modules; **124 are `/api/`**)

| Module | Routes | Class | Notes |
|---|---:|---|---|
| `skills_routes.py` | 48 | **Active (core V1 Skills)** | Learning→Build→Verify→Earn surface. |
| `admin_skills_routes.py` | 66 | Active (admin) | Admin surface for the above. |
| `admin_routes.py` | 20 | Active (admin) | Users, materials, videos, AI flags, audit. |
| `admin_academia_routes.py` | 17 | Active (admin) | University→Faculty→Department→Course→Topic CRUD. |
| `ai_routes.py` | 15 | Active | Notes, test gen, grading, project briefs, material/topic AI. **Direct OpenRouter calls.** |
| `live_meeting_routes.py` | 14 | Active but *not* in V2 Academia/Skills scope | Agora-backed live classes. |
| `community_routes.py` | 14 | Active but **out of V2 scope** | Groups/chat/events. |
| `materials_routes.py` | 12 | Active | Library, upload, view, insights. Cloudinary config inline here. |
| `cbt_routes.py` | 10 | Active | `/api/cbt/start`, submit, history. Uses `get_ai_provider()`. |
| `auth_routes.py` | 10 | Active | Password + Google OAuth, verify, reset. |
| `video_routes.py` | 9 | Active | YouTube search + uploads. |
| `tutor_routes.py` | 8 | Active | Streaming tutor (direct OpenRouter). |
| `onboarding_routes.py` | 8 | Active | Academic onboarding. |
| `academia_routes.py` | 8 | Active | Taxonomy browse + notifications. |
| `settings_routes.py` | 7 | Active | Account deletion = anonymise + deactivate. |
| `campus_map_routes.py` | 7 | Active utility | `/api/campus-map`. |
| `dashboard_routes.py` | 6 | Active | Includes `/api/debug-*` endpoints (**debug surface — must be gated/removed**). |
| `study_routes.py` | 4 | Active | Study mode. |
| `static_pages_routes.py` | 4 | Active | about / privacy / terms / mat101. |
| `employer_routes.py` | 4 | Active but out of V2 scope | Employer profiles. |
| `core_routes.py` | 4 | Active | `/health`, `/images/<file>`, cleanup stubs. |
| `reels_routes.py` | 2 | Active | Short-form video (not in README). |
| `pwa_routes.py` | 2 | Active | `/manifest.json`, icons. |
| `google_search_routes.py` | 2 | Active | Tavily-backed external material search. |
| `profile_routes.py` | 1 | Active | |
| `tech_routes.py` | — | **Deleted** (dead, per `__init__.py` comment) | |

**Dead/absent:** no `robots.txt`, no `sitemap.xml`, no `/api/v1/*` prefix, no OpenAPI schema, no token endpoints.

### 2.3 Models — `app/models.py`, 2,871 lines, **76 classes**

Grouping (all in one file — a V2 split candidate):
- **Identity/auth:** `User`, `UserQuestions`, `UserPreferences`, `StudentPrivacySettings`, `AdminAuditLog`.
- **Academia:** `University`, `Campus`, `CampusLocation`, `Faculty`, `Department`, `AcademicSession`, `Semester`, `Course`, `Topic`, `Enrollment`, `Material`, `MaterialView`, `MaterialChunk` (pgvector), `TopicProgress`, `CBTQuestion`, `CBTAttempt`, `CBTAnswer`, `StudySession`, `Exam`.
- **AI:** `TutorConversation`, `TutorMessage`, `AIUsageLog`, `FlaggedAIAnswer`, `AnalyzerSession`, `GradingEvent`, `GoogleSearchCache`.
- **Skills:** `SkillCategory`, `Skill`, `LearningPath`, `LearningPathStep`, `SkillCourse`, `CourseModule`, `Lesson`, `Quiz`, `StudentQuizAttempt`, `Challenge`, `ChallengeSubmission`, `ProjectTemplate`, `StudentProject`, `ProjectMilestone`, `ProjectFile`, `ProjectMessage`, `StudentSkill`, `StudentLessonProgress`, `StudentOnboarding`, `CareerTrack`, `CareerTrackStep`.
- **Work/money (V2-relevant, partial today):** `Opportunity`, `OpportunityApplication`, `OpportunityStatusEvent`, `Rating`, `Competition`, `CompetitionEntry`, `Cohort`, `CohortEnrollment`, `EmployerProfile`, `GradeScale`, `GradeWeight`, `Assignment`, `AssignmentSubmission`.
- **Messaging/notifications:** `MessageThread`, `Message`, `Notification`.
- **Community/live:** `Group`, `GroupMember`, `GroupMessage`, `GroupFile`, `GroupEvent`, `GroupInvite`, `Room`, `Video`.

### 2.4 Services — `app/services/`, 6,121 LOC, 25 modules

Active & strategically valuable: `ai_provider.py` (the abstraction), `rag_service.py` (**real RAG**: chunking + embeddings + pgvector cosine, honest-decline gate), `ai_service.py`, `tutor_service.py`, `ai_grading.py`, `material_service.py` (PDF extraction + cache), `search_service.py` (Postgres FTS + ILIKE fallback), `cbt_bank.py`, `insights_service.py`, `progress_service.py`, `skills_service.py`, `notification_service.py`, `messaging_service.py`, `analytics.py` (PostHog), `gpa_service.py`, `onboarding_service.py`, `academic_context.py`, `campus`/`opportunity`/`daily_class`/`meeting` services.

**Abstraction not finished:** `ai_provider.py` is used by `cbt_routes.py` and `ai_grading.py`, but **23 direct `openrouter.ai/api` call sites** remain (`ai_service.py` ×13+, `tutor_service.py`, `ai_routes.py`). This is the single biggest "carry forward the interface, finish the migration" item.

### 2.5 Templates — 106 `.html` (91 top-level + 15 in `components/`)

`components/` holds shared chrome (`navbar`, `footer`, `*_sidebar`, workspace partials). Two parallel shells (Academia vs Skills). `offline.html` and `error.html`: **`error.html` is used by the 404/500/503 handlers; `offline.html` is referenced by no Python → dead** (contradicts README).

---

## 3. Deployment reality

| Item | Reality |
|---|---|
| Host | Render ([assumption — no `render.yaml`/`render.json` in repo], so the service is configured **in the Render dashboard**, not in code). |
| Start command | `Procfile` → `gunicorn --worker-class eventlet -w 1 wsgi:app`. README warns the dashboard start command (if set) overrides `Procfile`. |
| Runtime | `runtime.txt` → `python-3.11.9`. |
| Workers | **1 eventlet worker, deliberately.** Real-time room/participant state lives in process memory (`meeting_service.py`) with no shared queue until `REDIS_URL` is set. `socketio.init_app(message_queue=REDIS_URL)`. |
| Migrations | `flask db upgrade` run manually after deploy; `SKIP_DB_INIT=1` must be set for migration runs. 50 revisions, **single head `f1b2c3d4e5f6`**. |
| CI/CD | **None.** No `.github/` directory exists — no lint, no tests, no migration check, no automation on push. |
| DB | Postgres on Render (prod); SQLite `tellavista.db` for local/test. `pool_pre_ping=True`. |
| `pgvector` | Enabled by migration (`CREATE EXTENSION IF NOT EXISTS vector`); Render Postgres 13+ has it. |

**Env var NAMES the app reads** (names only — values are never printed):
`FLASK_DEBUG`, `SECRET_KEY`, `PORT`, `ENVIRONMENT`, `DATABASE_URL`, `SKIP_DB_INIT`, `REDIS_URL`, `SUPPORT_EMAIL`, `SOCIAL_FACEBOOK_URL`, `SOCIAL_WHATSAPP_URL`, `SOCIAL_TIKTOK_URL`, `SOCIAL_TELEGRAM_URL`, `SOCKETIO_CORS_ORIGINS`, `SESSION_COOKIE_SECURE`, `PERMANENT_SESSION_LIFETIME_DAYS`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`, `OPENROUTER_API_KEY`, `YOUTUBE_API_KEY`, `YOUTUBE_API_KEY_2`, `GITHUB_TOKEN`, `TAVILY_API_KEY`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`, `AGORA_APP_ID`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `SENTRY_DSN`, `SENTRY_TRACES_SAMPLE_RATE`, `POSTHOG_API_KEY`, `POSTHOG_HOST`.

**Third-party integrations:** Render (host+DB), OpenRouter (AI), Tavily (external material search), Cloudinary (file storage — configured **inside two route modules**, not central config), Gmail/SMTP (Flask-Mail), Google OAuth (Authlib), Agora (live meetings), YouTube Data API, GitHub REST (project review), Sentry, PostHog, and pgvector/Postgres FTS internally.

---

## 4. Environment reality (LOCAL / STAGING / PROD today)

**There is no DEV/staging environment and no environment separation of any kind.**

- **One config path.** `app/config.py` + a single `.env` (or the host's env vars). The only branch is `DEBUG_MODE` (`FLASK_DEBUG`) and the unused-ish `ENVIRONMENT` label. There is no `APP_ENV`, no per-environment settings module, no startup validation beyond `SECRET_KEY`.
- **Which DB each setup points at:** whatever `DATABASE_URL` resolves to — a single value per machine/host. Unset → `sqlite:///tellavista.db`. Tests are the only thing that forces its own DB (`conftest.py` sets `SKIP_DB_INIT=1` and binds a temp SQLite).
- **Shared prod assets today:** with no staging, there is exactly one set of everything. **[assumption, to confirm]** prod's Google OAuth client, Cloudinary account, mail sender, Sentry project and PostHog project are the only ones — and a developer's local `.env` may point some of these at the *same* accounts as prod. This is the core risk the DEV environment removes.
- **Scripts that could damage prod (no guard exists):** every `scripts/seed/*` (idempotent but write to `DATABASE_URL`), `scripts/maintenance/*` (notably `cleanup_unembeddable_materials.py`, which **defaults to making changes**, and `migrate_static_materials_to_cloudinary.py`, which mutates rows + Cloudinary), `scripts/admin/make_admin.py`, and `scripts/audit/audit_broken_material_links.py --apply`. **Only `scripts/audit/check_template_links.py` sets `SKIP_DB_INIT`.** Every other script imports the app, so importing triggers `init_database()` (create_all/stamp + `ALTER TABLE` attempts) against the configured DB before the script does anything.
- **The hardcoded `test`/`test123` account** is created whenever `DEBUG_MODE` is on and `init_database` runs without `SKIP_DB_INIT` — i.e. a `pytest` run before the conftest fix, or any debug boot against a shared DB. `MIGRATION_MAP.md` records this as having opened a real prod connection once. **Action for Phase 3: check prod for a `test` user.**

---

## 5. Domain dependencies (everything tied to the current host)

| Dependency | Where | Impact of moving `nelavista.com` → `v1.nelavista.com` |
|---|---|---|
| **Session cookies** | `SESSION_COOKIE_SECURE`, `_HTTPONLY`, `_SAMESITE='Lax'`; **`SESSION_COOKIE_DOMAIN` is not set → host-only cookies** (positive: no cross-subdomain bleed). | Safe: host-only cookies mean v1 and v2 cannot clobber each other. Moving host **logs everyone out** (expected). Do **not** set a `.nelavista.com` domain cookie unless deliberate. |
| **Google OAuth redirect URI** | `auth_routes.py:289` — `url_for('auth.google_callback', _external=True)`; `ProxyFix(x_proto=1)` trusts Render's `X-Forwarded-Proto`, so the URI follows the request Host. | **Manual, blocking.** Add `https://v1.nelavista.com/auth/google/callback` in Google Cloud Console; keep `nelavista.com` during transition. Mismatch → `redirect_uri_mismatch`. |
| **Email absolute URLs** | `verify_link = f"{request.host_url}verify-email?token=…"`; reset link the same. | Good: derived from Host, no hardcoded domain. Risk is only in-flight emails around the swap. |
| **CORS** | `add_cors_headers` allowlist = `SOCKETIO_CORS_ORIGINS` (default only `https://nelavista.com`). | **Blocking.** Must add the new origin or same-origin XHR/fetch and cross-origin calls break. |
| **Socket.IO origins** | `socketio = SocketIO(cors_allowed_origins=SOCKETIO_CORS_ORIGINS)`; `message_queue=REDIS_URL`. | **Blocking.** Add new origin to `SOCKETIO_CORS_ORIGINS` or realtime connects are rejected. |
| **CSP** | `app/__init__.py` `add_security_headers` — allowlists third-party hosts (openrouter, cloudinary, agora, google analytics/tagmanager, jsdelivr/unpkg/cdnjs, youtube, osrm, fonts). | Not host-specific to nelavista; move does not break CSP. Note it is permissive (`'unsafe-inline' 'unsafe-eval'`, `frame-src https:`). |
| **PWA manifest** | `app/static/manifest.json` — `start_url:"/"`, `scope:"/"`, `id:"nelavista-pwa-v1"`, served by `pwa_routes.py`. | Relative paths follow the host. **`id` is a constant** — an install from v1 and from v2 would collide; make it version-aware. **No service-worker file exists anywhere**, and `nav.js`/`shell.js`/`dashboard.html` actively *unregister* service workers → there is no SW scope problem, and the "offline" PWA claim is false (§7). |
| **SEO** | No `robots.txt`, no `sitemap.xml`, no `<link rel=canonical>` in any template. | Nothing to migrate, nothing to break; recommend a Search Console **Domain property** so both versions are covered. |
| **Search Console file** | `google76268f26b118dad1.html` at repo root. **No route serves it; it is not in `app/static/` → it is not reachable in production.** | Must be served deliberately once a property is set. Today it is dead weight. |
| **Hardcoded domain strings (config-hygiene debt)** | `services/*` and `ai_routes.py` send `HTTP-Referer: https://nelavista.com` (~20 sites); `link_fetch_service` User-Agent references nelavista.com; `SUPPORT_EMAIL`/`MAIL_DEFAULT_SENDER` default to `@nelavista.com`; deleted-user email domain `deleted.nelavista.com`; `config.py` default Socket.IO origin. | Cosmetic/metadata today, but they violate "no hardcoded domains" and will mislabel traffic from v1/v2. Move to config. |

---

## 6. Mobile readiness

**Auth (the blocker).** Login is a Flask **server-side session cookie** holding a `session['user']` dict. There is **no access/refresh token, no `/auth/refresh`, no bearer auth**. `SESSION_COOKIE_SAMESITE='Lax'`, `HttpOnly`, `Secure` (prod). Native apps cannot use this cleanly: no cookie jar semantics across a custom host, no way to do Google sign-in. Google sign-in is the **web Authorization-Code flow** via Authlib with **server-side session state** and a **host-derived `redirect_uri`** — unusable from iOS/Android, which need AppAuth/Custom-Tabs + PKCE + a custom URI scheme (and iOS also needs the native Google SDK for a good UX).

**API surface.** 124 `/api/*` endpoints exist, but they are **page-support JSON, not an app API**: session-cookie authed, **CSRF-protected globally** (Flask-WTF; `csrf.js` sends an `X-CSRFToken` header from a `<meta>` tag), no `/v1` prefix, no auth tokens, no OpenAPI schema, no version negotiation. So V1 has **effectively no mobile-consumable API**, confirming the brief's expectation. `apps/api` must be built fresh.

**Realtime** is session-cookie Socket.IO — same limitation.

**No mobile app, no app identifiers, no push credentials, no deep-link config exist yet.**

---

## 7. Where the README (and the brief's assumptions) are wrong or out of date

1. **"OpenRouter AI behind `services/ai_provider.py`"** — only *partly* true. The interface exists but **23 direct OpenRouter call sites remain**; most AI traffic bypasses the abstraction.
2. **"PWA (manifest + offline page)"** — misleading. `manifest.json` is served, but there is **no service worker** and the JS **unregisters** any existing one. `offline.html` is referenced by **no Python route** and is effectively dead; error pages use `error.html`. The app is not a working offline PWA today.
3. **Repo-size framing ("≈1.2 GB of course-content files tracked in git")** — imprecise. Those files are **Git LFS** objects (180 files); `app/static/media` (**146 MB** of `.mp4`/`.jpeg`) is **not** LFS-covered and is ordinary history. History-purge planning must handle both.
4. **"Repository structure" block omits** `data/`, `seed_data/`, `uploads/`, `extracted_images/`, `instance/`, `google76268f26b118dad1.html`, `.env.example`, and `docs/product/`.
5. **DOCS stub lists `docs/` as three files**; there is now also `docs/product/`.
6. **Counts are stale** (in `MIGRATION_MAP.md`, which the README points to): 68 models → **76**; 45 migrations → **50**; 36 test suites → **49 modules**; ~289 routes → **302**; `frontend/` is described as deleted (correct). LOC is now **20,309** in `app/`.
7. **Two spaces framing understates V1.** The README's product framing says "two spaces," but the code ships a full **Community** (14 routes), **live video meetings** (14, Agora), **employer** (4) and **reels** (2). The V2 PRD drops/redefines several of these — V1's real surface is larger than documented.
8. **`test`/`test123` default user** is created on debug boot — not mentioned in the README's security story; a real prod-hygiene item.
9. **Cloudinary is configured inside two route modules** (not central config) — the README's "config.py is the authoritative list" is fine for *names* but the wiring is scattered.
10. **Search Console file** is described as tracked (true) but it is **not served** — the README implies a working verification setup.
11. **`data/cbt questions`** is named like a folder but is a **file**; the README references `data/cbt questions` as if it were a directory.
12. **`APP_ENV`** (the brief's required single switch) **does not exist**; the code uses `FLASK_DEBUG` + `ENVIRONMENT`.

---

## 8. Risks & tech debt, ranked

**8.1 Secrets (highest).**
- `.env` is **not tracked today and does not appear in current history** (`git log --all -- .env` is empty). However, the specific commits cited in `docs/SECRETS_ROTATION.md` (`866dea3`, `5c78a68`, `070ec51`, `d27dc45`) **do not exist in this repository's history** (114 commits; first commit is a single "production build" import). Meaning either the history was already rewritten, or those commits belong to an older/other lineage (the doc names remote `github.com/ABDULAFEEZ12/Tellavista.git`). **Either way, treat every credential named in `SECRETS_ROTATION.md` as compromised and rotate** (Render DB passwords ×3, OpenRouter keys ×2, Hugging Face token, Google API keys ×2, Custom Search engine ID, Cloudinary API secret, Groq key, and a real `SECRET_KEY` that was never set). **`SECRET_KEY` still needs to be verified as a real value in prod** — if it is ever the dev fallback, all sessions are forgeable.
- **gitleaks is not present** (no pre-commit, no CI). No secret scanning of any kind today.

**8.2 Repo size / history.**
- `.git` = **1.3 GB**; materials via LFS (good) plus 146 MB of un-LFS'd media (bad). Any "untrack + purge" plan must handle LFS refs and coordinate a force-push that the brief forbids without explicit approval.

**8.3 Single worker / eventlet.**
- **1 gunicorn worker** until `REDIS_URL` is set; **eventlet** is bugfix-only upstream. Both are scaling ceilings for the thousands→millions target and must be decided in Phase 1 (async framework + Redis).

**8.4 No CI and a slow suite.**
- **No `.github/`** — nothing enforces lint/tests/migrations. Baseline `pytest tests/` **did not finish within ~7 minutes** on this machine (54+ tests passing, no failures observed up to the cutoff) — the suite is too slow to gate a PR today and needs profiling before it can be a required check.

**8.5 Migration state.**
- **Single head confirmed: `f1b2c3d4e5f6`** — healthy. But the app can still run `db.create_all()`/`stamp()` at import on an untracked DB, and legacy `ALTER TABLE` bridges live in `database.py`; multi-developer Alembic rules (expand/contract, conflict resolution) don't exist yet.

**8.6 Test coverage gaps.**
- 49 modules cover a lot (auth security, CBT integrity, injection defense, scoping, performance). But there are **no tests for environment separation, config validation, or the mobile/API contract** (because those don't exist), and the suite is slow.

**8.7 Debug/leftover surface in prod.**
- `dashboard_routes.py` exposes `/api/debug-courses`, `/api/debug-all`, `/api/debug-tables`. Cores stubs `/cleanup_attachments`, `/clear_context`. `generate_pwa_icons()` runs on import in debug. `create_default_user()` creates a known-password account. All must be gated off in prod.

**8.8 Data hygiene.**
- Possible `test` user in prod (from the historical pytest bug — verify and remove).
- Low-sensitivity but real: hardcoded `HTTP-Referer` domain strings; Cloudinary config duplicated; junk tracked file `app/static/materials/accounting/h`.

---

## 9. Carry into V2 vs rewrite

**Carry (high value, already correct):**
- **Taxonomy + domain model**: `University→Faculty→Department→Course→Topic`, `AcademicSession`/`Semester`/`Enrollment` — the backbone of both paths.
- **Auth mechanics per se**: password hashing (PBKDF2 via Werkzeug — plan rehash-to-argon2 on login), hashed+expiring reset/verify tokens, `google_sub` linking, account deletion = anonymise+deactivate.
- **AI layer**: `ai_provider.py` interface (**finish migrating the 23 direct call sites**), `rag_service.py` (chunking + embeddings + pgvector + honest-decline), `material_service.py` (extraction cache), `search_service.py` (FTS), `cbt_bank.py`.
- **Skills domain objects** that map onto the PRD's verification/cohort/opportunity entities (`StudentSkill`, `Cohort`, `CohortEnrollment`, `Opportunity*`, `Rating`, `GradingEvent`, `Challenge*`, `ProjectTemplate`, `StudentProject`) — reuse the *semantics*, not necessarily the tables.
- **Operational services**: `notification_service`, `messaging_service`, `analytics` (PostHog), Sentry wiring, structured logging.
- **Content**: course taxonomy CSVs, CBT question banks, career-skill definitions, and the 1.2 GB of materials (as data, not as repo blobs).

**Rewrite / replace:**
- **Frontend** (server-rendered Jinja + 4 hand-written CSS files) → V2 web (React/TS) and native mobile.
- **Auth transport** (session cookie) → token-based, multi-client (web + native).
- **API** (`/api/*` page JSON) → versioned FastAPI with OpenAPI-generated clients.
- **Realtime** (eventlet Socket.IO) → decide per ADR-f (keep/replace/drop) + push notifications.
- **One 2,871-line `models.py`** → domain modules.
- **`database.py` import-time `create_all`/`ALTER`** → migrations only.
- **Money/work flows**: V1's `Opportunity`/`Competition` are a marketplace sketch; the V2 managed-workforce ledger (90/10/2 split, quality stage, payouts) is new and must be built as a first-class, transactional subsystem.

---

## 10. Conflicts between the brief and the code (flagged, per instruction)

1. **"Community — no Community product"** (V2) is fine, but **V1 already ships Community, live meetings, employer and reels**. The brief's "two spaces" framing matches the README, not the code. Any plan must place these explicitly (freeze/re-flag/retire), not assume they don't exist.
2. **`APP_ENV` does not exist**; the closest is `ENVIRONMENT`/`FLASK_DEBUG`. Introducing `APP_ENV` is net-new (and `ENVIRONMENT`/`IS_PRODUCTION` are barely used — only the Sentry label).
3. **"pgvector RAG"** is present and working (not a gap) — the brief is right; `MIGRATION_MAP.md`'s older "no RAG" row is now stale.
4. **"1.2 GB tracked in git"** — it's LFS (see §8.2), which changes the untrack/purge plan materially.
5. **Search Console file is not actually served** — the brief assumes it functions.
6. **The `.env` incident's commits are not in this repo's history** — the brief/`SECRETS_ROTATION.md` assume they are. Rotation still stands; the history-purge premise needs re-verification before any destructive action.
7. **Port 5000 is confirmed** as V1's default (`PORT` default 5000; `wsgi.py`).
8. **No CI, no staging** exist — Phase 2/3 create them, they are not "fix an existing setup".

---

## 11. Blocking questions (batched; nothing here is answerable from the code)

1. **Production domain:** what is V1's *current* live hostname? Is `nelavista.com` already pointing at V1, or is it still a Render `*.onrender.com` URL? (Code defaults to `nelavista.com` but cannot confirm DNS.)
2. **Team & machines:** how many developers, and does anyone work on Windows/Linux only (determines how iOS dev/test is done — Mac vs cloud builds)?
3. **Budget:** is a paid Render plan (Redis + a separate DB per environment + a background worker) funded, or must V2 stay on free tiers? This decides the Phase 1 hosting ADR.
4. **Timeline & ownership:** what is the target V2 launch window, and who is authorised to trigger a PROD deploy (a person, or CI with manual approval)?
5. **Store accounts:** do **Apple Developer Program** and **Google Play Console** accounts already exist, and is there a Mac or a cloud-build (EAS) budget for iOS? (Phase 1 mobile ADR and Phase 3 mobile setup depend on this.)

### 11.1 Answers received (2026-10-16)

| # | Answer | Phase 1 impact |
|---|---|---|
| 1 | **`nelavista.com` is live and serves V1 today. `v1.nelavista.com` does not exist yet.** | The swap is *additive*: create `v1.nelavista.com` (new DNS record + Render custom domain + cert) and point it at V1; keep the existing `nelavista.com` OAuth/CORS/Socket.IO entries during transition, then repoint `nelavista.com` to V2. No existing subdomain to preserve. |
| 2 | **2–3 developers, all on Windows/Linux. No Mac.** | The **iOS Simulator is unavailable** to the team: local mobile loops are **Android Emulator + real device over LAN only**. iOS is built/tested via **cloud builds + TestFlight**. This removes fully-native iOS and pushes hard toward **one cross-platform codebase with a cloud build service (Expo + EAS Build)**. |
| 3 | **Budget: "whatever is needed."** | Redis, a separate DB per environment, a background worker, and separate Sentry/PostHog projects are all funded → the Phase 1 hosting ADR can choose the correct shape, not the free-tier shape. |
| 4 | **Target launch within 1–3 months.** | Aggressive: bias every decision toward the **fewest moving parts**, maximum reuse of V1's data model/services, and the PRD's build-first slice. |
| 5 | **Google Play Console exists; other accounts obtainable when needed. No macOS.** | **Apple Developer Program enrolment must start early** (approval can take days) since there is no Mac to fall back on. iOS distribution = EAS cloud build → TestFlight. Deploy ownership still to confirm (routed to the PROD-approval ADR). |
