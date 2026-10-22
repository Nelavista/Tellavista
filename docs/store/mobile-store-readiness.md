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
| Feature graphic | 1024×500 | Generated placeholder (`apps/mobile/assets/feature-graphic.png`) |

Screenshots of a mock-up are rejected under both stores' metadata rules; capture
them from the release build with the seeded demo account (`.github` test account
below). The journey now includes the B13/B14 screens, so the set is: home, a
verified skill, an assessment, study materials, Ask Nelavista with a cited
answer, CBT results, the talent profile with a share link, an opportunity with its
match explanation, and earnings with a paid line.

## Screenshot and feature-graphic capture (release build)

The one thing that cannot be produced from this repository is a screenshot of the
real app. This is the exact capture pass for the first release build.

### Capture checklist

- [ ] Build a **release** binary, not Expo Go: `eas build --profile preview --platform ios`
      and `--platform android` (or `npx expo run:ios --configuration Release`).
- [ ] Sign in with the review account on a clean device or simulator. Confirm the
      seeded course, one verified skill, one passed assessment and one paid line.
- [ ] Capture in this order, so the story reads as a journey:
      1. Home with the next step
      2. Skills → a verified skill
      3. Verification → a passed assessment with its score
      4. Academia → Study materials
      5. Ask Nelavista with a grounded answer and its citations
      6. Practice (CBT) → results with strengths and weaknesses
      7. Talent profile and one active share link
      8. An opportunity with the "why you qualify" explanation
      9. Earnings with a paid line
- [ ] Use the device's own status bar (no overlay): a clean, current time and full
      signal. Apple rejects screenshots with a stale or obviously mocked status bar.
- [ ] Capture iPhone 6.7" and 6.1" (App Store requires the 6.7" set; the 6.1" set is
      optional but recommended). iPad is not required (`supportsTablet: false`).
- [ ] Capture Android phone and 7" tablet from the Play listing requirements.
- [ ] Crop nothing that hides a real empty state. An empty state is acceptable; a
      fake one is not.
- [ ] Check every image for real student data, tokens, email addresses or links.
      Only the review account may appear.
- [ ] Replace `apps/mobile/assets/feature-graphic.png` with the final brand artwork
      at 1024×500. Re-run `node tools/gen-mobile-assets.mjs` only to regenerate the
      placeholder, never to overwrite final design files.
- [ ] Upload the screenshots to App Store Connect and Play Console, then record the
      build number and capture date in the release ticket.

**Owed:** steps above are external because they need a signed release build and a
device. Everything else in this document is code, copy or a generated asset.

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

**Blocked on you:** the retention periods in the privacy policy (payout records and
deleted-account financial history) must be decided before these answers are final.
Contributor terms are decided (G3: version 2026-10-01, guardian consent below 18),
but the retention wording is a legal decision, not a build decision — an inaccurate
data-safety form is a policy violation, not a formality.

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

The policy is now decided (G3), and it is enforced by the API, not only by copy:

- Minimum age for paid work: **16** (`min_student_age`).
- Under **18** requires guardian consent (`guardian_consent_below_age`); the
  consent is recorded against the contributor terms version.
- Contributor terms: **2026-10-01**, Nelavista Contributor Licence 1.0, curriculum
  owned and authored in house.
- Intended audience: **16+**. Do not select a child category; Play's Families
  policy would otherwise apply. Answer the age-rating questionnaire honestly, and
  let the store's own rules raise the displayed rating if the work/payment content
  requires it.
- Age gate: none in-app; accounts are created through the web sign-up where the
  terms and guardian consent are accepted. The API refuses a payout below the
  configured age or without the required consent.
- Keep the listing, the terms page and `platform_settings` in step: changing a
  limit in the admin Platform screen changes the API rule immediately, so the
  store copy must be updated in the same release.

**Blocked on you:** the terms/privacy pages must be live and must state the same
16+/guardian-consent rule. A store listing that says 18+ while the API accepts 16
is a mismatch.

## Review notes for the reviewer

```
Nelavista is a learning-and-work app for university students. The review account
below is pre-seeded with a course, two verified skills, a completed assessment,
study material and practice questions, one open opportunity and one paid earning
line, so every screen has content.

Academia includes study materials, Ask Nelavista (answers are grounded in the
student's own course material and decline when nothing supports an answer) and CBT
practice. Practice is not verification. The talent profile is evidence-only; a
company sees it only through a scoped, expiring link the student creates.

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
- [ ] Age rating 16+ (guardian consent below 18), no child category; API limits match the listing
- [ ] No real student data in any screenshot or review note
