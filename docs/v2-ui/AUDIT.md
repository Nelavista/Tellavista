# V2 UI/UX audit — Phase 0 baseline

| Field | Value |
|---|---|
| Status | **Post-build 2026-10-28. Gates 1 and 2 approved 2026-10-27. Core UI build complete; remaining items are API/content dependencies and launch verification.** |
| Date | 2026-10-27; post-build and palette correction 2026-10-28 |
| Scope | Current V2 web, admin, design tokens and UI-facing API contracts; V1 used only as a reference |
| Not in scope | V1 code changes, backend changes, deployment changes, mobile launch |
| Companion documents | `docs/v2-ui/PARITY.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/DESIGN-DIRECTION.md`, `docs/v2-ui/IMAGE-PROMPTS.md`, `docs/design/ui-ux-framework.md` |

> This is the Phase 0 baseline. It records what existed before the redesign, what
> was broken or missing, what V1 actually does, and which documents were stale.
> The parity decisions are in `PARITY.md`; the route contract is in `ROUTE-MAP.md`;
> the visual direction is in `DESIGN-DIRECTION.md`. Read §1.1 first: it is the
> current state, and it overrides the baseline tables below where they disagree.
> Sections 2–14 are intentionally kept as the starting-point record.

## 1.1 Post-build status (2026-10-28)

The redesign has landed in code. This section replaces the baseline where they
disagree; the rest of the document remains useful as the starting-point record.

- **Design system:** Light/dark palettes built on Nelavista blue `#1535A8` and
  white `#FFFFFF`, the shared theme bridge, primitives, shared CSS and three
  self-hosted font families are in `packages/ui`. Web and admin both consume them.
- **Brand assets:** The V1 logo and favicon are copied into both V2 apps. The
  uploaded WebP is the boot and route loader, with a still-mark and
  reduced-motion fallback. The MP4 is a 1920x1080 brand video with a blue
  background, not a transparent loader, and is not used in the UI yet.
- **Public surface:** Landing, Features, How it works, About, Contact, FAQ,
  Privacy, Terms, Contributor terms, a real 404 and an offline screen exist as
  separate routes. Legal copy is an explicit draft pending counsel. Every public
  page now sets a title, description, canonical, robots and OG/Twitter metadata;
  `sitemap.xml` and `robots.txt` cover the public pages and disallow private app
  routes.
- **Auth:** Login, Signup, Verify email and Reset password use the shared auth
  layout and set page metadata. Signup links to the draft legal pages.
- **Student app:** The grouped app shell, mobile navigation, theme toggle,
  notifications, applications, CBT history, course detail and split settings
  routes exist. Home, Academia, Materials, Ask, CBT, Skills, My learning, Lesson,
  Practice, Verification, Assessment sitting, Attempt review, Practical task,
  Transcript, Opportunities, Applications, Work, Earnings, Talent, Campus,
  Notifications, Settings and Onboarding use the shared primitives and explicit
  states. Eligibility blockers are shown on opportunity detail before apply.
- **Settings:** Profile, security, notifications and data are separate routes.
  Consent history is read from `/me/consents` and rendered as an append-only
  table. Push devices are read from `/me/push-devices` and can be removed; the
  web app does not claim to register a browser device. The old push checkbox that
  promised delivery without a device is gone.
- **Admin:** The grouped shell, Overview, Waitlist, Campus, Audit, Imports, Users,
  Opportunities, Projects, Review, Money, Content, Platform, Security and a real
  404 exist. All admin screens now use the shared page header, panel, skeleton,
  error and empty primitives. Overview reads live queues; Campus is write-only
  because the read endpoint is missing. Application status and payout-item
  failure actions are exposed in Opportunities and Money.
- **Still open (API dependencies):** Course/topic detail beyond the current course
  route, CBT history/review detail, the student cohort-invite list, an admin
  campus read endpoint and a signed-in change-password endpoint. The admin Campus
  screen remains write-only with an explicit banner and session-local receipts.
- **Still open (business/content):** pricing, counsel-reviewed legal copy, real
  social links, real metrics/testimonials, photography, employer positioning and
  the material upload/analysis replacement copy. Images named in
  `IMAGE-PROMPTS.md` are not created yet. The MP4 brand video needs a placement
  decision.
- **Still open (verification):** Admin 2FA enrolment and the full
  `dev-local.ps1` flow are not verified end-to-end; the V2 domain switch is
  pending; legal pages remain drafts and block launch.
- **Removed as unused:** `Logo`, `ArrowLink` and `Spinner` exports, the unused
  spinner CSS, and `apps/web/src/components/Layout.tsx`.


---

## 1. Executive summary

V2 is a broad, working student journey with a real API, a real admin tool and an
honest state model. It is **not** a finished public product or a finished visual
system.

The short version:

- **The product spine is real.** Auth, onboarding, academia, skills, verification,
  opportunities, work, money, talent, campus and admin all have API routes and
  most have web screens.
- **The public surface is a stub.** The landing page is 36 lines. There is no
  Features, How it works, About, Contact, FAQ, Pricing or Legal route. Signup asks
  the student to accept terms that do not exist in V2.
- **The UI is a functional wireframe, not a design.** One top nav with 14 links,
  a 720px content column, local primitives, no icons, no motion, no responsive
  app shell, no page-level meta, no 404, no error boundary.
- **Admin is a second design system.** It hard-codes a different palette and
  different sizes instead of consuming `@nelavista/design-tokens`.
- **Several API capabilities have no UI.** The most serious are consent history,
  push-device registration, cohort invite response, admin waitlist/campus,
  application status and payout-item failure.
- **Two requested features are new, not parity.** There is no platform
  announcement banner and no newsletter/subscription feature in V1 or V2. The
  banner is a small, useful ops feature; the newsletter is a separate marketing
  system with consent, unsubscribe and data-protection work. Neither is required
  for V2 parity or the core launch.

**Verdict:** V2 has the hard product work; it does not yet have the public face,
the design system, the missing screens or the operational edges that make it feel
finished. The redesign should start with tokens and primitives, not with the
landing page.

---

## 2. What V2 is today

### 2.1 Stack

| Area | Current state |
|---|---|
| Student web | React 18.3 + Vite 5.4 + TypeScript, React Router 6.28, plain CSS + CSS variables, PWA via `vite-plugin-pwa` |
| Admin | React 18.3 + Vite 5.4 + TypeScript, in-repo hash router, its own CSS palette |
| API | FastAPI modular monolith under `/api/v1`, 13 mounted domain routers |
| Tokens | `packages/design-tokens/src/index.ts`; web publishes them at boot, admin does not |
| Shared UI | `packages/ui` exports only `VersionSwitcher`; web has local primitives in `apps/web/src/ui.tsx` |
| Tests | Vitest + jsdom; no Testing Library, axe, Playwright or visual regression |

### 2.2 Route surface

| Surface | Routes | Notes |
|---|---|---|
| Public | `/`, `/login`, `/signup`, `/auth/verify`, `/auth/reset`, `/share/:token` | Landing is the only marketing page; share is public by token |
| Signed-in web | 26 routes | Home, onboarding, academia, skills, verification, opportunities, work, money, talent, transcript, campus, settings |
| Admin | 10 hash sections | Audit, imports, users, opportunities, work, review, money, content, platform, security |
| Catch-all | `*` | Redirects to `/`; no 404 screen |
| Admin fallback | any unknown hash | Renders Audit; no admin 404 |

The exact route list is in `ROUTE-MAP.md` and `apps/web/src/App.tsx:104-353`.

### 2.3 What is genuinely strong

- **State honesty.** Most screens distinguish loading, empty, error and
  feature-off. `useApiResource` maps a 404 `not_found` to “not switched on here”
  (`apps/web/src/lib/resource.ts:18-63`).
- **Security and money are not cosmetic.** Verification is evidence-backed, the
  ledger is append-only, payouts need a second approver, and staff need TOTP.
- **Admin is real.** Audit, imports, users, review, money, content, platform and
  security are working tools, not mockups.
- **PWA basics exist.** Manifest, icons, offline shell, robots, sitemap and a
  Google verification file are present. API responses are deliberately not cached.
- **The API is broad.** Identity, academia, skills, verification, opportunities,
  talent, work, money, platform and ops are mounted. Several endpoints are ahead
  of the UI.

---

## 3. Public surface

### 3.1 What exists

| Item | Evidence | State |
|---|---|---|
| Landing | `apps/web/src/routes/Landing.tsx:4-36` | Headline, two-path card, signup/login CTAs. No features, proof, FAQ, footer or SEO. |
| Signup | `apps/web/src/routes/Signup.tsx` | Name, email, username, password, terms checkbox. Terms checkbox has no links. |
| Login | `apps/web/src/routes/Login.tsx` | Password login and staff 2FA challenge. |
| Verify email | `apps/web/src/routes/VerifyEmail.tsx` | Token consumption, resend path. |
| Reset password | `apps/web/src/routes/ResetPassword.tsx` | One route with request and set-password states. |
| Shared profile | `apps/web/src/routes/SharedProfile.tsx` | Public by token, scoped and revocable. |
| PWA | `apps/web/vite.config.ts:13-45`, `main.tsx:24-26` | Installable shell; API responses not cached. |
| Robots/sitemap | `apps/web/public/robots.txt`, `sitemap.xml` | Sitemap has only `/`, `/signup`, `/login`; `/share/` is disallowed. |
| Meta | `apps/web/index.html:4-8` | Title only. No description, canonical, OG or Twitter card. |

### 3.2 What is missing

| Missing | Why it matters |
|---|---|
| `/features` | The landing page is the only explanation of the product. |
| `/how-it-works` | The journey is the product's differentiator; it has no page. |
| `/about` | V1 has one; V2 has none. |
| `/contact` | No support path on the public site. |
| `/faq` | No answer to the obvious objections (free? verified? paid? data?). |
| `/pricing` | No pricing model exists in V2. Do not invent one. V1 only says “free for students”; V2 has no public price. |
| `/legal/privacy`, `/legal/terms` | Signup requires acceptance but links nowhere. This is a launch blocker. |
| `/legal/contributor-terms` | The platform has contributor terms in `platform_settings`; students cannot read them before work. |
| Public 404 | Unknown paths redirect to `/`, which hides broken links. |
| Public SEO | No per-page title/description, OG, canonical or JSON-LD. |
| Analytics | No analytics or error tracking in either app. |
| Newsletter | No form, endpoint, consent, unsubscribe or admin list. |
| Platform announcement | No global banner; `nv-banner` is an inline notice, not a platform announcement. |
| Employer page | V2 has no employer self-service; do not publish an employer product page until the business decides. |
| Theme | V2 now has light/dark surfaces on brand blue and white. V1 has a theme toggle. |

### 3.3 Public-surface verdict

V2's public surface is **not launch-ready**. It is a product demo behind a login,
with no legal pages, no support path, no explanation of how it works and no
crawlable marketing content. This is the largest gap between “the app works” and
“a student can find, trust and join it.”

---

## 4. Signed-in surface

### 4.1 What exists

The student app has the core journey:

- **Home / onboarding** — path choice, course state, verification banner.
- **Academia** — dashboard, materials list/search/reader, Ask Nelavista, CBT
  practice and results, campus.
- **Skills** — catalog, skill detail, path, lesson, practice, my learning.
- **Verification** — hub, assessment sitting, attempt review, practical task,
  transcript.
- **Opportunities** — list with per-student verdict, detail and apply.
- **Work** — assignments, submissions, quality, assignment detail and messages.
- **Money** — earnings.
- **Talent** — evidence profile, share links, revoke.
- **Settings** — profile, languages, availability, notification list, export,
  delete account.

### 4.2 Missing or weak signed-in screens

| Gap | Evidence | Impact |
|---|---|---|
| No dedicated notifications route | Notifications appear only as a 10-item list inside Settings (`Settings.tsx:311-358`) | Students cannot triage notifications; deep links are buried. |
| No change-password flow | No `change-password` endpoint or UI; only reset-by-email (`identity/routes.py`) | A signed-in student cannot rotate a password. |
| No re-consent UI | Consent history is now built from `GET /me/consents`; `POST /auth/consent` is still unused | A terms-version change cannot be accepted in-product; legal evidence is incomplete. |
| No browser push-device registration | Settings lists/removes `/me/push-devices`; the web app still cannot register a browser device | Push requires the mobile app; the copy is now honest. |
| No cohort invite response | `POST /work/cohorts/{id}/respond` exists; no web UI | Admin can invite; the student cannot accept or decline. |
| "My applications" | Built at `/opportunities/applications` | Students can see what they applied to and its status. |
| No “matches” view | `GET /opportunities/matches` exists; list shows verdicts only | Matching work is under-exposed. |
| No eligibility view | `GET /platform/me/eligibility` exists; no screen | Students discover age/consent blockers inside an opportunity, too late. |
| No CBT history | V2 shows current results only; V1 had history and attempt review | Students cannot revisit past practice or see improvement. |
| No course/topic pages | V2 has dashboard + materials; V1 had course and topic detail | Students lose the single-course hub and topic-level learning. |
| No student material upload/analysis | V1 had uploads, my-uploads and PDF→notes→test; V2 has curated materials only | A real V1 capability is dropped; decide whether to restore or explicitly replace. |
| No standalone search across courses/skills | Materials search exists; skills list has no search/filter | Finding a course or skill depends on browsing. |
| No page-level loading/error consistency | Home uses plain “Loading…”; Campus and Academia hand-roll state | The app feels uneven and can mislabel a flag-off as an error. |
| No global error boundary | Only `React.Suspense` | A render error blanks the app. |
| No 404 | Catch-all redirects to `/` | Broken links look like the home page. |

### 4.3 Signed-in verdict

The journey is present, but it is a collection of screens rather than a designed
product. The biggest student-facing gaps are notifications, password change,
consent, push devices, cohort invites, applications and CBT history. The biggest
experience gap is the lack of a real app shell, page headers and table/list
language.

---

## 5. Admin surface

### 5.1 What exists

`apps/admin/src/App.tsx` and `Shell.tsx` expose:

`#/audit`, `#/imports`, `#/users`, `#/opportunities`, `#/work`, `#/review`,
`#/money`, `#/content`, `#/platform`, `#/security`, plus login and forced 2FA.

Admin is genuinely operational: audit search, V1 import, user lookup, opportunity
creation and candidates, projects/cohorts, review queue, ledger and payout
batches, content authoring, platform policy and 2FA.

### 5.2 Admin gaps (current)

| Gap | Evidence | Impact |
|---|---|---|
| No campus read endpoint | `POST /ops/campus` exists; no ops list/read route | Campus remains write-only with session-local receipts; ops cannot audit published content in-app. |
| No student cohort-invite list | `POST /work/cohorts/{id}/invites` and `/respond` exist; no list endpoint | Admin can invite, but the student cannot see or answer an invite in-product. |
| Applications are now actionable | `POST /opportunities/applications/{id}/status` is exposed in Opportunities | Resolved; statuses are interested, applied, shortlisted, withdrawn and rejected. |
| Payout items are now actionable | `POST /money/payout-items/{id}/fail` is exposed in Money | Resolved; a reason is required and audited. |
| No admin 404 | Unknown hash renders a real `AdminNotFound` | Resolved. |
| No skeletons | Shared `Skeleton`, `EmptyState`, `ErrorState` and `Panel` are used across admin | Resolved. |
| No bulk actions | Review, money and content are one-row at a time | Ops work does not scale. |
| No aggregate overview endpoint | Overview composes live queues; one failed read does not hide the rest | Acceptable for now; a purpose-built aggregate API is a later optimisation. |
| No newsletter/announcement admin | No feature exists | Only relevant if those features are approved. |

### 5.3 Admin verdict

Admin is the strongest part of V2 functionally and now shares the student app's
design system at a denser rhythm. The remaining work is API-backed: a campus read
endpoint, a student cohort-invite list, and a purpose-built aggregate overview.
Bulk actions and richer application lifecycle states are useful next steps, not
launch blockers.

---

## 6. API capabilities with no UI, and UI with no API

### 6.1 API-only (current)

| Endpoint | Missing UI |
|---|---|
| `POST /work/cohorts/{id}/respond` | Accept/decline a cohort invite; no list endpoint exists to find the invite first |
| `GET /opportunities/matches` | Matches view; opportunity list shows verdicts only |
| `GET /platform/me/eligibility` | Standalone eligibility/readiness view; blockers are shown on opportunity detail |
| `GET /academia/cbt/practice-next` | Adaptive practice (deferred) |
| `POST /auth/google` | Google sign-in button (deferred) |
| `POST /work/submissions/sync` | Offline submission queue (deferred) |
| `GET /talent/me/transcript` | Duplicate of `/verification/transcript` |

Resolved by the build: consent history (`GET /me/consents`), push-device list and
removal (`GET/DELETE /me/push-devices`), my applications
(`GET /opportunities/applications`), admin waitlist (`GET /ops/waitlist`), admin
campus publishing (`POST /ops/campus`), application status
(`POST /opportunities/applications/{id}/status`) and payout-item failure
(`POST /money/payout-items/{id}/fail`).

### 6.2 UI without a real API

No screen calls a missing endpoint. The two former false claims are resolved:

- **Signup terms acceptance** links to the draft legal pages and sends
  `accept_terms`; the backend records `terms_of_service` at `TERMS_VERSION`.
  Consent history shows the recorded row. What is not built is re-consent when
  the terms version changes; `POST /auth/consent` exists but has no UI.
- **Push preference** is no longer a toggle that promises delivery. The web app
  says it cannot register a browser device and lists/removes devices registered
  elsewhere.


### 6.3 API-only verdict

The high-impact identity, notification, application and admin money edges are now
reachable. The remaining API-only items are either blocked on a missing list
endpoint (cohort invites), intentionally deferred (Google, offline sync, adaptive
practice) or a nice-to-have view (matches, standalone eligibility). Do not invent
the missing reads.

---

## 7. Design-system audit

### 7.1 Tokens

Current tokens (`packages/design-tokens/src/index.ts:6-26`):

- 10 colours, 6 spacing values, 4 radii, one system font stack and 5 sizes.
- Missing: semantic surfaces, strong border, subtle text, focus ring, info,
  accent contrast, elevation, motion, z-index, breakpoints, line-height, layout
  widths and touch minimum.
- `typography.sizes.xl` is defined but not published by `apps/web/src/lib/theme.ts`.
- Web CSS still carries fallback hex values and raw spacing.
- Admin declares a different palette (`apps/admin/src/styles.css:1-12`) and never
  imports the tokens.

### 7.2 Primitives

- Web has `Button`, `Field`, `Select`, `Skeleton`, `ErrorNote` in
  `apps/web/src/ui.tsx`.
- Admin has no shared primitive module; screens repeat raw `.nv-*` markup.
- `packages/ui` has only `VersionSwitcher`.
- There is no icon library, no toast, no dialog, no drawer, no table, no tabs, no
  tooltip, no command menu, no form validation summary.
- No shared stylesheet; `.nv-*` classes are duplicated across web and admin with
  different values.

### 7.3 Accessibility

Strengths: `aria-busy` on loading regions, `role="alert"` on web errors,
`aria-label` on admin nav.

Gaps:

- No skip link.
- No `aria-current` on active nav.
- No route-change focus management.
- No reduced-motion handling.
- Admin errors often lack `role="alert"`.
- No axe or keyboard test suite.

### 7.4 Performance and SEO (current)

- First-load budget exists and passes; re-run `pnpm check:web-budget` before
  release.
- No analytics, Sentry or other telemetry. This remains an operational gap, not a
  UI gap.
- Public routes now set title, description, canonical, robots and OG/Twitter
  metadata in `apps/web/src/lib/page-meta.ts`; the boot HTML carries the landing
  defaults.
- `sitemap.xml` covers the public marketing and legal routes; `robots.txt`
  disallows auth, private app routes and share tokens.

### 7.5 Design-system verdict

The tokens are a starting point, not a system. The redesign needs a token
foundation first, then shared primitives, then screens. Building pages on the
current primitives would repeat the same local-CSS drift.

---

## 8. V1 reference: what is real and what is not

V1 is a real product, but its public face and its signed-in surface are uneven.

### 8.1 V1 public

- Landing is polished, but **“2,500+” students is hardcoded** and not derived from
  the database (`app/templates/landing.html:273,278`;
  `app/routes/dashboard_routes.py:69-70`). The local DB has one user.
- The campus section shows a hardcoded LASU map while the dynamic count can say
  “0 universities” (`landing.html:260,267,285`).
- About claims “live study sessions,” but the live-meeting route is retired.
- Footer social links default to `example.com`; local support email is
  `support@localhost`.
- PWA is a manifest and install prompt, but the service worker is actively
  unregistered. It is not offline-capable.
- There is no pricing page, standalone features page, how-it-works page, contact
  page, FAQ, newsletter, announcement banner or blog.
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

1. **Legal review.** The privacy, terms and contributor-terms pages exist as
   explicit drafts. Counsel must review them against V2's actual data flows before
   launch.
2. **Re-consent.** Signup records `terms_of_service` at `TERMS_VERSION` and
   consent history is visible. When the version changes, there is no UI to ask an
   existing student to accept again; `POST /auth/consent` is unused.
3. **Password change.** No signed-in password rotation endpoint; reset-by-email is
   the only path.
4. **Cohort invite response.** Managed work is one-sided without a student-facing
   invite list and response UI.
5. **Admin campus read.** Publishing is write-only; ops cannot audit the published
   list in-app.
6. **Business content.** Pricing (if any), support response expectations, real
   social links and proof metrics are not supplied. Do not invent them.
7. **Photography and image assets.** The prompt manifest is ready; the files are
   not.
8. **Admin 2FA and local flow verification.** Login works, but first-login
   enrolment and `dev-local.ps1` need an end-to-end pass.
9. **Domain switch and deployment.** V2 is not yet on the production domain.

### 10.2 Strongly recommended for parity/quality

- Course/topic detail beyond the current course route, and CBT history/review
  detail, or an explicit decision that the current screens are the replacement.
- Student material upload/analysis, or publish the replacement copy that explains
  curated materials + Ask + CBT + the transcript evidence trail.
- “My matches” and a standalone eligibility/readiness view.
- Analytics and error tracking (not UI, but needed to run a launch).
- Bulk actions in review, money and content.
- A purpose-built admin overview endpoint.

### 10.3 Deliberately not in the first UI build

- Pricing page without a pricing model.
- Employer self-service page without an employer product.
- Newsletter without consent/unsubscribe.
- Platform banner without an announcement backend.
- Google SSO until the button and consent flow are designed.
- Offline submission sync until the client queue is wired.


---

## 11. Documentation audit

| Document | State | Action |
|---|---|---|
| `docs/README.md` | Current but incomplete; lists historical docs as “read first” in places | Update index; add `docs/v2-ui/`; separate current from historical |
| `docs/design/ui-ux-framework.md` | Current guard, corrected after Gate 2 approval to the light/dark brand blue and white direction | Keep it in sync with the approved tokens and routes |
| `docs/architecture/06-roadmap.md` | Delivery table is stale: says M7 Talent UI and M8 materials/Ask/CBT are owed, but they are delivered | Update delivery status and remove dead Sentry/PostHog claim |
| `docs/build/REMAINING_WORK.md` | Updated 2026-10-27; now a build tracker, not the UI readiness list | Keep; UI gaps live in `docs/v2-ui/AUDIT.md` |
| `docs/MIGRATION_MAP.md` | Superseded: records the rejected “keep Flask” decision and stale counts | **Delete**; keep the decision in ADR-0001 and git history |
| `docs/TEMPLATE_CLASSIFICATION.md` | Historical V1 template cleanup; only referenced by MIGRATION_MAP | **Delete** with MIGRATION_MAP |
| `docs/build/nelavista-01-organise-codebase-prompt.md` | Completed prompt; no longer needed | **Delete** |
| `docs/build/phase-0-plan.md` | Completed plan; useful history but not current | Keep as historical, or delete if the team does not need the audit trail |
| `docs/build/phase-1-10-plan.md` | Per-phase delivery record; current enough | Keep, update references if REMAINING_WORK is retired |
| `docs/architecture/00-audit.md` | Historical V1 audit; still useful context but not V2 UI status | Keep but mark historical; remove from “read first” |
| `docs/runbooks/local-setup.md` | Updated with no-Docker path | Keep |
| `docs/runbooks/v2-launch-checklist.md` | Deployment plan, not UI readiness | Keep; do not treat as proof the UI is ready |
| `docs/SECRETS_ROTATION.md` | Current operational checklist | Keep |

**Deletion rule:** delete only after confirming no current instruction depends on
the file. Historical context stays in git history.

---

## 12. Needs your input

These cannot be invented by the UI:

1. **Pricing model.** Is V2 free for students? Is there an employer/ops price? If
   there is no public price, do not build `/pricing`.
2. **Legal copy.** Privacy and terms must be reviewed for V2's actual data flows
   (payments, verification, managed work, no community). V1 text is not safe to
   copy unchanged.
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
9. **Course/topic and CBT history API detail.** Course and CBT history screens
   exist; the missing piece is the API detail for full topic content and CBT
   attempt review. Provide the endpoints or confirm the current screens are the
   replacement.
10. **Student uploads/analysis.** Restore V1's PDF→notes→test, or approve the
    replacement copy: curated materials + Ask + CBT + the transcript evidence
    trail.
11. **Brand video placement.** The uploaded MP4 is 1920x1080 with a blue
    background, not a transparent loader. Decide whether it appears on the public
    site, in onboarding, or nowhere. If it must be a transparent loader, supply a
    short looping WebM/VP9 with alpha (or HEVC with alpha for Safari) at 1:1,
    ideally under 500 KB; the current opaque 16:9 file is not that asset.
12. **Image production.** Approve the prompt manifest and supply or commission the
    P1 images; do not launch with generic stock or invented campus/founder
    photography.


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

### 13.2 Post-build verification (2026-10-28)

| Check | Result |
|---|---|
| Web typecheck | Passed |
| Admin typecheck | Passed |
| Web tests | 57 passed (11 files) |
| Admin tests | 2 passed (1 file) |
| Web/admin lint | Passed |
| Web/admin production build | Passed |
| First-load budget | Passed: 116.0 KB gzip JS of 150 KB; 7.0 KB gzip CSS of 20 KB |
| Prettier / `git diff --check` | Passed |
| Brand assets | V1 logo/favicon copied, V2 icons generated, boot loader present in both apps |
| Theme | Light and dark tokens verified in code; manual visual pass still recommended |
| API dependencies | Not exercised end-to-end; see §10.1 |
| V1 reference | Read-only; no V1 files changed |

The Phase 0 audit itself did not change code; the post-build rows record the
redesign that followed. The checks above were run on 2026-10-28 against the
working tree, not against a deployed environment.


---

## 14. Bottom line

V2 is now functionally broad and visually coherent on Nelavista blue and white.
The public surface, auth, student journey, admin tools, brand assets, metadata and
the high-impact consent/push/application/payout edges are built. The remaining
work is mostly not UI invention:

1. Legal review and a re-consent UI when the terms version changes.
2. A signed-in password-change endpoint.
3. Course/topic and CBT attempt-review detail endpoints; the CBT history route
   already exists as an explicit dependency state.
4. A student cohort-invite list endpoint and an admin campus read endpoint.
5. Real business content, photography and the approved image set.
6. End-to-end admin 2FA, the full local setup, a manual light/dark visual pass and
   the domain switch.
7. Analytics/error tracking before launch.

Do not invent the missing reads, business copy or imagery. Ship the working
record that exists, then close the API and content dependencies.
