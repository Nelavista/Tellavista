/**
 * Leaving the newsletter, from the link in the email.
 *
 * Two deliberate choices:
 *
 * * the link does not unsubscribe on load. Mail clients and link scanners fetch
 *   URLs, and a prefetch must not opt someone out of a list they still want to
 *   be on -- so the token is shown back as a confirmation step, and the POST is
 *   the only thing that changes the record;
 * * the token, not the address, is in the link. It is the whole authorisation,
 *   so the page never echoes an email address it was not given.
 */
import * as React from 'react';
import { Link, useSearchParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { Banner, Button } from '../ui';

type State = 'confirm' | 'busy' | 'done';

export function NewsletterUnsubscribe(): JSX.Element {
  const [params] = useSearchParams();
  const token = params.get('token');
  const [state, setState] = React.useState<State>('confirm');
  const [error, setError] = React.useState<string | null>(null);

  async function unsubscribe(): Promise<void> {
    if (!token) return;
    setState('busy');
    setError(null);
    try {
      await http.post('/newsletter/unsubscribe', { token });
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
          The unsubscribe link needs its full address, including the part after <code>token=</code>. Open the
          link from the most recent newsletter email, or reply to it and we will remove you.
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
        <h1 className="nv-h1">You are off the newsletter list</h1>
        <p className="nv-lede">
          We will not send you another issue. Your record on Nelavista is untouched: courses, proof and
          earnings are unaffected.
        </p>
        <p className="nv-muted">
          Changed your mind? The sign-up form at the bottom of any page adds the address again.
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
      <h1 className="nv-h1">Unsubscribe from the newsletter?</h1>
      <p className="nv-lede">
        This stops the monthly note. It does not close your Nelavista account or change anything about your
        learning record.
      </p>
      {error ? <Banner tone="danger">{error}</Banner> : null}
      <div className="nv-row">
        <Button disabled={state === 'busy'} onClick={() => void unsubscribe()} type="button">
          {state === 'busy' ? 'Unsubscribing' : 'Unsubscribe'}
        </Button>
        <Link className="nv-button nv-button--ghost" to="/">
          Keep receiving it
        </Link>
      </div>
    </section>
  );
}
