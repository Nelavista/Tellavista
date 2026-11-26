# V2 UI/UX audit — current state

| Field | Value |
|---|---|
| Status | **Re-audited 2026-11-26.** The original V2 UI build is implemented and the post-build admin, comms and public-surface gaps are closed (first-login 2FA coverage, bulk actions, aggregate ops overview, application lifecycle, announcements and newsletter, live impact metrics with an admin publish control, and PostHog analytics plus error tracking). The last four student-surface gaps are closed too: matches, eligibility, adaptive CBT practice and browser push all have web routes and tests. The 2026-11-26 pass re-ran web/admin typechecks and suites, the API suite and the web build, and corrected stale status in the companion docs. Launch remains blocked by business decisions, the manual checks in §9 and the single open V1 item in §6. |
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
  FAQ, Impact, legal pages, shared profile, 404 and offline routes are present.
  Public routes have page metadata, sitemap coverage and private-route robots
  rules. `/impact` publishes live aggregates from the product database; founder
  biography and portrait are no longer on the public site.
- **Admin surface:** overview, waitlist, campus, audit, imports, users, talent
  directory, opportunities, projects, review, money, content, public site,
  announcements, platform, security and 404 are present behind staff
  authentication and 2FA.
- **Mobile lockstep (found 2026-11-26):** the mobile app has not kept up with the
  web additions since 2026-11-01. It has no matches list, eligibility view,
  adaptive CBT practice, CBT history, course/topic detail, applications list,
  cohort invitations, password change, consent history, re-consent gate or
  date-of-birth field. ADR-0012 requires the core journey in lockstep; see §4.
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
  cutover is pending; the PostHog project keys must be set per environment and
  one event must be confirmed in the dashboard. The V2 API now
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
| Admin | Overview, waitlist, campus, audit, imports, users, talent directory, opportunities, projects, review, money, content, public site (impact preview and publish control), announcements (with newsletter subscribers), platform, security and 404 |
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
- `/impact` reads `GET /platform/impact` and renders counts the platform actually
  recorded: student accounts, published skills, universities, mapped courses,
  verified skills, passed assessments, passed practical tasks, approved work and
  open opportunities. It also shows money marked paid, grouped by currency. A
  zero stays visible; the page never substitutes copy for a missing number.
- The founder biography and portrait were removed from the public surface. V1's
  hardcoded "2,500+ students" band was replaced with the live account count.
- Pricing remains the approved commercial position: free for students at launch,
  managed work quoted per brief and university pilots scoped before a price. No
  amount was added or changed.

### Current gaps

- Approved pricing amounts are not supplied.
- Testimonials, partner logos and social profile URLs are not supplied. Share
  intents are used instead of fabricated profile links.
- Real team or campus photography is not supplied.
- The impact figures are only as meaningful as the live database. Before launch,
  ops should open **Public site** in admin, review the counts and switch
  publishing off if any figure is not ready to defend.

**Current verdict:** the public route surface is implemented and honest. The
proof metrics are live rather than claimed, and instrumentation is wired; only
business content and the manual launch checks remain.

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
- **Mobile is behind web.** A 2026-11-26 search of `apps/mobile/src` found no
  caller for `/opportunities/matches`, `/platform/me/eligibility`,
  `/academia/cbt/practice-next`, `/academia/cbt/history`,
  `/academia/courses/{id}`, `/academia/topics/{id}`, the applications list,
  cohort invitations, `/auth/password/change`, `/me/consents` or
  `/auth/consent`, and no date-of-birth field. The re-consent gap matters most: a
  mobile-only student is never asked to accept a new policy version. Signup,
  password reset, onboarding (university/faculty/department/courses) and Choose
  Path are handed to the web on purpose (`screens/Auth.tsx` links out), but
  ADR-0012 lists onboarding and path as lockstep screens and requires a written
  exception, which does not exist yet. Either port these or record in ADR-0012
  which of them mobile intentionally leaves to the web.

## 5. Admin surface

### Implemented

- Staff authentication with forced 2FA enrollment.
- Live overview queues, waitlist, campus publication/readback and audit trail.
- Imports, users, opportunities, projects, review, money, content, platform and
  security screens.
- A **Talent directory** screen over `GET /v1/talent/directory` with language,
  language level, academic level, visibility-status and background filters. The
  screen is read-only and permission-gated; employer self-service remains out of
  launch scope.
- Application status actions and payout-item failure actions.
- Shared page header, panels, skeletons, error states and empty states.
- Admin unknown routes render a real 404.
- Bulk actions on the work review queue, money (approve/cancel; pay stays
  single-record on purpose), content lessons, paths and task templates, and
  practical submissions, each answering a per-id applied/unchanged/failed
  report.
- One aggregate overview read with queue counts, their timestamps, live projects
  and recent audit rows.
- An enforced application lifecycle with allowed next states, a decision stamp
  and a refusal for skipped steps.
- A **Public site** screen that previews the live impact figures (including a
  hidden block), links to the public page and switches
  `impact_metrics_enabled` through the audited platform-settings write. Only a
  super admin can publish or hide the figures.
- Announcement compose/publish/archive and the newsletter subscriber list, with
  audience filtering, idempotent sends and an audit row per write.

### Current gaps

- One manual browser pass of the first-login 2FA flow: the API and admin tests
  cover the sequence, but no human has walked it in a clean browser yet.
- There is no separate newsletter issue builder or send schedule: publishing an
  announcement with the email channel is what mails the list.
- The Public site screen reports whether this admin build carries a PostHog key;
  it cannot verify that events arrived. Confirm one page view and one test error
  in the PostHog dashboard after the environment keys are set.

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
| Public impact page | **Ported with live data:** `/impact` renders counts from `GET /platform/impact`; V1's hardcoded reach figures were not copied, and the landing band now derives its account count from the database. Ops can hide the figures from the admin Public site screen. |
| FUTA taxonomy provenance | **Ported:** verified schools, departments and Surveying & GeoInformatics courses carry `semester`, `course_type`, `description` and `source`, preserved through V1 export/import. Unlisted department course lists stay absent. |
| Career-track progress | **Missing:** a track is an ordered suggestion; no per-student progress is stored. This needs a product decision, not a data-model port. |

Only career-track progress is open. The implementation record is
`docs/build/REMAINING_WORK.md` §H and §I, and the mapping is
`docs/v2-ui/PARITY.md` §1.2.

### 6.1 Unused or partially wired edges

These are current V2 edges that exist in code but have no web or admin caller.
They are recorded so a future change does not treat an endpoint as delivered UI,
or a deferred read as an outage. This is the section `REMAINING_WORK.md` §J
refers to.

| Edge | Current state | Decision |
|---|---|---|
| `POST /auth/google` | No Google sign-in button in web, admin or mobile. The endpoint exists behind `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`. | Deferred until the consent and UI flow are designed; normal auth is complete. |
| `POST /work/submissions/sync` | No web offline submission queue. Mobile uses its SQLite queue and the same idempotent write path. | Deferred; the API exists for a future web client. |
| `GET /talent/me/transcript` | Duplicate of the transcript read used by `/verification/transcript`. | Leave unused; do not build a second transcript screen. |
| `GET /talent/students/{user_id}` | Admin uses `GET /talent/directory`; no screen reads one student's talent profile by id. | Leave unused until a support-detail drawer needs it. |
| `GET /opportunities/{slug}/gaps` | The opportunity detail embeds the verdict, reasons and blocks in its own response, so no screen calls the standalone gaps read. | Leave unused; keep the embedded contract authoritative. |
| `GET /onboarding/sessions/{session_id}/semesters` | Onboarding reads only the current session. | Leave unused until a semester picker exists. |
| `REDIS_URL` | Read by `app/core/ratelimit.py`. Rate-limit counters are shared in Redis when set, in-process otherwise. | Set `REDIS_URL` on Render so limits survive restarts and span workers. |
| `FLAG_EXTERNAL_OPPORTUNITIES` | Only widens the opportunities router guard; no external-listing feature exists behind it. | Keep off; it is a placeholder, not a hidden feature. |
| Browser push registration | Settings registers, lists and removes browser devices through `push-sw.js`; delivery is signed with VAPID and needs both keys configured. | Delivered; set the VAPID pair per environment before claiming browser push. |
| Native push | `PUSH_ENDPOINT` is required for Expo/FCM delivery; unset leaves in-app rows only. | Delivered; provider credentials are deployment work, not UI work. |

Do not invent UI for these to make a checklist look complete. Close an edge by
building the product decision behind it, or leave it documented as unused.

## 7. Design, accessibility and performance

- Shared design tokens and primitives are used by both V2 web surfaces.
- Light/dark theme support is implemented.
- Loading, empty, error, partial and feature-off states are represented where
  their APIs require them.
- Public metadata, sitemap, robots, manifest, icons and offline shell are present.
- API responses are not cached by the PWA.
- A manual keyboard, focus, reduced-motion and contrast pass remains required.
- `prefers-reduced-motion` is honoured in the shared styles and MotionConfig.
  `prefers-contrast: more` and `forced-colors: active` rules live in
  `packages/ui/src/styles.css`: stronger text/border values (with `!important`
  because the theme bridge writes inline variables), opaque sticky bars, and
  system-colour borders, links and focus rings.
- `vitest-axe` runs on the root route and public-route tests. jsdom cannot
  compute colour contrast, so those two pixel-level rules are disabled there;
  the media queries plus the manual high-contrast pass cover colour.
  Visual-regression coverage is still absent.
- The public-route test helper's lazy-route wait budget was raised from 1.5 s to
  5 s on 2026-11-26. Under parallel load the old budget turned a slow dynamic
  import into a false page failure (first Features, then Impact in a focused
  rerun); the pages themselves render correctly.
- Analytics and error tracking are wired through PostHog, not Sentry. The web and
  admin apps initialise lazily only when `VITE_POSTHOG_KEY` is present; the API
  reports unhandled errors when `POSTHOG_API_KEY` is present. An unset key is a
  complete no-op, not a partially configured tracker.
- The first-load budget check was run against the current web build on
  2026-11-23: 125.8 KB gzip of a 150 KB budget, with the PostHog SDK absent from
  the build when no key is compiled in.

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

Do not add placeholder links, invented prices, unverified metrics or UI-only
versions of these features. Impact figures are an exception only because they
are computed from current rows and can be withdrawn from the admin Public site
screen.

## 9. Launch readiness

Before launch, the following current blockers must be closed:

1. Approve pricing amounts, support response expectations, social URLs and the
   team/campus photography position. Review the live impact figures in admin and
   decide whether they stay published.
2. Walk the admin 2FA enrollment and recovery-code flow once in a clean browser;
   the automated coverage exists, this is the manual confirmation.
3. Run `scripts/dev-local.ps1` once without duplicate API/worker processes or
   seed-lock interference.
4. Decide whether career-track progress is a product requirement; every other
   V1 capability in §6 is ported.
5. Complete deployment configuration and the V2 domain switch, including
   `VITE_POSTHOG_KEY` and `VITE_POSTHOG_HOST` (web and admin),
   `VITE_PUBLIC_SITE_URL` (admin), `POSTHOG_API_KEY` (API) and
   `VAPID_PUBLIC_KEY`/`VAPID_PRIVATE_KEY` (API, for browser push). Then confirm
   one page view, one test exception and one browser push subscription arrive.
   The launch checklist's migration head is `20261123_1200`; an older head in a
   runbook is stale.
6. Run the current web, admin and API checks, including the first-load budget.
7. Complete the manual accessibility and responsive browser pass.
8. Decide the mobile lockstep scope in §4 (port or record as web-only),
   at minimum the re-consent gate, before the store submission.

## 10. Documentation status

Keep these documents aligned with this current audit:

- `docs/v2-ui/PARITY.md` — capability mapping and V1 gaps.
- `docs/v2-ui/ROUTE-MAP.md` — approved routes and route dependencies.
- `docs/v2-ui/DESIGN-DIRECTION.md` — approved visual system.
- `docs/v2-ui/IMAGE-PROMPTS.md` — asset manifest and photography status.
- `docs/build/REMAINING_WORK.md` — implementation tracker.
- `docs/architecture/06-roadmap.md` — delivery status by milestone.
- `docs/architecture/04-v1-to-v2-migration.md` — V1 delta and migration head.
- `docs/runbooks/v2-launch-checklist.md` — deployment and cutover checks.
- `docs/design/AUDIT-AND-PLAN.md` — historical pre-redesign audit; the redesign
  in it is implemented, so read it as context, not as open work.

Historical V1 audits and completed build plans are not V2 readiness evidence.

## 11. Verification for this update

**2026-11-26 re-audit:** `pnpm typecheck` 8/8 successful; web `vitest run` 82
passed (15 files); admin `vitest run` 4 passed; API `pytest -q -x` 442 passed, 1
skipped; web build succeeded and the first-load budget is 125.8 KB gzip JS of 150
and 10.3 KB gzip CSS of 20. A caller scan of all 166 generated-client paths found
the mobile drift (§4) and the unused edges added to §6.1. Not run: mobile tests,
lint, the Postgres migration job and the manual passes.

The 2026-11-23 change (live impact metrics, admin Public site, founder copy
removal, PostHog instrumentation) was checked with:

- API: `tests/test_platform_policy.py` 15 passed, including public aggregates,
  the no-student-detail contract and the publish/unpublish path;
  `tests/test_migrations.py` 6 passed, 1 skipped, covering the new
  `impact_metrics_enabled` revision.
- Web: typecheck clean; full `vitest run` 82 passed (15 files), including the
  updated `/impact` read and the Features route. One earlier parallel run
  produced a timing failure in the existing Features assertion; it passed in the
  focused file run and in the full suite run alone.
- Admin: typecheck clean; `vitest run` 4 passed.
- Builds: web and admin production builds succeeded. The web first-load budget
  check reports 125.8 KB gzip JS and 10.3 KB gzip CSS, both within budget.
- Not run for this change: the manual 2FA browser pass, the accessibility and
  responsive pass, and a live PostHog delivery check (no project key is set in
  this environment). §7 and §9 keep those listed as owed.
