# @nelavista/config

The **single source of version truth** for every client and the API.

- `versions.json` — product versions (for the version switcher), the API path version, and the **minimum supported mobile version** per platform.
- `src/index.ts` — typed accessors (`allVersions`, `currentVersion`, `mobilePolicy`, `compareVersions`).

## Changing something
- **Add a version:** append to `versions.json`, set `current`. One edit — the web/admin switcher and the API's min-version policy both read this file.
- **Force a mobile update:** raise `mobile.<platform>.min_supported`, redeploy the API. Clients at a lower version get `426 Upgrade Required` (ADR-0010).

Consumed by `apps/web`, `apps/admin`, `apps/mobile` (bundled at build time) and `apps/api` (read at boot).
