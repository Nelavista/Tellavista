# ADR-0001 — V2 stack and monorepo layout

**Status:** Accepted · **Date:** 2026-10-16 · **Supersedes:** nothing

## Context

- V1 is a Flask + Jinja monolith at the repo root, live at `nelavista.com`, ~20.3k LOC, 76 models in one file, no CI, no staging, one eventlet worker.
- V2 must serve **web, iOS, Android and internal admin** from one team of 2–3 developers (all on Windows/Linux, **no Mac**) inside **1–3 months**, aiming at hundreds of thousands of students and a managed-workforce money flow that must never lose work or payments.
- The PRD (`docs/product/Nelavista_V2_PRD.pdf`) fixes *scope*, not stack; how to build is explicitly the team's decision.

## Options

| Area | Option A (hypothesis) | Option B | Option C |
|---|---|---|---|
| Repo | JS: pnpm + Turborepo · Python: `uv` workspaces · `make` | Nx monorepo | Keep two repos (web/mobile vs api) |
| API | FastAPI + Pydantic v2 + SQLAlchemy 2 + Alembic, modular monolith | Keep Flask, expand V1 | Node/NestJS |
| Queue | ARQ (Redis, async) | Celery (Redis) | Dramatiq |
| Web | React + TS + Vite + Tailwind PWA | SvelteKit | Next.js |
| Mobile | Expo (React Native) + TS + EAS | Flutter | Fully native (Swift + Kotlin) |
| Admin | Separate role-gated React app (`apps/admin`) | Reuse `apps/web` routes | Keep V1's Jinja admin |

## Decision

**Adopt the hypothesis with three amendments.**

1. **Monorepo:** `pnpm` workspaces + **Turborepo** for JS/TS, **`uv` workspaces** for Python, **`make`** as the root task runner (present on dev machines/CI, one fewer tool than `just`), **Docker Compose** for local services. `apps/*` for deployables, `packages/*` for shared code, `apps/v1` left in place for now (ADR-0004).
2. **API:** **FastAPI + Pydantic v2 + SQLAlchemy 2 + Alembic**, structured as a **modular monolith**: `identity, academia, skills, verification, matching, work, quality, ledger, notifications, admin`. Each domain owns its models, services and routers; no cross-domain writes except through a published service.
3. **Queue: ARQ.** Async-native (matches FastAPI), Redis-only (already required), tiny surface, no separate broker process beyond a worker — the fewest moving parts that reach the scale target. *Celery* is the fallback if ARQ blocks a feature; the worker is behind an internal `queue.enqueue()` seam so the swap is one adapter.
4. **DB: PostgreSQL (Render) + pgvector.** The ledger needs real transactions and constraints; no document database for money.
5. **Web:** React + TS + Vite + Tailwind, installed as a lightweight PWA. **Landing/marketing routes are prerendered at build time** (static HTML for the public pages, client-rendered for the authenticated app) so SEO does not need a Node SSR server. A server-rendered framework is a later option, not a V2 need.
6. **Mobile: Expo (React Native) + TypeScript + EAS Build.** One codebase, both stores, **cloud iOS builds without a Mac** — decisive given the team's machines. Shared **logic, not UI**, with web through workspace packages.
7. **Admin:** a **separate, role-gated React app** (`apps/admin`). Internal ops tools (run managed projects, quality review) are a different risk and audience from the student app and must not ship in the student bundle.
8. **Contracts:** FastAPI's OpenAPI schema generates a typed TS client (`packages/api-client`); **CI fails if it is stale**; web, mobile and admin all consume it.

### Why not the alternatives
- **Flutter** is a fine cross-platform choice with cloud builds, but it shares *no* code with the TS web app, so a 2–3 person team pays for two languages and two skill sets. Expo lets the team reuse TS types, validation and API-client logic across web/mobile/admin.
- **Fully native** is two codebases and two release trains — impossible in 1–3 months for this team, and cannot build iOS without a Mac.
- **Keeping Flask and expanding V1** was already rejected in the historical V1 migration analysis for the *V2* surface: V1's session-cookie auth and page-JSON `/api/*` cannot serve native apps, and the money flow needs a transactional domain model that V1 does not have. V1 stays live and untouched; V2 is a new app behind the same domain (ADR-0004).
- **Next.js** is heavier and pulls a Node server into the runtime; Vite + prerender keeps the moving parts down.

## Consequences / trade-offs
- **Two languages** (Python API + TS clients) — mitigated by generated types and shared packages.
- **Turborepo + pnpm + uv + make + Docker** is a real toolchain to learn — mitigated by a one-command `make bootstrap`.
- The **API is the single source of truth for contracts**, so schema changes are visible to all clients immediately (intended).

## Reversibility
- **High** at the edges (web framework, queue, prerender) — all swappable behind seams.
- **Medium** for the API framework: reversing FastAPI→Flask after domains are written is expensive, so the domain *boundaries* matter more than the framework.
- **Low** cost to change mobile **within Expo** providers; **high** to change mobile *platform* after native modules are chosen.

## Team cost
- ~1 week of setup (Phase 3 scaffolding is already delivered), then parallel streams: API domains (1 dev), web+admin (1 dev), mobile (shared). One owner per package via CODEOWNERS.
