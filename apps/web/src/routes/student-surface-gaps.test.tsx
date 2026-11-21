/**
 * DOM coverage for the three student screens that had no web surface:
 * matches, eligibility and adaptive practice.
 *
 * The API tests prove the payloads. These prove the wiring: matches renders the
 * order and verdicts the API returned, eligibility offers the action that clears
 * each blocker and records contributor terms through `/auth/consent`, and
 * adaptive practice answers the question the API actually served.
 */
import { act, type ReactElement } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { Cbt } from './Cbt';
import { Eligibility } from './Eligibility';
import { Matches } from './Matches';

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

async function waitFor(assertion: () => void, timeoutMs = 1200): Promise<void> {
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
  act(() => {
    root.render(
      <MemoryRouter initialEntries={[path]}>
        <Routes>
          <Route path="*" element={element} />
        </Routes>
      </MemoryRouter>,
    );
  });
  return { root, container };
}

function match(overrides: Record<string, unknown>) {
  return {
    opportunity_id: 1,
    user_id: 7,
    slug: 'data-annotation',
    title: 'Data annotation',
    type: 'managed',
    client_name: 'Nelavista',
    currency: 'NGN',
    rate_minor: 250000,
    headcount: 5,
    eligible: true,
    score: 80,
    blocked: false,
    blocked_reason: null,
    explanation: [],
    missing: [],
    qualifies_because: ['You proved Annotation'],
    next_steps: [],
    facts: {},
    ...overrides,
  };
}

describe('Matches', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('renders the API order, says why a role fits, and names a block', async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        eligible_count: 1,
        matches: [
          match({}),
          match({
            opportunity_id: 2,
            slug: 'translation-review',
            title: 'Translation review',
            type: 'external',
            eligible: false,
            score: 40,
            blocked: true,
            blocked_reason: 'Quality review found a returned submission.',
            qualifies_because: [],
            next_steps: [{ requirement_id: 9, detail: 'Practical task still needed.' }],
          }),
        ],
      }),
    );

    const { root, container } = render(<Matches />, '/opportunities/matches');

    await waitFor(() => expect(container.textContent).toContain('Data annotation'));
    const text = container.textContent ?? '';
    expect(text).toContain('Data annotation');
    expect(text).toContain('Translation review');
    expect(text.indexOf('Data annotation')).toBeLessThan(text.indexOf('Translation review'));
    expect(text).toContain('1 of 2 open roles match');
    expect(text).toContain('80 fit');
    expect(text).toContain('You qualify');
    expect(text).toContain('Quality review found a returned submission.');
    expect(text).toContain('Practical task still needed.');
    expect(calls(fetchMock)[0]?.url).toBe('/api/v1/opportunities/matches');

    act(() => root.unmount());
  });
});

describe('Eligibility', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  const eligibility = {
    eligible: false,
    blockers: ['date_of_birth_missing', 'contributor_terms_required'],
    reasons: [
      'Add your date of birth in Settings so we can apply the age rules.',
      'Read and accept the contributor terms before accepting work.',
    ],
    age: null,
    min_student_age: 16,
    guardian_consent_below_age: 18,
    contributor_terms_version: '2026-10',
    contributor_terms_body: 'Contributors keep ownership of their work.',
  };

  const config = {
    billing_currency: 'NGN',
    payout_currency: 'NGN',
    allowed_currencies: ['NGN'],
    min_student_age: 16,
    guardian_consent_below_age: 18,
    terms_version: '2026-10',
    contributor_terms_version: '2026-10',
    contributor_terms_body: 'Contributors keep ownership of their work.',
    curriculum_owner: 'Nelavista',
    curriculum_license: 'CC BY 4.0',
    curriculum_authoring_model: 'managed',
    target_launch_date: null,
    updated_at: null,
  };

  beforeEach(() => {
    fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes('/platform/me/eligibility')) {
        return Promise.resolve(jsonResponse(200, eligibility));
      }
      if (url.includes('/platform/config')) return Promise.resolve(jsonResponse(200, config));
      if (url.endsWith('/auth/consent')) {
        expect(init?.method).toBe('POST');
        return Promise.resolve(jsonResponse(200, { message: 'Consent recorded.' }));
      }
      return Promise.resolve(jsonResponse(404, { code: 'not_found', message: 'No route' }));
    });
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('names each blocker and records contributor terms against the published version', async () => {
    const { root, container } = render(<Eligibility />, '/eligibility');

    await waitFor(() => expect(container.textContent).toContain('Add your date of birth'));
    const text = container.textContent ?? '';
    expect(text).toContain('Blocked');
    expect(text).toContain('Accept the contributor terms');
    expect(text).toContain('Contributor terms 2026-10');

    const checkbox = container.querySelector('input[type="checkbox"]') as HTMLInputElement;
    await act(async () => {
      checkbox.click();
    });
    const accept = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Accept and record'),
    ) as HTMLButtonElement;
    await act(async () => {
      accept.click();
    });

    await waitFor(() => expect(container.textContent).toContain('accepted'));
    const consent = calls(fetchMock).find((call) => call.url.endsWith('/auth/consent'));
    expect(JSON.parse(String(consent?.init.body))).toEqual({
      kind: 'contributor_terms',
      document_version: '2026-10',
      granted: true,
    });

    act(() => root.unmount());
  });
});

describe('Adaptive practice', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  const onboarding = {
    path: 'academia',
    completed: true,
    enrolments: [
      {
        course_id: 3,
        code: 'SVG101',
        title: 'Surveying',
        university: 'FUTA',
        department: 'Surveying',
        level: '100',
        session: '2025/2026',
      },
    ],
    waitlisted: false,
  };

  beforeEach(() => {
    fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes('/onboarding/state')) return Promise.resolve(jsonResponse(200, onboarding));
      if (url.includes('/cbt/practice-next')) {
        return Promise.resolve(
          jsonResponse(200, {
            course_id: 3,
            focus_topics: [11, 12],
            questions: [
              {
                id: 501,
                topic_id: 11,
                prompt: 'Which instrument measures vertical angles?',
                options: [
                  { key: 'a', text: 'Theodolite' },
                  { key: 'b', text: 'Chain' },
                ],
              },
            ],
          }),
        );
      }
      if (url.endsWith('/cbt/answer')) {
        expect(init?.method).toBe('POST');
        return Promise.resolve(
          jsonResponse(200, {
            attempt_id: 9,
            question_id: 501,
            is_correct: true,
            correct_key: 'a',
            explanation: 'A theodolite reads vertical and horizontal angles.',
          }),
        );
      }
      return Promise.resolve(jsonResponse(404, { code: 'not_found', message: 'No route' }));
    });
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
  });

  it('draws the adaptive set and answers the question the API served', async () => {
    const { root, container } = render(<Cbt />, '/academia/cbt');

    await waitFor(() => expect(container.textContent).toContain('Practise what is weak'));
    const select = container.querySelector('select') as HTMLSelectElement;
    await act(async () => {
      select.value = '3';
      select.dispatchEvent(new Event('change', { bubbles: true }));
    });
    const draw = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Draw 5 questions'),
    ) as HTMLButtonElement;
    await act(async () => {
      draw.click();
    });

    await waitFor(() =>
      expect(container.textContent).toContain('Which instrument measures vertical angles?'),
    );
    expect(container.textContent).toContain('2 weak topics');

    const option = [...container.querySelectorAll('input[type="radio"]')].find(
      (input) => (input as HTMLInputElement).value === 'a',
    ) as HTMLInputElement;
    await act(async () => {
      option.click();
    });
    const check = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Check answer'),
    ) as HTMLButtonElement;
    await act(async () => {
      check.click();
    });

    await waitFor(() => expect(container.textContent).toContain('A theodolite'));

    const practice = calls(fetchMock).find((call) => call.url.includes('/cbt/practice-next'));
    expect(practice?.url).toContain('/api/v1/academia/cbt/practice-next');
    expect(practice?.url).toContain('course_id=');
    expect(String(practice?.url)).toContain('limit=5');

    const answer = calls(fetchMock).find((call) => call.url.endsWith('/cbt/answer'));
    const body = JSON.parse(String(answer?.init.body));
    expect(body.question_id).toBe(501);
    expect(body.selected_key).toBe('a');
    expect(body.client_key).toContain('cbt-adaptive-501');

    act(() => root.unmount());
  });
});
