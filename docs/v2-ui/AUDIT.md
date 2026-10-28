# V2 UI/UX audit — Phase 0 baseline

| Field | Value |
|---|---|
| Status | **Phase 0 baseline. Gates 1 and 2 approved 2026-10-27. Build in progress; see §1.1.** |
| Date | 2026-10-27; post-build and palette correction 2026-10-28 |
| Scope | Current V2 web, admin, design tokens and UI-facing API contracts; V1 used only as a reference |
| Not in scope | V1 code changes, backend changes, deployment changes, mobile launch |
| Companion documents | `docs/v2-ui/PARITY.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/DESIGN-DIRECTION.md`, `docs/design/ui-ux-framework.md` |

> This is the Phase 0 baseline. It records what existed before the redesign, what
> was broken or missing, what V1 actually does, and which documents were stale.
> The parity decisions are in `PARITY.md`; the route contract is in `ROUTE-MAP.md`;
> the visual direction is in `DESIGN-DIRECTION.md`.

## 1.1 Post-build status (2026-10-27)

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
  separate routes. Legal copy is an explicit draft pending counsel.
- **Auth:** Login, Signup, Verify email and Reset password use the shared auth
  layout. Signup links to the draft legal pages.
- **Student app:** The grouped app shell, mobile navigation, theme toggle,
  notifications, applications, CBT history, course detail and split settings
  routes exist. Home, Academia, Materials, Ask, CBT, Skills, My learning, Lesson,
  Practice, Verification, Assessment sitting, Attempt review, Practical task,
  Transcript, Opportunities, Applications, Work, Earnings, Talent, Campus,
  Notifications, Settings and Onboarding use the shared primitives and explicit
  states.
- **Admin:** The grouped shell, Overview, Waitlist, Campus, Audit, Imports, Users,
  Opportunities, Projects, Review, Money, Content, Platform, Security and a real
  404 exist. Overview reads live queues; Campus is write-only because the read
  endpoint is missing.
- **Still open:** The older admin screens (Opportunities, Projects, Review,
  Money, Content, Platform) still carry legacy markup. Course/topic detail, CBT
  review, the student cohort-invite list, admin campus read and the signed-in
  change-password endpoint are API dependencies. Consent history, push-device
  registration and the matches view still have no UI. `Logo`, `ArrowLink` and
  `Spinner` are unused exports; the old `Layout.tsx` has been removed. Images
  named in `IMAGE-PROMPTS.md` are not created yet.

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
| No consent history or re-consent UI | `GET/POST /me/consents` and `POST /auth/consent` exist but are unused | A terms-version change cannot be accepted in-product; legal evidence is incomplete. |
| No push-device registration | Settings toggles `notify_push` but never calls `/me/push-devices` | The toggle claims push is on when no device exists. |
| No cohort invite response | `POST /work/cohorts/{id}/respond` exists; no web UI | Admin can invite; the student cannot accept or decline. |
| No “my applications” | `GET /opportunities/applications` exists; no screen | Students cannot see what they applied to or its status. |
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

### 5.2 Admin gaps

| Gap | Evidence | Impact |
|---|---|---|
| No waitlist screen | `GET /ops/waitlist` exists | Ops cannot see or act on students waiting for an uncovered university. |
| No campus publishing screen | `POST /ops/campus` exists | Campus content cannot be managed from the admin app. |
| Applications are read-only | `POST /opportunities/applications/{id}/status` exists; UI has no action | Ops cannot move an application through its lifecycle. |
| Payout items are read-only | `POST /money/payout-items/{id}/fail` exists; UI has no action | A failed payout item cannot be resolved in the tool. |
| No admin 404 | Unknown hash renders Audit | A typo silently shows the wrong screen. |
| No skeletons | All loading is plain text | Dense tables flash and jump. |
| No bulk actions | Review, money and content are one-row at a time | Ops work does not scale. |
| No global error boundary | Same as web | A render error blanks the admin app. |
| No newsletter/announcement admin | No feature exists | Only relevant if those features are approved. |

### 5.3 Admin verdict

Admin is the strongest part of V2 functionally and the weakest part visually. It
has the right screens for the current API, but it needs the same design system as
the student app, at a denser rhythm, plus the four missing operational actions.

---

## 6. API capabilities with no UI, and UI with no API

### 6.1 API-only (highest impact)

| Endpoint | Missing UI |
|---|---|
| `POST /auth/consent`, `GET/POST /me/consents` | Re-consent and consent history |
| `GET/POST/DELETE /me/push-devices` | Device registration and removal |
| `POST /work/cohorts/{id}/respond` | Accept/decline a cohort invite |
| `GET /opportunities/applications` | My applications |
| `GET /opportunities/matches` | Matches |
| `GET /platform/me/eligibility` | Eligibility/readiness |
| `GET /ops/waitlist` | Admin waitlist |
| `POST /ops/campus` | Admin campus publishing |
| `POST /opportunities/applications/{id}/status` | Admin application status |
| `POST /money/payout-items/{id}/fail` | Admin payout-item failure |
| `POST /auth/google` | Google sign-in button (deferred) |
| `POST /work/submissions/sync` | Offline submission queue (deferred) |
| `GET /academia/cbt/practice-next` | Adaptive practice (deferred) |
| `GET /talent/me/transcript` | Duplicate of `/verification/transcript` |

### 6.2 UI without a real API

No screen calls a missing endpoint. Two UI claims are not backed:

- **Signup terms acceptance** sends `accept_terms: true` but links to no document
  and records no consent version (`Signup.tsx:81-84`, `session.tsx:78`).
- **Push preference** toggles a profile flag but registers no device
  (`Settings.tsx:255-258`).

### 6.3 API-only verdict

V2 is ahead of its UI in identity consent, notifications, matching, eligibility,
cohorts and ops. These are not speculative endpoints; they are built and tested.
The redesign should expose the ones that complete the student and ops journeys,
not invent new backend work first.

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

### 7.4 Performance and SEO

- First-load budget exists and passes (58.7 KB JS / 1.4 KB CSS in the last
  recorded build).
- No analytics, Sentry or other telemetry.
- No per-route meta; SPA has one static title.
- Sitemap is minimal; public marketing/legal pages would need to be added.

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

### 10.1 Launch blockers (must fix before a public launch)

1. **Legal pages and signup links.** No `/privacy`, `/terms`, no contributor
   terms page; signup accepts terms that do not exist.
2. **Consent capture/re-consent.** `POST /auth/consent` and `/me/consents` exist
   but are unused; a terms version change cannot be recorded.
3. **Password change.** No signed-in password rotation.
4. **404 and error boundary.** Unknown routes redirect home; a render error
   blanks the app.
5. **Notification centre.** Notifications are buried in Settings; no unread
   triage.
6. **Push device registration or an honest toggle.** The current toggle is a
   false promise.
7. **Cohort invite response.** Managed work is one-sided without it.
8. **Admin waitlist and campus.** API exists; ops has no screen.
9. **Application status and payout-item failure.** API exists; ops cannot act.
10. **Public support path.** No contact page; V1's support email is the only
    path and it is not in V2.

### 10.2 Strongly recommended for parity/quality

- About, Features, How it works, FAQ, Contact.
- CBT history and course/topic pages, or an explicit decision to replace them.
- Student material upload/analysis, or an explicit decision to drop it.
- “My applications” and “Matches.”
- Eligibility/readiness.
- Analytics and error tracking (not UI, but needed to run a launch).

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
3. **Support contact.** Real support email, response expectation and any social
   links. V1's `support@localhost` and `example.com` links are not usable.
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
9. **Course/topic and CBT history.** Restore V1's course hub/history, or accept
   the V2 dashboard + results as the replacement.
10. **Student uploads/analysis.** Restore V1's PDF→notes→test, or state that V2's
    curated materials + Ask + CBT is the deliberate replacement.

---

## 13. Verification at audit time

| Check | Result |
|---|---|
| API tests | 332 passed, 1 skipped (333 collected; 10m 42s) |
| Web tests | 53 passed (10 files) |
| Admin tests | 1 passed (1 file) |
| Typecheck/lint/build | Not re-run in this audit; run before UI work |
| Local V2 setup | Documented in `RUN-LOCALLY.md`; zero-config SQLite path exists |
| Admin 2FA | Login works; first-login enrolment is required and still needs a full end-to-end pass |
| V1 reference | Read-only; no V1 files changed |

The audit did not change code. The only changes are documentation and the
deletions listed in §11 once confirmed.

---

## 14. Bottom line

V2 is **functionally broad and visually unfinished**. The public surface is a
stub, the design system is a seed, and several built API capabilities are not
reachable. The highest-value sequence is:

1. Approve the route map and design direction.
2. Build tokens and primitives once.
3. Build the public surface and auth.
4. Build the app shell and the missing student screens.
5. Build the missing admin actions.
6. Add utility screens, legal/consent, notifications and password change.
7. Treat the platform banner and newsletter as separate, explicitly approved
   features, not as parity items.
