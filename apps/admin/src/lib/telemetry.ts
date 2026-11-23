/**
 * Analytics and error tracking for the ops app.
 *
 * Same provider and rules as the student web app: PostHog, no Sentry, memory-only
 * persistence, masked text, no session recording, and a complete no-op when the
 * build has no `VITE_POSTHOG_KEY`. The admin app is internal, so its page views
 * are hash routes and never contain a student token.
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

function enqueue(event: string, properties: Record<string, unknown>): void {
  if (!KEY) return;
  if (client) {
    client.capture(event, properties);
    return;
  }
  if (queue.length < 50) queue.push({ event, properties });
}

export function capturePageview(route: string): void {
  enqueue('$pageview', {
    $current_url: `${window.location.origin}${window.location.pathname}#${route}`,
    path: route,
    app: 'admin',
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
    app: 'admin',
    ...context,
  });
}

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
      // Blocked analytics must not take the ops tools offline.
    });
}
