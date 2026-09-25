# Nelavista — Legacy → Target Migration Map

**Status:** Stage 0 deliverable, complete.
**Source prompt:** *Nelavista Master Build Prompt v1.0*
**Legacy app:** `Tellavista` (Flask + Jinja), main branch
**Written:** 2026-09-25

This is the one-time inventory Section 1 requires before any new code is written. It maps
every existing route module and model class onto the PRD's target module structure and data
model, and records which PRD requirements are already met, partially met, or genuinely
missing. Nothing here is a proposal to build — it is a factual map of what exists.

---

## 1. Decision log

**Decision: keep Flask + Jinja and close the gaps, instead of executing the Section 1
full-stack rewrite.**

Recorded rationale, so this isn't relitigated every session:

- Section 1 **contradicts itself**. One bullet reads *"Do NOT attempt a live in-place rewrite
  of Flask routes — rebuild against the PRD's data model from scratch"*; the bullet three lines
  later reads *"Once feature parity is reached for a module, retire the corresponding Flask
  route/template."* The first is a greenfield rewrite, the second is a strangler-fig migration.
  They cannot both be the plan. The strangler-fig reading is the one that keeps the product
  shippable, so it wins.
- The PRD's binding scope (Sections 8–24) is **feature scope**, not stack scope. Every P0
  acceptance criterion in Section 5.1–5.9 is a backend/data property. Replacing Jinja with
  React moves none of them.
- 15 of the 20 Data Model entities in PRD §16 **already exist** (§3 below). A from-scratch
  rebuild discards working implementations of auth, onboarding, the material pipeline, the CBT
  engine, and the AI tutor — plus 36 test suites that already assert the PRD's acceptance
  criteria (`test_cbt_integrity.py`, `test_tutor_academic_scoping.py`,
  `test_ai_grading_injection_defense.py`, `test_auth_security.py`, `test_materials_scoping.py`).
- The genuine gaps the PRD exposes (§6 below) are backend and data problems. They are
  addressable without a rewrite.

**Consequence:** the target stack table in Section 1 is **not adopted as-is**. React/Vite/TS
and the FastAPI rewrite are dropped. Infrastructure choices that serve a real gap (pgvector,
Sentry, PostHog, ARQ) are still on the table — see §7.

---

## 2. Legacy inventory

| Metric | Count |
|---|---|
| Python LOC in `app/` | 18,242 |
| Route modules (`app/routes/`) | 25 files, 9,407 LOC |
| Registered routes | ~289 |
| Model classes (`app/models.py`) | 68 |
| Jinja templates (`app/templates/`) | 89 |
| Test suites (`tests/`) | 36 |
| Alembic migrations (`migrations/versions/`) | 45 |
| Service modules (`app/services/`) | 19 |
| Flask blueprints | 24 |
| `frontend/` | empty scaffold — no `package.json`, empty `src/` |

The `frontend/` directory is inert. It holds no code and nothing imports it.

---

## 3. PRD §16 data model → existing schema

Legend: **Present** = usable as-is · **Partial** = exists but diverges from the PRD shape ·
**Missing** = no equivalent · **Verify** = exists, shape not yet confirmed

| PRD §16 entity | Legacy equivalent | Status | Notes |
|---|---|---|---|
| `User` | `User` | Present | Adds `google_sub` (stable OIDC `sub`, not email), `is_admin`, `is_employer`, `preferred_path`, `is_deleted` |
| `UserProfile` | `User` (inline columns) | Partial | Profile is inline on `User` (`name`, `bio`, `profile_photo_url`, `university_id`, `department_id`, `user_level`), not a separate 1:1 table |
| `University` | `University` | Present | Has `slug`, `active` flag, `location`, `logo_url`; auto-slug listener on insert |
| `Faculty` | `Faculty` | Present | Scoped per-university, `uq_faculty_university_name` |
| `Department` | `Department` | Present | `uq_department_faculty_name` |
| `AcademicSession` | — | **Missing** | No table. No free-text column either |
| `Semester` | — | **Missing** | `User.semester` and `Course.semester` are free-text strings with no shared vocabulary |
| `AcademicCourse` | `Course` | Present | `uq_course_dept_level_code`; has `source` to distinguish registrar data from `nuc_ccmas_core` |
| `AcademicTopic` | `Topic` | Present | Has `order`, `explanation`, admin-pinned `video_url` |
| `AcademicMaterial` | `Material` | Present | Scoped by `university` with NULL = universal (same pattern as `CBTQuestion`) |
| `Enrollment` | `StudentOnboarding`, `CohortEnrollment` | **Partial** | No user↔course enrollment row carrying session/semester. `CohortEnrollment` is a different concept (cohort grouping) |
| `Progress` | `TopicProgress`, `MaterialView` | **Partial** | `TopicProgress` is boolean-only (`completed_at`), missing the PRD's `mastery_score` and `last_activity_at`. `MaterialView` is a one-row-per-(user,material) visit tracker |
| `Quiz` | `Quiz` (Skills), CBT subject grouping (Academia) | **Partial** | Two unrelated engines. Academia has no `Quiz` container row — `CBTAttempt.course_code` is a **free string, not an FK to `Course`** |
| `Question` | `CBTQuestion`, `Quiz.question` | Present | `CBTQuestion` supports MCQ + written, with `mark_scheme` |
| `QuizAttempt` | `CBTAttempt`, `StudentQuizAttempt` | Present | `CBTAttempt` snapshots `issued_question_ids_json` so a client can't inject or substitute question IDs |
| `QuizAnswer` | `CBTAnswer`, `StudentAnswer` | Present | Answers snapshot `question_text` at submit time, so later bank edits don't rewrite past results |
| `AIConversation` | `TutorConversation` | Present | Already carries `course_id` / `topic_id` / `material_id` |
| `AIMessage` | `TutorMessage` | Present | `role` is `user`/`assistant` only; system prompt rebuilt per-request from live context rather than stored |
| `Notification` | `Notification` | Present | Real service layer (`services/notification_service.py`), consumed by both Academia and Skills |
| `AdminUser` | `User.is_admin` + `AdminAuditLog` | **Partial** | Boolean flag, no role/permission table. No `instructor` role exists |

**Bottom line:** 15 present, 5 partial/missing. The five that matter:
`AcademicSession`, `Semester`, `Enrollment`, `Progress.mastery_score`, and a real
academia-side `Quiz` container with an FK to `Course`.

---

## 4. PRD §13 module structure → legacy route modules

Target modules from PRD §13: `core`, `auth`, `users`, `academics`, `courses`, `materials`,
`assessments`, `ai`, `progress`, `notifications`, `analytics`.

| Legacy module | Routes | Maps to target module | Notes |
|---|---|---|---|
| `core_routes.py` | 4 | `core` | Landing, `/images/<filename>` |
| `static_pages_routes.py` | 4 | `core` | About / privacy / terms / support |
| `pwa_routes.py` | 2 | `core` | Manifest + service worker |
| `auth_routes.py` | 10 | `auth` | Register, login, logout, Google OAuth, verify email, forgot/reset password |
| `profile_routes.py` | 1 | `users` | |
| `settings_routes.py` | 7 | `users` | Includes account deletion (anonymise + deactivate, not hard delete) |
| `academia_routes.py` | 7 | `academics` + `notifications` | Taxonomy browse, academia notification list |
| `admin_academia_routes.py` | 17 | `academics` (admin) | University→Faculty→Department→Course→Topic CRUD |
| `materials_routes.py` | 11 | `materials` | Upload, browse, view, profile completion |
| `study_routes.py` | 4 | `materials` | Study mode |
| `video_routes.py` | 9 | `materials` | YouTube search, shared with Skills via `services/youtube_service.py` |
| `google_search_routes.py` | 2 | `materials` | Tavily-backed external material search (`services/google_search_service.py`) |
| `cbt_routes.py` | 9 | `assessments` | Start / submit / history / summary |
| `ai_routes.py` | 14 | `ai` | Notes, test generation, grading, project briefs, lesson generation |
| `tutor_routes.py` | 8 | `ai` | Streaming tutor chat, conversation threads |
| `dashboard_routes.py` | 6 | `progress` | |
| `admin_routes.py` | 17 | `analytics` + `users` (admin) | Admin home, analytics view, audit |
| `campus_map_routes.py` | 7 | `core` | **Not in PRD.** Campus map + locations |
| `reels_routes.py` | 2 | — | **Not in PRD.** Short-form video |
| `community_routes.py` | 14 | — | **Out of scope (§14).** Groups, chat, events |
| `live_meeting_routes.py` | 14 | — | **Out of scope (§14).** Video meetings, Phase 3+ |
| `employer_routes.py` | 4 | — | **Out of scope (§14).** Employer profiles |
| `skills_routes.py` | 48 | — | **Out of scope (§14).** Skills marketplace, gigs, earnings, competitions |
| `admin_skills_routes.py` | 66 | — | **Out of scope (§14).** Admin surface for the above |

`notifications` has no dedicated route module — notification lists are served inside
`academia_routes.py` and `skills_routes.py`, over a shared `Notification` model and service.

---

## 5. Out-of-scope surface already built

PRD §14 lists what must not be built for MVP. Roughly **146 of ~289 routes (~50%)** are
functionality the PRD places outside MVP scope, and it is fully implemented:

| Domain | Routes | PRD §14 phase |
|---|---|---|
| Skills marketplace / gigs / earnings | 114 (`skills_routes` + `admin_skills_routes`) | Phase 3–4 (marketplace, escrow, payouts) |
| Community groups / chat / events | 14 | Not in MVP scope |
| Live video meetings | 14 | Phase 3+ |
| Employer profiles | 4 | Phase 3 |

This is a **product decision, not a bug** — the legacy build went further than the PRD's MVP.
It must not block MVP work, and per §14 it should not be extended further. Options for the
product owner: freeze as-is, keep maintaining, or retire behind a feature flag. Do not delete
without a decision; `Notification`, `AdminAuditLog`, and several services are shared with
in-scope Academia code.

---

## 6. Gap analysis — P0 features, PRD §9

### Genuinely missing (must be built)

| # | Gap | PRD ref |
|---|---|---|
| G1 | **No RAG — but less missing than it looks.** Text extraction already exists and is cached (`services/material_service.py` uses pdfplumber/PyMuPDF, caching into `Material.extracted_text` + `extracted_at`). What's actually missing is the RAG half: chunking, embeddings, vector storage, and semantic retrieval. No `pgvector` usage, no chunk table. | §5.5, §6 |
| G2 | **No `AcademicSession` / `Semester` / `Enrollment`.** Session and semester are unvalidated free-text strings on `User` and `Course`. | §16 |
| G3 | **No provider-agnostic AI layer.** The OpenRouter endpoint URL is hardcoded in **13 places** in `services/ai_service.py` alone, plus `tutor_service.py`, `ai_grading.py`, and 4 route modules. No `AIProvider` interface. | §6 |
| G4 | **No queued/background jobs.** No ARQ. Long AI generations run inside the request. | §19, §21 |
| G5 | **No PostHog. Sentry is already fully wired** — `logging_config.py` initializes `sentry_sdk` whenever `SENTRY_DSN` is set, with `FlaskIntegration` + `LoggingIntegration` (ERROR events) and `SENTRY_TRACES_SAMPLE_RATE` for latency tracing. It needs the DSN configured, not new code. PostHog (funnels, retention, feature usage) is genuinely absent. | §21 |
| G6 | **No AI usage/cost instrumentation.** No token or cost tracking per user or feature. | §21 |
| G7 | **Keyword search is `ILIKE`, not Postgres full-text search.** `materials_routes.py:410` does three `ilike` ORs. No `to_tsvector` anywhere. | §5.3, §21 |
| G8 | **No resume position.** `MaterialView` stores `(user_id, material_id, viewed_at)` — no page or scroll offset. "Continue learning" can return to the material but not to the position. | §5.3 AC |
| G9 | **No `mastery_score`.** `TopicProgress` is boolean completion only; there is no per-topic mastery signal for recommendations to read. | §16, §21 |
| G10 | **Flagged-answer moderation queue** does not exist. Hallucination logging has no destination. | §6, §8 |
| G11 | **Access-token + refresh rotation.** Auth is a Flask session cookie. | §5.1, §7 |
| G12 | **`CBTAttempt.course_code` is a free string**, not an FK. Blocks reliable per-course performance rollups. | §16 |

### Already present (do not rebuild)

| Requirement | Where it lives |
|---|---|
| Email + password registration with verification gating | `auth_routes.py`, `User.email_verified` |
| Google OAuth sign-in | `User.google_sub`, `test_google_oauth_flow.py` |
| Password recovery via emailed, hashed, expiring token | `auth_routes.py`, `User.reset_token_hash` |
| Academic hierarchy CRUD + browse | `academia_routes.py`, `admin_academia_routes.py` |
| Timed CBT with auto-submit, immediate scoring, history | `cbt_routes.py`, `test_cbt_integrity.py` |
| Answer-injection defence on CBT submit | `CBTAttempt.issued_question_ids_json` |
| AI tutor with auto-injected academic context + threads | `tutor_service.py`, `test_tutor_academic_scoping.py` |
| Prompt-injection defence in AI grading | `ai_grading.py`, `test_ai_grading_injection_defense.py` |
| Per-route AI rate limiting | `extensions.py` `Limiter`, `@limiter.limit` on 8+ AI routes |
| Deterministic weak/strong topic detection (partial) | `services/progress_service.py` |
| Notifications (in-app), audit logging, RBAC via `is_admin` | `notification_service.py`, `AdminAuditLog` |
| Secrets via env only, CORS allow-list, upload validation | `config.py`, `__init__.py` |
| Material scoping so students only see in-scope content | `test_materials_scoping.py`, `test_academic_scoping_ai_actions.py` |
| Structured logging + Sentry error tracking (activates on `SENTRY_DSN`) | `logging_config.py`; `sentry-sdk[flask]` already in `requirements.txt` |
| PDF text extraction with a DB cache | `services/material_service.py`, `Material.extracted_text` / `extracted_at` |

### Diverges from the PRD (decide, don't silently "fix")

| Item | Current | PRD | Note |
|---|---|---|---|
| Password hashing | `werkzeug.security.generate_password_hash` (PBKDF2-SHA256) | bcrypt/argon2 | PBKDF2 is adaptive and not plaintext, but §7 names bcrypt/argon2. Migration must be rehash-on-login |
| Rate limiting key | Per-IP (`get_remote_address`) | Per-user **and** per-IP | Shared campus NAT makes per-IP alone too coarse |
| Progress states | Binary complete/not | `mastery_score` + `last_activity_at` | |
| Design system | 4 hand-written CSS files (`main.css`, `auth.css`, `landing.css`, `skills.css`) | Tailwind tokens on the PRD palette | Tailwind tokens are adoptable via CSS custom properties without a framework swap |

---

## 7. Sequenced plan

Ordered by dependency. Each step names its PRD section and the acceptance criteria it moves.

**Step 1 — Migration map** *(this document)*. Complete.

**Step 2 — Verify platform prerequisites. RESOLVED.** Checked against Render's supported-
extensions docs: `pgvector` is available on **all** Render Postgres databases running
PostgreSQL 13 or later — there is no plan/instance-size restriction, and it does not require a
background worker. It is enabled per-database with `CREATE EXTENSION vector;`, so it must be
added by migration, not assumed present. No external vector store is needed. Two further
extensions are confirmed available and useful for Step 6: `pg_trgm` (index-backed fuzzy/
substring matching, which also speeds up the existing `ILIKE` queries) and `unaccent`.

*Still open:* whether the Redis instance is provisioned — it remains optional until a second
gunicorn worker exists, but §19/§21's background-job and AI-cost work (Step 8) depends on it.

**Step 3 — Missing data model (G2, G9, G12).** Add `academic_sessions`, `semesters`, and an
`enrollments` table; add `mastery_score` + `last_activity_at` to `TopicProgress`; add a
nullable `course_id` FK to `CBTAttempt` backfilled from `course_code`. One Alembic migration,
additive only, no destructive column drops. *§16.*

**Step 4 — Provider-agnostic AI layer (G3).** Introduce the `AIProvider` interface with an
`OpenRouterProvider` implementing today's behaviour, then collapse the 13+ duplicated
`requests.post` call sites onto it. Pure refactor: no behaviour change, and the existing AI
test suites must stay green. *§6.*

**Step 5 — pgvector RAG (G1).** Extraction → chunking → embeddings → vector storage →
semantic search → context injection. Chunk metadata carries material/page so citations can be
added later without a schema change. Retrieval must enforce the **same** academic-scope rules
as material viewing, reusing the existing scoping helpers. *§5.5, §6.*

**Step 6 — Search + resume position (G7, G8).** Move material search to Postgres FTS; add
page/offset to `MaterialView` for true "Continue learning". *§5.3.*

**Step 7 — Deterministic recommendations (G9).** Implement the PRD's explicit rules
(`IF quiz_performance(topic) < threshold → RECOMMEND revision_material(topic)`) as pure
functions over `mastery_score`. No ML. Feeds dashboard Section 3. *§5.8, §5.9, §21.*

**Step 8 — Observability (G5, G6).** Set `SENTRY_DSN` (the integration already exists and self-activates on it — no code needed), add PostHog, and add AI token/cost tracking. *§21.*

**Step 9 — Security + test hardening (G10, G11, §7).** Rehash-on-login to argon2, per-user
rate limiting, flagged-answer moderation queue, signed time-limited material URLs. *§7, §8.*

**Step 10 — Evaluation suites (§13).** AI eval set per course, RAG retrieval
precision/recall against a labelled question set, load tests on dashboard / tutor / CBT submit.
These are what make "100% MVP complete" (§15) verifiable rather than asserted.

Explicitly deferred: everything in PRD §14 (§5 above), plus React/Tailwind/FastAPI adoption.

---

## 8. Open questions for the product owner

1. **Out-of-scope surface (§5):** freeze, maintain, or retire the 146 marketplace/community/
   live-meeting routes? This is a product call with real cost either way.
2. **~~pgvector~~ Resolved:** available on all Render Postgres 13+ instances, no plan change
   needed. Only remaining check is confirming the live database's actual PostgreSQL version.
3. **The ~146 out-of-scope routes** cover product areas the PRD defers to Phase 3–4. If those
   phases have actually started, the PRD version in hand is stale and the scope needs
   re-baselining before Step 3.
4. **`mastery_score` semantics:** sourced from CBT/quiz results only, or also material
   completion and tutor engagement? The PRD does not define the formula.
