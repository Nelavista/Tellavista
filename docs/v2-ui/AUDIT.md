# V2 UI/UX audit — Phase 0 baseline

| Field | Value |
|---|---|
| Status | **Post-build 2026-11-01; V1 delta audited 2026-11-04. Gates 1 and 2 approved 2026-10-27. Core UI and API-detail build complete; remaining items are business content, launch verification, and the new V1 features that are not in V2 yet.** |
| Date | 2026-10-27; post-build, palette correction and API closure 2026-11-01; V1 delta 2026-11-04 |
| Scope | Current V2 web, admin, design tokens and UI-facing API contracts; V1 used only as a reference |
| Not in scope | V1 code changes, backend changes, deployment changes, mobile launch |
| Companion documents | `docs/v2-ui/PARITY.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/DESIGN-DIRECTION.md`, `docs/v2-ui/IMAGE-PROMPTS.md`, `docs/design/ui-ux-framework.md` |

> This is the Phase 0 baseline. It records what existed before the redesign, what
> was broken or missing, what V1 actually does, and which documents were stale.
> The parity decisions are in `PARITY.md`; the route contract is in `ROUTE-MAP.md`;
> the visual direction is in `DESIGN-DIRECTION.md`. Read §1.1 first: it is the
> current state, and it overrides the baseline tables below where they disagree.
> Sections 2–14 are intentionally kept as the starting-point record.

## 1.1 Post-build status (2026-11-01)

The redesign has landed in code. This section replaces the baseline where they
disagree; the rest of the document remains useful as the starting-point record.

- **Design system:** Light/dark palettes built on Nelavista blue `#1535A8` and
  white `#FFFFFF`, the shared theme bridge, primitives, shared CSS and three
  self-hosted font families are in `packages/ui`. Web and admin both consume them.
- **Brand assets:** The V1 logo and favicon are copied into both V2 apps. The
  uploaded WebP is the larger boot and route loader, with a still-mark and
  reduced-motion fallback. The MP4 is a 1920x1080 brand video, not a transparent
  loader; it runs full-width before the public footer with a reduced-motion
  still. The header and app rail use the circular mark only.
- **Public surface:** Landing, Features, How it works, About, Contact, FAQ,
  Privacy, Terms, Contributor terms, a real 404 and an offline screen exist as
  separate routes. Legal copy is final product copy with the current terms
  version. Every public page now sets a title, description, canonical, robots and
  OG/Twitter metadata;
  `sitemap.xml` and `robots.txt` cover the public pages and disallow private app
  routes.
- **Auth:** Login, Signup, Verify email and Reset password use the shared auth
  layout and set page metadata. Password fields have a show/hide control, and
  signup links to the legal pages and records the current terms version.
  `ConsentGate` handles a terms or privacy version change after sign-in.
- **Student app:** The grouped app shell, mobile navigation, theme toggle,
  notifications, applications, CBT history, course detail and split settings
  routes exist. Home, Academia, Materials, Ask, CBT, Skills, My learning, Lesson,
  Practice, Verification, Assessment sitting, Attempt review, Practical task,
  Transcript, Opportunities, Applications, Work, Earnings, Talent, Campus,
  Notifications, Settings and Onboarding use the shared primitives and explicit
  states. Onboarding and Home share one four-space model: Academia, Skills,
  Opportunities and Campus. Each opens its own dashboard, and Onboarding asks for
  only the context that space reads. Eligibility blockers are shown on opportunity
  detail before apply.
- **Settings:** Profile, security, notifications and data are separate routes.
  Consent history is read from `/me/consents` and rendered as an append-only
  table. Push devices are read from `/me/push-devices` and can be removed; the
  web app does not claim to register a browser device. The old push checkbox that
  promised delivery without a device is gone.
- **Admin:** The grouped shell, Overview, Waitlist, Campus, Audit, Imports, Users,
  Opportunities, Projects, Review, Money, Content, Platform, Security and a real
  404 exist. All admin screens now use the shared page header, panel, skeleton,
  error and empty primitives. Overview reads live queues; Campus publishes and
  reads the live set, including hidden rows. Application status and payout-item
  failure actions are exposed in Opportunities and Money.
- **Closed API dependencies:** Full course and topic detail, CBT history with
  answer review, the student cohort-invite list, admin campus read, the
  campus-only university choice (`PUT /onboarding/university`) and signed-in
  password change are implemented and wired. In-place password change revokes
  other refresh tokens and renews the current session. Signup records both terms
  and privacy consent at the platform terms version.
- **Still open (business/content):** approved pricing amounts, real social profile
  URLs, real metrics/testimonials, photography, employer positioning and the
  material upload/analysis replacement copy. The editorial images are integrated
  as optimized WebP derivatives; real photography is still pending. Share intents
  stand in for unavailable profile URLs.
- **Still open (verification):** Admin 2FA enrolment is code-complete and the
  recovery-code handoff is fixed, but the full browser path is not verified
  end-to-end. The local seed lock came from duplicate API/worker processes and was
  cleared by stopping them; `dev-local.ps1` still needs one clean run. The V2
  domain switch is a deployment-level step and remains pending.
- **V1 delta (2026-11-04):** V1 `main` added the African Languages Lab (94 skills,
  9 categories, 10 tracks), the language profile, structured scored language tasks
  with an assessment gate, per-skill transcript/talent evidence, language filters
  for talent search, a public `/impact` page and a verified FUTA taxonomy seed.
  None of these are in V2. They are not cosmetic parity gaps: ALL is a content
  product plus schema plus assessment behaviour, and the Impact page carries
  unverified public metrics. See `PARITY.md` §1.2 and `REMAINING_WORK.md` §I.
- **Removed as unused:** `Logo`, `ArrowLink` and `Spinner` exports, the unused
  spinner CSS, and `apps/web/src/components/Layout.tsx`.


---

## 1. Executive summary (current, 2026-11-04)

V2 is a broad, working product with a real public surface, a real student journey,
a real admin tool and a real API. The original Gate 1 UI scope is built.

The short version:

- **The product spine is real.** Auth, onboarding, academia, skills, verification,
  opportunities, work, money, talent, campus and admin all have API routes and web
  screens.
- **The public surface is built.** Landing, Features, How it works, Pricing, About,
  Contact, FAQ, Privacy, Terms, Contributor terms, a real 404 and an offline screen
  exist as separate routes, with per-page metadata, a sitemap and robots rules.
- **The design system is built.** Light/dark palettes on Nelavista blue and white,
  shared tokens, primitives, shared CSS and three self-hosted fonts live in
  `packages/ui`; web and admin both consume them.
- **Admin shares the design system.** Overview, Waitlist, Campus, Audit, Imports,
  Users, Opportunities, Projects, Review, Money, Content, Platform, Security and a
  real 404 use the shared primitives at a denser rhythm.
- **API/UI edges are closed.** Course/topic detail, CBT history with review, cohort
  invitations, admin campus read, application status, payout-item failure, consent
  history and signed-in password change are implemented and wired.
- **The V1 delta is missing.** V1 `main` added the African Languages Lab, language
  profile, structured scored tasks, per-skill evidence, talent filters, `/impact`,
  the FUTA taxonomy and AI prompt hardening after this audit. V2 has none of them.
  This is the one real parity regression; it is tracked in §1.1, `PARITY.md` §1.2
  and `REMAINING_WORK.md` §I.

**Verdict:** the UI build is complete for the Gate 1 route set. V2 is not
launch-ready because of unapproved business content (pricing amounts, proof
metrics, photography, social links), the admin 2FA end-to-end check, the DEV load
measurement, the domain switch and the V1 delta decision. It is not a wireframe or
a stub.

---

## 2. Current stack and route surface

### 2.1 Stack

| Area | Current state |
|---|---|
| Student web | React 18.3 + Vite 5.4 + TypeScript, React Router 6.28, plain CSS + shared CSS variables, PWA via `vite-plugin-pwa` |
| Admin | React 18.3 + Vite 5.4 + TypeScript, in-repo hash router, shared `@nelavista/design-tokens` and `@nelavista/ui` |
| API | FastAPI modular monolith under `/api/v1`, 13 mounted domain routers |
| Tokens | `packages/design-tokens/src/index.ts`; published through the shared theme bridge and consumed by both apps |
| Shared UI | `packages/ui` exports the shared primitives, theme bridge, shared CSS and fonts; `apps/web/src/ui.tsx` is a re-export alias |
| Tests | Vitest + jsdom + React DOM; no Testing Library, axe, Playwright or visual regression yet |
| Mobile | Expo 52 / React Native 0.76.5; post-launch, shares tokens not web components |

### 2.2 Route surface

| Surface | Routes | Notes |
|---|---|---|
| Public and auth | 15 | Landing, Features, How it works, Pricing, About, Contact, FAQ, three legal pages, share, login, signup, verify, reset |
| Signed-in web | 28 | Home, onboarding, academia, skills, verification, opportunities, work, earnings, talent, transcript, campus, notifications, settings |
| Admin | 14 hash sections | Overview, audit, imports, users, waitlist, opportunities, projects, review, money, content, campus, platform, security, 404 |
| Catch-all | `*` | Real public 404 |
| Admin fallback | any unknown hash | Real admin 404 |

The exact route list is `ROUTE-MAP.md`; the built status is §1.1.

### 2.3 What is genuinely strong

- **State honesty.** Screens distinguish loading, empty, error, partial and
  feature-off where those states occur. `useApiResource` maps a 404 `not_found` to
  “not switched on here”.
- **Security and money are not cosmetic.** Verification is evidence-backed, the
  ledger is append-only, payouts need a second approver, and staff need TOTP.
- **Admin is real.** Audit, imports, users, review, money, content, platform,
  security and the live campus set are working tools, not mockups.
- **PWA basics are real.** Manifest, icons, offline shell, robots, sitemap and a
  Google verification file are present. API responses are deliberately not cached.
- **The API is broad.** Identity, academia, skills, verification, opportunities,
  talent, work, money, platform and ops are mounted.

---

## 3. Public surface (current)

### 3.1 What exists

| Item | Current state |
|---|---|
| Landing | Routed landing with the working-record argument, proof chain and separate route links |
| Features / How it works | Built as separate pages with real product capabilities |
| Pricing | Built with commercial positions; no invented amounts |
| About / Contact / FAQ | Built with mission, a real support path and objection answers |
| Legal | Privacy, Terms and Contributor terms are final product copy at the current terms version |
| Shared profile | Public by token, scoped and revocable |
| Metadata | Every public page sets title, description, canonical, robots and OG/Twitter; sitemap and robots cover public pages and disallow private routes |
| Images | Editorial WebP set integrated; real photography is still pending |
| 404 / offline | Real screens, not redirects |
| Theme | Light/dark on brand blue and white |

### 3.2 What remains

| Item | Why it matters |
|---|---|
| `/impact` | V1 added it on 2026-11-01 with fixed 2,500+/500+ figures. Add only when the business verifies them; otherwise keep the honest `/about` working record. |
| Approved pricing amounts | `/pricing` ships commercial positions, not amounts. Replace them when the business approves figures. |
| Real photography | Editorial illustrations are integrated. Real founder/team/campus photos need consent and a licence. |
| Real proof | Student counts, university counts, testimonials and partner logos must be current and verifiable. Do not copy V1's hardcoded “2,500+”. |
| Real social URLs | Share intents stand in for profile links that do not exist. |
| Analytics and error tracking | Not wired. Operational gap, not a UI gap. |

### 3.3 Public-surface verdict

The public surface is built, crawlable and honest. It is not launch-ready because
business content and analytics are missing, not because routes or legal pages are
missing. The one public route V2 does not have is `/impact`, and it stays out
until its metrics are defensible.

---

## 4. Student surface (current)

### 4.1 What exists

The student app has the full Gate 1 journey:

- **Home / onboarding** — one four-space model (Academia, Skills, Opportunities,
  Campus), next-action home, explicit eligibility blockers.
- **Academia** — dashboard, materials list/search/reader, Ask Nelavista, CBT
  practice, CBT history with answer review, course and topic detail, campus.
- **Skills** — catalog, skill detail, path, lesson, practice, my learning.
- **Verification** — hub, assessment sitting, attempt review, practical task,
  transcript.
- **Opportunities** — list with per-student verdict, detail, apply and my
  applications.
- **Work** — assignments, submissions, quality, assignment detail, messages and
  cohort invitations with accept/decline.
- **Money** — earnings ledger.
- **Talent** — evidence profile, scoped share links and revoke.
- **Settings** — profile, security, notifications, data, consent history, push
  devices, export and delete account as separate routes.
- **Notifications** — a dedicated route, not a list buried in Settings.

### 4.2 Remaining gaps

| Gap | Current state | Impact |
|---|---|---|
| No “matches” view | `GET /opportunities/matches` is unused; the list shows verdicts | Matching work is under-exposed; nice-to-have |
| No standalone eligibility view | `GET /platform/me/eligibility` is unused; blockers appear on opportunity detail | Deferred; the detail screen covers the task |
| No adaptive practice UI | `GET /academia/cbt/practice-next` exists | Deferred |
| No web offline submission queue | `POST /work/submissions/sync` exists | Deferred; mobile is the offline path at launch |
| No browser push registration | Settings lists/removes devices; the web app cannot register a browser device | Intentional; push is a mobile capability at launch |
| Student material upload/analysis | Curated materials + Ask + CBT + transcript are the replacement | Product decision: approve the replacement copy and remove the upload expectation |
| No skills search/filter | Catalog browsing only | Later scope |
| V1 ALL and language work | Not in V2 | See §I; the largest parity gap |

### 4.3 Student-surface verdict

The core student journey is built and state-honest. The remaining items are
deferred features or the V1 delta, not missing primary screens.

---

## 5. Admin surface (current)

### 5.1 What exists

The admin app exposes 14 hash sections: Overview, Audit, Imports, Users, Waitlist,
Opportunities, Projects, Review, Money, Content, Campus, Platform, Security and a
real 404. Login and forced 2FA are in place.

All admin screens use the shared page header, panel, skeleton, error and empty
primitives. Overview reads live queues and keeps rendering when one read fails.
Campus publishes through `POST /ops/campus` and reads the live set, including
hidden rows, through `GET /ops/campus`. Application status and payout-item failure
actions are exposed in Opportunities and Money.

### 5.2 Remaining gaps

| Gap | Current state | Impact |
|---|---|---|
| No bulk actions | Review, money and content are one row at a time | Useful improvement, not a launch blocker |
| No aggregate overview endpoint | Overview composes live queues | Optional optimisation |
| Richer application lifecycle | Statuses exist; deeper states can follow | Improvement |
| No newsletter/announcement admin | No feature exists | Only relevant if those features are approved |
| Admin 2FA browser verification | Code-complete; recovery-code handoff fixed | Needs one full end-to-end pass before launch |

### 5.3 Admin verdict

Admin is the strongest part of V2 functionally and now shares the student app's
design system at a denser rhythm. Bulk actions, an aggregate overview and richer
application states are useful next steps, not launch blockers.

---

## 6. API capabilities with no UI, and UI with no API

### 6.1 API-only (current)

| Endpoint | Missing UI |
|---|---|
| `GET /opportunities/matches` | Matches view; opportunity list shows verdicts only |
| `GET /platform/me/eligibility` | Standalone eligibility/readiness view; blockers are shown on opportunity detail |
| `GET /academia/cbt/practice-next` | Adaptive practice (deferred) |
| `POST /auth/google` | Google sign-in button (deferred) |
| `POST /work/submissions/sync` | Offline submission queue (deferred) |
| `GET /talent/me/transcript` | Duplicate of `/verification/transcript` |

Resolved by the build: consent history (`GET /me/consents`), push-device list and
removal (`GET/DELETE /me/push-devices`), my applications
(`GET /opportunities/applications`), cohort invitations (`GET /work/invites`,
`POST /work/cohorts/{id}/respond`), admin waitlist (`GET /ops/waitlist`), campus
read and publishing (`GET/POST /ops/campus`), course/topic detail, CBT history,
password change, application status (`POST /opportunities/applications/{id}/status`)
and payout-item failure (`POST /money/payout-items/{id}/fail`).

### 6.2 UI without a real API

No screen calls a missing endpoint. The two former false claims are resolved:

- **Signup terms acceptance** links to the legal pages and sends `accept_terms`;
  the backend records `terms_of_service` and `privacy_policy` at
  `TERMS_VERSION`. Consent history shows the recorded rows. `ConsentGate` asks an
  existing signed-in student to accept again when the platform version changes.
- **Push preference** is no longer a toggle that promises delivery. The web app
  says it cannot register a browser device and lists/removes devices registered
  elsewhere.

### 6.3 API-only verdict

The high-impact identity, notification, application and admin money edges are
reachable. The remaining API-only items are intentionally deferred (Google SSO,
offline sync, adaptive practice) or a nice-to-have view (matches, standalone
eligibility). Do not invent the deferred reads or business data.

---

## 7. Design-system audit (current)

### 7.1 Tokens

- Light/dark palettes, semantic surfaces, strong borders, subtle text, focus ring,
  info, accent contrast, elevation, motion, z-index, breakpoints, line-height,
  layout widths and touch minimum are published from
  `packages/design-tokens/src/index.ts`.
- Both apps consume the same tokens through the shared theme bridge.
- Admin no longer carries a separate palette; a second brand colour is banned.

### 7.2 Primitives

- `packages/ui` exports buttons, fields, textarea, select, checkbox, cards, panels,
  page headers, badges, stamps, banners, empty/error states, skeletons, spinner,
  avatar, theme toggle and shared CSS/fonts.
- `apps/web/src/ui.tsx` is a re-export alias; admin imports the same primitives.
- Add a dialog, menu or table primitive only when a real screen needs it; do not
  fork a primitive into an app.

### 7.3 Accessibility

Strengths: skip links, landmarks, shared focus styles, labelled forms,
route-change focus and document titles in both shells, `aria-current` on active
navigation, reduced-motion handling, and status colours paired with text.

Gaps:

- No automated axe check in CI. Add it with the first component-level test.
- A full keyboard, 200% zoom and forced-colors pass is still manual work.
- Older screens may still have sentence-case table headers; fix them when touched.

### 7.4 Performance and SEO

- First-load budget exists and passes: 123.1 KB gzip JS of 150 KB and 8.3 KB gzip
  CSS of 20 KB. Re-run `pnpm check:web-budget` before release.
- Public routes set title, description, canonical, robots and OG/Twitter metadata
  in `apps/web/src/lib/page-meta.ts`; the boot HTML carries the landing defaults.
- `sitemap.xml` covers the public marketing and legal routes; `robots.txt`
  disallows auth, private app routes and share tokens.
- No analytics or error tracking. This is an operational gap, not a UI gap.

### 7.5 Design-system verdict

The design system is built and shared, not a starting point. The remaining work is
keeping the guide, tokens and screens in sync and running the manual accessibility
pass. Do not introduce a second palette or a second component language.

## 8. V1 reference: what is real and what is not

V1 is a real product, but its public face and its signed-in surface are uneven.

### 8.1 V1 public

- Landing is polished, but **“2,500+” students is still fixed copy**, not derived
  from the database. V1 now repeats the same 2,500+/500+ figures on `/impact`
  (added 2026-11-01) alongside live university/skill counts. V2 must not copy
  those figures until the business confirms they are current and defensible.
- The campus section shows a hardcoded LASU map while the dynamic count can say
  “0 universities” (`landing.html:260,267,285`).
- About claims “live study sessions,” but the live-meeting route is retired.
- Footer social links default to `example.com`; local support email is
  `support@localhost`.
- PWA is a manifest and install prompt, but the service worker is actively
  unregistered. It is not offline-capable.
- There is no pricing page, standalone features page, how-it-works page, contact
  page, FAQ, newsletter, announcement banner or blog. There **is** now an
  `/impact` page and a landing track-record band (2026-11-01); V2 has neither.
- Legal pages exist, but they are not lawyer-reviewed and describe V1 features
  (community, employer self-service) that V2 drops.

### 8.2 V1 signed-in

V1 has a broad Academia and Skills product, a real employer surface and a deep
admin console. It also has a large retired perimeter: Community, Live Rooms,
Videos, Reels and old AI entry points have dead or orphaned student front doors
while their backends and admin tools remain. V1 has no admin audit UI; V2 does.

V1 capabilities worth preserving conceptually:

- Course/topic hub and CBT history/review.
- Threaded AI tutor and PDF→notes→test analysis.
- Evidence transcript and public talent profile.
- Employer discoverability (V2 defers self-service).
- Theme toggle.
- Admin content moderation and AI answer flags (V2 has different admin tools).
- **African Languages Lab (2026-10-30):** 94 language-data skills across 9
  categories, 10 multi-skill tracks, a self-reported language profile that is
  verified only by skills, structured transcription/translation/labeling/recording
  tasks with deterministic scores, and an assessment gate before verification.
- **Impact page (2026-11-01):** a public track-record page and landing band. The
  page is a good shape for V2, but its fixed figures need verification first.
- **FUTA taxonomy seed (2026-11-01):** verified schools, departments and 35
  Surveying & GeoInformatics courses, with `Course.source` provenance and a cleanup
  script. V2's importer drops the semester/source fields because its `Course`
  model does not have them.

V1 capabilities V2 intentionally drops or replaces:

- Community, live rooms, reels: dead/retired in V1; no V2 replacement needed.
- Employer self-service: deferred until after manual ops; V2 runs managed work.
- V1 gig marketplace and status-only earnings: replaced by the V2 ledger and
  managed projects.
- V1 30-day class/GPA/rank: replaced by managed cohorts and quality review.
- Click-to-complete verification: explicitly rejected; V2 requires evidence.

The full mapping is in `PARITY.md`.

---

## 9. Requested features: platform banner and newsletter

Both were checked against V1 and V2 code.

**Approved decision (2026-10-27): defer both.** They are not launch blockers and
are not part of the first UI build. The notes below are kept for the later
workstream.

### 9.1 Platform info banner

**Verdict: new feature, not parity. Useful, low-risk, but not a launch blocker.**

- No V1 public announcement bar exists. V1 only has authenticated banners (PWA
  install, CBT resume, campus location).
- No V2 global banner exists. `nv-banner` is an inline status/notice class, not a
  platform announcement.
- `PlatformConfigOut` has no announcement field (`apps/api/app/api/v1/domains/platform/schemas.py`).
- Admin `#/platform` edits currency, payout, age, terms and curriculum; no banner.

If approved, implement it as a small **announcements** feature, not a generic CMS:

- Public model: id, severity (`info`/`warning`/`critical`), message, optional link,
  starts_at, ends_at, dismissible, audience.
- Public API: `GET /platform/config` includes the current announcement, or a
  dedicated `GET /platform/announcements/current`.
- Admin API/UI: create, schedule, end and audit an announcement. One screen, not a
  page builder.
- Web UI: a dismissible banner above the site header and in the app shell; store
  dismissal by announcement id; do not show expired announcements.
- Do not use it for marketing. Use it for maintenance, launch notices and
  time-sensitive operational messages.

This requires backend work. It cannot be done as a UI-only change without
hardcoding, which would be worse than no banner.

### 9.2 Newsletter subscription

**Verdict: new feature, not parity. A separate marketing system, not a UI screen.**

- No V1 newsletter form, route, model or admin list.
- No V2 newsletter UI, endpoint, model or copy.
- A newsletter needs: consent record, double opt-in, unsubscribe, suppression
  list, rate limiting, spam controls, email provider, admin list/export, privacy
  policy update and a data-retention rule.
- “Admin UI for newsletter” alone is not enough. Without the consent and
  unsubscribe backend, it is a compliance liability.

Recommendation: **defer until after launch**, when there is a content plan and a
legal basis. If approved later, build it as a separate marketing workstream with
its own admin screen (`#/newsletter`) and a public form in the footer or a
dedicated page. Do not conflate it with the platform announcement banner.

### 9.3 What “admin UI for both” would mean

If both are approved, they are two different admin screens:

| Feature | Admin screen | Backend dependency |
|---|---|---|
| Platform announcement | `#/announcements` or a section of `#/platform` | announcement model, public read, audit |
| Newsletter | `#/newsletter` | subscriber model, consent, double opt-in, unsubscribe, export, email provider |

Neither belongs in the first design-system PR. They come after the core screens.

---

## 10. Launch blockers and missing screens

### 10.1 Launch blockers (current)

1. **Re-consent:** resolved by `ConsentGate`, which reads `/platform/config` and
   records both terms and privacy consent at the current version.
2. **Password change:** resolved by `POST /auth/password/change`; the current
   device receives a fresh session and other refresh tokens are revoked.
3. **Cohort invitations:** resolved by `GET /work/invites` and the response flow
   on `/work`.
4. **Admin campus read:** resolved by `GET /ops/campus`; hidden rows and their
   publication state remain visible to ops.
5. **Business content.** Approved pricing, support response expectations, real
   social links and proof metrics are not supplied. Do not invent them.
6. **Photography and image assets.** The editorial WebP set is integrated; real
   photography is opted out and not supplied.
7. **Admin 2FA and local flow verification.** Login works, but first-login
   enrolment and `dev-local.ps1` need an end-to-end pass.
8. **Domain switch and deployment.** V2 is not yet on the production domain.
9. **V1 delta not in V2 (2026-11-04).** The ALL curriculum, language profile,
   structured scored tasks, transcript/talent evidence, talent language filters
   and `/impact` are on V1 `main` but absent from V2. If V2 launches from
   `develop` as-is, it regresses V1's newest product surface. Decide port vs drop
   before the merge in `docs/runbooks/v2-launch-checklist.md` step 1.

### 10.2 Strongly recommended for parity/quality

- Student material upload/analysis, or publish the replacement copy that explains
  curated materials + Ask + CBT + the transcript evidence trail.
- “My matches” and a standalone eligibility/readiness view.
- Analytics and error tracking (not UI, but needed to run a launch).
- Bulk actions in review, money and content.
- A purpose-built admin overview endpoint.

### 10.3 Deliberately not in the first UI build

- Approved pricing amounts; `/pricing` ships commercial positions, not amounts.
- Employer self-service page without an employer product.
- Newsletter without consent/unsubscribe.
- Platform banner without an announcement backend.
- Google SSO until the button and consent flow are designed.
- Offline submission sync until the client queue is wired.


---

## 11. Documentation audit

| Document | State | Action |
|---|---|---|
| `docs/README.md` | Updated 2026-11-04 with the post-build V1 delta pointer | Keep the index and the delta note current |
| `docs/v2-ui/AUDIT.md` | Current 2026-11-04 | This file; update on every state change |
| `docs/v2-ui/PARITY.md` | Updated 2026-11-04 with §1.2, the V1 delta table | Keep the delta rows current on every V1 feature release |
| `docs/v2-ui/ROUTE-MAP.md` | Updated 2026-11-04 with §1.2, the V1 routes not yet in V2 | Add routes only after the product decision |
| `docs/v2-ui/DESIGN-DIRECTION.md` | Approved 2026-10-27, implemented 2026-10-28, V1-delta visual rules added 2026-11-04 | Keep the delta section tied to the approved direction; no new palette |
| `docs/v2-ui/IMAGE-PROMPTS.md` | Status corrected 2026-11-04: P1/P2 assets are generated and integrated as WebP/JPG derivatives; real photography still pending | Keep the prompts for regeneration; do not re-export the whole set for an unrelated change |
| `docs/design/ui-ux-framework.md` | Current guard, updated 2026-11-04 with the V1 delta row and the ALL/language route note | Keep it in sync with the approved tokens and routes |
| `docs/architecture/06-roadmap.md` | Updated 2026-11-04: delivery status records Phases 0-8 delivered and adds the V1 delta | Keep the status table and the V1 delta table in sync with `REMAINING_WORK.md` |
| `docs/architecture/07-risk-register.md` | Updated 2026-11-04 with R15, V2 shipping smaller than live V1 | Keep R15 until the delta is ported or dropped |
| `docs/architecture/04-v1-to-v2-migration.md` | Updated 2026-11-04 with the V1 additions table, sequencing rule and migration head | Keep the schema/import implications aligned with `PARITY.md` |
| `docs/architecture/05-domain-map.md` | Updated 2026-11-04 with the V1 additions and their target placement | Keep entity ownership and V2 target fields current |
| `docs/architecture/01-target-structure.md` | Updated 2026-11-04 with `seed_data/all_skills/` and `futa_official_structure.md` | Keep V1-only file placement described as V1-only |
| `docs/architecture/00-audit.md` | Historical V1 audit, marked historical 2026-11-04; not V2 UI status | Keep as context; do not use for V2 readiness |
| `docs/build/REMAINING_WORK.md` | Updated 2026-11-04 with the V1 delta (§I) and the known unused/partial V2 edges (§J); still a build tracker, not the UI readiness list | Keep; UI gaps live in `docs/v2-ui/AUDIT.md` |
| `docs/build/phase-1-10-plan.md` | Updated 2026-11-04: Phases 7 and 8 delivered, with the post-build delta section | Keep the per-phase narrative aligned with the tracker |
| `docs/build/nelavista-02-v2-build-prompt.md` | Historical work order; a 2026-11-04 note corrects the “V1 frozen” assumption | Keep as build history; do not execute its V1-reuse assumptions blindly |
| `docs/build/phase-0-plan.md` | Completed plan; useful history but not current | Keep as historical |
| `docs/runbooks/v2-launch-checklist.md` | Deployment plan updated 2026-11-04 with the V1-delta merge gate | Do not treat it as proof the UI is ready |
| `docs/runbooks/local-setup.md` | Updated with no-Docker path | Keep |
| `docs/SECRETS_ROTATION.md` | Current operational checklist | Keep |
| `docs/MIGRATION_MAP.md` | Removed; recorded the rejected “keep Flask” path and stale counts | Decision lives in ADR-0001 and git history |
| `docs/TEMPLATE_CLASSIFICATION.md` | Removed with `MIGRATION_MAP.md` | Historical V1 template cleanup; git history |
| `docs/build/nelavista-01-organise-codebase-prompt.md` | Removed; completed prompt | Git history |

**Deletion rule:** delete only after confirming no current instruction depends on
the file. Historical context stays in git history.

---

## 12. Needs your input

These cannot be invented by the UI:

1. **Approved pricing amounts.** Is V2 free for students? Is there an employer/ops
   price? `/pricing` ships commercial positions, not amounts; replace them when the
   business approves figures.
2. **Legal copy approval.** Privacy, terms and contributor terms are final product
   copy for V2's actual data flows (payments, verification, managed work, no
   community). Confirm counsel approval and keep the version aligned with
   `/platform/config`; V1 text is not safe to copy back.
3. **Support contact.** `support@nelavista.com` is used; response expectation and
   real social links are still needed. V1's `support@localhost` and `example.com`
   links are not usable.
4. **Real proof.** Any student count, university count, testimonial or partner
   logo must be current and verifiable. V1's “2,500+” is hardcoded and should not
   be carried forward.
5. **Photography.** Real founder/team/campus photos, or approval to launch with
   no photos and product artifacts only.
6. **Employer positioning.** Is there a public “For employers” page at launch, or
   is employer contact ops-led?
7. **Newsletter decision.** Defer, or approve the consent/unsubscribe backend and
   admin screen.
8. **Platform banner decision.** Include a small announcement feature now, or
   defer until there is a real announcement to show.
9. **Course/topic and CBT history API detail.** Resolved: full course/topic detail
   (`GET /academia/courses/{id}`, `/topics/{id}`) and CBT history with answer review
   are built and used by the screens.
10. **Student uploads/analysis.** Restore V1's PDF→notes→test, or approve the
    replacement copy: curated materials + Ask + CBT + the transcript evidence
    trail.
11. **Brand video placement.** Resolved. The 1920x1080 MP4 runs full-width before
    the public footer with a reduced-motion still. It stays an opaque brand film,
    not a transparent loader.
12. **Image production.** Editorial WebP derivatives are integrated. Commission
    real photography before launch; do not launch with generic stock or invented
    campus/founder photography.
13. **African Languages Lab.** Port the 94-skill ALL curriculum, language profile
    and structured scored tasks into V2, or launch V2 without V1's newest skills
    catalogue? This is the largest post-build product decision.
14. **Impact metrics.** Are “2,500+ students reached” and “500+ trained in AI”
    current, verifiable and approved for public use? If yes, add `/impact` and the
    landing band; if no, keep the honest `/about` working-record copy.
15. **FUTA taxonomy.** Import the verified FUTA taxonomy from V1, or seed it
    natively in V2? If imported, V2's `Course` model needs `semester` and `source`
    first, because the importer currently drops both.


---

## 13. Verification

### 13.1 At audit time (Phase 0 baseline)

| Check | Result |
|---|---|
| API tests | 332 passed, 1 skipped (333 collected; 10m 42s) |
| Web tests | 53 passed (10 files) |
| Admin tests | 1 passed (1 file) |
| Typecheck/lint/build | Not re-run in this audit; run before UI work |
| Local V2 setup | Documented in `RUN-LOCALLY.md`; zero-config SQLite path exists |
| Admin 2FA | Login works; first-login enrolment is required and still needs a full end-to-end pass |
| V1 reference | Read-only; no V1 files changed |

### 13.2 Post-build verification (2026-11-03)

| Check | Result |
|---|---|
| Web typecheck | Passed |
| Admin typecheck | Passed |
| Web tests | 57 passed (11 files) |
| Admin tests | 2 passed (1 file) |
| API tests | 340 passed, 1 skipped |
| Web/admin lint | Passed |
| Web/admin production build | Passed |
| First-load budget | Passed: 123.1 KB gzip JS of 150 KB; 8.3 KB gzip CSS of 20 KB |
| Prettier / `git diff --check` | Passed |
| Brand assets | V1 logo/favicon copied, V2 icons generated, boot loader present in both apps |
| Theme | Light and dark tokens verified in code; manual visual pass still recommended |
| API closure | New routes covered by API tests; no live deployment run |
| V1 reference | Read-only; no V1 files changed |

The Phase 0 audit itself did not change code; the post-build rows record the
redesign that followed. The checks in 13.2 were last recorded on 2026-11-03
against the working tree, not against a deployed environment.

### 13.3 V1 delta verification (2026-11-04)

| Check | Result |
|---|---|
| V1 `main` pull | Fast-forwarded to `afd61b6`; 12 commits, including ALL, Impact and FUTA |
| V2 search for the delta | No `African Languages`, `StudentLanguage`, `language_profile`, `impact` or `FUTA` implementation in `apps/` |
| V2 test suite | Not re-run for this documentation audit; the last recorded run is §13.2 |
| V1 files changed by this audit | None; V1 is read-only reference |

This audit only updated documentation. It did not port code, run migrations or
change V1.


---

## 14. Bottom line

V2 is now functionally broad and visually coherent on Nelavista blue and white.
The public surface, auth, student journey, admin tools, brand assets, metadata and
the high-impact consent/push/application/payout edges are built. The remaining
work is not UI invention:

1. **The V1 delta:** ALL, the language profile, structured scored tasks,
   transcript/talent evidence, talent language filters and `/impact` are not in
   V2. Port them or explicitly drop them before the launch merge.
2. Approved pricing and real business content, including social profile URLs,
   metrics and employer positioning.
3. The editorial image set is integrated; real photography was opted out.
4. End-to-end admin 2FA, one clean local setup run and a manual light/dark visual
   pass.
5. Analytics/error tracking before launch and the deployment-level domain switch.

Do not invent the missing business copy or imagery. Ship the working record that
exists and finish the manual launch checks.
