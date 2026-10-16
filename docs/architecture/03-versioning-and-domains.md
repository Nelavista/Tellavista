# 03 — Versioning, domains and the launch swap

## Rules (from the brief, restated as buildable steps)
- **`nelavista.com` is always the latest version.**
- Older versions live **forever** on their own subdomain: `v1.nelavista.com`, later `v2.nelavista.com`.
- Versions are served from **git tags / release branches**, never duplicated folders.
- One shared file, **`packages/config/versions.json`**, feeds the nav version switcher.

`packages/config/versions.json` (shape):

```json
{
  "current": "v2",
  "versions": [
    { "id": "v1", "label": "V1 (legacy)", "url": "https://v1.nelavista.com", "status": "maintenance" },
    { "id": "v2", "label": "V2 (current)", "url": "https://nelavista.com",   "status": "current" }
  ],
  "mobile": {
    "ios":     { "min_supported": "2.0.0", "latest": "2.0.0", "store_url": "https://apps.apple.com/app/idXXXXXXXX" },
    "android": { "min_supported": "2.0.0", "latest": "2.0.0", "store_url": "https://play.google.com/store/apps/details?id=com.nelavista.app" }
  }
}
```

## Launch-day swap — steps, owners, manual tasks

| # | Step | Owner | Manual? |
|---|---|---|---|
| 1 | Lower DNS TTL on `nelavista.com` to **60 s**; announce freeze window | founder | **Manual (DNS)** |
| 2 | Add `v1.nelavista.com` custom domain to V1's Render service (cert auto-issues) | founder | **Manual (Render)** |
| 3 | Add `v1.nelavista.com` to V1 `SOCKETIO_CORS_ORIGINS` (additive) | eng | No |
| 4 | Register `https://v1.nelavista.com/auth/google/callback` in Google Cloud Console **in addition to** existing URI | founder | **Manual (Google Cloud)** |
| 5 | Verify V1 fully on `v1.nelavista.com` (login, Google, email links, materials, PWA install) | eng + founder | No |
| 6 | Deploy V2 with `nelavista.com`, `api.nelavista.com`, `admin.nelavista.com` | eng | **Manual (Render + DNS for the two subdomains)** |
| 7 | Point `nelavista.com` at V2 | founder | **Manual (DNS)** |
| 8 | Tag **`v1-final`**; create **`release/v1`** | eng | No |
| 9 | Set **Search Console Domain property**; submit V2 sitemap | founder | **Manual (Search Console)** |
| 10 | Keep V1's `nelavista.com` OAuth URI + CORS entry ≥ 30 days | eng | No |
| 11 | Restore normal TTL | founder | **Manual (DNS)** |

**Rollback:** re-point `nelavista.com` to V1's service (≤ 60 s TTL) and take V2 off. V2 DB is separate, so nothing is lost.

## SEO
- `nelavista.com` canonical. **Search Console = Domain property** (covers subdomains).
- **Old versions:** `noindex` (meta + `X-Robots-Tag: noindex`) in V1's headers so `v1.nelavista.com` never competes. They stay human-reachable.
- `robots.txt` + `sitemap.xml` served on `nelavista.com` only.
- **Search Console file:** currently **not served** (audit §5). Fix: serve `/google76268f26b118dad1.html` from the app root on V1 (and carry it to `apps/v1` after relocation) and on V2's public root.

## Cookies
Host-only in both versions (no `SESSION_COOKIE_DOMAIN`, no `.nelavista.com` cookie). Version sessions never share. V2's refresh cookie is host-only too.

## Minimum app version + force-update
Contract in ADR-0010. Operationally:
1. Mobile sends `X-App-Version` + `X-App-Platform` on every request.
2. API reads `mobile.<platform>.min_supported` from `packages/config/versions.json`.
3. Below minimum → `426 Upgrade Required` + `{upgrade:"required", min_version, store_url}`.
4. Clients block with an update screen; **the check runs on launch and on resume** so a stale app cannot silently keep working.
5. To force an update: **raise `min_supported` in the one JSON file and redeploy the API** — one edit, no client release needed.

## Version switcher
`packages/*/VersionSwitcher` reads `packages/config/versions.json` (bundled at build time) and renders the dropdown. Adding a future version = one entry in that file.
