"""V2 domain models. One module per domain, mirroring app/api/v1/domains.

Phase 0 (M0) built `identity`, `admin`, `academia`, `skills`, `verification`,
`matching`, `work` and `jobs`. The later phases add the tables they own:

* `quality`  — the standard, reviews, rolling score and consequences (M5).
* `ledger`   — append-only money, earnings, payouts, reconciliation (M6).
* `talent`   — evidence-backed profile sharing and external applications (M7).
* `ops`      — import receipts, campus utility, university waitlist (M1).
* `engagement` — notifications and assignment-scoped messages (M5/M9).

Nothing is exposed to a client until its router is mounted behind a feature flag.
"""
