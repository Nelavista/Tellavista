# V2 remaining work — live tracker

Last updated: 2026-10-18 (B7: the verification journey, typed end to end).

This is the single list of everything still to do for V2, in the order I intend to
work through it. It exists so progress is visible while the work happens and so
nothing on it gets forgotten. The build prompt's rules still apply: V1 untouched,
no production data, small changes behind feature flags, tests with the code.

Status legend: `[ ]` to do · `[~]` in progress · `[x]` done · `[!]` blocked on you
or on an external decision.

## Decisions taken (were open questions)

- **Money rounding rule: approved as documented.** `fee = round_half_up(10% of
  total)`, `department = round_half_up(20% of fee)`, `platform = fee − department`,
  `students = total − fee`; per-student allocation is largest remainder with ties
  by ascending user id. Leftover minor units land with the platform, never with
  the  student pool or the department. Recorded in ADR-0011 (E1).
- **Mobile ships in lockstep with web** for the core journey screens (D-work
  follows B/C screen by screen).

## A. Contracts and tooling

- [x] **A1** Typed client generation adopted. `packages/api-client/src/generated/schema.d.ts`
  (126 paths) is committed, `tools/gen_api_client.mjs` runs the CLI through Node
  so it works on Windows too, and `ci-contracts.yml` now regenerates and diffs
  every PR. `openapi.json` is a gitignored build artifact. Generated types are
  re-exported from `@nelavista/api-client` (`MeOut`, `TokenOut`, `ProfileOut`,
  `Schemas`, `ApiPaths`); web uses them for `/auth/me` and the session token.
- [x] **A2** Shared V2 types live in `packages/contracts`: the money and status
  unions, the page/cursor envelope, the error envelope and the onboarding and
  enrolment shapes. `Me`/`AuthToken` were **removed** because the generated schema
  owns them, and A3 removed the dashboard/campus copies for the same reason —
  contracts now holds only what the API has no model for yet.
- [x] **A3** The routes the student journey reads have real `response_model`s:
  the Academia dashboard, `/me/campus` and all of `/v1/skills` (plus
  `lesson_slug` on a path step, so a path can link into the reader). The
  hand-written journey interfaces are **gone** from `packages/contracts`; web
  imports `DashboardOut`, `CampusOut`, `PathOut`, … from the generated client.
  The routes no client reads yet (materials, CBT, Ask, work, money, ops) still
  return plain `dict`s; each gets its model when a typed client needs it, and
  `schema.ts` says so. Verification got its models in B7.

## B. Web PWA (`apps/web`) — student journey

Goal: the Phase 0 acceptance line, "a developer can log in on web against local
and dev", then the Phase 1 journey.

- [x] **B1** Sign in / register screens against `/v1/auth/*`, with the session
  refreshed from the httpOnly cookie on boot, the access token kept in memory and
  single-flight refresh on 401. **Remaining:** the verify-email landing screen and
  password reset. (Resend now exists server-side and is wired into the home
  banner — F8.)
- [x] **B2** Onboarding wizard: university → faculty → department → courses
  against `/v1/onboarding/*`, writing real enrolments and completing onboarding.
  **Remaining:** the level filter (the API takes `?level=`, the UI shows levels
  but does not filter) and the waitlist path for an uncovered university.
- [x] **B3** Choose Path + profile basics (`/v1/me`, `/v1/me/path`), with
  switching that never loses learning, proof or earnings.
- [x] **B0** Web test harness: Vitest + jsdom, `pnpm --filter @nelavista/web test`,
  covering CSRF, error-envelope parsing and single-flight refresh. Extend it to
  the route guards when the remaining screens land.
- [x] **B-fix** The dev/preview proxy was forwarding `/api/v1/...` to the API
  unchanged (every call 404'd); both `apps/web` and `apps/admin` now strip `/api`.
- [x] **B4** Academia dashboard at `/academia`: the five questions, the single
  next action with its reason, skeletons while loading, and an explicit
  "not switched on here" state when `FLAG_ACADEMIA_CONNECT` is off.
- [x] **B5** Campus utility page at `/campus`: university-scoped info and map
  points, with map links built from coordinates (no map SDK in the bundle).
- [x] **B6** Skills overview, skill detail, path with ordered steps and real
  progress, lesson reader, practice task and my-learning, all against
  `/v1/skills/*` and all typed from the generated schema. The practice form is
  generated from the template's own schemas (`lib/practice.ts`), and an
  unsupported task type says so instead of submitting a meaningless answer. The
  lesson body is rendered by a small in-repo markdown subset (`lib/markdown.ts`)
  with a `http(s)`/relative link allow-list — no markdown library in the bundle.
  **Remaining:** offline-safe answer saving once the offline store exists (D1).
- [x] **B7** Verification at `/verification`, `/verification/assessments/:slug`,
  `/verification/attempts/:id` and `/transcript`, all typed from response models
  added to the verification routes. The sitting resumes an open attempt (a lost
  connection is not a lost try), renders the form from the template's own
  schemas (the same generator as practice) and names the expiry. Unanswered tasks
  score zero and the page says so; a task with no template says it cannot be
  rendered instead of submitting noise. Expected answers appear only on the
  review screen, whose route refuses to serve them before submission. The hub
  states plainly that lessons and practice are not proof, and the transcript
  groups learned/proved/delivered with the evidence id on every line. Covered by
  an API end-to-end route test and three DOM tests.
  **Remaining:** practical-task submission (brief + rubric + a real form) and a
  re-verification prompt after a suspension.
- [ ] **B8** Opportunities list/detail with "why you qualify or what's missing".
- [ ] **B9** Work: assignments, submit (idempotency key per submission), rework.
- [ ] **B10** Earnings screen with per-line explanations.
- [ ] **B11** Settings: languages, availability, notifications, data export,
  in-app account deletion (store requirement).
- [~] **B12** Performance budgets. Done: route-level code splitting (every
  signed-in screen is lazy; landing/sign-in/sign-up stay eager), skeleton states
  instead of spinners, and **enforcement** — `tools/check_web_budget.mjs` reads
  the built `index.html`, gzips what the first load actually pulls, and fails the
  CI job over 150 KB JS / 20 KB CSS (`pnpm check:web-budget`). Current
  measurement: **57.2 KB gzip JS + 1.3 KB CSS**, lazy routes 0.4–2.5 KB each.
  Still owed: optimise the icons/screenshots (store assets, D4).

## C. Admin ops (`apps/admin`)

- [ ] **C1** Login, role gating and the audit trail view.
- [ ] **C2** Import runs: upload the V1 export, dry-run, apply, reconciliation.
- [ ] **C3** User lookup and support view.
- [ ] **C4** Opportunities: create/edit, requirements, candidate list with
  explanations; cohorts and invitations; replacements.
- [ ] **C5** Review queue, quality record, consequences, override with a reason.
- [ ] **C6** Money: funding, financials, payout batches (create → approve →
  pay), second-approver rule, ledger explorer and CSV exports, reconciliation.
- [ ] **C7** Content management: paths, lessons, steps, task templates with the
  draft/publish flow.
- [ ] **C8** Two-factor for admin accounts (Phase 0 security requirement, not yet
  built server-side either — see F1).

## D. Mobile (`apps/mobile`) — iOS and Android

- [ ] **D1** Shell internals: navigation, secure token storage, offline store with
  an idempotent sync queue and retry, deep links/universal links, push
  registration, per-environment build profiles (EAS).
- [ ] **D2** Journey screens in lockstep with B1–B11, reusing shared logic
  packages rather than sharing components.
- [ ] **D3** Minimum-version and force-update flow (the API already answers 426).
- [ ] **D4** Store readiness: icons, screenshots, listings, privacy/data-safety
  declarations, in-app account deletion, review notes and test accounts; verify
  current Apple and Google policies (payments/earnings rules change).
- [ ] **D5** Release pipeline: signed builds from tags, staged rollout,
  TestFlight and Play internal/closed testing, rollback path.

## E. Docs

- [x] **E1** ADR-0011 records the money rounding and largest-remainder rules;
  `services/money/split.py` now cites it as approved.
- [x] **E2** ADR-0012 records that mobile ships in lockstep with web.
- [ ] **E3** `docs/build/phase-N-plan.md` for Phases 0–10, starting with the
  Phase 0 gap analysis, plus the build-prompt ↔ roadmap (M1–M7) mapping table and
  every flagged difference.
- [ ] **E4** Update `docs/architecture/06-roadmap.md` where the build prompt's
  scope wins over the roadmap.
- [ ] **E5** Runbooks: local setup with the new flags and seed data; the DEV demo
  script from PR #13 made reproducible.

## F. Server follow-ups found while building

- [ ] **F1** Two-factor authentication for staff accounts (schema + routes + admin
  UI hook; C8 depends on it).
- [ ] **F2** Real Postgres execution of the migration suite in CI (the current
  test runs the SQLite round-trip and compiles Postgres DDL offline; the PR 0.14
  service container is still owed).
- [ ] **F3** Daily reconciliation job on the worker (the service and endpoint
  exist; nothing schedules it yet).
- [ ] **F4** Push delivery wired to a real endpoint per environment
  (`PUSH_ENDPOINT` is documented and unset, so notifications are in-app only).
- [ ] **F5** Rate limiting on the money and review routes (auth routes are covered;
  the store is in-process until Redis is wired).
- [ ] **F6** Load test the read paths against the p95 < 300 ms budget on
  representative data volumes.
- [ ] **F7** Content: the AI Data Annotation curriculum itself (lessons, practice
  samples, gold tasks, assessment items) — needs your authoring decision (G4).
- [x] **F8** `POST /auth/email/verify/resend` (authenticated, 3/5 min per account,
  invalidates the previous link) and a "send the link again" action on the web
  home banner. Covered by two service tests and one route test.
- [ ] **F9** The verification email body is still the relative path
  `/auth/verify?token=…` rather than an absolute link to a screen, and the web app
  has no verify-email landing route to consume it. The endpoint exists; the
  template and that screen are owed (part of B1).

## G. Open questions for you

- [ ] **G1** Currency for client billing and student payouts (the ledger is
  currency-agnostic; something must be chosen and seeded).
- [ ] **G2** Who approves payouts, and the identity checks required before paying
  a student.
- [ ] **G3** Minimum student age, consent wording and contributor terms before any
  real work starts.
- [ ] **G4** The first task types and who authors/owns the AI Data Annotation
  curriculum.
- [ ] **G5** Team size and area ownership (to make CODEOWNERS true again), and the
  target launch date.

## H. Local hygiene

- [x] **H1** `apps/api/.venv` is gitignored (created only to run the suite here).
- [ ] **H2** Decide whether to delete `apps/api/.venv` or keep it as the documented
  local interpreter.
- [x] **H3** `packages/api-client/src/generated/schema.d.ts` is committed and the
  freshness gate passes locally (regenerate → no diff).
