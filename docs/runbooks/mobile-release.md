# Runbook — Mobile release

## Two kinds of change
| Change | Path | Store review? |
|---|---|---|
| **JS/TS only** | **EAS Update (OTA)** | No |
| **Native** (new native module, SDK change, config) | **EAS Build → store** | Yes |

## OTA (JS-only)
```bash
pnpm --filter @nelavista/mobile update      # publishes to the production channel
```
Uses `runtimeVersion.policy: appVersion` (app.config.js), so an update only reaches binaries built for that version. **Roll back** by republishing the previous update, or `eas update:rollback`.

## Store build (native)
1. Branch from a **tagged commit** (`v2.0.0`) — PROD store builds come only from tags.
2. Bump `expo.version` in `app.config.js`.
3. Build: `pnpm --filter @nelavista/mobile build:prod` (EAS cloud; **no Mac needed**).
4. **Internal testing first:** iOS → TestFlight; Android → internal testing track (or a direct APK for the team).
5. **Staged rollout:** iOS phased release; Android staged rollout (e.g. 5% → 20% → 100%).
6. Submit: `eas submit` (iOS) / Play Console (Android).

## Signing keys
Stored **only** in the **EAS secret store**. Never in the repo. (`.gitignore` blocks `*.p8`, `*.p12`, `*.keystore`, `*.jks`, `*.mobileprovision`.)

## Force-update
To require an update for an old binary, **raise `mobile.<platform>.min_supported` in `packages/config/versions.json` and redeploy the API**. Old apps then get `426 Upgrade Required` with the store URL (ADR-0010).

## Rollback path
1. **OTA:** `eas update:rollback` (or republish the last good update on the channel).
2. **Binary:** promote the **previous build** in the store (halt the staged rollout / restore the prior version).
