/**
 * One opportunity (B8): the brief, every requirement with its verdict, and the
 * closing step for the ones that are not met yet.
 *
 * Managed work is invitation-only, so the apply form appears only for external
 * listings. The API enforces the same rule; this screen just does not offer an
 * action that would fail.
 */
import type { ApplyOut, OpportunityOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

export function OpportunityDetail(): JSX.Element {
  const { slug = '' } = useParams<{ slug: string }>();
  const { resource, reload } = useApiResource<OpportunityOut>(`/opportunities/${slug}`);
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
        <h1 className="nv-h1">Opportunity</h1>
        <p className="nv-banner">Opportunities are not switched on for this environment yet.</p>
        <Link to="/opportunities">All opportunities</Link>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Opportunity</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
        <p className="nv-muted">
          <Link to="/opportunities">All opportunities</Link>
        </p>
      </div>
    );
  }

  const opportunity = resource.data;

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
      <p className="nv-muted">
        <Link to="/opportunities">All opportunities</Link>
      </p>
      <div className="nv-row nv-row--between">
        <h1 className="nv-h1">{opportunity.title}</h1>
        <span className="nv-badge" data-status={opportunity.match.eligible ? 'verified' : 'at_risk'}>
          {opportunity.match.eligible ? 'You qualify' : 'Not yet'}
        </span>
      </div>
      <p className="nv-muted">
        {opportunity.type === 'managed' ? 'Managed by Nelavista' : 'External listing'}
        {opportunity.client_name ? ` · ${opportunity.client_name}` : ''}
        {opportunity.headcount ? ` · ${opportunity.headcount} place(s)` : ''}
      </p>
      {opportunity.description ? <p>{opportunity.description}</p> : null}

      <section className="nv-card">
        <h2 className="nv-h2">What this needs</h2>
        {opportunity.requirements.length === 0 ? (
          <p className="nv-muted">This brief has no formal requirements.</p>
        ) : (
          <ul className="nv-list">
            {opportunity.match.explanation.map((check) => (
              <li className="nv-row nv-row--between" key={check.requirement_id}>
                <span>
                  <span className="nv-badge" data-status={check.met ? 'verified' : 'at_risk'}>
                    {check.met ? 'Met' : check.mandatory ? 'Missing' : 'Optional'}
                  </span>{' '}
                  {check.description}
                  <span className="nv-muted"> · {check.detail}</span>
                </span>
              </li>
            ))}
          </ul>
        )}
        {opportunity.match.next_steps.length > 0 ? (
          <>
            <h3 className="nv-h2">How to close the gap</h3>
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
          </>
        ) : null}
      </section>

      <ErrorNote message={error} />

      {applied ? (
        <section className="nv-card" aria-live="polite">
          <h2 className="nv-h2">Application sent</h2>
          <p>
            Status: <strong>{applied.status.replace(/_/g, ' ')}</strong>. We will contact you here if
            the client shortlists you.
          </p>
        </section>
      ) : opportunity.type === 'external' ? (
        <section className="nv-card">
          <h2 className="nv-h2">Apply</h2>
          <p className="nv-muted">
            One short note helps the client see how your proof fits. You can apply once.
          </p>
          <div className="nv-field">
            <label className="nv-label" htmlFor="nv-apply-note">
              Note (optional)
            </label>
            <textarea
              className="nv-input"
              id="nv-apply-note"
              maxLength={1000}
              rows={4}
              value={note}
              onChange={(event) => setNote(event.target.value)}
            />
          </div>
          <button className="nv-button" disabled={busy} type="button" onClick={() => void apply()}>
            {busy ? 'Sending…' : 'Apply'}
          </button>
        </section>
      ) : (
        <p className="nv-banner">
          Managed work is invitation-only. Matching runs against your verified skills; there is nothing
          to apply for here.
        </p>
      )}

      <p className="nv-muted">
        <Link to="/verification">Prove a skill</Link> · <Link to="/work">Your work</Link>
      </p>
    </div>
  );
}
