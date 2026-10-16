# Nelavista

A platform for African (Nigerian first) university students, taking a student from the lecture hall to paid work.

**Two things live in this repo right now:**

| | Where | What it is |
|---|---|---|
| **V1** — live | repo root (`app/`, `migrations/`, `scripts/`, `tests/`) | The current production app at `nelavista.com`. **Frozen for new features; security/critical fixes only after V2 launches.** |
| **V2** — in progress | `apps/api`, `apps/web`, `apps/admin`, `apps/mobile`, `packages/*` | The next version: one journey — Enrol → Learn → Build → Verify → Match → Work → Quality check → Earn. |

`nelavista.com` always serves the **latest** version. Older versions live on their own subdomains (`v1.nelavista.com`). See `docs/architecture/03-versioning-and-domains.md`.

---

## Planning & decisions (read these first)

- **`docs/architecture/00-audit.md`** — what V1 actually is (verified against code, *not* this README's history).
- **`docs/adr/`** — the accepted decisions (stack, environments, domains, auth, ledger, API versioning…).
- **`docs/architecture/01-target-structure.md` … `07-risk-register.md`** — the target layout, environments, migration plan, domain map, roadmap, risks.
- **`docs/product/Nelavista_V2_PRD.pdf`** — the product requirements.
- **`docs/runbooks/`** — how to set up locally, deploy, roll back, rotate secrets.
- **`docs/SECRETS_ROTATION.md`** — credentials that must be rotated.

> This README was rewritten (2026-10) to match the code. The previous version described a UI and structure that no longer matched the implementation; the audit lists every discrepancy.

---

## V2 quick start (new developers)

```bash
# prerequisites: Docker, Node 20+, pnpm 9+, Python 3.11, uv, make
make bootstrap      # install deps + git hooks
make up             # Postgres+pgvector, Redis, Mailpit via Docker Compose
make seed-local     # safe fake sample data (never touches real data)
make dev            # api :8000, web :5173, admin :5174
```

Fixed port map: V1 `5000` · API `8000` · web `5173` · admin `5174` · Mailpit UI `8025` · Postgres `5432` · Redis `6379`.

Full setup, and mobile setup (Android Emulator; iOS via cloud builds — the team has no Mac): **`docs/runbooks/local-setup.md`** and **`docs/runbooks/mobile-local-setup.md`**.

## V1 quick start (unchanged)

```bash
pip install -r requirements.txt
cp .env.example .env          # see the file's comments
python wsgi.py                # http://localhost:5000
pytest tests/                 # tests use their own throwaway SQLite DB
```

V1 keeps its own `requirements.txt`, `Procfile` and Render config. **Do not upgrade V1 dependencies and do not change V1 behaviour.** Before and after any V1-touching change run `pytest tests/` and `python -m scripts.audit.check_template_links`.

---

## Repository layout

```
app/ migrations/ scripts/ tests/   V1 (live) — moves to apps/v1/ at V2 launch
data/ seed_data/                   V1 seed inputs
apps/
  api/       FastAPI modular monolith (only writer of the V2 DB)
  web/       React + TS + Vite student PWA
  admin/     React + TS internal ops tools (role-gated)
  mobile/    Expo (React Native) — iOS + Android, EAS Build
packages/
  config/        versions.json (the single source of version + min-app-version truth)
  api-client/    generated typed TS client (do not hand-edit)
  contracts/     shared TS types/validators
  design-tokens/ shared design values
tools/             prodguard, local seed, codegen
docs/              adr/ architecture/ runbooks/ product/
.github/workflows/ path-filtered CI/CD
```

One owner per area: **`CODEOWNERS`**. Conventions, branch/commit rules and the one-command setup: **`CONTRIBUTING.md`**.

---

## Environments

`APP_ENV` ∈ `{local, dev, prod}` drives everything; config is environment-variable-only and validated at startup. dev and prod share **no** credentials or data. Details and the full matrix: `docs/architecture/02-environments.md`.

---

## Licence & contact

Internal. Support: see `SUPPORT_EMAIL`.
