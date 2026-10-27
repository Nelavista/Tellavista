/**
 * Earnings (B10).
 *
 * A number a student cannot explain is a support ticket. Every line therefore
 * shows the project, the task count, the rate used and the status, and the total
 * is only ever the sum of those lines. Amounts arrive in minor units and are
 * formatted here, never rounded in the API.
 */
import type { EarningsOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { Receipt, Wallet } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';

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

function statusTone(status: string): 'neutral' | 'success' | 'info' | 'warning' | 'danger' {
  if (status === 'paid') return 'success';
  if (status === 'payable') return 'info';
  if (status === 'pending' || status === 'on_hold') return 'warning';
  if (status === 'reversed') return 'danger';
  return 'neutral';
}

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
        <PageHeader eyebrow="Work" title="Earnings" />
        <Banner tone="info">
          <p>Earnings are not switched on for this environment yet. Approved work is still recorded.</p>
        </Banner>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Earnings" />
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const { totals, lines } = resource.data;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Work"
        title="Earnings"
        description="Every total is the sum of the lines below. A pending line is not paid until review approves it."
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/work">
              My work
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/opportunities">
              Find more work
            </Link>
          </>
        }
      />

      <Panel title="Total earned">
        {totals.length === 0 ? (
          <EmptyState
            body="An approved task creates a line here with the rate and reason it was paid at."
            icon={Wallet}
            title="No earnings yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/opportunities">
                Browse opportunities
              </Link>
            }
          />
        ) : (
          <div className="nv-grid">
            {totals.map((total) => (
              <div className="nv-stat" key={total.currency}>
                <p className="nv-stat__value">{money(total.amount_minor, total.currency)}</p>
                <p className="nv-stat__label">Total earned · {total.currency}</p>
              </div>
            ))}
          </div>
        )}
      </Panel>

      <Panel title="Every line, and why" actions={<Badge tone="neutral">{lines.length}</Badge>}>
        {lines.length === 0 ? (
          <EmptyState
            body="No ledger line exists yet. Approved work appears here with its rate and status."
            icon={Receipt}
            title="No lines yet"
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Project</th>
                  <th>Amount</th>
                  <th>Rate</th>
                  <th>Tasks</th>
                  <th>Status</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {lines.map((line) => (
                  <tr key={line.id}>
                    <td>{line.project.title}</td>
                    <td className="nv-num">{money(line.amount_minor, line.currency)}</td>
                    <td className="nv-num">
                      {line.rate_minor !== null && line.rate_minor !== undefined
                        ? money(line.rate_minor, line.currency)
                        : '—'}
                    </td>
                    <td className="nv-num">
                      {line.task_count !== null && line.task_count !== undefined ? line.task_count : '—'}
                    </td>
                    <td>
                      <Badge tone={statusTone(line.status)}>
                        {STATUS_COPY[line.status] ?? line.status.replace(/_/g, ' ')}
                      </Badge>
                    </td>
                    <td>
                      {line.description ?? '—'}
                      {line.status === 'pending' ? (
                        <div className="nv-muted">
                          Becomes payable when the review is approved. Rework does not remove it.
                        </div>
                      ) : null}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <p className="nv-muted">Payouts are made in batches; a paid line shows here with its status.</p>
    </div>
  );
}
