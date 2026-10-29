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
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowRight, Lock, Route } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';

const KIND_LABELS: Record<string, string> = {
  lesson: 'Lesson',
  practice: 'Practice',
  project: 'Project',
  assessment: 'Assessment',
};

function stepDestination(step: PathStepOut, from: string): JSX.Element {
  if (!step.unlocked) {
    return (
      <span className="nv-muted">
        <Lock aria-hidden="true" size={13} /> Locked: finish the step before it.
      </span>
    );
  }
  if (step.kind === 'lesson' && step.lesson_slug) {
    return (
      <Link
        className="nv-button nv-button--secondary nv-button--sm"
        state={{ from }}
        to={`/skills/lessons/${step.lesson_slug}`}
      >
        Open lesson
        <ArrowRight aria-hidden="true" size={14} />
      </Link>
    );
  }
  if (step.kind === 'practice' && step.task_template_id) {
    return (
      <Link
        className="nv-button nv-button--secondary nv-button--sm"
        state={{ from }}
        to={`/skills/practice/${step.task_template_id}`}
      >
        Practise
        <ArrowRight aria-hidden="true" size={14} />
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
        <PageHeader eyebrow="Skills" title="Learning path" />
        {resource.status === 'off' ? (
          <Banner tone="info">
            <p>The skills journey is not switched on for this environment yet.</p>
          </Banner>
        ) : (
          <ErrorState
            body={resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={reload}>
                Try again
              </Button>
            }
          />
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
      <PageHeader
        eyebrow="Learning path"
        title={path.title}
        description={`${path.level}${
          path.estimated_hours ? ` · about ${path.estimated_hours} hour(s)` : ''
        } · ${path.completed_steps} of ${path.required_steps} steps done`}
        actions={
          <Badge tone={path.percent_complete === 100 ? 'success' : 'info'}>{path.percent_complete}%</Badge>
        }
      />

      <p className="nv-muted">
        <Link to="/skills">All skills</Link>
      </p>

      {path.summary ? <p>{path.summary}</p> : null}

      <div
        className="nv-meter"
        role="progressbar"
        aria-label={`${path.title} progress`}
        aria-valuenow={path.percent_complete}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <span className="nv-meter__fill" style={{ width: `${path.percent_complete}%` }} />
      </div>

      {next ? (
        <Panel title="Next step">
          <p className="nv-h3">{next.title ?? KIND_LABELS[next.kind] ?? next.kind}</p>
          {stepDestination(next, from)}
        </Panel>
      ) : (
        <Banner tone="success">
          <p>
            Every step in this path is done. Completing a path is progress. Verification comes from an
            assessment, not from finishing lessons.
          </p>
        </Banner>
      )}

      <Panel title="Steps" actions={<Badge tone="neutral">{path.steps.length} total</Badge>}>
        {path.steps.length === 0 ? (
          <EmptyState
            body="This path has no steps yet. It will appear here when the author publishes them."
            icon={Route}
            title="No steps published"
          />
        ) : (
          <ol className="nv-list nv-list--ruled">
            {path.steps.map((step) => (
              <li key={step.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <p className="nv-h4">
                      {step.ordinal}. {step.title ?? KIND_LABELS[step.kind] ?? step.kind}
                    </p>
                    <p className="nv-muted">
                      {KIND_LABELS[step.kind] ?? step.kind}
                      {step.estimated_minutes ? ` · ${step.estimated_minutes} min` : ''}
                    </p>
                  </div>
                  <Badge
                    status={step.completed ? 'completed' : step.unlocked ? 'open' : 'locked'}
                    tone={step.completed ? 'success' : step.unlocked ? 'info' : 'neutral'}
                  >
                    {step.completed ? 'Done' : step.unlocked ? 'Open' : 'Locked'}
                  </Badge>
                </div>
                <p>{stepDestination(step, from)}</p>
              </li>
            ))}
          </ol>
        )}
      </Panel>
    </div>
  );
}
