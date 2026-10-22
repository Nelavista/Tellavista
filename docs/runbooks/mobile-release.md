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

A production store build starts from a **version tag** — `.github/workflows/mobile-release.yml`
enforces it.

1. Bump `expo.version` in `apps/mobile/app.config.js` and merge it.
2. Tag that commit: `git tag v2.1.0 && git push origin v2.1.0`.
3. The workflow asks for approval on the `production-mobile` environment, typechecks,
   and **fails if the tag and `expo.version` disagree** (a binary labelled 1.0.0
   uploaded as v2.1.0 is rejected by the store and breaks the force-update policy,
   which keys off app version).
4. It queues EAS builds for both platforms (`eas build --platform all
   --profile production --no-wait`).
5. **Internal testing first:** when the builds finish, promote them to TestFlight /
   Play internal testing before the `submit` job (or `eas submit --platform …
   --latest` by hand).
6. **Staged rollout:** iOS phased release; Android staged rollout (e.g. 5% → 20%
   → 100%). Approval for the binary is not approval for a 100% rollout.

Local equivalent (debugging only — no store upload):

```bash
pnpm --filter @nelavista/mobile build:prod
```

### Repository configuration the workflow needs

| Kind | Name | Purpose |
|---|---|---|
| secret | `EXPO_TOKEN` | Expo robot user; builds and submissions |
| environment | `production-mobile` | Required reviewers — the human gate |
| EAS secret | iOS distribution certificate + provisioning profile | Signing (EAS manages them) |
| EAS secret | `ASC_API_KEY` (App Store Connect API key) | `eas submit --platform ios` |
| EAS secret | Play service-account JSON | `eas submit --platform android` |

## Signing keys
Stored **only** in the **EAS secret store**. Never in the repo. (`.gitignore` blocks `*.p8`, `*.p12`, `*.keystore`, `*.jks`, `*.mobileprovision`.)

## Force-update
To require an update for an old binary, **raise `mobile.<platform>.min_supported` in `packages/config/versions.json` and redeploy the API**. Old apps then get `426 Upgrade Required` with the store URL (ADR-0010).

## OTA during a staged rollout

An OTA update reaches every install on that runtime version, including the 5% in a
staged rollout. Ship the binary first, watch the staged cohort, then publish JS
updates; never use an OTA to "fix" a release that has not finished rolling out.

## Rollback path
1. **OTA:** `eas update:rollback` (or republish the last good update on the channel).
2. **Binary:** promote the **previous build** in the store (halt the staged rollout / restore the prior version).
