/**
 * Public site: what a visitor sees on /impact, and whether it is published.
 *
 * The figures are the same aggregates the public page reads, fetched through the
 * admin preview so a hidden block is still visible to ops. Publishing is a
 * platform setting: switching it off removes the numbers from the public
 * payload rather than hiding them in the browser.
 *
 * Analytics status is shown from this build's own environment. A VITE_* value
 * is baked in at build time, so this is a deployment check, not a live probe.
 */
import type { ImpactOut, PlatformSettingsOut } from '@nelavista/api-client';
import { Badge, Banner, ErrorNote, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowUpRight, BarChart3, Eye, EyeOff, RefreshCw } from 'lucide-react';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { when } from '../lib/format';
import { useResource } from '../lib/resource';
import { useSession } from '../lib/session';

function money(amountMinor: number, currency: string): string {
  const amount = amountMinor / 100;
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency,
      maximumFractionDigits: 2,
    }).format(amount);
  } catch {
    return `${currency} ${amount.toFixed(2)}`;
  }
}

export function PublicSite(): JSX.Element {
  const { me } = useSession();
  const impact = useResource<ImpactOut>('/platform/impact/admin');
  const settings = useResource<PlatformSettingsOut>('/platform/settings');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  const canWrite = me?.role === 'super_admin';
  const enabled = settings.resource.status === 'ready' ? settings.resource.data.impact_metrics_enabled : null;
  const analyticsConfigured = Boolean(import.meta.env.VITE_POSTHOG_KEY);
  const publicSiteUrl =
    (import.meta.env.VITE_PUBLIC_SITE_URL as string | undefined)?.replace(/\/$/, '') ??
    'https://nelavista.com';

  async function toggle(): Promise<void> {
    if (!canWrite || enabled === null) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      await http.patch<PlatformSettingsOut>('/platform/settings', {
        impact_metrics_enabled: !enabled,
      });
      setNote(
        enabled
          ? 'Impact figures are now published on /impact.'
          : 'Impact figures are no longer published. The admin preview still shows them.',
      );
      settings.reload();
      impact.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not change the impact setting.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Public site"
        title="What the public page publishes"
        description="The /impact page reads aggregates from the product database. Review them here before they appear on the marketing site."
        actions={
          <div className="nv-row">
            <button
              className="nv-button nv-button--secondary nv-button--sm"
              disabled={busy}
              type="button"
              onClick={() => {
                impact.reload();
                settings.reload();
              }}
            >
              <RefreshCw aria-hidden="true" size={15} />
              Refresh
            </button>
            <a
              className="nv-button nv-button--secondary nv-button--sm"
              href={`${publicSiteUrl}/impact`}
              rel="noreferrer"
              target="_blank"
            >
              Open public page
              <ArrowUpRight aria-hidden="true" size={14} />
            </a>
          </div>
        }
      />

      <ErrorNote message={error} />
      {note ? <Banner tone="success">{note}</Banner> : null}

      <Panel
        title="Impact figures"
        actions={
          enabled === null ? (
            <span className="nv-meta">Reading…</span>
          ) : (
            <Badge tone={enabled ? 'success' : 'warning'}>
              {enabled ? (
                <>
                  <Eye aria-hidden="true" size={12} /> Published
                </>
              ) : (
                <>
                  <EyeOff aria-hidden="true" size={12} /> Hidden
                </>
              )}
            </Badge>
          )
        }
      >
        <p className="nv-muted">
          Every number is a count from current rows: verified skills, passed assessments, reviewed practical
          work and approved paid work. No estimate, sample or projection is included.
          {impact.resource.status === 'ready' ? ` Generated ${when(impact.resource.data.generated_at)}.` : ''}
        </p>

        {impact.resource.status === 'error' ? (
          <ErrorState title="Impact figures did not load" body={impact.resource.message} />
        ) : null}

        {impact.resource.status === 'loading' ? <Skeleton lines={6} /> : null}

        {impact.resource.status === 'ready' ? (
          <>
            <div className="nv-grid">
              {impact.resource.data.metrics.map((metric) => (
                <div className="nv-card" key={metric.key}>
                  <p className="nv-meta">{metric.label}</p>
                  <p className="nv-stat__value">{metric.value.toLocaleString()}</p>
                  <p className="nv-muted">{metric.detail}</p>
                </div>
              ))}
            </div>

            <div className="nv-row nv-row--between" style={{ marginTop: 'var(--nv-space-md)' }}>
              <div>
                <p className="nv-meta">Paid to students</p>
                {impact.resource.data.paid_by_currency.length === 0 ? (
                  <p className="nv-muted">Nothing has been marked paid yet.</p>
                ) : (
                  <ul className="nv-list">
                    {impact.resource.data.paid_by_currency.map((row) => (
                      <li key={row.currency}>
                        <span className="nv-h4">{money(row.amount_minor, row.currency)}</span>
                        <span className="nv-meta"> · {row.currency}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </>
        ) : null}

        <div className="nv-row" style={{ marginTop: 'var(--nv-space-md)' }}>
          <button
            className="nv-button"
            disabled={busy || !canWrite || enabled === null}
            type="button"
            onClick={() => void toggle()}
          >
            {enabled ? 'Stop publishing figures' : 'Publish figures'}
          </button>
          <span className="nv-muted">
            {canWrite
              ? 'The change is audited and applies to the next public read.'
              : 'Only a super admin can change what the public page publishes.'}
          </span>
        </div>
      </Panel>

      <Panel title="Analytics and error tracking">
        <p className="nv-muted">
          Both apps report page views and unhandled errors to PostHog when this build carries a project key.
          Without a key they send nothing and keep the local console useful; no Sentry project is used.
        </p>
        <div className="nv-list">
          <div className="nv-row nv-row--between">
            <span>
              <BarChart3 aria-hidden="true" size={16} /> This admin build
            </span>
            <Badge tone={analyticsConfigured ? 'success' : 'warning'}>
              {analyticsConfigured ? 'Configured' : 'Not configured'}
            </Badge>
          </div>
        </div>
        <p className="nv-muted">
          Configure <code>VITE_POSTHOG_KEY</code> and <code>VITE_POSTHOG_HOST</code> in the web and admin
          build environments, and <code>POSTHOG_API_KEY</code> in the API environment for server journey
          events and unhandled-error reports.
        </p>
      </Panel>
    </div>
  );
}
