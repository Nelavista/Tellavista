/**
 * Product analytics and error tracking for the student web app.
 *
 * PostHog is the one third-party service we send product events to, because the
 * API already uses it for server-side journey events. No Sentry project is used.
 *
 * Two constraints shape this module:
 *
 * * **No key, no code path.** An unset `VITE_POSTHOG_KEY` is a complete no-op,
 *   and the SDK is only imported when the key exists, so the first-load bundle
 *   does not grow in an environment without analytics.
 * * **No silent PII.** Persistence is memory-only (no analytics cookie), text
 *   capture is masked, session recording is off, and share URLs are normalised
 *   before a page view leaves the browser.
 *
 * Errors are reported explicitly from the error boundary and automatically from
 * `error` / `unhandledrejection`, so a render crash and a failed fetch both reach
 * the same place as the API's own `$exception` events.
 */
type PostHogClient = import('posthog-js').PostHog;

interface QueuedEvent {
  event: string;
  properties: Record<string, unknown>;
}

const KEY = import.meta.env.VITE_POSTHOG_KEY as string | undefined;
const HOST = (import.meta.env.VITE_POSTHOG_HOST as string | undefined) || 'https://us.i.posthog.com';

let client: PostHogClient | null = null;
let started = false;
const queue: QueuedEvent[] = [];

function safePath(path: string): string {
  // A shared-profile token is a bearer grant. It is never sent to analytics.
  if (path.startsWith('/share/')) return '/share/:token';
  return path;
}

function enqueue(event: string, properties: Record<string, unknown>): void {
  if (!KEY) return;
  if (client) {
    client.capture(event, properties);
    return;
  }
  // Keep the queue short: analytics is best effort and must not grow unbounded
  // while a slow network delays the SDK.
  if (queue.length < 50) queue.push({ event, properties });
}

export function capturePageview(pathname: string): void {
  enqueue('$pageview', {
    $current_url: `${window.location.origin}${safePath(pathname)}`,
    path: safePath(pathname),
  });
}

export function capture(event: string, properties: Record<string, unknown> = {}): void {
  enqueue(event, properties);
}

export function identify(userId: number | string, properties: Record<string, unknown> = {}): void {
  if (!KEY) return;
  if (client) {
    client.identify(String(userId), properties);
    return;
  }
  enqueue('$identify', { distinct_id: String(userId), $set: properties });
}

export function reset(): void {
  queue.length = 0;
  client?.reset();
}

export function reportError(error: unknown, context: Record<string, unknown> = {}): void {
  if (!KEY) return;
  const value = error instanceof Error ? error : new Error(String(error));
  enqueue('$exception', {
    $exception_list: [
      {
        type: value.name || 'Error',
        value: value.message,
        stacktrace: value.stack ?? '',
        mechanism: { handled: true, synthetic: false },
      },
    ],
    ...context,
  });
}

/**
 * Start the SDK, if this build has a key.
 *
 * Idempotent: every entry point may call it, but only the first call installs
 * the global handlers and loads the SDK.
 */
export function initTelemetry(): void {
  if (!KEY || started) return;
  started = true;

  window.addEventListener('error', (event) => {
    reportError(event.error ?? event.message, { source: 'window.error' });
  });
  window.addEventListener('unhandledrejection', (event) => {
    reportError(event.reason, { source: 'unhandledrejection' });
  });

  void import('posthog-js')
    .then(({ default: posthog }) => {
      posthog.init(KEY, {
        api_host: HOST,
        capture_pageview: false,
        capture_pageleave: false,
        autocapture: false,
        disable_session_recording: true,
        person_profiles: 'identified_only',
        persistence: 'memory',
        mask_all_text: true,
        mask_all_element_attributes: true,
        capture_exceptions: true,
      });
      client = posthog;
      for (const item of queue.splice(0)) posthog.capture(item.event, item.properties);
    })
    .catch(() => {
      // A blocked CDN or an ad blocker must not break the app. The console still
      // receives the original error through the error boundary.
    });
}
