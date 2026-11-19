/**
 * Operations overview.
 *
 * This screen used to read six list endpoints and do its own arithmetic, which
 * meant six round trips and six different moments in time -- the counts could
 * disagree with each other and with the audit rows underneath them. It now reads
 * `/ops/overview` once: every count and its timestamp come from the same query on
 * the server, and the audit rows are read after them.
 *
 * A queue is still a real list length, not an estimate; the server caps each list
 * at 200/500 rows and the count is the length of that list.
 */
import type { OverviewOut } from '@nelavista/api-client';
import {
  Badge,
  Button,
  EmptyState,
  ErrorState,
  PageHeader,
  Panel,
  Skeleton,
} from '@nelavista/ui';
import {
  ArrowRight,
  ClipboardCheck,
  FolderKanban,
  RefreshCw,
  ScrollText,
  ShieldCheck,
  Upload,
  UserPlus,
  type LucideIcon,
} from 'lucide-react';
import * as React from 'react';

import { when } from '../lib/format';
import { useResource } from '../lib/resource';

const ICONS: Record<string, LucideIcon> = {
  work_review: ClipboardCheck,
  practical_review: ShieldCheck,
  waitlist: UserPlus,
  imports: Upload,
};

export function Overview(): JSX.Element {
  const overview = useResource<OverviewOut>('/ops/overview');
  const [busy, setBusy] = React.useState(false);

  async function refresh(): Promise<void> {
    setBusy(true);
    try {
      overview.reload();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Operations"
        title="What needs attention"
        description="Live queues, oldest items and the last recorded actions, read in one pass. Every number is a list length, not an estimate."
        actions={
          <div className="nv-row">
            <button
              className="nv-button nv-button--secondary nv-button--sm"
              disabled={busy}
              type="button"
              onClick={() => void refresh()}
            >
              <RefreshCw aria-hidden="true" size={15} />
              {busy ? 'Reading…' : 'Refresh'}
            </button>
            <a className="nv-button nv-button--secondary nv-button--sm" href="#/audit">
              <ScrollText aria-hidden="true" size={15} />
              Audit trail
            </a>
          </div>
        }
      />

      {overview.resource.status === 'error' ? (
        <ErrorState
          body={overview.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={overview.reload}>
              Try again
            </Button>
          }
        />
      ) : null}

      <Panel
        title="Needs attention"
        actions={
          <span className="nv-meta">
            {overview.resource.status === 'ready'
              ? `Generated ${when(overview.resource.data.generated_at)}`
              : 'Reading…'}
          </span>
        }
      >
        {overview.resource.status === 'loading' ? <Skeleton lines={5} /> : null}
        {overview.resource.status === 'ready' ? (
          <ul className="nv-list nv-list--ruled">
            {overview.resource.data.queues.map((row) => {
              const Icon = ICONS[row.key] ?? ClipboardCheck;
              return (
                <li key={row.key}>
                  <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                    <div className="nv-row" style={{ alignItems: 'flex-start', minWidth: 0 }}>
                      <Icon aria-hidden="true" size={18} strokeWidth={1.6} />
                      <div style={{ minWidth: 0 }}>
                        <p className="nv-h4">{row.label}</p>
                        <p className="nv-muted">{row.detail}</p>
                      </div>
                    </div>
                    <div style={{ minWidth: 132, textAlign: 'right' }}>
                      <p className="nv-stat__value">{row.count}</p>
                      <p className="nv-meta">
                        {row.stamp_label}: {row.stamp ? when(row.stamp) : 'Not set'}
                      </p>
                    </div>
                  </div>
                  <div style={{ marginTop: 'var(--nv-space-sm)' }}>
                    <a className="nv-button nv-button--ghost nv-button--sm" href={row.href}>
                      Open
                      <ArrowRight aria-hidden="true" size={14} />
                    </a>
                  </div>
                </li>
              );
            })}
          </ul>
        ) : null}
      </Panel>

      <div className="nv-split">
        <Panel
          title="Recent operations"
          actions={
            <a className="nv-button nv-button--ghost nv-button--sm" href="#/audit">
              Full trail
              <ArrowRight aria-hidden="true" size={14} />
            </a>
          }
        >
          {overview.resource.status === 'loading' ? <Skeleton lines={5} /> : null}
          {overview.resource.status === 'ready' ? (
            overview.resource.data.recent_audit.length === 0 ? (
              <EmptyState
                body="No sensitive action has been recorded yet."
                icon={ScrollText}
                title="The trail is empty"
              />
            ) : (
              <ul className="nv-list">
                {overview.resource.data.recent_audit.map((row) => (
                  <li key={row.id}>
                    <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                      <div style={{ minWidth: 0 }}>
                        <p className="nv-mono">{row.action}</p>
                        <p className="nv-muted">
                          {row.actor_role_code ?? 'system'}
                          {row.target_type ? ` · ${row.target_type}` : ''}
                          {row.target_id ? ` #${row.target_id}` : ''}
                        </p>
                      </div>
                      <span className="nv-meta">{when(row.created_at)}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )
          ) : null}
        </Panel>

        <Panel
          title="Delivery"
          actions={
            <a className="nv-button nv-button--ghost nv-button--sm" href="#/work">
              Projects
              <ArrowRight aria-hidden="true" size={14} />
            </a>
          }
        >
          {overview.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
          {overview.resource.status === 'ready' ? (
            overview.resource.data.live_projects.length === 0 ? (
              <EmptyState
                body="No project is live. Create one from Projects & cohorts."
                icon={FolderKanban}
                title="Nothing is running"
              />
            ) : (
              <ul className="nv-list">
                {overview.resource.data.live_projects.map((row) => (
                  <li key={row.id}>
                    <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                      <div style={{ minWidth: 0 }}>
                        <p className="nv-h4">{row.title}</p>
                        <p className="nv-muted nv-mono">{row.slug}</p>
                      </div>
                      <Badge tone="info">{row.status}</Badge>
                    </div>
                    <p className="nv-meta">
                      {row.starts_on ?? 'no start'} → {row.ends_on ?? 'no end'}
                    </p>
                  </li>
                ))}
              </ul>
            )
          ) : null}
        </Panel>
      </div>
    </div>
  );
}
