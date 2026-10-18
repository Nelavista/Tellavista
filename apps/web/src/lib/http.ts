/**
 * The web app's only way to talk to the API.
 *
 * Auth model (ADR-0009): the browser never stores the refresh token. It lives in
 * an httpOnly cookie; the access token stays in memory only. Every call is
 * same-origin (`/api/v1/...`) so the cookie rides along and no CORS is involved.
 * A 401 triggers exactly one refresh, deduplicated across concurrent requests, so
 * a burst of calls on tab-focus cannot rotate the refresh token twice.
 */
import { API_PATH_VERSION, type ApiErrorEnvelope } from '@nelavista/contracts';

const API_ROOT = `/api/${API_PATH_VERSION}`;
const CSRF_COOKIE = 'nv_csrf';
const CSRF_HEADER = 'X-CSRF-Token';

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly requestId?: string;
  readonly details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown, requestId?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.details = details;
    this.requestId = requestId;
  }
}

let accessToken: string | null = null;

export function setAccessToken(token: string | null): void {
  accessToken = token;
}

export function getAccessToken(): string | null {
  return accessToken;
}

function readCookie(name: string): string | null {
  const prefix = `${name}=`;
  for (const part of document.cookie.split(';')) {
    const value = part.trim();
    if (value.startsWith(prefix)) return decodeURIComponent(value.slice(prefix.length));
  }
  return null;
}

async function parseError(res: Response): Promise<ApiError> {
  let envelope: Partial<ApiErrorEnvelope> = {};
  try {
    envelope = (await res.json()) as Partial<ApiErrorEnvelope>;
  } catch {
    // A proxy or a 204 can produce an empty body; the status is still meaningful.
  }
  const body = envelope.error;
  return new ApiError(
    res.status,
    body?.code ?? `http_${res.status}`,
    body?.message ?? res.statusText ?? 'Something went wrong. Please try again.',
    body?.details,
    body?.request_id,
  );
}

type Method = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';

async function send(method: Method, path: string, body?: unknown): Promise<Response> {
  const headers: Record<string, string> = {
    Accept: 'application/json',
    'X-API-Version': API_PATH_VERSION,
  };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;

  // Double-submit CSRF: cookies alone never authorise a write.
  if (method !== 'GET') {
    const csrf = readCookie(CSRF_COOKIE);
    if (csrf) headers[CSRF_HEADER] = csrf;
  }

  return fetch(`${API_ROOT}${path}`, {
    method,
    headers,
    credentials: 'include',
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

let inFlightRefresh: Promise<boolean> | null = null;

/** Rotate the session using the httpOnly refresh cookie. Never throws. */
export function refreshSession(): Promise<boolean> {
  inFlightRefresh ??= (async () => {
    try {
      const res = await send('POST', '/auth/refresh', {});
      if (!res.ok) {
        accessToken = null;
        return false;
      }
      const data = (await res.json()) as { access_token?: string };
      accessToken = data.access_token ?? null;
      return accessToken !== null;
    } catch {
      accessToken = null;
      return false;
    } finally {
      inFlightRefresh = null;
    }
  })();
  return inFlightRefresh;
}

async function request<T>(method: Method, path: string, body?: unknown): Promise<T> {
  let res = await send(method, path, body);

  if (res.status === 401 && path !== '/auth/refresh' && path !== '/auth/login') {
    if (await refreshSession()) {
      res = await send(method, path, body);
    }
  }

  if (!res.ok) throw await parseError(res);
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export const http = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body ?? {}),
  patch: <T>(path: string, body?: unknown) => request<T>('PATCH', path, body ?? {}),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body ?? {}),
  del: <T>(path: string) => request<T>('DELETE', path),
};
