# Nelavista

A Flask-based student platform for Nigerian university students — **Academia** (course
materials, CBT mock exams, AI tutoring, RAG-grounded material Q&A, insights) and
**Skills** (structured learning paths, projects, verification, paid opportunities).
One product with two spaces; students pick a path at `/choose-path` and can switch
anytime.

## Stack

- **Backend:** Flask 3.1, SQLAlchemy 2, Flask-Migrate/Alembic, Flask-SocketIO (eventlet)
  for live classes & chat, Flask-Limiter (per-user rate limits), Flask-Mail.
- **Frontend:** server-rendered Jinja templates + vanilla JS/CSS (no build step, no
  bundler, no Node toolchain — see "Repository structure").
- **Data:** PostgreSQL in production (Render), SQLite for local dev/tests.
- **AI:** OpenRouter (chat/embeddings) behind the `services/ai_provider.py` abstraction;
  Postgres full-text + pgvector for RAG retrieval; Tavily for external PDF search.
- **Observability:** Sentry (`SENTRY_DSN`), structured stdout logging, PostHog product
  analytics (`POSTHOG_API_KEY`, both optional and env-gated).

## Feature set (current)

**Academia**
- Study materials library: department/level/university-scoped, full-text search
  (Postgres FTS + GIN, ILIKE fallback on SQLite), resume-position reading (PDF.js with
  page tracking), Cloudinary file storage with a local-`static` legacy path.
- CBT mock exams: MCQ, true/false and written formats, server-derived time limits with
  a client countdown + auto-submit, per-topic mastery signals.
- AI Tutor (Ask Nelavista): streaming chat with conversation history; CBT answer
  explanations with flag-for-review feedback loop.
- Material Q&A grounded in per-document RAG chunks (honest decline below a similarity
  threshold — never a fabricated answer).
- Onboarding wizard (university → faculty → department → level → session → semester →
  courses) writing real `Enrollment` rows; waitlist capture for uncovered schools.
- Dashboard insights: weak/strong topics, recommendations, progress.
- Campus map, notifications, profile + profile-completion enforcement.

**Skills**
- Catalog, learning paths, lessons, quizzes, challenges, projects with file workspace,
  cohorts/class system with GPAs, verification, opportunities/gigs/talent discovery,
  employer profiles & messaging.

**Platform**
- Auth (password + Google OAuth), email verification (hashed tokens), password reset,
  admin moderation consoles (materials, videos, users, AI flags, academia taxonomy),
  PWA (manifest + offline page), health endpoint at `/health`.

## Repository structure

```
app/
  __init__.py        # create_app(): extensions, CSP/security headers, blueprints
  config.py          # env-driven config (see .env.example)
  models.py          # all SQLAlchemy models
  routes/            # one module per blueprint (all registered in app/__init__.py)
  services/          # business logic (ai_provider, rag_service, insights, search, ...)
  templates/         # Jinja templates (components/ holds shared chrome)
  static/            # css/js/icons/images + materials/ (tracked content, see Limitations)
migrations/          # Alembic revisions (single head; `flask db upgrade`)
scripts/             # seed / audit / maintenance tools — not imported by the app
tests/               # pytest suite (own throwaway app; never touches DATABASE_URL)
docs/                # MIGRATION_MAP, SECRETS_ROTATION, TEMPLATE_CLASSIFICATION
```

## Running locally

```
pip install -r requirements.txt
cp .env.example .env   # fill in real values -- see comments in that file
python wsgi.py
```

Requires a database (`DATABASE_URL`; falls back to local SQLite if unset) and, for full
functionality, an OpenRouter key (AI), Cloudinary credentials (file storage), and a mail
server (password reset / email verification). `REDIS_URL` is optional locally but
required before running more than one worker/dyno in production — see `.env.example`.
Optional observability: `SENTRY_DSN`, `POSTHOG_API_KEY`.

## Database migrations

Schema changes go through Flask-Migrate/Alembic:

```
flask db migrate -m "description"
flask db upgrade
```

Set `SKIP_DB_INIT=1` when running `flask db upgrade` so importing the app does not
`create_all()` ahead of the migration (the app and `tests/conftest.py` already do this
where appropriate; `.env.example` documents the variable).

## Operational scripts

Maintenance/setup scripts, not part of the running app (nothing in `app/` imports them).
Run as modules from the repo root (e.g. `python -m scripts.seed.seed_academia`) against
whichever `DATABASE_URL` your `.env` points at — **know which database you're pointed at
before running any of these**, especially the seed scripts.

**Admin/maintenance**
- `python -m scripts.admin.make_admin <username> grant|revoke` — grant/revoke admin
  access; logs every change to `AdminAuditLog`.
- `python -m scripts.audit.check_materials` — inspect the `Material` table.
- `python -m scripts.audit.check_template_links` — verify every internal link/fetch in
  templates resolves to a real route or static file (exit 1 on dead links).
- `python -m scripts.audit.audit_broken_material_links [--apply]` — find (and, with
  `--apply`, deactivate) `Material` rows whose `file_url` points at a local static file
  that doesn't exist on disk. Dry run by default.
- `python -m scripts.audit.audit_broken_external_links` — same for external URLs.
- `python -m scripts.maintenance.cleanup_unembeddable_materials [--dry-run]` — remove
  external materials that can't be framed. **Defaults to making changes** — pass
  `--dry-run` first.
- `python -m scripts.maintenance.migrate_static_materials_to_cloudinary` — one-time
  migration of local `static/materials` files to Cloudinary (run before any attempt to
  drop tracked static content).
- Other `scripts/maintenance/` tools: backfill taxonomy links, generate PWA icons,
  validate career-skills data.

**Seeding** (all idempotent — safe to re-run)
- `scripts/seed/seed_academia.py` — university/faculty/department/course taxonomy from
  `data/Nelavista_Course_Codes.csv`.
- `scripts/seed/seed_ccmas_core.py` — NUC CCMAS national core curriculum floor.
- `scripts/seed/seed_cbt_questions.py` / `seed_lasu_cbt_questions.py` — CBT banks from
  `data/cbt questions`.
- `scripts/seed/seed_skills.py` — Skills catalog (categories, skills, courses, lessons,
  project templates).
- `scripts/seed/seed_oer_materials.py` — Open Educational Resource materials.
- `scripts/seed/seed_materials.py` — general material seeder (current).
- `scripts/seed/seed_100_level_science_500.py`, `seed_200_to_400_COMPLETE.py` — Faculty
  of Science material seeders (the latter supersedes the old
  `seed_200_to_400_level_science.py`, removed in the 2026-09 cleanup).
- `scripts/seed/seed_topics_*.py`, `seed_topic_content_*.py`,
  `seed_topic_explanations_broad.py` — topic/explanation backfills (idempotent;
  explanations support dry-run/`--apply`).
- `scripts/seed/seed_campus_map.py`, `seed_20_career_skills.py`.

Material-seeding scripts skip entries whose referenced local file doesn't exist on disk
(logged, not silently dropped). New entries must have their file committed under
`app/static/materials/` first.

## Tests

```
pip install -r requirements-dev.txt
pytest tests/
```

Tests build their own throwaway Flask app bound to a temporary SQLite file (see
`tests/conftest.py`) — they never touch whatever `DATABASE_URL` your local `.env` points
at, and an autouse fixture in `tests/test_route_smoke.py` blocks all outbound network.
`test_route_smoke.py` sweeps the entire registered route table for wiring regressions.

Known local-only caveats: endpoints that need unconfigured integrations (Agora, mail)
report as UNCONFIGURED rather than failing — expected without keys.

## Deployment

`Procfile` documents the required start command: `gunicorn --worker-class eventlet -w 1
wsgi:app`. The `--worker-class eventlet` flag is required for Flask-SocketIO (live
classes, community chat) to work at all — without it, WebSocket connections fail
outright. `-w 1` (single worker) is deliberate: real-time room/participant state
(`services/meeting_service.py`) lives in each worker's own process memory with no shared
message queue by default, so a second worker would silently miss events meant for
sockets connected to the other worker. **Do not increase worker count (or run more than
one instance) until `REDIS_URL` is set** — see `.env.example` and `extensions.py`; once
it's set, Socket.IO uses Redis as a cross-worker message queue and this constraint goes
away.

If your Render service (or wherever this is deployed) has its own Start Command
configured in its dashboard rather than reading `Procfile` automatically, **update that
dashboard setting to match**, since the dashboard setting takes precedence.

After deploying a schema change: `flask db upgrade` (migrations are idempotent and
dialect-guarded; Postgres-only statements are skipped on SQLite).

## Configuration

All configuration is environment-driven — `.env.example` is the authoritative list and
documents required vs. optional for every variable (core, database, Redis, AI/search,
Cloudinary, mail, Agora, Google OAuth, Sentry, PostHog).

## Known limitations

- **Repo size:** `app/static/materials/` (~1.2 GB of course-content files) and
  `app/static/media/` are tracked in git. That content is still referenced by seeded
  `Material` rows on the local/static path. The intended end-state is
  `scripts/maintenance/migrate_static_materials_to_cloudinary.py` followed by untracking
  the files — not a mechanical delete. Until that migration runs, do not remove them.
- **Single-worker deployments** until `REDIS_URL` is configured (see Deployment).
- **Local DB filename** still defaults to `tellavista.db` (pre-rename artifact);
  renaming the default would orphan existing local databases, so it stays.
- Written CBT answers are self-marked (not auto-graded) by design.
- Eventlet is in bugfix-only mode upstream; migrating off it is tracked as future work.

## Further documentation

- `docs/MIGRATION_MAP.md` — PRD gap analysis (G1–G17), decision log, sequenced plan,
  and the cleanup/consistency pass record.
- `docs/SECRETS_ROTATION.md` — credential rotation checklist for the historical
  committed-`.env` incident.
- `docs/TEMPLATE_CLASSIFICATION.md` — template sweep record (active/legacy/dead).
