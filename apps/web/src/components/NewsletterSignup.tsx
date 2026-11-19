/**
 * The public newsletter opt-in.
 *
 * Sits in the footer of the public site so a visitor who is not ready to make an
 * account can still ask to hear from us. The API is the only thing that decides
 * whether an address is subscribed, and it answers the same way for a new and an
 * existing address - so this form must not claim "you were added" either. It
 * says the address is on the list, which is true in both cases and tells an
 * outsider nothing about who else is subscribed.
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
        <p className="nv-h4">You are on the list</p>
        <p className="nv-muted" style={{ maxWidth: '38ch' }}>
          We send one note a month: new material, open opportunities and what changed on the platform.
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
