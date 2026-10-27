/**
 * Password recovery (B1 remaining).
 *
 * Two states on one route, decided by whether the emailed token is present:
 *
 * * no token - ask for the address and always answer with the same sentence, so
 *   the screen cannot be used to discover which emails have accounts;
 * * token - set a new password. A successful reset signs every device out, and
 *   the copy says so instead of letting the next refresh look like a bug.
 */
import * as React from 'react';
import { Link, useSearchParams } from 'react-router-dom';

import { AuthLayout } from '../components/AuthLayout';
import { ApiError, http } from '../lib/http';
import { Banner, Button, ErrorNote, Field } from '../ui';

export function ResetPassword(): JSX.Element {
  const [params] = useSearchParams();
  const token = params.get('token');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirm, setConfirm] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [message, setMessage] = React.useState<string | null>(null);

  async function requestLink(): Promise<void> {
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const result = await http.post<{ message: string }>('/auth/password/reset-request', {
        email: email.trim(),
      });
      setMessage(result.message);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send the reset link.');
    } finally {
      setBusy(false);
    }
  }

  async function reset(): Promise<void> {
    if (password !== confirm) {
      setError('The two passwords do not match.');
      return;
    }
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const result = await http.post<{ message: string }>('/auth/password/reset', {
        token,
        password,
      });
      setMessage(result.message);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not reset your password.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthLayout
      title={token ? 'Choose a new password' : 'Reset your password'}
      description={
        token
          ? 'A new password signs you out on every device. Your learning, proof and earnings stay.'
          : 'Enter the email on your account. If it has one, a single-use link arrives in a minute.'
      }
      footer={<Link to="/login">Back to sign in</Link>}
    >
      <ErrorNote message={error} />
      {message ? (
        <>
          <Banner tone="success">{message}</Banner>
          <Link className="nv-button" to="/login">
            Go to sign in
          </Link>
        </>
      ) : token ? (
        <>
          <Field
            autoComplete="new-password"
            label="New password"
            minLength={10}
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          <Field
            autoComplete="new-password"
            label="Type it again"
            minLength={10}
            type="password"
            value={confirm}
            onChange={(event) => setConfirm(event.target.value)}
          />
          <Button
            block
            disabled={busy || password.length < 10 || confirm.length < 10}
            type="button"
            onClick={() => void reset()}
          >
            {busy ? 'Saving' : 'Set the new password'}
          </Button>
        </>
      ) : (
        <>
          <Field
            autoComplete="email"
            label="Email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          <Button
            block
            disabled={busy || !email.includes('@')}
            type="button"
            onClick={() => void requestLink()}
          >
            {busy ? 'Sending' : 'Send the reset link'}
          </Button>
        </>
      )}
    </AuthLayout>
  );
}
