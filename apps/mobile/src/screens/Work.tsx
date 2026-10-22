import type { AssignmentDetailOut, AssignmentListOut } from '@nelavista/api-client';
import * as React from 'react';
import { Pressable } from 'react-native';

import { TaskControl, type TaskValue } from '../components/TaskControl';
import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { answerFor, controlFor } from '../lib/taskForm';
import { enqueue, due } from '../lib/offlineQueue';
import { flushQueue, queueStore } from '../lib/sync';
import { useApi } from '../lib/useApi';
import { Badge, Body, Button, Card, ErrorText, H2, Loading, Muted, Note, Screen } from '../ui';

export function Work({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const list = useApi<AssignmentListOut>('/work/assignments');
  const [queued, setQueued] = React.useState(0);

  React.useEffect(() => {
    void (async () => setQueued(due(await queueStore.load()).length))();
  }, []);

  return (
    <Screen title="Work" onBack={() => navigate({ name: 'home' })}>
      {queued > 0 ? <Note message={`${queued} submission(s) waiting to sync. They will send automatically.`} /> : null}
      {list.remote.status === 'loading' ? <Loading /> : null}
      {list.remote.status === 'error' ? <ErrorText message={list.remote.message} /> : null}
      {list.remote.status === 'ready'
        ? list.remote.data.assignments.map((row) => (
            <Pressable key={row.id} onPress={() => navigate({ name: 'assignment', id: row.id })}>
              <Card>
                <H2>{row.title}</H2>
                <Badge
                  label={row.status.replace(/_/g, ' ')}
                  tone={row.status === 'approved' ? 'ok' : row.status === 'rework' || row.status === 'rejected' ? 'bad' : 'muted'}
                />
                <Muted>
                  {row.project.title}
                  {row.due_at ? ` · due ${row.due_at.slice(0, 10)}` : ''}
                </Muted>
              </Card>
            </Pressable>
          ))
        : null}
      {list.remote.status === 'ready' && list.remote.data.assignments.length === 0 ? (
        <Muted>No assignment yet. Managed work starts with an invitation.</Muted>
      ) : null}
    </Screen>
  );
}

export function AssignmentScreen({
  id,
  navigate,
}: {
  id: number;
  navigate: (route: Route) => void;
}): JSX.Element {
  const detail = useApi<AssignmentDetailOut>(`/work/assignments/${id}`);
  const [value, setValue] = React.useState<TaskValue>(null);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  const control =
    detail.remote.status === 'ready'
      ? controlFor(detail.remote.data.task?.input_schema, detail.remote.data.task?.answer_schema)
      : { kind: 'unsupported' as const, reason: 'Loading…' };
  const answer = answerFor(control, value);

  async function submit(): Promise<void> {
    if (!answer) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      const item = await enqueue(queueStore, id, answer);
      const report = await flushQueue();
      const remaining = await queueStore.load();
      const stillQueued = remaining.some((row) => row.clientKey === item.clientKey);
      if (stillQueued) {
        const stored = remaining.find((row) => row.clientKey === item.clientKey);
        setNote(
          `Saved on this device and will retry automatically${stored?.lastError ? ` (${stored.lastError})` : ''}. Nothing you wrote is lost.`,
        );
      } else if (report.saved > 0) {
        setNote('Submitted. It will be reviewed; you can leave this screen.');
      } else {
        setNote('Already submitted — this retry did not create a duplicate.');
      }
      detail.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save that submission.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Assignment" onBack={() => navigate({ name: 'work' })}>
      {detail.remote.status === 'loading' ? <Loading /> : null}
      {detail.remote.status === 'error' ? <ErrorText message={detail.remote.message} /> : null}
      {detail.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{detail.remote.data.title}</H2>
            <Badge label={detail.remote.data.status.replace(/_/g, ' ')} />
            <Muted>{detail.remote.data.project.title}</Muted>
            {detail.remote.data.status === 'rework' ? (
              <Muted>This needs rework. Sending a new version is expected, not penalised.</Muted>
            ) : null}
          </Card>

          {detail.remote.data.task ? (
            <Card>
              <H2>{detail.remote.data.task.name}</H2>
              <Body>{detail.remote.data.task.instructions_md}</Body>
              <TaskControl control={control} value={value} onChange={setValue} />
            </Card>
          ) : (
            <Muted>{control.kind === 'unsupported' ? control.reason : null}</Muted>
          )}

          <Note message={note} />
          <ErrorText message={error} />
          <Button
            disabled={busy || !detail.remote.data.task || !answer}
            label={busy ? 'Saving…' : detail.remote.data.last_submission ? 'Send a new version' : 'Send this work'}
            onPress={() => void submit()}
          />
          <Muted>
            Submissions are saved on the device before sending. A retry uses the same key, so it cannot
            create two submissions.
          </Muted>
        </>
      ) : null}
    </Screen>
  );
}
