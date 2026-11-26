/**
 * Finishing the newsletter opt-in, from the link in the confirmation email.
 *
 * The click is the consent, so it must be a click: mail clients and link
 * scanners fetch URLs, and a prefetch must not confirm an address nobody asked
 * for. The token, not the address, is in the link; the page never echoes an
 * email address it was not given.
 */
import type { NewsletterSubscribeOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useSearchParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { Banner, Button } from '../ui';

type State = 'confirm' | 'busy' | 'done';

export function NewsletterConfirm(): JSX.Element {
  const [params] = useSearchParams();
  const token = params.get('token');
  const [state, setState] = React.useState<State>('confirm');
  const [error, setError] = React.useState<string | null>(null);

  async function confirm(): Promise<void> {
    if (!token) return;
    setState('busy');
    setError(null);
    try {
      await http.post<NewsletterSubscribeOut>('/newsletter/confirm', { token });
      setState('done');
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : 'Could not reach the server. The address is unchanged; try again.',
      );
      setState('confirm');
    }
  }

  if (!token) {
    return (
      <section className="nv-container nv-section">
        <h1 className="nv-h1">That link is incomplete</h1>
        <p className="nv-lede">
          The confirmation link needs its full address, including the part after <code>token=</code>.
          Open the link from the most recent confirmation email.
        </p>
        <div className="nv-row">
          <Link className="nv-button nv-button--secondary" to="/">
            Back to Nelavista
          </Link>
        </div>
      </section>
    );
  }

  if (state === 'done') {
    return (
      <section className="nv-container nv-section">
        <h1 className="nv-h1">You are on the list</h1>
        <p className="nv-lede">
          We send one note a month: new material, open opportunities and what changed on the
          platform. Every issue carries its own unsubscribe link.
        </p>
        <div className="nv-row">
          <Link className="nv-button nv-button--secondary" to="/">
            Back to Nelavista
          </Link>
        </div>
      </section>
    );
  }

  return (
    <section className="nv-container nv-section">
      <h1 className="nv-h1">Confirm your newsletter subscription?</h1>
      <p className="nv-lede">
        This confirms that you asked for the monthly Nelavista newsletter. Nothing is sent until you
        click below.
      </p>
      {error ? <Banner tone="danger">{error}</Banner> : null}
      <div className="nv-row">
        <Button disabled={state === 'busy'} onClick={() => void confirm()} type="button">
          {state === 'busy' ? 'Confirming' : 'Confirm subscription'}
        </Button>
        <Link className="nv-button nv-button--ghost" to="/">
          No thanks
        </Link>
      </div>
    </section>
  );
}
