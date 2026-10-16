# 07 — Risk register

Likelihood × impact. Owners are roles, not names. Every row links to its mitigation.

| # | Risk | L | I | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | **Exposed historical credentials not rotated** (OpenRouter ×2, HF, Google keys ×2, Cloudinary secret, Groq, Render DB passwords ×3, real `SECRET_KEY` never set) | H | H | Rotate everything in `docs/SECRETS_ROTATION.md`; gitleaks in pre-commit + CI; secrets only in Render. `.env` not in current history but exposure stands. | founder |
| R2 | **V1 breaks during prep** | L | H | V1 files untouched; relocation deferred to launch (ADR-0004); `pytest tests/` + `check_template_links` on any V1-touching PR. | backend |
| R3 | **Repo size / history** (`.git` 1.3 GB; 1.2 GB materials via LFS + 146 MB un-LFS'd media) | M | M | Written plan only: migrate to Cloudinary, untrack, purge history (needs explicit approval). Never delete `app/static/materials`/`media` before that. | backend |
| R4 | **Single worker / eventlet** | H | M | V2 drops Socket.IO (ADR-0006) so the constraint does not carry; V1 stays single-worker until Redis is funded/added (budget is available per founder). | backend |
| R5 | **No CI; suite too slow to gate** (baseline reached only ~25% in ~16 min) | H | M | Add CI (Phase 3d) with a **fast subset** + full suite nightly; profile and parallelise tests before making the full suite a required check. | backend |
| R6 | **Migration conflict / multiple heads** | M | M | Expand/contract + `alembic heads` check in CI + documented merge procedure (`04`). | backend |
| R7 | **Old mobile binaries calling a changed API** | M | H | API path versioning + min-app-version force-update (ADR-0010). | mobile |
| R8 | **Money correctness** | L | H | ADR-0008 principles (integer minor units, append-only, idempotency, reconciliation). | backend |
| R9 | **dev/prod credential bleed** | M | H | Separate credentials per env; prod-guard on scripts; no prod copy into dev (ADR-0002). | founder |
| R10 | **No Mac for iOS** | H | M | Expo + EAS cloud builds; **start Apple Developer enrolment early**; TestFlight for internal testing (ADR-0001). | mobile |
| R11 | **Store rejection** (account deletion, payments) | M | M | In-app account deletion in all clients; no digital-goods sale, so IAP is not triggered; Data-safety form completed (ADR-0009). | mobile |
| R12 | **`test`/`test123` account in prod** (historical pytest bug) | M | M | Verify and remove; never run debug boot against prod; conftest fix retained. | backend |
| R13 | **Hardcoded domains / debug endpoints in prod** | M | L | V2 derives everything from config; gate `/api/debug-*`; V1 unchanged. | backend |
| R14 | **Scope creep vs 1–3 month window** | M | M | Follow build-first strictly; feature flags for anything unfinished (Phase 3). | founder |

## Standing rules
- Never force-push; never rewrite history without explicit approval.
- Never run seed/maintenance/migration scripts without naming the target `DATABASE_URL`; the prod-guard is the mechanical backstop.
- Any Render/DNS/Google Cloud/Search Console/Apple/Play/EAS change is a **manual step**, listed before doing it.
