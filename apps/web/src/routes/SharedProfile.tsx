/**
 * A shared talent profile (B13).
 *
 * Public by design: the token in the URL is the grant, and it is scoped,
 * expiring and revocable. The page therefore receives only the sections the
 * student granted, and never the account's email or the internal skill list.
 */
import type { TalentProfileOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { BadgeCheck, Briefcase, CalendarClock, GraduationCap, Link2Off } from 'lucide-react';
import * as React from 'react';
import { useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';

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
      <div className="nv-stack" style={{ maxWidth: '42rem', margin: '0 auto' }}>
        <PageHeader eyebrow="Shared profile" title="This link is not active" />
        <Banner tone="warning">
          <p>It may have expired or been revoked by the student. Ask them for a new link.</p>
        </Banner>
        {resource.status === 'error' ? (
          <>
            <ErrorState body={resource.message} />
            <div>
              <Button size="sm" type="button" variant="secondary" onClick={reload}>
                Try again
              </Button>
            </div>
          </>
        ) : (
          <EmptyState
            body="A shared profile is only visible while its link is active."
            icon={Link2Off}
            title="Nothing to show"
          />
        )}
      </div>
    );
  }

  const data = resource.data;

  return (
    <div className="nv-stack" style={{ maxWidth: '56rem', margin: '0 auto' }}>
      <PageHeader
        eyebrow="Shared evidence profile"
        title={data.display_name ?? 'A Nelavista student'}
        description="Everything below is generated from verified work. Nothing on this page is self-reported."
        actions={<Badge tone="success">Verified record</Badge>}
      />

      <Panel title="Verified skills" actions={<BadgeCheck aria-hidden="true" size={16} />}>
        {data.verified_skills.length === 0 ? (
          <EmptyState
            body="No verified skill is shared on this link."
            icon={BadgeCheck}
            title="No skills shared"
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {data.verified_skills.map((skill) => (
              <li key={skill.skill_id}>
                <div className="nv-row nv-row--between">
                  <span>{skill.skill ?? `Skill #${skill.skill_id}`}</span>
                  <Badge
                    status={skill.at_risk ? 'at_risk' : 'verified'}
                    tone={skill.at_risk ? 'warning' : 'success'}
                  >
                    {skill.at_risk ? 'At risk' : 'Verified'}
                  </Badge>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Panel>

      {data.academic ? (
        <Panel title="Academic" actions={<GraduationCap aria-hidden="true" size={16} />}>
          <p>
            {data.academic.university ?? 'University not set'} ·{' '}
            {data.academic.department ?? 'Department not set'}
            {data.academic.level ? ` · Level ${data.academic.level}` : ''}
          </p>
        </Panel>
      ) : null}

      {data.quality?.overall ? (
        <Panel title="Quality history">
          <div className="nv-row nv-row--between">
            <p>
              {data.quality.overall.reviews_count} review
              {data.quality.overall.reviews_count === 1 ? '' : 's'} · {data.quality.overall.approvals}{' '}
              approved
              {data.quality.overall.average_score !== null
                ? ` · ${data.quality.overall.average_score}% average`
                : ''}
            </p>
            <Badge tone="info">From reviewed work</Badge>
          </div>
        </Panel>
      ) : null}

      {data.work_history && data.work_history.length > 0 ? (
        <Panel title="Delivered work" actions={<Briefcase aria-hidden="true" size={16} />}>
          <ul className="nv-list nv-list--ruled">
            {data.work_history.map((row) => (
              <li key={row.submission_id}>
                <strong>{row.assignment}</strong>
                <span className="nv-muted">
                  {' '}
                  · {row.project.title} · approved {when(row.approved_at)}
                </span>
              </li>
            ))}
          </ul>
        </Panel>
      ) : null}

      {data.availability ? (
        <Panel title="Availability" actions={<CalendarClock aria-hidden="true" size={16} />}>
          <p>
            {data.availability.hours_per_week !== null
              ? `${data.availability.hours_per_week} hours per week`
              : 'Hours not stated'}
            {data.availability.available_from ? ` · from ${data.availability.available_from}` : ''}
          </p>
          {data.availability.languages.length > 0 ? (
            <p className="nv-muted">
              {data.availability.languages
                .map((language) => `${language.language} (${language.level})`)
                .join(' · ')}
            </p>
          ) : null}
        </Panel>
      ) : null}

      <p className="nv-muted">
        This page shows only the sections the student chose to share. The link expires and can be revoked.
      </p>
    </div>
  );
}
