# Architecture Decision Records

Phase 1 of the Nelavista V2 preparation. Each ADR gives the options considered, the decision, its trade-offs, how reversible it is, and the team cost. They are written to be **decision-oriented**, not exhaustive.

Read `docs/architecture/00-audit.md` first — every decision here is grounded in what the audit found in the code, not in the README.

| # | Decision | Status |
|---|---|---|
| [0001](0001-v2-stack.md) | V2 stack and monorepo layout | Accepted |
| [0002](0002-environments-and-hosting.md) | LOCAL / DEV / PROD separation, hosting, secrets, prod-guard | Accepted |
| [0003](0003-versioned-domains.md) | Versioned domains and the launch-day swap | Accepted |
| [0004](0004-v1-in-repo.md) | Where V1 lives in the repo | Accepted |
| [0005](0005-accounts-and-data.md) | V2 database and V1 → V2 account/data import | Accepted |
| [0006](0006-realtime.md) | Realtime: keep / replace / drop V1 Socket.IO | Accepted |
| [0007](0007-offline-and-low-data.md) | Offline and low-data strategy | Accepted |
| [0008](0008-ledger-principles.md) | Money ledger principles | Accepted |
| [0009](0009-auth-multi-client.md) | Auth for web, mobile and admin | Accepted |
| [0010](0010-api-versioning-and-force-update.md) | API versioning vs product versions, min app version, force-update | Accepted |

**Status values:** Proposed · Accepted · Superseded by ADR-XXXX.
