# Nelavista

A Flask-based student platform for Nigerian university students — Academia (course
materials, CBT practice, AI tutoring) and Skills (structured learning, projects,
verification, paid opportunities).

## Running locally

```
pip install -r requirements.txt
cp .env.example .env   # fill in real values -- see comments in that file
python app.py
```

Requires a database (`DATABASE_URL` in `.env`; falls back to a local SQLite file if
unset) and, for full functionality, an OpenRouter API key (AI features), Cloudinary
credentials (file storage), and a mail server (password reset / email verification).
`REDIS_URL` is optional locally but required before running more than one worker/dyno in
production — see `.env.example`.

## Deployment

`Procfile` documents the required start command: `gunicorn --worker-class eventlet -w 1
app:app`. The `--worker-class eventlet` flag is required for Flask-SocketIO (live
classes, community chat) to work at all — without it, WebSocket connections fail
outright. `-w 1` (single worker) is deliberate: real-time room/participant state
(`services/meeting_service.py`) lives in each worker's own process memory with no shared
message queue by default, so a second worker would silently miss events meant for
sockets connected to the other worker. **Do not increase worker count (or run more than
one instance) until `REDIS_URL` is set** — see `.env.example` and `extensions.py`; once
it's set, Socket.IO uses Redis as a cross-worker message queue and this constraint goes
away.

This Procfile was added as part of the Level 1 fix pass — if your Render service (or
wherever this is deployed) has its own Start Command configured in its dashboard rather
than reading `Procfile` automatically, **update that dashboard setting to match**, since
the dashboard setting takes precedence and this repo has no way to verify or change it
directly.

## Database migrations

Schema changes go through Flask-Migrate/Alembic:

```
flask db migrate -m "description"
flask db upgrade
```

`migrate.py` and `fix_db.py` at the repo root are deprecated, pre-Alembic one-off
scripts — see their docstrings. Don't add new ones like them; use a real migration.

## Root-level scripts

These are maintenance/setup scripts, not part of the running app (nothing in `app.py`
imports them). Run with `python <script>.py` from the repo root, against whichever
`DATABASE_URL` your `.env` points at — **know which database you're pointed at before
running any of these**, especially the seed scripts.

**Admin/maintenance**
- `make_admin.py <username> grant|revoke` — grant or revoke admin access for a user.
  Requires typing the username again to confirm; logs every change to `AdminAuditLog`.
- `check_materials.py` — inspects the `Material` table.
- `audit_broken_material_links.py [--apply]` — finds (and, with `--apply`, deactivates)
  `Material` rows whose `file_url` points at a local static file that doesn't exist on
  disk. Defaults to a dry run.
- `cleanup_unembeddable_materials.py [--dry-run]` — checks external-URL materials for
  real embeddability (X-Frame-Options/CSP) and removes ones that can't be framed.
  **Defaults to making changes** — pass `--dry-run` to preview first.

**Seeding** (all idempotent — safe to re-run; each checks for existing rows before
inserting)
- `seed_academia.py` — university/faculty/department/course taxonomy from
  `Nelavista_Course_Codes.csv` (LASU/UNILAG/UI).
- `seed_ccmas_core.py` — NUC CCMAS national core curriculum floor for universities
  without a school-specific catalog yet.
- `seed_cbt_questions.py` — copies the CBT question bank into the `CBTQuestion` table.
- `seed_skills.py` — Skills catalog (categories, skills, courses, lessons, project
  templates).
- `seed_oer_materials.py` — Open Educational Resource materials.
- `seed_materials.py`, `seed_30_courses.py` — near-duplicate legacy material seeders;
  `seed_materials.py` is the more complete/current one.
- `seed_100_level_science_500.py`, `seed_200_to_400_level_science.py`,
  `seed_200_to_400_COMPLETE.py` — Faculty of Science material seeders;
  `seed_200_to_400_COMPLETE.py` supersedes `seed_200_to_400_level_science.py`
  (broader coverage, same level range).

All material-seeding scripts now skip any entry whose referenced local file doesn't
exist on disk at seed time (logged, not silently dropped) — added after an audit found
the large majority of hardcoded paths in these scripts didn't correspond to real files.
If you're adding new entries to any of them, make sure the file is actually committed
under `static/materials/` first.

## Tests

```
pip install -r requirements-dev.txt
pytest tests/
```

Tests build their own throwaway Flask app bound to a temporary SQLite file (see
`tests/conftest.py`) — they never touch whatever `DATABASE_URL` your local `.env` points
at.
