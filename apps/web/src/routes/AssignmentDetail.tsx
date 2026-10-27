/**
 * One assignment (B9).
 *
 * The form is generated from the template's own schemas, the same generator as
 * practice and assessments. Submitting carries a client key, so pressing the
 * button twice after a dropped connection stores one submission, not two.
 *
 * Gold work is not disclosed while it is in flight — the API does not send the
 * marker — and reviewer messages are shown in place, because a rework request
 * without the reason is just a closed door.
 */
import type {
  AssignmentDetailOut,
  AssignmentStateOut,
  MessageListOut,
  SubmissionResultOut,
} from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { MessageSquare, Send } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { TaskControl, TaskPrompt, buildAnswer, controlFor, type TaskValue } from '../components/TaskForm';
import { clearDraft, draftKey, stableClientKey, useDraft } from '../lib/draft';
import { ApiError, http } from '../lib/http';
import { formatDateTime } from '../lib/format';
import { isAnswerValue } from '../lib/practice';
import { useApiResource } from '../lib/resource';
import { useSessionOptional } from '../lib/session';

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

export function AssignmentDetail(): JSX.Element {
  const { assignmentId = '' } = useParams<{ assignmentId: string }>();
  const session = useSessionOptional();
  const owner = session?.me?.id ?? 'anonymous';
  const { resource, reload } = useApiResource<AssignmentDetailOut>(`/work/assignments/${assignmentId}`);
  const messages = useApiResource<MessageListOut>(`/work/assignments/${assignmentId}/messages`);
  // The answer is written as it is typed; the idempotency key is persisted too,
  // so a reload after a lost response re-sends the same submission rather than
  // creating a second one.
  const draft = useDraft<TaskValue>(draftKey('work', owner, assignmentId), null, isAnswerValue);
  const { value, setValue } = draft;
  const keyStorage = draftKey('work-client-key', owner, assignmentId);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [sent, setSent] = React.useState<SubmissionResultOut | null>(null);
  const [clientKey, setClientKey] = React.useState(() => stableClientKey(keyStorage));

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this assignment">
        <Skeleton height="2rem" width="50%" />
        <Skeleton lines={3} />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Assignment" />
        <Banner tone="info">
          <p>Work is not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/work">Back to your work</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Work" title="Assignment" />
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
        <p className="nv-muted">
          <Link to="/work">Back to your work</Link>
        </p>
      </div>
    );
  }

  const assignment = resource.data;
  const control = controlFor(
    assignment.task?.input_schema,
    assignment.task?.answer_schema,
    'This assignment is not attached to a task template, so there is no form to send. Message your reviewer from here if that looks wrong.',
  );
  const answer = buildAnswer(control, value);

  async function start(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<AssignmentStateOut>(`/work/assignments/${assignment.id}/start`);
      reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not start this assignment.');
    } finally {
      setBusy(false);
    }
  }

  async function submit(): Promise<void> {
    if (!answer) return;
    setBusy(true);
    setError(null);
    try {
      const result = await http.post<SubmissionResultOut>(`/work/assignments/${assignment.id}/submissions`, {
        payload: answer,
        client_key: clientKey,
      });
      setSent(result);
      // Accepted: the draft and its key have done their job. The next send from
      // this screen is a new version, so it needs a fresh key.
      draft.clear();
      clearDraft(keyStorage);
      setClientKey(stableClientKey(keyStorage));
      reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your work. Try again.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Work"
        title={assignment.title}
        description={`${assignment.project.title}${
          assignment.due_at ? ` · due ${formatDateTime(assignment.due_at)}` : ' · no deadline set'
        }`}
        actions={
          <Badge status={assignment.status} tone={statusTone(assignment.status)}>
            {STATUS_COPY[assignment.status] ?? assignment.status.replace(/_/g, ' ')}
          </Badge>
        }
      />

      <p className="nv-muted">
        <Link to="/work">Your work</Link>
      </p>

      {error ? (
        <Banner tone="danger">
          <p>{error}</p>
        </Banner>
      ) : null}

      {assignment.status === 'assigned' ? (
        <Banner
          tone="info"
          actions={
            <Button disabled={busy} size="sm" type="button" variant="secondary" onClick={() => void start()}>
              {busy ? 'Starting…' : 'Start this assignment'}
            </Button>
          }
        >
          <p>Start when you are ready. Starting does not use up a try.</p>
        </Banner>
      ) : null}

      {assignment.status === 'rework' ? (
        <Banner tone="warning">
          <p>
            This work needs rework. The reviewer&apos;s reason is below; sending a new version is expected,
            not penalised.
          </p>
        </Banner>
      ) : null}

      {assignment.task ? (
        <Panel title={assignment.task.name}>
          <div className="nv-stack">
            <div className="nv-prose">
              {assignment.task.instructions_md
                .split(/\n{2,}/)
                .filter((block) => block.trim().length > 0)
                .map((block, index) => (
                  <p key={index}>{block.trim()}</p>
                ))}
            </div>
            {assignment.task.input_schema && Object.keys(assignment.task.input_schema).length > 0 ? (
              <TaskPrompt payload={assignment.task.input_schema as Record<string, unknown>} />
            ) : null}
            <TaskControl control={control} value={value} onChange={setValue} />
          </div>
        </Panel>
      ) : (
        <Banner tone="warning">
          <p>{control.kind === 'unsupported' ? control.reason : null}</p>
        </Banner>
      )}

      {sent ? (
        <Banner tone="success">
          <h2 className="nv-h3">Sent</h2>
          <p>{sent.message}</p>
          <p className="nv-muted">
            Status: {sent.status.replace(/_/g, ' ')}
            {sent.submitted_at ? ` · ${formatDateTime(sent.submitted_at)}` : ''}. You will be told here when
            it is reviewed.
          </p>
        </Banner>
      ) : assignment.status !== 'approved' && assignment.status !== 'rejected' ? (
        <div className="nv-row nv-row--between">
          <span className="nv-muted">{answer ? 'Ready to send.' : 'Complete the form to send.'}</span>
          <Button disabled={busy || !assignment.task || !answer} type="button" onClick={() => void submit()}>
            <Send aria-hidden="true" size={15} />
            {busy ? 'Sending…' : assignment.last_submission ? 'Send a new version' : 'Send this work'}
          </Button>
        </div>
      ) : null}

      {draft.savedAt ? (
        <p className="nv-muted" aria-live="polite">
          Your answer is saved on this device — it is still here if the connection drops.
        </p>
      ) : null}

      {assignment.last_submission ? (
        <p className="nv-muted">
          Last sent {formatDateTime(assignment.last_submission.submitted_at) || 'just now'} ·{' '}
          {assignment.last_submission.status.replace(/_/g, ' ')}
        </p>
      ) : null}

      <Panel title="Messages about this work" actions={<MessageSquare aria-hidden="true" size={16} />}>
        {messages.resource.status === 'loading' ? <Skeleton lines={3} /> : null}
        {messages.resource.status === 'error' ? (
          <ErrorState
            body={messages.resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={messages.reload}>
                Try again
              </Button>
            }
          />
        ) : null}
        {messages.resource.status === 'ready' ? (
          messages.resource.data.messages.length === 0 ? (
            <EmptyState
              body="A reviewer's question or rework reason will appear here, in place with the work."
              icon={MessageSquare}
              title="No messages yet"
            />
          ) : (
            <ul className="nv-list nv-list--ruled">
              {messages.resource.data.messages.map((message) => (
                <li key={message.id}>
                  <p>{message.body}</p>
                  <p className="nv-meta">{formatDateTime(message.created_at)}</p>
                </li>
              ))}
            </ul>
          )
        ) : null}
      </Panel>
    </div>
  );
}
