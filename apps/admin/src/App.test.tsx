/**
 * C1/C8 wiring: a staff login is two steps, and the second step is the only way
 * to obtain a session.
 */
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from './App';

/** React tracks the previous value; the native setter + input event updates it. */
function setInputValue(input: HTMLInputElement, value: string): void {
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')?.set;
  setter?.call(input, value);
  input.dispatchEvent(new Event('input', { bubbles: true }));
}

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

describe('Admin sign in', () => {
  let fetchMock: ReturnType<typeof vi.fn>;
  let root: Root | null = null;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    window.location.hash = '';
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
    if (root) {
      act(() => root?.unmount());
      root = null;
    }
  });

  it('asks for an authenticator code and obtains no session from the password step', async () => {
    // Boot: the refresh cookie is dead, so the app goes anonymous.
    fetchMock.mockImplementation((url: string) => {
      if (String(url).endsWith('/auth/refresh')) return Promise.resolve(jsonResponse(401, {}));
      if (String(url).endsWith('/auth/login')) {
        return Promise.resolve(
          jsonResponse(403, {
            error: {
              code: 'mfa_required',
              message: 'Enter the code from your authenticator app to finish signing in.',
              details: { mfa_token: 'challenge-token' },
            },
          }),
        );
      }
      if (String(url).endsWith('/auth/2fa/verify')) {
        return Promise.resolve(
          jsonResponse(200, {
            access_token: 'access',
            token_type: 'bearer',
            expires_at: '2026-10-18T12:00:00Z',
          }),
        );
      }
      return Promise.resolve(jsonResponse(404, {}));
    });

    const container = document.createElement('div');
    document.body.appendChild(container);
    root = createRoot(container);
    await act(async () => {
      root?.render(<App />);
    });

    await waitFor(() => expect(container.textContent).toContain('Ops sign in'));
    const email = container.querySelector('#admin-email') as HTMLInputElement;
    const password = container.querySelector('#admin-password') as HTMLInputElement;
    await act(async () => {
      setInputValue(email, 'ops@example.test');
      setInputValue(password, 'staff-password-1');
    });

    const form = container.querySelector('form');
    await act(async () => {
      form?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    await waitFor(() => expect(container.querySelector('#mfa-code')).not.toBeNull());
    // The label names the app the code comes from; "code" alone is ambiguous
    // next to the password field the same screen just rendered.
    expect(container.textContent).toContain('Authenticator code');
    // The password response carried no access token, so the shell never appeared.
    expect(container.textContent).not.toContain('Audit trail');
  });
});
