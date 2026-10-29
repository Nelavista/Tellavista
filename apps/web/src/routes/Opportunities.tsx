/**
 * Opportunities (B8).
 *
 * Every row answers the only two questions that matter: can I do this, and if
 * not, what exactly is missing? The verdict comes from the API's matching engine
 * and is never recomputed here, so the list and the detail cannot disagree.
 */
import type { OpportunityListOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowRight, Briefcase } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';

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
        <PageHeader eyebrow="Work" title="Opportunities" />
        <Banner tone="info">
          <p>
            Opportunities are not switched on for this environment yet. Your learning and proof are
            unaffected.
          </p>
        </Banner>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Opportunities" />
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

  const rows = resource.data.opportunities;
  const eligible = rows.filter((row) => row.match.eligible).length;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Work"
        title="Opportunities"
        description={
          rows.length === 0
            ? 'No opportunity is open right now. New work appears here when it is published.'
            : `${eligible} of ${rows.length} open ${rows.length === 1 ? 'role fits' : 'roles fit'} what you have proved so far.`
        }
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/work">
              My work
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/earnings">
              Earnings
            </Link>
          </>
        }
      />

      <Panel title="Open roles" actions={<Badge tone="info">{rows.length}</Badge>}>
        {rows.length === 0 ? (
          <EmptyState
            body="Matching uses your verified skills. New work appears here when it is published."
            icon={Briefcase}
            image={EMPTY_IMAGES.opportunities}
            title="Nothing open right now"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/verification">
                Check your proof
              </Link>
            }
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {rows.map((row) => (
              <li key={row.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <Link className="nv-h3" to={`/opportunities/${row.slug}`}>
                      {row.title}
                    </Link>
                    <p className="nv-meta">
                      {row.type === 'managed' ? 'Managed by Nelavista' : 'External listing'}
                      {row.client_name ? ` · ${row.client_name}` : ''} ·{' '}
                      {rateLabel(row.currency, row.rate_minor)}
                    </p>
                  </div>
                  <Badge tone={row.match.eligible ? 'success' : 'warning'}>
                    {row.match.eligible ? 'You qualify' : 'Not yet'}
                  </Badge>
                </div>

                {row.description ? <p className="nv-muted">{row.description}</p> : null}

                {row.match.qualifies_because.length > 0 && row.match.eligible ? (
                  <p className="nv-muted">Because: {row.match.qualifies_because.join(' · ')}</p>
                ) : null}

                {!row.match.eligible && row.match.next_steps.length > 0 ? (
                  <div style={{ marginTop: 'var(--nv-space-sm)' }}>
                    <p className="nv-label">To qualify:</p>
                    <ul className="nv-list">
                      {row.match.next_steps.map((step) => (
                        <li key={step.requirement_id}>{step.detail}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}

                <div style={{ marginTop: 'var(--nv-space-sm)' }}>
                  <Link
                    className="nv-button nv-button--ghost nv-button--sm"
                    to={`/opportunities/${row.slug}`}
                  >
                    Read the brief
                    <ArrowRight aria-hidden="true" size={14} />
                  </Link>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}
