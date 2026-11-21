/**
 * Browser push registration, against a fake Push API.
 *
 * The value here is the contract with the API: the endpoint is the token, the
 * keys travel with it, and turning push off removes the server row before the
 * browser subscription. Those are the parts a real browser cannot be asked to
 * assert in CI.
 */
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { disablePush, enablePush, readPushStatus, urlBase64ToUint8Array } from './push';

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('push registration', () => {
  const endpoint = 'https://push.example.test/subscriptions/1234567890';
  const subscription = {
    endpoint,
    toJSON: () => ({
      endpoint,
      keys: { p256dh: 'p256dh-key', auth: 'auth-key' },
    }),
    unsubscribe: vi.fn(async () => true),
  };
  const registration = {
    pushManager: {
      getSubscription: vi.fn(async () => null as typeof subscription | null),
      subscribe: vi.fn(async () => subscription),
    },
  };
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/me/push-devices') && init?.method === 'POST') {
        return jsonResponse(201, {
          id: 5,
          token: endpoint,
          platform: 'web',
          last_seen_at: null,
        });
      }
      if (url.endsWith('/me/push-devices') && (init?.method ?? 'GET') === 'GET') {
        return jsonResponse(200, {
          devices: [{ id: 5, token: endpoint, platform: 'web', last_seen_at: null }],
        });
      }
      if (url.endsWith('/me/push-devices/5') && init?.method === 'DELETE') {
        return jsonResponse(200, { message: 'removed' });
      }
      return jsonResponse(404, { code: 'not_found', message: 'No route' });
    });
    vi.stubGlobal('fetch', fetchMock);

    Object.defineProperty(navigator, 'serviceWorker', {
      configurable: true,
      value: { getRegistration: vi.fn(async () => registration) },
    });
    Object.defineProperty(window, 'PushManager', { configurable: true, value: function PushManager() {} });
    // jsdom has no Notification implementation.
    vi.stubGlobal('Notification', {
      permission: 'granted',
      requestPermission: vi.fn(async () => 'granted'),
    });
    registration.pushManager.getSubscription.mockResolvedValue(null);
    subscription.unsubscribe.mockClear();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    // @ts-expect-error - the property is stubbed for this test only
    delete navigator.serviceWorker;
    // @ts-expect-error - the property is stubbed for this test only
    delete window.PushManager;
  });

  it('registers the endpoint as the token and sends the keys with it', async () => {
    const result = await enablePush('aGVsbG8gd29ybGQ');

    expect(result).toBe(endpoint);
    expect(registration.pushManager.subscribe).toHaveBeenCalledWith(
      expect.objectContaining({ userVisibleOnly: true }),
    );

    const post = fetchMock.mock.calls.find(([, init]) => init?.method === 'POST');
    expect(post?.[0]).toBe('/api/v1/me/push-devices');
    expect(JSON.parse(String(post?.[1]?.body))).toEqual({
      token: endpoint,
      platform: 'web',
      subscription: { endpoint, p256dh: 'p256dh-key', auth: 'auth-key' },
    });
  });

  it('reuses an existing subscription instead of asking for a second one', async () => {
    registration.pushManager.getSubscription.mockResolvedValue(subscription);

    await enablePush('aGVsbG8gd29ybGQ');

    expect(registration.pushManager.subscribe).not.toHaveBeenCalled();
    expect(fetchMock).toHaveBeenCalled();
  });

  it('removes the server row and then the browser subscription', async () => {
    registration.pushManager.getSubscription.mockResolvedValue(subscription);

    const removed = await disablePush();

    expect(removed).toBe(true);
    const del = fetchMock.mock.calls.find(([, init]) => init?.method === 'DELETE');
    expect(del?.[0]).toBe('/api/v1/me/push-devices/5');
    expect(subscription.unsubscribe).toHaveBeenCalled();
  });

  it('reports this browser as subscribed when a subscription exists', async () => {
    registration.pushManager.getSubscription.mockResolvedValue(subscription);

    const status = await readPushStatus();

    expect(status).toEqual({
      supported: true,
      ready: true,
      permission: 'granted',
      endpoint,
    });
  });

  it('decodes a base64url VAPID key into the bytes the Push API expects', () => {
    // "hello" in base64url, unpadded.
    expect(Array.from(urlBase64ToUint8Array('aGVsbG8'))).toEqual([104, 101, 108, 108, 111]);
  });
});
