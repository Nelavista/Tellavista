# ADR-0012 — Mobile ships in lockstep with web

**Status:** Accepted · **Date:** 2026-10-17
**Affects:** `apps/web`, `apps/mobile`, the journey roadmap (M1–M7)

## Context

The same student uses both surfaces: web for longer academic sessions, mobile for lessons and paid work in the gaps between them. Shipping a journey screen on web weeks before mobile splits the product into two different answers to "where do I do this?", and every gap becomes a support question. It also doubles the period in which the API must support both the new and the old interaction.

The alternative — web first, mobile later — is tempting because web is cheaper to iterate, but it makes the mobile app permanently a reduced copy.

## Decision

The core journey screens ship **in lockstep**:

- Each screen in the journey list (onboarding, path, dashboard, campus, learning, verification, opportunities, work, earnings, settings) is built for web and mobile in the **same milestone**.
- **Shared logic, not shared components.** Types and rules come from `@nelavista/contracts` and `@nelavista/api-client`; the UI is written twice, because a DOM component and a native component have different accessibility and gesture contracts.
- A screen is **not done** until both clients pass their own checks for it. Web is the reference for content and copy; mobile is the reference for the offline and low-data behaviour (ADR-0007).
- Exceptions require a written note in the milestone plan: a screen may ship web-only only when it is genuinely desktop-only (for example, bulk import), or mobile-only (for example, push-permission prompts).

## Consequences

- Fewer, larger milestones; each one closes a journey end to end on both surfaces.
- The API is exercised by two clients from the first release, so mismatch is found at build time rather than after launch.
- Mobile's slower release cadence (store review, force-update window — ADR-0010) is planned into the milestone instead of discovered at the end.

## Reversibility

**Medium.** Reverting to web-first is a process change, not a code change, but it leaves a period where the surfaces differ. Treat the lockstep rule as the default and the exception as the one to justify.
