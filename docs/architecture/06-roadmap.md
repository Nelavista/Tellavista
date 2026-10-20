# 06 — Roadmap

Ordered by the PRD's **build-first / build-later** split (PRD §15). Target: within 1–3 months to launch. Team: 2–3 devs, no Mac.

> **Reconciled 2026-10-16 with the V2 build prompt** (`docs/build/nelavista-02-v2-build-prompt.md`). The build prompt is the work order, so milestones are now **numbered to match its phases: `M<N>` = Phase `<N>`**. Every difference from the previous M0–M7 roadmap is listed in [What changed, and why](#what-changed-and-why). The per-phase plan, gaps and PR breakdown live in `docs/build/phase-N-plan.md`.

## Milestones

### M0 — Foundations and contracts (= Phase 0)
Domain model v1 + migrations for the PRD entities; API conventions (error envelope, pagination, **idempotency keys**, versioning, min-app-version and force-update); auth core for web **and** native including Google sign-in; roles, permissions and the audit log; design tokens + a small shared UI foundation (shared tokens, not shared components); background job system; feature flags; analytics and error tracking wired; local/dev seed; the mobile shell internals (navigation, secure storage, offline store + sync queue, push plumbing, deep links, per-env build profiles); the admin shell (login, role gating, audit trail).
**Exit:** a developer can log in on **web, iOS, Android and admin** against **local and dev**; CI is green; the **money and permission test harnesses exist**. No student features in this milestone.
Plan: `docs/build/phase-0-plan.md`.

### M1 — Identity, V1 bridge and Choose Path (= Phase 1)
Signup/login, email verification, password reset, Google sign-in, and "**Continue with your V1 account**" per ADR-0005/0009; the one-way V1 import tooling (users, taxonomy, materials metadata, CBT banks, skills catalog) with dry-run and reconciliation reports; the onboarding wizard writing real enrolment records, with a waitlist for uncovered universities; the Choose Path screen with switching at any time; profile, settings and the light Campus utility; ops slice (user lookup, support tools, import run history).
**Exit:** a real V1 test account is imported and continues into V2 with no re-registration; a new student onboards on web and on both mobile platforms.

### M2 — Skills engine and the AI Data Annotation path (= Phase 2)
Skills overview, discover, learning paths, lessons with real sequential progress, My Learning, practice challenges and projects; the **schema-driven task engine** (task templates are configuration); a practice sandbox with instant feedback; the AI Data Annotation path structure with sample curriculum; ops content management with draft/publish. Progress stays honest: **completing a lesson never counts as verification**.
**Exit:** a student completes the AI Data Annotation path, practises with feedback and submits a project, on web and mobile, **including with the connection dropped mid-task**.

### M3 — Verification and Skill Transcript (= Phase 3)
Practical assessments on gold-standard tasks (configurable pass thresholds, randomised selection, attempt limits, low-bandwidth-respecting anti-cheating); the verification state machine driven by evidence (`unverified → in progress → verified → at risk → suspended`) with every transition logged against its evidence; the student-facing **Skill Transcript**; hooks so Phase 5 quality results can strengthen or weaken verification; ops slice (assessment management, manual review/override with a mandatory reason).
**Exit:** a student can only become verified by passing the practical assessment; watching lessons alone never changes status; the transcript updates with linked evidence.

### M4 — Opportunities, matching and cohorts, internal first (= Phase 4)
The opportunity model for managed paid work (requirements, required skills/verification, headcount, language, university, availability, location where relevant, quality standard, rates, payout terms); rules-based eligibility with a **"why you qualify or exactly what you're missing"** explanation that always links back to the learning/verification step that closes the gap; cohorts and assignments (invite/accept, participation, replacing dropouts); the **ops slice is primary here** (create and run managed projects, review matched talent, form cohorts). Modelled so company self-service can sit on top later — **but not built**.
**Exit:** ops creates a project with requirements, the system lists eligible students with explanations, ops forms a cohort, and invited students see their personal qualification explanation.

### M5 — Work delivery and quality control (= Phase 5)
Assignment delivery with offline-first submission and idempotent sync; work batches, deadlines, progress; **quality control** (gold tasks mixed into live work at a configurable rate, double annotation with agreement scoring, reviewer sampling queues, approve/reject/request-rework against the project's quality standard); per-task and rolling per-student quality scores feeding verification, matching and the Talent profile; configurable consequence rules (warn, restrict matching, require re-verification, remove and replace) with logged human override; in-app + push notifications; ops slice (review queues, quality dashboards, flagged contributors, delivery progress).
**Exit:** a pilot project of test work runs end to end with quality scores updating verification and eligibility.

### M6 — Money: ledger, earnings and payouts (= Phase 6)
An **append-only** ledger (integer minor units + currency, corrections as new entries, idempotency on every write — ADR-0008); the split engine (fee, department share from the fee, student pool) with a documented deterministic rounding rule; payment states (pending quality, approved, payable, paid, failed, reversed) where work is only payable after approval; per-project tracking of value, student payout, fee, department share and the three statuses; a **payout provider abstraction with a manual provider first**; the student Earnings screen (web + mobile) and department share records; a daily reconciliation report with imbalance alerts; ops slice (payout batches, second approver for large amounts, ledger explorer, exports); property-based tests proving the split is exact and the department share never reduces the student's 90%.
**Exit:** the PRD's $10,000 example produces 9,000 / 800 / 200 exactly; a reversal leaves a full audit trail; reconciliation is clean.

### M7 — Talent profile and external opportunities (= Phase 7)
The evidence-only Talent profile (verified skills, transcript, projects, quality history, work history, availability, academic context) with student-owned privacy controls and an internal ops view; external opportunities (internships, jobs, scholarships, competitions, events) listed and matched with the same explanation contract and **no fee logic by default**; ops slice for managing/moderating listings.
**Exit:** the profile shows only evidence-backed items; an external opportunity is matched and explained without touching the ledger.

### M8 — Academia connected (= Phase 8, may start after M1 in parallel)
Study Materials for the student's own courses (reuse V1 files, metadata, full-text search); **Ask Nelavista** made course- and material-aware (port the AI provider abstraction and RAG with the honest-decline rule); CBT results showing strengths, weaknesses and what to practise next; the existing dashboard answering its five questions and nothing else. **Hard limits:** no assignments, no social feeds, no gamification for its own sake, no new academic feature areas.
**Exit:** each of the five dashboard questions has a real, data-backed answer for a seeded student.

### M9 — Mobile release (= Phase 9, iOS and Android)
Most mobile work happens inside M0–M8; this milestone finishes and ships it: offline/sync hardening on slow networks, push delivery on both platforms, deep/universal links, minimum-version and force-update flow, crash and performance monitoring, app size and startup on low-end Android; store readiness (icons, screenshots, listings, privacy/data-safety declarations, in-app account deletion, review notes and test accounts, and a **re-check of current Apple and Google policies rather than memory**); release pipeline (signed builds from tags, staged rollout, TestFlight + Play internal/closed tracks, rollback path).
**Exit:** both apps installable through beta channels, smoke suite green, budgets met on a mid-range Android phone and an older iPhone.

### M10 — Hardening and launch (= Phase 10)
Load and soak tests against the scale target; a security review (object-level authorization, uploads, rate limits, admin hardening); a backup/restore drill; a migration rehearsal on production-like **anonymised** data; closed beta, then a pilot with one university cohort and one real managed project (test-mode or tiny real money, with approval); the launch plan (flag gating, communication to V1 users, support playbook, alert thresholds, on-call); and the domain cutover per `03-versioning-and-domains.md` — `v1-final` tag, V1 to `v1.nelavista.com`, V2 to `nelavista.com`, version switcher live, OAuth/email/Search Console/deep-link updates, low DNS TTL and a rehearsed rollback.
**Exit:** launch checklist complete, rollback rehearsed, go/no-go approved.

## What changed, and why

| Build prompt | Milestone | Old roadmap | Difference |
|---|---|---|---|
| Phase 0 | **M0** | M0 — Foundation (scaffolding only) | Grows substantially: the domain model, auth core, roles/audit, jobs, analytics, tokens wiring and the mobile/admin shells are part of it, not "already done". |
| Phase 1 | **M1** | M1 — Identity & Academia core | Academia **materials + RAG moved to M8**; **Choose Path, onboarding and the Campus utility added**; V1 importer kept. |
| Phase 2 | **M2** | M2 — Skills: Learn → Build **→ Verify** | **Verification moved into its own milestone (M3)** — it needs a state machine, transcript and ops slice. |
| Phase 3 | **M3** | (tail of old M2) | Promoted to a milestone. |
| Phase 4 | **M4** | M3 — Match → Work → Quality | Split: matching/cohorts (M4) and work/quality (M5), with the Phase 4 ops slice marked primary. |
| Phase 5 | **M5** | tail of old M3 + **old M5 (Internal ops tools)** | Old **M5 is retired**: ops is a slice inside **every** phase, not a milestone of its own. "Internal ops tools" now appears as an ops slice in M1–M6. |
| Phase 6 | **M6** | M4 — Earn (ledger) | Adds the payout-provider abstraction (manual first), per-project value/status tracking, department-share records, reconciliation report + alerts, a second approver and the property-based tests. |
| Phase 7 | **M7** | **absent** | External (no-fee) opportunities and the evidence-only Talent profile were missing. |
| Phase 8 | **M8** | M6 — Academia focused fixes | Same content, but explicitly able to run in parallel after M1. |
| Phase 9 | **M9** | M7 — Mobile (both platforms) | Materially re-scoped: the old roadmap implied mobile built at the end; the build prompt requires a **mobile slice in every phase** (lockstep), so M9 is release hardening and stores only. |
| Phase 10 | **M10** | **absent** | Load/soak, security review, backup drill, beta, pilot, flag gating and the domain cutover had a runbook but no milestone. |

## Build later (explicitly deferred)
More skill paths (M2's task engine should make these configuration) · automated matching at scale · **company self-service** (requirements/assignments/quality/payouts are modelled for it, PRD §9) · escrow, taxes, currency and payout rails (PRD §12).

## Cross-cutting (built with, not after)
Offline + idempotency (ADR-0007) · observability (Sentry + PostHog per env) · feature flags · accessibility and low-data budgets · the money harness and property-based tests (ADR-0008) · the object-permission harness (ADR-0009).

## Milestone → ADR/plan references
M0 = `docs/build/phase-0-plan.md`, ADR-0001/0002/0005/0008/0009/0010 · M1 = ADR-0005/0009 · M2 = `05-domain-map.md`, ADR-0007 · M3 = `05`, ADR-0009 · M4/M5 = `05`, PRD §6–8, ADR-0006/0007 · M6 = ADR-0008 · M7 = `05`, PRD §10–11 · M8 = ADR-0001/0007 · M9 = ADR-0001/0007/0010 · M10 = `03-versioning-and-domains.md`, `04-v1-to-v2-migration.md`.

## Delivery status (2026-10-20)

Phases 0–6 and the API half of 7–8 are implemented; 9 and 10 are release and
hardening work. The live, item-by-item list is `docs/build/REMAINING_WORK.md`; the
per-phase account of what is delivered and what is owed is
`docs/build/phase-1-10-plan.md`.

| Milestone | State |
|---|---|
| M0 | Delivered (auth core, conventions, jobs, flags, observability, admin shell with 2FA) |
| M1 | Delivered (identity, V1 importer, onboarding, Choose Path, settings, campus) |
| M2 | Delivered; offline answer saving on web still owed; curriculum content blocked on G4 |
| M3 | Delivered; a re-verification call-to-action after suspension is owed |
| M4 | Delivered (opportunities, explanations, cohorts, replacements, candidate lists) |
| M5 | Delivered (delivery, quality, consequences, override, notifications) |
| M6 | Delivered (ledger, split, payouts, reconciliation, earnings); first scheduled reconciliation run unobserved |
| M7 | API delivered; **student Talent/share UI owed** |
| M8 | Dashboard + campus delivered; **materials reader, Ask and CBT results screens owed** |
| M9 | Build profiles, force-update, push, store assets and release workflow delivered; screenshots and a device smoke run owed |
| M10 | Rate limits, Postgres migrations in CI and the load-test tool delivered; the DEV measurement, security review, beta, pilot and cutover remain |

Known stale milestone references from the M0 renumbering are fixed: the API,
admin and mobile READMEs and the `academia` model now describe the delivered state
rather than the old M1–M7 numbering.
