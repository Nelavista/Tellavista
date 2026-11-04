# 04 — V1 → V2 migration plan

V1 is live and must never break. V2 is a **new app** that takes the domain at launch; V1 moves to `v1.nelavista.com` and then receives **security and critical fixes only** on `release/v1`.

## Sequenced steps

| Phase | Step | Gate |
|---|---|---|
| P1 | V2 API skeleton + identity module (health, APP_ENV, auth). | CI green |
| P2 | V2 DB migrations (identity, academia taxonomy) — **expand/contract**. | Migration check green |
| P3 | V1 → V2 importer (users, taxonomy, material metadata) — read-only on V1, **prod-guarded**. | Import dry-run on dev |
| P4 | Web + mobile "hello world" against the API; auth flows working end to end. | Manual QA on dev |
| P5 | Skills journey for **AI Data Annotation**: learn → build → verify → match → work → quality → earn. | Acceptance on dev |
| P6 | Internal ops tools (run managed projects, quality review) + **earnings ledger**. | Ledger reconciliation green |
| P7 | Focused Academia fixes (connect Dashboard/Ask Nelavista/CBT — PRD §3). | Regression on dev |
| P8 | **Launch swap** (ADR-0003/`03-versioning-and-domains.md`). | Founder approves |
| P9 | Post-launch: V1 security-only; retire V1 surface the PRD drops (Community, live classes, reels) behind flags or remove at V2 only. | — |

## Expand/contract migration rules (multi-developer)
- **Expand:** add nullable columns/tables, deploy, backfill in a job. **Never** make a column NOT NULL or drop it in the same release that stops writing to it.
- **Contract:** remove old columns/tables in a **later** release, after no code reads them.
- **Single Alembic head enforced in CI** (`alembic heads` must print exactly one).
- **Conflict procedure:** rebase; if two heads exist, create a merge revision with `alembic merge -m "merge heads" <rev1> <rev2>` and never hand-edit a previously-merged revision.

## V1 maintenance policy (after launch)
- V1 is **frozen** except security and critical bugs, on `release/v1`.
- Deploys to `v1.nelavista.com` come **only** from `release/v1`.
- **V1 is not made read-only** (students may still log in to see history), but **new students are directed to V2** and no new V1 features are planned after the swap. Note: V1 `main` did receive new features before this plan was executed; see the next section.

## V1 additions after this plan (2026-11-04)

V1 `main` received new work after the migration plan was written. V1 and V2 have
separate databases and migration heads, so these commits do not conflict with V2
migrations. They do change what "bring V1's content across" means.

| V1 addition | V1 schema / content | V2 impact |
|---|---|---|
| African Languages Lab (ALL) | Migration `d7a3c5e81f42` adds `skill_categories.program`, `skills.language`/`tags_json`, `challenges.task_spec_json`/`is_assessment`/`pass_score`, `challenge_submissions.score`/`result_json`, `user.language_background` and `student_languages`. Content is seeded by `scripts/seed/seed_all_skills.py` from `seed_data/all_skills/`. | V2 has no equivalent columns or content. Do not run the V1 seeder against V2 tables; port the curriculum through a V2 seed after adding the V2 fields. |
| Language profile | Self-reported languages and capabilities; verification is derived from verified language-specific skills. | V2 identity/skills need an equivalent; it must keep self-reported and verified separate. |
| Structured task scoring | Deterministic transcription/translation/labeling/recording scoring and an assessment gate. | V2 assessment grading is deterministic for gold tasks, but its task templates do not model these four kinds or WER/chrF. Map them into the V2 model rather than importing V1 submissions. |
| Impact page | Public static `/impact`, landing band, footer link. | No database change. Add to the V2 public surface only after its metrics are verified; otherwise keep it out. |
| FUTA official taxonomy | Schools/departments and 35 Surveying & GeoInformatics courses with `Course.semester` and `Course.source = 'futa_official'`; a cleanup script for unlisted departments. | V2's `Course` model has no `semester`, `course_type`, `description` or `source`, and `services/imports/v1.py` does not carry them. Add the fields and importer support before importing this taxonomy, or seed it natively. |
| AI grading hardening | `wrap_untrusted()` escapes student-supplied `<student_content>` delimiters. | Apply the same boundary to V2 Ask/practice AI prompts; V2 assessment grading is deterministic. |
| Test speed | Test-only SQLite pragmas. | Not a schema or production change; V2 has its own fixtures. |

**Sequencing rule:** if V2 ports ALL, do it as an expand/contract migration:
add nullable columns/tables and the seed first, backfill, then enforce constraints
in a later release. Keep the V1 export read-only. Do not make a V1 table change and
a V2 schema change in the same PR.

**Migration head note:** V1's head moved from `f1b2c3d4e5f6` to
`d7a3c5e81f42`. That is a V1-only fact; V2 still enforces its own single Alembic
head (`20261022_1000` at the time of writing).

## Risks & rollbacks

| Risk | Mitigation | Rollback |
|---|---|---|
| Import misfires (duplicates, wrong match) | match by `google_sub` then email; idempotent; dry-run on dev first | drop V2 identity rows, re-run importer |
| V2 breaks at launch | DNS pointer + separate DB; V1 untouched | re-point `nelavista.com` → V1 (≤60 s TTL) |
| Ledger error | append-only + reconciliation job + sandbox in dev | compensating entries; alert on mismatch |
| Old app calls changed API | API path versioning + min-app-version force-update (ADR-0010) | serve old path version |
| V1 regression during prep | V1 files not modified; `pytest tests/` + `check_template_links` before/after any V1-touching PR | revert the PR |
| V2 launches without V1's newest features (ALL, Impact, FUTA) | Port the delta or record an explicit drop in `PARITY.md`; gate the `develop` → `main` merge on that decision | keep V1 live at `v1.nelavista.com` until V2 reaches parity |

## Explicitly **not** done in this preparation
- No V1 dependency upgrades. No V1 behaviour change. No prod data touched. No forced git-history rewrite. No V1 relocation (deferred to launch, ADR-0004). Materials/Cloudinary move and secrets rotation are **written plans only** (`docs/runbooks/`).
