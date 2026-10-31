import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { AuthLayout } from '../components/AuthLayout';
import { ApiError } from '../lib/http';
import { useSession } from '../lib/session';
import { Button, Checkbox, ErrorNote, Field, PasswordField } from '../ui';

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
      return 'Usernames are 3-40 characters: letters, numbers, dot, dash or underscore.';
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
    <AuthLayout
      title="Create your account"
      description="One account for your courses, skills, evidence, work and earnings."
      footer={
        <>
          Already have an account? <Link to="/login">Sign in</Link>
        </>
      }
    >
      <form className="nv-stack" onSubmit={onSubmit} noValidate>
        <Field autoComplete="name" label="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <Field
          autoComplete="email"
          label="Email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Field
          autoComplete="username"
          hint="Letters, numbers, dot, dash or underscore."
          label="Username"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <PasswordField
          autoComplete="new-password"
          hint="At least 10 characters."
          label="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Checkbox
          checked={accepted}
          onChange={(e) => setAccepted(e.target.checked)}
          label={
            <>
              I accept the <Link to="/legal/terms">terms</Link> and{' '}
              <Link to="/legal/privacy">privacy notice</Link>.
            </>
          }
        />
        <ErrorNote message={error} />
        <Button block disabled={busy} type="submit">
          {busy ? 'Creating your account' : 'Create account'}
        </Button>
      </form>
    </AuthLayout>
  );
}
