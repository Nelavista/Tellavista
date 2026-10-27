# V2 remaining work - build tracker

> **Build history, not the UI readiness list.** This tracker records the
> implementation work through 2026-10-27. For the current public/auth/app/admin
> screen gaps and the launch blockers, use `docs/v2-ui/AUDIT.md` and
> `docs/v2-ui/ROUTE-MAP.md`.

Last updated: 2026-10-27 (Phases 0-10 delivered as code. B13/B14 now have typed
contracts and web + mobile screens, F7 curriculum is seeded, G1-G5 are policy plus
admin controls, the B6 answer drafts and B7 re-verification prompt are closed, and
the API suite was run green - see Verification below. UI readiness is tracked
separately in `docs/v2-ui/AUDIT.md`).

This is the build list still to do for V2, in the order it was worked through. It
exists so progress is visible and nothing gets forgotten. UI readiness and the
missing public/app/admin screens are tracked separately in
`docs/v2-ui/AUDIT.md`. The build prompt's rules still apply: V1 untouched, no
production data, small changes behind feature flags, tests with the code.

Status legend: `[ ]` to do · `[~]` in progress · `[x]` done · `[!]` blocked on you
or on an external decision.

## Verification (2026-10-27)

Run after the last code change, not before it. Every line below is a command that
was executed and its real result.

| Check | Command | Result |
|---|---|---|
| API suite (including migrations) | `pytest -q` in `apps/api` | **332 passed, 1 skipped** (333 collected; 10m 42s) |
| Web DOM/unit | `npx vitest run` in `apps/web` | **53 passed** (10 files) |
| Admin DOM | `npx vitest run` in `apps/admin` | **1 passed** |
| Mobile core (queue, deep links, versions) | `npx vitest run` in `apps/mobile` | **11 passed** (last recorded; not re-run in this audit) |
| Typechecks | `tsc --noEmit` in web, admin, mobile | **0 errors** each (last recorded; re-run before UI work) |
| Lint | `ruff check app tests` (api), `ruff check tools`, `eslint src` (web, admin, mobile) | **clean** (last recorded; 2 pre-existing mobile warnings) |
| First-load budget | `node tools/check_web_budget.mjs` after `vite build` | **58.7 KB JS + 1.4 KB CSS** of 150/20 KB (last recorded) |
| Typed client freshness | `node tools/gen_api_client.mjs --schema openapi.json` | regenerated after the B13/B14 models; the generated file is committed |
| Load-test tool | offline: percentile/report maths, over-budget exit 1, unreachable API exit 2 | **works**; no live measurement yet (F6) |

Fixed while verifying (they were real defects, not test noise): the typed client
was stale after the new response models (regenerated, now including Talent,
Materials, Ask and CBT); a generated `answers[current.id]` access lost narrowing
under `noUncheckedIndexedAccess` on both web and mobile; the seed's span-gold
offsets did not point at the words they claimed (a broken assessment, caught by
the new curriculum test); `CandidateListOut` silently dropped the candidate's
name; a passing practical could not move verification from unverified because the
state machine requires `in_progress` first; the scheduler counted an existing
day's job as new on every tick; the platform migration's timestamps were nullable
against the models; and a handful of screens lost null-narrowing against the
stricter generated types.

## Decisions taken (were open questions)

- **Money rounding rule: approved as documented.** `fee = round_half_up(10% of
  total)`, `department = round_half_up(20% of fee)`, `platform = fee − department`,
  `students = total − fee`; per-student allocation is largest remainder with ties
  by ascending user id. Leftover minor units land with the platform, never with
  the student pool or the department. Recorded in ADR-0011.
- **Mobile ships in lockstep with web** for the core journey screens (D2).
- **G1 — currency:** billing and payout default to **NGN**; allowed currencies are
  NGN, USD, GBP, EUR, GHS, KES and ZAR. Admins change it in the Platform screen.
- **G2 — payouts:** a second approver is required at or above **NGN 50,000.00**
  (5,000,000 minor units); an admin can require one for every payout. Payees need a
  verified email by default; deleted or under-minimum-age accounts are blocked.
- **G3 — age and consent:** paid work starts at **16**; under **18** needs guardian
  consent. Contributor terms are version **2026-10-01**, owner Nelavista, licence
  Nelavista Contributor Licence 1.0.
- **G4 — curriculum:** Nelavista owns and authors the AI Data Annotation
  curriculum in house (`in_house`). The five task types are the five validators the
  engine already has.
- **G5 — ownership:** CODEOWNERS is `@hiipraise`. Launch date is still a business
  input, not a build decision.
- **H2 — Python interpreter:** keep `apps/api/.venv` as the documented local
  interpreter; it stays gitignored and `uv sync` remains the source of truth.
- **TOTP** is the staff second factor (C8/F1); **Resend** is the email provider.

## A. Contracts and tooling

- [x] **A1** Typed client generation adopted. `packages/api-client/src/generated/schema.d.ts`
  is committed, `tools/gen_api_client.mjs` runs on Windows, `ci-contracts.yml`
  regenerates and diffs every PR. Generated types are re-exported from
  `@nelavista/api-client`.
- [x] **A2** Shared V2 types live in `packages/contracts`; the generated schema owns
  the rest.
- [x] **A3** The routes the student journey reads have real `response_model`s,
  including materials, CBT, Ask, talent and the platform policy (B13/B14/G1–G5).
  The generated client now types every screen in this tracker; admin-only write
  routes keep their own models in `apps/admin`.

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
  an in-repo subset with a link allow-list. Answers are written to a versioned
  per-student draft in `localStorage` as they are typed and cleared only when the
  API accepts them (`lib/draft.ts`, `useDraft`), so a reload, a closed tab or a
  failed send never loses work — the web counterpart of the mobile queue.
- [x] **B7** Verification hub, sitting, review and transcript, with resume, form
  generation, expiry and zero-for-unanswered. A lowered badge is a prompt, not a
  silent label change: `/verification` returns the latest event's reason and time,
  the hub and the mobile Proof screen show what happened and link straight at the
  re-sitting, and the quality review sends a verification notification carrying
  the skill and assessment so Settings can link to it too. Answers typed during a
  sitting are drafted by attempt id, so reloading a timed sitting does not lose
  them.
- [x] **B8** Opportunities list/detail with "why you qualify or what's missing".
- [x] **B9** Work: assignments, idempotent submission, rework, messages.
- [x] **B10** Earnings screen with per-line explanations.
- [x] **B11** Settings: languages, availability, notifications, data export,
  in-app account deletion.
- [x] **B12** Performance budgets: route-level splitting, skeletons, and
  `tools/check_web_budget.mjs` enforcing 150 KB JS / 20 KB CSS in CI
  (last measurement **58.6 KB JS + 1.4 KB CSS** after B13/B14 landed). Store
  assets are D4.
- [x] **B13** **Talent profile and shares (Phase 7 UI).** Typed contracts
  (`TalentProfileOut`, `Share*Out`) and screens on **web and mobile**: the
  evidence-only profile, scoped/expiring share creation with the token shown once,
  and revoke. The public `/share/:token` page renders the same shape; the mobile
  app opens both `/talent` and a shared link. Tests cover the API; the deep-link
  parser covers the new route.
- [x] **B14** **Academia connected screens (Phase 8 UI).** Typed contracts
  (`Material*Out`, `Ask*Out`, `Cbt*Out`) and screens on **web and mobile**:
  materials list/search/reader, Ask Nelavista (course-aware, citations, honest
  decline) and CBT practice/results. Web routes are `/academia/materials[/:id]`,
  `/academia/ask` and `/academia/cbt`; the dashboard links to all three. Mobile
  mirrors them through deep links and Home buttons.

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
- [x] **D2** Journey screens in lockstep with B1–B14 (auth, home, learning,
  proof, opportunities, work, earnings, notifications, settings, materials, Ask,
  CBT and the talent profile). The deep-link parser has a test for each new route.
- [x] **D3** Minimum-version and force-update: server `426` + blocking screen,
  store link, comparison helpers and `versions.json` policy.
- [~] **D4** Store readiness (`docs/store/mobile-store-readiness.md`): generated
  icon/adaptive/splash **and a 1024×500 feature graphic**
  (`tools/gen-mobile-assets.mjs`, wired into `app.config.js`), listing copy,
  data-safety table, review notes, test-account plan, in-app deletion, the
  16+/guardian-consent policy, a screenshot/feature-graphic capture checklist and a
  pre-submission checklist.
  **Owed (external):** real-brand assets and the store screenshots captured from a
  signed release build on a device (mock-ups are rejected). That is the only part
  of D4 this repository cannot produce.
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
- [x] **F7** Content: the AI Data Annotation curriculum in
  `apps/api/app/seed/curriculum.py` — one skill, five lessons, a published learning
  path, five task templates with practice samples and expected answers, an
  assessment with five gold tasks, and a practical task with a 100-point rubric.
  The local seed also creates an AID301 course with topics, searchable material
  chunks and eight CBT questions so the Academia/Ask screens have real content.
  `tests/test_curriculum_seed.py` proves every gold task validates and that a
  re-run changes nothing.
- [x] **F8** `POST /auth/email/verify/resend` with a per-account limit and a
  "send the link again" action on the home banner.
- [x] **F9** The verification email now links to the web screen, and
  `/auth/verify` exists to consume it (signed out is fine).

## G. Open questions for you

- [x] **G1** Currency: **NGN** for billing and payouts by default, editable by an
  admin; allowed set NGN/USD/GBP/EUR/GHS/KES/ZAR. Seeded in local and enforced by
  `platform_settings`.
- [x] **G2** Payouts: second approver at **≥ NGN 50,000.00**, optional
  always-require, verified email required by default, deleted/under-age recipients
  blocked. Enforced in `services/money/payouts.py`, not just the admin form.
- [x] **G3** Age and consent: minimum **16**, guardian consent below **18**,
  contributor terms **2026-10-01** (Nelavista Contributor Licence 1.0), recorded
  per student and checked before work/payout.
- [x] **G4** Curriculum: owned and authored in house by Nelavista; five task types,
  all backed by the existing validators. Delivered as F7.
- [x] **G5** Ownership: CODEOWNERS is `@hiipraise`. The target launch date is a
  business input and remains outside the build; the release pipeline is D5.

All five are dynamic admin controls, not constants: `/v1/platform/settings`
(super-admin only) validates, audits and applies them, and `/v1/platform/config`
publishes the parts a signed-out visitor needs. Admin UI: **Platform** in
`apps/admin`. Tests: `tests/test_platform_policy.py`.

## H. Local hygiene

- [x] **H1** `apps/api/.venv` is gitignored.
- [x] **H2** `apps/api/.venv` is **kept** as the documented local interpreter and
  stays gitignored; `uv sync`/`uv run` remain the source of truth and CI uses its
  own environment. Documented in `docs/runbooks/local-setup.md`.
- [x] **H3** `packages/api-client/src/generated/schema.d.ts` is committed and the
  freshness gate passes locally.
