# ADR-0003 — Versioned domains and the launch-day swap

**Status:** Accepted · **Date:** 2026-10-16

## Context

The rule: **`nelavista.com` is always the latest version.** Older versions live forever on their own subdomains. Today `nelavista.com` is V1 and `v1.nelavista.com` does not exist yet (confirmed 2026-10-16). The swap is **not** part of this task — it is designed and documented here.

V1 is a dynamic app with sessions, Google OAuth, email links, CSP, CORS, Socket.IO, a PWA manifest and (claimed) SEO — so a host change touches all of them (audit §5).

## Decision

### The swap, in order (executed at V2 launch, by the founder + one engineer)

1. **T-7 days:** lower DNS TTL on `nelavista.com` records to **60 s**. Add `v1.nelavista.com` → V1's Render service (new custom domain + managed cert). **No traffic change yet.**
2. **T-1 day:** verify V1 fully works on `v1.nelavista.com` (login, Google sign-in, email links, realtime, PWA install, materials). Add `v1.nelavista.com` to `SOCKETIO_CORS_ORIGINS` **alongside** `nelavista.com`, and register `https://v1.nelavista.com/auth/google/callback` in Google Cloud Console **in addition to** the existing URI.
3. **T-0:** point `nelavista.com` at V2. Deploy V2 with all three of `nelavista.com`, `api.nelavista.com`, `admin.nelavista.com` live.
4. **T+0:** keep V1's `nelavista.com` OAuth URI and CORS entry for **≥ 30 days** (in-flight sessions, cached redirects, old bookmarks).
5. **T+0:** tag V1 **`v1-final`**; create branch **`release/v1`** (security + critical fixes only).
6. **T+7 days:** raise TTL back to a normal value.

**Rollback:** because step 3 is a single DNS/service pointer, rolling back = point `nelavista.com` back at V1's service (TTL 60 s makes this fast) and re-pause V2. V2's database is separate (ADR-0005) so nothing is lost by rolling back.

### Cookies
V1 sets **host-only** cookies (no `SESSION_COOKIE_DOMAIN`) — keep it that way. **Do not** set a `.nelavista.com` cookie domain unless deliberately sharing a session across versions (we are not). V2 must also be host-only, so v1/v2 sessions never collide.

### OAuth
V2's Google client (and the dev client) get their own redirect URIs. Never reuse V1's client. V1's URIs are added for `v1.` and retained on `nelavista.com` for the transition window.

### SEO
- `nelavista.com` is the canonical property. **Search Console is set up as a Domain property** (covers all subdomains).
- **Old versions serve `noindex`** (meta robots + `X-Robots-Tag: noindex`) so `v1.nelavista.com` never competes with `nelavista.com`. They stay reachable for humans, invisible to crawlers.
- Add `robots.txt` and a `sitemap.xml` for `nelavista.com` only.
- The Search Console **verification file** (`google76268f26b118dad1.html`) is currently **not served** (audit §5). Serve it deliberately from V2's public root; on the future V1 relocation, keep serving it there too (ADR-0004).

### Version switcher
A single shared file, **`packages/config/versions.json`**, is the only place versions are declared. A nav dropdown reads it and shows the current + older versions. Adding a future version is a one-line edit.

## Options considered
- **Per-version deploys in the same service with path routing** (`nelavista.com/v1`): rejected — paths are not the rule, subdomains are, and path-scoped cookies/SEO get messy.
- **Duplicated folders per version**: explicitly rejected by the brief; versions come from tags/branches.

## Reversibility
**High** — the swap is a DNS pointer plus additive OAuth/CORS entries. Rollback is minutes.

## Team cost
~1 day of coordination on launch day + ongoing `release/v1` security maintenance. Concrete steps and owners: `docs/architecture/03-versioning-and-domains.md` and `docs/runbooks/domain-switch.md`.
