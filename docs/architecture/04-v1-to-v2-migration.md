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
- **V1 is not made read-only** (students may still log in to see history), but **new students are directed to V2** and no new V1 features are built.

## Risks & rollbacks

| Risk | Mitigation | Rollback |
|---|---|---|
| Import misfires (duplicates, wrong match) | match by `google_sub` then email; idempotent; dry-run on dev first | drop V2 identity rows, re-run importer |
| V2 breaks at launch | DNS pointer + separate DB; V1 untouched | re-point `nelavista.com` → V1 (≤60 s TTL) |
| Ledger error | append-only + reconciliation job + sandbox in dev | compensating entries; alert on mismatch |
| Old app calls changed API | API path versioning + min-app-version force-update (ADR-0010) | serve old path version |
| V1 regression during prep | V1 files not modified; `pytest tests/` + `check_template_links` before/after any V1-touching PR | revert the PR |

## Explicitly **not** done in this preparation
- No V1 dependency upgrades. No V1 behaviour change. No prod data touched. No forced git-history rewrite. No V1 relocation (deferred to launch, ADR-0004). Materials/Cloudinary move and secrets rotation are **written plans only** (`docs/runbooks/`).
