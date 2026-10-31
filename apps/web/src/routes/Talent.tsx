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
import type {
  PlatformConfigOut,
  ShareCreatedOut,
  ShareListOut,
  TalentProfileOut,
} from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  Checkbox,
  ConfirmDialog,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Skeleton,
} from '@nelavista/ui';
import { ArrowRight, BadgeCheck, Link2, Share2 } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

const SCOPE_COPY: Record<string, string> = {
  academic: 'University, department and level',
  transcript: 'Transcript: what was learned, proved and delivered',
  quality: 'Review history and gold-task accuracy',
  work_history: 'Approved work and the projects it was for',
  availability: 'Hours, start date and languages',
};

function when(value: string | null | undefined): string {
  if (!value) return 'Not set';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? 'Not set' : date.toLocaleDateString();
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
  const [pendingShareId, setPendingShareId] = React.useState<number | null>(null);
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
    setBusy(true);
    setError(null);
    try {
      await http.post(`/talent/me/shares/${shareId}/revoke`, {});
      shares.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not revoke that link.');
    } finally {
      setBusy(false);
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
        <PageHeader eyebrow="Prove" title="Talent profile" />
        <Banner tone="info">
          <p>
            Sharing your profile is not switched on for this environment yet. Your proof and transcript are
            unaffected.
          </p>
        </Banner>
      </div>
    );
  }

  if (profile.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="Talent profile" />
        <ErrorState
          body={profile.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={profile.reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const data = profile.resource.data;
  const shareRows = shares.resource.status === 'ready' ? shares.resource.data.shares : [];

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Prove"
        title="Talent profile"
        description="Built from evidence only: verified skills, review history and delivered work. A company sees only the scopes you grant in a link, and a link can be revoked at any time."
        actions={
          <>
            <Badge tone={data.visibility === 'private' ? 'neutral' : 'success'}>
              {data.visibility === 'private' ? 'Private' : 'Shared'}
            </Badge>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/transcript">
              <ArrowRight aria-hidden="true" size={15} />
              Transcript
            </Link>
          </>
        }
      />

      {!data.display_name ? (
        <Banner tone="warning">
          <p>
            Add a display name in <Link to="/settings">Settings</Link> so a shared profile has a name on it.
          </p>
        </Banner>
      ) : null}

      <div className="nv-split">
        <div className="nv-stack">
          <Panel title="Verified skills" actions={<Badge tone="info">{data.verified_skills.length}</Badge>}>
            {data.verified_skills.length === 0 ? (
              <EmptyState
                body="Take a verification when you are ready. A finished lesson is progress, not proof."
                icon={BadgeCheck}
                title="No verified skill yet"
                action={
                  <Link className="nv-button nv-button--secondary nv-button--sm" to="/verification">
                    Take a verification
                  </Link>
                }
              />
            ) : (
              <div className="nv-table-wrap">
                <table className="nv-table">
                  <thead>
                    <tr>
                      <th>Skill</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.verified_skills.map((skill) => (
                      <tr key={skill.skill_id}>
                        <td>{skill.skill ?? `Skill #${skill.skill_id}`}</td>
                        <td>
                          <Badge tone={skill.at_risk ? 'warning' : 'success'}>
                            {skill.at_risk ? 'At risk' : 'Verified'}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Panel>

          <Panel title="Academic">
            {data.academic ? (
              <ul className="nv-list">
                <li className="nv-row nv-row--between">
                  <span className="nv-muted">University</span>
                  <span>{data.academic.university ?? 'Not set'}</span>
                </li>
                <li className="nv-row nv-row--between">
                  <span className="nv-muted">Department</span>
                  <span>{data.academic.department ?? 'Not set'}</span>
                </li>
                <li className="nv-row nv-row--between">
                  <span className="nv-muted">Level</span>
                  <span>{data.academic.level ?? 'Not set'}</span>
                </li>
              </ul>
            ) : (
              <EmptyState body="Academic details appear after onboarding." title="Not set" />
            )}
          </Panel>

          <Panel title="Quality">
            {data.quality?.overall ? (
              <div className="nv-stack">
                <div className="nv-grid">
                  <div className="nv-stat">
                    <p className="nv-stat__value">{data.quality.overall.reviews_count}</p>
                    <p className="nv-stat__label">Reviews</p>
                  </div>
                  <div className="nv-stat">
                    <p className="nv-stat__value">{data.quality.overall.approvals}</p>
                    <p className="nv-stat__label">Approved</p>
                  </div>
                  <div className="nv-stat">
                    <p className="nv-stat__value">
                      {data.quality.overall.average_score !== null
                        ? `${data.quality.overall.average_score}%`
                        : 'Not set'}
                    </p>
                    <p className="nv-stat__label">Average score</p>
                  </div>
                </div>
                <p className="nv-muted">
                  Gold checks: {data.quality.overall.gold_correct} of {data.quality.overall.gold_tasks}{' '}
                  correct.
                </p>
              </div>
            ) : (
              <EmptyState body="Quality appears after reviewed work." title="No review history" />
            )}
          </Panel>

          <Panel
            title="Delivered work"
            actions={<Badge tone="neutral">{data.work_history?.length ?? 0}</Badge>}
          >
            {data.work_history && data.work_history.length > 0 ? (
              <div className="nv-table-wrap">
                <table className="nv-table">
                  <thead>
                    <tr>
                      <th>Assignment</th>
                      <th>Project</th>
                      <th>Approved</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.work_history.map((row) => (
                      <tr key={row.submission_id}>
                        <td>{row.assignment}</td>
                        <td>{row.project.title}</td>
                        <td>{when(row.approved_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <EmptyState body="Approved client work appears here." title="No delivered work yet" />
            )}
          </Panel>

          <Panel title="Transcript">
            {data.transcript ? (
              <div className="nv-stack">
                <p>
                  {data.transcript.counts.learned} learned · {data.transcript.counts.proved} proved ·{' '}
                  {data.transcript.counts.delivered} delivered
                </p>
                <div>
                  <Link className="nv-button nv-button--ghost nv-button--sm" to="/transcript">
                    Open the full transcript
                    <ArrowRight aria-hidden="true" size={14} />
                  </Link>
                </div>
              </div>
            ) : (
              <EmptyState
                body="The transcript appears after your first recorded learning."
                title="Nothing recorded yet"
              />
            )}
          </Panel>
        </div>

        <div className="nv-stack">
          <Panel title="Share a link" actions={<Share2 aria-hidden="true" size={16} />}>
            <p className="nv-muted">
              A link is the only way a company sees this profile. It expires automatically, and you can revoke
              it early; the token is shown once and never again.
            </p>
            <Field
              label="What is this link for?"
              maxLength={120}
              placeholder="e.g. Client interview, October"
              value={label}
              onChange={(event) => setLabel(event.target.value)}
            />
            <Field
              label="Days until it expires"
              max={90}
              min={1}
              type="number"
              value={ttlDays}
              onChange={(event) => setTtlDays(event.target.value)}
            />
            <fieldset className="nv-field">
              <legend className="nv-label">What it includes</legend>
              {Object.entries(SCOPE_COPY).map(([scope, copy]) => (
                <Checkbox
                  checked={scopes.includes(scope)}
                  key={scope}
                  label={copy}
                  onChange={(event) =>
                    setScopes((current) =>
                      event.target.checked ? [...current, scope] : current.filter((value) => value !== scope),
                    )
                  }
                />
              ))}
            </fieldset>
            {error ? (
              <Banner tone="danger">
                <p>{error}</p>
              </Banner>
            ) : null}
            <Button disabled={busy || scopes.length === 0} type="button" onClick={() => void createShare()}>
              <Link2 aria-hidden="true" size={15} />
              {busy ? 'Creating…' : 'Create link'}
            </Button>

            {created ? (
              <Banner tone="success">
                <p>
                  <strong>Copy this link now.</strong> It cannot be shown again.
                </p>
                <p className="nv-code">
                  <code>{`${window.location.origin}/share/${created.token}`}</code>
                </p>
                <p className="nv-meta">Expires {when(created.expires_at)}.</p>
              </Banner>
            ) : null}
          </Panel>

          <Panel title="Your links" actions={<Badge tone="neutral">{shareRows.length}</Badge>}>
            {shares.resource.status === 'loading' ? <Skeleton lines={3} /> : null}
            {shares.resource.status === 'error' ? (
              <ErrorState
                body={shares.resource.message}
                action={
                  <Button size="sm" type="button" variant="secondary" onClick={shares.reload}>
                    Try again
                  </Button>
                }
              />
            ) : null}
            {shares.resource.status === 'ready' ? (
              shareRows.length === 0 ? (
                <EmptyState body="Create a scoped link when you are ready to share." title="No link yet" />
              ) : (
                <ul className="nv-list">
                  {shareRows.map((share) => (
                    <li key={share.id}>
                      <div className="nv-row nv-row--between">
                        <div style={{ minWidth: 0 }}>
                          <p className="nv-h4">{share.label ?? `Link #${share.id}`}</p>
                          <p className="nv-meta">
                            {share.scopes.join(', ')} · expires {when(share.expires_at)}
                          </p>
                        </div>
                        {share.active ? (
                          <Button
                            size="sm"
                            type="button"
                            variant="ghost"
                            onClick={() => setPendingShareId(share.id)}
                          >
                            Revoke
                          </Button>
                        ) : (
                          <Badge tone="neutral">{share.revoked_at ? 'Revoked' : 'Expired'}</Badge>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              )
            ) : null}
          </Panel>

          <Panel title="Working with Nelavista">
            <p className="nv-muted">
              Curriculum owner:{' '}
              {config.resource.status === 'ready' ? config.resource.data.curriculum_owner : 'Not set'} ·{' '}
              {config.resource.status === 'ready' ? config.resource.data.curriculum_license : 'Not set'}
            </p>
            <p className="nv-muted">
              Paid work starts at{' '}
              {config.resource.status === 'ready' ? config.resource.data.min_student_age : 16}; under{' '}
              {config.resource.status === 'ready' ? config.resource.data.guardian_consent_below_age : 18}{' '}
              needs guardian consent. Terms version{' '}
              {config.resource.status === 'ready'
                ? config.resource.data.contributor_terms_version
                : 'Not set'}
              .
            </p>
          </Panel>
        </div>
      </div>

      <ConfirmDialog
        body={
          <p>
            The company that holds this link will lose access immediately. You can create another link, but
            this one cannot be restored.
          </p>
        }
        busy={busy}
        confirmLabel="Revoke link"
        onCancel={() => setPendingShareId(null)}
        tone="danger"
        onConfirm={() => {
          if (pendingShareId !== null) {
            void revoke(pendingShareId).finally(() => setPendingShareId(null));
          }
        }}
        open={pendingShareId !== null}
        title="Revoke this share link?"
      />
    </div>
  );
}
