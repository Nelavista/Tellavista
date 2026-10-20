/**
 * Opportunities (B8).
 *
 * Every card answers the only two questions that matter: can I do this, and if
 * not, what exactly is missing? The verdict comes from the API's matching engine
 * and is never recomputed here, so the list and the detail cannot disagree.
 */
import type { OpportunityListOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

function rateLabel(currency: string | null | undefined, rateMinor: number | null | undefined): string {
  if (!currency || rateMinor == null) return 'Rate shared on the brief';
  try {
    return `${new Intl.NumberFormat(undefined, { style: 'currency', currency }).format(rateMinor / 100)} per approved task`;
  } catch {
    return `${currency} ${(rateMinor / 100).toFixed(2)} per approved task`;
  }
}

export function Opportunities(): JSX.Element {
  const { resource, reload } = useApiResource<OpportunityListOut>('/opportunities');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading opportunities">
        <Skeleton height="2rem" width="45%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Opportunities</h1>
        <p className="nv-banner">
          Opportunities are not switched on for this environment yet. Your learning and proof are
          unaffected.
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Opportunities</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
      </div>
    );
  }

  const rows = resource.data.opportunities;
  const eligible = rows.filter((row) => row.match.eligible).length;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Opportunities</h1>
      <p className="nv-muted">
        {rows.length === 0
          ? 'No opportunity is open right now. New work appears here when it is published.'
          : `${eligible} of ${rows.length} open ${rows.length === 1 ? 'role fits' : 'roles fit'} what you have proved so far.`}
      </p>

      {rows.length > 0 ? (
        <ul className="nv-list">
          {rows.map((row) => (
            <li className="nv-card" key={row.id}>
              <div className="nv-row nv-row--between">
                <h2 className="nv-h2">
                  <Link to={`/opportunities/${row.slug}`}>{row.title}</Link>
                </h2>
                <span className="nv-badge" data-status={row.match.eligible ? 'verified' : 'at_risk'}>
                  {row.match.eligible ? 'You qualify' : 'Not yet'}
                </span>
              </div>
              <p className="nv-muted">
                {row.type === 'managed' ? 'Managed by Nelavista' : 'External listing'}
                {row.client_name ? ` · ${row.client_name}` : ''} · {rateLabel(row.currency, row.rate_minor)}
              </p>
              {row.description ? <p>{row.description}</p> : null}
              {row.match.qualifies_because.length > 0 && row.match.eligible ? (
                <p className="nv-muted">Because: {row.match.qualifies_because.join(' · ')}</p>
              ) : null}
              {!row.match.eligible && row.match.next_steps.length > 0 ? (
                <div>
                  <p className="nv-muted">To qualify:</p>
                  <ul className="nv-list">
                    {row.match.next_steps.map((step) => (
                      <li key={step.requirement_id}>{step.detail}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </li>
          ))}
        </ul>
      ) : null}

      <p className="nv-muted">
        <Link to="/work">Your work</Link> · <Link to="/earnings">Your earnings</Link>
      </p>
    </div>
  );
}
