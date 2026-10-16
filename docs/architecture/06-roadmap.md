# 06 — Roadmap

Ordered by the PRD's **build-first / build-later** split (PRD §15). Target: within 1–3 months to launch. Team: 2–3 devs, no Mac.

## Build first

### M0 — Foundation (already scaffolded in Phase 3)
Monorepo, CI, environments, `.env`, local Compose, prod-guard, skeletons with health + hello-world, `versions.json`. **Exit:** green pipeline; `make bootstrap && make dev` works.

### M1 — Identity & Academia core
`identity` (register/login/Google/MFA-for-admin, Argon2, rotation, account deletion), `academia` taxonomy + materials + RAG; V1 importer (P3). **Exit:** a V1 account logs into V2 with the same identity.

### M2 — Skills: Learn → Build → Verify
AI Data Annotation learning path; challenges/projects; **verification** via assessment + practical task + quality; Skill Transcript. **Exit:** a student can become *verified* for AI Data Annotation without watching a lesson.

### M3 — Match → Work → Quality
`matching` (requirements, gaps, eligibility with reasons), `work` (cohort, assignment, submission), `quality` (review workflow, quality record feeding verification). **Exit:** a managed project can be distributed, submitted and quality-approved.

### M4 — Earn (ledger)
`ledger` per ADR-0008: append-only balanced entries, idempotency keys, statuses, reconciliation. Earnings UI on web + mobile. **Exit:** a project's 90/10/2 split is trackable end to end and reconciles.

### M5 — Internal ops tools
`apps/admin`: run managed projects, quality review queue, audit. **Exit:** the team can run a project end to end without DB access.

### M6 — Academia focused fixes
Connect Dashboard / Ask Nelavista / CBT to weak-area signals (PRD §3). No new academic feature areas.

### M7 — Mobile (both platforms)
Expo app: auth, Academia reads, Skills journey, work submission with offline queue, push, force-update. **Exit:** TestFlight + internal Android track builds; staged store release.

## Build later (explicitly deferred)
More skill paths; automated matching at scale; **company self-service** (the model must allow it — requirements/assignments/quality/payouts are modelled for it, PRD §9); escrow/taxes/currency/payout rails (PRD §12).

## Cross-cutting (built with, not after)
Offline + idempotency (ADR-0007), observability (Sentry + PostHog per env), feature flags, accessibility + low-data budgets.

## Milestone → ADR/plan references
M0 = ADR-0001/0002, `01-target-structure.md` · M1 = ADR-0005/0009 · M2 = `05-domain-map.md` · M3 = `05`, PRD §6–8 · M4 = ADR-0008 · M7 = ADR-0001/0007/0010.
