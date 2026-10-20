# V2 remaining work — live tracker

Last updated: 2026-10-20 (Phases 0–6 delivered; 7–8 API-only; 9–10 in release
mode. E3/E4 docs, D4/D5 store + release, F2/F5/F6 infrastructure landed, and the
whole suite was run green — see Verification below).

This is the single list of everything still to do for V2, in the order I intend to
work through it. It exists so progress is visible while the work happens and so
nothing on it gets forgotten. The build prompt's rules still apply: V1 untouched,
no production data, small changes behind feature flags, tests with the code.

Status legend: `[ ]` to do · `[~]` in progress · `[x]` done · `[!]` blocked on you
or on an external decision.

## Verification (2026-10-20)

Run after the last code change, not before it. Every line below is a command that
was executed and its real result.

| Check | Command | Result |
|---|---|---|
| API suite | `pytest -q --ignore=tests/test_migrations.py` | **283 passed** |
| Migrations (SQLite round trip, heads, model agreement) | `pytest -q tests/test_migrations.py` | **5 passed, 1 skipped** (Postgres case skips without `POSTGRES_TEST_URL`) |
| Web DOM/unit | `npx vitest run` in `apps/web` | **38 passed** (7 files) |
| Admin DOM | `npx vitest run` in `apps/admin` | **1 passed** |
| Mobile core (queue, deep links, versions) | `npx vitest run` in `apps/mobile` | **10 passed** |
| Typechecks | `tsc --noEmit` in web, admin, mobile | **0 errors** each |
| Lint | `ruff check` (api, tools), `eslint src` (web, admin) | **clean** |
| First-load budget | `node tools/check_web_budget.mjs` after `vite build` | **58.4 KB JS + 1.4 KB CSS** of 150/20 KB |
| Typed client freshness | `node tools/gen_api_client.mjs --schema openapi.json` | regenerated; diffs are committed here |
| Load-test tool | offline: percentile/report maths, over-budget exit 1, unreachable API exit 2 | **works**; no live measurement yet (F6) |

Fixed while verifying (they were real defects, not test noise): the typed client
was stale after the new response models (regenerated); `CandidateListOut` silently
dropped the candidate's name; a passing practical could not move verification from
unverified because the state machine requires `in_progress` first; the scheduler
counted an existing day's job as new on every tick; the new migration's timestamps
were nullable against the models; and a handful of screens lost null-narrowing
against the stricter generated types.

## Decisions taken (were open questions)

- **Money rounding rule: approved as documented.** `fee = round_half_up(10% of
  total)`, `department = round_half_up(20% of fee)`, `platform = fee − department`,
  `students = total − fee`; per-student allocation is largest remainder with ties
  by ascending user id. Leftover minor units land with the platform, never with
  the student pool or the department. Recorded in ADR-0011.
- **Mobile ships in lockstep with web** for the core journey screens (D2).
- **TOTP** is the staff second factor (C8/F1); **Resend** is the email provider.

## A. Contracts and tooling

- [x] **A1** Typed client generation adopted. `packages/api-client/src/generated/schema.d.ts`
  is committed, `tools/gen_api_client.mjs` runs on Windows, `ci-contracts.yml`
  regenerates and diffs every PR. Generated types are re-exported from
  `@nelavista/api-client`.
- [x] **A2** Shared V2 types live in `packages/contracts`; the generated schema owns
  the rest.
- [x] **A3** The routes the student journey reads have real `response_model`s.
  The routes no client reads yet (materials, CBT, Ask, talent, money, ops) still
  return plain `dict`s; each gets its model when a typed client needs it — see
  B14/B13.

## B. Web PWA (`apps/web`) — student journey

- [x] **B1** Sign in / register / **verify-email landing** / **password reset**,
  session refreshed from the httpOnly cookie, access token in memory, single-flight
  refresh on 401. Resend is wired into the home banner (F8).
- [x] **B2** Onboarding wizard (university → faculty → department → courses) writing
  real enrolments, **level filter** and the **waitlist path** included.
- [x] **B3** Choose Path + profile basics, switching that never loses learning,
  proof or earnings.
- [x] **B0** Web test harness: Vitest + jsdom, route-guard, CSRF, error-envelope
  and single-flight tests.
- [x] **B-fix** Dev/preview proxy no longer forwards `/api/v1/...` unchanged.
- [x] **B4** Academia dashboard with the five questions, the single next action and
  its reason, skeletons, and the flag-off state.
- [x] **B5** Campus utility page, map links from coordinates.
- [x] **B6** Skills overview, detail, path, lesson reader, practice, my-learning,
  all typed. The practice form is generated from the template schemas; markdown is
  an in-repo subset with a link allow-list.
  **Remaining:** offline-safe answer saving (the mobile queue exists; web does not).
- [x] **B7** Verification hub, sitting, review and transcript, with resume, form
  generation, expiry and zero-for-unanswered.
  **Remaining:** a re-verification prompt after a suspension.
- [x] **B8** Opportunities list/detail with "why you qualify or what's missing".
- [x] **B9** Work: assignments, idempotent submission, rework, messages.
- [x] **B10** Earnings screen with per-line explanations.
- [x] **B11** Settings: languages, availability, notifications, data export,
  in-app account deletion.
- [x] **B12** Performance budgets: route-level splitting, skeletons, and
  `tools/check_web_budget.mjs` enforcing 150 KB JS / 20 KB CSS in CI
  (last measurement **58.4 KB JS + 1.4 KB CSS** after the journey screens
  landed). Store assets are D4.
- [ ] **B13** **Talent profile and shares (Phase 7 UI).** The API is complete and
  tested (`/talent/me`, `/talent/me/shares`, revoke, public share token) but no web
  or mobile screen shows the evidence-only profile or lets a student create and
  revoke a share. Needs typed `response_model`s first (A3).
- [ ] **B14** **Academia connected screens (Phase 8 UI).** Materials list/search/
  reader, Ask Nelavista (course-aware, honest decline) and CBT results are
  implemented in the API and used by nothing. Needs typed `response_model`s, then
  web + mobile screens in lockstep.

## C. Admin ops (`apps/admin`)

- [x] **C1** Login, role gating (students refused), audit trail.
- [x] **C2** Import runs: upload the V1 export, dry-run, apply, reconciliation.
- [x] **C3** User lookup and support view.
- [x] **C4** Opportunities, requirements, candidate list with explanations, cohorts,
  invites, replacements.
- [x] **C5** Review queue, quality record, consequences, override with a reason.
- [x] **C6** Money: funding, financials, payout batches, second approver, ledger
  explorer, CSV exports, reconciliation.
- [x] **C7** Content: paths, lessons, steps, task templates, draft/publish.
- [x] **C8** Mandatory TOTP for staff, enforced in the shell and by the API, with
  recovery codes shown once.

## D. Mobile (`apps/mobile`) — iOS and Android

- [x] **D1** Shell: navigation, SecureStore tokens, SQLite offline queue with an
  idempotent retry and backoff, deep/universal links, push registration, EAS
  profiles. Covered by `mobile-core.test.ts`.
- [x] **D2** Journey screens in lockstep with B1–B11 (auth, home, learning,
  proof, opportunities, work, earnings, notifications, settings).
  **Remaining:** B13/B14 screens when those land.
- [x] **D3** Minimum-version and force-update: server `426` + blocking screen,
  store link, comparison helpers and `versions.json` policy.
- [~] **D4** Store readiness (`docs/store/mobile-store-readiness.md`): generated
  icon/adaptive/splash (`tools/gen-mobile-assets.mjs`, wired into
  `app.config.js`), listing copy, data-safety table, review notes, test-account
  plan, in-app deletion, policy re-check notes and a pre-submission checklist.
  **Owed:** real-brand assets and store screenshots/feature graphic captured from
  a release build (mock-ups are rejected).
- [x] **D5** Release pipeline: `.github/workflows/mobile-release.yml` builds only
  from `v*.*.*` tags, requires the `production-mobile` approval, fails when the tag
  and `expo.version` disagree, submits to TestFlight/Play, and documents staged
  rollout and rollback (`docs/runbooks/mobile-release.md`).
  **Owed:** a device smoke run (Maestro) on the first dev build.

## E. Docs

- [x] **E1** ADR-0011 records the rounding and largest-remainder rules.
- [x] **E2** ADR-0012 records that mobile ships in lockstep with web.
- [x] **E3** `docs/build/phase-1-10-plan.md`: per-phase scope, delivered state,
  evidence, owed items, the build-prompt ↔ milestone mapping and every flagged
  difference. Phase 0 keeps its own gap analysis in `phase-0-plan.md`.
- [x] **E4** `docs/architecture/06-roadmap.md` has a delivery-status table and the
  stale milestone references in the API/admin/mobile READMEs and the academia
  model are fixed.
- [x] **E5** Runbooks: local setup, deploy dev/prod, mobile local setup, mobile
  release, **load test**, restore, rollback, secrets rotation, domain switch.

## F. Server follow-ups found while building

- [x] **F1** Two-factor for staff (schema, TOTP service, routes, admin UI, recovery
  codes, login challenge). Covered by `test_two_factor_and_delivery.py`.
- [x] **F2** Real Postgres execution of the migration suite in CI: the
  `migrations-postgres` job starts a `postgres:16` service and
  `test_migrations_execute_on_postgres` applies, reverses and re-applies the real
  DDL (skips locally when `POSTGRES_TEST_URL` is unset).
- [x] **F3** Daily reconciliation on the worker: `worker/scheduler.py` enqueues
  `reconcile:{YYYY-MM-DD}` with a date key, and the worker loop calls it every
  tick, so one day produces one run.
  **Owed:** watch the first run in an environment.
- [x] **F4** Push delivery wired: `push_devices` (unique token, reassigns on
  re-login), `POST/DELETE /me/push-devices`, a `send_push` job and the
  `PUSH_ENDPOINT` doc. In-app rows always exist; push is best-effort.
- [x] **F5** Rate limiting on money reads/writes and on the review/quality routes
  (auth routes were already covered); the store is in-process until Redis is wired.
- [x] **F6** Read-path load test: `tools/load_read_paths.py` measures the eleven
  journey GETs, reports p50/p95/p99 and row counts, fails over the 300 ms p95
  budget, and warns when the dataset is too small to trust
  (`docs/runbooks/load-test.md`, `make load-test`).
  Verified offline: percentile maths, the pass/fail report exits (0/1) and the
  unreachable-API exit (2).
  **Owed:** an actual DEV run with representative volumes — the tool is proven,
  the measurement is not.
- [ ] **F7** Content: the AI Data Annotation curriculum (lessons, practice samples,
  gold tasks, assessment items) — needs your authoring decision (G4).
- [x] **F8** `POST /auth/email/verify/resend` with a per-account limit and a
  "send the link again" action on the home banner.
- [x] **F9** The verification email now links to the web screen, and
  `/auth/verify` exists to consume it (signed out is fine).

## G. Open questions for you

- [ ] **G1** Currency for client billing and student payouts (the ledger is
  currency-agnostic; something must be chosen and seeded).
- [ ] **G2** Who approves payouts, the second-approver threshold, and the identity
  checks required before paying a student.
- [ ] **G3** Minimum student age, consent wording and contributor terms before any
  real work starts.
- [ ] **G4** The first task types and who authors/owns the AI Data Annotation
  curriculum.
- [ ] **G5** Team size and area ownership (to make CODEOWNERS true again), and the
  target launch date.

## H. Local hygiene

- [x] **H1** `apps/api/.venv` is gitignored.
- [ ] **H2** Decide whether to delete `apps/api/.venv` or keep it as the documented
  local interpreter.
- [x] **H3** `packages/api-client/src/generated/schema.d.ts` is committed and the
  freshness gate passes locally.
