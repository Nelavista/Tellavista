# ADR-0005 — V2 database and V1 → V2 account/data import

**Status:** Accepted · **Date:** 2026-10-16

## Context

V1 holds real students (password + Google OAuth), the university taxonomy, course data and material metadata. V2 needs one student identity across Academia and Skills and a transactional ledger. V1 must keep running untouched.

## Decision

### Separate databases
**V2 gets its own database.** No shared tables, no shared Alembic history. Reasons: the ledger must not be entangled with V1's schema; V2 migrations must never risk V1 rows; and V1 must be able to roll back the domain swap with zero data impact (ADR-0003).

### One-way import (V1 → V2), no sync back
A repeatable import job copies, **one direction only**:

| V1 source | V2 target | Notes |
|---|---|---|
| `User` (username, email, password hash, `google_sub`, name, university/department/level, `email_verified`) | `identity.user` | Password hash carried **as-is** (Werkzeug PBKDF2 or scrypt) and **rehashed to Argon2 on next successful login**. |
| `University`, `Faculty`, `Department`, `Course`, `Topic` | `academia.*` | Taxonomy is the backbone of both paths. |
| `Material` metadata (title, course/topic links, `file_url`) | `academia.material` | **Metadata only** — files stay where they are until the Cloudinary plan runs. |
| `CbtQuestion` banks | `academia.question` | Course-code-keyed banks. |
| `StudentSkill`, `Cohort`, `Opportunity*`, `Rating`, `GradingEvent` | skills/work domains | **Semantics reused, schema redesigned** — do not copy rows blindly (audit §9). |

**Not imported:** Community, live-meeting rooms, reels, Social, message threads, sessions, AI conversation history. V2 has no Community product (PRD §2).

### Identity mapping rules
- **Match by `google_sub` first**, then by lowercased email.
- A V1 account with **no usable password and no `google_sub`** is imported as an account requiring a **password reset** on first use.
- **Idempotent**: the importer keys on email/`google_sub` and can be re-run safely. It never writes to V1.
- The import is a **script, not a migration**, and is **prod-guarded** (ADR-0002): it reads V1 (read-only) and writes to V2.

### Per-feature cutover
Students are not forced to switch at once. V1 stays live at `v1.nelavista.com`; V2 launches at `nelavista.com`. Accounts created only on V2 (post-launch) have no V1 row — the importer runs to cover pre-launch accounts and can be re-run for stragglers.

## Options considered
- **Share V1's database with V2**: rejected (couples rollback and ledger integrity; V1 schema is not suitable).
- **Force everyone to re-register**: rejected (loses identity and trust; the brief requires one identity).

## Reversibility
**High** — a separate DB can be dropped and the import re-run. Nothing in V1 is modified by the import (read-only reads).

## Team cost
~2 days to write and test the importer + rehash-on-login. Ongoing: run it once at launch, then quarterly for stragglers.
