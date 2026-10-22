# Phase 0 — Foundations and contracts · PLAN (gate 1)

**Status:** awaiting approval. **No V2 feature code has been written for this phase.** This document is the only artifact.
**Date:** 2026-10-16 · **Branch:** `v2/phase-0-plan` (branched from `develop` @ `8295963`).
**Source of scope:** `docs/build/nelavista-02-v2-build-prompt.md` § PHASE 0. Where it disagrees with `docs/architecture/06-roadmap.md`, the build prompt wins and the difference is listed in §7.
**Rules in force:** V1 untouched · no production data · no secrets · small PRs behind feature flags · stop at every gate.

---

## 0. Preconditions (checked against the code, not assumed)

The brief says to stop if the monorepo, CI, environment separation or versioning plan are missing. They are present and green:

| Precondition | Evidence |
|---|---|
| Monorepo skeletons (api, web, admin, mobile) | `apps/{api,web,admin,mobile}`; `pnpm-workspace.yaml`, `pyproject.toml` (uv workspace), `turbo.json` |
| CI green | 8 workflows in `.github/workflows/`; all jobs verified locally and green on `main`/`develop` |
| Environment separation (local/dev/prod) | `apps/api/app/core/config.py` (`APP_ENV`, fail-fast validation), `docker-compose.yml`, `docs/architecture/02-environments.md`, `deploy-dev.yml` + `deploy-prod.yml` |
| Versioning plan + ADRs | ADR-0003/0010, `packages/config/versions.json`, `docs/architecture/03-versioning-and-domains.md` |
| Docs the brief tells me to read | `docs/architecture/00`–`07`, `docs/adr/0001`–`0010`, 11 runbooks, `docs/product/Nelavista_V2_PRD.pdf` |
| `CODEOWNERS` committed | `/CODEOWNERS` (every path → `@hiipraise`; see question Q8) |

### Branch decision (brief, kickoff item 4)

The prep PRs are **merged and the prep branch is deleted**: PR #4 and PR #5 (`chore/v2-prep-phase1-3`) are both in `main` (`d1d6d53`, `8295963`), and `develop` was fast-forwarded to `main`, so the integration branch is current. **I branched from `develop`, not from the deleted prep branch.**

---

## 1. What Phase 0 is

**Goal:** everything later phases depend on, with **no student features**.

**Scope (the brief's build list, verbatim in intent):** domain model v1 + migrations · API conventions (error format, pagination, idempotency, versioning, min-app-version, force-update) · auth core for web and native (incl. Google sign-in), roles/permissions, audit log · design tokens + a small shared UI foundation for web and mobile (**shared tokens, not shared components**) · background job system, feature flags, analytics + error tracking, local/dev seed · mobile shell internals (navigation, secure storage, offline store + sync queue, push plumbing, deep links, per-env build profiles) · admin shell (login, role gating, audit trail).

**Exit criteria (brief):** a developer can log in on **web, iOS, Android and admin** against **local and dev**; **CI is green**; the **money and permission test harnesses exist**.

**Non-goals:** every Phase 1–10 feature (identity *flows* beyond what the core needs, V1 import, Choose Path, skills content, matching, quality, ledger behaviour), any student-facing screen beyond a signed-in placeholder, and anything the PRD says not to build.

---

## 2. Gap analysis

### 2.1 Already built — do not rebuild (verified in code)

| Area | What exists | Where |
|---|---|---|
| Monorepo + tooling | pnpm 9.12.3 + Turborepo, uv workspace, `make` targets, Compose (pgvector pg16, Redis 7, Mailpit), prettier/eslint/editorconfig, pre-commit (gitleaks + ruff + hygiene) | `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `pyproject.toml`, `Makefile`, `docker-compose.yml`, `.pre-commit-config.yaml` |
| CI/CD | `ci-api` (uv sync → ruff → pytest → single Alembic head), `ci-js` (lint/typecheck/build), `ci-mobile` (typecheck), `ci-contracts` (OpenAPI export + freshness), `ci-v1` (V1 tests + template links), `security` (gitleaks CLI v8.30.1, checksum-pinned), `deploy-dev` (Render hooks on `develop`), `deploy-prod` (approval environment + explicit migrate job) | `.github/workflows/*` |
| Env/config | `APP_ENV ∈ {local,dev,prod}`, fail-fast validation (SECRET_KEY, DATABASE_URL, no `*` CORS outside local), mail/Google/Cloudinary/Sentry/PostHog placeholders | `apps/api/app/core/config.py` |
| API shell | FastAPI app, security-headers middleware, CORS from settings (already allows `Idempotency-Key`, `X-App-Version`, `X-App-Platform`), docs disabled in prod, `/v1/health`, root handshake | `apps/api/app/main.py`, `app/core/security_headers.py`, `app/api/v1/` |
| Min-app-version / force-update | `426 Upgrade Required` + `{upgrade,min_version,store_url}`, `X-Update-Recommended`, `X-API-Version` on every response | `apps/api/app/core/versioning.py` (ADR-0010) |
| Version policy | One file: product versions, API path versions, per-platform `min_supported`/`latest`/`store_url` | `packages/config/versions.json` |
| Feature flags | Server `FLAG_*`, client build-time flags with `VITE_`/`EXPO_PUBLIC_` prefixes | `apps/api/app/core/flags.py`, `packages/config/src/flags.ts` |
| DB + migrations | Declarative base + `TimestampMixin` + model registry, engine from settings (`pool_pre_ping`), `get_db` dependency, one Alembic revision, single-head enforced in CI | `apps/api/app/db/`, `apps/api/migrations/` |
| Sample data | Idempotent fake seed, prod-guarded entrypoint | `apps/api/app/seed/local.py`, `tools/seed_local.py`, `tools/prodguard.py` |
| Contracts + tokens | Money/`Page`/pagination and the three project statuses, `OpportunityType`; design tokens seeded from V1's palette; one shared component | `packages/contracts`, `packages/design-tokens`, `packages/ui` |
| API client | Hand-written `createApiClient` (bearer, `Idempotency-Key`, 426 handling) + generator tool + CI freshness check | `packages/api-client/src/index.ts`, `tools/gen_api_client.mjs` |
| Client shells | Web/admin Vite+React hello-world reading config-derived API URLs; Expo 52 hello-world with env variants, bundle IDs, deep-link config, 3 EAS profiles | `apps/web`, `apps/admin`, `apps/mobile/app.config.js`, `apps/mobile/eas.json` |
| API tests | 16 passing (config, flags, health) with a safe test environment | `apps/api/tests/` |

### 2.2 Still missing — the Phase 0 work

The brief's eight bullets, each with what is actually absent today:

| # | Build-prompt item | Status | What is missing |
|---|---|---|---|
| 1 | **Domain model v1 + migrations** | ~5 % present | Only `users`, `universities`, `faculties`, `departments`, `courses`, `materials` exist. Missing: identity (profile, preferences, role, session/refresh token, email token, consent, idempotency key), academia (session, semester, enrolment, topic, material chunk, question bank, attempt/answer), skills (skill, category, learning path + step, lesson, **task template**, progress), verification (verification record + event, assessment, practical task), matching (opportunity + `type`, requirement, skill gap, match result), work (project, cohort, member, assignment, submission), quality (quality standard, review, quality record), ledger (accounts, entries + postings, project value, payout, department share, reconciliation run), notifications (notification, push token, outbox) |
| 2 | **API conventions** (error format, pagination, idempotency, versioning, min-app-version, force-update) | ~35 % | ✅ min-app-version + force-update + `X-API-Version`. ❌ error envelope + exception handlers, ❌ request id/tracing, ❌ cursor pagination (contracts declare it, the server has nothing), ❌ idempotency **store** + replay (the header is only allow-listed in CORS), ❌ unknown-version guard, ❌ conventions doc, ❌ contract generation actually adopted (`packages/api-client/src/generated` absent → the CI step no-ops) |
| 3 | **Auth core, web + native, incl. Google** | 0 % | No signup/login/verify/reset, no Argon2id, no JWT access + rotating refresh with reuse detection, no cookie or bearer paths, no CSRF for cookie mutations, no `expo-secure-store` use, no Google web or native (PKCE/ID-token) flow, no rate limiting, no account-deletion endpoint, no admin MFA. Config placeholders for Google exist; nothing consumes them |
| 4 | **Roles, permissions, audit log** | 0 % | No role column, no policy/authorization layer, no object-level check, no `AuditLog` model/service, no admin gating |
| 5 | **Design tokens + shared UI foundation** | ~25 % | Tokens exist as TS data and mobile consumes them, but **Tailwind is not installed in web/admin** (no dependency, no config, no CSS entry) and no token→CSS bridge exists; `packages/ui` has one component; no primitives (button, input, field, layout, skeleton, empty/offline states) |
| 6 | **Background job system** | 0 % | `arq` is a declared dependency with no worker module, no enqueue seam, no job/outbox table, no retry/backoff policy, no worker process in Compose or Render, no queue health or CI check |
| 7 | **Analytics + error tracking wired** | 0 % | `SENTRY_DSN` / `POSTHOG_API_KEY` are config fields only — no initialisation anywhere (server, web or mobile), no event taxonomy, no dashboards or alert thresholds |
| 8 | **Mobile shell internals** | ~20 % | Environment profiles, bundle IDs and deep-link *config* exist. Missing: navigation, `expo-secure-store` usage, `expo-sqlite` offline store + **sync queue with idempotency keys**, push permission/token plumbing, in-app deep-link handling, launch/resume force-update check, offline/error states, e2e smoke scaffolding |
| 9 | **Admin shell internals** | ~5 % | Hello-world only: no login, no role gating, no audit trail view, no layout/navigation |
| 10 | **Acceptance harnesses** (money + permission) | 0 % | No real-Postgres integration harness (conftest points at a Postgres URL, but nothing creates/migrates a throwaway DB and CI runs no Postgres service, so no test currently touches the database), no object-permission harness, no property-based test dependency (Hypothesis), no float-usage lint rule (ADR-0008 §1) |
| 11 | **Performance budgets set in Phase 0, checked in CI** | 0 % | Targets exist only as prose in the brief; nothing measures or enforces them |

Also missing, and needed by Phase 0's own exit criteria: provisioning/verification of the **dev** environment (the deploy workflow reads Render hooks that may not be configured yet — Q6), and a `mypy` run (declared as a dev dependency, never executed in CI).

### 2.3 Explicitly not in Phase 0

Ledger *behaviour*, split-engine money maths and payouts (M6) · matching, cohorts and work delivery (M4/M5) · skills content and the task engine (M2) · V1 import tooling (M1) · Choose Path, onboarding, campus utility (M1) · external opportunities and Talent profile (M7) · company self-service, extra skill paths, automated matching (build later).

---

## 3. PR breakdown

Every PR: ≤ ~400 changed lines, one purpose, behind a flag where it is half-built, tests with the code, expand-only migrations, single Alembic head.

| PR | Title | Touches (folders/files) | ~Lines | Depends on |
|---|---|---|---|---|
| **0.1** | `identity` models: user, role, session/refresh, email token, consent, idempotency key, audit log | `apps/api/app/models/identity.py`, `app/models/admin.py` (new), `migrations/versions/*` | 350 | — |
| **0.2** | `academia` + `skills` models: session, semester, enrolment, topic, chunk, question bank, skill, category, path + step, lesson, task template, progress | `apps/api/app/models/academia.py`, `app/models/skills.py` (new), migration | 380 | 0.1 |
| **0.3** | `verification` + `matching` + `work` models | `apps/api/app/models/{verification,matching,work}.py` (new), migration | 380 | 0.1 |
| **0.4** | `quality` + `ledger` + `notifications` models (+ outbox, push token) | `apps/api/app/models/{quality,ledger,notifications}.py` (new), migration | 380 | 0.1 |
| **0.5** | API conventions: error envelope + handlers, request id, cursor pagination, idempotency store + replay, version guard, conventions doc | `apps/api/app/api/deps.py` (new), `app/core/errors.py` (new), `app/core/idempotency.py` (new), `app/main.py`, `docs/architecture/api-conventions.md` | 400 | 0.1 |
| **0.6** | Job system: ARQ worker, enqueue seam, job/outbox persistence, retry + backoff, queue health, Compose service | `apps/api/app/worker/` (new), `apps/api/pyproject.toml`, `docker-compose.yml`, `Makefile`, `docs/runbooks/jobs.md` | 380 | 0.1, 0.5 |
| **0.7** | Observability: Sentry (api/web/mobile) + PostHog (api/web/mobile), event taxonomy, structured logging with request id | `apps/api/app/core/observability.py` (new), `apps/web/src/lib/`, `apps/mobile/src/lib/` (new), `docs/observability.md` | 350 | 0.5 |
| **0.8** | Auth core for web/admin: Argon2id, access JWT + rotating refresh (reuse detection), cookie + CSRF, signup/login/verify/reset/refresh/logout/delete, rate limits, mail seam | `apps/api/app/api/v1/domains/identity/*` (new), `app/services/identity/*` (new), `app/core/mail.py` | 400 | 0.1, 0.5, 0.6 |
| **0.9** | Auth core for native + Google: ID-token verification (aud/iss/exp), PKCE flow config, secure-store token handling, refresh-in-flight, 426 handling | same domain + `apps/mobile/src/auth/*` (new), `apps/mobile/app.config.js` | 380 | 0.8 |
| **0.10** | Roles + permissions + audit + admin login (MFA) | `apps/api/app/core/authz.py` (new), `app/services/audit.py`, `apps/api/app/api/v1/domains/admin/*`, `apps/admin/src/*` | 400 | 0.8 |
| **0.11** | Web foundation: Tailwind + token bridge, `packages/ui` primitives, app shell (routing, error boundary, skeleton/offline states), bundle budget check | `apps/web/*`, `packages/ui/src/*`, `packages/design-tokens/*`, `tools/check_bundle_size.mjs` (new), `ci-js.yml` | 400 | 0.5, 0.7 |
| **0.12** | Mobile shell: navigation, secure storage, SQLite offline store + sync queue, push plumbing, deep links, force-update check, env badge | `apps/mobile/src/*` (new), `apps/mobile/app.config.js`, `apps/mobile/package.json` | 400 | 0.5, 0.7, 0.9 |
| **0.13** | Contract pipeline adopted: generate the typed client, enforce freshness, add auth/error/pagination types | `packages/api-client/src/generated/*` (new), `packages/contracts/src/index.ts`, `tools/gen_api_client.mjs`, `ci-contracts.yml` | 400 | 0.5, 0.8 |
| **0.14** | Test + CI harness: Postgres service in `ci-api` with real-Postgres fixtures, permission harness, **money harness** (Hypothesis) + no-float rule, `mypy`, roadmap reference fixes | `apps/api/tests/conftest.py`, `apps/api/tests/harness/*` (new), `.github/workflows/ci-api.yml`, `apps/api/pyproject.toml`, stale-reference fixes (§7) | 400 | 0.1–0.5 |

### 3.1 Streams (so two or three developers do not collide)

| Stream | Owner | PRs | Owns these paths |
|---|---|---|---|
| A — API + data | backend | 0.1–0.6, 0.8, 0.9 | `apps/api/**`, `apps/api/migrations/**` |
| B — web + admin | web | 0.7 (client side), 0.10 (admin UI), 0.11 | `apps/web/**`, `apps/admin/**`, `packages/ui/**`, `packages/design-tokens/**` |
| C — mobile | mobile (shared) | 0.7 (client side), 0.12 | `apps/mobile/**` |
| Shared, one writer at a time | any | 0.5, 0.13, 0.14 | `apps/api/app/api/deps.py`, `packages/contracts/**`, `packages/api-client/**`, `apps/api/tests/harness/**`, CI workflow files |

### 3.2 Order

`0.1 → (0.2, 0.3, 0.4 in parallel) → 0.5 → 0.6 → 0.7 → 0.8 → 0.9 → 0.10 → (0.11, 0.12) → 0.13 → 0.14`. Stream B can start 0.11's token/Tailwind work as soon as 0.5's error shape is fixed, and stream C can start 0.12's navigation/offline primitives against a mocked auth response before 0.9 lands.

### 3.3 Schedule reality (a decision for you, Q9)

Phase 0 as specified is roughly **3–4 weeks of one backend developer** (the model layer alone is four migrations). Inside a 1–3 month launch window that is a large share. If you want a shorter Phase 0, the trim I would propose is: move **0.4's ledger + quality models** to the phases that use them (M6/M5), keep every other PR, and accept that the money harness then lands with the ledger. I do **not** recommend trimming 0.5, 0.6, 0.8 or 0.14 — those are the reliability and security floor.

---

## 4. Tests and acceptance harnesses

| Level | What | Where |
|---|---|---|
| Unit | config validation, flags, version compare, error envelope, pagination, idempotency replay | `apps/api/tests/` |
| Integration (real Postgres) | throwaway DB created + migrated per run; repository and transaction tests | new `tests/harness/` + Postgres service in `ci-api` |
| Auth | Argon2id, rotation + **reuse detection**, CSRF, rate limit, Google ID-token verification (test key), account deletion | `tests/test_auth_*.py` |
| **Permission harness** (exit criterion) | object-level authorization: student A can never read/write B's records; role matrix for reviewer/ops/super; admin MFA gate | `tests/harness/permissions.py` |
| **Money harness** (exit criterion) | property-based: every posting set nets to zero; `student_payout = 90 %` exactly; department share always from the fee; rounding deterministic; no float in money paths | `tests/harness/money.py` (Hypothesis) |
| Migrations | single head; upgrade → downgrade → upgrade round trip on a throwaway DB; expand-only lint | `ci-api` |
| Contracts | OpenAPI export → generated client → `git diff --exit-code` (step 0.13 makes this real) | `ci-contracts` |
| Web | component tests for the shell/primitives + bundle budget check | `ci-js` |
| Mobile | typecheck (exists) + Maestro smoke against the dev build | `ci-mobile` / manual EAS |
| End-to-end | demo script in §11 run on dev | manual, per gate |

---

## 5. Performance budgets (set here, enforced from here on)

| Budget | Target | Checked by |
|---|---|---|
| Web first load (gzipped JS) | ≤ 150 KB | `tools/check_bundle_size.mjs` in `ci-js` (fails the build) |
| Web usable on throttled slow 4G, mid-range Android | Lighthouse mobile ≥ 80 perf | manual on dev per phase; automated later in M9 |
| API p95, common reads | < 300 ms | small k6/locust smoke on dev before each gate; budget test for `/health` + one real read in `ci-api` |
| Payloads | cursor pagination, sparse lists, gzip/brotli | conventions doc + contract tests |
| Images | served at requested size (CDN transform) | runbook + review checklist |
| Mobile download size | ≤ 30 MB, aggressive size report | EAS build report, reviewed per release |
| Loading UX | skeleton states, never spinners | `packages/ui` primitives + review checklist |

---

## 6. Risks (new ones; `07-risk-register.md` still stands)

| # | Risk | L | I | Mitigation |
|---|---|---|---|---|
| P1 | Phase 0 balloons and eats the launch window | H | H | Fixed PR list, ≤400 lines each, the trim in §3.3, a gate after 0.8 |
| P2 | Identity is the security boundary and is being built in-house | M | H | Spec in ADR-0009; rotation + reuse detection tested; external review before Phase 10 |
| P3 | Four migrations in one phase invite Alembic conflicts | M | M | One PR = one revision; `alembic heads` in CI; documented merge procedure (`04`) |
| P4 | Dev environment not actually provisioned, so "log in on dev" cannot be demonstrated | M | H | Manual steps §10 items 1–4 are on the critical path; the gate cannot pass without them |
| P5 | Mobile without a Mac delays iOS verification | M | M | Android emulator + real device locally; EAS cloud + TestFlight for iOS; Apple enrolment started now (Q7) |
| P6 | Offline/sync built before there is a real write to sync | M | L | Build the queue primitive in 0.12 but prove it on the first student write in M2 |
| P7 | Analytics/error tracking wired but unread | M | M | Event taxonomy + dashboard list is a deliverable of 0.7, not an afterthought |

---

## 7. Roadmap reconciliation (build-prompt Phases 0–10 ↔ old M0–M7)

The build prompt's scope wins. `docs/architecture/06-roadmap.md` has been rewritten accordingly: milestones are now numbered to match the phases (**M<N> = Phase <N>**), so the two documents cannot drift again.

| Build prompt | New milestone | Old roadmap | Difference (flagged) |
|---|---|---|---|
| Phase 0 — foundations & contracts | **M0** | M0 — Foundation (scaffolding only) | The old M0 ended at "green pipeline". Phase 0 adds the domain model, auth core, roles/audit, jobs, analytics, tokens wiring and the mobile/admin shells. **M0 grows substantially.** |
| Phase 1 — identity, V1 bridge, Choose Path | **M1** | M1 — Identity & Academia core | Old M1 also carried **academia materials + RAG** (build prompt puts those in Phase 8 → M8); old M1 was **missing Choose Path, onboarding and the Campus utility** (added). Kept: the exit criterion. |
| Phase 2 — skills engine + AI Data Annotation | **M2** | M2 — Skills: Learn → **Build → Verify** | **Verification moves out of M2** into its own phase: it needs a state machine, transcript and ops slice, which is Phase 3 in the build prompt. |
| Phase 3 — verification + Skill Transcript | **M3** | (tail of old M2) | Promoted to a milestone of its own. |
| Phase 4 — opportunities, matching, cohorts (internal first) | **M4** | M3 — Match → Work → Quality | Old M3 bundled matching, work **and** quality; the build prompt splits them across Phases 4 and 5, and makes Phase 4's ops slice primary. |
| Phase 5 — work delivery + quality control | **M5** | old M3 + **old M5 (Internal ops tools)** | The old **M5 milestone is retired**: the build prompt makes ops a slice inside *every* phase, not a phase of its own. |
| Phase 6 — money: ledger, earnings, payouts | **M6** | M4 — Earn (ledger) | Old M4 was thinner: Phase 6 adds the payout-provider abstraction (manual first), project value/status tracking, department-share records, reconciliation report + alerts, a second approver, and the property-based tests. |
| Phase 7 — Talent profile + external opportunities | **M7** | **absent** | The old roadmap never listed external (no-fee) opportunities or the evidence-only Talent profile. **Added.** |
| Phase 8 — Academia connected | **M8** | M6 — Academia focused fixes | Same content; the build prompt allows it to start after M1 **in parallel** with a second squad. |
| Phase 9 — mobile release | **M9** | M7 — Mobile (both platforms) | Materially different: old M7 implied mobile built at the end; the build prompt requires a **mobile slice inside every phase** (lockstep), so M9 is release hardening and stores only. |
| Phase 10 — hardening & launch | **M10** | **absent** | Load/soak, security review, backup drill, closed beta, pilot, flag gating, and the domain cutover (the steps existed in `03-versioning-and-domains.md`, but there was **no milestone**). **Added.** |

Unchanged: the "build later" list (more skill paths, automated matching, company self-service), the cross-cutting list (offline/idempotency, observability, flags, low-data budgets) and every ADR.

**Known stale references** caused by the renumbering — fixed in the same Phase 0 docs-sync PR, listed here so they are not forgotten: `apps/api/README.md` ("M1–M4"), `apps/admin/README.md` ("built first for M5"), `apps/mobile/README.md` ("built in M7"), `apps/api/app/models/academia.py` ("M1"). They are documentation comments only; nothing behaves differently.

---

## 8. Identity module sequencing (kickoff item 3)

Identity is the one slice that spans Phase 0 and Phase 1, so it is sequenced explicitly:

| Step | Where | Contents | Why here |
|---|---|---|---|
| 1 | **Phase 0 · PR 0.1** | Tables: user, profile, role, session/refresh token, email token, consent, idempotency key, audit log | Everything else (auth, audit, permissions, V1 bridge) needs these |
| 2 | **Phase 0 · PR 0.5** | Error envelope + idempotency store | Signup must be safely retryable on a flaky connection before it exists |
| 3 | **Phase 0 · PR 0.8** | Argon2id, access JWT + rotating refresh with reuse detection, cookie + CSRF path, signup/login/verify/reset/logout/delete, rate limits, mail seam | The single security boundary; built once, used by all four clients |
| 4 | **Phase 0 · PR 0.9** | Native flow (bearer + PKCE Google, secure storage) | Depends on 0.8's token shape being frozen |
| 5 | **Phase 0 · PR 0.10** | Roles, permissions, audit, admin login + MFA | Turns "logged in" into "allowed to", which every ops slice needs |
| 6 | **Phase 1 · first PR** | The V1 bridge: importer with dry-run + reconciliation, PBKDF2 verify + **rehash to Argon2 on first login**, "no usable hash and no `google_sub`" → reset path | Proves "Continue with your V1 account" before any other Phase 1 UI, using the permission/money-harness style dry-run report |
| 7 | **Phase 1 · then** | Onboarding/enrolment and Choose Path screens on web + mobile | Consumes the identity core as an ordinary authenticated feature |

Two deliberate choices: **(a)** the auth core lands in Phase 0 with no student-facing screens (it is exercised by tests and a placeholder "signed in as" page behind a flag), because Phase 1's importer and Phase 4's ops tools both depend on it; **(b)** the V1 hash-upgrade path is written in Phase 0 as a seam (`verify_legacy_hash` + rehash hook) but only *proven* in Phase 1 against real V1 hash fixtures taken from a read-only V1 snapshot — never from production data.

---

## 9. Open questions (batched — nothing here is answerable from the code)

**From the build prompt:**
1. **Task types + curriculum.** Which task types ship first (candidates: text classification, entity tagging, ranking/preference, transcription/translation incl. Nigerian languages, image labelling), and **who authors the AI Data Annotation curriculum**? It does not exist in the 20 website paths and must be created.
2. **Money decisions.** Currency for client billing and student payouts (NGN first?); the rounding rule for the 90/8/2 split (my proposal: largest-remainder, any remainder to the platform); **who approves payouts**, and at what threshold a **second approver** is required; which **identity checks** are needed before paying a student.
3. **Legal.** Minimum student age, and the consent + contributor terms required before real work starts (I will build the hooks only — no legal conclusions).
4. **Team + ownership.** How many developers, who owns which area for `CODEOWNERS`, and the target launch date?
5. **Mobile cadence.** Lockstep with web, or one phase behind? Your stated preference is lockstep for core journey screens — confirming that is the plan.

**From the code / my analysis:**
6. **Is the dev environment already provisioned?** `deploy-dev.yml` expects `RENDER_DEV_API_DEPLOY_HOOK`, `RENDER_DEV_WEB_DEPLOY_HOOK`, `RENDER_DEV_ADMIN_DEPLOY_HOOK`, and Phase 0's exit criterion requires logins **on dev**. Are the dev Render services, dev database/Redis and `api-dev.nelavista.com` / `admin-dev.nelavista.com` DNS in place, or must I list them as manual steps (§10)?
7. **Apple Developer enrolment** — started yet? It needs lead time, and Google Play already exists (audit §11.1). Who owns store accounts?
8. **`CODEOWNERS`** currently maps every path to `@hiipraise`. With 2–3 developers the file should name areas per person; what are the handles?
9. **Phase 0 size** — do you want the full four-migration model layer in Phase 0, or the trim in §3.3?
10. **Admin MFA method** (TOTP app is my assumption) and whether an IP allowlist is also wanted.
11. **Email provider** — see §10 item 5: **I recommend Resend** (SMTP or API, a test mode without a verified domain, free tier that covers auth mail, and it fits the existing `MAIL_*` settings). Postmark, SendGrid and MailerSend are equivalent choices; confirm one.
12. **Retention + consent copy** — who writes the privacy/consent text and what retention periods apply (needed by the deletion/export endpoints in 0.8)?
13. **`packages/ui`** is not listed in `01-target-structure.md`. Keep it (web/admin only, tokens shared with mobile) or fold its contents elsewhere?
14. **Launch gating** — which of the seven journey analytics events are must-have before real students see V2, and who watches the dashboards 0.7 delivers?

---

## 10. Manual steps only you can do (ordered, with lead times)

| # | Step | Where | Lead time |
|---|---|---|---|
| 1 | Confirm/create the **dev** environment: Render services (API, web static, admin static, Postgres, Redis, worker) and DNS for `api-dev` / `admin-dev` / `dev.nelavista.com` | Render + DNS | days |
| 2 | Set the dev deploy-hook secrets (`RENDER_DEV_API_DEPLOY_HOOK`, `RENDER_DEV_WEB_DEPLOY_HOOK`, `RENDER_DEV_ADMIN_DEPLOY_HOOK`) and the `dev` environment secrets | GitHub → Settings → Environments | hours |
| 3 | Add the dev API's env vars (`APP_ENV=dev`, `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `CORS_ORIGINS`, mail, Google, Sentry, PostHog, Cloudinary) — names only, values never in git | Render | hours |
| 4 | Create **separate dev** Google OAuth client + native iOS/Android client IDs, and the dev Cloudinary folder | Google Cloud Console | hours |
| 5 | Confirmed email provider account: **Resend** (or Postmark/SendGrid) — verify `nelavista.com` with SPF/DKIM/DMARC and create dev + prod keys | Resend + DNS | hours–day |
| 6 | Sentry and PostHog **projects per environment** (dev separate from prod) + the alert recipients | Sentry, PostHog | hours |
| 7 | **Apple Developer Program** enrolment (no Mac fallback) and the EAS project ID + credentials | Apple, Expo | days–weeks |
| 8 | Branch protection: `develop` (CI required) and `main` (CI + your approval), plus `release/v1` when we get to launch | GitHub | minutes |
| 9 | Rotate every credential in `docs/SECRETS_ROTATION.md` (risk R1 — still open) | provider consoles | hours |
| 10 | Answers to §9 | — | — |

---

## 11. Gate output

**Done in this step:** the plan itself — gap analysis, PR breakdown with owners, test plan, budgets, risks, roadmap reconciliation (roadmap doc updated), identity sequencing, questions and manual steps.
**Not done (deliberately):** every line of Phase 0 code. Nothing outside `docs/` was touched; V1 was not touched; no database was read or written; no secrets were printed.

**Files changed:** `docs/build/phase-0-plan.md` (new), `docs/architecture/06-roadmap.md` (reconciled), and `v2_build.txt` (the pasted brief, removed — its build-prompt body is already tracked at `docs/build/nelavista-02-v2-build-prompt.md`, and its kickoff context is addressed in §§0–11 of this document).

**Test results:** none applicable — documentation only. The path-filtered jobs (api, js, mobile, contracts, v1) cannot trigger because nothing outside `docs/` changed; the only workflow that runs unconditionally is the secret scan (`security`), which documentation cannot affect. I ran `prettier --check "docs/**/*.md"` (passes) and grepped for stale milestone references (the four in §7).

**Demo script for Phase 0 (to run when the phase is built, on dev):**
1. **Web:** open `https://dev.nelavista.com` → sign up with a real address → receive the verification mail (dev sender) → verify → land signed-in with a placeholder page showing role `student`.
2. **Android:** open the dev build on a phone → Google sign-in → kill the app mid-action → relaunch → the pending action syncs once, not twice (idempotency).
3. **iPhone:** same flow via TestFlight; then set `mobile.ios.min_supported` one patch above the build in `versions.json`, redeploy the API, relaunch the app → blocking "Please update" screen.
4. **Admin:** open `https://admin-dev.nelavista.com` → log in with MFA → see the audit trail containing the actions from steps 1–3 → confirm a student account cannot reach any admin route.
5. **Job system:** trigger a password-reset mail and watch the job succeed in the queue health view; kill Redis for one request and confirm the retry queue recovers.

**Open questions:** §9 (14 items).
**Manual steps:** §10 (10 items).

---

## 12. Answers received (2026-10-16) — decisions now binding

| # | Question | Answer |
|---|---|---|
| 1 | Phase 0 size | **Take the §3.3 trim**: PR 0.4's quality + ledger models move to M5/M6; every other PR stands. 0.4's notifications / push-token / outbox content folds into **0.6 (job system)**. |
| 2 | Email provider | **Resend** — test mode in dev, Mailpit locally. |
| 3 | Mobile cadence | **Lockstep** with web for the core journey screens. |
| 4 | Payout rounding | **Largest-remainder**, leftover to the platform; the PRD's $10,000 example is the test case. |
| 5 | Currency | Store the currency **on every project and ledger entry**; never hardcode one. Client-billing and payout currency confirmed before M6. |
| 6 | Payout approval | Founder approves; a **second approver above a threshold set before M6**. |
| 7 | Minimum age | **18** (pending legal review) — build the **hooks only** (consent kinds + age fields, no enforcement). |
| 8 | Dev environment | Not confirmed as provisioned → **build against local Docker, mock the rest**, and hand over the exact Render/DNS/env-var list (manual steps in every PR). |
| 9 | Apple enrolment / team size / CODEOWNERS | Unconfirmed → assume **not started**; team assumed 2–3 developers per ADR-0001; CODEOWNERS stays `@hiipraise` for all paths. |
| 10 | Admin MFA | **TOTP authenticator app**. |
| 11 | Task types + curriculum | Decided before M2; **must not block M0 or M1**. |
| 12 | Everything else | Implement my recommended default and **flag each one in the PR description**. |

**RUN MODE (given with the approval):** build 0.1 → 0.14 in the §3.2 dependency order, **one PR at a time** against `develop`; wait for CI to go green and for the founder to merge before starting the next; **no branch stacking**; no approval stops between PRs; stop only if CI cannot be fixed, a manual step blocks, or a build-prompt rule would be broken. Phase 0 gate report after 0.14, then the Phase 1 plan and a wait for approval. Gates remain mandatory after M3, M6 and M10.

**Defaults adopted because of #8, #9 and #12** (flagged in the relevant PR):
- dev infrastructure is treated as **not provisioned** — all Phase 0 work runs against local Docker + mocks, and every PR lists the console steps to do later.
- **Apple Developer enrolment assumed not started**; team size assumed 2–3 developers (ADR-0001).
- Postgres/Redis stay on Render (ADR-0002); admin MFA is **TOTP**; retention periods are defined at M10 with legal.
- `packages/ui` stays, web/admin only, with tokens shared with mobile (recorded in `01-target-structure.md` when 0.11 lands).

---

**Approved 2026-10-16** — Phase 0 build starts at PR 0.1.
