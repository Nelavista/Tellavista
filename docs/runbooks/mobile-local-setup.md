# Runbook — Mobile local setup

**The team has no Mac.** This changes what is possible locally, so read the table first.

| Task | Windows / Linux dev | Needs a Mac? |
|---|---|---|
| Android Emulator / real Android device | ✅ | No |
| Expo dev server + JS/TS work | ✅ | No |
| iOS Simulator | ❌ | **Yes** (macOS + Xcode only) |
| iOS device build / TestFlight | ✅ via **EAS cloud build** | No |
| iOS App Store submission | ✅ via EAS Submit | No |

## Android (the everyday local loop)
```bash
make mobile-start          # start Expo
make mobile-android        # open in the Android Emulator
```
Or on a real Android device: enable USB debugging, `adb devices` to confirm, then press `a` in the Expo terminal (or scan the QR with Expo Go).

## Reaching the local API from a device/emulator
The app must not hardcode a host. `app.config.js` reads `API_BASE_URL` at build time.

- **Android Emulator** → the host machine is `10.0.2.2`: set `API_BASE_URL=http://10.0.2.2:8000`.
- **Real device on the same LAN** → use the dev machine's LAN IP: `API_BASE_URL=http://192.168.x.x:8000` (find it with `ipconfig` / `ip addr`).
- Ensure the API listens on `0.0.0.0` (dev command does) and that the OS firewall allows the port.

Test it: open `http://<host>:8000/v1/health` in the device browser first.

## iOS without a Mac
1. Enrol in the **Apple Developer Program** (manual; can take days — start early).
2. Log in to EAS: `pnpm dlx eas-cli login`.
3. Build a dev client: `pnpm --filter @nelavista/mobile build:dev`.
4. Install the resulting build on a test iPhone (EAS gives a QR/registration flow).
5. Distribute via **TestFlight** for wider testing.

EAS handles signing in the cloud — no Xcode, no local `.p12`/`.mobileprovision`. **Signing keys live in the EAS secret store, never in the repo.**

## Environment
Environment comes from the **build profile** (`eas.json` → `APP_VARIANT`), not runtime guessing. DEV builds use a `.dev` bundle ID/package so they install **alongside** PROD. Details: `apps/mobile/README.md`.
