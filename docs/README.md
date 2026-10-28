# Docs index

For the V2 web launch, read these first:

1. **`RUN-LOCALLY.md`** (repo root) - run V2 on Windows in about 15 minutes.
2. **`docs/v2-ui/AUDIT.md`** - what V2 actually has, what is missing, and what is stale.
3. **`docs/v2-ui/ROUTE-MAP.md`** - the approved public, auth, student, admin and utility routes.
4. **`docs/v2-ui/DESIGN-DIRECTION.md`** - the approved brand blue and white visual system and component direction.
5. **`docs/runbooks/v2-launch-checklist.md`** - the deployment and cutover plan.
6. **`docs/runbooks/domain-switch.md`** - the domain move and rollback in detail.

## V2 UI work

Gate 1 (route map) and Gate 2 (design direction) were approved on 2026-10-27.
Newsletter and the platform announcement banner are deferred post-launch.

- **`docs/v2-ui/AUDIT.md`** - current-state audit, launch blockers, docs audit.
- **`docs/v2-ui/PARITY.md`** - V1 to V2 capability mapping, including deliberate drops.
- **`docs/v2-ui/ROUTE-MAP.md`** - Gate 1 route contract.
- **`docs/v2-ui/DESIGN-DIRECTION.md`** - Gate 2 visual direction.
- **`docs/v2-ui/IMAGE-PROMPTS.md`** - image manifest, exact filenames and art direction.
- **`docs/design/ui-ux-framework.md`** - the project UI/UX guard. Read it before changing a screen. It is updated after Gate 2 approval where it conflicts with the approved direction.

## Reference (only when a step sends you there)

- **`docs/runbooks/rollback.md`** - put V1 back if the cutover goes wrong.
- **`docs/runbooks/restore-from-backup.md`** - Render Postgres restore drill.
- **`docs/runbooks/rotate-secrets.md`** - key rotation.
- **`docs/architecture/02-environments.md`** - env vars and environments.
- **`docs/architecture/03-versioning-and-domains.md`** - why V1 lives on `v1`.
- **`docs/architecture/05-domain-map.md`** - domain ownership.
- **`docs/architecture/06-roadmap.md`** - milestones and current delivery status.
- **`docs/adr/`** - the accepted decisions behind the architecture.
- **`docs/product/Nelavista_V2_PRD.pdf`** - the product requirements.

## Build and delivery history

- **`docs/build/nelavista-02-v2-build-prompt.md`** - the build work order.
- **`docs/build/phase-0-plan.md`** - completed Phase 0 gap analysis and plan.
- **`docs/build/phase-1-10-plan.md`** - per-phase delivery narrative.
- **`docs/build/REMAINING_WORK.md`** - build tracker. It is not the UI readiness list; use `docs/v2-ui/AUDIT.md` for that.

## Not part of this launch

The mobile app, DEV preview, load-test measurement and Cloudinary material
migration are post-launch. Their runbooks are kept for later but are not steps in
the launch plan.

## Historical, not instructions

`docs/architecture/00-audit.md` is the V1 code audit. It is useful context for
understanding what V1 actually is, but it is not V2 status. If a historical page
disagrees with `docs/v2-ui/AUDIT.md` or the launch plan, the current V2 documents
win.

`docs/MIGRATION_MAP.md` and `docs/TEMPLATE_CLASSIFICATION.md` were removed because
they described the rejected "keep Flask" path and a completed template cleanup.
Git history keeps them if someone needs the old detail.
