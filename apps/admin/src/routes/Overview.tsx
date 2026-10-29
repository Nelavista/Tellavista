/**
 * Operations overview.
 *
 * There is no aggregate endpoint yet, so this screen reads the queues that
 * already exist and says exactly what it found. Nothing here is an estimate:
 * a count is the length of a live list, and "oldest" is the earliest timestamp
 * in that list. If one read fails, the rest of the screen still works and the
 * failed row says so.
 */
import type {
  AuditLogListOut,
  ImportListOut,
  PracticalQueueOut,
  ProjectListOut,
  ReviewQueueOut,
  WaitlistOut,
} from '@nelavista/api-client';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import {
  ArrowRight,
  ClipboardCheck,
  FolderKanban,
  ScrollText,
  ShieldCheck,
  Upload,
  UserPlus,
  type LucideIcon,
} from 'lucide-react';
import * as React from 'react';

import { when } from '../lib/format';
import { useResource, type Resource } from '../lib/resource';

function oldest(values: Array<string | null | undefined>): string | null {
  let best: string | null = null;
  for (const value of values) {
    if (!value) continue;
    const time = new Date(value).getTime();
    if (Number.isNaN(time)) continue;
    if (best === null || time < new Date(best).getTime()) best = value;
  }
  return best;
}

function countOf<T>(resource: Resource<T>, read: (data: T) => number): number | null {
  return resource.status === 'ready' ? read(resource.data) : null;
}

function errorOf(resource: Resource<unknown>): string | null {
  return resource.status === 'error' ? resource.message : null;
}

function AttentionItem({
  icon: Icon,
  label,
  detail,
  href,
  count,
  stampLabel,
  stamp,
  resource,
  onRetry,
}: {
  icon: LucideIcon;
  label: string;
  detail: string;
  href: string;
  count: number | null;
  stampLabel: string;
  stamp: string | null;
  resource: Resource<unknown>;
  onRetry: () => void;
}): JSX.Element {
  const loading = resource.status === 'loading';
  const error = errorOf(resource);

  return (
    <li>
      <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
        <div className="nv-row" style={{ alignItems: 'flex-start', minWidth: 0 }}>
          <Icon aria-hidden="true" size={18} strokeWidth={1.6} />
          <div style={{ minWidth: 0 }}>
            <p className="nv-h4">{label}</p>
            <p className="nv-muted">{detail}</p>
          </div>
        </div>
        <div style={{ minWidth: 132, textAlign: 'right' }}>
          {loading ? (
            <Skeleton height="1.5rem" width="56px" />
          ) : error ? (
            <Badge tone="danger">Unavailable</Badge>
          ) : (
            <p className="nv-stat__value">{count ?? 0}</p>
          )}
          {!loading && !error ? (
            <p className="nv-meta">
              {stampLabel}: {stamp ? when(stamp) : 'Not set'}
            </p>
          ) : null}
        </div>
      </div>
      {error ? (
        <div className="nv-row nv-row--between" style={{ marginTop: 'var(--nv-space-sm)' }}>
          <p className="nv-error">{error}</p>
          <Button size="sm" type="button" variant="ghost" onClick={onRetry}>
            Try again
          </Button>
        </div>
      ) : (
        <div style={{ marginTop: 'var(--nv-space-sm)' }}>
          <a className="nv-button nv-button--ghost nv-button--sm" href={href}>
            Open
            <ArrowRight aria-hidden="true" size={14} />
          </a>
        </div>
      )}
    </li>
  );
}

export function Overview(): JSX.Element {
  const reviews = useResource<ReviewQueueOut>('/work/review-queue');
  const practical = useResource<PracticalQueueOut>('/verification/practical/submissions');
  const waitlist = useResource<WaitlistOut>('/ops/waitlist?limit=500');
  const imports = useResource<ImportListOut>('/ops/imports');
  const projects = useResource<ProjectListOut>('/work/projects');
  const audit = useResource<AuditLogListOut>('/ops/audit-logs?limit=8');

  const latestImport = imports.resource.status === 'ready' ? (imports.resource.data.runs[0] ?? null) : null;
  const liveProjects =
    projects.resource.status === 'ready'
      ? projects.resource.data.projects.filter((row) => row.status === 'active')
      : [];

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Operations"
        title="What needs attention"
        description="Live queues, oldest items and the last recorded actions. Every number is a list length, not an estimate."
        actions={
          <a className="nv-button nv-button--secondary nv-button--sm" href="#/audit">
            <ScrollText aria-hidden="true" size={15} />
            Audit trail
          </a>
        }
      />

      <Panel title="Needs attention" actions={<span className="nv-meta">Read on this page load</span>}>
        <ul className="nv-list nv-list--ruled">
          <AttentionItem
            count={countOf(reviews.resource, (data) => data.queue.length)}
            detail="Student submissions waiting for a quality decision."
            href="#/review"
            icon={ClipboardCheck}
            label="Work review queue"
            onRetry={reviews.reload}
            resource={reviews.resource}
            stamp={oldest(
              reviews.resource.status === 'ready'
                ? reviews.resource.data.queue.map((row) => row.submitted_at)
                : [],
            )}
            stampLabel="Oldest"
          />
          <AttentionItem
            count={countOf(practical.resource, (data) => data.submissions.length)}
            detail="Practical tasks waiting for a reviewer."
            href="#/review"
            icon={ShieldCheck}
            label="Practical verification"
            onRetry={practical.reload}
            resource={practical.resource}
            stamp={oldest(
              practical.resource.status === 'ready'
                ? practical.resource.data.submissions.map((row) => row.submitted_at)
                : [],
            )}
            stampLabel="Oldest"
          />
          <AttentionItem
            count={countOf(waitlist.resource, (data) => data.waitlist.length)}
            detail="Requests for universities that are not covered yet."
            href="#/waitlist"
            icon={UserPlus}
            label="University waitlist"
            onRetry={waitlist.reload}
            resource={waitlist.resource}
            stamp={
              waitlist.resource.status === 'ready'
                ? (waitlist.resource.data.waitlist[0]?.created_at ?? null)
                : null
            }
            stampLabel="Newest"
          />
          <AttentionItem
            count={countOf(imports.resource, (data) => data.runs.length)}
            detail={
              latestImport
                ? `Last run #${latestImport.id} · ${latestImport.mode} · ${latestImport.status}`
                : 'Dry-run and apply receipts for V1 data.'
            }
            href="#/imports"
            icon={Upload}
            label="Import runs"
            onRetry={imports.reload}
            resource={imports.resource}
            stamp={latestImport?.started_at ?? null}
            stampLabel="Last run"
          />
        </ul>
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
          {audit.resource.status === 'loading' ? <Skeleton lines={5} /> : null}
          {audit.resource.status === 'error' ? (
            <ErrorState
              body={audit.resource.message}
              action={
                <Button size="sm" type="button" variant="secondary" onClick={audit.reload}>
                  Try again
                </Button>
              }
            />
          ) : null}
          {audit.resource.status === 'ready' ? (
            audit.resource.data.logs.length === 0 ? (
              <EmptyState
                body="No sensitive action has been recorded yet."
                icon={ScrollText}
                title="The trail is empty"
              />
            ) : (
              <ul className="nv-list">
                {audit.resource.data.logs.map((row) => (
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
          {projects.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
          {projects.resource.status === 'error' ? (
            <ErrorState
              body={projects.resource.message}
              action={
                <Button size="sm" type="button" variant="secondary" onClick={projects.reload}>
                  Try again
                </Button>
              }
            />
          ) : null}
          {projects.resource.status === 'ready' ? (
            liveProjects.length === 0 ? (
              <EmptyState
                body="No project is live. Create one from Projects & cohorts."
                icon={FolderKanban}
                title="Nothing is running"
              />
            ) : (
              <ul className="nv-list">
                {liveProjects.map((row) => (
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
