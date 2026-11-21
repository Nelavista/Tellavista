/**
 * Matches (B8).
 *
 * The ranked list the API already computes, read on its own rather than folded
 * into the opportunity list. Two rules come from the engine and are not
 * recomputed here:
 *
 * * the order is the API's (eligible first, then score), because a client sort
 *   would disagree with the score it is showing;
 * * a blocked match is not a low score. `blocked` means a quality consequence
 *   stops matching, so the screen says that instead of "not yet".
 */
import type { MatchListOut, MatchOut } from '@nelavista/api-client';
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

function MatchRow({ match }: { match: MatchOut }): JSX.Element {
  return (
    <li>
      <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
        <div style={{ minWidth: 0 }}>
          <Link className="nv-h3" to={`/opportunities/${match.slug}`}>
            {match.title}
          </Link>
          <p className="nv-meta">
            {match.type === 'managed' ? 'Managed by Nelavista' : 'External listing'}
            {match.client_name ? ` · ${match.client_name}` : ''} ·{' '}
            {rateLabel(match.currency, match.rate_minor)}
          </p>
        </div>
        <div className="nv-row">
          <Badge tone="neutral">{match.score} fit</Badge>
          <Badge tone={match.blocked ? 'danger' : match.eligible ? 'success' : 'warning'}>
            {match.blocked ? 'Blocked' : match.eligible ? 'You qualify' : 'Not yet'}
          </Badge>
        </div>
      </div>

      {match.blocked && match.blocked_reason ? <p className="nv-muted">{match.blocked_reason}</p> : null}

      {match.qualifies_because.length > 0 ? (
        <p className="nv-muted">Because: {match.qualifies_because.join(' · ')}</p>
      ) : null}

      {match.next_steps.length > 0 ? (
        <div style={{ marginTop: 'var(--nv-space-sm)' }}>
          <p className="nv-label">Closest next step:</p>
          <ul className="nv-list">
            {match.next_steps.map((step) => (
              <li key={step.requirement_id}>{step.detail}</li>
            ))}
          </ul>
        </div>
      ) : null}

      <div style={{ marginTop: 'var(--nv-space-sm)' }}>
        <Link className="nv-button nv-button--ghost nv-button--sm" to={`/opportunities/${match.slug}`}>
          Read the brief
          <ArrowRight aria-hidden="true" size={14} />
        </Link>
      </div>
    </li>
  );
}

export function Matches(): JSX.Element {
  const { resource, reload } = useApiResource<MatchListOut>('/opportunities/matches');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading matches">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Matches" />
        <Banner tone="info">
          <p>Matching is not switched on for this environment yet. Your learning and proof are unaffected.</p>
        </Banner>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Matches" />
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

  const matches = resource.data.matches;
  const eligibleCount = resource.data.eligible_count;
  const blocked = matches.filter((match) => match.blocked);

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Work"
        title="Matches"
        description={
          matches.length === 0
            ? 'No opportunity is open right now. New work appears here when it is published.'
            : `${eligibleCount} of ${matches.length} open ${matches.length === 1 ? 'role matches' : 'roles match'} what you have proved so far, best first.`
        }
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/opportunities">
              All openings
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/verification">
              Check your proof
            </Link>
          </>
        }
      />

      {blocked.length > 0 ? (
        <Banner tone="warning">
          <p>
            {blocked.length === 1
              ? 'One match is blocked by a quality consequence.'
              : `${blocked.length} matches are blocked by a quality consequence.`}{' '}
            Open the brief to see what the engine recorded; a re-review is the only way back.
          </p>
        </Banner>
      ) : null}

      <Panel title="Ranked for you" actions={<Badge tone="info">{matches.length}</Badge>}>
        {matches.length === 0 ? (
          <EmptyState
            body="Matching uses your verified skills and requirements. New work appears here when it is published."
            icon={Briefcase}
            image={EMPTY_IMAGES.opportunities}
            title="Nothing to match yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/verification">
                Check your proof
              </Link>
            }
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {matches.map((match) => (
              <MatchRow key={match.opportunity_id} match={match} />
            ))}
          </ul>
        )}
      </Panel>

      <p className="nv-muted">
        The score and the order come from the API. A missing requirement is shown on the brief, and
        eligibility for paid work is separate from fit for one role.
      </p>
    </div>
  );
}
