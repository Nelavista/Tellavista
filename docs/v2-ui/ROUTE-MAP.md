# V2 route map — Gate 1

| Field | Value |
|---|---|
| Status | **Implemented 2026-11-01; V1 delta audited 2026-11-04. See §1.1 for post-build state and §1.2 for routes V1 added after the map.** |
| Gate | Gate 1 — route map |
| Date | 2026-10-27; post-build status 2026-11-01; V1 delta 2026-11-04 |
| Scope | Public, auth, student app, admin and utility routes for the V2 web launch |
| Companion documents | `docs/v2-ui/AUDIT.md`, `docs/v2-ui/PARITY.md`, `docs/v2-ui/DESIGN-DIRECTION.md`, `docs/v2-ui/IMAGE-PROMPTS.md` |

> V2 uses separate routed pages. It does not repeat V1's one long landing page
> with `#section` anchors. Every route has one job and one dominant anchor. The
> route map is the contract between the design and the API; if a screen has no
> API, it is marked as a dependency, not invented.

## 1.1 Post-build status (2026-11-01)

Every route below has a real API or real static content. The former dependency
states are closed:

- **Built:** all public/auth routes, the student shell and routes, the split
  settings routes, notifications, applications, CBT history, course and topic
  detail, campus, transcript, talent share, admin shell, Overview, Waitlist,
  Campus, Audit, Imports, Users, Opportunities, Projects, Review, Money, Content,
  Platform, Security, public 404, admin 404, error boundary and offline.
- **Closed API gaps:** course/topic detail (`GET /academia/courses/{id}`,
  `GET /academia/topics/{id}`), CBT attempt history with reviewed answers
  (`GET /academia/cbt/history`), the student cohort-invite list
  (`GET /work/invites`), admin campus read (`GET /ops/campus`) and signed-in
  password change (`POST /auth/password/change`).
- **Deferred:** Google SSO, offline submission sync, newsletter and platform
  announcement banner.
- **Admin Campus:** publishes through `POST /ops/campus` and reads the live set
  back through `GET /ops/campus`, including hidden rows with their state shown.
- **Route metadata:** public and auth routes set title, description, canonical,
  robots and social metadata; signed-in shells set the document title and move
  focus to `main` on route change.

### 1.2 V1 routes added after this map (2026-11-04)

V1 `main` added these routes. The qualitative `/impact` route is now in V2; the
language routes remain outside V2 scope until the product decision in
`PARITY.md` §1.2 is taken:

| V1 route | V1 screen / job | V2 state | Notes |
|---|---|---|---|
| `/impact` | Public impact page; current product outcomes and verified metrics when available | **Implemented qualitatively** | No reach figures, testimonials or partner claims are published until verified against a current source and approved. |
| `/skills/african-languages` | African Languages Lab hub; 9 categories, 94 skills, language/level filters, tracks, language profile summary | **Missing** | The ALL catalogue is seeded in V2; add the focused hub and filters over the existing skill catalog. |
| `/skills/languages` | Own language profile; add/update self-reported language, dialect, proficiency and capabilities; academic background | **Missing** | Requires `StudentLanguage`-equivalent data and a verified-by-skill derivation. |
| `/skills/languages/:id/delete` | POST action to remove a language from the profile | **Missing** | Action on the same route family; confirm before delete. |
| Existing `/skills/:skillSlug` challenge route | Structured, auto-scored transcription/translation/labeling/recording tasks; assessment gate and pass mark | **Partial** | V2's existing practice/verification routes can host the UI, but the task spec, deterministic scoring and assessment gate are not implemented. |

Do not add these rows to the “built” table until the code exists. If the product
decides to launch V2 without ALL, record that decision in `PARITY.md` and keep the
routes out rather than shipping links to empty screens.

---

## 1. Principles

1. **One route, one job.** A route may have sections, but it must not try to be a
   second home page.
2. **Public routes are static-first.** They do not block on API calls.
3. **Signed-in routes are guarded.** Anonymous users go to `/login` with a return
   path; authenticated users do not see auth screens.
4. **Deep links are stable.** A student can bookmark a material, lesson,
   assessment, assignment, opportunity, share link or admin record.
5. **Unknown paths are not silently redirected.** A 404 is a real screen with a
   way back.
6. **Feature-off is a state, not a 404.** A route whose API returns
   `not_found` because its flag is off says “not switched on here”, not “page not
   found”.
7. **No route is added for a feature without a real API or a real static page.**
8. **Admin uses hash routes.** Keep the existing `#/section` protocol; do not add
   React Router to admin without a concrete need.

---

## 2. Public routes

| Route | Screen | Job | Dominant anchor | Primary content | Data | States | Auth |
|---|---|---|---|---|---|---|---|
| `/` | Home | Explain the promise and start signup | **Create your account** | Hero, proof chain, four-step journey, three capability rows, proof/verification section, FAQ preview, final CTA | Static; optional public platform config | Static; no API blocking | Public |
| `/features` | Features | Show what the product actually does | **Create your account** | Academia, Skills, Verification, Opportunities, Work, Earnings, Talent — as rows with real product artifacts | Static | Static | Public |
| `/how-it-works` | How it works | Explain Learn → Prove → Work → Earn | **Create your account** | Four-step chain, eligibility/verification explanation, payout explanation, what Nelavista does not claim | Static | Static | Public |
| `/pricing` | Pricing | Explain the commercial model without inventing amounts | **Create your account / Talk to us** | Student launch position, employer scoped quote, university pilot agreement, what a quote covers, what is not charged | Static | Static | Public |
| `/about` | About | Explain why Nelavista exists | **Create your account** | Mission, operating principles, editorial working-record illustration, what the product refuses to fake | Static | Static | Public |
| `/impact` | Impact | Explain current product outcomes without unsupported claims | **See how it works** | Qualitative outcomes, evidence standards and a clear statement that numeric claims require verification | Static | Static | Public |
| `/contact` | Contact | Give a real support path | **Email support** | Support email, response expectation, topics (account, verification, payouts, employers), FAQ link | Static | Static | Public |
| `/faq` | FAQ | Answer the obvious objections | **Create your account** | Is it free? How verification works, how payouts work, data/privacy, eligibility, what happens if a university is missing | Static | Static | Public |
| `/legal/privacy` | Privacy | Explain data collection and rights | **Contact support** | Plain-language privacy policy, effective date, data list, retention, deletion, third parties, contact | Static | Static | Public |
| `/legal/terms` | Terms | Set the rules of use | **Contact support** | Account, academic content, verification, opportunities/work, payments, acceptable use, termination, contact | Static | Static | Public |
| `/legal/contributor-terms` | Contributor terms | Explain paid-work terms before eligibility | **Back to opportunities** | Contributor licence, quality/payment terms, version, contact | `GET /platform/config` (optional) | Loading/error fallback | Public |
| `/login` | Login | Sign in | **Sign in** | Email, password, show password, forgot link, 2FA step | `POST /auth/login`, `POST /auth/2fa/verify` | Idle, submitting, error, 2FA | Public only |
| `/signup` | Sign up | Create an account | **Create account** | Name, email, username, password, terms links, consent | `POST /auth/signup` | Idle, validating, submitting, error, success | Public only |
| `/auth/verify` | Verify email | Consume the email token | **Continue to your home** | Success, expired, invalid, resend | `POST /auth/email/verify`, resend | Loading, success, expired, error | Public |
| `/auth/reset` | Reset password | Request or set a new password | **Send the reset link / Set the new password** | Request state and token state on one route | `POST /auth/password/reset-request`, `/reset` | Idle, submitting, success, error, invalid token | Public |
| `/share/:token` | Shared profile | Show a student's scoped proof | **What this proves** | Verified skills, academic context, quality, delivered work, availability | `GET /talent/share/{token}` | Loading, expired/revoked, error | Public by token |

### Deferred public routes

| Route | Why not now |
|---|---|
| `/for-employers` | V2 has no employer self-service. Use `/contact` with an employer topic until the product exists. |
| `/blog` | No content plan or authoring system. |
| `/newsletter` | No consent/unsubscribe backend. See `AUDIT.md` §9. |
| `/status` | No status-page integration. Use the platform banner for operational notices if approved. |

---

## 3. Auth and account routes

| Route | Screen | Job | Anchor | Notes |
|---|---|---|---|---|
| `/onboarding` | Onboarding | Choose one of four spaces, then collect only the context that space reads; waitlist if missing | **The next incomplete step** | Guarded. Academia uses university, faculty, department, level and courses. Campus uses the university only through `PUT /onboarding/university`. Skills and Opportunities finish at the path choice. |
| `/settings` | Settings — profile and work | Edit identity, bio, location, timezone, visibility, languages, availability | **Save changes** | Guarded. |
| `/settings/security` | Settings — security | Change password, view 2FA, sessions/devices | **Change password** | Uses `POST /auth/password/change`; the response replaces the current access token and revokes other sessions. |
| `/settings/notifications` | Settings - notifications | Email preference, honest push availability, registered device list/removal, notification list link | **Save notification settings** | New. Uses `/me/push-devices`; link to `/notifications`. The web app does not register a browser device. |
| `/settings/data` | Settings - data and consent | Export, consent history, delete account | **Download my data / Delete account** | New. Uses `/me/export`, `/me/consents`, `DELETE /auth/account`; `POST /auth/consent` is a re-consent dependency, not wired. |

Why split Settings: the current one-page Settings mixes profile, work preferences,
notifications, data and deletion. Splitting gives each task one anchor, keeps deep
links stable and makes security/data easy to find.

---

## 4. Student app routes

### 4.1 Home and notifications

| Route | Screen | Job | Anchor | Data | States |
|---|---|---|---|---|---|
| `/home` | Home | Answer “what should I do next?” | **The next action** | `GET /onboarding/state`, `GET /me`, notifications summary | Skeleton, empty, error, feature-off |
| `/notifications` | Notifications | Triage everything that changed | **Unread items** | `GET /me/notifications`, `POST /me/notifications/read` | Skeleton, empty, error, success |

Home composition: space switcher, next action, due/this week table, proof status,
earnings strip, recent notifications. The four spaces are Academia, Skills,
Opportunities and Campus. A returning login opens the saved space; Home keeps the
switcher available. Not a grid of welcome cards.

### 4.2 Academia

| Route | Screen | Job | Anchor | Data | States |
|---|---|---|---|---|---|
| `/academia` | Academia dashboard | Answer the five study questions | **One thing to do next** | `GET /academia/dashboard` | Skeleton, empty, error, feature-off |
| `/academia/materials` | Materials | Find a material | **Search / filter** | `GET /academia/materials`, `/materials/search` | Skeleton, empty, error, feature-off |
| `/academia/materials/:materialId` | Material reader | Read and continue | **Continue reading** | `GET /academia/materials/{id}` | Skeleton, missing, error, feature-off |
| `/academia/ask` | Ask Nelavista | Ask a course-aware question | **The question field** | `GET /academia/ask/sessions`, `POST /academia/ask` | Skeleton, empty, error, feature-off |
| `/academia/cbt` | CBT practice | Practise under exam conditions | **Start / resume a paper** | `POST /academia/cbt/quiz`, `/answer`, `GET /results` | Skeleton, empty, error, feature-off |
| `/academia/cbt/history` | CBT history | Review past practice | **Most recent attempt** | `GET /academia/cbt/history`; filter by course and open the answer, key and explanation | Skeleton, empty, filtered-empty, error, feature-off |
| `/academia/courses/:courseCode` | Course hub | See one course's topics, materials and practice | **Next topic** | `GET /onboarding/state` for the code-to-id map, then `GET /academia/courses/{id}` | Skeleton, missing, error, feature-off |
| `/academia/topics/:topicId` | Topic detail | Understand one topic and its practice record | **Practise this course** | `GET /academia/topics/{id}` | Skeleton, missing, error, feature-off |
| `/campus` | Campus dashboard | Read university information and map points | **Relevant campus item** | `GET /me/campus` | Skeleton, empty, error. A Campus-first student can set the university without enrolling in courses. |

The course route links its topic rows to the topic detail route. Both endpoints
scope the read to the signed-in student's active enrolment; an unenrolled course
is refused by the API, not shown as an empty list.

### 4.3 Skills

| Route | Screen | Job | Anchor | Data | States |
|---|---|---|---|---|---|
| `/skills` | Skills catalog | Choose a skill | **Continue / start** | `GET /skills` | Skeleton, empty, error, feature-off |
| `/skills/my-learning` | My learning | Resume across skills | **Most useful next step** | `GET /skills/my-learning` | Skeleton, empty, error, feature-off |
| `/skills/:skillSlug` | Skill detail | Understand the skill and its path | **Start / continue path** | `GET /skills/{slug}` | Skeleton, missing, error, feature-off |
| `/skills/paths/:pathSlug` | Path detail | Follow an ordered path | **Continue current step** | `GET /skills/paths/{slug}` | Skeleton, missing, error, feature-off |
| `/skills/lessons/:lessonSlug` | Lesson reader | Complete a lesson | **Complete lesson** | `GET /skills/lessons/{slug}`, `POST /start`, `/complete` | Skeleton, missing, error, feature-off |
| `/skills/practice/:templateId` | Practice | Do a practice task | **Submit practice** | `GET /skills/tasks/{id}`, `POST /practice` | Skeleton, empty, error, feature-off |

Add search/filter inside `/skills`; no separate `/skills/search` route unless the
API adds server-side search.

**V1 delta (not built):** V1 added `/skills/african-languages` and
`/skills/languages` (plus the delete action) on 2026-11-04. If ALL is ported, add
them to the student route set; the ALL hub should reuse `/skills/:skillSlug`,
`/skills/paths/:pathSlug` and the practice route rather than creating parallel
lesson or task screens. The multi-skill career tracks need a route decision
(`/skills/tracks/:slug`) before the hub can link to them.

### 4.4 Verification and proof

| Route | Screen | Job | Anchor | Data | States |
|---|---|---|---|---|---|
| `/verification` | Verification hub | Understand proof status and what is missing | **Current status / next assessment** | `GET /verification`, `/assessments`, `/practical` | Skeleton, empty, error, feature-off |
| `/verification/assessments/:assessmentSlug` | Assessment sitting | Sit an assessment | **Current question / timer** | `POST /verification/assessments/{slug}/start`, `/attempts/{id}/submit` | Loading, in-progress, submitted, expired, error |
| `/verification/attempts/:attemptId` | Attempt review | Understand the result | **Result / next action** | `GET /verification/attempts/{id}` | Skeleton, missing, error, feature-off |
| `/verification/practical/:taskSlug` | Practical task | Submit practical work | **Submit work** | `GET /verification/practical`, `POST /verification/practical/{slug}` | Skeleton, empty, error, feature-off |
| `/transcript` | Transcript | See the verified record | **The verified record** | `GET /verification/transcript` | Skeleton, empty, error, feature-off |
| `/talent` | Talent | Share proof with an employer | **Share proof** | `GET /talent/me`, `/me/shares`, `POST /me/shares`, revoke | Skeleton, empty, error, feature-off |

Eligibility is shown as a readiness panel on `/verification` and
`/opportunities` using `GET /platform/me/eligibility`; it does not need a separate
route.

### 4.5 Opportunities, work and money

| Route | Screen | Job | Anchor | Data | States |
|---|---|---|---|---|---|
| `/opportunities` | Opportunities | Find work that fits | **Best match with rate and fit** | `GET /opportunities` | Skeleton, empty, error, feature-off |
| `/opportunities/applications` | My applications | Track what I applied to | **Latest application status** | `GET /opportunities/applications` | Skeleton, empty, error |
| `/opportunities/:slug` | Opportunity detail | Decide whether to apply | **Apply / save** | `GET /opportunities/{slug}`, `POST /{slug}/apply` | Skeleton, missing, error, applied, not eligible |
| `/work` | Work | Do and submit assigned work | **Active invitation / assignment / deadline** | `GET /work/invites`, `/work/assignments`, `/submissions`, `/quality` | Skeleton, empty, error, feature-off, invitation success/error |
| `/work/assignments/:assignmentId` | Assignment detail | Complete the brief | **Submit work** | `GET /work/assignments/{id}`, `/messages`, `POST /start`, `/submissions` | Skeleton, missing, error, feature-off |
| `/earnings` | Earnings | Understand money owed and paid | **Available balance** | `GET /money/earnings` | Skeleton, empty, error, feature-off |

Cohort invites belong on `/work`. The page reads `GET /work/invites` and answers
with `POST /work/cohorts/{id}/respond`. Declining is confirmed in a dialog;
accepting re-reads assignments, because the new work is created by the API.

### 4.6 Account and public share

| Route | Screen | Job | Anchor | Notes |
|---|---|---|---|---|
| `/settings` | Profile/work settings | Edit how I work | **Save changes** | See §3 |
| `/settings/security` | Security | Protect my account | **Save security changes** | New |
| `/settings/notifications` | Notifications settings | Choose how I am contacted | **Save notification settings** | New |
| `/settings/data` | Data/consent | Control my data | **Download / delete** | Built; consent history is read-only, re-consent is handled by `ConsentGate` after a version change |
| `/share/:token` | Shared profile | Show scoped proof | **What this proves** | Public; no app chrome |

---

## 5. Admin routes

Keep the hash router. Group the rail by **Operate** and **Configure**.

| Hash | Screen | Job | Anchor | Data | States |
|---|---|---|---|---|---|
| `#/overview` | Overview | See what needs attention now | **Oldest queue / exception** | Existing admin lists; may need a small aggregate API | Skeleton, empty, error |
| `#/audit` | Audit trail | Investigate a change | **Most recent critical event** | `GET /ops/audit-logs` | Skeleton, empty, error |
| `#/imports` | Import runs | Bring V1 data across safely | **Dry-run / apply** | `GET/POST /ops/imports`, `GET /ops/imports/{id}` | Loading, empty, error, report |
| `#/users` | Users | Find and act on an account | **Search result / selected user** | `GET /ops/users?q`, `/ops/users/{id}` | Skeleton, empty, error |
| `#/waitlist` | Waitlist | See demand for uncovered universities | **Waitlist entry** | `GET /ops/waitlist` | Skeleton, empty, error |
| `#/opportunities` | Opportunities | Create and run opportunities | **Opportunity / applications** | `GET /opportunities/admin/all`, `/{slug}/candidates`, `/{slug}/applications`, `POST /opportunities`, `PATCH /{slug}`, `POST /applications/{id}/status` | Skeleton, empty, error |
| `#/work` | Projects & cohorts | Run managed projects | **Project / cohort** | `GET /work/projects`, `/{slug}`, `/cohorts/{id}`, `/replacements`; create/assign/invite/remove | Skeleton, empty, error |
| `#/review` | Review queue | Clear the quality queue | **Oldest pending review** | `GET /work/review-queue`, `/verification/practical/submissions`; reviews, quality standard, override | Skeleton, empty, error |
| `#/money` | Money | Resolve payout and ledger exceptions | **Exception / outstanding total** | Financials, ledger, payout batches, reconciliation; `POST /money/payout-items/{id}/fail` | Skeleton, empty, error |
| `#/content` | Content | Author and publish skills content | **Draft / published item** | `GET /skills`, `/skills/content/*`; create/update | Skeleton, empty, error, validation |
| `#/campus` | Campus | Publish and audit campus locations | **Publish / live campus record** | `GET /ops/campus`, `POST /ops/campus`; the read includes hidden rows and publication state | Skeleton, empty, filtered-empty, error, publish success/error |
| `#/platform` | Platform settings | Set currency, payout, age, terms, curriculum | **Save settings** | `GET/PATCH /platform/settings` | Skeleton, error, saved |
| `#/security` | Security | Manage staff 2FA and security events | **Current risk / required action** | `POST /auth/2fa/disable`, security events | Loading, error, note |
| `#/announcements` | Announcements | Publish a platform notice | **Publish / end** | **Only if approved**; needs backend | Skeleton, empty, error |
| `#/newsletter` | Newsletter | Manage subscribers | **Subscriber list** | **Only if approved**; needs backend | Skeleton, empty, error |

**Admin 404:** unknown hash renders a NotFound screen with a link to
`#/overview`, not Audit.

**Admin overview (built):** `#/overview` is the default. It composes the review
queue, practical submissions, waitlist, imports, projects and recent audit
events from existing list endpoints, with per-row loading/error/retry. Do not
build fake metrics or a silent fallback to Audit.

---

## 6. Utility routes and states

| State | Route / mechanism | Behaviour |
|---|---|---|
| Web 404 | `*` route renders `NotFound` | Keeps the URL, explains the path is not found, links Home, Features, Contact |
| Admin 404 | unknown hash renders `AdminNotFound` | Links `#/overview` and `#/audit` |
| Render error | React error boundary | Shows “Something broke”, a support link, and a reload action; logs the error |
| Offline | PWA shell / `Offline` component | Explains that the shell is available but API data is not cached; retry |
| Feature off | Existing `useApiResource` `off` state | “Not switched on here” with a link back; not a 404 |
| Maintenance | Platform banner (if approved) | A dismissible notice; does not replace the app shell |
| Session expired | Auth guard / HTTP layer | Return to `/login` with the attempted path |
| Empty | Per-screen empty state | Keeps the page structure and gives one next action |
| Error | Per-screen error state | Says what happened, what was preserved, and the next step |

---

## 7. Redirects and aliases

Keep old V1 bookmarks and public links working where the V2 destination is clear.
Do not redirect a missing feature to the home page silently.

| Old path | New path | Reason |
|---|---|---|
| `/privacy-policy` | `/legal/privacy` | V1 public link |
| `/terms-of-service` | `/legal/terms` | V1 public link |
| `/dashboard` | `/academia` | V1 Academia dashboard |
| `/CBT` | `/academia/cbt` | V1 CBT |
| `/profile` | `/settings` | V1 profile |
| `/notifications` | `/notifications` | Same concept; V2 now has a real route |
| `/courses` | `/academia` | V2 has no public course browse yet |
| `/employer/*` | `/contact?topic=employers` | No employer self-service at launch; give a real contact path |
| `/auth/forgot-password` | `/auth/reset` | Alias |
| `/auth/reset-password` | `/auth/reset` | Alias |

**Do not redirect** V1 dead products (community, live, reels, videos) to the home
page. If the URL is hit, show a 404 with a short note that the feature is no
longer part of Nelavista. A silent redirect hides the change.

---

## 8. Navigation model

### Public header

Logo · Features · How it works · About · Log in · **Get started**

- Sticky, solid white, 1px bottom rule.
- No translucent blur.
- Mobile: logo, Get started, menu button; menu is a full-height panel with the
  same links plus legal/contact.
- Theme control: Light/Dark.

### Public footer

- **Platform:** Features, How it works, FAQ
- **Company:** About, Contact
- **Legal:** Privacy, Terms, Contributor terms
- **Account:** Log in, Create account
- **Contact:** real support email
- Social links only if real.
- No giant decorative wordmark.

### Student app shell

Desktop:

- 240px left rail:
  - Home
  - Notifications
  - **Learn:** Academia, Skills, My learning
  - **Prove:** Verification, Transcript
  - **Work:** Opportunities, Work, Earnings
  - **You:** Talent, Campus, Settings
- 64px top bar: page title, search/command, notifications, avatar.
- Content max 1120px; optional 320px inspector on detail screens.

Mobile:

- 56px top bar: page title, notifications, avatar.
- 64px bottom bar: Home, Learn, Work, Proof, You.
- Full-width content; tables scroll inside a labelled region.

### Admin shell

- 220px left rail:
  - **Operate:** Overview, Audit, Imports, Users, Waitlist, Opportunities, Work,
    Review, Money
  - **Configure:** Content, Campus, Platform, Security
  - Announcements/Newsletter only if approved.
- 56px top bar: environment badge, command search, user menu.
- Dense tables; detail drawer; audit footer.

### Auth shell

- Split 5/7: form on white, “what happens next” panel on navy.
- Mobile: form first, panel collapses to a short note.
- Minimal header: logo and “Back to home”.

---

## 9. API reads and actions

### Built reads and actions

| Screen | Endpoint |
|---|---|
| `/notifications` | `GET /me/notifications`, `POST /me/notifications/read` |
| `/opportunities/applications` | `GET /opportunities/applications` |
| Eligibility panel | `GET /platform/me/eligibility` |
| `/work` invitations | `GET /work/invites`, `POST /work/cohorts/{id}/respond` |
| `/settings/notifications` | `GET/POST/DELETE /me/push-devices` |
| `/settings/security` | `POST /auth/password/change`, `POST /auth/password/reset-request` |
| `/settings/data` | `GET /me/consents`; `ConsentGate` handles re-consent |
| `/academia/cbt/history` | `GET /academia/cbt/history?course_id=&limit=` |
| `/academia/courses/:courseCode` | `/onboarding/state`, `GET /academia/courses/{id}` |
| `/academia/topics/:topicId` | `GET /academia/topics/{id}` |
| `/onboarding` path step | `POST /me/path` with `academia`, `skills`, `opportunities` or `campus` |
| `/onboarding` campus step | `PUT /onboarding/university`, then `POST /me/onboarding/complete` |
| Admin `#/waitlist` | `GET /ops/waitlist` |
| Admin `#/campus` | `GET /ops/campus`, `POST /ops/campus` |
| Admin application status | `POST /opportunities/applications/{id}/status` |
| Admin payout-item failure | `POST /money/payout-items/{id}/fail` |

### Deliberately deferred

| Screen | Missing API | Status |
|---|---|---|
| Admin `#/overview` | Optional aggregate endpoint; otherwise compose from existing lists | Built by composing existing lists |
| `#/announcements` | Announcement model, public read, admin CRUD, audit | Deferred |
| `#/newsletter` | Subscriber model, consent, double opt-in, unsubscribe, export, email provider | Deferred |
| `/pricing` | No approved pricing amounts | Built as commercial positions; replace with approved amounts when supplied |

### No UI without API

Do not build a screen that calls an endpoint that does not exist. If a screen is
needed before the API, use an explicit “not available yet” state, not fake data.

---

## 10. Screen count and build order

This is the Gate 1 plan. The build has completed it except for the deferred items
in §1.1.

| Surface | Routes in this map | Build order |
|---|---|---|
| Public | 15 | After tokens/primitives |
| Auth/account | 5 | After public shell |
| Student app | 28 | After auth |
| Admin | 14 | After student app or in parallel once primitives exist |
| Utility | 4 states + redirects | With the shells |

Total: **~62 routes**, of which 19 are new or split from existing screens. This is
a full product surface, not a landing-page refresh. The count does **not** include
the remaining 2026-11-04 V1 language delta (`/skills/african-languages`,
`/skills/languages` and the language delete action); add those only if the product
decision in `PARITY.md` §1.2 approves them.

Build order after Gate 2 approval:

1. Tokens, theme bridge, primitives.
2. Public shell, header/footer, Home.
3. Features, How it works, Pricing, About, Contact, FAQ, Legal.
4. Auth and onboarding.
5. Student shell, Home, Notifications.
6. Academia and Skills.
7. Verification, Opportunities, Work, Earnings.
8. Talent, Transcript, Settings subroutes, Campus.
9. Admin shell, Overview, existing screens, missing actions.
10. Utility screens, 404, error boundary, offline, announcement if approved.

---

## 11. Gate 1 decisions requested

Approved 2026-10-27:

1. **Public route set:** Home, Features, How it works, Pricing, About, Contact,
   FAQ, Privacy, Terms, Contributor terms. Employer pricing is handled by the
   scoped-quote path on `/pricing` and `/contact`; no separate employer route.
2. **Auth/account split:** `/settings`, `/settings/security`,
   `/settings/notifications`, `/settings/data`.
3. **New student routes:** `/notifications`, `/opportunities/applications`,
   `/academia/cbt/history`, `/academia/courses/:courseCode`,
   `/academia/topics/:topicId`.
4. **New admin routes:** `#/overview`, `#/waitlist`, `#/campus`; application
   status and payout-item failure as actions, not new routes.
5. **Utility behaviour:** real 404s, error boundary, offline state, no silent
   redirects for dead V1 products.
6. **Redirects:** the table in §7.
7. **Deferred features:** pricing, employer self-service, newsletter and the
   platform announcement banner are post-launch. Do not build them now.
8. **API closure:** CBT history, course/topic detail, cohort invitations, admin
   campus read and password change are implemented and wired; the UI no longer
   uses dependency placeholders for them.
9. **Parity decision:** course/topic and CBT history are in scope. Student
   material upload/analysis is deferred; the replacement is curated materials,
   Ask, CBT and the transcript evidence trail.
10. **Post-map V1 delta (2026-11-04):** `/impact`, the ALL hub, the language
    profile and structured scored tasks are new V1 scope. They are not added to
    the V2 route contract until the product decision is taken; if approved, add
    them here first and then build them.

Gate 2 (design direction) was approved on the same date. The first build change
is the token and primitive foundation, not a page.
