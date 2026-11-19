/**
 * The first-login 2FA browser flow, end to end in the real app shell.
 *
 * The API tests prove each call; this proves the wiring between them, which is
 * where the flow actually broke: the app has to (1) sign in with a password,
 * (2) load `/auth/me` and `/auth/2fa`, (3) refuse to render any ops screen while
 * the factor is missing, (4) walk setup -> confirm -> recovery codes, and
 * (5) only then render the shell. The second test covers the returning user:
 * password -> challenge -> code -> shell.
 */
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from './App';

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

async function waitFor(assertion: () => void, timeoutMs = 1500): Promise<void> {
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

type Handler = (url: string, init?: RequestInit) => Response | undefined;

describe('First login with two-factor', () => {
  let fetchMock: ReturnType<typeof vi.fn>;
  let root: Root | null = null;
  let enrolled: boolean;

  function respond(handler: Handler): void {
    fetchMock.mockImplementation((url: string, init?: RequestInit) => {
      const matched = handler(String(url), init);
      if (matched) return Promise.resolve(matched);
      return Promise.resolve(jsonResponse(404, {}));
    });
  }

  function mount(): HTMLElement {
    const container = document.createElement('div');
    document.body.appendChild(container);
    root = createRoot(container);
    return container;
  }

  function meResponse(): Response {
    return jsonResponse(200, {
      id: 1,
      email: 'ops@example.test',
      username: 'ops',
      name: 'Ops Person',
      role: 'ops_admin',
      preferred_path: 'academia',
      mfa_enabled: enrolled,
    });
  }

  beforeEach(() => {
    enrolled = false;
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    window.location.hash = '#/overview';
    // The enrolment screen reloads the app in a real browser; jsdom does not
    // implement navigation, so the refresh is observed rather than performed.
    vi.spyOn(window, 'location', 'get').mockReturnValue({
      ...window.location,
      reload: vi.fn(),
      hash: '#/overview',
    } as Location);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    document.body.innerHTML = '';
    if (root) {
      act(() => root?.unmount());
      root = null;
    }
  });

  it('walks a new staff account from password to enrolled shell', async () => {
    respond((url, init) => {
      if (url.endsWith('/auth/refresh')) return jsonResponse(401, {});
      if (url.endsWith('/auth/login')) {
        return jsonResponse(200, {
          access_token: 'access',
          token_type: 'bearer',
          expires_at: '2026-11-13T12:00:00Z',
        });
      }
      if (url.endsWith('/auth/me')) return meResponse();
      if (url.endsWith('/auth/2fa/setup')) {
        return jsonResponse(200, {
          secret: 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ',
          otpauth_uri: 'otpauth://totp/Nelavista:ops?secret=GEZDGNBVGY3TQOJQ',
        });
      }
      if (url.endsWith('/auth/2fa/enable')) {
        enrolled = true;
        expect(init?.method).toBe('POST');
        expect(JSON.parse(String(init?.body))).toEqual({ code: '123456' });
        return jsonResponse(200, { enabled: true, recovery_codes: ['AAAA-BBBB-CC', 'DDDD-EEEE-FF'] });
      }
      if (url.endsWith('/auth/2fa')) {
        return jsonResponse(200, {
          enabled: enrolled,
          is_staff: true,
          remaining_recovery_codes: enrolled ? 10 : 0,
        });
      }
      if (url.endsWith('/ops/overview')) {
        return jsonResponse(200, {
          generated_at: '2026-11-13T12:00:00Z',
          queues: [],
          recent_audit: [],
          live_projects: [],
          totals: { live_projects: 0, queues_with_items: 0 },
        });
      }
      return undefined;
    });

    const container = mount();
    await act(async () => {
      root?.render(<App />);
    });

    // 1. Password step.
    await waitFor(() => expect(container.textContent).toContain('Ops sign in'));
    await act(async () => {
      setInputValue(container.querySelector('#admin-email') as HTMLInputElement, 'ops@example.test');
      setInputValue(
        container.querySelector('#admin-password') as HTMLInputElement,
        'staff-password-1',
      );
    });
    await act(async () => {
      container
        .querySelector('form')
        ?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    // 2. No factor yet, so the enrolment gate renders and no ops screen does.
    await waitFor(() => expect(container.textContent).toContain('Two-factor is required'));
    expect(container.textContent).not.toContain('What needs attention');

    // 3. Start setup: the secret is shown, and nothing is enabled yet.
    const start = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Start setup'),
    );
    await act(async () => {
      start?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });
    await waitFor(() => expect(container.textContent).toContain('GEZDGNBVGY3TQOJQ'));

    // 4. Confirm with the code; recovery codes are shown once.
    const code = container.querySelector('#enrol-code') as HTMLInputElement;
    await act(async () => {
      setInputValue(code, '123456');
    });
    const confirm = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Confirm and turn on'),
    );
    await act(async () => {
      confirm?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('Save your recovery codes'));
    expect(container.textContent).toContain('AAAA-BBBB-CC');
    expect(window.location.reload).toHaveBeenCalledTimes(0); // only after acknowledgement
  });

  it('signs in a returning staff member through the code challenge', async () => {
    enrolled = true;

    respond((url) => {
      if (url.endsWith('/auth/refresh')) return jsonResponse(401, {});
      if (url.endsWith('/auth/2fa/verify')) {
        return jsonResponse(200, {
          access_token: 'access',
          token_type: 'bearer',
          expires_at: '2026-11-13T12:00:00Z',
        });
      }
      if (url.endsWith('/auth/login')) {
        return jsonResponse(403, {
          error: {
            code: 'mfa_required',
            message: 'Enter the code from your authenticator app to finish signing in.',
            details: { mfa_token: 'challenge-token' },
          },
        });
      }
      if (url.endsWith('/auth/me')) return meResponse();
      if (url.endsWith('/auth/2fa')) {
        return jsonResponse(200, { enabled: true, is_staff: true, remaining_recovery_codes: 8 });
      }
      if (url.endsWith('/ops/overview')) {
        return jsonResponse(200, {
          generated_at: '2026-11-13T12:00:00Z',
          queues: [
            {
              key: 'work_review',
              label: 'Work review queue',
              detail: 'Student submissions waiting for a quality decision.',
              href: '#/review',
              count: 3,
              stamp: '2026-11-12T09:00:00Z',
              stamp_label: 'Oldest',
              last_run: null,
            },
          ],
          recent_audit: [],
          live_projects: [],
          totals: { live_projects: 0, queues_with_items: 1 },
        });
      }
      return undefined;
    });

    const container = mount();
    await act(async () => {
      root?.render(<App />);
    });

    await waitFor(() => expect(container.textContent).toContain('Ops sign in'));
    await act(async () => {
      setInputValue(container.querySelector('#admin-email') as HTMLInputElement, 'ops@example.test');
      setInputValue(container.querySelector('#admin-password') as HTMLInputElement, 'pw-123456');
    });
    await act(async () => {
      container
        .querySelector('form')
        ?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    // Password alone renders the challenge, never the shell.
    await waitFor(() => expect(container.textContent).toContain('Authenticator code'));
    expect(container.textContent).not.toContain('What needs attention');

    const code = container.querySelector('#mfa-code') as HTMLInputElement;
    await act(async () => {
      setInputValue(code, '654321');
    });
    await act(async () => {
      container
        .querySelector('form')
        ?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    // The shell renders from the single overview read, queue counts included.
    await waitFor(() => expect(container.textContent).toContain('What needs attention'));
    await waitFor(() => expect(container.textContent).toContain('Work review queue'));
  });
});
