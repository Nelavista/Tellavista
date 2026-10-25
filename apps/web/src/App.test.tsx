/**
 * `/` is the landing page for people who are not signed in.
 *
 * Signed-in students who opened the bare host used to get the marketing hero —
 * "Create your account" / "I already have one" — under a signed-in nav, because
 * the root route was the only one of the three entry routes without the
 * public-only guard. The route now matches /login and /signup: a restored
 * session continues to /home.
 */
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from './App';
import { setAccessToken } from './lib/http';

// Only the route decision is under test; Home reads a dashboard of its own.
vi.mock('./routes/Home', () => ({ Home: () => <div>home screen</div> }));

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

// One app per test, and every root is torn down afterwards: a leftover render
// keeps its markup in document.body and the next assertion reads both screens.
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

describe('root route', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    for (const { root, container } of mounted.splice(0)) {
      act(() => root.unmount());
      container.remove();
    }
    setAccessToken(null);
    vi.unstubAllGlobals();
  });

  it('shows the landing page to a signed-out visitor', async () => {
    fetchMock.mockImplementation((url: string) => {
      if (String(url).endsWith('/auth/refresh')) {
        return Promise.resolve(jsonResponse(401, { error: { code: 'unauthenticated' } }));
      }
      return Promise.resolve(jsonResponse(404, { error: { code: 'not_found' } }));
    });

    const { container } = render('/');

    await waitFor(() => {
      expect(container.textContent).toContain('Create your account');
    });
  });

  it('continues a signed-in visitor to /home instead of the landing page', async () => {
    fetchMock.mockImplementation((url: string) => {
      const target = String(url);
      if (target.endsWith('/auth/refresh')) {
        return Promise.resolve(jsonResponse(200, { access_token: 'token' }));
      }
      if (target.endsWith('/auth/me')) {
        return Promise.resolve(
          jsonResponse(200, {
            id: 1,
            email: 'student@example.com',
            username: 'student',
            name: 'Student',
            roles: ['student'],
            permissions: [],
          }),
        );
      }
      if (target.endsWith('/me')) {
        return Promise.resolve(
          jsonResponse(200, { onboarding_completed_at: null, path: null }),
        );
      }
      return Promise.resolve(jsonResponse(404, { error: { code: 'not_found' } }));
    });

    const { container } = render('/');

    await waitFor(() => {
      expect(container.textContent).toContain('home screen');
    });
    expect(container.textContent).not.toContain('Create your account');
  });
});
