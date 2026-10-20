import type { EarningsOut } from '@nelavista/api-client';
import * as React from 'react';

import type { Route } from '../lib/deepLink';
import { useApi } from '../lib/useApi';
import { Badge, Body, Card, ErrorText, H2, Loading, Muted, Screen } from '../ui';

function amount(minor: number | null | undefined, currency: string | null | undefined): string {
  if (minor == null) return '—';
  if (!currency) return String(minor);
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency }).format(minor / 100);
  } catch {
    return `${currency} ${(minor / 100).toFixed(2)}`;
  }
}

export function Earnings({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const earnings = useApi<EarningsOut>('/money/earnings');
  return (
    <Screen title="Earnings" onBack={() => navigate({ name: 'home' })}>
      {earnings.remote.status === 'loading' ? <Loading /> : null}
      {earnings.remote.status === 'error' ? <ErrorText message={earnings.remote.message} /> : null}
      {earnings.remote.status === 'ready' ? (
        <>
          {earnings.remote.data.totals.length === 0 ? (
            <Muted>No earnings yet. An approved task creates a line with its rate and reason.</Muted>
          ) : (
            earnings.remote.data.totals.map((total) => (
              <Card key={total.currency}>
                <Muted>Total earned ({total.currency})</Muted>
                <H2>{amount(total.amount_minor, total.currency)}</H2>
              </Card>
            ))
          )}
          {earnings.remote.data.lines.map((line) => (
            <Card key={line.id}>
              <H2>{line.project.title}</H2>
              <Body>{amount(line.amount_minor, line.currency)}</Body>
              <Badge
                label={line.status.replace(/_/g, ' ')}
                tone={line.status === 'paid' ? 'ok' : line.status === 'reversed' ? 'bad' : 'warn'}
              />
              <Muted>
                {line.task_count ?? 0} approved task(s)
                {line.rate_minor !== null ? ` · ${amount(line.rate_minor, line.currency)} per task` : ''}
              </Muted>
              {line.description ? <Muted>{line.description}</Muted> : null}
            </Card>
          ))}
        </>
      ) : null}
    </Screen>
  );
}
