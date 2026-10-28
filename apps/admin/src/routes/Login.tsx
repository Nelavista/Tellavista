import { BrandMark } from '@nelavista/ui';
import * as React from 'react';

import { ApiError } from '../lib/http';
import { useSession } from '../lib/session';

export function Login(): JSX.Element {
  const { login, verifyMfa } = useSession();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [challenge, setChallenge] = React.useState<string | null>(null);
  const [code, setCode] = React.useState('');
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (challenge) {
        await verifyMfa(challenge, code.trim());
      } else {
        await login(email.trim().toLowerCase(), password);
      }
    } catch (err) {
      if (err instanceof ApiError && err.code === 'mfa_required') {
        const details = err.details as { mfa_token?: string } | undefined;
        if (details?.mfa_token) {
          setChallenge(details.mfa_token);
          setError(null);
          return;
        }
      }
      setError(err instanceof ApiError ? err.message : 'Could not sign in.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-card nv-login">
      <div className="nv-row" style={{ marginBottom: 'var(--nv-space-lg)' }}>
        <BrandMark size={36} />
        <span className="nv-meta">Nelavista ops</span>
      </div>
      <h1 className="nv-h1">Ops sign in</h1>
      <p className="nv-muted">
        Staff account only. Every action here is written to the audit trail with your account.
      </p>
      <form className="nv-stack" onSubmit={submit}>
        {challenge ? (
          <div>
            <label className="nv-label" htmlFor="mfa-code">
              Authenticator code
            </label>
            <input
              autoComplete="one-time-code"
              autoFocus
              className="nv-input"
              id="mfa-code"
              maxLength={20}
              value={code}
              onChange={(event) => setCode(event.target.value)}
            />
          </div>
        ) : (
          <>
            <div>
              <label className="nv-label" htmlFor="admin-email">
                Email
              </label>
              <input
                autoComplete="email"
                className="nv-input"
                id="admin-email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </div>
            <div>
              <label className="nv-label" htmlFor="admin-password">
                Password
              </label>
              <input
                autoComplete="current-password"
                className="nv-input"
                id="admin-password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </div>
          </>
        )}
        {error ? (
          <p className="nv-error" role="alert">
            {error}
          </p>
        ) : null}
        <button className="nv-button" disabled={busy} type="submit">
          {busy ? 'Signing in…' : challenge ? 'Verify and sign in' : 'Sign in'}
        </button>
      </form>
      <p className="nv-muted">
        Not staff? This app is not for student accounts. Use the student web app instead.
      </p>
    </div>
  );
}
