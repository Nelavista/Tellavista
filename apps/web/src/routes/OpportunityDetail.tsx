/**
 * One opportunity (B8): the brief, every requirement with its verdict, and the
 * closing step for the ones that are not met yet.
 *
 * Managed work is invitation-only, so the apply form appears only for external
 * listings. The API enforces the same rule; this screen just does not offer an
 * action that would fail.
 */
import type { ApplyOut, EligibilityOut, OpportunityOut } from '@nelavista/api-client';
import { Badge, Banner, Button, ErrorState, PageHeader, Panel, Skeleton, Textarea } from '@nelavista/ui';
import { ArrowRight, Briefcase, ShieldCheck } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

export function OpportunityDetail(): JSX.Element {
  const { slug = '' } = useParams<{ slug: string }>();
  const { resource, reload } = useApiResource<OpportunityOut>(`/opportunities/${slug}`);
  const eligibility = useApiResource<EligibilityOut>('/platform/me/eligibility');
  const [note, setNote] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [applied, setApplied] = React.useState<ApplyOut | null>(null);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this opportunity">
        <Skeleton height="2rem" width="55%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Opportunity" />
        <Banner tone="info">
          <p>Opportunities are not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/opportunities">All opportunities</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Opportunity" />
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
        <p className="nv-muted">
          <Link to="/opportunities">All opportunities</Link>
        </p>
      </div>
    );
  }

  const opportunity = resource.data;
  const eligibilityBlocked = eligibility.resource.status === 'ready' && !eligibility.resource.data.eligible;

  async function apply(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const result = await http.post<ApplyOut>(`/opportunities/${opportunity.slug}/apply`, {
        note: note.trim() || null,
      });
      setApplied(result);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your application.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow={opportunity.type === 'managed' ? 'Managed work' : 'External listing'}
        title={opportunity.title}
        description={[
          opportunity.client_name,
          opportunity.headcount ? `${opportunity.headcount} place(s)` : null,
          opportunity.currency && opportunity.rate_minor != null
            ? `${opportunity.currency} ${(opportunity.rate_minor / 100).toFixed(2)} per approved task`
            : 'Rate shared on the brief',
        ]
          .filter(Boolean)
          .join(' · ')}
        actions={
          <Badge
            status={opportunity.match.eligible ? 'verified' : 'at_risk'}
            tone={opportunity.match.eligible ? 'success' : 'warning'}
          >
            {opportunity.match.eligible ? 'You qualify' : 'Not yet'}
          </Badge>
        }
      />

      {opportunity.description ? <p>{opportunity.description}</p> : null}

      <Panel title="What this needs">
        {opportunity.requirements.length === 0 ? (
          <p className="nv-muted">This brief has no formal requirements.</p>
        ) : (
          <ul className="nv-list nv-list--ruled">
            {opportunity.match.explanation.map((check) => (
              <li key={check.requirement_id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div>
                    <Badge
                      status={check.met ? 'verified' : 'at_risk'}
                      tone={check.met ? 'success' : check.mandatory ? 'danger' : 'warning'}
                    >
                      {check.met ? 'Met' : check.mandatory ? 'Missing' : 'Optional'}
                    </Badge>{' '}
                    <span>{check.description}</span>
                    <span className="nv-muted"> · {check.detail}</span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}

        {opportunity.match.next_steps.length > 0 ? (
          <div style={{ marginTop: 'var(--nv-space-xl)' }}>
            <h3 className="nv-h3">How to close the gap</h3>
            <ul className="nv-list">
              {opportunity.match.next_steps.map((step) => (
                <li key={step.requirement_id}>
                  {step.detail}
                  {step.closes_via.assessment_id ? (
                    <>
                      {' '}
                      <Link to="/verification">Sit the assessment</Link>
                    </>
                  ) : step.closes_via.learning_path_id ? (
                    <>
                      {' '}
                      <Link to="/skills">Open the learning path</Link>
                    </>
                  ) : null}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </Panel>

      <Panel title="Before you apply" actions={<ShieldCheck aria-hidden="true" size={16} />}>
        {eligibility.resource.status === 'loading' ? <Skeleton lines={2} /> : null}
        {eligibility.resource.status === 'off' ? (
          <Banner tone="info">
            <p>Eligibility checks are not switched on for this environment yet.</p>
          </Banner>
        ) : null}
        {eligibility.resource.status === 'error' ? (
          <Banner
            tone="warning"
            actions={
              <Button size="sm" type="button" variant="secondary" onClick={eligibility.reload}>
                Try again
              </Button>
            }
          >
            <p>{eligibility.resource.message}</p>
          </Banner>
        ) : null}
        {eligibility.resource.status === 'ready' ? (
          <div className="nv-stack">
            <div className="nv-row nv-row--between">
              <p>
                {eligibility.resource.data.eligible
                  ? 'You meet the platform rules for paid work.'
                  : 'The platform still has a blocker before you can accept paid work.'}
              </p>
              <Badge tone={eligibility.resource.data.eligible ? 'success' : 'warning'}>
                {eligibility.resource.data.eligible ? 'Eligible' : 'Blocked'}
              </Badge>
            </div>
            {eligibility.resource.data.blockers.length > 0 ? (
              <ul className="nv-list">
                {eligibility.resource.data.blockers.map((blocker) => (
                  <li key={blocker}>{blocker}</li>
                ))}
              </ul>
            ) : null}
            {eligibility.resource.data.reasons.length > 0 ? (
              <p className="nv-muted">Why: {eligibility.resource.data.reasons.join(' · ')}</p>
            ) : null}
            <p className="nv-meta">
              Contributor terms {eligibility.resource.data.contributor_terms_version}
              {eligibility.resource.data.age !== null ? ` · age ${eligibility.resource.data.age}` : ''}
            </p>
          </div>
        ) : null}
      </Panel>

      {error ? (
        <Banner tone="danger">
          <p>{error}</p>
        </Banner>
      ) : null}

      {applied ? (
        <Banner tone="success">
          <h2 className="nv-h3">Application sent</h2>
          <p>
            Status: <strong>{applied.status.replace(/_/g, ' ')}</strong>. We will contact you here if the
            client shortlists you.
          </p>
          <p className="nv-muted">
            <Link to="/opportunities/applications">See all your applications</Link>
          </p>
        </Banner>
      ) : opportunity.type === 'external' ? (
        <Panel title="Apply" actions={<Briefcase aria-hidden="true" size={16} />}>
          <p className="nv-muted">
            One short note helps the client see how your proof fits. You can apply once.
          </p>
          <Textarea
            hint="Optional. Up to 1,000 characters."
            id="nv-apply-note"
            label="Note"
            maxLength={1000}
            rows={4}
            value={note}
            onChange={(event) => setNote(event.target.value)}
          />
          <div style={{ marginTop: 'var(--nv-space-lg)' }}>
            <Button disabled={busy || eligibilityBlocked} type="button" onClick={() => void apply()}>
              {busy ? 'Sending…' : 'Apply'}
              <ArrowRight aria-hidden="true" size={15} />
            </Button>
            {eligibilityBlocked ? (
              <p className="nv-muted">Resolve the platform blocker above before applying.</p>
            ) : null}
          </div>
        </Panel>
      ) : (
        <Banner tone="info">
          <p>
            Managed work is invitation-only. Matching runs against your verified skills; there is nothing to
            apply for here.
          </p>
        </Banner>
      )}

      <p className="nv-muted">
        <Link to="/verification">Prove a skill</Link> · <Link to="/work">Your work</Link> ·{' '}
        <Link to="/opportunities">All opportunities</Link>
      </p>
    </div>
  );
}
