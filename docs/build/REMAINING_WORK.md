# V2 remaining work — live tracker

Last updated: 2026-10-18 (web client slice landed on `feat/v2-journey-services`).

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
  the student pool or the department. To be recorded in an ADR (E1).
- **Mobile ships in lockstep with web** for the core journey screens (D-work
  follows B/C screen by screen).

## A. Contracts and tooling

- [x] **A2 (partial)** Shared types for the auth session, profile, taxonomy and
  onboarding now live in `packages/contracts` and are imported by web. The other
  domains (dashboard answers, verification status, opportunity match, assignment,
  earning line) still need the same treatment when their screens land.
- [ ] **A1** Adopt typed client generation: add `openapi-typescript` to the
  workspace, export `openapi.json` from `app.main`, run
  `node tools/gen_api_client.mjs --schema openapi.json`, commit
  `packages/api-client/src/generated/schema.d.ts`. This turns the
  `ci-contracts.yml` skip-notice into a real freshness gate.
- [ ] **A2** Publish shared V2 response types in `packages/contracts` (auth
  session, enrolment, dashboard answers, verification status, opportunity match,
  assignment, earning line) so web/admin/mobile cannot drift from the API.

## B. Web PWA (`apps/web`) — student journey

Goal: the Phase 0 acceptance line, "a developer can log in on web against local
and dev", then the Phase 1 journey.

- [x] **B1** Sign in / register screens against `/v1/auth/*`, with the session
  refreshed from the httpOnly cookie on boot, the access token kept in memory and
  single-flight refresh on 401. **Remaining:** the verify-email screen (the API
  has `/auth/email/verify` but no resend endpoint — see F8) and password reset.
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
- [ ] **B4** Academia dashboard, answering the five questions from
  `/v1/academia/dashboard`, with honest empty states.
- [ ] **B5** Campus utility page (`/v1/me/campus`).
- [ ] **B6** Skills overview, path, lesson reader, practice task and my-learning
  (`/v1/skills/*`), including offline-safe answer saving once the offline store
  exists (D1).
- [ ] **B7** Verification: assessment sitting, result, transcript.
- [ ] **B8** Opportunities list/detail with "why you qualify or what's missing".
- [ ] **B9** Work: assignments, submit (idempotency key per submission), rework.
- [ ] **B10** Earnings screen with per-line explanations.
- [ ] **B11** Settings: languages, availability, notifications, data export,
  in-app account deletion (store requirement).
- [ ] **B12** Performance budgets: ≤150 KB gzipped JS first load, route-level code
  splitting, skeleton states (no spinners), image optimisation; checked in CI.

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

- [ ] **E1** ADR: the approved money rounding rule (extends ADR-0008).
- [ ] **E2** ADR or note: mobile ships in lockstep with web.
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
- [ ] **H3** `packages/api-client/src/generated` — confirm the generator's output
  is committed once A1 lands so CI freshness passes on the first try.
