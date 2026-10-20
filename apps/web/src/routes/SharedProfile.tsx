/**
 * A shared talent profile (B13).
 *
 * Public by design: the token in the URL is the grant, and it is scoped,
 * expiring and revocable. The page therefore receives only the sections the
 * student granted, and never the account's email or the internal skill list.
 */
import type { TalentProfileOut } from '@nelavista/api-client';
import * as React from 'react';
import { useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

function when(value: string | null | undefined): string {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : date.toLocaleDateString();
}

export function SharedProfile(): JSX.Element {
  const { token = '' } = useParams();
  const { resource, reload } = useApiResource<TalentProfileOut>(`/talent/share/${token}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading shared profile">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-card nv-card--narrow">
        <h1 className="nv-h1">This link is not active</h1>
        <p className="nv-muted">
          It may have expired or been revoked by the student. Ask them for a new link.
        </p>
        {resource.status === 'off' ? null : <ErrorNote message={resource.message} />}
        {resource.status === 'error' ? (
          <button className="nv-button" type="button" onClick={reload}>
            Try again
          </button>
        ) : null}
      </div>
    );
  }

  const data = resource.data;

  return (
    <div className="nv-stack">
      <p className="nv-muted">Shared evidence profile</p>
      <h1 className="nv-h1">{data.display_name ?? 'A Nelavista student'}</h1>
      <p className="nv-muted">
        Everything below is generated from verified work. Nothing on this page is self-reported.
      </p>

      <section className="nv-card">
        <h2 className="nv-h2">Verified skills</h2>
        {data.verified_skills.length === 0 ? (
          <p className="nv-muted">No verified skill is shared.</p>
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
          <h2 className="nv-h2">Quality history</h2>
          <p>
            {data.quality.overall.reviews_count} review
            {data.quality.overall.reviews_count === 1 ? '' : 's'} · {data.quality.overall.approvals} approved
            {data.quality.overall.average_score !== null ? ` · ${data.quality.overall.average_score}% average` : ''}
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

      {data.availability ? (
        <section className="nv-card">
          <h2 className="nv-h2">Availability</h2>
          <p>
            {data.availability.hours_per_week !== null
              ? `${data.availability.hours_per_week} hours per week`
              : 'Hours not stated'}
            {data.availability.available_from ? ` · from ${data.availability.available_from}` : ''}
          </p>
          {data.availability.languages.length > 0 ? (
            <p className="nv-muted">
              {data.availability.languages.map((language) => `${language.language} (${language.level})`).join(' · ')}
            </p>
          ) : null}
        </section>
      ) : null}

      <p className="nv-muted">
        This page shows only the sections the student chose to share. The link expires and can be revoked.
      </p>
    </div>
  );
}
