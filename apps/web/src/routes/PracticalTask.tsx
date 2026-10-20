/**
 * A practical task (B7 remaining).
 *
 * Unlike an assessment, there is no hidden answer: the brief and the rubric are
 * public, because the standard should be known before the work starts. The form
 * asks for what a reviewer can actually judge — a written account and a link to
 * the deliverable — and the client key makes a retry safe.
 */
import type { PracticalSubmissionOut, PracticalTaskListOut, PracticalTaskOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

function rubricRows(rubric: unknown): Array<{ label: string; detail: string }> {
  if (Array.isArray(rubric)) {
    return rubric.map((item, index) => {
      if (typeof item === 'string') return { label: `Criterion ${index + 1}`, detail: item };
      if (item && typeof item === 'object') {
        const record = item as Record<string, unknown>;
        return {
          label: String(record.name ?? record.label ?? `Criterion ${index + 1}`),
          detail: String(record.description ?? record.detail ?? record.weight ?? ''),
        };
      }
      return { label: `Criterion ${index + 1}`, detail: String(item) };
    });
  }
  if (rubric && typeof rubric === 'object') {
    return Object.entries(rubric as Record<string, unknown>).map(([label, detail]) => ({
      label,
      detail: typeof detail === 'string' ? detail : JSON.stringify(detail),
    }));
  }
  return [];
}

export function PracticalTask(): JSX.Element {
  const { slug = '' } = useParams<{ slug: string }>();
  const { resource, reload } = useApiResource<PracticalTaskListOut>('/verification/practical');
  const [summary, setSummary] = React.useState('');
  const [deliverable, setDeliverable] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [sent, setSent] = React.useState<PracticalSubmissionOut | null>(null);
  const clientKey = React.useRef(`practical-${slug}-${crypto.randomUUID()}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this practical task">
        <Skeleton height="2rem" width="50%" />
        <Skeleton lines={4} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Practical task</h1>
        <p className="nv-banner">Verification is not switched on for this environment yet.</p>
        <Link to="/home">Back to your home</Link>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Practical task</h1>
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

  const task: PracticalTaskOut | undefined = resource.data.tasks.find((row) => row.slug === slug);

  if (!task) {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Practical task</h1>
        <p className="nv-banner">
          This task is not published, or it was withdrawn. Nothing you already submitted is lost.
        </p>
        <p className="nv-muted">
          <Link to="/verification">Back to verification</Link>
        </p>
      </div>
    );
  }

  async function submit(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      // `slug` is the route parameter the lookup above matched, and using it here
      // avoids capturing a value the compiler cannot prove is defined.
      const result = await http.post<PracticalSubmissionOut>(`/verification/practical/${slug}`, {
        payload: {
          summary: summary.trim(),
          deliverable_url: deliverable.trim() || null,
        },
        client_key: clientKey.current,
      });
      setSent(result);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your work. Try again.');
    } finally {
      setBusy(false);
    }
  }

  const criteria = rubricRows(task.rubric);

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to="/verification">Verification</Link>
      </p>
      <h1 className="nv-h1">{task.title}</h1>
      <p className="nv-muted">Reviewed by a person against the rubric below.</p>

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">The brief</h2>
        {task.brief_md.trim().length === 0 ? (
          <p className="nv-muted">The brief has not been written yet. Do not start this task.</p>
        ) : (
          task.brief_md
            .split(/\n{2,}/)
            .filter((block) => block.trim().length > 0)
            .map((block, index) => <p key={index}>{block.trim()}</p>)
        )}
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">How it will be judged</h2>
        {criteria.length === 0 ? (
          <p className="nv-muted">No rubric is published, so this task cannot be reviewed yet.</p>
        ) : (
          <ul className="nv-list">
            {criteria.map((row) => (
              <li key={row.label}>
                <strong>{row.label}</strong>
                {row.detail ? <span className="nv-muted"> · {row.detail}</span> : null}
              </li>
            ))}
          </ul>
        )}
      </section>

      <ErrorNote message={error} />

      {sent ? (
        <section className="nv-card" aria-live="polite">
          <h2 className="nv-h2">Sent for review</h2>
          <p>{sent.message}</p>
          <p className="nv-muted">
            Status: {sent.status.replace(/_/g, ' ')}. You will see the result and the reviewer&apos;s
            notes on your transcript and in notifications.
          </p>
          <Link className="nv-button" to="/verification">
            Back to verification
          </Link>
        </section>
      ) : (
        <section className="nv-card nv-stack">
          <h2 className="nv-h2">Send your work</h2>
          <p className="nv-muted">
            Explain what you did and how it meets the brief. A link is optional but makes review faster.
          </p>
          <div className="nv-field">
            <label className="nv-label" htmlFor="nv-practical-summary">
              What you did
            </label>
            <textarea
              className="nv-input"
              id="nv-practical-summary"
              minLength={20}
              required
              rows={6}
              value={summary}
              onChange={(event) => setSummary(event.target.value)}
            />
            <span className="nv-muted">{summary.trim().length} characters (at least 20)</span>
          </div>
          <div className="nv-field">
            <label className="nv-label" htmlFor="nv-practical-link">
              Link to the deliverable (optional)
            </label>
            <input
              className="nv-input"
              id="nv-practical-link"
              maxLength={1024}
              placeholder="https://"
              type="url"
              value={deliverable}
              onChange={(event) => setDeliverable(event.target.value)}
            />
          </div>
          <button
            className="nv-button"
            disabled={busy || summary.trim().length < 20}
            type="button"
            onClick={() => void submit()}
          >
            {busy ? 'Sending…' : 'Send for review'}
          </button>
        </section>
      )}
    </div>
  );
}
