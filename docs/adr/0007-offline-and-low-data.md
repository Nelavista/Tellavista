# ADR-0007 — Offline and low-data strategy

**Status:** Accepted · **Date:** 2026-10-16

## Context

Target users are on **mid-range Android phones on expensive, unstable data** (PRD §15). V2 must be **reliable: no lost work, no lost answers, no lost payments**. V1's "offline" claim is false (audit §7) — there is no service worker and the JS unregisters one.

## Decision

### Web (PWA)
- A **Workbox** service worker with **app-shell precache** + **runtime caching** for static assets.
- **Network-first for API reads**, cache-fallback for previously seen catalog/course/material *metadata* (never for money or work-submission responses).
- **Only GET is cached.** Mutations are never served from cache.

### Mobile
- **`expo-sqlite`** for structured local storage (catalog, course/topic metadata, the student's own work drafts) + **AsyncStorage** for small KV flags.
- Downloaded **course material files** cached on device (file-system), with an explicit "download for offline" action and a size shown before download.

### Idempotent writes with a retry queue (the reliability core)
- Every mutating request from web or mobile carries a **client-generated `Idempotency-Key`** (UUID v4). The API stores it with the response and **returns the same response on replay** — this is what makes "no lost work" true on a flaky network.
- Failed mutations go into a **persistent local retry queue** with exponential backoff; the UI shows pending/synced state (especially for **work submissions** and **anything money-related**).
- **Money and work submissions are never optimistically marked "done"** — they show "pending sync" until the server confirms.

### Small payloads
- **Cursor-based pagination** everywhere (no offset paging on large sets).
- **Field selection / sparse responses** on list endpoints; **gzip/brotli** at the edge.
- **Delta sync**: list endpoints return `updated_since` results; clients store `last_synced_at`.
- Images served at **requested sizes** (CDN transform), not originals.

## Options considered
- **Full offline-first CRDT sync** — over-engineered for V2; deferred.
- **No offline at all** — unacceptable on Nigerian mobile data.

## Reversibility
**High** — caching policy and queue behaviour are client-local and tunable without schema change.

## Team cost
~2–3 days across web + mobile for the cache + idempotency/queue primitives; it is a **prerequisite** for the work-submission flow, so it is built with the first work feature, not after.
