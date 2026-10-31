/**
 * Mandatory staff 2FA (C8).
 *
 * A staff account without a second factor is how an ops login becomes a
 * newspaper story. The shell refuses to render any other screen until this is
 * done, and the API refuses to hand out a session to an enrolled staff account
 * that does not present a code.
 */
import type { MfaEnableOut, MfaSetupOut } from '@nelavista/api-client';
import { ConfirmDialog } from '@nelavista/ui';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';

export function TwoFactor(): JSX.Element {
  const { logout } = useSession();
  const [setup, setSetup] = React.useState<MfaSetupOut | null>(null);
  const [code, setCode] = React.useState('');
  const [codes, setCodes] = React.useState<string[] | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [signOutOpen, setSignOutOpen] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function begin(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      setSetup(await http.post<MfaSetupOut>('/auth/2fa/setup'));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not start 2FA setup.');
    } finally {
      setBusy(false);
    }
  }

  async function enable(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const result = await http.post<MfaEnableOut>('/auth/2fa/enable', { code: code.trim() });
      // Keep this screen mounted until the operator has seen the one-time
      // recovery codes. Reloading the session here would unmount it first.
      setCodes(result.recovery_codes);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'That code did not work.');
    } finally {
      setBusy(false);
    }
  }

  if (codes) {
    return (
      <div className="nv-card nv-login">
        <h1 className="nv-h1">Save your recovery codes</h1>
        <p>
          These are shown once. Each works once if you lose your phone. Store them somewhere other than the
          phone.
        </p>
        <div className="nv-code">
          {codes.map((row) => (
            <div key={row}>{row}</div>
          ))}
        </div>
        <p className="nv-muted">
          You can sign in now. Every future admin login asks for your authenticator code.
        </p>
        <button className="nv-button" type="button" onClick={() => window.location.reload()}>
          I have saved them
        </button>
      </div>
    );
  }

  return (
    <div className="nv-card nv-login">
      <h1 className="nv-h1">Two-factor is required</h1>
      <p className="nv-muted">
        Staff accounts must enrol an authenticator before using the ops tools. This is a Phase 0 security
        requirement, not a preference.
      </p>
      {error ? (
        <p className="nv-error" role="alert">
          {error}
        </p>
      ) : null}

      {setup === null ? (
        <button className="nv-button" disabled={busy} type="button" onClick={() => void begin()}>
          {busy ? 'Preparing…' : 'Start setup'}
        </button>
      ) : (
        <>
          <p>Add this secret to your authenticator app, then enter the six-digit code it shows.</p>
          <div className="nv-code">{setup.secret}</div>
          <details>
            <summary>Use the otpauth link instead</summary>
            <pre className="nv-pre">{setup.otpauth_uri}</pre>
          </details>
          <div>
            <label className="nv-label" htmlFor="enrol-code">
              Code from the app
            </label>
            <input
              autoComplete="one-time-code"
              className="nv-input"
              id="enrol-code"
              inputMode="numeric"
              maxLength={6}
              value={code}
              onChange={(event) => setCode(event.target.value)}
            />
          </div>
          <button
            className="nv-button"
            disabled={busy || code.trim().length !== 6}
            type="button"
            onClick={() => void enable()}
          >
            {busy ? 'Confirming…' : 'Confirm and turn on'}
          </button>
        </>
      )}

      <button className="nv-button nv-button--ghost" type="button" onClick={() => setSignOutOpen(true)}>
        Sign out
      </button>
      <ConfirmDialog
        body={<p>Two-factor enrolment is not finished. You will need to sign in and start again.</p>}
        confirmLabel="Sign out"
        onCancel={() => setSignOutOpen(false)}
        onConfirm={() => void logout()}
        open={signOutOpen}
        title="Are you sure you want to sign out?"
      />
    </div>
  );
}
