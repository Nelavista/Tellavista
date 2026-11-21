# V2 UI/UX audit — current state

| Field | Value |
|---|---|
| Status | **Current as of 2026-11-21.** The original V2 UI build is implemented and the post-build admin and comms gaps are closed (first-login 2FA coverage, bulk actions, aggregate ops overview, application lifecycle, announcements and newsletter). The last four student-surface gaps are closed too: matches, eligibility, adaptive CBT practice and browser push all have web routes and tests. Launch remains blocked by business decisions, one manual browser pass and the single open V1 item in §6. |
| Scope | V2 web, admin, design system and UI-facing API contracts |
| Source of truth | Current code in `apps/`, `packages/` and the V2 API contracts |
| Companion documents | `docs/v2-ui/PARITY.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/DESIGN-DIRECTION.md`, `docs/v2-ui/IMAGE-PROMPTS.md`, `docs/build/REMAINING_WORK.md` |

This document is a current-state audit. It does not preserve a baseline, previous
implementation status or historical decision record. When code or product scope
changes, update the current statements here and the companion documents together.

## Executive summary

V2 currently provides a broad student product, public marketing surface, internal
admin console and FastAPI API. The approved core route set is implemented and the
web and admin apps use the shared design system.

The current launch position is:

- **Core V2 UI:** implemented for the approved route set.
- **Student journey:** auth, onboarding, academia, skills, verification,
  opportunities, work, earnings, talent, campus, notifications and settings are
  routed and wired to current API contracts.
- **Public surface:** landing, Features, How it works, Pricing, About, Contact,
  FAQ, legal pages, shared profile, 404 and offline routes are present. Public
  routes have page metadata, sitemap coverage and private-route robots rules.
- **Admin surface:** overview, waitlist, campus, audit, imports, users,
  opportunities, projects, review, money, content, platform, security and 404 are
  present behind staff authentication and 2FA.
- **Design system:** shared tokens, theme bridge, primitives, CSS and self-hosted
  fonts are consumed by both web and admin. Light and dark themes use Nelavista
  blue and white.
- **API/UI closure:** course and topic detail, CBT history with answer review,
  cohort invitations, admin campus reads, consent history, application status,
  payout-item failure and signed-in password change are implemented.
- **Admin operations:** the overview reads one aggregate endpoint
  (`GET /v1/ops/overview`); review, money and content act on a selection and
  report every refused id; applications move through an enforced lifecycle; and
  announcements plus the newsletter subscriber list have an admin screen, an
  audit row per write and a token-based unsubscribe path.
- **Not launch-ready:** business content is not fully approved; the admin 2FA
  flow is covered by the API and admin tests but still needs one manual browser
  pass, and the local startup path needs a clean run; deployment/domain
  cutover is pending; analytics and error tracking are not wired. The V2 API now
  supports the approved talent-directory language, level, visibility-status and
  background filters at `/v1/talent/directory`; employer self-service UI remains
  intentionally out of launch scope. FUTA's verified taxonomy seed and Course
  provenance fields/importer are now implemented; unverified department course
  lists remain intentionally absent. Ask prompt-boundary hardening is complete;
  practice and assessment grading remain deterministic with no AI prompt path.
  Structured assessments enforce the per-skill scored-practice prerequisite, and
  Talent API responses now carry append-only verification evidence plus scoped
  academic and language context; presentation work remains a separate UI task.

## 1. Current stack

| Area | Current implementation |
|---|---|
| Student web | React 18, Vite 5, TypeScript, React Router 6 and an installable PWA |
| Admin | React 18, Vite 5, TypeScript and an in-repo hash router |
| API | FastAPI modular monolith under `/api/v1` |
| Python | Python 3.11 minimum; `apps/api` is managed by the uv workspace |
| Shared UI | `packages/ui`, `packages/design-tokens` and `packages/contracts` |
| API types | Generated OpenAPI types in `packages/api-client` |
| Tests | Vitest/jsdom for web, admin and mobile; pytest for the API |
| Mobile | Expo app exists but is outside the V2 web launch scope |

## 2. Current route and capability coverage

The exact route contract is maintained in `docs/v2-ui/ROUTE-MAP.md`. The current
surface is:

| Surface | Current coverage |
|---|---|
| Public and auth | Landing, Features, How it works, Pricing, About, Contact, FAQ, privacy, terms, contributor terms, login, signup, email verification, password reset, shared profile, 404 and offline |
| Student app | Home, onboarding, academia, materials, Ask, CBT, skills, learning, lessons, practice, verification, assessment, attempt review, practical task, transcript, opportunities, applications, work, earnings, talent, campus, notifications and split settings routes |
| Admin | Overview, waitlist, campus, audit, imports, users, opportunities, projects, review, money, content, announcements (with newsletter subscribers), platform, security and 404 |
| Platform behaviour | Auth guards, return paths, session refresh, consent re-consent, error boundary, offline shell, route focus handling and theme switching |

## 3. Public surface

### Implemented

- Separate routed marketing and legal pages with current product copy.
- Pricing positions without invented prices.
- Support contact and FAQ routes.
- Scoped, revocable public talent profiles.
- Per-page title, description, canonical, robots and OG/Twitter metadata.
- Sitemap and robots rules for public pages and private-route exclusion.
- Editorial WebP assets, brand assets, 404 and offline states.
- Newsletter opt-in in the public footer and the `/newsletter/unsubscribe` page
  reached from any issue; there is no standalone `/newsletter` marketing route.

### Current gaps

- Approved pricing amounts are not supplied.
- Real proof metrics, testimonials, partner logos and social profile URLs are not
  supplied. Share intents are used instead of fabricated profile links.
- Real founder, team or campus photography is not supplied.
- `/impact` is implemented as a qualitative page. It publishes no reach figures,
  testimonials or partner claims until each is verified against a current source
  and approved for publication.
- Analytics and error tracking are not wired.

**Current verdict:** the public route surface is implemented and honest, but
business content and operational instrumentation must be resolved before launch.

## 4. Student surface

### Implemented

- Four-space onboarding and home model: Academia, Skills, Opportunities and
  Campus.
- Academia dashboard, materials, Ask, CBT, history with answer review, courses,
  topics and campus.
- Skills catalog, detail, paths, lessons, practice and learning history.
- Evidence-based verification with assessment sitting, review, practical task and
  transcript.
- Opportunity qualification blockers, applications, work assignments,
  submissions, quality review and cohort invitations.
- Earnings ledger, talent evidence profile, scoped share links and revocation.
- A standalone matches list (`/opportunities/matches`) that shows the API's rank,
  verdict, reasons, next steps and blocks without recomputing any of them.
- A standalone eligibility view (`/eligibility`) that maps each blocker code to the
  action that clears it, records contributor-terms consent against the published
  version, and explains the age rules.
- Adaptive CBT practice inside `/academia/cbt`: the UI draws weak-topic questions
  from `GET /academia/cbt/practice-next` and answers them through the same
  `POST /academia/cbt/answer` the paper uses.
- A date-of-birth field in Settings → Profile, so the age blocker the eligibility
  view reports can actually be cleared.
- Separate profile, security, notifications and data settings routes.
- Consent history, browser and mobile push-device registration, device removal,
  export and account deletion controls.
- Published notices render above the workspace shell, dismissible per id and
  remembered across reloads; the mobile Home feed shows the same notices.

### Current gaps

- Newsletter membership is per address: there is no signed-in subscribe or leave
  control in Settings, and leaving means using the link in the last email.
- Web offline submission sync is API-only; mobile is the supported offline path.
- Web Push needs `VAPID_PUBLIC_KEY`/`VAPID_PRIVATE_KEY` set in an environment before
  Settings offers the switch; unset is reported as "not configured", not as off.
- Material upload/analysis is replaced by curated materials, Ask, CBT and
  transcript evidence; the replacement copy still needs product approval.
- Career-track progress is not stored: a track is a suggested order, not a
  learning path with its own progress.

## 5. Admin surface

### Implemented

- Staff authentication with forced 2FA enrollment.
- Live overview queues, waitlist, campus publication/readback and audit trail.
- Imports, users, opportunities, projects, review, money, content, platform and
  security screens.
- Application status actions and payout-item failure actions.
- Shared page header, panels, skeletons, error states and empty states.
- Admin unknown routes render a real 404.
- Bulk actions on review, money (approve/cancel; pay stays single-record on
  purpose) and content, each answering a per-id applied/unchanged/failed report.
- One aggregate overview read with queue counts, their timestamps, live projects
  and recent audit rows.
- An enforced application lifecycle with allowed next states, a decision stamp
  and a refusal for skipped steps.
- Announcement compose/publish/archive and the newsletter subscriber list, with
  audience filtering, idempotent sends and an audit row per write.

### Current gaps

- One manual browser pass of the first-login 2FA flow: the API and admin tests
  cover the sequence, but no human has walked it in a clean browser yet.
- There is no separate newsletter issue builder or send schedule: publishing an
  announcement with the email channel is what mails the list.

## 6. V1 capabilities and where they stand

Every V1 capability added after the original parity review is now in V2 except
career-track progress. The current state of each:

| Capability | Current V2 state |
|---|---|
| African Languages Lab catalogue | **Ported:** 9 categories, 94 published skills, lessons, practice tasks, assessments and 10 ordered career tracks; `/skills/african-languages` lists them and `/skills` filters by search, programme, language and level. |
| Language profile | **Ported:** `user_languages` carries dialect and the five self-reported flags; `/skills/languages` edits them and shows verified capabilities as a separate read-only derivation. |
| Structured scored language tasks | **Ported:** four task kinds scored deterministically (WER, chrF, label accuracy, recording requirements, repeat consistency); expected answers stay server-side and are stripped from practice briefs and sittings. |
| Per-skill scored-practice assessment gate | **Ported for structured templates:** a sitting requires one scored practice attempt per published structured practice task. Legacy non-structured templates keep the older gate. |
| Language catalogue filters and ALL hub | **Ported:** the hub and catalogue filters read server-side `q`, `program`, `category`, `language`, `tag` and `level`. |
| Language evidence and talent filters | **Ported:** the transcript "By skill" table and per-skill talent evidence; `/v1/talent/directory` filters language, language level, academic level, visibility status and background, and the admin Talent directory uses it. |
| Public impact page | **Ported qualitatively:** `/impact` and the landing band publish outcomes, with no reach figures until they are verified against a current source. |
| FUTA taxonomy provenance | **Ported:** verified schools, departments and Surveying & GeoInformatics courses carry `semester`, `course_type`, `description` and `source`, preserved through V1 export/import. Unlisted department course lists stay absent. |
| Career-track progress | **Missing:** a track is an ordered suggestion; no per-student progress is stored. This needs a product decision, not a data-model port. |

Only career-track progress is open. The implementation record is
`docs/build/REMAINING_WORK.md` §H and §I, and the mapping is
`docs/v2-ui/PARITY.md` §1.2.

## 7. Design, accessibility and performance

- Shared design tokens and primitives are used by both V2 web surfaces.
- Light/dark theme support is implemented.
- Loading, empty, error, partial and feature-off states are represented where
  their APIs require them.
- Public metadata, sitemap, robots, manifest, icons and offline shell are present.
- API responses are not cached by the PWA.
- A manual keyboard, focus, reduced-motion and contrast pass remains required.
- No automated axe, visual-regression, analytics or error-tracking coverage is
  currently wired.
- The first-load budget check exists and must be run against the current build
  before launch.

## 8. Current decisions and deferrals

The following are intentionally outside the current launch surface or were
deliberately deferred:

- A newsletter issue builder and send scheduling; an emailed announcement is
  the current path to the list.
- Double opt-in confirmation: a submitted address is subscribed immediately, so
  suppression and re-confirmation remain open consent work.
- Employer self-service; launch uses managed work.
- Google SSO until its consent and UI flow are designed.
- Offline submission sync on web until the client queue is implemented.
- Numeric `/impact` claims until every public metric is verified.

Do not add placeholder links, invented prices, unverified metrics or UI-only
versions of these features.

## 9. Launch readiness

Before launch, the following current blockers must be closed:

1. Approve pricing amounts, support response expectations, social URLs, proof
   metrics and the photography position.
2. Walk the admin 2FA enrollment and recovery-code flow once in a clean browser;
   the automated coverage exists, this is the manual confirmation.
3. Run `scripts/dev-local.ps1` once without duplicate API/worker processes or
   seed-lock interference.
4. Decide whether career-track progress is a product requirement; every other
   V1 capability in §6 is ported.
5. Complete deployment configuration and the V2 domain switch.
6. Run the current web, admin and API checks, including the first-load budget.
7. Complete the manual accessibility and responsive browser pass.

## 10. Documentation status

Keep these documents aligned with this current audit:

- `docs/v2-ui/PARITY.md` — capability mapping and V1 gaps.
- `docs/v2-ui/ROUTE-MAP.md` — approved routes and route dependencies.
- `docs/v2-ui/DESIGN-DIRECTION.md` — approved visual system.
- `docs/v2-ui/IMAGE-PROMPTS.md` — asset manifest and photography status.
- `docs/build/REMAINING_WORK.md` — implementation tracker.
- `docs/runbooks/v2-launch-checklist.md` — deployment and cutover checks.

Historical V1 audits and completed build plans are not V2 readiness evidence.

## 11. Verification for this update

This change updates documentation only. No application or API code changed, so
the suites were not rerun for it. The results it records come from the two code
changes it documents:

- `5a4f141` (comms, bulk actions, overview, lifecycle): API `test_comms.py`,
  `test_admin_overview.py`, `test_application_lifecycle.py`, `test_bulk_actions.py`
  and `test_migrations.py` pass; web 74 tests (9 in `comms-surfaces.test.tsx`),
  admin Vitest including the first-login 2FA flow, mobile 14.
- `672d7eb` (matches payload): full API suite 429 passed; `test_student_surfaces.py`,
  `test_matching_service.py` and `test_bulk_actions.py` 32 passed; ruff clean on
  the touched files; web, admin and mobile typechecks clean against the
  regenerated client.

No accessibility, contrast, reduced-motion or first-load budget check was run for
either change; §7 still lists them as owed.
