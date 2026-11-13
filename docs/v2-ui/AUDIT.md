# V2 UI/UX audit — current state

| Field | Value |
|---|---|
| Status | **Current as of 2026-11-04.** The original V2 UI build is implemented; launch remains blocked by business decisions, manual verification and the V1 capability delta listed below. |
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
- **Not launch-ready:** business content is not fully approved; admin 2FA and the
  local startup path need a clean browser verification; deployment/domain
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
| Admin | Overview, waitlist, campus, audit, imports, users, opportunities, projects, review, money, content, platform, security and 404 |
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
- Separate profile, security, notifications and data settings routes.
- Consent history, push-device removal, export and account deletion controls.

### Current gaps

- No standalone matches view; opportunity verdicts remain on the existing list.
- No standalone eligibility view; blockers remain on opportunity detail.
- Adaptive CBT practice is API-only.
- Web offline submission sync is API-only; mobile is the supported offline path.
- Browser push registration is not implemented.
- Material upload/analysis is replaced by curated materials, Ask, CBT and
  transcript evidence; the replacement copy still needs product approval.
- Skills search and filtering are not implemented.

## 5. Admin surface

### Implemented

- Staff authentication with forced 2FA enrollment.
- Live overview queues, waitlist, campus publication/readback and audit trail.
- Imports, users, opportunities, projects, review, money, content, platform and
  security screens.
- Application status actions and payout-item failure actions.
- Shared page header, panels, skeletons, error states and empty states.
- Admin unknown routes render a real 404.

### Current gaps

- The complete first-login 2FA browser flow needs end-to-end verification.
- Review, money and content actions are single-record actions; bulk actions are
  not implemented.
- Overview composes several reads; no aggregate overview endpoint exists.
- Deeper application lifecycle states are not implemented.
- Newsletter and platform-announcement administration do not exist.

## 6. V1 capabilities not currently in V2

V2 must not claim full parity while these current V1 capabilities are absent:

| Capability | Current V2 state |
|---|---|
| African Languages Lab catalogue | **Seeded in V2:** 9 categories, 94 published skills, lessons, practice tasks, assessments and 10 ordered career tracks. The language profile, ALL hub/filter UI and richer task UX remain missing. |
| Language profile | Missing: self-reported language, dialect, proficiency and capability fields are not in V2 |
| Structured scored language tasks | V2 stores the transcription, translation, labeling and recording task specs and has an ALL validator; the richer task UI and V1 scoring algorithms remain missing |
| Per-skill scored-practice assessment gate | Missing: V2 verification does not require the V1 language-task prerequisite sequence |
| Language catalogue filters and ALL hub | Missing: language, level, tag and programme filters and the dedicated hub are not in V2 |
| Language evidence and talent filters | Missing: language-specific transcript evidence and talent search filters are not in V2 |
| Public impact page | Missing: do not copy unverified public metrics into V2 |
| FUTA taxonomy provenance | Missing: V2 does not currently carry the V1 taxonomy source and semester provenance |

These are product and data-model gaps, not cosmetic UI gaps. Port them through V2
models, contracts, seeds and tests, or record an explicit product decision to
drop each capability before launch. The implementation tracker is
`docs/build/REMAINING_WORK.md` §I and the mapping is `docs/v2-ui/PARITY.md` §1.2.

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

The following are intentionally outside the current launch surface:

- Newsletter, until consent, double opt-in, unsubscribe, suppression and admin
  workflows exist.
- Platform announcement banner, until an announcement backend and audit trail
  exist.
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
2. Verify the admin 2FA enrollment and recovery-code flow in a clean browser path.
3. Run `scripts/dev-local.ps1` once without duplicate API/worker processes or
   seed-lock interference.
4. Decide whether each V1 capability in §6 is ported or explicitly dropped.
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
the test suites were not rerun for this update. The next code change must run the
smallest relevant checks and refresh this section only with results from that
current run.
