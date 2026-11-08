# V1 → V2 parity

| Field | Value |
|---|---|
| Status | **Implemented 2026-11-01; V1 delta audited 2026-11-04; ALL catalogue ported 2026-11-04.** The original parity scope is wired. The V2 seed now contains the ALL catalogue and tracks; the language profile, hub/filter UI, richer task scoring and FUTA taxonomy remain open. |
| Date | 2026-10-27; post-build, palette correction and API closure 2026-11-01; V1 delta 2026-11-04 |
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
| Public marketing | Separate routed pages: Landing, Features, How it works, About, Contact, FAQ, 404, Offline; per-page metadata and sitemap | **Parity/stronger** for the original set; **gap** for V1's new `/impact` page and landing track-record band |
| Auth | Login, signup, verify, reset; shared auth layout; legal links; signup records terms and privacy at the current version | **Parity**; `ConsentGate` handles re-consent after a version change |
| Student journey | Home, Academia, Materials, Ask, CBT, Skills, My learning, Lesson, Practice, Verification, Assessment, Attempt review, Practical task, Transcript, Opportunities, Applications, Work, Earnings, Talent, Campus, Notifications, Settings, Onboarding | **Parity/stronger** for the original set; **gap** for V1's new ALL hub and language profile |
| Skills | Verification/evidence journey and practice | **Stronger** in verification/evidence; the ALL catalogue is seeded. **Gap** for the language profile, hub/filter UI and structured scored-task UX |
| Academia | Dashboard, materials, Ask, CBT, course and topic detail, CBT history | **Parity/stronger**; uploads/analysis deferred |
| Opportunities/work/money | Managed model, eligibility blockers, applications, invitations, ledger, payout batches | **Stronger** than V1's status-only marketplace |
| Talent/transcript | Evidence-only, scoped revocable shares, consent history | **Stronger** privacy; **parity** on the original proof surface. **Gap** for V1's per-skill evidence trail, academic background and language profile on the talent view |
| Employer | No self-service | **Dropped by design** at launch; managed work instead. The V2 API now has the permission-gated `/v1/talent/directory` contract for language, language level, academic level, visibility status and background filtering; no employer UI is planned unless this surface is later approved |
| Admin | Overview, Waitlist, Campus, Audit, Imports, Users, Opportunities, Projects, Review, Money, Content, Platform, Security, 404 | **Stronger** in audit/money/quality; bulk actions remain later work |
| Utility | Real 404, error boundary, offline screen, route focus/title | **Parity/stronger** |
| Theme | Light/dark with Nelavista blue and white | **Parity**; both surfaces implemented, manual visual pass recommended |
| Public legal/contact | Privacy, terms and contributor terms in final product copy; real support email | **Parity**; legal copy is not a draft |

**Bottom line:** V2 covers the original V1 journey and exceeds it in verification,
managed work, money controls and admin audit. It does **not** yet cover the V1
additions landed on `main` between 2026-10-30 and 2026-11-04: the African Languages
Lab (ALL) skills, the language profile and structured scored tasks, the Impact page,
and the FUTA official taxonomy seed. Those are recorded in §1.2 and tracked as I1–I8
in `docs/build/REMAINING_WORK.md`. The other remaining gaps are real business
content, approved pricing, social profile URLs, photography and the manual launch
checks.

### 1.1 What is still limited

- **Closed API work:** in-place signed-in password change; full course/topic
  detail; CBT history with answer review; student cohort-invite list; admin campus
  read. All are implemented and used by the UI.
- **Content:** real social profile URLs, real metrics/testimonials, photography,
  employer positioning, and the material upload/analysis replacement copy. Pricing
  is published as commercial positions, not invented amounts.
- **Verification:** admin 2FA enrolment recovery-code handoff is fixed; a full
  browser end-to-end check and the V2 domain switch remain. The local seed lock
  was traced to duplicate API/worker processes, not seed logic.
- **Images:** the editorial set is integrated with WebP derivatives; real
  photography is still pending.
- **Brand video:** the MP4 now runs full-width before the public footer with a
  reduced-motion still fallback.
- **V1 delta (2026-11-04):** the V1 additions listed in §1.2 are not in V2. They are
  not a reason to reopen the closed UI work, but they are a real regression risk if
  `develop` is merged to `main` at launch without porting them or explicitly
  deciding to drop them.

### 1.2 V1 additions after the parity review (2026-11-04)

The V1 `main` branch received new work after the 2026-11-01 parity close. The
source of truth for the delta is the V1 code on `main`, not this table:

| V1 addition | What V1 now has | V2 state | Verdict | Action |
|---|---|---|---|---|
| African Languages Lab (ALL) content | 9 ALL categories (`SkillCategory.program = 'all'`), 94 published skills (including the `african-language-data-beginner` entry path), 10 multi-skill career tracks, lessons, practice tasks and assessments | V2 seed now contains the catalogue, tracks and learning content; V2 does not yet have the language profile, ALL hub/filter UI or V1 project-template parity | **Partial** | Keep the V2 seed idempotent and add the remaining profile, hub/filter and project/task UX before claiming full parity. |
| Language profile | `/skills/languages`: self-reported languages, dialect, proficiency, `can_speak/read/write/transcribe/translate`; `user.language_background`; verified capabilities derived from verified language-specific skills | None in the V2 identity or skills model | **Gap** | Add `StudentLanguage`/profile fields to V2 identity or skills, with the same self-reported vs verified separation. |
| Structured scored tasks | `Challenge.task_spec_json` for transcription, translation, labeling and recording; deterministic scoring (WER, chrF, label accuracy, recording requirements, repeat consistency); `ChallengeSubmission.score`/`result_json` | V2 has `TaskTemplate` validators and first-class verification assessments, but no structured language-task spec or deterministic WER/chrF scoring | **Gap/decide** | Map the four task kinds to V2 `TaskTemplate`/assessment models; keep expected answers out of student responses. |
| Assessment gate | A skill with an assessment is verified only after every lesson is complete, every scored practice task is attempted and the assessment reaches its pass mark; assessment prerequisites are enforced server-side | V2 verification is already assessment/practical-evidence based, but has no equivalent per-skill scored-practice gate | **Partial** | Reuse V2's evidence model; add the per-skill scored-practice prerequisite only if ALL is ported. |
| ALL hub and catalogue filters | `/skills/african-languages` hub with language/level filters, recommended skills and track progress; catalogue filters for language, level, tag and programme | `/skills` catalogue only; no language/tag/programme filters, no hub, no tracks | **Gap** | Add the hub and the filters only after the data model exists. |
| Transcript and talent evidence | Per-skill verification records on the transcript; evidence records, academic background and languages on the Talent profile; evidence visibility still respects the `show_skill_transcript` privacy toggle | V2 transcript/talent exist, but not the per-skill evidence trail, academic background or languages | **Partial** | Extend the V2 transcript/talent reads; keep the privacy toggle authoritative. |
| Employer talent search filters | Language, level, verification/assessment status, practical-done and academic-background filters on `/employer/discover` (employers and admins) | V2 API provides `/v1/talent/directory` with language, language level, academic level, visibility status and background filters; verification/practical status filters and UI remain out of scope with employer self-service dropped | **Partial/decision** | Keep the API contract available for a future approved talent-search surface; add UI and evidence-status filters only if that product decision changes |
| Impact page | Public `/impact` with reach numbers, "what we've built", CTA; landing track-record band and footer link | No `/impact`, no band, no footer link | **Gap** | Add `/impact` only after the 2,500+/500+ figures are verified. Do not copy unverified social proof into V2. |
| FUTA official taxonomy | Verified FUTA schools/departments and 35 Surveying & GeoInformatics courses, with provenance (`Course.source = 'futa_official'`) and a cleanup script for unlisted departments | V2 now seeds the verified structure and SVG rows, adds `semester`, `course_type`, `description` and `source`, and preserves them through V1 export/import | **Partial** | Add further department course lists only after their official FUTA pages are verified; do not infer unlisted courses |
| AI grading hardening | `wrap_untrusted` escapes student-supplied `<student_content>` delimiters, so a submission cannot close the untrusted block early | V2's Ask prompt still interpolates the raw question and retrieved text into one prompt; V2 assessment grading is deterministic | **Gap (hardening)** | Apply the same untrusted-content boundary to V2's Ask/practice AI prompts before launch. |
| Test-suite speed | Test-only SQLite pragmas (`synchronous=OFF`, `journal_mode=MEMORY`) shorten V1 suite setup | V2 has its own test fixtures; no user-facing change | **No action** | Keep the optimisation in V1; do not copy test pragmas into production configuration. |

**V1 delta verdict:** the original V2 parity claim still holds for the features it
audited, but V2 is no longer a superset of V1. The ALL work is the largest gap:
it is a content product plus schema plus assessment behaviour, and it crosses
skills, verification, transcript, talent and mobile. Impact and FUTA are smaller
but still visible to users or operators. Treat all three as launch decisions, not
as documentation-only omissions.

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
| No pricing page; “free for students” only | `/pricing` with launch, scoped-quote and pilot positions; no invented amounts | **Stronger** | Replace positions with approved amounts when supplied |
| `/privacy-policy` | `/legal/privacy` final product copy for V2 data flows | **Parity** | Keep the version in sync with `/platform/config` |
| `/terms-of-service` | `/legal/terms` final product copy for V2 | **Parity** | Keep the version in sync with `/platform/config` |
| Contributor terms only in platform settings | `/legal/contributor-terms` public final copy | **Parity/stronger** | Keep quality, payment and licence terms aligned with the API |
| `/impact` track-record page (new 2026-11-01) with 2,500+ students reached, 500+ trained in AI, live university/skill counts; landing band and footer link | None | **Gap** | Add `/impact` only after the fixed figures are verified; otherwise keep the honest “working record” copy on `/about` and do not imply the numbers |
| No newsletter | None | **New** | Deferred; needs consent/unsubscribe |
| No public announcement banner | None | **New** | Deferred; not parity |
| No blog | None | **Not required** | Do not add |
| Employer signup/dashboard/discover | None | **Dropped by design** | Managed work through ops; employer self-service later |
| Footer social links (placeholder `example.com`) | Facebook, WhatsApp and Telegram share intents in a wave layout; no invented profile URLs | **Parity/stronger** | Add real profile URLs only when supplied |
| Theme toggle | Light/dark on brand blue/white | **Parity** | Manual visual pass recommended |
| PWA manifest, no offline | Real PWA shell and offline route | **Stronger** | Keep; add update/install UX |
| No V1 robots/sitemap/OG | Per-page title/description/canonical/OG; expanded sitemap | **Stronger** | Keep route and meta maps in sync |

### Public parity verdict (post-build)

V1's public site is a polished landing page plus thin About/legal pages, and now
an Impact page with fixed reach figures. V2 has the separate marketing routes,
the three legal documents, a real 404 and an offline screen, plus per-page
metadata and a fuller sitemap. The Impact page is the one new public route V2
does not have; add it only after the figures are verified. The remaining public
work is otherwise approved pricing and real business content.

---

## 3. Auth parity

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Login with username or email + password | Login with email + password; staff 2FA | **Parity** | Redesign; keep 2FA challenge |
| Google sign-in when configured | `POST /auth/google` exists, no button | **Gap** | Add only if the flow and consent are designed; otherwise defer |
| Signup username/email/password | Signup name/email/username/password; links to legal pages; records terms and privacy at the current version | **Parity/stronger** | Keep versions in sync with `/platform/config` |
| Email verification result + resend | `/auth/verify` + resend | **Parity** | Redesign; handle expired/invalid states |
| Forgot password | `/auth/reset` request state | **Parity** | Redesign; keep anti-enumeration copy |
| Reset password | `/auth/reset` token state | **Parity** | Redesign; keep single-use token behavior |
| Signup accepted terms with no links | Legal links; signup records `terms_of_service` and `privacy_policy` at `TERMS_VERSION`; consent history and re-consent gate are visible | **Parity/stronger** | Keep versions in sync with `/platform/config` |
| No change-password in V1? | V1 has `/account/change-password` | **Parity** | `POST /auth/password/change` renews this session and revokes other refresh tokens |
| Auth pages prevent zoom (`maximum-scale=1.0`) | V2 viewport allows zoom | **Stronger** | Keep |

### Auth parity verdict (post-build)

V2 auth is functionally close to V1 and stronger on 2FA. Login, signup, verify
and reset are redesigned, password fields have a show/hide control, signup links
to the legal pages and records both consents. Re-consent is handled by
`ConsentGate`, and the in-place password change is wired.

---

## 4. Student app parity

### 4.1 Entry, identity and account

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Landing redirects signed-in users to saved path | `/` redirects signed-in users to `/home`; a returning login opens the saved space | **Parity/stronger** | Keep the Home switcher visible for deliberate changes |
| `/choose-path` two-product fork | Four-space picker in onboarding and Home: `academia`, `skills`, `opportunities`, `campus` | **Stronger** | Each space has its own dashboard destination |
| Academia onboarding wizard | `/onboarding` two-step flow that collects only what the chosen space reads | **Parity/stronger** | Academia uses university/faculty/department/courses; Campus uses the university only; Skills and Opportunities finish at the choice |
| Skills onboarding modal | Folded into the four-space `/onboarding` choice | **Replaced** | No separate first-run modal |
| Profile + LASU curriculum browser | Settings profile + academic context | **Partial** | Keep academic context; decide whether to restore a curriculum reference |
| Settings (AI prefs, study prefs, notifications, theme, export, delete, password) | Split Settings: profile, security, notifications, data; consent history and push devices; theme in the shell | **Parity/stronger** | In-place password change is built |
| Separate Academia and Skills notifications | `/notifications` plus a recent list in Settings | **Parity/stronger** | Built |
| No global command/search | None | **New opportunity** | Add app search/command menu if budget allows |

### 4.2 Academia

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Dashboard: performance, AI insights, upcoming exams, continue studying, courses, recent materials | Dashboard: five questions, next action, courses, materials, CBT | **Parity/stronger** | Redesign with a next-action anchor and tables |
| Materials browse by taxonomy | Materials list + search + reader | **Parity/stronger** | Add course filter and topic grouping |
| Upload material + my uploads + moderation | No student upload; curated materials only | **Dropped/decide** | Decide: restore uploads or state curated materials + Ask as replacement |
| Course detail hub | `/academia/courses/:courseCode` with topics, materials and the student's practice record | **Parity/stronger** | Keep the course page a reading surface |
| Topic detail (explanation, videos, materials, AI) | `/academia/topics/:topicId` with the topic record, materials and practice state | **Parity** | Video and AI explanation remain outside current scope |
| Browse courses + academic search | Materials search and course filter | **Partial** | Add course/skill search/filter; consider a unified search |
| Threaded AI tutor with streaming | Ask Nelavista sessions | **Parity/stronger** | Keep threads, citations, honest decline |
| CBT practice with timer and server grading | CBT quiz/answer/results | **Parity/stronger** | Keep integrity; add question palette |
| CBT history + attempt review + AI explain | `/academia/cbt/history` shows each attempt, the selected and correct key, and the explanation; results exist | **Parity/stronger** | Keep answer review scoped to the signed-in student |
| Analyze Materials: PDF → notes → test | None | **Dropped/decide** | Deferred with replacement: curated materials + Ask + CBT + transcript evidence trail |
| Campus map + locations | Campus dashboard and read-only map links | **Parity** | A Campus-first student sets the university without a course enrolment; map detail stays data-driven |
| Notifications | `/notifications` and recent list in Settings | **Parity/stronger** | Built |

### 4.3 Skills

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Skills home with pipeline, stats, continue learning, earnings | Skills catalog + My Learning + Home | **Partial** | Add a “next step” anchor to Skills; avoid stat-card clutter |
| Catalog with categories | Skills catalog | **Parity** | Add search/filter and time/difficulty metadata if available; V1 now also filters by language, level, tag and programme |
| Skills search | None | **Gap** | Add search/filter to `/skills`; the V1 delta makes language/tag filters part of the target if ALL is ported |
| African Languages Lab hub (new 2026-10-30) | V2 catalogue seed exists; no dedicated hub | **Gap** | Add `/skills/african-languages` with language/level filters over the seeded ALL programme |
| Language profile (new 2026-10-30) | None; Settings has a languages field, but no self-reported capability profile and no verified-by-skill derivation | **Gap** | Add `StudentLanguage`-equivalent data and `/skills/languages`; keep self-reported and verified visibly separate |
| Structured scored tasks and assessment gate (new 2026-10-30) | V2 TaskTemplate validators + verification assessments; no transcription/translation/labeling/recording task spec, WER/chrF scoring or per-skill scored-practice gate | **Gap/decide** | Map the four task kinds into V2's task/assessment model; never reveal expected answers on an assessment |
| Per-skill evidence on transcript/talent (new 2026-10-30) | Transcript groups and talent shares exist; no per-skill evidence record, academic background or language profile | **Partial** | Extend the existing reads; keep `show_skill_transcript` authoritative |
| Learning paths/tracks | Paths | **Parity** for single-skill paths; **gap** for V1's multi-skill career tracks | Keep ordered steps; decide whether V2 needs multi-skill tracks or maps them to paths |
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
| Cohort invite response absent | `/work` reads `GET /work/invites` and answers through `POST /work/cohorts/{id}/respond` | **Parity/stronger** | Decline is confirmed; accept re-reads assignments |
| Earnings status-only, no gateway | Ledger, payout batches, second approver | **Stronger** | Keep; add payout status detail |
| No quality record | Quality score with counts | **New/stronger** | Keep |
| No transcript for work | Work history in Talent | **New/stronger** | Keep |

### 4.5 Campus

| V1 | V2 | Verdict | Action |
|---|---|---|---|
| Campus map with locations, categories, coordinates | Campus page | **Partial** | Keep as a light utility; add map/location detail if data supports it |
| Admin campus management | `#/campus` publishes through `POST /ops/campus` and reads the live set through `GET /ops/campus`, including hidden rows | **Parity/stronger** | Keep publication state visible in the table |

### 4.6 Student app verdict (post-build)

V2 is stronger in verification, matching, managed work, quality, ledger and
talent privacy. The four spaces are a first-class product choice, with a
dashboard destination for each. The notification centre, applications,
invitations, eligibility blockers, consent history, push-device
list/removal, CBT review, course and topic detail, password change and split
settings are built. Skills search and uploads remain later-scope items, not
missing primary screens. The V1 delta adds one missing product area rather than a
missing screen: ALL content, the language profile and structured language tasks
are absent from V2 and must be ported or explicitly dropped.

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
| Campus map admin | `#/campus` publishes and reads live items, including hidden rows | **Stronger** | Keep the filter and publication state visible |
| No audit UI | Audit | **Stronger** | Keep |
| No waitlist screen | `#/waitlist` | **Stronger** | Built |
| No payout item failure action | Money exposes the fail action with a required reason | **Parity/stronger** | Built |
| No platform policy | Platform | **Stronger** | Keep |
| No security/2FA | Security + forced 2FA | **Stronger** | Keep |

### Admin parity verdict (post-build)

V2 admin is stronger than V1 in audit, money, quality, platform policy, security,
overview, waitlist and campus publishing, including live campus reads. Application
status and payout-item failure are now exposed. The remaining gaps are bulk
actions, a purpose-built aggregate overview, and a material/content-ops decision.
Do not rebuild V1's dead moderation tools.

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
| Course/topic pages | In scope and built. The course page links to a separate topic route. |
| CBT history/review | In scope and built. Answers and explanations are scoped to the signed-in student. |
| AI answer flags / AI quality loop | Does Ask need a flag/review queue? |
| Admin material/video moderation | Does V2 need ops ingestion/moderation for materials? |
| LASU curriculum browser | Is academic context enough, or is the curriculum reference needed? |
| Employer self-service | Later product; managed work is the launch replacement. |
| African Languages Lab | Port the 94-skill curriculum and its assessment model into V2, or launch V2 without V1's newest catalogue? |
| Impact page metrics | Are the 2,500+ students reached and 500+ trained in AI current and approved for public use? |
| FUTA taxonomy | Import the verified FUTA taxonomy from V1, or seed it natively in V2? If imported, add V2 `Course` semester/source fields first. |

---

## 8. Post-build checklist

### Built

- Public: `/features`, `/how-it-works`, `/about`, `/contact`, `/faq`,
  `/legal/privacy`, `/legal/terms`, `/legal/contributor-terms`, real 404,
  offline screen, per-page metadata and sitemap.
- Auth: redesigned login, signup, verify and reset; legal links and recorded
  terms/privacy consent.
- Student: notification centre, my applications, invitations, eligibility
  blockers on opportunity detail, honest push-device list/removal, consent
  history, CBT review, course and topic detail, in-place password change, split
  settings, 404/offline, light/dark brand theme.
- Admin: Overview, Waitlist, Campus, Audit, Imports, Users, Opportunities,
  Projects, Review, Money, Content, Platform, Security, admin 404, application
  status action and payout-item failure action.
- Brand: V1 logo/favicon copied into V2, generated PWA/apple icons, larger WebP
  boot loader and still-mark fallback, circular nav mark, brand film before the
  footer.
- UX guards: confirmation dialog for sign out, device/language removal, share
  revocation and destructive admin actions; password reveal controls.

### Still blocked or deferred

- **V1 delta (2026-11-04):** ALL curriculum, language profile, structured scored
  tasks, the ALL hub, transcript/talent evidence, talent language filters, the
  Impact page and the FUTA taxonomy seed. See §1.2 and `REMAINING_WORK.md` §I.
- Approved pricing amounts and real business content.
- Skills search/filter (later scope).
- Material upload/analysis (deferred with replacement copy).
- Google SSO (deferred).
- Offline submission sync (deferred).
- Newsletter and platform announcement banner (post-launch, not parity).
- Analytics/error tracking (before launch).
- Real business content, photography and the approved image set.

### New, not parity

- Platform announcement banner (backend + admin + public).
- Newsletter subscription (backend + consent + admin + public).

---

## 9. What not to carry from V1

- Hardcoded “2,500+” students or any unverified social proof. V1 now repeats
  those figures on `/impact`; do not copy them into V2 until the business owner
  confirms they are current and defensible.
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
is now built: public routes, final legal pages, notification centre, applications,
consent history, push-device control, course/topic detail, CBT review, cohort
invitations and utility screens exist.

What remains is not a missing primary screen or API route for the original parity
scope. It is real business content and a small set of later-scope items (skills
search, uploads, Google SSO, offline sync, analytics), plus the manual launch
checks. The exception is the 2026-11-04 V1 delta: ALL, the language profile,
structured scored tasks, the Impact page and the FUTA taxonomy are real new
product scope. V2 must port them or explicitly drop them before claiming parity
again. The redesign should keep V2's stronger core and explicitly retire V1's
dead or unsafe surfaces.
