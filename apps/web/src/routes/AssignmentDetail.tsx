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
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { TaskControl, TaskPrompt, buildAnswer, controlFor, type TaskValue } from '../components/TaskForm';
import { ApiError, http } from '../lib/http';
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

export function AssignmentDetail(): JSX.Element {
  const { assignmentId = '' } = useParams<{ assignmentId: string }>();
  const { resource, reload } = useApiResource<AssignmentDetailOut>(`/work/assignments/${assignmentId}`);
  const messages = useApiResource<MessageListOut>(`/work/assignments/${assignmentId}/messages`);
  const [value, setValue] = React.useState<TaskValue>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [sent, setSent] = React.useState<SubmissionResultOut | null>(null);
  // One key per mounted assignment: a retry after a timeout reuses it.
  const clientKey = React.useRef(`web-${assignmentId}-${crypto.randomUUID()}`);

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
        <h1 className="nv-h1">Assignment</h1>
        <p className="nv-banner">Work is not switched on for this environment yet.</p>
        <Link to="/work">Back to your work</Link>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Assignment</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
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
      const result = await http.post<SubmissionResultOut>(
        `/work/assignments/${assignment.id}/submissions`,
        { payload: answer, client_key: clientKey.current },
      );
      setSent(result);
      reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your work. Try again.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to="/work">Your work</Link>
      </p>
      <div className="nv-row nv-row--between">
        <h1 className="nv-h1">{assignment.title}</h1>
        <span className="nv-badge" data-status={assignment.status === 'approved' ? 'verified' : 'unverified'}>
          {STATUS_COPY[assignment.status] ?? assignment.status.replace(/_/g, ' ')}
        </span>
      </div>
      <p className="nv-muted">
        {assignment.project.title}
        {assignment.due_at ? ` · due ${formatDateTime(assignment.due_at)}` : ' · no deadline set'}
      </p>

      <ErrorNote message={error} />

      {assignment.status === 'assigned' ? (
        <section className="nv-card">
          <p>Start when you are ready. Starting does not use up a try.</p>
          <button className="nv-button" disabled={busy} type="button" onClick={() => void start()}>
            {busy ? 'Starting…' : 'Start this assignment'}
          </button>
        </section>
      ) : null}

      {assignment.status === 'rework' ? (
        <p className="nv-banner">
          This work needs rework. The reviewer&apos;s reason is below; sending a new version is expected,
          not penalised.
        </p>
      ) : null}

      {assignment.task ? (
        <section className="nv-card nv-stack">
          <h2 className="nv-h2">{assignment.task.name}</h2>
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
        </section>
      ) : (
        <p className="nv-banner">{control.kind === 'unsupported' ? control.reason : null}</p>
      )}

      {sent ? (
        <section className="nv-card" aria-live="polite">
          <h2 className="nv-h2">Sent</h2>
          <p>{sent.message}</p>
          <p className="nv-muted">
            Status: {sent.status.replace(/_/g, ' ')}
            {sent.submitted_at ? ` · ${formatDateTime(sent.submitted_at)}` : ''}. You will be told here
            when it is reviewed.
          </p>
        </section>
      ) : assignment.status !== 'approved' && assignment.status !== 'rejected' ? (
        <div className="nv-row">
          <button
            className="nv-button"
            disabled={busy || !assignment.task || !answer}
            type="button"
            onClick={() => void submit()}
          >
            {busy ? 'Sending…' : assignment.last_submission ? 'Send a new version' : 'Send this work'}
          </button>
          <span className="nv-muted">
            {answer ? 'Ready to send.' : 'Complete the form to send.'}
          </span>
        </div>
      ) : null}

      {assignment.last_submission ? (
        <p className="nv-muted">
          Last sent {formatDateTime(assignment.last_submission.submitted_at) || 'just now'} ·{' '}
          {assignment.last_submission.status.replace(/_/g, ' ')}
        </p>
      ) : null}

      {messages.resource.status === 'ready' && messages.resource.data.messages.length > 0 ? (
        <section className="nv-card">
          <h2 className="nv-h2">Messages about this work</h2>
          <ul className="nv-list">
            {messages.resource.data.messages.map((message) => (
              <li key={message.id}>
                <p>{message.body}</p>
                <p className="nv-muted">{formatDateTime(message.created_at)}</p>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </div>
  );
}
