/**
 * The screen an emailed verification link opens (F9/B1).
 *
 * The token is single-use and arrives in the query string; posting it here is
 * the only thing this page does. It works signed out — the link may open on a
 * different device — and says which account state it found, never a raw error.
 */
import * as React from 'react';
import { Link, useSearchParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';
import { ErrorNote, Skeleton } from '../ui';

type State =
  | { status: 'checking' }
  | { status: 'done'; email: string }
  | { status: 'failed'; message: string };

export function VerifyEmail(): JSX.Element {
  const [params] = useSearchParams();
  const token = params.get('token') ?? '';
  const { status: sessionStatus, reload } = useSession();
  const [state, setState] = React.useState<State>({ status: 'checking' });
  const attempted = React.useRef(false);

  React.useEffect(() => {
    if (attempted.current) return;
    attempted.current = true;
    void (async () => {
      if (!token) {
        setState({
          status: 'failed',
          message: 'This link has no token. Open the link from your email again.',
        });
        return;
      }
      try {
        const me = await http.post<{ email: string }>('/auth/email/verify', { token });
        if (sessionStatus === 'authenticated') await reload();
        setState({ status: 'done', email: me.email });
      } catch (err) {
        setState({
          status: 'failed',
          message:
            err instanceof ApiError ? err.message : 'Could not confirm this email. Try the link again.',
        });
      }
    })();
  }, [token, sessionStatus, reload]);

  if (state.status === 'checking') {
    return (
      <div className="nv-card nv-card--narrow" aria-busy="true" aria-label="Confirming your email">
        <Skeleton height="2rem" width="60%" />
        <Skeleton lines={2} />
      </div>
    );
  }

  return (
    <div className="nv-card nv-card--narrow nv-stack">
      <h1 className="nv-h1">{state.status === 'done' ? 'Email confirmed' : 'This link did not work'}</h1>
      {state.status === 'done' ? (
        <>
          <p>
            <strong>{state.email}</strong> is confirmed. Proof, work and payout notices can reach you.
          </p>
          <Link className="nv-button" to={sessionStatus === 'authenticated' ? '/home' : '/login'}>
            {sessionStatus === 'authenticated' ? 'Go to your home' : 'Sign in'}
          </Link>
        </>
      ) : (
        <>
          <ErrorNote message={state.message} />
          <p className="nv-muted">
            Verification links expire and work once. Sign in and use &ldquo;Send the link again&rdquo; on
            your home screen for a fresh one.
          </p>
          <Link to={sessionStatus === 'authenticated' ? '/home' : '/login'}>
            {sessionStatus === 'authenticated' ? 'Back to your home' : 'Sign in'}
          </Link>
        </>
      )}
    </div>
  );
}
