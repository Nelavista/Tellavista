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
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

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
        <h1 className="nv-h1">Verification</h1>
        <p className="nv-banner">
          Verification is not switched on for this environment yet. Your account, courses and learning are
          unaffected.
        </p>
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
        <h1 className="nv-h1">Verification</h1>
        <ErrorNote message={'message' in failed ? failed.message : null} />
        <button
          className="nv-button"
          type="button"
          onClick={() => {
            badges.reload();
            catalog.reload();
          }}
        >
          Try again
        </button>
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

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Verification</h1>
      <p className="nv-muted">
        Proof comes from passing an assessment with known answers. Watching a lesson or pressing complete is
        never verification.
      </p>
      <p className="nv-muted">
        <Link to="/transcript">See your skill transcript</Link>
      </p>

      <section className="nv-stack">
        <h2 className="nv-h2">Your badges</h2>
        {skills.length === 0 ? (
          <p className="nv-banner">
            No skill has a badge yet. Start an assessment below — the first sitting also opens the badge.
          </p>
        ) : (
          <ul className="nv-list">
            {skills.map((skill) => {
              const copy = statusCopy(skill.status);
              return (
                <li className="nv-card" key={skill.skill_id}>
                  <div className="nv-row nv-row--between">
                    <h3 className="nv-h2">
                      <Link to={`/skills/${skill.slug}`}>{skill.skill}</Link>
                    </h3>
                    <span className="nv-badge" data-status={skill.status}>
                      {copy.label}
                    </span>
                  </div>
                  <p className="nv-muted">{copy.note}</p>
                  {!skill.verified && reverifyLink(skill.skill_id) ? (
                    <p>
                      <Link className="nv-button" to={reverifyLink(skill.skill_id) ?? '/verification'}>
                        {skill.status === 'suspended' ? 'Re-verify this skill' : 'Prove this skill'}
                      </Link>
                    </p>
                  ) : null}
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <section className="nv-stack">
        <h2 className="nv-h2">Assessments you can sit</h2>
        {assessments.length === 0 ? (
          <p className="nv-banner">
            No assessment is published yet. This is content, not an app update — it appears here as soon as
            one is published.
          </p>
        ) : (
          <ul className="nv-list">
            {assessments.map((assessment) => (
              <li className="nv-card" key={assessment.id}>
                <h3 className="nv-h2">
                  <Link to={`/verification/assessments/${assessment.slug}`}>{assessment.title}</Link>
                </h3>
                <p className="nv-muted">
                  {assessment.task_count} task{assessment.task_count === 1 ? '' : 's'} · pass at{' '}
                  {assessment.pass_threshold}% · {assessment.max_attempts} attempt
                  {assessment.max_attempts === 1 ? '' : 's'}
                </p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="nv-stack">
        <h2 className="nv-h2">Practical tasks</h2>
        <p className="nv-muted">
          A practical task is real work judged against a published rubric. It is reviewed by a person, so
          it takes longer than an assessment and is not graded instantly.
        </p>
        {practicalTasks.length === 0 ? (
          <p className="nv-banner">No practical task is published yet for the skills you are learning.</p>
        ) : (
          <ul className="nv-list">
            {practicalTasks.map((task) => (
              <li className="nv-card" key={task.id}>
                <h3 className="nv-h2">
                  <Link to={`/verification/practical/${task.slug}`}>{task.title}</Link>
                </h3>
                <p className="nv-muted">Reviewed against a rubric · read the brief before you start</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
