/**
 * Public routes render as separate pages and an unknown path is a real 404.
 *
 * These screens must not require a session. The only network call is the
 * session refresh probe, which is answered with 401 here.
 */
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from './App';
import { setAccessToken } from './lib/http';
import { expectNoA11yViolations } from './test-a11y';

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

interface Mounted {
  root: Root;
  container: HTMLElement;
}

const mounted: Mounted[] = [];

function render(path: string): Mounted {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  act(() => {
    root.render(
      <MemoryRouter initialEntries={[path]}>
        <App />
      </MemoryRouter>,
    );
  });
  const entry = { root, container };
  mounted.push(entry);
  return entry;
}

// Public routes are lazy-loaded. On a cold Vitest run (especially on a slow or
// network-backed checkout) resolving the route module can take more than a
// second, so give the first paint a realistic budget instead of turning a slow
// module load into a false product failure.
async function waitFor(assertion: () => void, timeoutMs = 5000): Promise<void> {
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

describe('public routes', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn((url: string) => {
        if (String(url).endsWith('/auth/refresh')) {
          return Promise.resolve(jsonResponse(401, { error: { code: 'unauthenticated' } }));
        }
        if (String(url).endsWith('/platform/impact')) {
          return Promise.resolve(
            jsonResponse(200, {
              generated_at: '2026-11-23T10:00:00Z',
              enabled: true,
              metrics: [
                {
                  key: 'published_skills',
                  label: 'Published skills',
                  value: 94,
                  detail: 'Skills a student can learn and be assessed in.',
                },
                {
                  key: 'verified_skills',
                  label: 'Verified skills',
                  value: 0,
                  detail: 'Skill verifications backed by an assessment or practical task.',
                },
              ],
              paid_by_currency: [],
            }),
          );
        }
        return Promise.resolve(jsonResponse(404, { error: { code: 'not_found' } }));
      }),
    );
  });

  afterEach(() => {
    for (const { root, container } of mounted.splice(0)) {
      act(() => root.unmount());
      container.remove();
    }
    setAccessToken(null);
    vi.unstubAllGlobals();
  });

  it('renders the features page with public metadata', async () => {
    const { container } = render('/features');
    await waitFor(() => {
      expect(container.textContent).toContain('CBT practice');
      expect(document.title).toBe('Features | Nelavista');
    });
    expect(document.head.querySelector('link[rel="canonical"]')?.getAttribute('href')).toBe(
      'https://nelavista.com/features',
    );
    expect(document.head.querySelector('meta[name="robots"]')?.getAttribute('content')).toBe('index, follow');
    await expectNoA11yViolations(container);
  });

  it('renders the FAQ page', async () => {
    const { container } = render('/faq');
    await waitFor(() => {
      expect(container.textContent).toContain('Who is Nelavista for?');
    });
    await expectNoA11yViolations(container);
  });

  it('renders the impact page with the live figures the API returns', async () => {
    const { container } = render('/impact');
    await waitFor(() => {
      expect(container.textContent).toContain('Make the work easier to trust.');
      expect(container.textContent).toContain('Published skills');
      expect(container.textContent).toContain('94');
      expect(document.title).toBe('Impact | Nelavista');
    });
    // A zero is shown rather than hidden; the page does not substitute copy for
    // a count the database actually returned.
    expect(container.textContent).toContain('Verified skills');
    expect(container.textContent).not.toContain('publishes no reach figures');
    await expectNoA11yViolations(container);
  });

  it('renders the offline page', async () => {
    const { container } = render('/offline');
    await waitFor(() => {
      expect(container.textContent).toContain('The shell is here. The data is not.');
    });
    await expectNoA11yViolations(container);
  });

  it('renders a real 404 for an unknown public path and marks it noindex', async () => {
    const { container } = render('/this-page-does-not-exist');
    await waitFor(() => {
      expect(container.textContent).toContain('That page is not part of the record.');
      expect(document.title).toBe('Page not found | Nelavista');
    });
    expect(document.head.querySelector('meta[name="robots"]')?.getAttribute('content')).toBe(
      'noindex, nofollow',
    );
    await expectNoA11yViolations(container);
  });
});
