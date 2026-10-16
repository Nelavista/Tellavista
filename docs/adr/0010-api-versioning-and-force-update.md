# ADR-0010 — API versioning, minimum app version, force-update

**Status:** Accepted · **Date:** 2026-10-16

## Context

Two different "versions" now exist and must never be confused: **product versions** (V1, V2 — the student-facing product on subdomains) and **API versions** (the wire contract). Also: **mobile apps always talk to the latest API**, but **old app binaries stay installed for a long time**, so the API must be able to tell an old app to update — or refuse to serve it.

## Decision

### Naming that keeps the two apart
- **Product versions** are **`V1`, `V2`** (and `v1.nelavista.com`, `v2.nelavista.com`). Human-facing only.
- **API versions** are **`/v1`, `/v2`** in the **URL path** of the API host (`api.nelavista.com/v1/...`). Machine-facing only.
- They are **independent**: product V2 ships on API `/v1` (there is no reason for a first API version to be called v2). The path version increments only on a **breaking wire change**.

### Versioning scheme
- **Additive changes** (new fields, new endpoints) do **not** bump the version.
- **Breaking changes** create a **new path version** (`/v2`) served **in parallel**; the old one is deprecated with a documented sunset window.
- Every response carries the API version in a header (`X-API-Version`) for observability.

### Minimum supported app version + force-update
- Every mobile request sends **`X-App-Version`** (e.g. `2.1.0`) and **`X-App-Platform`** (`ios`|`android`).
- The API compares against a **minimum supported version per platform**, declared in **`packages/config/versions.json`** (the same single file the web version switcher reads — one edit changes the policy everywhere).
- If the app is **below minimum**, the API returns **`426 Upgrade Required`** with a machine-readable body: `{ "upgrade": "required", "min_version": "2.2.0", "store_url": "…" }`.
- If the app is **below the latest but above minimum**, the API returns normally and adds a **`X-Update-Recommended`** header; the app shows a dismissible prompt.
- The mobile clients **check this on launch and on resume** and route to a blocking "Please update" screen when required.

### Interaction with OTA (ADR-0001)
JS-only changes ship via **EAS Update** and do **not** need a store release. **Native changes** need a store build. The minimum-version mechanism is only for **native** incompatibilities; OTA handles the rest.

## Options considered
- **Header-based versioning** (`Accept: application/vnd.nelavista.v1+json`): RESTful but harder for a small team to debug and for generated clients. Path versioning chosen.
- **No versioning** ("mobile always updates"): unrealistic — users do not update promptly.

## Reversibility
**High** — the policy lives in one JSON file; the path version is additive.

## Team cost
~0.5 day (the middleware + the versions.json fields + the client check). Prevents an entire class of "the old app is calling a removed field" incidents.
