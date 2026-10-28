# V1 → V2 parity

| Field | Value |
|---|---|
| Status | **Implemented 2026-10-28.** Course/topic and CBT history are in scope; material upload/analysis is deferred with a stated replacement. Remaining gaps are API/content dependencies. |
| Date | 2026-10-27; post-build status and palette correction 2026-10-28 |
| Method | V2 code and API contracts are the source of truth. V1 is read-only reference. |
| Legend | **Stronger** = V2 does more or does it better. **Parity** = capability exists in both. **Gap** = V2 needs work to match. **Dropped** = V2 intentionally removes it; a reason is required. **New** = not in V1. **Decide** = product decision needed. |
| Companion documents | `docs/v2-ui/AUDIT.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/DESIGN-DIRECTION.md`, `docs/v2-ui/IMAGE-PROMPTS.md` |

> The rule: every V1 screen, flow, capability and piece of information must exist
> in V2, be replaced by something stronger, or be explicitly dropped with a
> reason. “It is not in the PRD” is not enough on its own; say what the student
> gains instead.

> **Read this first.** The tables below preserve the Gate 1 decision record and
> mark post-build status where it has changed. Where a row still describes the
> pre-build state, §1.1 and the post-build verdicts are authoritative.

---

## 1. Summary

| Area | V2 state (post-build) | Verdict |
|---|---|---|
| Public marketing | Separate routed pages: Landing, Features, How it works, About, Contact, FAQ, 404, Offline; per-page metadata and sitemap | **Parity/stronger**; legal review pending |
| Auth | Login, signup, verify, reset; shared auth layout; draft legal links; signup records the terms version | **Parity**; re-consent UI pending |
| Student journey | Home, Academia, Materials, Ask, CBT, Skills, My learning, Lesson, Practice, Verification, Assessment, Attempt review, Practical task, Transcript, Opportunities, Applications, Work, Earnings, Talent, Campus, Notifications, Settings, Onboarding | **Mostly parity**; course/topic and CBT detail endpoints, cohort invite list, password change |
| Skills | Verification/evidence journey and practice | **Stronger** in verification/evidence; search and project workspaces remain later work |
| Academia | Dashboard, materials, Ask, CBT, course route, CBT history | **Parity/stronger**; full topic detail and uploads/analysis deferred |
| Opportunities/work/money | Managed model, eligibility blockers, applications, ledger, payout batches | **Stronger** than V1's status-only marketplace |
| Talent/transcript | Evidence-only, scoped revocable shares, consent history | **Stronger** privacy; **parity** on proof |
| Employer | No self-service | **Dropped by design** at launch; managed work instead |
| Admin | Overview, Waitlist, Campus, Audit, Imports, Users, Opportunities, Projects, Review, Money, Content, Platform, Security, 404 | **Stronger** in audit/money/quality; campus read and bulk actions remain gaps |
| Utility | Real 404, error boundary, offline screen, route focus/title | **Parity/stronger** |
| Theme | Light/dark with Nelavista blue and white | **Parity**; both surfaces implemented, manual visual pass recommended |
| Public legal/contact | Draft privacy, terms, contributor terms; real support email | **Parity**; counsel review is a launch blocker |

**Bottom line:** V2 now covers the V1 journey and exceeds it in verification,
managed work, money controls and admin audit. The remaining gaps are not missing
screens: they are API detail (course/topic, CBT review, cohort invites, campus
read, password change), legal review, and real business content/imagery.

### 1.1 What is still limited

- **API dependencies:** signed-in password change; full course/topic detail;
  CBT history/review detail; student cohort-invite list; admin campus read.
- **Content:** pricing, counsel-reviewed legal copy, real social links, real
  metrics/testimonials, photography, employer positioning, and the material
  upload/analysis replacement copy.
- **Verification:** admin 2FA enrolment and `dev-local.ps1` end-to-end; the V2
  domain switch; a manual light/dark visual pass.
- **Images:** the manifest is ready; the files are not.
- **Brand video:** the MP4 is not a transparent loader; placement is undecided.

---

## 2. Public surface parity (post-build)

| V1 | V2 (post-build) | Verdict | Action |
|---|---|---|---|
| `/` landing with hero, pillars, skills, journey, academics, opportunities, campus, founder, CTA | `/` routed landing with a working-record argument | **Parity/stronger** | Keep separate routes; do not copy V1's long page |
| No standalone Features page; landing `/#platform` | `/features` with capability rows | **Stronger** | Keep |
| No standalone How it works; landing journey strip | `/how-it-works` with the Learn → Prove → Work → Earn chain | **Stronger** | Keep |
| `/about` one-paragraph stub | `/about` with mission, principles and honest scope | **Parity/stronger** | Add real team/campus imagery only when supplied |
| No contact page; footer mailto | `/contact` with `support@nelavista.com` and topics | **Stronger** | Add response expectation when supplied |
| No FAQ | `/faq` with eligibility, verification, payouts, privacy | **Stronger** | Keep |
| No pricing page; “free for students” only | No pricing model; no `/pricing` | **Decide** | Do not build until the business defines a price |
| `/privacy-policy` | `/legal/privacy` draft for V2 data flows | **Parity/partial** | Counsel review required |
| `/terms-of-service` | `/legal/terms` draft for V2 | **Parity/partial** | Counsel review required |
| Contributor terms only in platform settings | `/legal/contributor-terms` public draft | **Parity/stronger** | Counsel review required |
| No newsletter | None | **New** | Deferred; needs consent/unsubscribe |
| No public announcement banner | None | **New** | Deferred; not parity |
| No blog | None | **Not required** | Do not add |
| Employer signup/dashboard/discover | None | **Dropped by design** | Managed work through ops; employer self-service later |
| Footer social links (placeholder `example.com`) | No placeholder links; real support email only | **Parity/stronger** | Add real social links only when supplied |
| Theme toggle | Light/dark on brand blue/white | **Parity** | Manual visual pass recommended |
| PWA manifest, no offline | Real PWA shell and offline route | **Stronger** | Keep; add update/install UX |
| No V1 robots/sitemap/OG | Per-page title/description/canonical/OG; expanded sitemap | **Stronger** | Keep route and meta maps in sync |

### Public parity verdict (post-build)

V1's public site is a polished landing page plus thin About/legal pages. V2 now
has the separate marketing routes, the three legal drafts, a real 404 and an
offline screen, plus per-page metadata and a fuller sitemap. The remaining public
blocker is counsel review of the legal drafts, not missing screens.

---

## 3. Auth parity

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Login with username or email + password | Login with email + password; staff 2FA | **Parity** | Redesign; keep 2FA challenge |
| Google sign-in when configured | `POST /auth/google` exists, no button | **Gap** | Add only if the flow and consent are designed; otherwise defer |
| Signup username/email/password | Signup name/email/username/password; links to legal drafts; records terms version | **Parity/stronger** | Keep; add re-consent for a version change |
| Email verification result + resend | `/auth/verify` + resend | **Parity** | Redesign; handle expired/invalid states |
| Forgot password | `/auth/reset` request state | **Parity** | Redesign; keep anti-enumeration copy |
| Reset password | `/auth/reset` token state | **Parity** | Redesign; keep single-use token behavior |
| Signup accepted terms with no links | Links to the legal drafts; signup records `terms_of_service` at `TERMS_VERSION`; consent history is visible | **Parity/partial** | Add re-consent UI for a version change |
| No change-password in V1? | V1 has `/account/change-password` | **Gap** | Add the signed-in password-change API, then the form |
| Auth pages prevent zoom (`maximum-scale=1.0`) | V2 viewport allows zoom | **Stronger** | Keep |

### Auth parity verdict (post-build)

V2 auth is functionally close to V1 and stronger on 2FA. Login, signup, verify
and reset are redesigned, and signup links to the legal drafts. The remaining
blockers are re-consent when the terms version changes and a signed-in
password-change endpoint, not the login form.

---

## 4. Student app parity

### 4.1 Entry, identity and account

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Landing redirects signed-in users to saved path | `/` redirects signed-in users to `/home` | **Parity** | Keep |
| `/choose-path` two-product fork | Home path switch (`academia`/`skills`/`both`) | **Parity/stronger** | Make it a first-class choice, not a select buried in Home |
| Academia onboarding wizard | `/onboarding` wizard | **Parity** | Redesign as a clear stepper; keep waitlist |
| Skills onboarding modal | No separate Skills onboarding | **Gap/decide** | Add a first-run Skills preference step, or fold into `/onboarding` |
| Profile + LASU curriculum browser | Settings profile + academic context | **Partial** | Keep academic context; decide whether to restore a curriculum reference |
| Settings (AI prefs, study prefs, notifications, theme, export, delete, password) | Split Settings: profile, security, notifications, data; consent history and push devices; theme in the shell | **Parity/stronger** | Password change is the remaining API dependency |
| Separate Academia and Skills notifications | `/notifications` plus a recent list in Settings | **Parity/stronger** | Built |
| No global command/search | None | **New opportunity** | Add app search/command menu if budget allows |

### 4.2 Academia

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Dashboard: performance, AI insights, upcoming exams, continue studying, courses, recent materials | Dashboard: five questions, next action, courses, materials, CBT | **Parity/stronger** | Redesign with a next-action anchor and tables |
| Materials browse by taxonomy | Materials list + search + reader | **Parity/stronger** | Add course filter and topic grouping |
| Upload material + my uploads + moderation | No student upload; curated materials only | **Dropped/decide** | Decide: restore uploads or state curated materials + Ask as replacement |
| Course detail hub | `/academia/courses/:courseCode` using onboarding state and materials | **Parity/partial** | Full topic detail still needs an API contract |
| Topic detail (explanation, videos, materials, AI) | No topic route | **Gap** | Add topic view or fold topics into the course hub when the API supports it |
| Browse courses + academic search | Materials search and course filter | **Partial** | Add course/skill search/filter; consider a unified search |
| Threaded AI tutor with streaming | Ask Nelavista sessions | **Parity/stronger** | Keep threads, citations, honest decline |
| CBT practice with timer and server grading | CBT quiz/answer/results | **Parity/stronger** | Keep integrity; add question palette |
| CBT history + attempt review + AI explain | `/academia/cbt/history` built as an explicit dependency state; results exist | **Partial** | Attempt-review detail needs an API contract |
| Analyze Materials: PDF → notes → test | None | **Dropped/decide** | Deferred with replacement: curated materials + Ask + CBT + transcript evidence trail |
| Campus map + locations | Campus read-only page | **Partial** | Add map/location detail if data exists; otherwise keep a clear utility |
| Notifications | `/notifications` and recent list in Settings | **Parity/stronger** | Built |

### 4.3 Skills

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Skills home with pipeline, stats, continue learning, earnings | Skills catalog + My Learning + Home | **Partial** | Add a “next step” anchor to Skills; avoid stat-card clutter |
| Catalog with categories | Skills catalog | **Parity** | Add search/filter and time/difficulty metadata if available |
| Skills search | None | **Gap** | Add search/filter to `/skills` |
| Learning paths/tracks | Paths | **Parity** | Keep ordered steps; show progress |
| Skill detail | Skill detail | **Parity** | Keep |
| Course view | Path/lesson routes | **Partial** | Add course/module grouping if the API supports it |
| Lesson with multiple explanations, quiz, complete | Lesson reader + complete | **Parity** | Keep; make completion honest (not verification) |
| 30-day class, GPA, rank | No student class | **Dropped by design** | Managed cohorts replace it; explain the replacement |
| Challenges | Practice tasks | **Parity/stronger** | Keep; show rubric/feedback |
| Competitions | External opportunities | **Replaced** | Treat competitions as opportunities, not a separate product |
| Projects + four typed workspaces + AI mentor | Work assignments/submissions | **Replaced** | Managed work replaces self-directed project workspaces; decide if a portfolio remains |
| Project detail | Assignment detail | **Replaced** | Keep brief, messages, submission, feedback |
| Transcript | Transcript | **Stronger** | Keep evidence links and status |
| Opportunities list + apply | Opportunities with verdict + gaps | **Stronger** | Keep; add my applications |
| Gigs marketplace | Managed work | **Replaced** | No open gig marketplace; explain managed work |
| Earnings status-only | Ledger + earnings | **Stronger** | Keep line items and payout status |
| My Learning | My Learning | **Parity** | Keep |
| Public talent URL | Scoped, expiring share link | **Stronger** | Keep; add share management |
| Global messages | Work-scoped messages | **Partial/intentional** | Keep work-scoped; do not rebuild a social inbox |
| Skills notifications | `/notifications` and a recent list in Settings | **Parity/stronger** | Built |
| Skills profile/privacy | Settings visibility | **Parity** | Keep; explain what employers see |

### 4.4 Opportunities, work, money

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Job-board list + one-click apply | Opportunities with eligibility explanation | **Stronger** | Keep; application tracking and status are built |
| No skill-gap explanation | “Why you qualify / what is missing” | **Stronger** | Keep; make it prominent |
| No application tracking | `/opportunities/applications` | **Stronger** | Built |
| No matches view | Match verdict, reason and next steps on every row | **Stronger** | Built into the list and detail |
| No eligibility view | Platform eligibility panel on opportunity detail | **Stronger** | Built; keep the terms/age blockers visible |
| Work not a V1 student concept | Assignments, submissions, quality | **New/stronger** | Keep |
| Cohort invite response absent | `POST /work/cohorts/{id}/respond` exists; no student invite-list endpoint | **Blocked** | Add the list endpoint, then accept/decline on `/work`; do not fake an invite id |
| Earnings status-only, no gateway | Ledger, payout batches, second approver | **Stronger** | Keep; add payout status detail |
| No quality record | Quality score with counts | **New/stronger** | Keep |
| No transcript for work | Work history in Talent | **New/stronger** | Keep |

### 4.5 Campus

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Campus map with locations, categories, coordinates | Campus page | **Partial** | Keep as a light utility; add map/location detail if data supports it |
| Admin campus management | `#/campus` publishes items through `POST /ops/campus`; write-only with session receipts | **Parity/partial** | Add an ops read endpoint before claiming a published list |

### 4.6 Student app verdict (post-build)

V2 is stronger in verification, matching, managed work, quality, ledger and
talent privacy. The notification centre, applications, eligibility blockers,
consent history, push-device list/removal, CBT history, course route and split
settings are now built. Still open: full course/topic detail, CBT attempt-review
detail, the cohort-invite list endpoint, password change, and skills search.
Those are API or later-scope items, not missing primary screens.

---

## 5. Admin parity

| V1 admin | V2 admin (post-build) | Verdict | Action |
|---|---|---|---|
| Dashboard with counts and newest users | Overview is the default; it composes live queues with per-row states | **Parity/stronger** | Keep; a purpose-built aggregate API is optional |
| Users + activity | Users | **Parity/stronger** | Keep; add activity detail if needed |
| Materials moderation, approve/reject/reindex | No material moderation; imports only | **Gap/decide** | V2 materials are curated; add ops ingestion/moderation if needed |
| Videos moderation | None | **Dropped** | V2 has no video product |
| AI flags | None | **Dropped/decide** | Decide whether Ask needs a flag/review loop |
| Community moderation | None | **Dropped** | V1 community is dead |
| Live rooms | None | **Dropped** | V1 live is dead |
| Employer verification | None | **Dropped by design** | No employer self-service |
| Academia taxonomy/course editor | No academia admin | **Gap/decide** | V2 content is seeded/imported; add taxonomy/course editing if ops needs it |
| Missing videos queue | None | **Dropped** | No video product |
| Skills categories/skills | Content | **Parity/stronger** | Keep |
| Skill editor | Content | **Parity/stronger** | Keep; add preview/versioning |
| Classes/cohorts | Projects & cohorts | **Replaced** | Keep managed cohorts |
| Tracks | Content | **Parity** | Keep |
| Opportunities + applications | Opportunities; application status is editable | **Parity/stronger** | Built |
| Competitions | External opportunities | **Replaced** | Use opportunities |
| Campus map admin | `#/campus` publishes items | **Stronger, write-only** | Read endpoint is a launch dependency; do not fake a published list |
| No audit UI | Audit | **Stronger** | Keep |
| No waitlist screen | `#/waitlist` | **Stronger** | Built |
| No payout item failure action | Money exposes the fail action with a required reason | **Parity/stronger** | Built |
| No platform policy | Platform | **Stronger** | Keep |
| No security/2FA | Security + forced 2FA | **Stronger** | Keep |

### Admin parity verdict (post-build)

V2 admin is stronger than V1 in audit, money, quality, platform policy, security,
overview, waitlist and campus publishing. Application status and payout-item
failure are now exposed. The remaining gaps are the missing campus read endpoint,
bulk actions, a purpose-built aggregate overview, and a material/content-ops
decision. Do not rebuild V1's dead moderation tools.

---

## 6. Utility and system parity

| V1 | V2 (post-build) | Verdict | Action |
|---|---|---|---|
| 404/500/503 pages | Public 404, admin 404, error boundary and offline route | **Parity/stronger** | Keep; add maintenance state if deployment needs it |
| Theme toggle | Light/dark implemented on brand blue/white | **Parity** | Manual visual pass recommended |
| PWA manifest but no offline | Real PWA shell | **Stronger** | Keep; add update/install UX |
| No robots/sitemap | Robots and sitemap cover public pages; private routes disallowed | **Parity/stronger** | Keep in sync with routes |
| No OG/canonical | Per-page title, description, canonical, OG and Twitter metadata | **Stronger** | Keep the route map and meta map in sync |
| No analytics/error tracking | None | **Gap** | Add before launch |
| Support email/social links | `support@nelavista.com`; no placeholder social links | **Parity** | Add real social links only when supplied |
| No admin 404 | Unknown hash renders `AdminNotFound` | **Stronger** | Keep |
| No skip link/aria-current | Skip link, focus-to-main, route titles and current nav state | **Stronger** | Keep |

---

## 7. Dropped by design (with replacement)

These are intentional V2 scope decisions. They are not parity gaps as long as the
replacement is real and the product does not pretend the old feature exists.

| V1 capability | Why V2 drops it | Stronger replacement |
|---|---|---|
| Community groups, chat, events | V1 student front door is retired; V2 has no social product | None; not needed for the core journey. Do not advertise it. |
| Live video rooms | V1 front door is retired; realtime is not in V2 core | None; async work, notifications and campus utility |
| Reels / short video | Not in PRD; V1 page is orphaned | Materials + Ask + CBT |
| Employer self-service | V2 runs managed work through ops first | Managed projects, quality review, ledger and payouts; employer self-service later |
| V1 gig marketplace | No payment rail and no quality gate | Managed work + ledger + quality |
| V1 30-day class/GPA/rank | Hardcoded cohort model; V2 uses managed cohorts | Managed projects/cohorts, quality record, verification |
| Click-to-complete verification | Completion is not proof | Evidence-backed assessments and practical tasks |
| V1 job-board matching | Generic listings | Requirement → gap → eligibility explanation |
| Full campus map | Not in PRD; V2 keeps a light utility | Campus page with location data; no separate map product |
| Global social inbox | Work messaging is the need | Work-scoped assignment messages |
| V1 public talent URL | Privacy risk | Scoped, expiring, revocable share links |

### Decisions still needed

| V1 capability | Question |
|---|---|
| Student material uploads + my uploads | Deferred with an explicit replacement: curated materials, Ask, CBT and the transcript evidence trail. Confirm the replacement copy. |
| PDF → notes → test analysis | Deferred with the same replacement; do not imply uploads work. |
| Course/topic pages | In scope. Course route exists; full topic detail needs an API contract. |
| CBT history/review | In scope. History route exists; attempt-review detail needs an API contract. |
| AI answer flags / AI quality loop | Does Ask need a flag/review queue? |
| Admin material/video moderation | Does V2 need ops ingestion/moderation for materials? |
| LASU curriculum browser | Is academic context enough, or is the curriculum reference needed? |
| Employer self-service | Later product; managed work is the launch replacement. |

---

## 8. Post-build checklist

### Built

- Public: `/features`, `/how-it-works`, `/about`, `/contact`, `/faq`,
  `/legal/privacy`, `/legal/terms`, `/legal/contributor-terms`, real 404,
  offline screen, per-page metadata and sitemap.
- Auth: redesigned login, signup, verify and reset; legal draft links.
- Student: notification centre, my applications, eligibility blockers on
  opportunity detail, honest push-device list/removal, consent history, CBT
  history, course route, split settings, 404/offline, light/dark brand theme.
- Admin: Overview, Waitlist, Campus, Audit, Imports, Users, Opportunities,
  Projects, Review, Money, Content, Platform, Security, admin 404, application
  status action and payout-item failure action.
- Brand: V1 logo/favicon copied into V2, generated PWA/apple icons, WebP boot
  loader and still-mark fallback.

### Still blocked or deferred

- Signed-in password change (API dependency).
- Full course/topic detail (API dependency).
- CBT attempt-review detail (API dependency).
- Student cohort-invite list (API dependency).
- Admin campus read (API dependency).
- Skills search/filter (later scope).
- Material upload/analysis (deferred with replacement copy).
- Google SSO (deferred).
- Offline submission sync (deferred).
- Newsletter and platform announcement banner (post-launch, not parity).
- Analytics/error tracking (before launch).
- Legal review, real business content, photography and the approved image set.

### New, not parity

- Platform announcement banner (backend + admin + public).
- Newsletter subscription (backend + consent + admin + public).

---

## 9. What not to carry from V1

- Hardcoded “2,500+” students or any unverified social proof.
- The hardcoded LASU map/count mismatch.
- Placeholder social links (`example.com`) or `support@localhost`.
- The retired community/live/reels front doors or their admin consoles.
- Employer self-service pages without an employer product.
- Click-to-complete as verification.
- V1 legal text that describes features V2 no longer has.
- V1's long single-page marketing layout, glass cards, gradient blobs and
  decorative motion.
- V1's `maximum-scale=1.0` viewport or any zoom prevention.
- V1's dead PWA claim; V2's PWA is real, keep it honest.

---

## 10. Parity verdict (post-build)

V2 has a **stronger core** than V1: evidence-based verification, managed work,
quality, ledger, scoped talent shares and a real admin audit trail. The perimeter
is now built: public routes, legal drafts, notification centre, applications,
consent history, push-device control and utility screens exist.

What remains is not a missing primary screen. It is API detail (password change,
course/topic, CBT review, cohort invites, campus read), legal review, real
business content, and a small set of later-scope items (skills search, uploads,
Google SSO, offline sync, analytics). The redesign should keep V2's stronger core
and explicitly retire V1's dead or unsafe surfaces.
