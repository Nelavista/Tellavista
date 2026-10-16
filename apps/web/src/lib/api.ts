/**
 * API base URL comes from config — never hardcoded (ADR-0002).
 * In local dev, Vite proxies /api to the API (vite.config.ts), so relative
 * calls work same-origin and cookies behave.
 */
const API_VERSION = import.meta.env.VITE_API_VERSION ?? 'v1';

/** Build a URL to an API path under the current API version. */
export function apiUrl(path: string): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  return `/api/${API_VERSION}${clean}`;
}
