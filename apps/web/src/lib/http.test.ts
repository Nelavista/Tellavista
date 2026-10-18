import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { ApiError, http, refreshSession, setAccessToken } from './http';

type Call = { url: string; init: RequestInit };

function json(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function calls(fetchMock: ReturnType<typeof vi.fn>): Call[] {
  return fetchMock.mock.calls.map(([url, init]) => ({
    url: String(url),
    init: (init ?? {}) as RequestInit,
  }));
}

function headersOf(call: Call): Record<string, string> {
  return (call.init.headers ?? {}) as Record<string, string>;
}

describe('http', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    setAccessToken(null);
    document.cookie = 'nv_csrf=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    setAccessToken(null);
  });

  it('sends the access token, the API version and cookies', async () => {
    fetchMock.mockResolvedValue(json(200, { ok: true }));
    setAccessToken('access-1');

    await http.get('/auth/me');

    const [call] = calls(fetchMock);
    expect(call?.url).toBe('/api/v1/auth/me');
    expect(headersOf(call!)).toMatchObject({
      'X-API-Version': 'v1',
      Authorization: 'Bearer access-1',
    });
    expect(call?.init.credentials).toBe('include');
  });

  it('adds the CSRF header on writes but not on reads', async () => {
    document.cookie = 'nv_csrf=csrf-123';
    // A fresh Response per call: a body can only be read once.
    fetchMock.mockImplementation(() => Promise.resolve(json(200, {})));

    await http.get('/onboarding/state');
    await http.post('/me/path', { path: 'skills' });

    const [read, write] = calls(fetchMock);
    expect(headersOf(read!).Authorization).toBeUndefined();
    expect(headersOf(read!)['X-CSRF-Token']).toBeUndefined();
    expect(headersOf(write!)['X-CSRF-Token']).toBe('csrf-123');
    expect(write?.init.body).toBe(JSON.stringify({ path: 'skills' }));
  });

  it('unwraps the shared error envelope', async () => {
    fetchMock.mockResolvedValue(
      json(409, {
        error: {
          code: 'email_taken',
          message: 'That email already has an account.',
          request_id: 'req-7',
          details: { field: 'email' },
        },
      }),
    );

    const error = await http.post('/auth/signup', {}).catch((e: unknown) => e);

    expect(error).toBeInstanceOf(ApiError);
    const apiError = error as ApiError;
    expect(apiError.status).toBe(409);
    expect(apiError.code).toBe('email_taken');
    expect(apiError.message).toBe('That email already has an account.');
    expect(apiError.requestId).toBe('req-7');
    expect(apiError.details).toEqual({ field: 'email' });
  });

  it('refreshes once on 401 and retries with the new token', async () => {
    fetchMock.mockImplementation((url: string, init: RequestInit) => {
      const auth = (init.headers as Record<string, string>).Authorization;
      if (url.endsWith('/auth/refresh')) return Promise.resolve(json(200, { access_token: 'fresh' }));
      return Promise.resolve(
        auth === 'Bearer fresh' ? json(200, { ok: true }) : json(401, { error: { code: 'unauthorized', message: 'No' } }),
      );
    });
    setAccessToken('stale');

    const result = await http.get<{ ok: boolean }>('/auth/me');

    expect(result).toEqual({ ok: true });
    expect(calls(fetchMock).map((c) => c.url)).toEqual([
      '/api/v1/auth/me',
      '/api/v1/auth/refresh',
      '/api/v1/auth/me',
    ]);
  });

  it('rotates the refresh token only once for concurrent 401s', async () => {
    let refreshCount = 0;
    fetchMock.mockImplementation((url: string, init: RequestInit) => {
      const auth = (init.headers as Record<string, string>).Authorization;
      if (url.endsWith('/auth/refresh')) {
        refreshCount += 1;
        return Promise.resolve(json(200, { access_token: 'fresh' }));
      }
      return Promise.resolve(
        auth === 'Bearer fresh' ? json(200, { ok: true }) : json(401, { error: { code: 'unauthorized', message: 'No' } }),
      );
    });
    setAccessToken('stale');

    await Promise.all([http.get('/auth/me'), http.get('/me')]);

    expect(refreshCount).toBe(1);
  });

  it('reports the original 401 when the refresh fails', async () => {
    fetchMock.mockImplementation((url: string) =>
      Promise.resolve(
        url.endsWith('/auth/refresh')
          ? json(401, { error: { code: 'unauthorized', message: 'Session expired.' } })
          : json(401, { error: { code: 'unauthorized', message: 'Sign in again.' } }),
      ),
    );
    setAccessToken('stale');

    await expect(http.get('/auth/me')).rejects.toMatchObject({
      status: 401,
      message: 'Sign in again.',
    });
    expect(await refreshSession()).toBe(false);
  });
});
