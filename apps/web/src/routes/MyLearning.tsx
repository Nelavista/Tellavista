/**
 * My learning (B6): every path the student has actually touched.
 *
 * The API returns only paths with real `LessonProgress` rows, so an empty page
 * means "you have not started anything", not "we could not find your work". Each
 * path shows its own progress and its own next step - this page never guesses
 * what the student should do.
 */
import type { MyLearningOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { BookOpen, Play } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';

export function MyLearning(): JSX.Element {
  const { resource, reload } = useApiResource<MyLearningOut>('/skills/my-learning');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your learning">
        <Skeleton height="2rem" width="45%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Skills" title="My learning" />
        <Banner tone="info">
          <p>The skills journey is not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Skills" title="My learning" />
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const paths = resource.data.paths;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Skills"
        title="My learning"
        description="Only paths you have opened appear here. Progress is saved per step, not per visit."
        actions={
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/skills">
            Browse skills
          </Link>
        }
      />

      <Panel
        title="In progress"
        actions={
          <Badge tone="neutral">
            {paths.length} path{paths.length === 1 ? '' : 's'}
          </Badge>
        }
      >
        {paths.length === 0 ? (
          <EmptyState
            body="Pick a skill and open its first lesson. Progress appears here as soon as you start."
            icon={BookOpen}
            image={EMPTY_IMAGES.learning}
            title="Nothing started yet"
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {paths.map((path) => (
              <li key={path.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <h2 className="nv-h3">
                      <Link to={`/skills/paths/${path.slug}`}>{path.title}</Link>
                    </h2>
                    <p className="nv-muted">
                      {path.completed_steps} of {path.required_steps} steps done
                    </p>
                  </div>
                  <Badge tone={path.percent_complete === 100 ? 'success' : 'info'}>
                    {path.percent_complete}%
                  </Badge>
                </div>
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
                {path.next_step ? (
                  <div className="nv-row nv-row--between" style={{ marginTop: 'var(--nv-space-sm)' }}>
                    <p className="nv-muted">Next: {path.next_step.title ?? path.next_step.kind}</p>
                    {path.next_step.kind === 'lesson' && path.next_step.lesson_slug ? (
                      <Link
                        className="nv-button nv-button--ghost nv-button--sm"
                        to={`/skills/lessons/${path.next_step.lesson_slug}`}
                      >
                        <Play aria-hidden="true" size={14} />
                        Continue
                      </Link>
                    ) : null}
                  </div>
                ) : (
                  <p className="nv-muted">
                    Every step is done. Verification comes from an assessment, not from these steps.
                  </p>
                )}
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}
