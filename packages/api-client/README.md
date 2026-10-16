# @nelavista/api-client

The typed API client shared by **web, admin and mobile** (ADR-0001).

- `src/index.ts` — the hand-written wrapper the apps import (`createApiClient`). Stable surface: auth header, API path version, idempotency key, and `426` force-update handling.
- `src/generated/` — **generated** from the API's OpenAPI schema. Never hand-edit.

## Regenerate
```bash
pnpm --filter @nelavista/api-client generate
```
CI runs a **freshness check**: if the API schema changed and the client was not regenerated, the build fails. This is what keeps web, admin and mobile honest against the single API contract.
