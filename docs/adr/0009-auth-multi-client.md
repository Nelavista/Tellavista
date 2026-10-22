# ADR-0009 — Auth for web, mobile and admin

**Status:** Accepted · **Date:** 2026-10-16

## Context

V1 auth is a **Flask server-side session cookie** holding `session['user']`; Google sign-in is the **web Authorization-Code flow** (Authlib) with server-side state and a **host-derived redirect URI**. The audit (§6) found this is **unusable for native apps**: no token, no refresh, no way to do Google sign-in from iOS/Android. V2 has four clients: web, iOS, Android, admin — all needing one identity.

## Decision

### One identity service, three client flows

**Tokens:** short-lived **access token (JWT, ~15 min)** + rotating **refresh token (opaque, ~30 days, single-use)**. Refresh **rotation with reuse detection** (a replayed refresh token revokes the family).

| Client | Access token stored | Refresh token stored | Login |
|---|---|---|---|
| **Web** | in memory | **httpOnly, Secure, SameSite=Lax cookie** (host-only, no `.nelavista.com` domain — ADR-0003) | email+password; **Google via server-side Authorization-Code flow** (same as V1) |
| **Mobile (iOS/Android)** | in memory | **`expo-secure-store`** (Keychain / Keystore) | email+password; **Google via `expo-auth-session` + PKCE** (system browser / Custom Tabs), **native Google client IDs** |
| **Admin** | in memory | httpOnly cookie **+ mandatory MFA** | email+password + MFA; **Google sign-in disabled**; IP allowlist optional |

### Details
- **CSRF:** web/admin keep a CSRF token for cookie-authenticated mutations. Native uses bearer tokens and needs no CSRF.
- **Google native:** the app obtains an **ID token** via the platform Google SDK/PKCE; the **API verifies the ID token's signature, audience, issuer and expiry** and matches/link by `google_sub`. Never trust an unverified email claim (same rule as V1's OAuth callback).
- **Logout:** revokes the refresh-token family server-side; client clears both tokens.
- **Password hashing:** **Argon2id**. V1's Werkzeug hashes (PBKDF2 or scrypt) are verified on first login and **rehashed** (ADR-0005).
- **Rate limiting:** per-user (as V1 fixed) **and** per-IP on login/signup/reset.
- **Email verification / reset:** same token model as V1 (only the hash stored, single active token, expiry), links built from configured base URL — **not** `request.host_url`, so the link is correct per environment (ADR-0002).
- **Store requirements:** because both stores require **in-app account deletion** (Apple 5.1.1(v); Google Play Data-safety/account-deletion), account deletion is a **first-class endpoint** available in every client, mirroring V1's anonymise-and-deactivate behaviour.

### V1 account import fit
V1 accounts import with their Werkzeug hash (PBKDF2 or scrypt) and `google_sub`; the first successful login upgrades the hash. No forced password reset except for accounts with neither a usable hash nor `google_sub`.

## Options considered
- **Keep session cookies for everything**: rejected — cannot serve native apps.
- **Third-party identity provider (Auth0/Clerk/Supabase Auth)**: viable, but adds a vendor for the core security boundary and a cost per MAU before revenue; deferred as an option if MFA/enterprise SSO needs outgrow the built-in service.
- **Long-lived non-rotating tokens**: rejected — a stolen token is permanent.

## Reversibility
**Medium.** The token *shape* is easy to change; the *identity store* is core. Choosing to build it in-house (not a vendor) is the harder-to-reverse half — justified by cost at the million-student target.

## Team cost
~1 week to build identity + rotation + native Google + MFA for admin. Reused by all four clients via `packages/api-client`.
