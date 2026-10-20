# apps/admin

Internal ops tools for running managed workforces — the team's control room (ADR-0001). **Role-gated server-side** and `noindex`.

Ops is a slice of every phase (the old M5 milestone was retired): import runs,
user lookup, projects/cohorts, quality review and override, payments/ledger, content
management, audit trail and mandatory staff 2FA. See
`docs/build/phase-1-10-plan.md`.

```bash
make admin-dev    # http://localhost:5174
```

Implemented screens live in `src/routes/`; every one is role-gated server-side and
refuses to render for a student account or an unenrolled staff account.
