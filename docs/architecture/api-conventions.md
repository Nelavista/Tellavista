# API conventions

Every endpoint added from Phase 0 onward follows these rules. The code is the
source of truth; this page explains it so a client developer does not have to
read the handlers.

## Errors

One envelope, always:

```json
{
  "error": {
    "code": "invalid_credentials",
    "message": "Email or password is incorrect.",
    "request_id": "6f1c…",
    "details": { "field": "email" }
  }
}
```

- `code` is stable and machine-readable (`app/core/errors.py` lists the mappings).
- `message` is safe to show a student; it never contains an exception, SQL or a
  stack trace.
- `details` is optional structured data — field errors on a 422, a retry hint on
  a 429.
- `request_id` matches the `X-Request-ID` response header and the log line, so a
  screenshot from a phone is enough to trace the failure.

500s are logged with the traceback and answered with `internal_error` and the
request id only.

## Request ids

Every response carries `X-Request-ID`. An inbound id is reused only when it
matches `^[A-Za-z0-9._-]{8,64}$`; otherwise a fresh 32-hex id is generated.

## Pagination

Keyset only, never offset (ADR-0007):

```
GET /v1/items?limit=20&cursor=<opaque>
→ { "items": [...], "next_cursor": "<opaque>" | null }
```

A cursor is the last row's id, base64url-encoded and treated as opaque by
clients. `limit` defaults to 20 and is capped at 100; an invalid cursor is a 400
`pagination.invalid_cursor`, not an empty page.

## Idempotency

Every write that matters takes a client-generated `Idempotency-Key` (UUID v4).
`app/services/idempotency.py` implements three outcomes:

| Situation | Result |
|---|---|
| same key + same request, already completed | the stored response is replayed |
| same key, first attempt still running | `409 idempotency.in_progress` |
| same key + different body | `409 idempotency.key_reused` |

Rows live 24 hours. The claim is inserted in a savepoint, so losing a race does
not roll back the caller's transaction.

## Versioning and force-update

- The path carries the API version (`/v1`), separate from the product version.
- `X-API-Version` is on every response.
- Mobile sends `X-App-Version` and `X-App-Platform`. Below
  `mobile.<platform>.min_supported` (in `packages/config/versions.json`) the API
  answers `426 Upgrade Required` with `{upgrade, min_version, store_url}`.
- Below `latest` but still supported → `X-Update-Recommended`.

## Auth shape

- Web and admin: httpOnly `nv_refresh` cookie + readable `nv_csrf` cookie; the
  CSRF value must be sent as `X-CSRF-Token` on cookie-based refresh.
- Native: bearer access token + refresh token in secure storage, sent in the
  request body.
- Access tokens are 15-minute JWTs; refresh tokens are opaque, hashed at rest,
  single-use, and belong to a rotatable family.
