# Store readiness — Nelavista mobile (D4)

Everything the App Store and Play Console ask for, in one place, with the state of
each item. Placeholder artwork and copy are marked; a real submission replaces
them. Review notes and test accounts are deliberately not committed with real
credentials.

Last reviewed against policy text: 2026-10-18. **Re-check before every
submission** — Apple's payment/earnings rules and Google's data-safety form both
change, and a stale declaration is a rejection or a takedown.

## Identity

| Field | Value |
|---|---|
| App name (PROD) | Nelavista |
| Bundle ID / package | `com.nelavista.app` |
| DEV / preview | `com.nelavista.app.dev`, `com.nelavista.app.preview` |
| Scheme | `nelavista://` |
| Universal links | `https://nelavista.com` (PROD), `https://api-dev.nelavista.com` (DEV) |
| Category | Education |
| Primary language | English |
| Support URL | `https://nelavista.com/support` |
| Privacy policy URL | `https://nelavista.com/privacy` |
| Terms URL | `https://nelavista.com/terms` |

**Blocked on you:** the three URLs must be live before submission; the support
address (`support@nelavista.com`) must be monitored.

## Assets

| Asset | Size | State |
|---|---|---|
| iOS icon | 1024×1024 PNG, no alpha | Generated placeholder (`apps/mobile/assets/icon.png`) |
| Android icon | 512×512 PNG | Same file, downscaled by Play |
| Android adaptive | foreground 1024×1024 + `#050810` | Generated (`adaptive-icon.png`) |
| Splash | 1284×2778 | Generated (`splash.png`) |
| iPhone screenshots | 6.7" and 6.1" | **Owed — must come from a real build** |
| iPad screenshots | — | Not required (`supportsTablet: false`) |
| Android screenshots | phone + 7" tablet | **Owed — must come from a real build** |
| Feature graphic | 1024×500 | **Owed** |

Screenshots of a mock-up are rejected under both stores' metadata rules; capture
them from the release build with the seeded demo account (`.github` test account
below). Suggested set, in journey order: home, a verified skill, an assessment,
an opportunity with its match explanation, earnings with a paid line.

## Listing copy (draft)

**Short description (Play, 80 chars):** Learn job-ready skills, prove them, and
earn from real work.

**Promotional text (Apple, 170 chars):** Turn what you study into proof. Practise
real tasks, pass assessments, and get matched to paid work you can do from your
phone.

**Description:**

> Nelavista connects what you learn at university to work you can actually get.
>
> - Learn along your course with short lessons and practice tasks.
> - Prove your skills with assessments and practical tasks, and keep a transcript
>   of what you have proved — not just what you attended.
> - Get matched to real, paid work. Every opportunity tells you why you qualify
>   or exactly what is missing.
> - See every naira you earn, line by line, and what it was for.
>
> Works on a slow connection: your work is saved on the device and sent when you
> are back online.
>
> Nelavista is built for students in Nigeria. Opportunities are invitation-based
> while we grow.

**Keywords (Apple):** skills, students, jobs, freelance, learn, work, nigeria

## Data safety / privacy declarations

Both stores ask the same questions with different labels. Answer from this table;
it must match what the API actually stores.

| Data type | Collected | Linked to identity | Purpose | Optional? |
|---|---|---|---|---|
| Email address | Yes | Yes | Account, sign-in, notices | No |
| Name | Yes | Yes | Profile, work matching | No |
| Password | Yes (hashed, Argon2) | Yes | Sign-in | No |
| University, department, level | Yes | Yes | Onboarding, matching | No |
| Learning progress and assessment answers | Yes | Yes | Deliver the service, transcript | No |
| Work submissions and review outcomes | Yes | Yes | Deliver the service, quality, pay | No |
| Earnings and payout details | Yes | Yes | Pay the student, tax/records | No |
| Device push token | Yes | Yes | Notifications | Yes (refused permission) |
| Approximate location | **No** — campus coordinates are university data, not the user's | — | — | — |
| Contacts, photos, health, browsing | **No** | — | — | — |
| Diagnostics/crash logs | Request IDs only, no third-party SDK | — | Support | — |
| Advertising / tracking | **None.** No ad SDK, no IDFA, no cross-app tracking | — | — | — |

Declaration answers:

- **Tracking:** No. The app does not track users across other companies' apps or
  websites, so no App Tracking Transparency prompt is shown.
- **Encryption in transit:** Yes (HTTPS only; cleartext is not permitted in
  release builds).
- **Data deletion:** Yes, in-app (Settings → Delete my account) and by request to
  support. Deletion is immediate for the account; financial records are retained
  where law requires and the app says so before deleting.
- **Data export:** Yes, machine-readable JSON from Settings.

**Blocked on you:** the retention periods in the privacy policy (G3 contributor
terms, payout records) must be decided before these answers are final — an
inaccurate data-safety form is a policy violation, not a formality.

## In-app account deletion (store requirement)

Built and wired: Settings → *Delete my account* explains what is deleted, requires
typing the account email to confirm, calls `DELETE /v1/me`, clears the session and
returns to sign-in. It is reachable in two taps from the signed-in home, which is
what both stores check.

## Payments and earnings — policy check

The app **does not sell digital content or subscriptions**. It shows earnings a
student has accrued from work delivered to clients; money moves off-platform via
bank transfer, not through in-app purchase. That keeps it out of Apple's IAP
rules and Google Play Billing.

**Re-check before submission:** if any in-app purchase, subscription or paid
digital feature is added, the IAP rules apply. If the app ever lets students pay
for anything inside the app, Google Play Billing applies to digital goods.

## Age rating and consent

- Intended audience: **18+** (work and payouts). Do not select a child category;
  Play's Families policy would otherwise apply.
- Age gate: none in-app; accounts are created through the web sign-up where the
  terms are accepted.
- **Blocked on you (G3):** the minimum student age and consent wording. Until
  that is decided, store listing and terms must say 18+.

## Review notes for the reviewer

```
Nelavista is a learning-and-work app for university students. The review account
below is pre-seeded with a course, two verified skills, a completed assessment,
one open opportunity and one paid earning line, so every screen has content.

Sign in: <review account email> / <password in App Store Connect, not in the repo>

There is no in-app purchase. Earnings shown are from work delivered to external
clients and are paid by bank transfer; the app only reports them.

Push notifications are optional and the app works with permission denied.
Account deletion: Settings at the bottom of the home screen -> Delete my account.
```

**Test accounts** (create per environment, never a real student):

| Platform | Email | Purpose |
|---|---|---|
| iOS review | `review-ios@example.test` | Seeded journey, no 2FA |
| Android review | `review-android@example.test` | Same |
| Internal QA | `qa@example.test` | Richer data, safe to reset |

Passwords live in App Store Connect / Play Console only. Rotate them after each
review cycle.

## Store review failure modes seen in practice

| Rejection | Cause | Prevention here |
|---|---|---|
| 2.1 App completeness | Empty states on every screen | Review account is seeded; empty states name the next action |
| 5.1.1 Permission requests | Push asked before it is explained | Push is requested after sign-in, and only the in-app inbox depends on it |
| 5.1.1(v) Account deletion | No in-app deletion | Settings → Delete my account |
| 4.2 Minimum functionality | A wrapper around a website | Native offline queue, secure token storage, deep links |
| Data safety mismatch | Declared less than collected | Table above mirrors the models; update both together |

## Pre-submission checklist

- [ ] Icon, splash and screenshots replaced with the real brand assets
- [ ] Privacy, terms and support URLs live and monitored
- [ ] Data-safety answers match the current models (review `apps/api/app/models`)
- [ ] Account deletion works on a real device, signed in with the review account
- [ ] Push permission denial leaves the app fully usable
- [ ] Force-update policy (`packages/config/versions.json`) has the new minimum
- [ ] Review account seeded, password stored in the consoles, 2FA off for it
- [ ] Age rating 18+, no child category
- [ ] No real student data in any screenshot or review note
