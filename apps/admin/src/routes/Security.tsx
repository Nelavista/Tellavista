/**
 * Staff security (C8).
 *
 * 2FA is enrolled before the shell loads. This screen is where it is turned off
 * deliberately — with a current code — and where the remaining recovery codes are
 * counted. Turning it off is audited like any other security change.
 */
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';

export function Security(): JSX.Element {
  const { me, mfa, reload } = useSession();
  const [code, setCode] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  async function disable(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      const result = await http.post<{ message: string }>('/auth/2fa/disable', { code: code.trim() });
      setNote(result.message);
      setCode('');
      await reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not turn off two-factor.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Security</h1>
      <p className="nv-muted">
        Signed in as {me?.email} ({me?.role ?? 'no role'}).
      </p>

      <section className="nv-card">
        <h2 className="nv-h2">Two-factor authentication</h2>
        <p>
          <span className="nv-tag" data-tone={mfa?.enabled ? 'ok' : 'bad'}>
            {mfa?.enabled ? 'on' : 'off'}
          </span>{' '}
          <span className="nv-muted">
            {mfa?.remaining_recovery_codes ?? 0} recovery code(s) left.
          </span>
        </p>
        <p className="nv-muted">
          Every admin login asks for a code. Turning it off lowers the account to a password only; do it
          only to re-enrol a new device.
        </p>
        {error ? <p className="nv-error">{error}</p> : null}
        {note ? <p className="nv-muted">{note}</p> : null}
        <div className="nv-row">
          <div>
            <label className="nv-label" htmlFor="disable-code">Current code or a recovery code</label>
            <input
              autoComplete="one-time-code"
              className="nv-input"
              id="disable-code"
              maxLength={20}
              value={code}
              onChange={(event) => setCode(event.target.value)}
            />
          </div>
          <button className="nv-button nv-button--danger" disabled={busy || code.trim().length < 6} type="button" onClick={() => void disable()}>
            Turn off two-factor
          </button>
        </div>
      </section>
    </div>
  );
}
