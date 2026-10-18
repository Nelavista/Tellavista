/**
 * DOM coverage for the skills screens (B6).
 *
 * The compile and the bundle prove the screens exist; they do not prove they are
 * wired to the API correctly. These tests render the real components in jsdom with
 * `fetch` mocked, and assert the two things that matter most:
 *
 * * the practice form is generated from the template's schemas and the payload it
 *   posts is the answer object the validator expects;
 * * a 404 from a flagged-out router reads as "not switched on here", not an error.
 */
import { act, type ReactElement } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { Practice } from './Practice';
import { Skills } from './Skills';

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

/** Poll until the assertion passes, so a discarded render does not flake the test. */
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

function render(element: ReactElement, path = '/'): { root: Root; container: HTMLElement } {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const tree = (
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/skills/practice/:templateId" element={element} />
        <Route path="/skills" element={element} />
      </Routes>
    </MemoryRouter>
  );
  act(() => {
    root.render(tree);
  });
  return { root, container };
}

describe('Practice screen', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('posts the answer object the schema asks for', async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        template_id: 7,
        slug: 'sentiment',
        name: 'Sentiment label',
        instructions_md: 'Label the text positive or negative.',
        input_schema: {
          text: 'I loved it',
          options: [
            { key: 'positive', label: 'Positive' },
            { key: 'negative', label: 'Negative' },
          ],
        },
        answer_schema: { type: 'object', properties: { key: { type: 'string' } } },
        sample: null,
        version: 1,
      }),
    );
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        attempt_id: 3,
        is_correct: true,
        score: 100,
        feedback: 'Correct.',
        details: {},
        counts_as_verification: false,
      }),
    );

    const { root, container } = render(<Practice />, '/skills/practice/7');

    await waitFor(() => expect(container.textContent).toContain('Sentiment label'));

    const positive = [...container.querySelectorAll('input[type="radio"]')].find(
      (input) => (input as HTMLInputElement).value === 'positive',
    ) as HTMLInputElement;
    expect(positive).toBeDefined();

    await act(async () => {
      positive.click();
    });

    const submit = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Check my answer'),
    );
    await act(async () => {
      submit?.click();
    });

    await waitFor(() => expect(container.textContent).toContain('Correct'));

    const post = calls(fetchMock).find((call) => call.init.method === 'POST');
    expect(post?.url).toBe('/api/v1/skills/tasks/7/practice');
    expect(JSON.parse(String(post?.init.body))).toEqual({ answer: { key: 'positive' } });
    // The verdict is feedback from a sandbox, and the page must keep saying so.
    expect(container.textContent).toContain('not verification');

    act(() => root.unmount());
  });

  it('declines a task type it cannot render instead of submitting', async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        template_id: 8,
        slug: 'spans',
        name: 'Tag entities',
        instructions_md: '',
        input_schema: { text: 'Ada Lovelace wrote notes.' },
        answer_schema: { type: 'object', properties: { spans: { type: 'array' } } },
        sample: null,
        version: 1,
      }),
    );

    const { root, container } = render(<Practice />, '/skills/practice/8');

    await waitFor(() => expect(container.textContent).toContain('not built yet'));
    expect(calls(fetchMock).some((call) => call.init.method === 'POST')).toBe(false);

    act(() => root.unmount());
  });
});

describe('Skills screen', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('reads a flagged-out router as "not switched on", not as an error', async () => {
    fetchMock.mockResolvedValue(
      jsonResponse(404, { error: { code: 'not_found', message: 'This feature is not available.' } }),
    );

    const { root, container } = render(<Skills />, '/skills');

    await waitFor(() => expect(container.textContent).toContain('not switched on for this environment'));
    expect(container.querySelector('[role="alert"]')).toBeNull();

    act(() => root.unmount());
  });

  it('lists the published skills', async () => {
    fetchMock.mockResolvedValue(
      jsonResponse(200, {
        skills: [
          {
            id: 1,
            slug: 'ai-data-annotation',
            name: 'AI Data Annotation',
            description: 'Label data well.',
            category: 'AI & Data',
            category_slug: 'ai-data',
            published_paths: 1,
          },
        ],
      }),
    );

    const { root, container } = render(<Skills />, '/skills');

    await waitFor(() => expect(container.textContent).toContain('AI Data Annotation'));
    expect(container.textContent).toContain('1 path available');

    act(() => root.unmount());
  });
});
