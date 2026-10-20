/**
 * My learning (B6): every path the student has actually touched.
 *
 * The API returns only paths with real `LessonProgress` rows, so an empty page
 * means "you have not started anything", not "we could not find your work". Each
 * path shows its own progress and its own next step — this page never guesses
 * what the student should do.
 */
import type { MyLearningOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

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
        <h1 className="nv-h1">My learning</h1>
        <p className="nv-banner">The skills journey is not switched on for this environment yet.</p>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">My learning</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
      </div>
    );
  }

  const paths = resource.data.paths;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">My learning</h1>

      {paths.length === 0 ? (
        <p className="nv-banner">
          You have not started a path yet. Pick a skill and open its first lesson — progress appears here.
        </p>
      ) : (
        <ul className="nv-list">
          {paths.map((path) => (
            <li className="nv-card" key={path.id}>
              <h2 className="nv-h2">
                <Link to={`/skills/paths/${path.slug}`}>{path.title}</Link>
              </h2>
              <p className="nv-muted">
                {path.completed_steps} of {path.required_steps} steps done
              </p>
              <div
                className="nv-meter"
                role="progressbar"
                aria-valuenow={path.percent_complete}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <span className="nv-meter__fill" style={{ width: `${path.percent_complete}%` }} />
              </div>
              {path.next_step ? (
                <p className="nv-muted">
                  Next: {path.next_step.title ?? path.next_step.kind}
                  {path.next_step.kind === 'lesson' && path.next_step.lesson_slug ? (
                    <>
                      {' · '}
                      <Link to={`/skills/lessons/${path.next_step.lesson_slug}`}>Continue</Link>
                    </>
                  ) : null}
                </p>
              ) : (
                <p className="nv-muted">
                  Every step is done. Verification comes from an assessment, not from these steps.
                </p>
              )}
            </li>
          ))}
        </ul>
      )}

      <p className="nv-muted">
        <Link to="/skills">Browse skills</Link>
      </p>
    </div>
  );
}
