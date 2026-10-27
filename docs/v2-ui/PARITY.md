# V1 → V2 parity

| Field | Value |
|---|---|
| Status | **Approved 2026-10-27.** Course/topic and CBT history are in scope; material upload/analysis is deferred with a stated replacement. |
| Date | 2026-10-27 |
| Method | V2 code and API contracts are the source of truth. V1 is read-only reference. |
| Legend | **Stronger** = V2 does more or does it better. **Parity** = capability exists in both. **Gap** = V2 needs work to match. **Dropped** = V2 intentionally removes it; a reason is required. **New** = not in V1. **Decide** = product decision needed. |
| Companion documents | `docs/v2-ui/AUDIT.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/DESIGN-DIRECTION.md` |

> The rule: every V1 screen, flow, capability and piece of information must exist
> in V2, be replaced by something stronger, or be explicitly dropped with a
> reason. “It is not in the PRD” is not enough on its own; say what the student
> gains instead.

---

## 1. Summary

| Area | V2 state | Verdict |
|---|---|---|
| Public marketing | Landing stub only | **Major gap** |
| Auth | Login, signup, verify, reset | **Parity**, needs legal/consent and polish |
| Student journey | Broad | **Mostly parity**, with gaps in notifications, password, CBT history, course/topic, applications, eligibility |
| Skills | Core journey | **Stronger** in verification/evidence; **gap** in search, project workspaces, class/cohort model |
| Academia | Dashboard, materials, Ask, CBT | **Parity/stronger** in materials/Ask; **gap** in course/topic, uploads/analysis, CBT history |
| Opportunities/work/money | Managed model | **Stronger** than V1's status-only marketplace |
| Talent/transcript | Evidence-only, scoped shares | **Stronger** privacy; **parity** on proof |
| Employer | No self-service | **Dropped by design** at launch; managed work instead |
| Admin | Real ops tools | **Stronger** in audit/money/quality; **gaps** in waitlist, campus, applications, payout items, content/material ops |
| Utility | No 404/error boundary | **Gap** |
| Theme | Dark only | **Gap** vs V1 theme toggle; propose Ink + Paper |
| Public legal/contact | None | **Major gap** |

**Bottom line:** V2's product spine is stronger than V1's in the areas V2 chose to
build. Its public surface, utility screens and several student/admin edges are
weaker. The redesign must close those gaps before it can claim “not less than V1.”

---

## 2. Public surface parity

| V1 | V2 today | Verdict | Action |
|---|---|---|---|
| `/` landing with hero, pillars, skills, journey, academics, opportunities, campus, founder, CTA | `/` 36-line landing stub | **Gap** | Build a routed public site; do not copy V1's long-page layout |
| No standalone Features page; landing `/#platform` | None | **Gap** | Add `/features` with rows, not card grids |
| No standalone How it works; landing journey strip | None | **Gap** | Add `/how-it-works` with the Learn → Prove → Work → Earn chain |
| `/about` one-paragraph stub | None | **Gap** | Add `/about` with mission, founder, principles, real photos or none |
| No contact page; footer mailto | None | **Gap** | Add `/contact` with the real support email and response expectation |
| No FAQ | None | **Gap** | Add `/faq` with real objections (free, verified, paid, data, eligibility) |
| No pricing page; “free for students” only | None; no pricing model | **Decide** | Do not build `/pricing` until the business defines a price |
| `/privacy-policy` | None | **Gap** | Add `/legal/privacy`, rewritten for V2 data flows |
| `/terms-of-service` | None | **Gap** | Add `/legal/terms`, rewritten for V2; V1 text is not safe to copy |
| Contributor terms only in platform settings | None public | **Gap** | Add `/legal/contributor-terms` |
| No newsletter | None | **New** | Defer or build as a separate consent/unsubscribe system |
| No public announcement banner | None | **New** | Optional small announcements feature; not parity |
| No blog | None | **Not required** | Do not add |
| Employer signup/dashboard/discover | None | **Dropped by design** | V2 runs managed work through ops; no employer self-service at launch |
| Footer social links (placeholder `example.com`) | None | **Gap** | Use real links or omit; never ship placeholders |
| Theme toggle | Dark only | **Gap** | Add Ink + Paper, or state a stronger replacement |
| PWA manifest, no offline | Real PWA shell | **Stronger** | Keep; fix install/update UX |
| No V1 robots/sitemap/OG | Basic robots/sitemap, title only | **Partial** | Add per-page meta, OG, canonical and full sitemap |

### Public parity verdict

V1's public site is a polished landing page plus thin About/legal pages. V2 has
none of the marketing pages and no legal pages. **V2 cannot launch publicly until
the public surface is built.** The good news: this is a content and design task,
not a new backend.

---

## 3. Auth parity

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Login with username or email + password | Login with email + password; staff 2FA | **Parity** | Redesign; keep 2FA challenge |
| Google sign-in when configured | `POST /auth/google` exists, no button | **Gap** | Add only if the flow and consent are designed; otherwise defer |
| Signup username/email/password | Signup name/email/username/password | **Parity/stronger** | Add terms links and real consent recording |
| Email verification result + resend | `/auth/verify` + resend | **Parity** | Redesign; handle expired/invalid states |
| Forgot password | `/auth/reset` request state | **Parity** | Redesign; keep anti-enumeration copy |
| Reset password | `/auth/reset` token state | **Parity** | Redesign; keep single-use token behavior |
| Signup accepted terms with no links | Same problem | **Gap** | Add links; record document version via `POST /auth/consent` |
| No change-password in V1? | V1 has `/account/change-password` | **Gap** | Add signed-in password change |
| Auth pages prevent zoom (`maximum-scale=1.0`) | V2 viewport allows zoom | **Stronger** | Keep |

### Auth parity verdict

V2 auth is functionally close to V1 and stronger on 2FA. The legal/consent gap is
the blocker, not the login form.

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
| Settings (AI prefs, study prefs, notifications, theme, export, delete, password) | Settings (profile, languages, availability, notifications, export, delete) | **Partial** | Add password, consent history, push devices, theme; keep export/delete |
| Separate Academia and Skills notifications | One notification list in Settings | **Gap** | Add `/notifications` with filters and deep links |
| No global command/search | None | **New opportunity** | Add app search/command menu if budget allows |

### 4.2 Academia

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Dashboard: performance, AI insights, upcoming exams, continue studying, courses, recent materials | Dashboard: five questions, next action, courses, materials, CBT | **Parity/stronger** | Redesign with a next-action anchor and tables |
| Materials browse by taxonomy | Materials list + search + reader | **Parity/stronger** | Add course filter and topic grouping |
| Upload material + my uploads + moderation | No student upload; curated materials only | **Dropped/decide** | Decide: restore uploads or state curated materials + Ask as replacement |
| Course detail hub | No course/topic route | **Gap** | Add `/academia/courses/:code` if the API exposes enough, or extend the API |
| Topic detail (explanation, videos, materials, AI) | No topic route | **Gap** | Add topic view or fold topics into the course hub |
| Browse courses + academic search | Materials search only | **Partial** | Add course/skill search/filter; consider a unified search |
| Threaded AI tutor with streaming | Ask Nelavista sessions | **Parity/stronger** | Keep threads, citations, honest decline |
| CBT practice with timer and server grading | CBT quiz/answer/results | **Parity/stronger** | Keep integrity; add question palette |
| CBT history + attempt review + AI explain | No history; results only | **Gap** | Add history/review; needs API work |
| Analyze Materials: PDF → notes → test | None | **Dropped/decide** | Decide: restore, or state Ask + CBT + curated materials is the replacement |
| Campus map + locations | Campus read-only page | **Partial** | Add map/location detail if data exists; otherwise keep a clear utility |
| Notifications | Settings list only | **Gap** | Add `/notifications` |

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
| Skills notifications | Settings list | **Gap** | Add `/notifications` |
| Skills profile/privacy | Settings visibility | **Parity** | Keep; explain what employers see |

### 4.4 Opportunities, work, money

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Job-board list + one-click apply | Opportunities with eligibility explanation | **Stronger** | Keep; add application status |
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
| Admin campus management | No admin campus screen | **Gap** | Add `#/campus` using `POST /ops/campus` |

### 4.6 Student app verdict

V2 is stronger in verification, matching, managed work, quality, ledger and
talent privacy. It is weaker in notifications, password change, consent, push
devices, CBT history, course/topic learning, search, applications and eligibility.
Those are the screens to add or restore before calling V2 “not less than V1.”

---

## 5. Admin parity

| V1 admin | V2 admin | Verdict | Action |
|---|---|---|---|
| Dashboard with counts and newest users | No dashboard; Audit is the default | **Gap** | Add an overview or make Audit a useful landing |
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
| Opportunities + applications | Opportunities | **Parity/stronger** | Add the application status action |
| Competitions | External opportunities | **Replaced** | Use opportunities |
| Campus map admin | `#/campus` publishes items | **Stronger, write-only** | Read endpoint is a launch dependency; do not fake a published list |
| No audit UI | Audit | **Stronger** | Keep |
| No waitlist screen | `#/waitlist` | **Stronger** | Built |
| No payout item failure action | API exists | **Gap** | Add action in Money |
| No platform policy | Platform | **Stronger** | Keep |
| No security/2FA | Security + forced 2FA | **Stronger** | Keep |

### Admin parity verdict

V2 admin is stronger than V1 in audit, money, quality, platform policy,
security, overview, waitlist and campus publishing. It is weaker in
content/material ops, the application status action, payout-item failure and the
missing campus read. Add those actions; do not rebuild V1's dead moderation
tools.

---

## 6. Utility and system parity

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| 404/500/503 pages | Catch-all redirects home; no error boundary | **Gap** | Add 404, error boundary, offline and maintenance states |
| Theme toggle | Dark only | **Gap** | Add Ink + Paper |
| PWA manifest but no offline | Real PWA shell | **Stronger** | Keep; add update/install UX |
| No robots/sitemap | Basic robots/sitemap | **Partial** | Expand for public pages |
| No OG/canonical | Title only | **Gap** | Add per-page meta |
| No analytics/error tracking | None | **Gap** | Add before launch |
| Support email/social links | None | **Gap** | Add real contact details or omit |
| No admin 404 | Unknown hash renders Audit | **Gap** | Add admin 404 |
| No skip link/aria-current | None | **Gap** | Add in the shell |

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
| Student material uploads + my uploads | Restore, or state curated materials is the replacement? |
| PDF → notes → test analysis | Restore, or state Ask + CBT + materials is the replacement? |
| Course/topic pages | Restore, or state dashboard + materials + CBT is the replacement? |
| CBT history/review | Restore, or state current results is enough? |
| AI answer flags / AI quality loop | Does Ask need a flag/review queue? |
| Admin material/video moderation | Does V2 need ops ingestion/moderation for materials? |
| LASU curriculum browser | Is academic context enough, or is the curriculum reference needed? |
| Theme toggle | Add Ink + Paper, or choose Ink only with a clear reason? |

---

## 8. What V2 must add to be “not less than V1”

### Public

1. `/features`
2. `/how-it-works`
3. `/about`
4. `/contact`
5. `/faq`
6. `/legal/privacy`
7. `/legal/terms`
8. `/legal/contributor-terms`
9. Real footer/contact/social links, or none
10. Per-page SEO and a full sitemap

### Auth

11. Terms links + consent recording
12. Signed-in password change
13. Google SSO decision
14. 2FA/security settings for students if the product offers it

### Student app

15. `/notifications`
16. `/opportunities/applications`
17. Eligibility/readiness
18. Cohort invite response
19. Push-device registration or an honest toggle
20. Consent history/re-consent
21. CBT history/review (or explicit replacement)
22. Course/topic view (or explicit replacement)
23. Skills search/filter
24. Material upload/analysis decision
25. 404, error boundary, offline state
26. Ink + Paper theme

### Admin

27. `#/waitlist`
28. `#/campus`
29. Application status action
30. Payout-item failure action
31. Admin 404
32. Overview/dashboard or a better default
33. Material/content ops decision
34. Newsletter/announcement admin only if approved

### New, not parity

35. Platform announcement banner (backend + admin + public)
36. Newsletter subscription (backend + consent + admin + public)

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

## 10. Parity verdict

V2 has a **stronger core** than V1: evidence-based verification, managed work,
quality, ledger, scoped talent shares and a real admin audit trail. It has a
**weaker perimeter**: no public site, no legal/consent UX, no notification centre,
no password change, no 404, no theme, and several API capabilities with no screen.

The redesign should not try to reproduce V1. It should keep V2's stronger core,
close the perimeter gaps, and explicitly retire V1's dead or unsafe surfaces.
