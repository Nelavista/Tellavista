/**
 * The graded sitting, after submission (B7).
 *
 * This is the only screen allowed to show expected answers: the route refuses to
 * serve them before the attempt is submitted. Every task is shown with the input,
 * what the student answered, what was expected and the validator's feedback, so a
 * retry is a learning step rather than a guess.
 */
import type { AttemptReviewOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { formatAnswer, formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

export function AttemptReview(): JSX.Element {
  const { attemptId = '' } = useParams<{ attemptId: string }>();
  const { resource, reload } = useApiResource<AttemptReviewOut>(`/verification/attempts/${attemptId}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this attempt">
        <Skeleton height="2rem" width="45%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Attempt</h1>
        <p className="nv-banner">Verification is not switched on for this environment yet.</p>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Attempt</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
        <p className="nv-muted">
          <Link to="/verification">Back to verification</Link>
        </p>
      </div>
    );
  }

  const review = resource.data;

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to="/verification">Verification</Link>
      </p>
      <h1 className="nv-h1">Your answers</h1>
      <p>
        Score: {review.score ?? 0}% ·{' '}
        <span className="nv-badge" data-status={review.passed ? 'verified' : 'at_risk'}>
          {review.passed ? 'Passed' : 'Not passed'}
        </span>
        {review.submitted_at ? (
          <span className="nv-muted"> · submitted {formatDateTime(review.submitted_at)}</span>
        ) : null}
      </p>

      <ol className="nv-list">
        {review.tasks.map((task) => (
          <li className="nv-card" key={task.task_id}>
            <h2 className="nv-h2">
              Task {task.ordinal}{' '}
              <span className="nv-badge" data-status={task.correct ? 'verified' : 'at_risk'}>
                {task.correct ? 'Correct' : 'Incorrect'}
              </span>
            </h2>
            {Object.entries(task.payload ?? {})
              .filter(([, value]) => typeof value === 'string' || typeof value === 'number')
              .map(([key, value]) => (
                <p key={key}>
                  <span className="nv-muted">{key.replace(/_/g, ' ')}: </span>
                  {String(value)}
                </p>
              ))}
            <p>
              <span className="nv-muted">Your answer: </span>
              {formatAnswer(task.answer)}
            </p>
            {!task.correct ? (
              <p>
                <span className="nv-muted">Expected: </span>
                {formatAnswer(task.expected_answer)}
              </p>
            ) : null}
            {task.feedback ? <p className="nv-muted">{task.feedback}</p> : null}
          </li>
        ))}
      </ol>

      <div className="nv-row">
        <Link className="nv-button" to="/verification">
          Sit an assessment
        </Link>
        <Link to="/transcript">See your transcript</Link>
      </div>
    </div>
  );
}
