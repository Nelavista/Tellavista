# Phases 1–10 — plans and delivered state

Phase 0 has its own document (`phase-0-plan.md`: gap analysis, PR breakdown,
harnesses). This document is the equivalent for **Phases 1–10**, written after the
build rather than before it, because the phases were implemented in sequence and
the useful artifact now is an honest account of what each phase contains, what is
delivered, and what is still owed.

Two rules carried over from the build prompt:

1. **The build prompt is the work order.** Where it disagrees with
   `docs/architecture/06-roadmap.md`, the prompt wins and the difference is
   listed below and in the roadmap's own table.
2. **A phase is not done because a screen exists.** Each section names its exit
   criterion and links it to the code or test that proves it — or says plainly
   that it is not proven yet.

Status legend: **Delivered** · **Delivered, partial** · **Owed** · **Blocked on you**

---

## Mapping: build prompt ↔ milestone ↔ plan ↔ evidence

| Phase | Milestone | Student surfaces | API | Admin | Evidence |
|---|---|---|---|---|---|
| 0 Foundations | M0 | signed-in placeholder | conventions, auth core, jobs, flags | login, audit, 2FA | `phase-0-plan.md`, `tests/test_api_conventions.py`, `tests/test_two_factor_and_delivery.py` |
| 1 Identity + V1 bridge + Choose Path | M1 | sign-in/up, verify, reset, onboarding, Choose Path, settings, campus | `/auth/*`, `/onboarding/*`, `/me/*` | users, imports, waitlist, campus | `tests/test_identity_models.py`, `tests/test_ops_routes.py` |
| 2 Skills engine | M2 | skills, path, lesson, practice, my learning | `/skills/*` | content management | `tests/test_skills_learning.py` |
| 3 Verification + transcript | M3 | verification hub, sitting, review, practical task, transcript | `/verification/*` | review queue, override | `tests/test_verification_flow.py` |
| 4 Opportunities + matching + cohorts | M4 | opportunities, detail, application | `/opportunities/*`, `/work/cohorts/*` | projects, cohorts, candidates | `tests/test_student_surfaces.py`, `tests/test_admin_read_surfaces.py` |
| 5 Work delivery + quality | M5 | assignments, submission, rework, messages | `/work/*` | review queue, quality, override | `tests/test_work_delivery.py`, `tests/test_quality_service.py`, mobile `mobile-core.test.ts` |
| 6 Money | M6 | earnings | `/money/*` | funding, payouts, ledger, exports | `tests/test_money_split.py`, `tests/test_money_ledger.py`, `tests/test_money_payouts.py`, ADR-0008/0011 |
| 7 Talent + external opportunities | M7 | **owed** (no screen) | `/talent/*`, opportunity `type` | admin opportunity list | `tests/test_talent_service.py` — see §Phase 7 |
| 8 Academia connected | M8 | dashboard, campus; **materials/Ask/CBT owed** | `/academia/*` | — | `tests/test_academia_services.py` |
| 9 Mobile release | M9 | all journey screens | — | — | `docs/store/mobile-store-readiness.md`, `mobile-release.yml` |
| 10 Hardening + launch | M10 | — | rate limits, load test | security headers, audit | `docs/runbooks/load-test.md`, `tools/load_read_paths.py` |

Flagged differences from the pre-build roadmap (unchanged, restated so this
document stands alone):

- **Phase 1** adds Choose Path, onboarding and the Campus utility; academia
  materials + RAG moved to Phase 8.
- **Phase 2/3** split: verification is a phase of its own, not the tail of skills.
- **Phase 4/5** split: matching/cohorts and work/quality are separate, and the
  Phase 4 ops slice is primary.
- **Old M5 (internal ops tools) is retired**; ops is a slice inside every phase.
- **Phase 6** adds the payout-provider abstraction, reconciliation and
  second-approver rule.
- **Phase 7** was absent from the old roadmap (external opportunities + Talent).
- **Phase 9** is release hardening only, because mobile ships in lockstep
  (ADR-0012).
- **Phase 10** was absent from the old roadmap.

---

## Phase 1 — Identity, V1 bridge and Choose Path

**Delivered.** Argon2id sign-in, access JWT + rotating refresh with reuse
detection, cookie path for web and bearer for native, email verification with
resend, password reset, Google ID-token sign-in, consent records, account
deletion, TOTP 2FA for staff (F1), rate limits on auth. The V1 importer
(`services/imports/v1.py`) does dry-run → apply → reconciliation against a V1
export with per-table counts and a report stored on `import_runs`. Onboarding
writes real `enrolments` with a waitlist for uncovered universities. Choose Path
switches without touching learning, proof or earnings.

Exit criterion — *a real V1 test account continues with no re-registration*:
covered by `test_ops_routes.py` (dry-run/apply/report) and
`test_auth_service.py` (legacy hash verify → rehash on first login).

**Owed:** nothing functional. The verify-email screen and reset screens exist
(`routes/VerifyEmail.tsx`, `routes/ResetPassword.tsx`); the email template should
point at `https://…/auth/verify?token=…` rather than a relative path — see
`REMAINING_WORK.md` F9.

---

## Phase 2 — Skills engine and the AI Data Annotation path

**Delivered.** Skills overview/detail, ordered paths with real progress, lesson
reader (in-repo markdown subset, link allow-list), schema-driven practice tasks
(the form is generated from `task_templates.input_schema`), My Learning, and the
gold-task migration that Phase 5 consumes. Content management in admin
(paths → lessons → steps → templates, draft/publish).

Exit criterion — *a student completes a path, practises with feedback, submits a
project, including with the connection dropped*: web is covered by
`skills-journey.test.tsx` and `journey-screens.test.tsx` (practice, assignment and
sitting answers are drafted to `localStorage` and survive a reload or a failed
send — `lib/draft.test.ts`); the offline half is covered on mobile by the queue
tests in `mobile-core.test.ts` and `Work.tsx`.

**Delivered since:** the AI Data Annotation curriculum itself (F7/G4) —
`apps/api/app/seed/curriculum.py` now ships the lessons, practice samples, five
gold tasks and assessment items, with a test that every gold answer validates.

---

## Phase 3 — Verification and Skill Transcript

**Delivered.** Assessments with randomised gold-standard tasks, attempt limits,
resume-in-progress, expiry, unanswered tasks scoring zero, review-only expected
answers, the evidence-driven state machine
(`unverified → in progress → verified → at risk → suspended`) with every
transition logged against its evidence, practical tasks (brief + rubric form),
the transcript grouping learned/proved/delivered with an evidence id per line,
and the ops review/override with a mandatory reason.

Exit criterion — *verification only by assessment*: `test_verification_flow.py`
and `verification-journey.test.tsx`.

**Re-verification prompt:** `/verification` now returns the latest event's reason
and time per skill; the hub and the mobile Proof screen lead with what happened and
a link to the re-sitting, and the quality review sends a verification notification
that carries the skill and assessment slugs
(`test_quality_service.py::test_a_suspended_badge_prompts_the_student_with_the_way_back`).

---

## Phase 4 — Opportunities, matching and cohorts

**Delivered.** Opportunity model with requirements, eligibility explained as
"why you qualify or exactly what's missing" and a link back to the step that
closes the gap; applications; ops project/cohort creation, invites, removals,
replacements, candidate lists; per-cohort quality standards.

Exit criterion — *ops creates a project, the system explains eligibility, ops
forms a cohort, students see their explanation*: `test_student_surfaces.py` and
`test_admin_read_surfaces.py`.

**Owed:** external (no-fee) opportunities have API support and appear in the same
list, but nothing in the UI distinguishes "managed paid work" from "external
opportunity" beyond the type label — see Phase 7.

---

## Phase 5 — Work delivery and quality control

**Delivered.** Assignments with deadlines and progress, idempotent submissions
(`client_key`), rework requests, messages, gold tasks mixed into live work,
double annotation with agreement scoring, reviewer sampling, quality records and
per-student rolling scores feeding verification/matching, consequence rules with
logged human override.

Exit criterion — *a pilot project runs end to end with quality updating
verification and eligibility*: `tests/test_work_delivery.py` and
`tests/test_quality_service.py`, plus the offline queue tests on mobile.

**Owed:** nothing functional; a real pilot is an operational step (Phase 10).

---

## Phase 6 — Money: ledger, earnings and payouts

**Delivered.** Append-only ledger in integer minor units, corrections as new
entries, idempotency on every write, the split engine with the approved rounding
rule (ADR-0011), payout states with quality-gated payability, a manual payout
provider behind an interface, payout batches with approval + second approver
above threshold, per-project value/payout/fee/department tracking, department
share records, daily reconciliation with imbalance alerts, the student Earnings
screen with per-line explanations, and CSV exports.

Exit criterion — *the PRD's $10,000 example gives 9,000 / 800 / 200 exactly*:
`tests/test_money_split.py` asserts the example and the largest-remainder property;
`tests/test_money_ledger.py` proves the postings net to zero and corrections are
new entries.

**Owed:** F3's scheduler exists (`worker/scheduler.py`) and the worker enqueues it;
nothing observes the first production run yet. That is a launch-checklist item.

---

## Phase 7 — Talent profile and external opportunities

**Delivered (API).** Evidence-only Talent profile (`/talent/me`) that refuses
unverified claims by construction, transcript reuse, student-owned shares with
expiry/revocation and a public share token, ops view of a student profile,
external opportunity type with the same explanation contract and no fee logic.

**Owed (student UI).** There is no web or mobile screen for the Talent profile or
for creating/revoking a share; the API and typed shapes exist and are tested.
Tracked as **B13** in `REMAINING_WORK.md`.

Exit criterion — *the profile shows only evidence-backed items; an external
opportunity is matched and explained without touching the ledger*: the API half
is proven; the student-visible half is not.

---

## Phase 8 — Academia connected

**Delivered.** Dashboard answering the five questions with one next action and
its reason, flag-gated "not switched on here" state, Campus utility, materials
list/search/index (reusing V1 metadata), course-aware Ask Nelavista with the
honest-decline rule and session history, CBT quiz/answer/results/practice-next.

**Owed (student UI).** Web and mobile show the dashboard and campus only. There
is no materials reader, Ask screen or CBT results screen; the endpoints exist and
return plain dicts (not yet `response_model`s — A3 notes this). Tracked as **B14**.

Exit criterion — *each of the five dashboard questions has a data-backed answer*:
`tests/test_academia_services.py` and `AcademiaDashboard.tsx`.

---

## Phase 9 — Mobile release

**Delivered.** One Expo codebase, per-environment profiles (`eas.json`), secure
token storage, SQLite offline queue with idempotent sync and backoff, deep and
universal links, push registration and delivery (`PUSH_ENDPOINT`, F4), 426
force-update screen plus server-side minimum version, placeholder icons/splash,
store readiness document, and a tag-triggered release workflow with a manual
approval gate and a tag/version equality check.

**Owed / blocked:**
- Store screenshots and the feature graphic must come from a real build (D4).
- Apple Developer enrolment, EAS project ID and store credentials are yours
  (manual steps; the workflow assumes them).
- A Maestro smoke suite on a real build is still the gap between "typechecks" and
  "installs and works".

Exit criterion — *installable through beta channels, smoke green, budgets met on
a mid-range Android and an older iPhone*: not yet proven; needs a build.

---

## Phase 10 — Hardening and launch

**Delivered.** Error envelope + request ids, security headers, object-level
authorization helpers, auth rate limits, money/review rate limits (F5), the
read-path load test with a p95 budget (F6), migration round-trip on SQLite **and
Postgres** in CI (F2), backup/restore and rollback runbooks, domain cutover plan.

**Owed:**
- Run the load test against DEV with representative volumes and record the
  numbers (the tool exists; the measurement is F6's remaining half).
- A security review pass (object-level authorization across every new route,
  uploads, admin hardening) — the harness exists, the review does not.
- Closed beta, one university cohort, one real managed project with approval.
- Go/no-go, flag gating, support playbook, alert thresholds, on-call.
- Domain cutover per `03-versioning-and-domains.md` (`v1-final` tag, V1 to
  `v1.nelavista.com`, version switcher live, DNS TTL, rehearsed rollback).

Exit criterion — *launch checklist complete, rollback rehearsed, go/no-go*: not
started; it is an operational milestone, not a coding one.

---

## What is genuinely left, in one list

| # | Item | Phase | Owner |
|---|---|---|---|
| 1 | Store screenshots from a real build (D4; feature graphic is generated) | 9 | design + you |
| 2 | Maestro smoke on a dev build | 9 | code + device |
| 3 | Run and record the load test on DEV (F6 remainder) | 10 | you + code |
| 4 | Security review; beta; pilot; go/no-go; cutover | 10 | you |

Delivered since this list was written: B13, B14, the AI Data Annotation content
(F7/G4) and the G1–G5 policy controls.

The build status is tracked in `REMAINING_WORK.md`; UI readiness and the missing
public/app/admin screens are tracked in `docs/v2-ui/AUDIT.md`. This document is
the per-phase narrative behind the build tracker.
