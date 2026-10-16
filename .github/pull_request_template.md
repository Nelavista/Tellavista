## What & why
<!-- One or two sentences. Link the issue/PRD section. -->

## Area
- [ ] `apps/api`  - [ ] `apps/web`  - [ ] `apps/admin`  - [ ] `apps/mobile`  - [ ] `packages/*`
- [ ] **V1 (`app/` etc.)** ← if ticked, the V1 checklist below is mandatory
- [ ] docs / CI / tooling

## V1 safety (required if this touches V1)
- [ ] `pytest tests/` result pasted below
- [ ] `python -m scripts.audit.check_template_links` result pasted below
- [ ] No V1 dependency changes
- [ ] No change to V1 runtime behaviour
- [ ] No production data touched

## Data / migrations
- [ ] No schema change
- [ ] Schema change is expand/contract, single Alembic head (`alembic heads` → 1)
- [ ] Target `DATABASE_URL` for any script named here: `________________`

## Secrets
- [ ] No secret added to the repo, PR text or CI logs
- [ ] Any new env var added to the relevant `.env.example` (names + placeholders only)

## Contracts
- [ ] `packages/api-client` regenerated (if the API schema changed)

## Manual steps required (do not automate)
<!-- Render / DNS / Google Cloud / Search Console / Apple / Play / EAS. List or write "none". -->

## Feature flag
<!-- Name the flag if this merges unfinished work, or write "n/a". -->
