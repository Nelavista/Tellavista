import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { ApiError } from '../lib/http';
import { useSession } from '../lib/session';
import { Button, ErrorNote, Field } from '../ui';

const USERNAME_RE = /^[A-Za-z0-9_.-]+$/;

export function Signup(): JSX.Element {
  const { signup } = useSession();
  const navigate = useNavigate();
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [accepted, setAccepted] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  function validate(): string | null {
    if (!email.includes('@')) return 'Enter a valid email address.';
    if (username.length < 3 || username.length > 40 || !USERNAME_RE.test(username)) {
      return 'Usernames are 3–40 characters: letters, numbers, dot, dash or underscore.';
    }
    if (password.length < 10) return 'Use at least 10 characters for your password.';
    if (!accepted) return 'Please accept the terms to continue.';
    return null;
  }

  async function onSubmit(e: React.FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    const problem = validate();
    if (problem) {
      setError(problem);
      return;
    }
    setError(null);
    setBusy(true);
    try {
      await signup({ name: name.trim() || undefined, email, username, password });
      navigate('/onboarding', { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create your account.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-card nv-card--narrow">
      <h1 className="nv-h2">Create your account</h1>
      <p className="nv-muted">One account for learning, proof and work.</p>
      <form className="nv-stack" onSubmit={onSubmit} noValidate>
        <Field label="Name" autoComplete="name" value={name} onChange={(e) => setName(e.target.value)} />
        <Field
          label="Email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Field
          label="Username"
          autoComplete="username"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          hint="Letters, numbers, dot, dash or underscore."
        />
        <Field
          label="Password"
          type="password"
          autoComplete="new-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          hint="At least 10 characters."
        />
        <label className="nv-check">
          <input type="checkbox" checked={accepted} onChange={(e) => setAccepted(e.target.checked)} />
          <span>I accept the terms and privacy policy.</span>
        </label>
        <ErrorNote message={error} />
        <Button type="submit" disabled={busy}>
          {busy ? 'Creating…' : 'Create account'}
        </Button>
      </form>
      <p className="nv-muted">
        Already have an account? <Link to="/login">Sign in</Link>
      </p>
    </div>
  );
}
