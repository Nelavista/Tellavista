# Runbook — Local setup (web + API in under 15 minutes)

## Prerequisites
Docker · Node 20+ (`.nvmrc`) · pnpm 9+ · Python 3.11 · [uv](https://docs.astral.sh/uv/) · `make` · Git LFS (`git lfs install`).

## Steps
```bash
git clone <repo> && cd nelavista
make bootstrap     # pnpm install, uv sync (api), pre-commit install
make up            # Postgres+pgvector, Redis, Mailpit
make seed-local    # fake sample data (prod-guarded)
make dev           # api :8000, web :5173, admin :5174
```

Then: web at http://localhost:5173 · admin at http://localhost:5174 · API docs at http://localhost:8000/docs · Mailpit UI at http://localhost:8025.

## Port map (fixed — do not clash)
| Service | Port |
|---|---|
| V1 (Flask dev) | 5000 |
| V2 API | 8000 |
| Web | 5173 |
| Admin | 5174 |
| Mailpit UI / SMTP | 8025 / 1025 |
| Postgres / Redis | 5432 / 6379 |

## No real secrets needed
Every integration has a safe local fallback or is cleanly disabled:
- **Email** → Mailpit (`MAIL_HOST=localhost`, `MAIL_PORT=1025`).
- **Storage** → `STORAGE_BACKEND=local` (no Cloudinary).
- **AI** → either a personal low-limit `OPENROUTER_API_KEY`, or leave it unset (AI features report "unconfigured").
- **Sentry / PostHog** → unset = complete no-op.

`.env.local` is gitignored. Copy from the relevant `.env.example`.

## Troubleshooting
- **API exits with "Invalid configuration"** → that is the fail-fast contract. Read the message; a required variable is missing.
- **Port clash** → the map above is fixed; stop whatever holds the port rather than moving these.
- **DB schema out of date** → `make db-upgrade`.
- **Reset the local DB** → `make reset-db` (destroys the local Docker volume only).

## V1 locally (unchanged)
```bash
pip install -r requirements.txt
cp .env.example .env
python wsgi.py     # http://localhost:5000
```
Do not upgrade V1 dependencies.
