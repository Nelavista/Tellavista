import type { NotificationListOut } from '@nelavista/api-client';
import * as React from 'react';

import { formatDateTime } from '../lib/format';
import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Skeleton } from '../ui';

export function Notifications(): JSX.Element {
  const { resource, reload } = useApiResource<NotificationListOut>('/me/notifications');
  const [busy, setBusy] = React.useState(false);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const unread =
    resource.status === 'ready' ? resource.data.notifications.filter((row) => row.read_at === null) : [];

  async function markAllRead(): Promise<void> {
    if (unread.length === 0) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      await http.post('/me/notifications/read', { ids: unread.map((row) => row.id) });
      setNote('All notifications marked read.');
      reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not update notifications.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Account"
        title="Notifications"
        description="Review, payouts, deadlines and verification decisions. Unread items stay at the top of the record."
        actions={
          <Button
            disabled={busy || unread.length === 0}
            onClick={() => void markAllRead()}
            type="button"
            variant="secondary"
          >
            {busy ? 'Marking read' : `Mark ${unread.length || ''} read`.trim()}
          </Button>
        }
      />

      {note ? <Banner tone="success">{note}</Banner> : null}
      {error ? <Banner tone="danger">{error}</Banner> : null}

      {resource.status === 'loading' ? (
        <div className="nv-card nv-stack" aria-busy="true">
          <Skeleton height="1.5rem" width="35%" />
          <Skeleton lines={4} />
        </div>
      ) : resource.status === 'off' ? (
        <EmptyState
          title="Notifications are not switched on here"
          body="This environment has the feature off. It is not a missing account setting."
        />
      ) : resource.status === 'missing' || resource.status === 'error' ? (
        <ErrorState
          title="Notifications did not load"
          body={resource.message}
          action={
            <Button onClick={reload} type="button" variant="secondary">
              Try again
            </Button>
          }
        />
      ) : resource.data.notifications.length === 0 ? (
        <EmptyState
          title="No notifications yet"
          body="When a review, deadline or payout changes, it will appear here. There is nothing to clear."
        />
      ) : (
        <div className="nv-panel">
          <div className="nv-panel__head">
            <h2 className="nv-h3">Inbox</h2>
            <span className="nv-meta">{unread.length} unread</span>
          </div>
          <ul className="nv-list" style={{ padding: '0 var(--nv-space-xl)' }}>
            {resource.data.notifications.map((row) => (
              <li
                key={row.id}
                className="nv-stack nv-stack--tight"
                style={{ paddingBlock: 'var(--nv-space-lg)' }}
              >
                <div className="nv-row nv-row--between">
                  <div className="nv-row">
                    <Badge tone={row.read_at === null ? 'info' : 'neutral'}>
                      {row.kind.replaceAll('_', ' ')}
                    </Badge>
                    <span className="nv-h4">{row.title}</span>
                  </div>
                  <span className="nv-meta">{formatDateTime(row.created_at)}</span>
                </div>
                <p className="nv-muted" style={{ maxWidth: '72ch' }}>
                  {row.body}
                </p>
                {row.read_at === null ? <span className="nv-meta">Unread</span> : null}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
