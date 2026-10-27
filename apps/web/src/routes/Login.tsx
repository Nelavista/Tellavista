import type { TokenOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import { AuthLayout } from '../components/AuthLayout';
import { ApiError, http, setAccessToken } from '../lib/http';
import { useSession } from '../lib/session';
import { Button, ErrorNote, Field } from '../ui';

interface RedirectState {
  from?: string;
}

/**
 * Sign in, with a second step when the account has 2FA (F1).
 *
 * The password call returns `mfa_required` and a short-lived challenge, never a
 * session. Only `/auth/2fa/verify` turns that challenge into an access token, so
 * a staff password alone cannot open the admin app.
 */
export function Login(): JSX.Element {
  const { login, reload } = useSession();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [challenge, setChallenge] = React.useState<string | null>(null);
  const [code, setCode] = React.useState('');
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  function goNext(): void {
    const from = (location.state as RedirectState | null)?.from;
    navigate(from && from.startsWith('/') ? from : '/home', { replace: true });
  }

  async function onSubmit(e: React.FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (challenge) {
        const token = await http.post<TokenOut>('/auth/2fa/verify', { mfa_token: challenge, code });
        setAccessToken(token.access_token);
        await reload();
        goNext();
        return;
      }
      await login(email.trim().toLowerCase(), password);
      goNext();
    } catch (err) {
      if (err instanceof ApiError && err.code === 'mfa_required') {
        const details = err.details as { mfa_token?: string } | undefined;
        if (details?.mfa_token) {
          setChallenge(details.mfa_token);
          setError(null);
          return;
        }
      }
      setError(err instanceof ApiError ? err.message : 'Could not sign you in.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthLayout
      title={challenge ? 'Enter your code' : 'Sign in'}
      description={
        challenge
          ? 'Your account has two-factor authentication. Enter the six-digit code from your authenticator app, or one of your recovery codes.'
          : 'Pick up your record where you left it.'
      }
      footer={
        <>
          New here? <Link to="/signup">Create an account</Link>
        </>
      }
    >
      <form className="nv-stack" onSubmit={onSubmit} noValidate>
        {challenge ? (
          <Field
            autoComplete="one-time-code"
            autoFocus
            label="Code"
            maxLength={20}
            required
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
        ) : (
          <>
            <Field
              autoComplete="email"
              autoFocus
              label="Email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Field
              autoComplete="current-password"
              label="Password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </>
        )}
        <ErrorNote message={error} />
        <Button block disabled={busy || (challenge !== null && code.trim().length < 6)} type="submit">
          {busy ? 'Signing in' : challenge ? 'Verify and sign in' : 'Sign in'}
        </Button>
        <div className="nv-row nv-row--between">
          <Link to="/auth/reset">Forgot your password?</Link>
          {challenge ? (
            <button
              className="nv-button nv-button--ghost nv-button--sm"
              type="button"
              onClick={() => {
                setChallenge(null);
                setCode('');
                setError(null);
              }}
            >
              Use a password
            </button>
          ) : null}
        </div>
      </form>
    </AuthLayout>
  );
}
