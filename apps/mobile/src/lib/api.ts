/**
 * The mobile API client (D1, ADR-0009/0010).
 *
 * Native clients authenticate with bearer tokens: the access token is short-lived
 * and kept in memory, the refresh token lives in SecureStore and never in plain
 * storage. A 401 triggers one refresh, deduplicated; a 426 is a typed
 * `UpgradeRequired` so the shell can show a blocking update screen.
 */
import Constants from 'expo-constants';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const extra = (Constants.expoConfig?.extra ?? {}) as Record<string, string>;
const BASE_URL = extra.apiBaseUrl ?? 'https://api-dev.nelavista.com';
const API_VERSION = extra.apiVersion ?? 'v1';
const REFRESH_KEY = 'nelavista.refresh';
const PLATFORM = Platform.OS === 'ios' ? 'ios' : Platform.OS === 'android' ? 'android' : 'web';

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

let upgradeHandler: ((error: UpgradeRequired) => void) | null = null;

/** The shell registers once; a 426 from any request becomes a blocking screen. */
export function setUpgradeHandler(handler: ((error: UpgradeRequired) => void) | null): void {
  upgradeHandler = handler;
}

export class UpgradeRequired extends Error {
  readonly minVersion?: string;
  readonly storeUrl?: string;

  constructor(minVersion?: string, storeUrl?: string) {
    super('This version of the app is no longer supported.');
    this.name = 'UpgradeRequired';
    this.minVersion = minVersion;
    this.storeUrl = storeUrl;
  }
}

let accessToken: string | null = null;
let refreshToken: string | null = null;

export async function hydrateSession(): Promise<boolean> {
  try {
    refreshToken = await SecureStore.getItemAsync(REFRESH_KEY);
  } catch {
    refreshToken = null;
  }
  return refreshToken !== null;
}

async function storeRefresh(token: string | null): Promise<void> {
  refreshToken = token;
  try {
    if (token === null) await SecureStore.deleteItemAsync(REFRESH_KEY);
    else await SecureStore.setItemAsync(REFRESH_KEY, token);
  } catch {
    // A device without a working keystore still gets an in-memory session for
    // this run; the next launch asks for a password rather than failing open.
  }
}

export function getAccessToken(): string | null {
  return accessToken;
}

async function parseError(res: Response): Promise<ApiError> {
  let envelope: { error?: { code?: string; message?: string; details?: unknown } } = {};
  try {
    envelope = await res.json();
  } catch {
    // empty body
  }
  return new ApiError(
    res.status,
    envelope.error?.code ?? `http_${res.status}`,
    envelope.error?.message ?? res.statusText,
    envelope.error?.details,
  );
}

async function send(method: string, path: string, body?: unknown, idempotencyKey?: string): Promise<Response> {
  const headers: Record<string, string> = {
    Accept: 'application/json',
    'X-API-Version': API_VERSION,
    'X-App-Version': Constants.expoConfig?.version ?? '0.0.0',
    'X-App-Platform': PLATFORM,
  };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  if (idempotencyKey) headers['Idempotency-Key'] = idempotencyKey;
  return fetch(`${BASE_URL}/${API_VERSION}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

let inFlightRefresh: Promise<boolean> | null = null;

export function refresh(): Promise<boolean> {
  inFlightRefresh ??= (async () => {
    if (!refreshToken) return false;
    try {
      const res = await send('POST', '/auth/refresh', { refresh_token: refreshToken });
      if (!res.ok) {
        accessToken = null;
        await storeRefresh(null);
        return false;
      }
      const data = (await res.json()) as { access_token?: string; refresh_token?: string };
      accessToken = data.access_token ?? null;
      if (data.refresh_token) await storeRefresh(data.refresh_token);
      return accessToken !== null;
    } catch {
      return false;
    } finally {
      inFlightRefresh = null;
    }
  })();
  return inFlightRefresh;
}

async function request<T>(
  method: string,
  path: string,
  body?: unknown,
  idempotencyKey?: string,
): Promise<T> {
  let res = await send(method, path, body, idempotencyKey);
  if (res.status === 401 && path !== '/auth/refresh' && path !== '/auth/login') {
    if (await refresh()) res = await send(method, path, body, idempotencyKey);
  }
  if (res.status === 426) {
    const data = (await res.json().catch(() => ({}))) as {
      min_version?: string;
      store_url?: string;
      error?: { details?: { min_version?: string; store_url?: string } };
    };
    const details = data.error?.details ?? data;
    const upgrade = new UpgradeRequired(details.min_version, details.store_url);
    upgradeHandler?.(upgrade);
    throw upgrade;
  }
  if (!res.ok) throw await parseError(res);
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown, idempotencyKey?: string) =>
    request<T>('POST', path, body ?? {}, idempotencyKey),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body ?? {}),
  patch: <T>(path: string, body?: unknown) => request<T>('PATCH', path, body ?? {}),
  del: <T>(path: string) => request<T>('DELETE', path),
};

export async function login(email: string, password: string): Promise<void> {
  const token = await api.post<{ access_token: string; refresh_token?: string }>('/auth/login', {
    email,
    password,
    platform: PLATFORM,
  });
  accessToken = token.access_token;
  if (token.refresh_token) await storeRefresh(token.refresh_token);
}

export async function verifyMfa(challenge: string, code: string): Promise<void> {
  const token = await api.post<{ access_token: string; refresh_token?: string }>('/auth/2fa/verify', {
    mfa_token: challenge,
    code,
  });
  accessToken = token.access_token;
  if (token.refresh_token) await storeRefresh(token.refresh_token);
}

export async function logout(): Promise<void> {
  try {
    await api.post('/auth/logout', { refresh_token: refreshToken });
  } catch {
    // signing out locally is still correct
  }
  accessToken = null;
  await storeRefresh(null);
}

export { BASE_URL, PLATFORM };
