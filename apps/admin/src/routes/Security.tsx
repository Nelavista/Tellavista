/**
 * Staff security (C8).
 *
 * 2FA is enrolled before the shell loads. This screen is where it is turned off
 * deliberately — with a current code — and where the remaining recovery codes are
 * counted. Turning it off is audited like any other security change.
 */
import { Badge, Banner, Button, Field, PageHeader, Panel } from '@nelavista/ui';
import { ShieldCheck } from 'lucide-react';
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
      const result = await http.post<{ message: string }>('/auth/2fa/disable', {
        code: code.trim(),
      });
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
      <PageHeader
        eyebrow="Security"
        title="Security"
        description={`Signed in as ${me?.email ?? 'unknown'} (${me?.role ?? 'no role'}).`}
        actions={
          <Badge status={mfa?.enabled ? 'enabled' : 'disabled'} tone={mfa?.enabled ? 'success' : 'danger'}>
            <ShieldCheck aria-hidden="true" size={13} />
            {mfa?.enabled ? '2FA on' : '2FA off'}
          </Badge>
        }
      />

      <Panel title="Two-factor authentication">
        <div className="nv-stack">
          <p>
            <span className="nv-muted">{mfa?.remaining_recovery_codes ?? 0} recovery code(s) left.</span>
          </p>
          <p className="nv-muted">
            Every admin login asks for a code. Turning it off lowers the account to a password only; do it
            only to re-enrol a new device.
          </p>

          {error ? (
            <Banner tone="danger">
              <p>{error}</p>
            </Banner>
          ) : null}
          {note ? (
            <Banner tone="success">
              <p>{note}</p>
            </Banner>
          ) : null}

          <div className="nv-row" style={{ alignItems: 'flex-end' }}>
            <div style={{ flex: 1, minWidth: 220 }}>
              <Field
                autoComplete="one-time-code"
                hint="A current authenticator code or one recovery code."
                id="disable-code"
                label="Current code or a recovery code"
                maxLength={20}
                value={code}
                onChange={(event) => setCode(event.target.value)}
              />
            </div>
            <Button
              disabled={busy || code.trim().length < 6}
              type="button"
              variant="danger"
              onClick={() => void disable()}
            >
              {busy ? 'Turning off…' : 'Turn off two-factor'}
            </Button>
          </div>
        </div>
      </Panel>
    </div>
  );
}
