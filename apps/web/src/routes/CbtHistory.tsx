/**
 * CBT history (B14).
 *
 * The attempt trail is what makes a practice score useful: the question, the
 * answer the student gave, the correct key and the explanation. The API only
 * returns the signed-in student's own attempts, so this page can show the answer
 * key without leaking another learner's work.
 */
import type { CbtHistoryItemOut, CbtHistoryOut } from '@nelavista/api-client';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Panel, Select, Skeleton } from '@nelavista/ui';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';

function durationLabel(ms: number | null | undefined): string {
  if (ms === null || ms === undefined) return 'Not recorded';
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(1)} s`;
}

export function CbtHistory(): JSX.Element {
  const { resource, reload } = useApiResource<CbtHistoryOut>('/academia/cbt/history?limit=300');
  const [courseFilter, setCourseFilter] = React.useState('all');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading CBT history">
        <Skeleton height="2rem" width="35%" />
        <Skeleton lines={3} />
        <Skeleton lines={6} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia · CBT" title="CBT history" />
        <EmptyState
          title="CBT history is not switched on here"
          body="This environment has the feature off. It is not a missing attempt record."
        />
      </div>
    );
  }

  if (resource.status === 'missing' || resource.status === 'error') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia · CBT" title="CBT history" />
        <ErrorState
          title="The attempt history did not load"
          body={resource.message}
          action={
            <Button onClick={reload} type="button" variant="secondary">
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const history = resource.data;
  const courses = Array.from(
    new Map(
      history.items
        .filter((item) => item.course_code)
        .map((item) => [String(item.course_id), item.course_code as string]),
    ),
  ).sort((a, b) => a[1].localeCompare(b[1]));
  const items =
    courseFilter === 'all'
      ? history.items
      : history.items.filter((item) => String(item.course_id) === courseFilter);

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Academia · CBT"
        title="CBT history"
        description="Every answered practice question, newest first, with your answer, the correct key and the explanation."
        actions={
          <Link className="nv-button" to="/academia/cbt">
            Start practice
          </Link>
        }
      />

      <div className="nv-grid">
        <div className="nv-stat">
          <p className="nv-stat__value">{history.attempts}</p>
          <p className="nv-stat__label">Answers recorded</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{history.correct}</p>
          <p className="nv-stat__label">Correct</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{history.attempts === 0 ? 'Not set' : `${history.accuracy}%`}</p>
          <p className="nv-stat__label">Accuracy</p>
        </div>
      </div>

      <Panel title="Attempts" actions={<Badge tone="neutral">{items.length} shown</Badge>}>
        {courses.length > 1 ? (
          <div className="nv-row" style={{ marginBottom: 'var(--nv-space-md)', maxWidth: '18rem' }}>
            <Select
              label="Course"
              options={[
                { value: 'all', label: 'All courses' },
                ...courses.map(([id, code]) => ({ value: id, label: code })),
              ]}
              value={courseFilter}
              onChange={(event) => setCourseFilter(event.target.value)}
            />
          </div>
        ) : null}
        {history.items.length === 0 ? (
          <EmptyState
            title="No answered questions yet"
            body="Practice records an answer as soon as you submit it. Your first attempt will appear here."
            image={EMPTY_IMAGES.cbt}
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/cbt">
                Open CBT practice
              </Link>
            }
          />
        ) : items.length === 0 ? (
          <EmptyState
            title="No attempts in this course"
            body="Choose another course or all courses to see the rest of your history."
            action={
              <Button onClick={() => setCourseFilter('all')} size="sm" type="button" variant="secondary">
                Show all courses
              </Button>
            }
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <caption className="nv-sr-only">CBT attempt history</caption>
              <thead>
                <tr>
                  <th scope="col">Answered</th>
                  <th scope="col">Course and topic</th>
                  <th scope="col">Question</th>
                  <th scope="col">Result</th>
                  <th scope="col">Review</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <HistoryRow key={item.attempt_id} item={item} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </div>
  );
}

function HistoryRow({ item }: { item: CbtHistoryItemOut }): JSX.Element {
  return (
    <tr>
      <td>
        <span>{item.answered_at ? formatDateTime(item.answered_at) : 'Not recorded'}</span>
        <p className="nv-meta">{durationLabel(item.duration_ms)}</p>
      </td>
      <td>
        <span className="nv-mono">{item.course_code ?? `Course ${item.course_id}`}</span>
        <p className="nv-meta">{item.topic ?? 'General'}</p>
      </td>
      <td>
        <p>{item.prompt}</p>
      </td>
      <td>
        <Badge tone={item.is_correct ? 'success' : 'warning'}>
          {item.is_correct ? 'Correct' : 'Incorrect'}
        </Badge>
      </td>
      <td>
        <details>
          <summary>Open answer</summary>
          <dl className="nv-stack nv-stack--tight" style={{ marginTop: 'var(--nv-space-sm)' }}>
            <div className="nv-row nv-row--between">
              <dt className="nv-muted">Your answer</dt>
              <dd className="nv-mono">{item.selected_key ?? 'Not recorded'}</dd>
            </div>
            <div className="nv-row nv-row--between">
              <dt className="nv-muted">Correct answer</dt>
              <dd className="nv-mono">{item.correct_key ?? 'Not recorded'}</dd>
            </div>
          </dl>
          {item.explanation ? <p className="nv-muted">{item.explanation}</p> : null}
        </details>
      </td>
    </tr>
  );
}
