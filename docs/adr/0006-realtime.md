# ADR-0006 — Realtime: keep, replace or drop V1's Socket.IO

**Status:** Accepted · **Date:** 2026-10-16

## Context

V1 uses **Flask-SocketIO on eventlet** for live classes and community chat, authenticated by the **session cookie**, with in-process room state that forces a **single worker** until `REDIS_URL` is set. V2's PRD has **no Community product** and does not list live classes as a V2 feature. V2's needs are far smaller: work status updates, notification arrival, and managed-project monitoring.

## Decision

**Drop Socket.IO for V2 core. Use request/response + push, with an optional thin SSE channel.**

| V1 realtime use | V2 decision |
|---|---|
| Live video classes (Agora signalling) | **Out of V2 scope.** Not carried. |
| Community chat / groups | **Dropped** (no Community product). |
| Notification bell updates | **Push notifications** (APNs/FCM via Expo) + polling on screen focus. |
| Managed-project/work status | **Push** to the student; **polling** in the internal admin tools. |
| "Live" dashboards (admin ops) | **Short-interval polling** (admin tool, low traffic) — no websocket server to run. |

**If** a genuine server-push need appears later, add a **single FastAPI SSE endpoint** (works through the API's existing auth, no new stateful server), not Socket.IO. A websocket server is only justified once a feature cannot be built with SSE.

**Consequence:** V2 has **no per-worker in-memory realtime state**, which removes the single-worker constraint from the API's design. Redis is still used for the ARQ queue and caching, not for websocket fan-out.

## Options considered
- **Keep Socket.IO in V2** — rejected: carries eventlet, the single-worker constraint and a room model V2 does not need.
- **WebSockets (FastAPI native)** — deferred; only if SSE proves insufficient.

## Reversibility
**High** — adding SSE or websockets later does not change the domain model.

## Team cost
Saves the ongoing cost of running and scaling a stateful realtime tier. Push notifications add ~1 day (Expo credentials per environment; ADR-0009/0010).
