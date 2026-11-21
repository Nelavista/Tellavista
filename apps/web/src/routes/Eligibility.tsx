/**
 * Eligibility (G5).
 *
 * The platform rules that decide whether a student may accept paid work, read on
 * their own so a blocked student has one place to go instead of discovering a
 * blocker on an opportunity they wanted.
 *
 * `blockers` are stable codes and `reasons` are the API's own sentences. This
 * screen maps the code to the action that clears it and never writes its own
 * verdict: the badge is `eligible` as returned, not as inferred.
 */
import type { EligibilityOut, PlatformConfigOut } from '@nelavista/api-client';
import { Badge, Banner, Button, Checkbox, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ShieldCheck } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

const BLOCKER_COPY: Record<string, { title: string; action?: { label: string; to: string } }> = {
  email_unverified: {
    title: 'Confirm your email address',
    action: { label: 'Resend the confirmation email', to: '/settings' },
  },
  date_of_birth_missing: {
    title: 'Add your date of birth',
    action: { label: 'Add it in Settings', to: '/settings' },
  },
  under_minimum_age: { title: 'Paid work starts at the platform minimum age' },
  guardian_consent_required: { title: 'A parent or guardian has to agree to the contributor terms' },
  contributor_terms_required: {
    title: 'Accept the contributor terms',
    action: { label: 'Read them', to: '/legal/contributor-terms' },
  },
};

export function Eligibility(): JSX.Element {
  const eligibility = useApiResource<EligibilityOut>('/platform/me/eligibility');
  const config = useApiResource<PlatformConfigOut>('/platform/config');
  const [checked, setChecked] = React.useState(false);
  const [busy, setBusy] = React.useState(false);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  if (eligibility.resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading eligibility">
        <Skeleton height="2rem" width="35%" />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (eligibility.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Eligibility" />
        <Banner tone="info">
          <p>Eligibility checks are not switched on for this environment yet.</p>
        </Banner>
      </div>
    );
  }

  if (eligibility.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Eligibility" />
        <ErrorState
          body={eligibility.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={eligibility.reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const data = eligibility.resource.data;
  const version = config.resource.status === 'ready' ? config.resource.data.contributor_terms_version : null;
  const termsBody = config.resource.status === 'ready' ? config.resource.data.contributor_terms_body : null;
  const needsTerms = data.blockers.includes('contributor_terms_required');

  async function acceptTerms(): Promise<void> {
    if (!version) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      await http.post('/auth/consent', {
        kind: 'contributor_terms',
        document_version: version,
        granted: true,
      });
      setNote(`Contributor terms ${version} accepted.`);
      setChecked(false);
      eligibility.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not record your acceptance.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Work"
        title="Eligibility"
        description="What the platform checks before you can accept paid work. Fitting a role is separate: a match can be a good fit while this page still has a blocker."
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/opportunities/matches">
              See your matches
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/verification">
              Check your proof
            </Link>
          </>
        }
      />

      <Panel
        title="Platform decision"
        actions={
          <Badge tone={data.eligible ? 'success' : 'warning'}>{data.eligible ? 'Eligible' : 'Blocked'}</Badge>
        }
      >
        <div className="nv-stack">
          <p>
            {data.eligible
              ? 'You meet the platform rules for paid work. Each opportunity still checks its own requirements.'
              : `${data.blockers.length === 1 ? 'One rule is' : `${data.blockers.length} rules are`} still open before you can accept paid work.`}
          </p>

          {data.blockers.length > 0 ? (
            <ul className="nv-list nv-list--ruled">
              {data.blockers.map((blocker) => {
                const copy = BLOCKER_COPY[blocker];
                return (
                  <li key={blocker} className="nv-row nv-row--between">
                    <div className="nv-stack nv-stack--tight">
                      <strong>{copy?.title ?? blocker}</strong>
                      {data.reasons[data.blockers.indexOf(blocker)] ? (
                        <span className="nv-muted">{data.reasons[data.blockers.indexOf(blocker)]}</span>
                      ) : null}
                    </div>
                    {copy?.action ? (
                      <Link className="nv-button nv-button--secondary nv-button--sm" to={copy.action.to}>
                        {copy.action.label}
                      </Link>
                    ) : null}
                  </li>
                );
              })}
            </ul>
          ) : null}

          <p className="nv-meta">
            Contributor terms {data.contributor_terms_version}
            {data.age !== null ? ` · age ${data.age}` : ' · age unknown'}
            {` · paid work from ${data.min_student_age}, guardian consent below ${data.guardian_consent_below_age}`}
          </p>
        </div>
      </Panel>

      {needsTerms ? (
        <Panel title={`Contributor terms ${data.contributor_terms_version}`}>
          <div className="nv-stack">
            {termsBody ? (
              <div className="nv-prose" style={{ maxHeight: 260, overflow: 'auto' }}>
                {termsBody.split('\n').map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
              </div>
            ) : (
              <p className="nv-muted">
                Read the <Link to="/legal/contributor-terms">contributor terms</Link> before accepting.
              </p>
            )}
            <Checkbox
              checked={checked}
              label={`I have read and accept contributor terms ${data.contributor_terms_version}.`}
              onChange={(event) => setChecked(event.target.checked)}
            />
            {note ? <p role="status">{note}</p> : null}
            {error ? (
              <p className="nv-error" role="alert">
                {error}
              </p>
            ) : null}
            <div>
              <Button
                disabled={!checked || busy || !version}
                type="button"
                onClick={() => void acceptTerms()}
              >
                {busy ? 'Recording' : 'Accept and record'}
              </Button>
            </div>
          </div>
        </Panel>
      ) : null}

      {!data.eligible && data.blockers.includes('email_unverified') ? <ResendVerification /> : null}

      {!data.eligible && data.blockers.includes('date_of_birth_missing') ? (
        <Banner tone="info">
          <p>
            Your date of birth is only used for these age rules and is not shown on your public profile. Add
            it under <Link to="/settings">Settings → Profile</Link>.
          </p>
        </Banner>
      ) : null}

      <p className="nv-muted">
        <ShieldCheck aria-hidden="true" size={14} /> Eligibility is evaluated by the API on every read; this
        page never decides it in the browser.
      </p>
    </div>
  );
}

function ResendVerification(): JSX.Element {
  const [busy, setBusy] = React.useState(false);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  async function resend(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      const result = await http.post<{ message: string }>('/auth/email/verify/resend');
      setNote(result.message);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send the email.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Banner
      tone="warning"
      actions={
        <Button disabled={busy} size="sm" type="button" variant="secondary" onClick={() => void resend()}>
          {busy ? 'Sending' : 'Resend email'}
        </Button>
      }
    >
      <div className="nv-stack nv-stack--tight">
        <strong>Your email is not confirmed yet.</strong>
        {note ? <p role="status">{note}</p> : null}
        {error ? (
          <p className="nv-error" role="alert">
            {error}
          </p>
        ) : null}
      </div>
    </Banner>
  );
}
