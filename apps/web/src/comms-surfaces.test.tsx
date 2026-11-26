/**
 * The two public/comms surfaces that close the gap between the API and the site:
 * the announcement banner inside the student workspace (read side of
 * `/v1/announcements`) and the newsletter opt-in in the public footer.
 *
 * Both are rendered on their own here. The banner must never block a screen and
 * must remember a dismissal; the form must post exactly one address and must not
 * invent a different answer for a new and an existing subscriber.
 */
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { AnnouncementBanner } from './components/AnnouncementBanner';
import { NewsletterSignup } from './components/NewsletterSignup';
import { clearDismissedAnnouncements } from './lib/announcements';
import { NewsletterConfirm } from './routes/NewsletterConfirm';
import { NewsletterUnsubscribe } from './routes/NewsletterUnsubscribe';

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function setInputValue(input: HTMLInputElement, value: string): void {
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')?.set;
  setter?.call(input, value);
  input.dispatchEvent(new Event('input', { bubbles: true }));
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

let root: Root | null = null;

function mount(node: JSX.Element): HTMLElement {
  const container = document.createElement('div');
  document.body.appendChild(container);
  root = createRoot(container);
  act(() => {
    root?.render(node);
  });
  return container;
}

function announcement(id: number, title: string, body: string) {
  return {
    id,
    title,
    body,
    audience: 'all',
    channel: 'platform',
    status: 'published',
    published_at: '2026-11-12T09:00:00Z',
    archived_at: null,
    email_sent_at: null,
    email_recipient_count: 0,
  };
}

afterEach(() => {
  vi.unstubAllGlobals();
  document.body.innerHTML = '';
  window.localStorage.clear();
  if (root) {
    act(() => root?.unmount());
    root = null;
  }
});

beforeEach(() => {
  clearDismissedAnnouncements();
});

describe('announcement banner', () => {
  it('shows published notices and hides only the one that was dismissed', async () => {
    // A fresh Response per call: a body can only be read once, and this test
    // remounts the banner to prove the dismissal persisted.
    const fetchMock = vi.fn().mockImplementation(() =>
      Promise.resolve(
        jsonResponse(200, {
          announcements: [
            announcement(7, 'Campus closed on Friday', 'Lectures move online for the day.'),
            announcement(6, 'New CBT window open', 'Book a sitting before 30 November.'),
          ],
        }),
      ),
    );
    vi.stubGlobal('fetch', fetchMock);

    const first = mount(<AnnouncementBanner />);
    await waitFor(() => expect(first.textContent).toContain('Campus closed on Friday'));
    expect(first.textContent).toContain('New CBT window open');

    const dismiss = [...first.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Dismiss'),
    );
    act(() => {
      dismiss?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });

    // The first notice is gone; the second is untouched.
    await waitFor(() => expect(first.textContent).not.toContain('Campus closed on Friday'));
    expect(first.textContent).toContain('New CBT window open');
    expect(window.localStorage.getItem('nv.announcements.dismissed')).toContain('7');

    // Remounting reads the stored id, so a reload does not bring it back.
    act(() => root?.unmount());
    root = null;
    const second = mount(<AnnouncementBanner />);
    await waitFor(() => expect(second.textContent).toContain('New CBT window open'));
    expect(second.textContent).not.toContain('Campus closed on Friday');
  });

  it('renders nothing while the read is in flight or after it fails', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse(500, {})));
    const container = mount(<AnnouncementBanner />);
    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 20));
    });
    // An announcement is news, not a dependency: a failed read is silent.
    expect(container.textContent).toBe('');
  });

  it('shows a published notice with no body without leaving an empty gap', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue(
          jsonResponse(200, { announcements: [announcement(9, 'Exam timetable is up', '')] }),
        ),
    );
    const container = mount(<AnnouncementBanner />);
    await waitFor(() => expect(container.textContent).toContain('Exam timetable is up'));
    expect(container.querySelectorAll('p')).toHaveLength(2); // title + published stamp
  });
});

describe('newsletter signup', () => {
  it('posts the address once and confirms without saying whether it was new', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        jsonResponse(201, { subscribed: true, pending: true, email: 'ada@example.test' }),
      );
    vi.stubGlobal('fetch', fetchMock);

    const container = mount(<NewsletterSignup />);
    await act(async () => {
      setInputValue(container.querySelector('#newsletter-email') as HTMLInputElement, 'ada@example.test');
    });
    await act(async () => {
      container
        .querySelector('form')
        ?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    // Double opt-in: the form asks for a click, not claims the address is on.
    await waitFor(() => expect(container.textContent).toContain('Check your inbox'));
    expect(container.textContent).not.toContain('You are on the list');

    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe('/api/v1/newsletter/subscribe');
    expect(init.method).toBe('POST');
    expect(JSON.parse(String(init.body))).toEqual({
      email: 'ada@example.test',
      source: 'web_footer',
    });
    // Wording that would leak list membership ("already subscribed") is absent.
    expect(container.textContent).not.toMatch(/already/i);
  });

  it('surfaces a refusal and keeps the address so it can be corrected', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        jsonResponse(429, {
          error: { code: 'rate_limited', message: 'Too many attempts. Try again in a minute.' },
        }),
      ),
    );

    const container = mount(<NewsletterSignup />);
    await act(async () => {
      setInputValue(container.querySelector('#newsletter-email') as HTMLInputElement, 'ada@example.test');
    });
    await act(async () => {
      container
        .querySelector('form')
        ?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('Too many attempts'));
    expect((container.querySelector('#newsletter-email') as HTMLInputElement).value).toBe('ada@example.test');
  });

  it('does not call the API for an empty address', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);

    const container = mount(<NewsletterSignup />);
    await act(async () => {
      container
        .querySelector('form')
        ?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('Enter the email address'));
    expect(fetchMock).not.toHaveBeenCalled();
  });
});

describe('newsletter confirm page', () => {
  const TOKEN = 'c'.repeat(43);

  function renderAt(path: string): HTMLElement {
    const container = document.createElement('div');
    document.body.appendChild(container);
    root = createRoot(container);
    act(() => {
      root?.render(
        <MemoryRouter initialEntries={[path]}>
          <NewsletterConfirm />
        </MemoryRouter>,
      );
    });
    return container;
  }

  it('waits for a click before confirming the address', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        jsonResponse(200, { subscribed: true, pending: false, email: 'x@example.test' }),
      );
    vi.stubGlobal('fetch', fetchMock);

    const container = renderAt(`/newsletter/confirm?token=${TOKEN}`);
    expect(container.textContent).toContain('Confirm your newsletter subscription?');
    // Opening the link - or a scanner prefetching it - must not confirm by itself.
    expect(fetchMock).not.toHaveBeenCalled();

    const confirm = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Confirm subscription'),
    );
    await act(async () => {
      confirm?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('You are on the list'));
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe('/api/v1/newsletter/confirm');
    expect(JSON.parse(String(init.body))).toEqual({ token: TOKEN });
  });

  it('explains a link that lost its token', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);

    const container = renderAt('/newsletter/confirm');
    expect(container.textContent).toContain('That link is incomplete');
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('keeps the address pending when the token is refused', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        jsonResponse(404, {
          error: {
            code: 'confirm_link_invalid',
            message: 'That confirmation link is not valid.',
          },
        }),
      ),
    );

    const container = renderAt(`/newsletter/confirm?token=${TOKEN}`);
    const confirm = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Confirm subscription'),
    );
    await act(async () => {
      confirm?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('not valid'));
    expect(container.textContent).not.toContain('You are on the list');
  });
});

describe('newsletter unsubscribe page', () => {
  const TOKEN = 'k'.repeat(43);

  function renderAt(path: string): HTMLElement {
    const container = document.createElement('div');
    document.body.appendChild(container);
    root = createRoot(container);
    act(() => {
      root?.render(
        <MemoryRouter initialEntries={[path]}>
          <NewsletterUnsubscribe />
        </MemoryRouter>,
      );
    });
    return container;
  }

  it('waits for a click before changing anything', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(jsonResponse(200, { subscribed: false, email: 'x@example.test' }));
    vi.stubGlobal('fetch', fetchMock);

    const container = renderAt(`/newsletter/unsubscribe?token=${TOKEN}`);
    expect(container.textContent).toContain('Unsubscribe from the newsletter?');
    // Opening the link - or a mail client prefetching it - must not opt anyone out.
    expect(fetchMock).not.toHaveBeenCalled();

    const confirm = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Unsubscribe'),
    );
    await act(async () => {
      confirm?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('You are off the newsletter list'));
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe('/api/v1/newsletter/unsubscribe');
    expect(JSON.parse(String(init.body))).toEqual({ token: TOKEN });
  });

  it('explains a link that lost its token instead of blaming the reader', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);

    const container = renderAt('/newsletter/unsubscribe');
    expect(container.textContent).toContain('That link is incomplete');
    expect(container.textContent).toContain('token=');
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('keeps the reader subscribed when the token is refused', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        jsonResponse(404, {
          error: {
            code: 'unsubscribe_link_invalid',
            message: 'That unsubscribe link is not valid. Use the link in the most recent email.',
          },
        }),
      ),
    );

    const container = renderAt(`/newsletter/unsubscribe?token=${TOKEN}`);
    const confirm = [...container.querySelectorAll('button')].find((button) =>
      button.textContent?.includes('Unsubscribe'),
    );
    await act(async () => {
      confirm?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });

    await waitFor(() => expect(container.textContent).toContain('not valid'));
    expect(container.textContent).toContain('Unsubscribe from the newsletter?');
    expect(container.textContent).not.toContain('You are off the newsletter list');
  });
});
