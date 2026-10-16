# Nelavista V2: Build Plan (Prompt 2 of 2)

Use this AFTER Prompt 1 (organise the codebase) has finished Phase 3. Paste everything inside the code block into your coding agent. Keep the PRD at `docs/product/Nelavista_V2_PRD.pdf`.

---

```
ROLE
You are the lead engineer building Nelavista V2. The monorepo, environments, CI and empty skeletons already exist (from the organise-codebase work). Your job is to build V2 in phases, reusing V1 assets wherever that is cheaper and safer than rewriting, without ever breaking V1, which is live.

PRODUCT CONTEXT
Nelavista takes an African university student from lecture hall to paid work:
University student → Education → Skills → Verified talent → Real work → Income.
The core system, and the only thing that matters for V2, is:
Student → Learn → Build → Verify → Match → Work → Quality → Earn.
If a feature does not move a student along that journey, it waits.

PRD essentials (the full PDF is in docs/product/; the PRD wins if this summary conflicts):
- Choose Path after login: Academia ("help me succeed in university": Learn → Practice → Improve) and Skills ("help me build skills and earn"). Campus is a light utility reachable from both. There is no Community product. One student identity across everything: account, profile, and a record of what they learned, proved and earned.
- Academia: improve and connect what exists (Dashboard, Study Materials, Ask Nelavista, CBT, Material Analysis, Profile, Campus Map, Settings). Do NOT build assignments, social feeds, gamification for its own sake, or new academic feature areas. Ask Nelavista becomes aware of the student's courses, materials and topics. CBT shows strengths, weaknesses and what to practise next. The existing dashboard answers: What am I studying? What did I study recently? What should I practise? Where am I weak? What should I do next?
- Skills: Discover → Learn → Practice → Build → Verify → Match → Work → Quality check → Earn.
- Verification is proof, not claims. Never verified for watching lessons or clicking complete. Earned through assessments, practical tasks, projects and quality history on real work. It is alive: good work strengthens it, poor quality weakens it.
- Matching is not a job board. It uses verified skills, assessments, project history, quality, availability, university, language, location where relevant, and the opportunity's requirements. Every student sees why they qualify or exactly what they are missing, and a gap always points back into learning and verification: Opportunity → Requirement → Skill gap → Learning → Verification → Eligibility.
- Quality control is a first-class stage: work is reviewed against the project's quality standard before approval and payment; each student builds a quality record feeding verification, matching and their Talent profile; consistently poor quality has consequences (fewer matches, re-verification, removal from a project).
- Managed workforce: a company hands us a large project (for example 5,000 contributors for AI data work) and we identify qualified students, confirm eligibility, organise a cohort, distribute work, track participation, monitor quality, replace poor performers, coordinate delivery and process payouts. Early on our team runs company-side steps by hand with internal tools, but the model must let company self-service sit on top later without a rebuild.
- Talent profile: every item is evidence, not a claim (skills, verified skills, projects, Skill Transcript, assessments, quality history, work history, portfolio, availability, academic context).
- Opportunities: managed paid work (gigs, AI/data projects, freelance and project work we run end to end; the 10% fee applies) and external opportunities (internships, jobs, scholarships, competitions; we surface and match; no fee by default, never 10% of a salary, stipend or prize).
- Money (managed paid work only): the client pays Nelavista; students receive 90%; Nelavista's fee is 10%; 20% of that fee (2% of the total) goes to the participating department, taken from the fee and NEVER from the student's 90%. Example: $10,000 → students $9,000, department $200, Nelavista keeps $800. Every managed project tracks project value, student payout, Nelavista fee, department share, work status, quality status and payment status. Escrow, taxes, currency and payout rails are undecided; the requirement now is that money is transparent and trackable and every student can see what they earned and why.
- Build first: the full Skills journey for AI Data Annotation, internal tools for our team to run managed projects, quality review, and the earnings ledger, plus focused fixes connecting the existing Academia experience. Build later (do NOT build now): more skill paths, automated matching at scale, company self-service.
- Quality bar: mobile-first (mid-range Android AND iOS), lightweight on expensive and unstable data, simple enough to use without a tutorial, built for African university realities, scalable beyond one university and one skill, reliable (no lost work, answers or payments). Scale: thousands of students, then hundreds of thousands, then millions.

PRECONDITIONS (check first, and stop if they fail)
Read docs/architecture/*, docs/adr/* and docs/runbooks/*. Confirm that the monorepo skeletons (api, web, mobile for iOS and Android, admin), CI, the environment separation (local, dev, prod) and the V1 versioning plan exist and are green. If anything is missing or contradicts this brief, report it and wait. Use the stack and conventions chosen in the ADRs. Do not re-litigate them unless you find a blocking problem. The ADR default is FastAPI + Postgres + SQLAlchemy/Alembic, React/Vite/Tailwind PWA, Expo (React Native) for iOS and Android, a separate admin app, and a generated TypeScript API client.

V1 REUSE POLICY
V1 stays live and frozen (security and critical fixes only, on its own branch). V2 never imports V1 code, and V2 never connects to the V1 production database. Anything reused comes through one of three routes:
  A) DATA: one-way, repeatable, idempotent imports from V1 exports or a read-only snapshot, each with a dry-run mode and a reconciliation report (counts and checksums, V1 versus V2).
  B) LOGIC: ported into V2 modules as clean code with tests, using V1's behaviour as the spec. V1's tests become acceptance cases where they apply.
  C) CONTENT AND FILES: reused in place (for example Cloudinary files referenced by ID or URL), never copied blindly.
Verify each item against the real code before relying on it. This table is a starting hypothesis from V1's README:

  REUSE (data)          University/faculty/department/level/course taxonomy (data/Nelavista_Course_Codes.csv, CCMAS core), CBT question banks (data/cbt questions), materials metadata and Cloudinary files, the Skills catalog (the 20 learning paths and their topics from seed_skills), campus map data, V1 users (see accounts below).
  PORT (logic)          services/ai_provider.py abstraction, RAG chunking/embedding/retrieval with the honest-decline-below-threshold rule, insights (weak/strong topics, recommendations), full-text search approach, onboarding flow logic, CBT timing/scoring rules, email copy and templates, PWA assets and icons, the admin moderation concepts.
  REWRITE               All Jinja/vanilla-JS UI, V1 auth plumbing, anything built around eventlet/Socket.IO, V1's cohort/class GPA system (evaluate against the PRD's cohort model, which is different), employer messaging.
  DROP OR DEFER         Community chat (the PRD has no Community product), live classes unless the audit shows real usage and a clear job in the journey, anything the PRD says not to build.

Accounts: V1 users must be able to continue into V2 without starting over ("Continue with your V1 account"). Plan for V1 password-hash verification with silent re-hash on first V2 login, Google OAuth account linking by verified email, and no password ever leaving V1 in plain form. Follow the approved ADR on identity.

WORKING METHOD (every phase)
1. PLAN: write docs/build/phase-N-plan.md: goal, scope, tasks broken into PRs of about 400 changed lines or fewer, which modules and folders each PR touches (so parallel developers don't collide), risks, test plan, and the manual steps I must do. STOP and wait for my approval.
2. BUILD in small PRs behind feature flags. Contract first: the API schema and typed client before the screens. Tests with the code. Migrations use expand/contract and keep a single Alembic head.
3. MOBILE AND ADMIN SLICES: every phase has a student-facing slice that ships on the web PWA and on mobile (iOS and Android) from the same API and shared logic packages, and an ops slice in apps/admin where the phase needs one. Propose in Phase 0 whether mobile ships in lockstep with web or one phase behind, based on team size. My preference is lockstep for the core journey screens.
4. VERIFY: run the full test suite, a demo script (exact steps I can follow in the DEV environment on a web browser, an Android phone and an iPhone), and an acceptance checklist. Report results honestly, including what is not done.
5. GATE: summarise, list files changed, open questions and manual steps, then STOP until I approve the next phase.

GLOBAL STANDARDS (apply in every phase)
- PERFORMANCE: budgets set in Phase 0 and checked in CI where possible. Targets to start with: web first load about 150 KB of gzipped JavaScript or less, usable on throttled slow 4G on a mid-range Android phone, API p95 under 300 ms for common reads, small paginated payloads, image optimisation, skeleton states instead of spinners, and a mobile app download size kept deliberately small.
- OFFLINE AND LOW DATA: student work (task answers, quiz answers, project drafts) is saved locally first, synced with idempotency keys and a retry queue, and is never lost on a dropped connection. Reads degrade gracefully with cached data and clear "offline" states.
- RELIABILITY: no lost work, answers or payments. Every write that matters is idempotent. Background jobs are retryable and observable.
- SECURITY: object-level authorisation on every endpoint (a student can only ever see their own records), role-based access for ops tools, rate limiting, input validation, safe file upload handling, audit logs for sensitive actions, short-lived access tokens with refresh for native clients, secure token storage on device, strong protection and two-factor for admin accounts, dependency and secret scanning in CI, and no secrets in app bundles.
- PRIVACY AND COMPLIANCE HOOKS: collect only what is needed, record consent, support data export and account deletion (the app stores require deletion in-app), and define retention. Nigerian data protection law, payout identity checks and contributor terms are decisions for me and legal counsel: build the hooks, list the questions, and do not give legal conclusions.
- OBSERVABILITY: structured logs, error tracking, product analytics events for each journey stage (enrolled, lesson done, assessment passed, matched, task submitted, approved, paid), and basic dashboards plus alerts for the API, the queue and the ledger.
- ACCESSIBILITY AND LANGUAGE: readable on small screens, good contrast, large touch targets, plain English, and strings externalised so other languages can be added later.
- TESTING: unit, integration against a real Postgres, API contract tests, web end-to-end tests, mobile end-to-end smoke tests for iOS and Android, property-based tests for money, load tests before launch.
- FEATURE FLAGS for everything unfinished. V2 data for real students is never exposed before launch gating is approved.
- DOCS: every phase updates docs/ (architecture, runbooks, ADRs for any new decision).

PHASES

PHASE 0, FOUNDATIONS AND CONTRACTS
Goal: everything later phases depend on, with no student features yet.
Build:
- Domain model v1 for the PRD entities (identity, university/department/course taxonomy, skill, learning path, lesson, task template, project, assessment, verification record, skill transcript, opportunity, requirement, cohort, assignment, submission, quality review, ledger entry, payout, department share), with migrations. Keep it extensible so skill number two is configuration and content, not new code.
- API conventions: error format, pagination, idempotency keys, API versioning, minimum-supported-app-version check and a force-update flag for mobile.
- Auth core for web and native (including Google sign-in on iOS and Android), roles and permissions (student, reviewer, ops admin, super admin; leave room for department rep and company roles), audit log.
- Design tokens and a small shared UI foundation for web and for mobile (shared tokens, not shared components).
- Background job system, feature-flag system, analytics and error tracking wired up, local and dev seed data.
- Mobile shell on both platforms: navigation, secure storage, offline store with sync queue, push notification plumbing, deep-link handling, per-environment build profiles.
- Admin shell with login, role gating and audit trail.
Acceptance: a developer can log in on web, iOS, Android and admin against local and dev; CI is green; the money and permission test harnesses exist.

PHASE 1, IDENTITY, V1 BRIDGE AND CHOOSE PATH
Goal: one student, one identity, and V1 users can come across.
Build:
- Signup/login, email verification, password reset, Google sign-in, "Continue with your V1 account" per the identity ADR.
- The one-way V1 import tooling (users, taxonomy, materials metadata, CBT banks, Skills catalog) with dry-run and reconciliation reports.
- Onboarding wizard (university → faculty → department → level → session → semester → courses) writing real enrolment records, with the waitlist for universities not yet covered.
- Choose Path screen with switching at any time, profile, settings, and the light Campus utility (campus map and university-specific info) reachable from both paths.
- Ops slice: user lookup, support tools, import run history.
Reuse: taxonomy, course data, onboarding logic, campus map data, email copy.
Acceptance: a real V1 test account is imported and continues into V2 with no re-registration; a new student onboards on web and on both mobile platforms.

PHASE 2, SKILLS ENGINE AND THE AI DATA ANNOTATION PATH
Goal: the learn, practise and build stages, proven end to end on one skill.
Build:
- Skills overview, discover, learning paths, lessons with real sequential progress, My Learning, practice challenges and projects. Progress tracking stays honest: completing a lesson never counts as verification.
- A schema-driven task engine: task templates are configuration (instructions, input type, answer schema, validation), so new annotation task types need no new code. Confirm the first task types with me (candidates: text classification, entity tagging, ranking or preference comparison, transcription or translation, language data for Nigerian languages, image labelling).
- A practice sandbox with sample tasks and instant feedback against known answers.
- The AI Data Annotation learning path structure and a placeholder or sample curriculum. The real curriculum content must be authored or sourced by the team. Build the engine, and list exactly what content I must supply.
- Ops slice: content management for paths, lessons and task templates, with a draft/publish flow.
Reuse: the Skills catalog data and structure (the other 19 paths carry across as content, but only AI Data Annotation is built end to end), lesson/quiz logic, search.
Acceptance: a student completes the AI Data Annotation path, practises on sample tasks with feedback, and submits a project, on web and mobile, including with the connection dropped mid-task.

PHASE 3, VERIFICATION AND SKILL TRANSCRIPT
Goal: a verified badge that companies can trust.
Build:
- Practical assessments using gold-standard tasks (known correct answers) with configurable pass thresholds, randomised task selection, attempt limits, and anti-cheating measures that respect low-bandwidth users.
- A verification state machine driven by evidence, not clicks: unverified, in progress, verified, at risk, suspended. Every transition is logged with the evidence behind it.
- The Skill Transcript: a student-facing record of what they learned, proved and delivered, with each entry linked to its evidence.
- Hooks so that quality results from real work (Phase 5) can strengthen or weaken verification, and rules for re-verification, all configurable and auditable.
- Ops slice: assessment management, manual review and override (with a mandatory reason, logged).
Acceptance: a student can only become verified by passing the practical assessment; watching lessons alone never changes status; the transcript updates with linked evidence.

PHASE 4, OPPORTUNITIES, MATCHING AND COHORTS (internal first)
Goal: our team can create managed projects and see exactly who qualifies.
Build:
- The opportunity model for managed paid work: requirements, required skills and verification, headcount, language, university, availability, location where relevant, quality standard, rates and payout terms.
- Rules-based eligibility and matching with an explanation for every result: why a student qualifies, or the exact missing requirement, each linking back to the learning or verification step that closes the gap.
- Cohorts and assignments: select or assign students, invite and accept flows, participation tracking, replacement of dropouts.
- Ops slice (primary here): create and manage managed projects, review matched talent, build cohorts, and see project status. This is the internal tool that runs the managed workforce.
- Design the data model so a company-facing experience can sit on top later, but do NOT build company self-service.
Acceptance: ops creates a project with requirements, the system lists eligible students with explanations, ops forms a cohort, and invited students see the opportunity with their personal "why you qualify or what you're missing".

PHASE 5, WORK DELIVERY AND QUALITY CONTROL
Goal: reliable work, which is the reason companies come back.
Build:
- Work delivery: students receive assigned tasks, work offline-first, and submit with idempotent sync. Work batches, deadlines and progress.
- Quality control: gold tasks mixed into live work at a configurable rate, double annotation with agreement scoring, reviewer sampling queues, review against the project's quality standard, approve, reject or request rework. Per-task and rolling per-student quality scores.
- The student quality record, feeding verification, matching and the Talent profile.
- Consequence rules, all configurable per project and visible to ops: warn, restrict matching, require re-verification, remove from a project and trigger replacement. Humans can override, with a logged reason.
- Messages and notifications (in-app and push on both platforms) for assignments, reviews, rework and payments.
- Ops slice: review queues, quality dashboards, flagged contributors, and delivery progress per project.
Acceptance: a pilot project of test work runs end to end: assigned, completed (including offline), reviewed, approved or sent back, with quality scores updating verification and eligibility.

PHASE 6, MONEY: LEDGER, EARNINGS AND PAYOUTS
Goal: transparent, trackable, correct money.
Build:
- An append-only ledger. Integer minor units plus a currency code; never floating point anywhere (add a lint rule). Corrections are new entries, never edits. Every write carries an idempotency key.
- The split engine: fee, department share and student pool computed exactly as the PRD defines, with a documented, deterministic rounding rule (propose one, for example largest remainder with leftovers to the platform, and ask me to approve it). Per-student payouts are proportional to approved work, with each earning line showing why: tasks, approvals, rate.
- Payment states: pending quality, approved, payable, paid, failed, reversed. Work is only payable after approval.
- Every managed project tracks project value, student payout, Nelavista fee, department share, work status, quality status and payment status.
- A payout provider abstraction with a manual provider first (ops marks batches paid, with export), so the real payout rail, escrow, tax and currency decisions can plug in later. Record any exchange-rate snapshot used.
- The student Earnings screen (web and mobile) and the department share records.
- Daily reconciliation report and alerts on any imbalance.
- Ops slice: payout batches, approval with a second approver for large amounts, ledger explorer, and exports.
- Property-based tests proving that sums always balance, that the 90/8/2 split is exact, and that the department share never reduces the student's 90%.
Acceptance: the PRD's $10,000 example produces $9,000 / $800 / $200 exactly; a reversal leaves a full audit trail; the reconciliation report is clean.

PHASE 7, TALENT PROFILE AND EXTERNAL OPPORTUNITIES
Goal: evidence-based supply side, plus the non-fee opportunities.
Build:
- The Talent profile assembled only from evidence (verified skills, transcript, projects, quality history, work history, availability, academic context), with privacy controls the student owns, and an internal view for ops.
- External opportunities (internships, jobs, scholarships, competitions, events): listed and matched with the same "why you qualify or what's missing" explanation, with no fee logic by default.
- Ops slice: manage and moderate opportunity listings.
Acceptance: the profile shows only evidence-backed items; an external opportunity is matched and explained without touching the ledger.

PHASE 8, ACADEMIA CONNECTED (can start after Phase 1 and run in parallel with a second squad)
Goal: focused fixes that connect the existing Academia experience, and nothing more.
Build:
- Study Materials: students find notes, textbooks and past questions for their own courses without searching (reuse V1's files, metadata and full-text search).
- Ask Nelavista: course-aware and material-aware (port the V1 AI provider abstraction and RAG with the honest-decline rule), so a Mathematics student and a Computer Science student get different help.
- CBT: results show strengths, weaknesses and what to practise next (port V1's scoring and insights), with offline-safe answer saving.
- The existing dashboard answers its five questions and nothing else.
Hard limits: no assignments, no social feeds, no gamification for its own sake, no new academic feature areas.
Acceptance: each of the five dashboard questions has a real, data-backed answer for a seeded student.

PHASE 9, MOBILE RELEASE (iOS AND ANDROID)
Goal: store-ready apps. Most of the mobile work happens inside Phases 0 to 8, and this phase finishes and ships it.
Build and prepare:
- Offline and sync hardening on slow and flaky networks, push notification delivery on both platforms, deep links and universal links on nelavista.com, minimum-version and force-update flow, crash and performance monitoring, and app size and startup time on low-end Android.
- Store readiness: app icons, screenshots, store listings, privacy and data-safety declarations, in-app account deletion, review notes and test accounts, and a check of current Apple and Google policies (verify them rather than relying on memory, especially anything touching payments or earnings).
- Release pipeline: signed builds from tags, staged rollout, beta testing through TestFlight and the Play internal and closed testing tracks, and a rollback path.
Manual steps for me: Apple Developer and Google Play accounts and enrolment, signing credentials, store listings, and any identity or business verification the stores require. List each with lead times.
Acceptance: both apps are installable through the beta channels, pass the smoke suite, and meet the performance budgets on a mid-range Android phone and an older iPhone.

PHASE 10, HARDENING AND LAUNCH
Goal: safe cutover to V2 at nelavista.com.
Build and run:
- Load and soak tests against the scale target, a security review (including object-level authorisation, upload handling, rate limits and admin hardening), backup and restore drill, and a final migration rehearsal on production-like anonymised data.
- Closed beta with a small group, then a pilot with one university cohort and one real managed pilot project (money in test mode or a very small real amount, with my approval).
- Launch plan: feature-flag gating, communication to existing V1 users, support playbook, monitoring and alert thresholds, and on-call.
- The domain cutover per the versioning plan: tag `v1-final`, V1 to v1.nelavista.com, V2 to nelavista.com, version switcher live, OAuth and email-link updates, Search Console, app deep links. Low DNS TTL beforehand, with a written and rehearsed rollback.
Manual steps for me: DNS changes, Google Cloud OAuth changes, Render settings and every other external console. List them in order with exact values.
Acceptance: the launch checklist is complete, the rollback has been rehearsed, and I have approved go or no-go.

AFTER V2 (BACKLOG ONLY, DO NOT BUILD): more skill paths (the content engine from Phase 2 should make these configuration), automated matching at scale, company self-service on top of the existing opportunity, assignment, quality and payout models.

QUESTIONS FOR ME (batch them in the Phase 0 plan, and ask nothing the code can answer)
- The first task types and the source and owner of the AI Data Annotation curriculum. (The 20 learning paths on the website do not include AI Data Annotation, so this content must be created.)
- Currency for client billing and student payouts, the rounding rule for the 90/8/2 split, who approves payouts, and the identity checks required before paying a student.
- The minimum student age and the consent and contributor terms needed before real work starts.
- Team size, who owns which area (to set CODEOWNERS), and the target launch date.
- Whether mobile ships in lockstep with web or one phase behind.

RULES THAT NEVER CHANGE
- V1 stays live and is never modified except by approved security or critical fixes on its own branch.
- Never run anything that touches production data without telling me which database it hits and getting my approval.
- Never print, copy or commit secrets. Never put secrets in an app bundle.
- Do not build anything the PRD says not to build.
- Do not invent facts. Mark assumptions, and verify claims about V1 against its code.
- Small PRs, feature flags, tests with the code, and stop at every gate.

OUTPUT FORMAT
At every gate give: a short summary, what is done and not done, files changed, test results, the demo script, open questions, and the manual steps I must do.
```
