/**
 * A practical task (B7 remaining).
 *
 * Unlike an assessment, there is no hidden answer: the brief and the rubric are
 * public, because the standard should be known before the work starts. The form
 * asks for what a reviewer can actually judge — a written account and a link to
 * the deliverable — and the client key makes a retry safe.
 */
import type { PracticalSubmissionOut, PracticalTaskListOut, PracticalTaskOut } from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Skeleton,
  Textarea,
} from '@nelavista/ui';
import { ArrowLeft, ClipboardCheck, Send, ShieldCheck } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

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
        <PageHeader eyebrow="Verification" title="Practical task" />
        <Banner tone="info">
          <p>Verification is not switched on for this environment yet.</p>
        </Banner>
        <Link to="/home">Back to your home</Link>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Verification" title="Practical task" />
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

  const task: PracticalTaskOut | undefined = resource.data.tasks.find((row) => row.slug === slug);

  if (!task) {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Verification" title="Practical task" />
        <EmptyState
          body="This task is not published, or it was withdrawn. Nothing you already submitted is lost."
          icon={ClipboardCheck}
          title="Task not available"
        />
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
        <Link to="/verification">
          <ArrowLeft aria-hidden="true" size={14} /> Verification
        </Link>
      </p>

      <PageHeader
        eyebrow="Practical task"
        title={task.title}
        description="Reviewed by a person against the rubric below."
        actions={
          <Badge tone="info">
            <ShieldCheck aria-hidden="true" size={13} /> Human review
          </Badge>
        }
      />

      <Panel title="The brief">
        {task.brief_md.trim().length === 0 ? (
          <Banner tone="warning">
            <p>The brief has not been written yet. Do not start this task.</p>
          </Banner>
        ) : (
          <div className="nv-reading">
            {task.brief_md
              .split(/\n{2,}/)
              .filter((block) => block.trim().length > 0)
              .map((block, index) => (
                <p key={index}>{block.trim()}</p>
              ))}
          </div>
        )}
      </Panel>

      <Panel title="How it will be judged">
        {criteria.length === 0 ? (
          <EmptyState
            body="No rubric is published, so this task cannot be reviewed yet."
            icon={ClipboardCheck}
            title="No rubric"
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {criteria.map((row) => (
              <li key={row.label}>
                <strong>{row.label}</strong>
                {row.detail ? <span className="nv-muted"> · {row.detail}</span> : null}
              </li>
            ))}
          </ul>
        )}
      </Panel>

      {error ? (
        <Banner tone="danger">
          <p>{error}</p>
        </Banner>
      ) : null}

      {sent ? (
        <Banner tone="success">
          <h2 className="nv-h3">Sent for review</h2>
          <p>{sent.message}</p>
          <p className="nv-muted">
            Status: {sent.status.replace(/_/g, ' ')}. You will see the result and the reviewer&apos;s notes on
            your transcript and in notifications.
          </p>
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/verification">
            Back to verification
          </Link>
        </Banner>
      ) : (
        <Panel title="Send your work">
          <p className="nv-muted">
            Explain what you did and how it meets the brief. A link is optional but makes review faster.
          </p>
          <Textarea
            hint={`${summary.trim().length} characters (at least 20)`}
            id="nv-practical-summary"
            label="What you did"
            minLength={20}
            required
            rows={6}
            value={summary}
            onChange={(event) => setSummary(event.target.value)}
          />
          <div style={{ marginTop: 'var(--nv-space-lg)' }}>
            <Field
              hint="Optional. A URL a reviewer can open."
              id="nv-practical-link"
              label="Link to the deliverable"
              maxLength={1024}
              placeholder="https://"
              type="url"
              value={deliverable}
              onChange={(event) => setDeliverable(event.target.value)}
            />
          </div>
          <div style={{ marginTop: 'var(--nv-space-lg)' }}>
            <Button disabled={busy || summary.trim().length < 20} type="button" onClick={() => void submit()}>
              <Send aria-hidden="true" size={15} />
              {busy ? 'Sending…' : 'Send for review'}
            </Button>
          </div>
        </Panel>
      )}
    </div>
  );
}
