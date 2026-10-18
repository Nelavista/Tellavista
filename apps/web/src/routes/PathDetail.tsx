/**
 * A learning path (B6): the steps in order, with the student's real state on each.
 *
 * The API decides what is unlocked (`unlocked` is computed from the steps before
 * it), so this page never re-derives path order and cannot disagree with the
 * server about what is next. A locked step is shown, not hidden: the student
 * should see what is coming, just not open it.
 *
 * Project and assessment steps have no destination in the app yet. They are
 * labelled as such instead of being rendered as a dead link.
 */
import type { PathOut, PathStepOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

const KIND_LABELS: Record<string, string> = {
  lesson: 'Lesson',
  practice: 'Practice',
  project: 'Project',
  assessment: 'Assessment',
};

function stepDestination(step: PathStepOut, from: string): JSX.Element {
  if (!step.unlocked) {
    return <span className="nv-muted">Locked — finish the step before it.</span>;
  }
  if (step.kind === 'lesson' && step.lesson_slug) {
    return (
      <Link to={`/skills/lessons/${step.lesson_slug}`} state={{ from }}>
        Open lesson
      </Link>
    );
  }
  if (step.kind === 'practice' && step.task_template_id) {
    return (
      <Link to={`/skills/practice/${step.task_template_id}`} state={{ from }}>
        Practise
      </Link>
    );
  }
  return <span className="nv-muted">Not available in the app yet.</span>;
}

export function PathDetail(): JSX.Element {
  const { pathSlug = '' } = useParams<{ pathSlug: string }>();
  const from = `/skills/paths/${pathSlug}`;
  const { resource, reload } = useApiResource<PathOut>(`/skills/paths/${pathSlug}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this path">
        <Skeleton height="2rem" width="60%" />
        <Skeleton lines={2} />
        <Skeleton lines={5} />
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Learning path</h1>
        {resource.status === 'off' ? (
          <p className="nv-banner">The skills journey is not switched on for this environment yet.</p>
        ) : (
          <>
            <ErrorNote message={resource.message} />
            <button className="nv-button" type="button" onClick={reload}>
              Try again
            </button>
          </>
        )}
        <p className="nv-muted">
          <Link to="/skills">All skills</Link>
        </p>
      </div>
    );
  }

  const path = resource.data;
  const next = path.next_step;

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to="/skills">All skills</Link>
      </p>

      <h1 className="nv-h1">{path.title}</h1>
      <p className="nv-muted">
        {path.level}
        {path.estimated_hours ? ` · about ${path.estimated_hours} hour(s)` : ''} · {path.completed_steps} of{' '}
        {path.required_steps} steps done
      </p>
      {path.summary ? <p>{path.summary}</p> : null}

      <div
        className="nv-meter"
        role="progressbar"
        aria-valuenow={path.percent_complete}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <span className="nv-meter__fill" style={{ width: `${path.percent_complete}%` }} />
      </div>

      {next ? (
        <section className="nv-action" aria-labelledby="nv-next-step">
          <p className="nv-label" id="nv-next-step">
            Next step
          </p>
          <p className="nv-action__label">{next.title ?? KIND_LABELS[next.kind] ?? next.kind}</p>
          {stepDestination(next, from)}
        </section>
      ) : (
        <p className="nv-banner">
          Every step in this path is done. Completing a path is progress — verification comes from an
          assessment, not from finishing lessons.
        </p>
      )}

      <ol className="nv-list">
        {path.steps.map((step) => (
          <li className="nv-step" data-done={step.completed} key={step.id}>
            <div className="nv-row nv-row--between">
              <strong>
                {step.ordinal}. {step.title ?? KIND_LABELS[step.kind] ?? step.kind}
              </strong>
              <span className="nv-muted">
                {KIND_LABELS[step.kind] ?? step.kind}
                {step.completed ? ' · done' : ''}
              </span>
            </div>
            {step.estimated_minutes ? <p className="nv-muted">{step.estimated_minutes} min</p> : null}
            <p>{stepDestination(step, from)}</p>
          </li>
        ))}
      </ol>
    </div>
  );
}
