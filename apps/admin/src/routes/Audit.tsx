/**
 * Audit trail (C1).
 *
 * Append-only by construction; this screen only reads. A row names the actor,
 * the action, the target, the reason and the request id, so a decision can be
 * tied to the exact request that made it.
 */
import type { AuditLogListOut } from '@nelavista/api-client';
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
      <h1 className="nv-h1">Audit trail</h1>
      <p className="nv-muted">
        Every sensitive action is recorded with its actor, reason and request id. There is no route that
        edits or deletes a row.
      </p>

      <form
        className="nv-row"
        onSubmit={(event) => {
          event.preventDefault();
          reload();
        }}
      >
        <div>
          <label className="nv-label" htmlFor="audit-action">
            Action
          </label>
          <input
            className="nv-input"
            id="audit-action"
            placeholder="payout.approved"
            value={action}
            onChange={(event) => setAction(event.target.value)}
          />
        </div>
        <div>
          <label className="nv-label" htmlFor="audit-target">
            Target type
          </label>
          <input
            className="nv-input"
            id="audit-target"
            placeholder="payout_batch"
            value={targetType}
            onChange={(event) => setTargetType(event.target.value)}
          />
        </div>
        <button className="nv-button" type="submit">
          Filter
        </button>
      </form>

      {resource.status === 'loading' ? <p className="nv-muted">Loading…</p> : null}
      {resource.status === 'error' ? (
        <div className="nv-card">
          <p className="nv-error">{resource.message}</p>
          <button className="nv-button" type="button" onClick={reload}>
            Try again
          </button>
        </div>
      ) : null}
      {resource.status === 'ready' ? (
        <div className="nv-card">
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
              {resource.data.logs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="nv-muted">
                    Nothing matches those filters.
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
