import type { ApplicationListOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Skeleton } from '../ui';

function toneFor(status: string): 'neutral' | 'success' | 'info' | 'warning' | 'danger' {
  if (['accepted', 'hired', 'completed'].includes(status)) return 'success';
  if (['rejected', 'withdrawn', 'failed'].includes(status)) return 'danger';
  if (['reviewing', 'shortlisted', 'in_progress'].includes(status)) return 'info';
  if (['pending', 'submitted'].includes(status)) return 'warning';
  return 'neutral';
}

export function Applications(): JSX.Element {
  const { resource, reload } = useApiResource<ApplicationListOut>('/opportunities/applications');

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Work"
        title="My applications"
        description="Every application you have made, with its current status and the note the reviewer left."
        actions={
          <Link className="nv-button nv-button--secondary" to="/opportunities">
            Find work
          </Link>
        }
      />

      {resource.status === 'loading' ? (
        <div className="nv-card nv-stack" aria-busy="true">
          <Skeleton height="1.5rem" width="30%" />
          <Skeleton lines={5} />
        </div>
      ) : resource.status === 'off' ? (
        <EmptyState
          title="Applications are not switched on here"
          body="This environment has the feature off. It is not a missing application."
        />
      ) : resource.status === 'missing' || resource.status === 'error' ? (
        <ErrorState
          title="Applications did not load"
          body={resource.message}
          action={
            <Button onClick={reload} type="button" variant="secondary">
              Try again
            </Button>
          }
        />
      ) : resource.data.applications.length === 0 ? (
        <EmptyState
          title="You have not applied yet"
          body="Open an opportunity, read the eligibility reason and apply when the work fits. Your applications will be listed here."
          action={
            <Link className="nv-button" to="/opportunities">
              Browse opportunities
            </Link>
          }
        />
      ) : (
        <div className="nv-table-wrap">
          <table className="nv-table">
            <caption className="nv-sr-only">My applications</caption>
            <thead>
              <tr>
                <th scope="col">Opportunity</th>
                <th scope="col">Type</th>
                <th scope="col">Status</th>
                <th scope="col">Note</th>
                <th scope="col" />
              </tr>
            </thead>
            <tbody>
              {resource.data.applications.map((row) => (
                <tr key={row.id}>
                  <td>
                    <strong>{row.opportunity.title}</strong>
                    <div className="nv-meta">{row.opportunity.slug}</div>
                  </td>
                  <td>{row.opportunity.type}</td>
                  <td>
                    <Badge tone={toneFor(row.status)}>{row.status.replace(/_/g, ' ')}</Badge>
                  </td>
                  <td className="nv-muted" style={{ maxWidth: '34ch' }}>
                    {row.note || 'No note yet.'}
                  </td>
                  <td>
                    <Link className="nv-link-arrow" to={`/opportunities/${row.opportunity.slug}`}>
                      Open
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
