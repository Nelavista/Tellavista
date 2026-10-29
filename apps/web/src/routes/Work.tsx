/**
 * Work (B9).
 *
 * Three lists answer three different questions, in the order a student asks
 * them: what do I have to do, what did I already send, and why is my quality
 * where it is? The quality record shows the counts that produced it, because a
 * score with no explanation is not actionable.
 */
import type { AssignmentListOut, QualityOut, SubmissionListOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ClipboardCheck, FileCheck2, Gauge } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';

const STATUS_COPY: Record<string, string> = {
  assigned: 'Ready to start',
  in_progress: 'In progress',
  submitted: 'Waiting for review',
  approved: 'Approved',
  rework: 'Rework needed',
  rejected: 'Not accepted',
};

function statusTone(status: string): 'neutral' | 'success' | 'info' | 'warning' | 'danger' {
  if (status === 'approved') return 'success';
  if (status === 'submitted' || status === 'in_progress') return 'info';
  if (status === 'rework') return 'warning';
  if (status === 'rejected') return 'danger';
  return 'neutral';
}

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
        <PageHeader eyebrow="Work" title="My work" />
        <Banner tone="info">
          <p>Work is not switched on for this environment yet. Your learning and proof are unaffected.</p>
        </Banner>
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
        <PageHeader eyebrow="Work" title="My work" />
        <ErrorState
          body={failed && 'message' in failed ? failed.message : undefined}
          action={
            <Button
              size="sm"
              type="button"
              variant="secondary"
              onClick={() => {
                assignments.reload();
                submissions.reload();
                quality.reload();
              }}
            >
              Try again
            </Button>
          }
        />
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
      <PageHeader
        eyebrow="Work"
        title="My work"
        description={
          open.length === 0
            ? 'Nothing needs you right now. Accepted work is paid as it is approved.'
            : `${open.length} piece${open.length === 1 ? '' : 's'} of work still need${open.length === 1 ? 's' : ''} you.`
        }
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/opportunities">
              Find more work
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/earnings">
              Earnings
            </Link>
          </>
        }
      />

      <Panel title="Assignments" actions={<Badge tone="info">{rows.length}</Badge>}>
        {rows.length === 0 ? (
          <EmptyState
            body="Managed work starts with an invitation, and matching uses your verified skills."
            icon={ClipboardCheck}
            image={EMPTY_IMAGES.work}
            title="No assignment yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/opportunities">
                Browse opportunities
              </Link>
            }
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Project</th>
                  <th>Due</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id}>
                    <td>
                      <Link to={`/work/assignments/${row.id}`}>{row.title}</Link>
                    </td>
                    <td>{row.project.title}</td>
                    <td>{row.due_at ? formatDateTime(row.due_at) : 'No deadline set'}</td>
                    <td>
                      <Badge tone={statusTone(row.status)}>
                        {STATUS_COPY[row.status] ?? row.status.replace(/_/g, ' ')}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <Panel
        title="What you sent"
        actions={<Badge tone="neutral">{submissions.resource.data.submissions.length}</Badge>}
      >
        {submissions.resource.data.submissions.length === 0 ? (
          <EmptyState
            body="Submit an assignment and its status will appear here with the time it was sent."
            icon={FileCheck2}
            title="No submission yet"
          />
        ) : (
          <ul className="nv-list">
            {submissions.resource.data.submissions.map((row) => (
              <li key={row.submission_id}>
                <div className="nv-row nv-row--between">
                  <Link to={`/work/assignments/${row.assignment_id}`}>{row.assignment_title}</Link>
                  <Badge tone={statusTone(row.status)}>{row.status.replace(/_/g, ' ')}</Badge>
                </div>
                <p className="nv-meta">{formatDateTime(row.submitted_at) || 'just now'}</p>
              </li>
            ))}
          </ul>
        )}
      </Panel>

      <Panel title="Your quality record">
        {record == null ? (
          <EmptyState
            body="Quality is built from real submissions. A missing record is not a bad one."
            icon={Gauge}
            title="No reviewed work yet"
          />
        ) : (
          <div className="nv-stack">
            <div className="nv-grid">
              <div className="nv-stat">
                <p className="nv-stat__value">{record.reviews_count}</p>
                <p className="nv-stat__label">Reviews</p>
              </div>
              <div className="nv-stat">
                <p className="nv-stat__value">{record.approvals}</p>
                <p className="nv-stat__label">Approved</p>
              </div>
              <div className="nv-stat">
                <p className="nv-stat__value">{record.reworks}</p>
                <p className="nv-stat__label">Rework</p>
              </div>
              <div className="nv-stat">
                <p className="nv-stat__value">{record.rejections}</p>
                <p className="nv-stat__label">Rejected</p>
              </div>
            </div>
            {record.average_score !== null ? (
              <p className="nv-muted">Average score: {record.average_score}%</p>
            ) : null}
            {record.gold_tasks > 0 ? (
              <p className="nv-muted">
                Gold checks: {record.gold_correct} of {record.gold_tasks} correct. A gold task is normal work
                with a known answer, used to keep review honest.
              </p>
            ) : null}
            {consequences.length > 0 ? (
              <div>
                <h3 className="nv-h4">What it changed</h3>
                <ul className="nv-list">
                  {consequences.map((row, index) => (
                    <li key={`${row.kind}-${index}`}>
                      <strong>{row.kind.replace(/_/g, ' ')}</strong>
                      {row.reason ? <span className="nv-muted"> · {row.reason}</span> : null}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        )}
      </Panel>
    </div>
  );
}
