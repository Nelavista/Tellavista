/**
 * Earnings (B10).
 *
 * A number a student cannot explain is a support ticket. Every line therefore
 * shows the project, the task count, the rate used and the status, and the total
 * is only ever the sum of those lines. Amounts arrive in minor units and are
 * formatted here, never rounded in the API.
 */
import type { EarningsOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

function money(amountMinor: number, currency: string): string {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency }).format(amountMinor / 100);
  } catch {
    return `${currency} ${(amountMinor / 100).toFixed(2)}`;
  }
}

const STATUS_COPY: Record<string, string> = {
  pending: 'Waiting for review',
  payable: 'Ready to be paid',
  paid: 'Paid',
  reversed: 'Reversed',
  on_hold: 'On hold',
};

export function Earnings(): JSX.Element {
  const { resource, reload } = useApiResource<EarningsOut>('/money/earnings');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your earnings">
        <Skeleton height="2rem" width="35%" />
        <Skeleton lines={2} />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Earnings</h1>
        <p className="nv-banner">
          Earnings are not switched on for this environment yet. Approved work is still recorded.
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Earnings</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
      </div>
    );
  }

  const { totals, lines } = resource.data;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Earnings</h1>

      {totals.length === 0 ? (
        <p className="nv-banner">
          No earnings yet. An approved task creates a line here with the rate and reason it was paid at.
        </p>
      ) : (
        <ul className="nv-list">
          {totals.map((total) => (
            <li className="nv-card" key={total.currency}>
              <p className="nv-muted">Total earned ({total.currency})</p>
              <p className="nv-h1">{money(total.amount_minor, total.currency)}</p>
            </li>
          ))}
        </ul>
      )}

      {lines.length > 0 ? (
        <section className="nv-stack">
          <h2 className="nv-h2">Every line, and why</h2>
          <ul className="nv-list">
            {lines.map((line) => (
              <li className="nv-card" key={line.id}>
                <div className="nv-row nv-row--between">
                  <h3 className="nv-h2">{line.project.title}</h3>
                  <strong>{money(line.amount_minor, line.currency)}</strong>
                </div>
                <p className="nv-muted">
                  {line.task_count !== null && line.task_count !== undefined
                    ? `${line.task_count} approved task${line.task_count === 1 ? '' : 's'}`
                    : 'Approved work'}
                  {line.rate_minor !== null && line.rate_minor !== undefined
                    ? ` · ${money(line.rate_minor, line.currency)} per task`
                    : ''}
                  {' · '}
                  {STATUS_COPY[line.status] ?? line.status.replace(/_/g, ' ')}
                </p>
                {line.description ? <p>{line.description}</p> : null}
                {line.status === 'pending' ? (
                  <p className="nv-muted">
                    This line becomes payable when the review is approved. Rework does not remove it.
                  </p>
                ) : null}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <p className="nv-muted">
        <Link to="/work">Your work</Link> · Payouts are made in batches; a paid line shows here with its
        status.
      </p>
    </div>
  );
}
