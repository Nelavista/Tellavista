/**
 * The graded sitting, after submission (B7).
 *
 * This is the only screen allowed to show expected answers: the route refuses to
 * serve them before the attempt is submitted. Every task is shown with the input,
 * what the student answered, what was expected and the validator's feedback, so a
 * retry is a learning step rather than a guess.
 */
import type { AttemptReviewOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowRight, CheckCircle2, ClipboardList, XCircle } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { formatAnswer, formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';

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
        <PageHeader eyebrow="Verification" title="Attempt" />
        <Banner tone="info">
          <p>Verification is not switched on for this environment yet.</p>
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
        <PageHeader eyebrow="Verification" title="Attempt" />
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
        <p className="nv-muted">
          <Link to="/verification">Back to verification</Link>
        </p>
      </div>
    );
  }

  const review = resource.data;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Verification"
        title="Your answers"
        description={`Score: ${review.score ?? 0}%${
          review.submitted_at ? ` · submitted ${formatDateTime(review.submitted_at)}` : ''
        }`}
        actions={
          <Badge status={review.passed ? 'verified' : 'at_risk'} tone={review.passed ? 'success' : 'warning'}>
            {review.passed ? 'Passed' : 'Not passed'}
          </Badge>
        }
      />

      <p className="nv-muted">
        <Link to="/verification">Verification</Link>
      </p>

      <Panel
        title="Tasks"
        actions={
          <Badge tone="neutral">
            {review.tasks.length} task{review.tasks.length === 1 ? '' : 's'}
          </Badge>
        }
      >
        {review.tasks.length === 0 ? (
          <EmptyState
            body="This attempt has no recorded tasks. If that looks wrong, contact support."
            icon={ClipboardList}
            title="Nothing to review"
          />
        ) : (
          <ol className="nv-list nv-list--ruled">
            {review.tasks.map((task) => (
              <li key={task.task_id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <h2 className="nv-h3">Task {task.ordinal}</h2>
                  <Badge
                    status={task.correct ? 'verified' : 'at_risk'}
                    tone={task.correct ? 'success' : 'danger'}
                  >
                    {task.correct ? (
                      <>
                        <CheckCircle2 aria-hidden="true" size={13} /> Correct
                      </>
                    ) : (
                      <>
                        <XCircle aria-hidden="true" size={13} /> Incorrect
                      </>
                    )}
                  </Badge>
                </div>

                {Object.entries(task.payload ?? {})
                  .filter(([, value]) => typeof value === 'string' || typeof value === 'number')
                  .map(([key, value]) => (
                    <p key={key}>
                      <span className="nv-muted">{key.replace(/_/g, ' ')}: </span>
                      {String(value)}
                    </p>
                  ))}

                <div className="nv-stack" style={{ gap: 'var(--nv-space-xs)' }}>
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
                </div>
              </li>
            ))}
          </ol>
        )}
      </Panel>

      <div className="nv-row">
        <Link className="nv-button" to="/verification">
          Sit an assessment
          <ArrowRight aria-hidden="true" size={15} />
        </Link>
        <Link to="/transcript">See your transcript</Link>
      </div>
    </div>
  );
}
