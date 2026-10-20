/**
 * Runtime coverage for `@nelavista/api-client` — the hand-written wrapper the
 * admin and mobile apps use. Web imports its generated types (MeOut/TokenOut),
 * and this test keeps the wrapper itself honest: a failure must surface the
 * shared error envelope, not the empty top level of the response body.
 */
import { createApiClient } from '@nelavista/api-client';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

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

describe('@nelavista/api-client', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('sends the bearer token, API version and idempotency key', async () => {
    fetchMock.mockResolvedValue(json(201, { id: 1 }));
    const client = createApiClient({
      baseUrl: 'https://api.example.com/',
      getAccessToken: async () => 'access-1',
    });

    await client.post('/work/assignments/7/submissions', { body: 'x' }, 'idem-9');

    const [call] = calls(fetchMock);
    expect(call?.url).toBe('https://api.example.com/v1/work/assignments/7/submissions');
    expect(call?.init.headers).toMatchObject({
      'X-API-Version': 'v1',
      Authorization: 'Bearer access-1',
      'Idempotency-Key': 'idem-9',
      'Content-Type': 'application/json',
    });
    expect(call?.init.body).toBe(JSON.stringify({ body: 'x' }));
  });

  it('uses the message and code from the error envelope', async () => {
    fetchMock.mockResolvedValue(
      json(409, {
        error: { code: 'email_taken', message: 'That email already has an account.', request_id: 'req-7' },
      }),
    );
    const client = createApiClient({ baseUrl: 'http://localhost:8000' });

    const error = await client.post('/auth/signup', {}).catch((e: unknown) => e);

    expect(error).toMatchObject({
      status: 409,
      code: 'email_taken',
      message: 'That email already has an account.',
      request_id: 'req-7',
    });
  });

  it('surfaces a 426 as an upgrade requirement, with the store link', async () => {
    fetchMock.mockResolvedValue(
      json(426, { error: { code: 'upgrade_required', message: 'Update the app.' } }),
    );
    const client = createApiClient({ baseUrl: 'http://localhost:8000' });

    const error = (await client.get('/me').catch((e: unknown) => e)) as {
      status: number;
      min_version?: string;
      store_url?: string;
    };

    expect(error.status).toBe(426);
  });

  it('returns undefined for 204 instead of trying to parse a body', async () => {
    fetchMock.mockResolvedValue(new Response(null, { status: 204 }));
    const client = createApiClient({ baseUrl: 'http://localhost:8000' });

    await expect(client.del('/me/availability')).resolves.toBeUndefined();
  });
});
