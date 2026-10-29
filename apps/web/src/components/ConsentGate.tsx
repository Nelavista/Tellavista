import type { ConsentListOut, ConsentOut, PlatformConfigOut } from '@nelavista/api-client';
import { Banner, Button, Checkbox } from '@nelavista/ui';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

const VERSIONED = [
  { kind: 'terms_of_service', label: 'Terms of Service', to: '/legal/terms' },
  { kind: 'privacy_policy', label: 'Privacy Notice', to: '/legal/privacy' },
] as const;

function latestGranted(rows: ConsentOut[], kind: string): ConsentOut | null {
  return rows
    .filter((row) => row.kind === kind && row.granted)
    .reduce<ConsentOut | null>(
      (latest, row) => (!latest || row.created_at > latest.created_at ? row : latest),
      null,
    );
}

/**
 * Re-consent when the published terms version moves. The API already records
 * consent; this is the missing prompt, not a second source of truth.
 */
export function ConsentGate(): JSX.Element | null {
  const config = useApiResource<PlatformConfigOut>('/platform/config');
  const consents = useApiResource<ConsentListOut>('/me/consents');
  const [checked, setChecked] = React.useState(false);
  const [busy, setBusy] = React.useState(false);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const configData = config.resource.status === 'ready' ? config.resource.data : null;
  const consentData = consents.resource.status === 'ready' ? consents.resource.data : null;
  if (!configData || !consentData) return null;

  const version = configData.terms_version;
  const needs = VERSIONED.filter(
    (item) => latestGranted(consentData.consents, item.kind)?.document_version !== version,
  );
  if (needs.length === 0) return null;

  async function record(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      for (const item of needs) {
        await http.post('/auth/consent', {
          kind: item.kind,
          document_version: version,
          granted: true,
        });
      }
      setNote(`Acceptance recorded for version ${version}.`);
      setChecked(false);
      consents.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not record your acceptance.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Banner
      tone="warning"
      actions={
        <Button disabled={!checked || busy} onClick={() => void record()} size="sm" type="button">
          {busy ? 'Recording' : 'Record acceptance'}
        </Button>
      }
    >
      <div className="nv-stack nv-stack--tight">
        <strong>We published a new document version.</strong>
        <p className="nv-muted">
          Version {version} is current. Read the documents and accept them to keep using Nelavista.
        </p>
        <div className="nv-row">
          {needs.map((item) => (
            <Link key={item.kind} to={item.to}>
              {item.label}
            </Link>
          ))}
        </div>
        <Checkbox
          checked={checked}
          label={`I have read and accept the current ${needs.map((item) => item.label).join(' and ')}.`}
          onChange={(event) => setChecked(event.target.checked)}
        />
        {note ? <p role="status">{note}</p> : null}
        {error ? (
          <p className="nv-error" role="alert">
            {error}
          </p>
        ) : null}
      </div>
    </Banner>
  );
}
