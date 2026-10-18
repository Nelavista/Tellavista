/**
 * DOM coverage for the verification screens (B7).
 *
 * The API tests prove the shapes; these prove the wiring the student actually
 * touches:
 *
 * * a sitting posts `{answers: {task_id: answer}}` — the object the grader reads,
 *   not an array of answers in screen order;
 * * an unsupported task is never counted as answered;
 * * an unproved skill says out loud that lessons are not proof.
 */
import { act, type ReactElement } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { AssessmentSitting } from './AssessmentSitting';
import { Verification } from './Verification';

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

function render(element: ReactElement, path = '/'): { root: Root; container: HTMLElement } {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const tree = (
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/verification" element={element} />
        <Route path="/verification/assessments/:assessmentSlug" element={element} />
      </Routes>
    </MemoryRouter>
  );
  act(() => {
    root.render(tree);
  });
  return { root, container };
}

const STARTED_AT = '2026-10-18T10:00:00Z';
const EXPIRES_AT = '2026-10-19T10:00:00Z';
const ANSWER_SCHEMA = { type: 'object', properties: { key: { type: 'string' } } };
const INPUT_SCHEMA = {
  options: [
    { key: 'positive', label: 'Positive' },
    { key: 'negative', label: 'Negative' },
  ],
};

function sitting() {
  return {
    attempt_id: 11,
    assessment_id: 1,
    started_at: STARTED_AT,
    expires_at: EXPIRES_AT,
    tasks: [
      {
        task_id: 5,
        ordinal: 1,
        payload: { text: 'I love it' },
        points: 1,
        template_id: 2,
        input_schema: INPUT_SCHEMA,
        answer_schema: ANSWER_SCHEMA,
      },
      {
        task_id: 6,
        ordinal: 2,
        payload: { text: 'I hate it' },
        points: 1,
        template_id: 2,
        input_schema: INPUT_SCHEMA,
        answer_schema: ANSWER_SCHEMA,
      },
    ],
  };
}

describe('Assessment sitting', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('posts answers keyed by task id and shows the graded result', async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse(200, sitting()));
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        attempt_id: 11,
        score: 50,
        passed: false,
        expired: false,
        pass_threshold: 80,
        verification_status: 'in_progress',
        tasks: [
          { task_id: 5, ordinal: 1, correct: true, points: 1, max_points: 1, feedback: 'Correct.' },
          {
            task_id: 6,
            ordinal: 2,
            correct: false,
            points: 0,
            max_points: 1,
            feedback: 'That is not the right key.',
          },
        ],
      }),
    );

    const { root, container } = render(<AssessmentSitting />, '/verification/assessments/annotation');

    await waitFor(() => expect(container.textContent).toContain('I love it'));
    // Starting is a POST, and the page names the expiry so the sitting is honest.
    const start = calls(fetchMock)[0];
    expect(start?.url).toBe('/api/v1/verification/assessments/annotation/start');
    expect(start?.init.method).toBe('POST');

    const positive = [...container.querySelectorAll('input[type="radio"]')].find(
      (input) => (input as HTMLInputElement).value === 'positive',
    ) as HTMLInputElement | undefined;
    expect(positive).toBeDefined();

    await act(async () => {
      positive?.click();
    });

    const submit = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Submit this sitting'),
    );
    await act(async () => {
      submit?.click();
    });

    await waitFor(() => expect(container.textContent).toContain('Not passed yet'));

    const post = calls(fetchMock).find((call) => call.init.method === 'POST' && call.url.endsWith('/submit'));
    expect(post?.url).toBe('/api/v1/verification/attempts/11/submit');
    expect(JSON.parse(String(post?.init.body))).toEqual({ answers: { 5: { key: 'positive' } } });
    expect(container.textContent).toContain('pass mark 80%');

    act(() => root.unmount());
  });

  it('does not count a task it cannot render as answered', async () => {
    const attempt = sitting();
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        ...attempt,
        tasks: [
          {
            task_id: 9,
            ordinal: 1,
            payload: { text: 'Tag the entities' },
            points: 2,
            template_id: null,
            input_schema: null,
            answer_schema: null,
          },
        ],
      }),
    );

    const { root, container } = render(<AssessmentSitting />, '/verification/assessments/spans');

    await waitFor(() => expect(container.textContent).toContain('not attached to a task template'));
    const submit = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Submit this sitting'),
    ) as HTMLButtonElement;
    expect(submit.disabled).toBe(true);
    expect(calls(fetchMock).some((call) => call.url.endsWith('/submit'))).toBe(false);

    act(() => root.unmount());
  });
});

describe('Verification hub', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('says an unproved skill is not proof and links to a real assessment', async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        skills: [
          {
            skill_id: 1,
            skill: 'AI Data Annotation',
            slug: 'ai-data-annotation',
            status: 'unverified',
            verified_at: null,
            last_evaluated_at: null,
            verified: false,
          },
        ],
      }),
    );
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        assessments: [
          {
            id: 2,
            slug: 'annotation-check',
            title: 'Annotation check',
            skill_id: 1,
            pass_threshold: 80,
            max_attempts: 3,
            task_count: 5,
          },
        ],
      }),
    );

    const { root, container } = render(<Verification />, '/verification');

    await waitFor(() => expect(container.textContent).toContain('Annotation check'));
    expect(container.textContent).toContain('Not proved yet');
    expect(container.textContent).toContain('Lessons and practice are progress, not proof');
    expect(container.querySelector('a[href="/verification/assessments/annotation-check"]')).not.toBeNull();
    expect(container.querySelector('.nv-badge[data-status="unverified"]')).not.toBeNull();

    act(() => root.unmount());
  });
});
