/**
 * Work (B9).
 *
 * Three lists answer three different questions, in the order a student asks
 * them: what do I have to do, what did I already send, and why is my quality
 * where it is? The quality record shows the counts that produced it, because a
 * score with no explanation is not actionable.
 */
import type {
  AssignmentListOut,
  QualityOut,
  SubmissionListOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

const STATUS_COPY: Record<string, string> = {
  assigned: 'Ready to start',
  in_progress: 'In progress',
  submitted: 'Waiting for review',
  approved: 'Approved',
  rework: 'Rework needed',
  rejected: 'Not accepted',
};

export function Work(): JSX.Element {
  const assignments = useApiResource<AssignmentListOut>('/work/assignments');
  const submissions = useApiResource<SubmissionListOut>('/work/submissions');
  const quality = useApiResource<QualityOut>('/work/quality');

  if (
    assignments.resource.status === 'loading' ||
    submissions.resource.status === 'loading' ||
    quality.resource.status === 'loading'
  ) {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your work">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
        <Skeleton lines={2} />
      </div>
    );
  }

  if (assignments.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Work</h1>
        <p className="nv-banner">
          Work is not switched on for this environment yet. Your learning and proof are unaffected.
        </p>
      </div>
    );
  }

  if (
    assignments.resource.status !== 'ready' ||
    submissions.resource.status !== 'ready' ||
    quality.resource.status !== 'ready'
  ) {
    const failed = [assignments.resource, submissions.resource, quality.resource].find(
      (resource) => resource.status !== 'ready',
    );
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Work</h1>
        <ErrorNote message={failed && 'message' in failed ? failed.message : null} />
        <button
          className="nv-button"
          type="button"
          onClick={() => {
            assignments.reload();
            submissions.reload();
            quality.reload();
          }}
        >
          Try again
        </button>
      </div>
    );
  }

  const rows = assignments.resource.data.assignments;
  const open = rows.filter((row) => !['approved', 'rejected'].includes(row.status));
  // Bind once so the JSX below narrows the optional `record` to a value instead
  // of repeating a property access the compiler cannot keep narrowed.
  const record = quality.resource.data.record;
  const consequences = quality.resource.data.consequences;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Work</h1>
      <p className="nv-muted">
        {open.length === 0
          ? 'Nothing needs you right now. Accepted work is paid as it is approved.'
          : `${open.length} piece${open.length === 1 ? '' : 's'} of work still need${open.length === 1 ? 's' : ''} you.`}
      </p>

      <section className="nv-stack">
        <h2 className="nv-h2">Assignments</h2>
        {rows.length === 0 ? (
          <p className="nv-banner">
            No assignment yet. Managed work starts with an invitation, and matching uses your verified
            skills.
          </p>
        ) : (
          <ul className="nv-list">
            {rows.map((row) => (
              <li className="nv-card" key={row.id}>
                <div className="nv-row nv-row--between">
                  <h3 className="nv-h2">
                    <Link to={`/work/assignments/${row.id}`}>{row.title}</Link>
                  </h3>
                  <span className="nv-badge" data-status={row.status === 'approved' ? 'verified' : 'unverified'}>
                    {STATUS_COPY[row.status] ?? row.status.replace(/_/g, ' ')}
                  </span>
                </div>
                <p className="nv-muted">
                  {row.project.title}
                  {row.due_at ? ` · due ${formatDateTime(row.due_at)}` : ' · no deadline set'}
                </p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="nv-stack">
        <h2 className="nv-h2">What you sent</h2>
        {submissions.resource.data.submissions.length === 0 ? (
          <p className="nv-muted">No submission yet.</p>
        ) : (
          <ul className="nv-list">
            {submissions.resource.data.submissions.map((row) => (
              <li key={row.submission_id}>
                <Link to={`/work/assignments/${row.assignment_id}`}>{row.assignment_title}</Link>{' '}
                <span className="nv-muted">
                  · {row.status.replace(/_/g, ' ')} · {formatDateTime(row.submitted_at) || 'just now'}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">Your quality record</h2>
        {record == null ? (
          <p className="nv-muted">
            No reviewed work yet. Quality is built from real submissions — a missing record is not a bad
            one.
          </p>
        ) : (
          <>
            <p>
              {record.reviews_count} review
              {record.reviews_count === 1 ? '' : 's'} ·{' '}
              {record.approvals} approved ·{' '}
              {record.reworks} rework ·{' '}
              {record.rejections} rejected
            </p>
            {record.average_score !== null ? (
              <p className="nv-muted">Average score: {record.average_score}%</p>
            ) : null}
            {record.gold_tasks > 0 ? (
              <p className="nv-muted">
                Gold checks: {record.gold_correct} of {record.gold_tasks} correct. A gold task is normal
                work with a known answer, used to keep review honest.
              </p>
            ) : null}
          </>
        )}
        {consequences.length > 0 ? (
          <>
            <h3 className="nv-h2">What it changed</h3>
            <ul className="nv-list">
              {consequences.map((row, index) => (
                <li key={`${row.kind}-${index}`}>
                  <strong>{row.kind.replace(/_/g, ' ')}</strong>
                  {row.reason ? <span className="nv-muted"> · {row.reason}</span> : null}
                </li>
              ))}
            </ul>
          </>
        ) : null}
      </section>

      <p className="nv-muted">
        <Link to="/earnings">See your earnings</Link> · <Link to="/opportunities">Find more work</Link>
      </p>
    </div>
  );
}
