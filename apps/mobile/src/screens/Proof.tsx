import type {
  AttemptOut,
  AttemptResultOut,
  AssessmentListOut,
  TranscriptOut,
  VerificationOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Pressable } from 'react-native';

import { TaskControl, type TaskValue } from '../components/TaskControl';
import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { answerFor, controlFor } from '../lib/taskForm';
import { useApi } from '../lib/useApi';
import { Body, Badge, Button, Card, ErrorText, H2, Loading, Muted, Screen } from '../ui';

export function Verification({
  navigate,
}: {
  navigate: (route: Route) => void;
}): JSX.Element {
  const badges = useApi<VerificationOut>('/verification');
  const catalog = useApi<AssessmentListOut>('/verification/assessments');

  return (
    <Screen title="Verification" onBack={() => navigate({ name: 'home' })}>
      <Muted>Proof comes from a passed assessment or a reviewed practical task. Lessons are not proof.</Muted>
      {badges.remote.status === 'loading' ? <Loading /> : null}
      {badges.remote.status === 'error' ? <ErrorText message={badges.remote.message} /> : null}
      {badges.remote.status === 'ready'
        ? badges.remote.data.skills.map((skill) => (
            <Card key={skill.skill_id}>
              <H2>{skill.skill}</H2>
              <Badge
                label={skill.verified ? 'Verified' : skill.status.replace(/_/g, ' ')}
                tone={skill.verified ? 'ok' : skill.status === 'suspended' || skill.status === 'at_risk' ? 'bad' : 'muted'}
              />
              <Muted>
                {skill.verified
                  ? 'You passed an assessment for this skill.'
                  : 'An open sitting is not proof until it is submitted and passed.'}
              </Muted>
            </Card>
          ))
        : null}

      <H2>Assessments</H2>
      {catalog.remote.status === 'loading' ? <Loading /> : null}
      {catalog.remote.status === 'error' ? <ErrorText message={catalog.remote.message} /> : null}
      {catalog.remote.status === 'ready'
        ? catalog.remote.data.assessments.map((assessment) => (
            <Pressable key={assessment.id} onPress={() => navigate({ name: 'assessment', slug: assessment.slug })}>
              <Card>
                <H2>{assessment.title}</H2>
                <Muted>
                  {assessment.task_count} task{assessment.task_count === 1 ? '' : 's'} · pass at{' '}
                  {assessment.pass_threshold}% · {assessment.max_attempts} attempt(s)
                </Muted>
              </Card>
            </Pressable>
          ))
        : null}
      {catalog.remote.status === 'ready' && catalog.remote.data.assessments.length === 0 ? (
        <Muted>No assessment is published yet.</Muted>
      ) : null}

      <Button label="See your transcript" onPress={() => navigate({ name: 'transcript' })} tone="ghost" />
    </Screen>
  );
}

export function AssessmentScreen({
  slug,
  navigate,
}: {
  slug: string;
  navigate: (route: Route) => void;
}): JSX.Element {
  const [attempt, setAttempt] = React.useState<AttemptOut | null>(null);
  const [values, setValues] = React.useState<Record<number, TaskValue>>({});
  const [result, setResult] = React.useState<AttemptResultOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);
  const started = React.useRef(false);

  React.useEffect(() => {
    if (started.current) return;
    started.current = true;
    void (async () => {
      try {
        setAttempt(await api.post<AttemptOut>(`/verification/assessments/${slug}/start`));
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Could not open this assessment.');
      }
    })();
  }, [slug]);

  const answers: Record<string, Record<string, unknown>> = {};
  if (attempt) {
    for (const task of attempt.tasks) {
      const control = controlFor(task.input_schema, task.answer_schema);
      const answer = answerFor(control, values[task.task_id] ?? null);
      if (answer) answers[String(task.task_id)] = answer;
    }
  }

  async function submit(): Promise<void> {
    if (!attempt) return;
    setBusy(true);
    setError(null);
    try {
      setResult(await api.post<AttemptResultOut>(`/verification/attempts/${attempt.attempt_id}/submit`, { answers }));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not submit this sitting.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Assessment" onBack={() => navigate({ name: 'verification' })}>
      {error ? <ErrorText message={error} /> : null}
      {!attempt && !error ? <Loading /> : null}
      {result ? (
        <Card>
          <H2>{result.expired ? 'Expired' : result.passed ? 'Passed' : 'Not passed yet'}</H2>
          <Body>
            Score {result.score}
            {result.pass_threshold !== null ? ` · pass mark ${result.pass_threshold}%` : ''}
          </Body>
          <Muted>
            {result.passed
              ? 'A proved line is on your transcript.'
              : 'A failed sitting does not remove an existing badge.'}
          </Muted>
          {result.tasks.map((task) => (
            <Muted key={task.task_id}>
              Task {task.ordinal}: {task.correct ? 'correct' : 'incorrect'} ({task.points}/{task.max_points})
              {task.feedback ? ` · ${task.feedback}` : ''}
            </Muted>
          ))}
          <Button label="Back to verification" onPress={() => navigate({ name: 'verification' })} />
        </Card>
      ) : attempt ? (
        <>
          <Muted>
            {attempt.tasks.length} task(s). Leaving the app does not lose the sitting; it resumes these
            tasks until it expires.
          </Muted>
          {attempt.tasks.map((task) => {
            const control = controlFor(task.input_schema, task.answer_schema);
            return (
              <Card key={task.task_id}>
                <H2>
                  Task {task.ordinal} · {task.points} point(s)
                </H2>
                {Object.entries(task.payload)
                  .filter(([, value]) => typeof value === 'string' || typeof value === 'number')
                  .map(([key, value]) => (
                    <Muted key={key}>
                      {key.replace(/_/g, ' ')}: {String(value)}
                    </Muted>
                  ))}
                <TaskControl
                  control={control}
                  value={values[task.task_id] ?? null}
                  onChange={(next) => setValues((current) => ({ ...current, [task.task_id]: next }))}
                />
              </Card>
            );
          })}
          <Button
            disabled={busy || Object.keys(answers).length === 0}
            label={busy ? 'Submitting…' : 'Submit this sitting'}
            onPress={() => void submit()}
          />
          <Muted>
            {Object.keys(answers).length} of {attempt.tasks.length} answered — unanswered tasks score zero.
          </Muted>
        </>
      ) : null}
    </Screen>
  );
}

export function Transcript({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const transcript = useApi<TranscriptOut>('/verification/transcript');
  return (
    <Screen title="Transcript" onBack={() => navigate({ name: 'home' })}>
      {transcript.remote.status === 'loading' ? <Loading /> : null}
      {transcript.remote.status === 'error' ? <ErrorText message={transcript.remote.message} /> : null}
      {transcript.remote.status === 'ready' ? (
        <>
          <Muted>
            {transcript.remote.data.counts.learned} learned · {transcript.remote.data.counts.proved} proved ·{' '}
            {transcript.remote.data.counts.delivered} delivered
          </Muted>
          {transcript.remote.data.entries.map((entry) => (
            <Card key={entry.id}>
              <H2>{entry.title}</H2>
              <Muted>
                {entry.kind} · {entry.skill ?? 'general'} · {entry.occurred_at.slice(0, 10)} · evidence{' '}
                {entry.evidence.type} #{entry.evidence.id}
              </Muted>
            </Card>
          ))}
          {transcript.remote.data.entries.length === 0 ? <Muted>Nothing recorded yet.</Muted> : null}
        </>
      ) : null}
    </Screen>
  );
}
