# V2 remaining work — live tracker

Last updated: 2026-10-18 (A1/A2, B4/B5, first slice of B12 and the resend endpoint).

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
  (125 paths) is committed, `tools/gen_api_client.mjs` runs the CLI through Node
  so it works on Windows too, and `ci-contracts.yml` now regenerates and diffs
  every PR. `openapi.json` is a gitignored build artifact. Generated types are
  re-exported from `@nelavista/api-client` (`MeOut`, `TokenOut`, `ProfileOut`,
  `Schemas`, `ApiPaths`); web uses them for `/auth/me` and the session token.
- [x] **A2** Shared V2 response types are in `packages/contracts`: dashboard
  (five questions, next action, topic stat), campus, plus the existing auth,
  onboarding and enrolment types. `Me`/`AuthToken` were **removed** from
  contracts because the generated schema now owns them.
- [ ] **A3** Give the `dict`-returning journey routes (`/academia/dashboard`,
  `/me/campus`, …) real `response_model`s, then move the hand-written contract
  types onto the generated schema. Until then those shapes are hand-maintained.

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
- [ ] **B6** Skills overview, path, lesson reader, practice task and my-learning
  (`/v1/skills/*`), including offline-safe answer saving once the offline store
  exists (D1).
- [ ] **B7** Verification: assessment sitting, result, transcript.
- [ ] **B8** Opportunities list/detail with "why you qualify or what's missing".
- [ ] **B9** Work: assignments, submit (idempotency key per submission), rework.
- [ ] **B10** Earnings screen with per-line explanations.
- [ ] **B11** Settings: languages, availability, notifications, data export,
  in-app account deletion (store requirement).
- [~] **B12** Performance budgets. Done: route-level code splitting (`Home`,
  `Onboarding`, `Academia`, `Campus` are lazy; landing/login/signup stay eager),
  skeleton states instead of spinners, and a first measurement — the production
  build's entry is **58.1 KB gzipped JS** plus 1.2 KB CSS, with each lazy route
  1.1–1.8 KB gzipped. Still owed: enforce the budget in CI and optimise the
  icons/screenshots.

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
  home banner. Covered by two service tests.
- [ ] **F8** `POST /auth/email/resend-verification` does not exist, so the web app
  can only show the "confirm your email" banner and cannot re-send the link.
  Needs the route, the mail template and a rate limit.
- [ ] **F9** `apps/web` still has no route-level code splitting: the first load is
  ~59 KB gzipped of JS today, but B12's ≤150 KB budget must be enforced in CI
  before the surface grows.

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
