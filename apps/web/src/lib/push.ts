/**
 * Browser push registration.
 *
 * The browser owns the subscription; the API owns the delivery. This module is
 * the only place that bridges them, so the rules live in one spot:
 *
 * * the subscription endpoint is the device token (that is what the API stores
 *   and what makes a device unique across accounts on a shared machine);
 * * unsubscribing removes the server row *and* the browser subscription, because
 *   leaving one without the other either delivers to a closed door or keeps an
 *   address the student cannot see;
 * * nothing asks for permission until the student presses the button — a
 *   permission prompt on load is the fastest way to have it permanently denied.
 */
import type { PushDeviceListOut, PushDeviceOut } from '@nelavista/api-client';

import { http } from './http';

export interface PushStatus {
  /** This browser can do Web Push at all (service worker + Push API). */
  supported: boolean;
  /** The service worker is registered and can be subscribed to. */
  ready: boolean;
  permission: NotificationPermission | 'unsupported';
  endpoint: string | null;
}

function subscriptionPayload(subscription: PushSubscription): {
  token: string;
  platform: 'web';
  subscription: { endpoint: string; p256dh: string; auth: string };
} | null {
  const json = subscription.toJSON();
  const endpoint = json.endpoint ?? subscription.endpoint;
  const p256dh = json.keys?.p256dh;
  const auth = json.keys?.auth;
  if (!endpoint || !p256dh || !auth) return null;
  return { token: endpoint, platform: 'web', subscription: { endpoint, p256dh, auth } };
}

/** VAPID keys travel base64url; the Push API wants raw bytes. */
export function urlBase64ToUint8Array(base64Url: string): Uint8Array<ArrayBuffer> {
  const padding = '='.repeat((4 - (base64Url.length % 4)) % 4);
  const base64 = (base64Url + padding).replace(/-/g, '+').replace(/_/g, '/');
  const raw = window.atob(base64);
  // Backed by a plain ArrayBuffer: `applicationServerKey` rejects a view over a
  // possibly-shared buffer, which is what the generic Uint8Array infers.
  const bytes = new Uint8Array(new ArrayBuffer(raw.length));
  for (let index = 0; index < raw.length; index += 1) {
    bytes[index] = raw.charCodeAt(index);
  }
  return bytes;
}

async function serviceWorkerRegistration(): Promise<ServiceWorkerRegistration | null> {
  if (!('serviceWorker' in navigator)) return null;
  // `getRegistration` never waits. `navigator.serviceWorker.ready` waits
  // forever when no worker is registered, which in a dev build is every time.
  return (await navigator.serviceWorker.getRegistration()) ?? null;
}

export async function readPushStatus(): Promise<PushStatus> {
  const supported = 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
  if (!supported) {
    return { supported: false, ready: false, permission: 'unsupported', endpoint: null };
  }
  const registration = await serviceWorkerRegistration();
  const subscription = registration ? await registration.pushManager.getSubscription() : null;
  return {
    supported: true,
    ready: registration !== null,
    permission: Notification.permission,
    endpoint: subscription?.endpoint ?? null,
  };
}

/**
 * Subscribe this browser and register it with the API.
 *
 * Throws a readable message rather than an exception type: every failure here is
 * something the student has to do differently, so the caller renders text.
 */
export async function enablePush(publicKey: string): Promise<string> {
  const registration = await serviceWorkerRegistration();
  if (!registration) {
    throw new Error('This browser has no service worker yet. Reload the app and try again.');
  }

  const permission =
    Notification.permission === 'granted' ? 'granted' : await Notification.requestPermission();
  if (permission !== 'granted') {
    throw new Error(
      permission === 'denied'
        ? 'Notifications are blocked for this site. Allow them in your browser settings, then try again.'
        : 'Notification permission was not granted.',
    );
  }

  const existing = await registration.pushManager.getSubscription();
  const subscription =
    existing ??
    (await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(publicKey),
    }));

  const payload = subscriptionPayload(subscription);
  if (!payload) {
    throw new Error('This browser did not return a usable push subscription.');
  }
  await http.post<PushDeviceOut>('/me/push-devices', payload);
  return subscription.endpoint;
}

/**
 * Remove this browser's subscription from the API and from the browser.
 *
 * The server row is removed by device id, so a subscription that was already
 * replaced elsewhere still ends in a clean state rather than a 404 the student
 * has to understand.
 */
export async function disablePush(): Promise<boolean> {
  const registration = await serviceWorkerRegistration();
  const subscription = registration ? await registration.pushManager.getSubscription() : null;
  if (!subscription) return false;

  const endpoint = subscription.endpoint;
  const list = await http.get<PushDeviceListOut>('/me/push-devices');
  const device = list.devices.find((row) => row.token === endpoint);
  if (device) {
    await http.del(`/me/push-devices/${device.id}`);
  }
  await subscription.unsubscribe();
  return true;
}
