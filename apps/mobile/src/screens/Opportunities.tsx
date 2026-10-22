import type { ApplyOut, OpportunityListOut, OpportunityOut } from '@nelavista/api-client';
import * as React from 'react';
import { Pressable } from 'react-native';

import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { useApi } from '../lib/useApi';
import { Badge, Body, Button, Card, ErrorText, H2, Loading, Muted, Note, Screen } from '../ui';

export function Opportunities({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const list = useApi<OpportunityListOut>('/opportunities');
  return (
    <Screen title="Opportunities" onBack={() => navigate({ name: 'home' })}>
      {list.remote.status === 'loading' ? <Loading /> : null}
      {list.remote.status === 'error' ? <ErrorText message={list.remote.message} /> : null}
      {list.remote.status === 'ready' ? (
        <>
          <Muted>
            {list.remote.data.opportunities.filter((row) => row.match.eligible).length} of{' '}
            {list.remote.data.opportunities.length} fit what you have proved.
          </Muted>
          {list.remote.data.opportunities.map((row) => (
            <Pressable key={row.id} onPress={() => navigate({ name: 'opportunity', slug: row.slug })}>
              <Card>
                <H2>{row.title}</H2>
                <Badge label={row.match.eligible ? 'You qualify' : 'Not yet'} tone={row.match.eligible ? 'ok' : 'warn'} />
                <Muted>
                  {row.type === 'managed' ? 'Managed by Nelavista' : 'External listing'}
                  {row.headcount ? ` · ${row.headcount} place(s)` : ''}
                </Muted>
                {!row.match.eligible && row.match.next_steps[0] ? (
                  <Muted>To qualify: {row.match.next_steps[0]?.detail}</Muted>
                ) : null}
              </Card>
            </Pressable>
          ))}
          {list.remote.data.opportunities.length === 0 ? <Muted>Nothing open right now.</Muted> : null}
        </>
      ) : null}
    </Screen>
  );
}

export function OpportunityScreen({
  slug,
  navigate,
}: {
  slug: string;
  navigate: (route: Route) => void;
}): JSX.Element {
  const detail = useApi<OpportunityOut>(`/opportunities/${slug}`);
  const [note, setNote] = React.useState('');
  const [applied, setApplied] = React.useState<ApplyOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  async function apply(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      setApplied(await api.post<ApplyOut>(`/opportunities/${slug}/apply`, { note: note.trim() || null }));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your application.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Opportunity" onBack={() => navigate({ name: 'opportunities' })}>
      {detail.remote.status === 'loading' ? <Loading /> : null}
      {detail.remote.status === 'error' ? <ErrorText message={detail.remote.message} /> : null}
      {detail.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{detail.remote.data.title}</H2>
            <Badge
              label={detail.remote.data.match.eligible ? 'You qualify' : 'Not yet'}
              tone={detail.remote.data.match.eligible ? 'ok' : 'warn'}
            />
            {detail.remote.data.description ? <Body>{detail.remote.data.description}</Body> : null}
          </Card>

          <Card>
            <H2>Requirements</H2>
            {detail.remote.data.match.explanation.map((check) => (
              <Muted key={check.requirement_id}>
                {check.met ? '✓' : check.mandatory ? '✗' : '○'} {check.description} · {check.detail}
              </Muted>
            ))}
            {detail.remote.data.match.next_steps.map((step) => (
              <Muted key={step.requirement_id}>→ {step.detail}</Muted>
            ))}
          </Card>

          {applied ? (
            <Note message={`Application sent. Status: ${applied.status.replace(/_/g, ' ')}.`} />
          ) : detail.remote.data.type === 'external' ? (
            <Card>
              <H2>Apply</H2>
              <Button label={busy ? 'Sending…' : 'Send my application'} onPress={() => void apply()} disabled={busy} />
            </Card>
          ) : (
            <Muted>Managed work is invitation-only; matching uses your verified skills.</Muted>
          )}
          <ErrorText message={error} />
        </>
      ) : null}
    </Screen>
  );
}
