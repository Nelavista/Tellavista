/**
 * The public newsletter opt-in.
 *
 * Sits in the footer of the public site so a visitor who is not ready to make an
 * account can still ask to hear from us. The list is double opt-in: submitting
 * only starts the confirmation, so this form asks the reader to check their
 * inbox and never claims the address is on the list. The API answers the same
 * way for a new, pending and already-confirmed address, so the wording also
 * tells an outsider nothing about who is subscribed.
 */
import type { NewsletterSubscribeOut } from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { Button, Field } from '../ui';

type State = 'idle' | 'busy' | 'done';

export function NewsletterSignup(): JSX.Element {
  const [email, setEmail] = React.useState('');
  const [state, setState] = React.useState<State>('idle');
  const [error, setError] = React.useState<string | null>(null);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    const address = email.trim();
    if (!address) {
      setError('Enter the email address to send the newsletter to.');
      return;
    }
    setState('busy');
    setError(null);
    try {
      await http.post<NewsletterSubscribeOut>('/newsletter/subscribe', {
        email: address,
        source: 'web_footer',
      });
      setState('done');
      setEmail('');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not add that address. Try again.');
      setState('idle');
    }
  }

  if (state === 'done') {
    return (
      <div className="nv-stack nv-stack--tight" role="status">
        <p className="nv-h4">Check your inbox</p>
        <p className="nv-muted" style={{ maxWidth: '38ch' }}>
          If that address has not been confirmed yet, a link is on its way. One click adds you to
          the monthly note; we send nothing until then.
        </p>
      </div>
    );
  }

  return (
    <form className="nv-newsletter" onSubmit={(event) => void onSubmit(event)}>
      <Field
        autoComplete="email"
        disabled={state === 'busy'}
        error={error}
        id="newsletter-email"
        label="Monthly newsletter"
        onChange={(event) => setEmail(event.target.value)}
        placeholder="you@example.com"
        type="email"
        value={email}
      />
      <Button disabled={state === 'busy'} type="submit" variant="secondary">
        {state === 'busy' ? 'Adding' : 'Subscribe'}
      </Button>
    </form>
  );
}
