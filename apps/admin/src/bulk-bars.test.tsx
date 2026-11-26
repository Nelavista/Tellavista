/**
 * Bulk bars for content paths, task templates and practical submissions.
 *
 * Each bar must call its own endpoint with the ticked ids, and must say what
 * the server reported — including the ids that did not take.
 */
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { Content } from './routes/Content';
import { Review } from './routes/Review';

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

async function waitFor(assertion: () => void, timeoutMs = 1000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    try {
      assertion();
      return;
    } catch (err) {
      if (Date.now() > deadline) throw err;
      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 10));
      });
    }
  }
}

function buttonNamed(container: HTMLElement, name: string): HTMLButtonElement {
  const match = Array.from(container.querySelectorAll('button')).find(
    (button) => button.textContent?.trim() === name,
  );
  if (!match) throw new Error(`No button named "${name}"`);
  return match;
}

async function click(element: HTMLElement): Promise<void> {
  await act(async () => {
    element.click();
  });
}

type Call = { method: string; path: string; body: unknown };

const BULK_RESULT = { requested: 2, applied: 1, unchanged: 0, failed: [{ id: 8, code: 'template_not_found' }] };

describe('Admin bulk bars', () => {
  let calls: Call[];
  let root: Root | null = null;
  let container: HTMLDivElement;

  beforeEach(() => {
    calls = [];
    // jsdom has no modal dialog; the confirm step only needs open/close.
    HTMLDialogElement.prototype.showModal ??= function showModal(this: HTMLDialogElement) {
      this.setAttribute('open', '');
    };
    HTMLDialogElement.prototype.close ??= function close(this: HTMLDialogElement) {
      this.removeAttribute('open');
    };
    vi.stubGlobal(
      'fetch',
      vi.fn((url: string, init?: RequestInit) => {
        const path = String(url).replace(/^\/api\/v\d+/, '');
        const method = init?.method ?? 'GET';
        calls.push({ method, path, body: init?.body ? JSON.parse(String(init.body)) : undefined });
        if (method === 'POST' && path.endsWith('/bulk')) return Promise.resolve(jsonResponse(200, BULK_RESULT));
        if (method === 'POST' && path.endsWith('/bulk-review')) {
          return Promise.resolve(jsonResponse(200, { requested: 2, applied: 2, unchanged: 0, failed: [] }));
        }
        if (path === '/skills') return Promise.resolve(jsonResponse(200, { skills: [] }));
        if (path === '/skills/content/validators') return Promise.resolve(jsonResponse(200, { validators: [] }));
        if (path === '/skills/content/lessons') return Promise.resolve(jsonResponse(200, { lessons: [] }));
        if (path === '/skills/content/paths') {
          return Promise.resolve(
            jsonResponse(200, {
              paths: [
                { id: 4, slug: 'intro', title: 'Intro path', level: 'beginner', status: 'draft', steps: [] },
                { id: 5, slug: 'next', title: 'Next path', level: 'beginner', status: 'draft', steps: [] },
              ],
            }),
          );
        }
        if (path === '/skills/content/tasks') {
          return Promise.resolve(
            jsonResponse(200, {
              templates: [
                { id: 7, slug: 'sentiment', name: 'Sentiment', validator: 'exact_key', version: 1, status: 'draft' },
              ],
            }),
          );
        }
        if (path === '/work/review-queue') return Promise.resolve(jsonResponse(200, { queue: [] }));
        if (path.startsWith('/verification/practical/submissions')) {
          return Promise.resolve(
            jsonResponse(200, {
              submissions: [
                { id: 11, practical_task_id: 2, user_id: 30, submitted_at: '2026-11-20T10:00:00Z' },
                { id: 12, practical_task_id: 2, user_id: 31, submitted_at: '2026-11-20T11:00:00Z' },
              ],
            }),
          );
        }
        return Promise.resolve(jsonResponse(404, {}));
      }),
    );
    container = document.createElement('div');
    document.body.appendChild(container);
    root = createRoot(container);
  });

  afterEach(() => {
    if (root) {
      act(() => root?.unmount());
      root = null;
    }
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('publishes the ticked paths through the paths bulk endpoint', async () => {
    await act(async () => root?.render(<Content />));
    await waitFor(() => expect(container.textContent).toContain('Intro path'));

    await click(container.querySelector('input[aria-label="Select Intro path"]') as HTMLInputElement);
    await click(container.querySelector('input[aria-label="Select Next path"]') as HTMLInputElement);
    expect(container.textContent).toContain('2 paths selected');

    await click(buttonNamed(container, 'Publish selected'));

    const bulk = calls.find((call) => call.method === 'POST');
    expect(bulk).toEqual({ method: 'POST', path: '/skills/content/paths/bulk', body: { ids: [4, 5], status: 'published' } });
    // The report names the id that failed instead of claiming the whole batch.
    await waitFor(() => expect(container.textContent).toContain('1 failed: #8 (template_not_found)'));
    expect(container.textContent).not.toContain('paths selected');
  });

  it('archives ticked templates through the tasks bulk endpoint and warns about versions', async () => {
    await act(async () => root?.render(<Content />));
    await waitFor(() => expect(container.textContent).toContain('Sentiment'));

    await click(container.querySelector('input[aria-label="Select Sentiment"]') as HTMLInputElement);
    expect(container.textContent).toContain('1 template selected');
    expect(container.textContent).toContain('Publishing creates a new version of each template.');

    await click(buttonNamed(container, 'Archive'));

    const bulk = calls.find((call) => call.method === 'POST');
    expect(bulk).toEqual({ method: 'POST', path: '/skills/content/tasks/bulk', body: { ids: [7], status: 'archived' } });
  });

  it('passes ticked practical submissions with the bar score', async () => {
    await act(async () => root?.render(<Review />));
    await waitFor(() => expect(container.textContent).toContain('#11'));

    await click(container.querySelector('input[aria-label="Select practical submission 11"]') as HTMLInputElement);
    await click(container.querySelector('input[aria-label="Select practical submission 12"]') as HTMLInputElement);
    await click(buttonNamed(container, 'Pass selected'));

    const bulk = calls.find((call) => call.method === 'POST');
    expect(bulk).toEqual({
      method: 'POST',
      path: '/verification/practical/submissions/bulk-review',
      body: { submission_ids: [11, 12], score: 90, passed: true, notes: null },
    });
    await waitFor(() => expect(container.textContent).toContain('2 passed.'));
  });

  it('asks before failing ticked practical submissions', async () => {
    await act(async () => root?.render(<Review />));
    await waitFor(() => expect(container.textContent).toContain('#12'));

    await click(container.querySelector('input[aria-label="Select practical submission 12"]') as HTMLInputElement);
    await click(buttonNamed(container, 'Fail selected'));

    expect(calls.some((call) => call.method === 'POST')).toBe(false);
    await click(buttonNamed(container, 'Fail 1 submission'));

    const bulk = calls.find((call) => call.method === 'POST');
    expect(bulk?.body).toEqual({ submission_ids: [12], score: 0, passed: false, notes: null });
  });
});
