# Runbook — Domain switch (V1 → V2 at launch)

> Executed once at V2 launch. Full decision: ADR-0003 · Steps/owners: `docs/architecture/03-versioning-and-domains.md`. **Do not run before the V2 launch.**

## Preconditions
- [ ] V2 fully QA'd on DEV; acceptance signed off.
- [ ] `v1.nelavista.com` resolves to V1 and everything works there.
- [ ] Search Console is set as a **Domain property**.
- [ ] All manual steps below confirmed with the founder.

## The switch (with rollback at each point)
| # | Step | Manual? | Rollback |
|---|---|---|---|
| 1 | Lower DNS TTL on `nelavista.com` to **60 s** (T-7d) | **DNS** | raise it back |
| 2 | Add `v1.nelavista.com` → V1 service | **Render + DNS** | remove record |
| 3 | Add `v1.nelavista.com` to V1 `SOCKETIO_CORS_ORIGINS` | No | revert commit |
| 4 | Register `v1.nelavista.com/auth/google/callback` **in addition** to existing | **Google Cloud** | remove URI |
| 5 | Verify V1 on `v1.nelavista.com` end to end | No | — |
| 6 | Deploy V2 with `nelavista.com`, `api.nelavista.com`, `admin.nelavista.com` | **Render + DNS** | take V2 down |
| 7 | Point `nelavista.com` → V2 | **DNS** | point back to V1 (≤60 s) |
| 8 | Tag `v1-final`, create `release/v1` | No | — |
| 9 | Set Search Console Domain property; submit V2 sitemap | **Search Console** | — |
| 10 | Keep V1's `nelavista.com` OAuth URI + CORS for ≥30 days | No | — |

## Cookies
Both versions are **host-only** (no `.nelavista.com` domain cookie). Do not add one — it would blur version sessions (ADR-0003).

## SEO
`nelavista.com` is canonical. **Old versions serve `noindex`.** `robots.txt` + `sitemap.xml` only on `nelavista.com`.

## Verify after
Login/lockout, Google sign-in, an email link, realtime (V1), PWA install, materials download, a V2 write, Search Console coverage.

## Emergency
Point `nelavista.com` back at V1 (60 s TTL). Nothing is lost — V2 has its own database (ADR-0005).
