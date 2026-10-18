# apps/web

Nelavista V2 student web app — React + TypeScript + Vite, built as an **installable PWA** (ADR-0001).

- Public routes are client-rendered; signed-in screens are lazy-loaded per route (B12).
- API access goes through this app's `src/lib/http.ts`, which owns the cookie session
  (ADR-0009): the refresh token stays in an httpOnly cookie, the access token lives in
  memory, and a 401 triggers one de-duplicated refresh. Types for the wire come from
  `@nelavista/api-client` (generated from the OpenAPI schema) and
  `@nelavista/contracts` (shapes the schema cannot describe yet).
- Config from `VITE_*` only. **No secrets** — the bundle is public.

```bash
make web-dev     # http://localhost:5173
make web-build
pnpm --filter @nelavista/web test
```

## Routes

| Route         | Screen                                             |
| ------------- | -------------------------------------------------- |
| `/`           | Landing                                            |
| `/signup`     | Create account                                     |
| `/login`      | Sign in (returns to the attempted URL)             |
| `/onboarding` | Profile → path → university → department → courses |
| `/home`       | Greeting, path switch, courses, verify-email banner |
| `/academia`   | Dashboard: the five questions and one next action  |
| `/campus`     | University info and map points                     |

Everything from `/onboarding` down requires a session; an anonymous visit redirects to
`/login` and comes back afterwards.

## Tests

`vitest run` in this package covers the request layer: CSRF on writes, the shared error
envelope, single-flight refresh, and the `@nelavista/api-client` wrapper. It does not
cover the screens — there is no browser-level harness yet.
