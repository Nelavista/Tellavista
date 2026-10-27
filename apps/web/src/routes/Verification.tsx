/**
 * Verification hub (B7).
 *
 * Two things live here and they answer different questions:
 *
 * * the badge list says what is proved *now* for each skill, in the student's
 *   words — a finished lesson never appears as proof;
 * * the assessment list is the only route to a badge, so every unproved skill
 *   points at a real sitting rather than at more reading.
 *
 * The transcript is linked from here because "what have I proved?" and "show me
 * the evidence" should not be two different products.
 */
import type { AssessmentListOut, PracticalTaskListOut, VerificationOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowRight, BadgeCheck, ClipboardCheck, FileCheck2 } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';

const STATUS_COPY: Record<string, { label: string; note: string }> = {
  verified: {
    label: 'Verified',
    note: 'You passed an assessment for this skill. The transcript holds the evidence.',
  },
  in_progress: {
    label: 'In progress',
    note: 'A sitting is open. Finish it to be graded — an unfinished attempt is not proof.',
  },
  at_risk: {
    label: 'At risk',
    note: 'Recent work quality lowered this badge. Passing a new assessment restores it.',
  },
  suspended: {
    label: 'Suspended',
    note: 'This badge is suspended. Starting a new assessment is the way back.',
  },
  unverified: {
    label: 'Not proved yet',
    note: 'Lessons and practice are progress, not proof. Pass an assessment to prove this skill.',
  },
};

function statusCopy(status: string): { label: string; note: string } {
  return (
    STATUS_COPY[status] ?? {
      label: status.replace(/_/g, ' '),
      note: 'The API reported a state this screen does not know yet.',
    }
  );
}

function statusTone(status: string): 'neutral' | 'success' | 'info' | 'warning' | 'danger' {
  if (status === 'verified') return 'success';
  if (status === 'in_progress') return 'info';
  if (status === 'at_risk') return 'warning';
  if (status === 'suspended') return 'danger';
  return 'neutral';
}

export function Verification(): JSX.Element {
  const badges = useApiResource<VerificationOut>('/verification');
  const catalog = useApiResource<AssessmentListOut>('/verification/assessments');
  const practical = useApiResource<PracticalTaskListOut>('/verification/practical');

  if (
    badges.resource.status === 'loading' ||
    catalog.resource.status === 'loading' ||
    practical.resource.status === 'loading'
  ) {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your verification">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (badges.resource.status === 'off' || catalog.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="Verification" />
        <Banner tone="info">
          <p>
            Verification is not switched on for this environment yet. Your account, courses and learning are
            unaffected.
          </p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (badges.resource.status !== 'ready' || catalog.resource.status !== 'ready') {
    const failed = badges.resource.status !== 'ready' ? badges.resource : catalog.resource;
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="Verification" />
        <ErrorState
          body={'message' in failed ? failed.message : undefined}
          action={
            <Button
              size="sm"
              type="button"
              variant="secondary"
              onClick={() => {
                badges.reload();
                catalog.reload();
              }}
            >
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const skills = badges.resource.data.skills;
  const assessments = catalog.resource.data.assessments;
  const practicalTasks = practical.resource.status === 'ready' ? practical.resource.data.tasks : [];

  // The way back from a suspension is a new assessment, so the prompt links
  // straight at the sitting for that skill rather than at the hub again.
  function reverifyLink(skillId: number): string | null {
    const assessment = assessments.find((row) => row.skill_id === skillId);
    return assessment ? `/verification/assessments/${assessment.slug}` : null;
  }

  // A lowered badge is a prompt, not a quiet label change: say what happened,
  // when, and the one action that restores it. Nothing else is restricted.
  const lowered = skills.filter((skill) => skill.status === 'suspended' || skill.status === 'at_risk');

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Prove"
        title="Verification"
        description="Proof comes from passing an assessment with known answers. Watching a lesson or pressing complete is never verification."
        actions={
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/transcript">
            <FileCheck2 aria-hidden="true" size={15} />
            Skill transcript
          </Link>
        }
      />

      {lowered.length > 0 ? (
        <Banner tone="warning">
          <h2 className="nv-h3">
            {lowered.some((skill) => skill.status === 'suspended')
              ? 'Re-verification needed'
              : 'Your badge is at risk'}
          </h2>
          <p>
            Recent work quality lowered {lowered.length === 1 ? 'one badge' : `${lowered.length} badges`}.
            Your courses, learning and earnings are unaffected — passing the assessment again restores the
            badge.
          </p>
          <ul className="nv-list">
            {lowered.map((skill) => {
              const link = reverifyLink(skill.skill_id);
              return (
                <li key={skill.skill_id}>
                  <strong>{skill.skill}</strong> — {statusCopy(skill.status).label}
                  {skill.status_reason ? <span className="nv-muted"> · {skill.status_reason}</span> : null}
                  {skill.status_changed_at ? (
                    <span className="nv-muted"> · {formatDateTime(skill.status_changed_at)}</span>
                  ) : null}
                  {link ? (
                    <div className="nv-row">
                      <Link className="nv-button nv-button--secondary nv-button--sm" to={link}>
                        Re-verify {skill.skill}
                      </Link>
                    </div>
                  ) : (
                    <p className="nv-muted">
                      No assessment is published for this skill yet, so there is nothing to sit today.
                    </p>
                  )}
                </li>
              );
            })}
          </ul>
        </Banner>
      ) : null}

      <Panel title="Your badges" actions={<Badge tone="info">{skills.length}</Badge>}>
        {skills.length === 0 ? (
          <EmptyState
            body="Start an assessment below — the first sitting also opens the badge."
            icon={BadgeCheck}
            title="No skill has a badge yet"
            action={
              assessments.length > 0 ? (
                <Link
                  className="nv-button nv-button--secondary nv-button--sm"
                  to={`/verification/assessments/${assessments[0]?.slug ?? ''}`}
                >
                  Start the first assessment
                </Link>
              ) : undefined
            }
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Status</th>
                  <th>What it means</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {skills.map((skill) => {
                  const copy = statusCopy(skill.status);
                  const link = reverifyLink(skill.skill_id);
                  return (
                    <tr key={skill.skill_id}>
                      <td>
                        <Link to={`/skills/${skill.slug}`}>{skill.skill}</Link>
                      </td>
                      <td>
                        <Badge status={skill.status} tone={statusTone(skill.status)}>
                          {copy.label}
                        </Badge>
                      </td>
                      <td className="nv-muted">{copy.note}</td>
                      <td>
                        {!skill.verified && link ? (
                          <Link className="nv-button nv-button--ghost nv-button--sm" to={link}>
                            {skill.status === 'suspended' ? 'Re-verify' : 'Prove'}
                            <ArrowRight aria-hidden="true" size={14} />
                          </Link>
                        ) : null}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <Panel title="Assessments you can sit" actions={<Badge tone="neutral">{assessments.length}</Badge>}>
        {assessments.length === 0 ? (
          <EmptyState
            body="This is content, not an app update — it appears here as soon as one is published."
            icon={ClipboardCheck}
            title="No assessment is published yet"
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Assessment</th>
                  <th>Tasks</th>
                  <th>Pass mark</th>
                  <th>Attempts</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {assessments.map((assessment) => (
                  <tr key={assessment.id}>
                    <td>
                      <Link to={`/verification/assessments/${assessment.slug}`}>{assessment.title}</Link>
                    </td>
                    <td className="nv-num">{assessment.task_count}</td>
                    <td className="nv-num">{assessment.pass_threshold}%</td>
                    <td className="nv-num">{assessment.max_attempts}</td>
                    <td>
                      <Link
                        className="nv-button nv-button--ghost nv-button--sm"
                        to={`/verification/assessments/${assessment.slug}`}
                      >
                        Sit
                        <ArrowRight aria-hidden="true" size={14} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <Panel title="Practical tasks" actions={<Badge tone="neutral">{practicalTasks.length}</Badge>}>
        <p className="nv-muted">
          A practical task is real work judged against a published rubric. It is reviewed by a person, so it
          takes longer than an assessment and is not graded instantly.
        </p>
        {practicalTasks.length === 0 ? (
          <EmptyState
            body="No practical task is published yet for the skills you are learning."
            icon={ClipboardCheck}
            title="Nothing to sit yet"
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {practicalTasks.map((task) => (
              <li key={task.id}>
                <div className="nv-row nv-row--between">
                  <Link className="nv-h4" to={`/verification/practical/${task.slug}`}>
                    {task.title}
                  </Link>
                  <Link
                    className="nv-button nv-button--ghost nv-button--sm"
                    to={`/verification/practical/${task.slug}`}
                  >
                    Read the brief
                    <ArrowRight aria-hidden="true" size={14} />
                  </Link>
                </div>
                <p className="nv-muted">Reviewed against a rubric · read the brief before you start</p>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}
