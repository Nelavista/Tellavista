# ADR-0008 — Money ledger principles

**Status:** Accepted · **Date:** 2026-10-16
**Scope:** principles only — **no schema here.** Money must be correct on day one; a schema decided before the principles will be wrong.

## Context

For managed paid work the split is fixed (PRD §12): the **client pays Nelavista**; the student receives **90%**; Nelavista keeps **10%**, of which **20% (2% of the total) goes to the student's participating department** — always **out of Nelavista's fee, never out of the student's 90%**. Every managed project must track: **project value, student payout, Nelavista fee, department share, work status, quality status, payment status** (PRD §12). Escrow, taxes, currency and payout rails are deliberately undecided (PRD §12).

## Principles (binding)

1. **Integer minor units only.** All money is stored as integers in the smallest currency unit (kobo, cents). **No floats, ever** — not in the DB, not in the API, not in the client. Serialise as `{amount_minor, currency}`.
2. **Append-only.** Ledger entries are **never updated or deleted**. A correction is a **new, compensating entry** that references the original. Balances are **derived by summing entries**, not stored as a mutable column (a cached balance may exist only as a rebuildable projection).
3. **Every entry is balanced.** Each business event writes a **set of entries that nets to zero** across accounts (client/escrow, student-payable, platform-fee, department-payable, payout-cleared). The three-way split is three postings, not one number.
4. **Idempotency keys on every money mutation.** Replaying a payout or a fee posting must be a no-op, exactly like ADR-0007's writes. Keys are server-issued and unique per business event.
5. **Immutable audit trail.** Every entry records **who/what/when**: actor (student, admin, system), the source document (project, assignment, submission, quality review), and a reason string. Nothing money-related changes without a trace.
6. **Statuses are explicit and separate.** *Work status*, *quality status* and *payment status* are **three different fields** on a project/assignment (PRD §12). Never overload one field to mean all three.
7. **No money moves on unverified quality.** Payout is only authorised from a `quality_approved` state (PRD §7). The quality review is a first-class workflow, not a flag.
8. **Currency is explicit on every amount.** Even if only NGN ships first, the field exists from the start (PRD leaves currency open).
9. **Adjustments are first-class.** Disputes, clawbacks and re-verification consequences are entries like any other, never silent edits.
10. **Reconciliation is a scheduled job.** A daily job re-derives balances from entries and alerts on any mismatch — the same alert path as monitoring.
11. **Sandbox/real separation.** dev uses sandbox keys; **no code path may move real money when `APP_ENV != prod`.**

## Options considered
- **Store balances as columns**: rejected — mutable state on money is how ledgers drift.
- **Single "payout" row per project**: rejected — it cannot express the department share as a separate obligation, nor support corrections.

## Reversibility
**High** — these are principles; they constrain the eventual schema (see `docs/architecture/05-domain-map.md`) but add no runtime dependency.

## Team cost
~0 foundation cost (it is a design rule). The eventual ledger schema builds on it; a reconciliation job adds ~1 day and is part of the "earnings ledger" build-first slice (PRD §15).
