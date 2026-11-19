/**
 * Published platform announcements, shown in place above the screen.
 *
 * Ops writes a notice once (`/v1/ops/announcements`) and publishes it; this is
 * the other end, so the same message reaches students without a deploy or an
 * email. Two rules shape it:
 *
 * * it never blocks the page - a failed or slow read renders nothing, because
 *   an announcement is news, not a dependency of the screen behind it;
 * * dismissing hides that announcement id only, and the choice survives a
 *   reload, so "I have read this" is remembered while the next notice still
 *   arrives.
 */
import type { AnnouncementListOut } from '@nelavista/api-client';
import * as React from 'react';

import { dismissAnnouncement, readDismissedIds } from '../lib/announcements';
import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';
import { Banner, Button } from '../ui';

/** More than a couple at once is a wall, not a notice. The rest stay published. */
const MAX_SHOWN = 2;

export function AnnouncementBanner(): JSX.Element | null {
  const { resource } = useApiResource<AnnouncementListOut>('/announcements');
  const [dismissed, setDismissed] = React.useState<number[]>(() => readDismissedIds());

  const visible =
    resource.status === 'ready'
      ? resource.data.announcements.filter((row) => !dismissed.includes(row.id)).slice(0, MAX_SHOWN)
      : [];

  if (visible.length === 0) return null;

  return (
    <div className="nv-stack nv-stack--tight" style={{ marginBottom: 'var(--nv-space-lg)' }}>
      {visible.map((row) => (
        <Banner
          key={row.id}
          tone="info"
          actions={
            <Button onClick={() => setDismissed(dismissAnnouncement(row.id))} type="button" variant="ghost">
              Dismiss
            </Button>
          }
        >
          <p className="nv-h4">{row.title}</p>
          {row.body ? (
            <p className="nv-muted" style={{ marginTop: 'var(--nv-space-2xs)', maxWidth: '78ch' }}>
              {row.body}
            </p>
          ) : null}
          {row.published_at ? (
            <p className="nv-meta" style={{ marginTop: 'var(--nv-space-2xs)' }}>
              {formatDateTime(row.published_at)}
            </p>
          ) : null}
        </Banner>
      ))}
    </div>
  );
}
