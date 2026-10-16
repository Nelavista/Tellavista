# ADR-0004 — Where V1 lives in the repo

**Status:** Accepted · **Date:** 2026-10-16

## Context

V1 is live at `nelavista.com` and is deployed by Render from the **repo root** (`Procfile` → `gunicorn ... wsgi:app`). The V2 monorepo wants `apps/api`, `apps/web`, `apps/mobile`, `apps/admin`. V1 could move to `apps/v1` now (via `git mv`, keeping history) or stay at the root until launch.

## Options

**Option A — `git mv` V1 to `apps/v1` now.**
- Requires changing Render's **Root Directory** to `apps/v1` in the dashboard (manual) and re-pointing `runtime.txt`/`Procfile` paths.
- **Critical ordering hazard:** the moment the move is pushed, the old root no longer has `wsgi.py`, so if the dashboard change is not made first (or is wrong), **the live site 500s on deploy**. There is no atomic way to change repo layout and dashboard setting together.
- Touches `app/`, `migrations/`, `scripts/`, `tests/` — every path in `README`, tests and CI must be rewritten.

**Option B — Leave V1 at the root until launch; put V2 under `apps/`.**
- Zero deploy risk. Render config, `Procfile`, `wsgi.py` and all V1 paths are untouched.
- The transitional tree is "V1 at root + V2 in `apps/`", which is slightly untidy for a few months.
- The relocation happens **once**, at launch, as its own isolated PR with a before/after test run and the founder confirming the dashboard change.

## Decision

**Option B — leave V1 at the root until launch.**

Rationale: V1 must not break, and Option A makes "repo layout" and "live deploy config" two halves of one non-atomic change. Nothing in V2 needs V1 to move first; the monorepo works with V1 at the root.

**At launch** (separate, approved PR): `git mv app migrations scripts tests data seed_data wsgi.py Procfile runtime.txt requirements*.txt pytest.ini apps/v1/`, update the Render Root Directory to `apps/v1`, update CI path filters, then tag `v1-final`. Exact steps: `docs/runbooks/v1-relocation.md`.

## The Search Console file
`google76268f26b118dad1.html` must keep being served at the **root of whichever app answers for the property**. Today it is served by nobody (audit §5) and must be fixed regardless: V1 gets a tiny route/static mapping so `/google76268f26b118dad1.html` returns the verification line, and after relocation the file moves with `apps/v1` and keeps that route. V2's public root serves it too (ADR-0003).

## Reversibility
**High** — the move is deferred; nothing has been changed. If Option A is later preferred it is still a `git mv` + dashboard change.

## Team cost
Essentially zero now. ~2 hours at launch (the relocation PR + dashboard change + verification).
