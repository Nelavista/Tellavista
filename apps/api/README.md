# apps/api

Nelavista V2 API — **FastAPI modular monolith** (ADR-0001). It is the only writer of the V2 database.

## Run locally
```bash
make up            # Postgres+pgvector, Redis, Mailpit
make api-dev       # uvicorn on :8000
# docs at http://localhost:8000/docs  (disabled when APP_ENV=prod)
```

## Layout
```
app/
  core/     settings (APP_ENV, fail-fast), versioning + security middleware
  db/       engine, session, declarative base
  models/   domain models (identity, academia, …)
  api/v1/   versioned routers (health today; domains attach as they are built)
  seed/     local/dev sample data
migrations/ Alembic (single head enforced in CI)
tests/      pytest
```

## Conventions
- **Config is environment-variable only.** `APP_ENV` ∈ `{local,dev,prod}`; invalid config fails at startup with a readable message (`app/core/config.py`).
- **No hardcoded domains/URLs/keys.** Base URLs, CORS and OAuth redirects come from settings.
- **API version = path** (`/v1`), independent of product version (ADR-0010). Mobile sends `X-App-Version` + `X-App-Platform`; below `min_supported` → `426`.
- **Migrations:** expand/contract; never make a column NOT NULL in the same release that stops writing to it; `alembic heads` must print exactly one.

## Status
Domain modules are implemented for Phases 1–8 (`docs/build/phase-1-10-plan.md`):
identity/auth, onboarding, skills, verification, opportunities/matching, work and
quality, money, talent, academia and ops. Phase 9/10 work is release and hardening
(`docs/build/REMAINING_WORK.md` is the live list).
