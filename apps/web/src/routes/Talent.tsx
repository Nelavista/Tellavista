/**
 * Talent profile and shares (B13).
 *
 * The profile is evidence: verified skills, quality history, delivered work and
 * the transcript. Nothing here is editable except availability and the share
 * links, because a claim a student can type is not evidence a company can trust.
 *
 * A share link is scoped, expiring and revocable, and its token is shown exactly
 * once. After that the screen can list the link but never reproduce it.
 */
import type { PlatformConfigOut, ShareCreatedOut, ShareListOut, TalentProfileOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

const SCOPE_COPY: Record<string, string> = {
  academic: 'University, department and level',
  transcript: 'Transcript: what was learned, proved and delivered',
  quality: 'Review history and gold-task accuracy',
  work_history: 'Approved work and the projects it was for',
  availability: 'Hours, start date and languages',
};

function when(value: string | null | undefined): string {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : date.toLocaleDateString();
}

export function Talent(): JSX.Element {
  const profile = useApiResource<TalentProfileOut>('/talent/me');
  const shares = useApiResource<ShareListOut>('/talent/me/shares');
  const config = useApiResource<PlatformConfigOut>('/platform/config');

  const [label, setLabel] = React.useState('');
  const [ttlDays, setTtlDays] = React.useState('30');
  const [scopes, setScopes] = React.useState<string[]>(Object.keys(SCOPE_COPY));
  const [created, setCreated] = React.useState<ShareCreatedOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function createShare(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const share = await http.post<ShareCreatedOut>('/talent/me/shares', {
        label: label.trim() || null,
        scopes,
        ttl_days: Number(ttlDays) || 30,
      });
      setCreated(share);
      setLabel('');
      shares.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create that link.');
    } finally {
      setBusy(false);
    }
  }

  async function revoke(shareId: number): Promise<void> {
    setError(null);
    try {
      await http.post(`/talent/me/shares/${shareId}/revoke`, {});
      shares.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not revoke that link.');
    }
  }

  if (profile.resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your talent profile">
        <Skeleton height="2rem" width="30%" />
        <Skeleton lines={3} />
        <Skeleton lines={5} />
      </div>
    );
  }

  if (profile.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Talent profile</h1>
        <p className="nv-banner">
          Sharing your profile is not switched on for this environment yet. Your proof and transcript are unaffected.
        </p>
      </div>
    );
  }

  if (profile.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Talent profile</h1>
        <ErrorNote message={profile.resource.message} />
        <button className="nv-button" type="button" onClick={profile.reload}>
          Try again
        </button>
      </div>
    );
  }

  const data = profile.resource.data;

  return (
    <div className="nv-stack">
      <div className="nv-row nv-row--between">
        <h1 className="nv-h1">Talent profile</h1>
        <span className="nv-tag">{data.visibility === 'private' ? 'private' : 'shared'}</span>
      </div>
      <p className="nv-muted">
        This page is built from evidence only: verified skills, review history and delivered work. A
        company sees only the scopes you grant in a link, and a link can be revoked at any time.
      </p>

      {!data.display_name ? (
        <p className="nv-banner">
          Add a display name in <Link to="/settings">Settings</Link> so a shared profile has a name on it.
        </p>
      ) : null}

      <section className="nv-card">
        <h2 className="nv-h2">Verified skills</h2>
        {data.verified_skills.length === 0 ? (
          <p className="nv-muted">
            No verified skill yet. <Link to="/verification">Take a verification</Link> when you are ready.
          </p>
        ) : (
          <ul className="nv-list">
            {data.verified_skills.map((skill) => (
              <li key={skill.skill_id} className="nv-row nv-row--between">
                <span>{skill.skill ?? `Skill #${skill.skill_id}`}</span>
                <span className="nv-tag" data-tone={skill.at_risk ? 'warn' : 'ok'}>
                  {skill.at_risk ? 'at risk' : 'verified'}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>

      {data.academic ? (
        <section className="nv-card">
          <h2 className="nv-h2">Academic</h2>
          <p>
            {data.academic.university ?? 'University not set'} · {data.academic.department ?? 'Department not set'}
            {data.academic.level ? ` · Level ${data.academic.level}` : ''}
          </p>
        </section>
      ) : null}

      {data.quality?.overall ? (
        <section className="nv-card">
          <h2 className="nv-h2">Quality</h2>
          <p>
            {data.quality.overall.reviews_count} review
            {data.quality.overall.reviews_count === 1 ? '' : 's'} · {data.quality.overall.approvals} approved
            {data.quality.overall.average_score !== null ? ` · ${data.quality.overall.average_score}% average` : ''}
          </p>
          <p className="nv-muted">
            Gold checks: {data.quality.overall.gold_correct} of {data.quality.overall.gold_tasks} correct.
          </p>
        </section>
      ) : null}

      {data.work_history && data.work_history.length > 0 ? (
        <section className="nv-card">
          <h2 className="nv-h2">Delivered work</h2>
          <ul className="nv-list">
            {data.work_history.map((row) => (
              <li key={row.submission_id}>
                <strong>{row.assignment}</strong>
                <span className="nv-muted"> · {row.project.title} · approved {when(row.approved_at)}</span>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {data.transcript ? (
        <section className="nv-card">
          <h2 className="nv-h2">Transcript</h2>
          <p>
            {data.transcript.counts.learned} learned · {data.transcript.counts.proved} proved ·{' '}
            {data.transcript.counts.delivered} delivered
          </p>
          <p className="nv-muted">
            <Link to="/transcript">Open the full transcript</Link>
          </p>
        </section>
      ) : null}

      <section className="nv-card">
        <h2 className="nv-h2">Share a link</h2>
        <p className="nv-muted">
          A link is the only way a company sees this profile. It expires automatically, and you can revoke it
          early; the token is shown once and never again.
        </p>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="share-label">What is this link for?</label>
            <input
              className="nv-input"
              id="share-label"
              maxLength={120}
              placeholder="e.g. Client interview, October"
              value={label}
              onChange={(event) => setLabel(event.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="share-days">Days until it expires</label>
            <input
              className="nv-input"
              id="share-days"
              type="number"
              min={1}
              max={90}
              value={ttlDays}
              onChange={(event) => setTtlDays(event.target.value)}
            />
          </div>
        </div>
        <fieldset className="nv-field">
          <legend className="nv-label">What it includes</legend>
          {Object.entries(SCOPE_COPY).map(([scope, copy]) => (
            <label className="nv-check" key={scope}>
              <input
                type="checkbox"
                checked={scopes.includes(scope)}
                onChange={(event) =>
                  setScopes((current) =>
                    event.target.checked ? [...current, scope] : current.filter((value) => value !== scope),
                  )
                }
              />
              {copy}
            </label>
          ))}
        </fieldset>
        <ErrorNote message={error} />
        <button
          className="nv-button"
          disabled={busy || scopes.length === 0}
          type="button"
          onClick={() => void createShare()}
        >
          Create link
        </button>

        {created ? (
          <div className="nv-banner">
            <p>
              <strong>Copy this link now.</strong> It cannot be shown again.
            </p>
            <p className="nv-code">{`${window.location.origin}/share/${created.token}`}</p>
            <p className="nv-muted">Expires {when(created.expires_at)}.</p>
          </div>
        ) : null}
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">Your links</h2>
        {shares.resource.status === 'ready' ? (
          shares.resource.data.shares.length === 0 ? (
            <p className="nv-muted">No link yet.</p>
          ) : (
            <ul className="nv-list">
              {shares.resource.data.shares.map((share) => (
                <li key={share.id} className="nv-row nv-row--between">
                  <div>
                    <strong>{share.label ?? `Link #${share.id}`}</strong>
                    <div className="nv-muted">
                      {share.scopes.join(', ')} · expires {when(share.expires_at)}
                    </div>
                  </div>
                  {share.active ? (
                    <button className="nv-button nv-button--ghost" type="button" onClick={() => void revoke(share.id)}>
                      Revoke
                    </button>
                  ) : (
                    <span className="nv-tag">{share.revoked_at ? 'revoked' : 'expired'}</span>
                  )}
                </li>
              ))}
            </ul>
          )
        ) : (
          <p className="nv-muted">Loading links…</p>
        )}
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">Working with Nelavista</h2>
        <p className="nv-muted">
          Curriculum owner: {config.resource.status === 'ready' ? config.resource.data.curriculum_owner : '—'} ·{' '}
          {config.resource.status === 'ready' ? config.resource.data.curriculum_license : '—'}
        </p>
        <p className="nv-muted">
          Paid work starts at {config.resource.status === 'ready' ? config.resource.data.min_student_age : 16};
          under {config.resource.status === 'ready' ? config.resource.data.guardian_consent_below_age : 18} needs
          guardian consent. Terms version{' '}
          {config.resource.status === 'ready' ? config.resource.data.contributor_terms_version : '—'}.
        </p>
      </section>
    </div>
  );
}
