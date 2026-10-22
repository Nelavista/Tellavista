# apps/mobile

One **Expo (React Native) + TypeScript** codebase for **iOS and Android** (ADR-0001).

**The team has no Mac.** Handling that is a core design constraint:
- iOS is built and tested through **EAS cloud builds** — no Mac required.
- Local development uses the **Android Emulator** (or a real Android device over LAN).
- iOS verification is via **TestFlight** (needs the Apple Developer account) and EAS **simulator builds** if a Mac is ever available.

## Environment = build profile, not runtime (ADR-0002/0009)
`eas.json` sets `APP_VARIANT` per profile; `app.config.js` derives the name, bundle
identifier/package name and API base URL from it:

| Profile | Name | iOS bundle / Android package | API |
|---|---|---|---|
| development | Nelavista Dev | `com.nelavista.app.dev` | `api-dev.nelavista.com` |
| preview | Nelavista (Preview) | `com.nelavista.app.preview` | `api-dev.nelavista.com` |
| production | Nelavista | `com.nelavista.app` | `api.nelavista.com` |

DEV and PROD install **side by side** on one phone.

## Common commands
```bash
make mobile-start            # Expo dev server
make mobile-android          # Android Emulator
pnpm --filter @nelavista/mobile build:dev      # EAS dev build (internal)
pnpm --filter @nelavista/mobile build:prod     # store build (tagged commits only)
pnpm --filter @nelavista/mobile update         # OTA for JS-only changes
```

## In the shell
Secure token storage, the SQLite offline queue with an idempotent retry, deep and
universal links, push registration, per-environment build profiles and the 426
force-update screen (ADR-0007/0009). Journey screens are in `src/screens/`.
Release: `docs/runbooks/mobile-release.md`; store readiness:
`docs/store/mobile-store-readiness.md`.
