/**
 * DOM coverage for B8, B9 and F9.
 *
 * These are the wiring checks the API tests cannot make: the list renders the
 * API's own reasons, the assignment form posts the answer object plus a client
 * key, and the emailed verification link is actually consumed by a screen.
 */
import { act, type ReactElement } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { SessionProvider } from '../lib/session';
import { AssignmentDetail } from './AssignmentDetail';
import { Opportunities } from './Opportunities';
import { VerifyEmail } from './VerifyEmail';

type Call = { url: string; init: RequestInit };

function jsonResponse(status: number, body: unknown): Response {
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

function render(
  element: ReactElement,
  path: string,
  { withSession = false }: { withSession?: boolean } = {},
): { root: Root; container: HTMLElement } {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const tree = (
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/opportunities" element={element} />
        <Route path="/work/assignments/:assignmentId" element={element} />
        <Route path="/auth/verify" element={element} />
      </Routes>
    </MemoryRouter>
  );
  act(() => {
    // Only the screen that reads the session needs the provider; wrapping the
    // others would fire a refresh on mount and confuse their call assertions.
    root.render(withSession ? <SessionProvider>{tree}</SessionProvider> : tree);
  });
  return { root, container };
}

describe('Opportunities', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('shows why a student does not qualify yet, using the API reason', async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        opportunities: [
          {
            id: 3,
            slug: 'annotation-pilot',
            type: 'managed',
            title: 'Annotation pilot',
            description: 'Label 1,000 rows.',
            client_name: 'Example Client',
            headcount: 5,
            status: 'open',
            currency: 'USD',
            rate_minor: 150,
            starts_on: null,
            ends_on: null,
            requirements: [],
            match: {
              eligible: false,
              score: 40,
              explanation: [],
              qualifies_because: [],
              next_steps: [
                { requirement_id: 7, detail: 'This skill is not verified yet.', closes_via: {} },
              ],
            },
          },
        ],
      }),
    );

    const { root, container } = render(<Opportunities />, '/opportunities');

    await waitFor(() => expect(container.textContent).toContain('Annotation pilot'));
    expect(container.textContent).toContain('Not yet');
    expect(container.textContent).toContain('To qualify:');
    expect(container.textContent).toContain('This skill is not verified yet.');
    expect(container.textContent).toContain('$1.50');

    act(() => root.unmount());
  });
});

describe('Assignment detail', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  const assignment = {
    id: 12,
    title: 'Label ten rows',
    status: 'in_progress',
    due_at: null,
    project: { slug: 'pilot', title: 'Annotation pilot' },
    task: {
      template_id: 2,
      name: 'Sentiment label',
      instructions_md: 'Label each row positive or negative.',
      input_schema: {
        options: [
          { key: 'positive', label: 'Positive' },
          { key: 'negative', label: 'Negative' },
        ],
      },
      answer_schema: { type: 'object', properties: { key: { type: 'string' } } },
    },
    last_submission: null,
  };

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    localStorage.clear();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('keeps one client key across a failed send and a reload, so a retry is one submission', async () => {
    let posts = 0;
    fetchMock.mockImplementation((url: string, init?: RequestInit) => {
      if (String(url).includes('/messages')) return Promise.resolve(jsonResponse(200, { messages: [] }));
      if (init?.method === 'POST') {
        posts += 1;
        if (posts === 1) {
          return Promise.resolve(
            jsonResponse(500, { error: { code: 'server_error', message: 'Could not save that.' } }),
          );
        }
        return Promise.resolve(
          jsonResponse(201, {
            id: 44,
            status: 'submitted',
            is_gold: false,
            submitted_at: '2026-10-18T11:00:00Z',
            created: true,
            message: 'Submitted for review.',
          }),
        );
      }
      return Promise.resolve(jsonResponse(200, assignment));
    });

    const first = render(<AssignmentDetail />, '/work/assignments/12');

    await waitFor(() => expect(first.container.textContent).toContain('Sentiment label'));
    const choose = (container: HTMLElement): HTMLInputElement =>
      [...container.querySelectorAll('input[type="radio"]')].find(
        (input) => (input as HTMLInputElement).value === 'positive',
      ) as HTMLInputElement;
    const send = (container: HTMLElement): HTMLButtonElement | undefined =>
      [...container.querySelectorAll('button')].find((button) =>
        button.textContent?.includes('Send this work'),
      );

    await act(async () => {
      choose(first.container).click();
    });
    await act(async () => {
      send(first.container)?.click();
    });
    await waitFor(() => expect(first.container.textContent).toContain('Could not save that.'));
    const firstKey = (
      JSON.parse(
        String(calls(fetchMock).filter((call) => call.init.method === 'POST')[0]?.init.body),
      ) as { client_key: string }
    ).client_key;
    expect(firstKey).toMatch(/^web-/);
    expect(firstKey.length).toBeLessThanOrEqual(64);

    // A reload after the failed send: the answer and the key both come back.
    act(() => first.root.unmount());
    document.body.innerHTML = '';
    const second = render(<AssignmentDetail />, '/work/assignments/12');
    await waitFor(() => expect(choose(second.container).checked).toBe(true));

    await act(async () => {
      send(second.container)?.click();
    });
    await waitFor(() => expect(second.container.textContent).toContain('Submitted for review.'));

    const bodies = calls(fetchMock)
      .filter((call) => call.init.method === 'POST')
      .map((call) => JSON.parse(String(call.init.body)) as { payload: unknown; client_key: string });
    expect(bodies).toHaveLength(2);
    expect(bodies[0]?.payload).toEqual({ key: 'positive' });
    expect(bodies[1]?.client_key).toBe(firstKey);

    act(() => second.root.unmount());
  });
});

describe('Verify email landing', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('posts the token once and confirms the address', async () => {
    // The provider tries to restore the session on mount; this test is signed
    // out, so the refresh fails and the page stays usable (the link may open on
    // a different device).
    fetchMock.mockImplementation(async (url: string, init?: RequestInit) => {
      const target = String(url);
      if (target.endsWith('/auth/refresh')) return jsonResponse(401, { error: { code: 'unauthenticated' } });
      if (target.endsWith('/auth/email/verify')) {
        expect(init?.method).toBe('POST');
        return jsonResponse(200, {
          id: 1,
          email: 'student@example.test',
          username: 'student',
          email_verified: true,
          role: 'student',
          preferred_path: null,
          mfa_enabled: false,
        });
      }
      return jsonResponse(404, { error: { code: 'not_found' } });
    });

    const { root, container } = render(<VerifyEmail />, '/auth/verify?token=abc1234567890', {
      withSession: true,
    });

    await waitFor(() => expect(container.textContent).toContain('Email confirmed'));
    expect(container.textContent).toContain('student@example.test');
    const posts = calls(fetchMock).filter((call) => call.url.endsWith('/auth/email/verify'));
    expect(posts).toHaveLength(1);
    expect(posts[0]?.url).toBe('/api/v1/auth/email/verify');
    expect(JSON.parse(String(posts[0]?.init.body))).toEqual({ token: 'abc1234567890' });

    act(() => root.unmount());
  });
});
