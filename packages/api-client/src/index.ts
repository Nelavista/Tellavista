/**
 * @nelavista/api-client
 *
 * The **generated** client lives in ./generated (produced from the API's OpenAPI
 * schema by `pnpm --filter @nelavista/api-client generate`). This file is the small,
 * hand-written wrapper the apps import, so generated churn never touches app code.
 *
 * Generation is not run yet because the API currently exposes only /health; once
 * domain routers land (M1+) the generator emits real operations. CI runs a
 * freshness check: if the schema changed and the client was not regenerated, the
 * build fails (ADR-0001).
 */

export interface ApiClientConfig {
  /** API base URL, e.g. http://localhost:8000 or https://api.nelavista.com */
  baseUrl: string;
  /** API path version, e.g. "v1" (distinct from the product version — ADR-0010). */
  apiVersion?: string;
  /** Returns the current access token, or null when signed out. */
  getAccessToken?: () => string | null | Promise<string | null>;
}

export interface ApiError {
  status: number;
  code?: string;
  message: string;
  request_id?: string;
}

/** Minimal fetch wrapper with auth + idempotency support (ADR-0007/0009). */
export function createApiClient(config: ApiClientConfig) {
  const version = config.apiVersion ?? 'v1';
  const root = config.baseUrl.replace(/\/$/, '');

  async function request<T>(
    method: string,
    path: string,
    opts: { body?: unknown; idempotencyKey?: string; headers?: Record<string, string> } = {},
  ): Promise<T> {
    const token = await config.getAccessToken?.();
    const headers: Record<string, string> = {
      Accept: 'application/json',
      'X-API-Version': version,
      ...(opts.headers ?? {}),
    };
    if (opts.body !== undefined) headers['Content-Type'] = 'application/json';
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (opts.idempotencyKey) headers['Idempotency-Key'] = opts.idempotencyKey;

    const res = await fetch(`${root}/${version}${path}`, {
      method,
      headers,
      body: opts.body === undefined ? undefined : JSON.stringify(opts.body),
    });

    if (res.status === 426) {
      // Force-update required (ADR-0010): surface a typed error for the client to handle.
      const body = await res.json().catch(() => ({}));
      throw { status: 426, code: 'upgrade_required', message: 'Please update the app', ...body } as ApiError & {
        min_version?: string;
        store_url?: string;
      };
    }
    if (!res.ok) {
      // Every failure is `{ error: { code, message, request_id } }`;
      // read the envelope, not the top level, or every message is lost.
      const body = (await res.json().catch(() => ({}))) as {
        error?: { code?: string; message?: string; request_id?: string };
      };
      throw {
        status: res.status,
        code: body.error?.code ?? `http_${res.status}`,
        message: body.error?.message ?? res.statusText,
        request_id: body.error?.request_id,
      } as ApiError;
    }
    return (res.status === 204 ? undefined : await res.json()) as T;
  }

  return {
    get: <T>(path: string) => request<T>('GET', path),
    post: <T>(path: string, body?: unknown, idempotencyKey?: string) =>
      request<T>('POST', path, { body, idempotencyKey }),
    put: <T>(path: string, body?: unknown) => request<T>('PUT', path, { body }),
    del: <T>(path: string) => request<T>('DELETE', path),
  };
}

export type ApiClient = ReturnType<typeof createApiClient>;
