import type {
  LessonCompletedOut,
  LessonOut,
  PathOut,
  PracticeBriefOut,
  PracticeResultOut,
  SkillDetailOut,
  SkillsOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Pressable } from 'react-native';

import { TaskControl, type TaskValue } from '../components/TaskControl';
import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { answerFor, controlFor } from '../lib/taskForm';
import { useApi } from '../lib/useApi';
import { Body, Button, Card, ErrorText, H2, Loading, Muted, Note, Screen } from '../ui';

export function Skills({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const skills = useApi<SkillsOut>('/skills');
  return (
    <Screen title="Skills" onBack={() => navigate({ name: 'home' })}>
      {skills.remote.status === 'loading' ? <Loading /> : null}
      {skills.remote.status === 'error' ? <ErrorText message={skills.remote.message} /> : null}
      {skills.remote.status === 'ready' ? (
        skills.remote.data.skills.map((skill) => (
          <Pressable key={skill.id} onPress={() => navigate({ name: 'skill', slug: skill.slug })}>
            <Card>
              <H2>{skill.name}</H2>
              {skill.description ? <Muted>{skill.description}</Muted> : null}
              <Muted>
                {skill.published_paths} published path{skill.published_paths === 1 ? '' : 's'}
              </Muted>
            </Card>
          </Pressable>
        ))
      ) : null}
    </Screen>
  );
}

export function SkillDetail({
  slug,
  navigate,
}: {
  slug: string;
  navigate: (route: Route) => void;
}): JSX.Element {
  const skill = useApi<SkillDetailOut>(`/skills/${slug}`);
  return (
    <Screen title="Skill" onBack={() => navigate({ name: 'skills' })}>
      {skill.remote.status === 'loading' ? <Loading /> : null}
      {skill.remote.status === 'error' ? <ErrorText message={skill.remote.message} /> : null}
      {skill.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{skill.remote.data.name}</H2>
            {skill.remote.data.description ? <Body>{skill.remote.data.description}</Body> : null}
          </Card>
          {skill.remote.data.paths.map((path) => (
            <Pressable key={path.id} onPress={() => navigate({ name: 'path', slug: path.slug })}>
              <Card>
                <H2>{path.title}</H2>
                <Muted>
                  {path.level}
                  {path.estimated_hours ? ` · about ${path.estimated_hours} hour(s)` : ''}
                </Muted>
                {path.summary ? <Muted>{path.summary}</Muted> : null}
              </Card>
            </Pressable>
          ))}
          {skill.remote.data.paths.length === 0 ? (
            <Muted>No published learning path for this skill yet.</Muted>
          ) : null}
        </>
      ) : null}
    </Screen>
  );
}

export function PathScreen({
  slug,
  navigate,
}: {
  slug: string;
  navigate: (route: Route) => void;
}): JSX.Element {
  const path = useApi<PathOut>(`/skills/paths/${slug}`);
  return (
    <Screen title="Learning path" onBack={() => navigate({ name: 'skills' })}>
      {path.remote.status === 'loading' ? <Loading /> : null}
      {path.remote.status === 'error' ? <ErrorText message={path.remote.message} /> : null}
      {path.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{path.remote.data.title}</H2>
            <Muted>
              {path.remote.data.completed_steps} of {path.remote.data.required_steps} required steps ·{' '}
              {path.remote.data.percent_complete}%
            </Muted>
          </Card>
          {path.remote.data.steps.map((step) => (
            <Card key={step.id}>
              <H2>
                {step.ordinal}. {step.title ?? step.kind}
              </H2>
              <Muted>
                {step.kind} · {step.completed ? 'complete' : step.unlocked ? 'open' : 'locked'}
              </Muted>
              {step.unlocked && step.lesson_slug ? (
                <Button
                  label={step.completed ? 'Read again' : 'Open lesson'}
                  onPress={() => navigate({ name: 'lesson', slug: step.lesson_slug as string })}
                />
              ) : null}
              {step.unlocked && step.task_template_id ? (
                <Button
                  label="Practise"
                  onPress={() => navigate({ name: 'practice', id: step.task_template_id as number })}
                  tone="ghost"
                />
              ) : null}
            </Card>
          ))}
        </>
      ) : null}
    </Screen>
  );
}

export function LessonScreen({
  slug,
  navigate,
}: {
  slug: string;
  navigate: (route: Route) => void;
}): JSX.Element {
  const lesson = useApi<LessonOut>(`/skills/lessons/${slug}`);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  async function complete(): Promise<void> {
    if (lesson.remote.status !== 'ready') return;
    setBusy(true);
    setError(null);
    try {
      const result = await api.post<LessonCompletedOut>(
        `/skills/lessons/${lesson.remote.data.id}/complete`,
      );
      setNote(result.note);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your progress.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Lesson" onBack={() => navigate({ name: 'skills' })}>
      {lesson.remote.status === 'loading' ? <Loading /> : null}
      {lesson.remote.status === 'error' ? <ErrorText message={lesson.remote.message} /> : null}
      {lesson.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{lesson.remote.data.title}</H2>
            {lesson.remote.data.body_md
              .split(/\n{2,}/)
              .filter((block) => block.trim())
              .map((block, index) => (
                <Body key={index}>{block.replace(/[#*`>]/g, '').trim()}</Body>
              ))}
          </Card>
          <Note message={note} />
          <ErrorText message={error} />
          <Button label={busy ? 'Saving…' : 'Mark complete'} onPress={() => void complete()} disabled={busy} />
          <Muted>Completing a lesson is progress, not proof of the skill.</Muted>
        </>
      ) : null}
    </Screen>
  );
}

export function PracticeScreen({
  templateId,
  navigate,
}: {
  templateId: number;
  navigate: (route: Route) => void;
}): JSX.Element {
  const brief = useApi<PracticeBriefOut>(`/skills/tasks/${templateId}`);
  const [value, setValue] = React.useState<TaskValue>(null);
  const [result, setResult] = React.useState<PracticeResultOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  const control =
    brief.remote.status === 'ready'
      ? controlFor(brief.remote.data.input_schema, brief.remote.data.answer_schema)
      : { kind: 'unsupported' as const, reason: 'Loading…' };
  const answer = answerFor(control, value);

  async function submit(): Promise<void> {
    if (!answer) return;
    setBusy(true);
    setError(null);
    try {
      setResult(
        await api.post<PracticeResultOut>(`/skills/tasks/${templateId}/practice`, { answer }),
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not check that answer.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Practice" onBack={() => navigate({ name: 'skills' })}>
      {brief.remote.status === 'loading' ? <Loading /> : null}
      {brief.remote.status === 'error' ? <ErrorText message={brief.remote.message} /> : null}
      {brief.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{brief.remote.data.name}</H2>
            <Muted>{brief.remote.data.instructions_md}</Muted>
            <TaskControl control={control} value={value} onChange={setValue} />
          </Card>
          {result ? (
            <Card>
              <H2>{result.is_correct ? 'Correct' : 'Not yet'}</H2>
              <Body>{result.feedback}</Body>
              <Muted>Practice is feedback, never verification.</Muted>
            </Card>
          ) : null}
          <ErrorText message={error} />
          <Button
            disabled={busy || !answer}
            label={busy ? 'Checking…' : 'Check my answer'}
            onPress={() => void submit()}
          />
        </>
      ) : null}
    </Screen>
  );
}

