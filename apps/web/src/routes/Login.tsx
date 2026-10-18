import * as React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import { ApiError } from '../lib/http';
import { useSession } from '../lib/session';
import { Button, ErrorNote, Field } from '../ui';

interface RedirectState {
  from?: string;
}

export function Login(): JSX.Element {
  const { login } = useSession();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await login(email.trim().toLowerCase(), password);
      const from = (location.state as RedirectState | null)?.from;
      navigate(from && from.startsWith('/') ? from : '/home', { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not sign you in.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-card nv-card--narrow">
      <h1 className="nv-h2">Sign in</h1>
      <form className="nv-stack" onSubmit={onSubmit} noValidate>
        <Field
          label="Email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Field
          label="Password"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <ErrorNote message={error} />
        <Button type="submit" disabled={busy}>
          {busy ? 'Signing in…' : 'Sign in'}
        </Button>
      </form>
      <p className="nv-muted">
        New here? <Link to="/signup">Create an account</Link>
      </p>
    </div>
  );
}
