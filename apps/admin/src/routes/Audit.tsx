/**
 * Audit trail (C1).
 *
 * Append-only by construction; this screen only reads. A row names the actor,
 * the action, the target, the reason and the request id, so a decision can be
 * tied to the exact request that made it.
 */
import type { AuditLogListOut } from '@nelavista/api-client';
import { Badge, Button, EmptyState, ErrorState, Field, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ScrollText } from 'lucide-react';
import * as React from 'react';

import { useResource } from '../lib/resource';
import { when } from '../lib/format';

export function Audit(): JSX.Element {
  const [action, setAction] = React.useState('');
  const [targetType, setTargetType] = React.useState('');
  const query = new URLSearchParams();
  if (action.trim()) query.set('action', action.trim());
  if (targetType.trim()) query.set('target_type', targetType.trim());
  const suffix = query.toString() ? `?${query.toString()}` : '';
  const { resource, reload } = useResource<AuditLogListOut>(`/ops/audit-logs${suffix}`);

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Trust"
        title="Audit trail"
        description="Every sensitive action is recorded with its actor, reason and request id. There is no route that edits or deletes a row."
      />

      <Panel title="Filter">
        <form
          className="nv-row"
          style={{ alignItems: 'flex-end' }}
          onSubmit={(event) => {
            event.preventDefault();
            reload();
          }}
        >
          <div style={{ flex: 1, minWidth: 200 }}>
            <Field
              hint="Exact action, for example payout.approved."
              id="audit-action"
              label="Action"
              placeholder="payout.approved"
              value={action}
              onChange={(event) => setAction(event.target.value)}
            />
          </div>
          <div style={{ flex: 1, minWidth: 200 }}>
            <Field
              hint="For example payout_batch."
              id="audit-target"
              label="Target type"
              placeholder="payout_batch"
              value={targetType}
              onChange={(event) => setTargetType(event.target.value)}
            />
          </div>
          <Button type="submit">Filter</Button>
        </form>
      </Panel>

      {resource.status === 'loading' ? <Skeleton lines={5} /> : null}
      {resource.status === 'error' ? (
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
      ) : null}
      {resource.status === 'ready' ? (
        <Panel title="Entries" actions={<Badge tone="neutral">{resource.data.logs.length}</Badge>}>
          {resource.data.logs.length === 0 ? (
            <EmptyState
              body="Nothing matches those filters. Clear them to see the full trail."
              icon={ScrollText}
              title="No entries"
            />
          ) : (
            <div className="nv-table-wrap">
              <table className="nv-table">
                <thead>
                  <tr>
                    <th>When</th>
                    <th>Actor</th>
                    <th>Action</th>
                    <th>Target</th>
                    <th>Reason / context</th>
                    <th>Request</th>
                  </tr>
                </thead>
                <tbody>
                  {resource.data.logs.map((row) => (
                    <tr key={row.id}>
                      <td>{when(row.created_at)}</td>
                      <td>
                        {row.actor_user_id ?? 'system'}
                        <div className="nv-muted">{row.actor_role_code ?? ''}</div>
                      </td>
                      <td>{row.action}</td>
                      <td>
                        {row.target_type ?? '—'}
                        <div className="nv-muted">{row.target_id ?? ''}</div>
                      </td>
                      <td>
                        {row.reason ?? '—'}
                        {row.context ? (
                          <pre className="nv-pre nv-muted">{JSON.stringify(row.context)}</pre>
                        ) : null}
                      </td>
                      <td className="nv-muted">{row.request_id ?? '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
      ) : null}
    </div>
  );
}
