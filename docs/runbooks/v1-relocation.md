# Runbook — Relocate V1 to `apps/v1` (at launch)

> **STATUS: PLANNED ONLY. NOT EXECUTED.** ADR-0004 decided V1 stays at the repo root until V2 launches. This is the launch-time move.

## Why it is deferred
Renaming/moving V1 and changing Render's **Root Directory** are two halves of one **non-atomic** change. Push the move before the dashboard change and the live site 500s (no `wsgi.py` at the root). Doing it at launch, in a freeze window, is safe.

## Preconditions
- [ ] V2 is live at `nelavista.com` and V1 is confirmed working at `v1.nelavista.com`.
- [ ] A freeze window is agreed; no other PRs in flight.
- [ ] Founder is available to change the Render dashboard immediately.

## Steps
1. Branch `chore/v1-relocation` from `main`.
2. `git mv` (history-preserving) — one commit:
   ```bash
   mkdir -p apps/v1
   git mv app migrations scripts tests data seed_data wsgi.py Procfile runtime.txt \
          requirements.txt requirements-dev.txt pytest.ini google76268f26b118dad1.html apps/v1/
   ```
3. Update paths that referenced the old locations: CI `ci-v1.yml` path filters, `.dockerignore`, README, any absolute references. Run `git grep` for stragglers.
4. **Run the V1 checks and paste the output in the PR:**
   ```bash
   (cd apps/v1 && python -m pytest tests/)
   python -m scripts.audit.check_template_links     # from the new location
   ```
5. **Render (manual):** set V1's service **Root Directory** to `apps/v1`; confirm the Start Command still matches `Procfile`.
6. Deploy and verify at `v1.nelavista.com` (login, Google, email links, materials, PWA install, Search Console file served).
7. Tag **`v1-final`**; create **`release/v1`**.
8. Merge.

## Deploy impact & rollback
- **Impact:** one Render setting + the repo move. `nelavista.com` is unaffected (V2 serves it).
- **Rollback:** `git revert` the move and restore the Root Directory. Keep the freeze window until verified.

## Search Console file
`google76268f26b118dad1.html` moves with V1 **and** must be served at `/google76268f26b118dad1.html`. Add a route/static mapping on V1 (it is **not served today** — audit §5) before relying on it.
