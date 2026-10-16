# apps/web

Nelavista V2 student web app — React + TypeScript + Vite, built as an **installable PWA** (ADR-0001).

- Public/marketing routes are **prerendered at build time**; the authenticated app is client-rendered. No SSR server.
- API access goes through `packages/api-client` (generated) — do not hand-write fetch calls to the API.
- Config from `VITE_*` only. **No secrets** — the bundle is public.

```bash
make web-dev     # http://localhost:5173
make web-build
```

Skeleton only (`hello world` + version switcher + health check).
