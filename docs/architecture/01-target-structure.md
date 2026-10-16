# 01 — Target repository structure

**Transitional until V2 launch:** V1 stays at the repo root (ADR-0004); V2 lives under `apps/`. At launch, V1 moves into `apps/v1/` in one isolated PR.

## Tree

```
nelavista/                              (repo root = Render Root Directory until launch)
├── app/  migrations/  scripts/  tests/   ← V1 (LIVE). Untouched. Becomes apps/v1/ at launch.
├── data/  seed_data/                    ← V1 seed inputs (see "Root clutter" below)
├── instance/ uploads/ extracted_images/  ← V1 local runtime artifacts (gitignored)
├── google76268f26b118dad1.html           ← Search Console file (ADR-0004)
├── wsgi.py  Procfile  runtime.txt        ← V1 entry point / deploy config
├── requirements.txt  requirements-dev.txt  pytest.ini
│
├── apps/
│   ├── api/            FastAPI modular monolith            owner: @backend
│   ├── web/            React + TS + Vite student PWA        owner: @web
│   ├── admin/          React + TS internal ops (role-gated) owner: @web
│   └── mobile/         Expo (React Native) iOS + Android    owner: @mobile
│
├── packages/
│   ├── config/         versions.json + shared app constants (the ONE version file)
│   ├── api-client/     generated typed TS client (from apps/api OpenAPI)
│   ├── contracts/      shared TS types/validators used by web/admin/mobile
│   └── design-tokens/  colour/spacing/type tokens shared by web/admin/mobile
│
├── tools/
│   ├── prodguard.py    refuses destructive scripts against prod (ADR-0002)
│   ├── seed_local.py   safe, idempotent LOCAL/DEV sample data
│   └── gen_api_client.ts  regenerates packages/api-client
│
├── docs/
│   ├── adr/            decision records (Phase 1)
│   ├── architecture/   audit + these plan docs
│   ├── runbooks/       operational how-tos
│   ├── product/        the V2 PRD
│   └── MIGRATION_MAP.md  SECRETS_ROTATION.md  TEMPLATE_CLASSIFICATION.md
│
├── .github/workflows/  CI/CD (path-filtered)
├── docker-compose.yml  local Postgres+pgvector, Redis, Mailpit
├── Makefile            root task runner
├── pnpm-workspace.yaml turbo.json package.json   JS workspace
├── pyproject.toml      uv workspace root
└── .env.example  .env.local(gitignored)  .gitignore  .gitattributes
```

## Purpose and owner of each folder

| Folder | Purpose | Owner (CODEOWNERS) |
|---|---|---|
| `app/`…(V1) | Live Flask app | `@v1-maintainer` |
| `apps/api` | The V2 HTTP API (only writer of the V2 DB) | `@backend` |
| `apps/web` | Student web app (PWA) | `@web` |
| `apps/admin` | Internal ops tools (role-gated) | `@web` |
| `apps/mobile` | iOS + Android app | `@mobile` |
| `packages/config` | `versions.json`, min-app-version, env names | `@backend` |
| `packages/api-client` | **Generated** — never hand-edited | `@backend` |
| `packages/contracts` | Shared types/validators | `@backend` |
| `packages/design-tokens` | Shared design values | `@web` |
| `tools/` | Repo-wide scripts (seed, guard, codegen) | `@backend` |
| `docs/` | ADRs, architecture, runbooks, product | `@founder` |
| `.github/` | CI/CD | `@backend` |

## Naming conventions

- **Files/packages:** `kebab-case` (`api-client`, `design-tokens`). **Python modules:** `snake_case`. **React components:** `PascalCase.tsx`.
- **Branches:** `feat/…`, `fix/…`, `chore/…`, `docs/…` (trunk-based, short-lived). **Commits:** Conventional Commits (`feat(api): …`).
- **DB:** tables `snake_case` plural; migrations are `expand/contract` (see `04-v1-to-v2-migration.md`).
- **Domains in the API** mirror the PRD: `identity, academia, skills, verification, matching, work, quality, ledger, notifications, admin`.

## Where docs, scripts, data and seeds live

- **Docs:** `docs/` (this file lives there). Operational steps go in `docs/runbooks/`.
- **Repo-wide scripts:** `tools/`. **V1 scripts:** stay in `scripts/` with V1.
- **Seed data:** `data/seed-inputs/` (V1's `data/` renamed at launch). Sample data for local/dev is produced by `tools/seed_local.py`, never by copying prod.
- **Seeds never touch prod** without `--i-know-this-is-production` (ADR-0002).

## Root clutter — the approved disposition

| Item | Disposition |
|---|---|
| `data/` (369 CBT bank files, CSV, `cbt questions` **file** misnamed as a dir) | Keep tracked. **Rename** `cbt questions` → `cbt_questions.txt` **only when** the seed scripts that read it are updated in the same PR (deferred — see note). |
| `seed_data/career_skills/` | Fold into `scripts/seed/data/career_skills/` (it is seed payload). |
| `uploads/`, `extracted_images/`, `instance/` | Keep, gitignored, documented as ephemeral runtime artifacts. |
| `google76268f26b118dad1.html` | Keep at root; **add a route/static mapping so it is actually served** (currently not). |
| `.env` (on disk) | Local only, gitignored. |

> **Note:** renaming `data/cbt questions` and moving `seed_data/` are V1-touching edits (they change paths the V1 seed scripts read). They are **deliberately deferred** to a reviewed PR with a V1 test run, per the hard rule that V1 must not break. The disposition above is the plan; the moves are logged in `docs/runbooks/v1-relocation.md`.
