/**
 * Academia connected screens (B14).
 *
 * Materials, Ask Nelavista and CBT practice, in lockstep with the web screens.
 * Search is scoped to enrolled courses by the API; Ask declines instead of
 * guessing when nothing in the student's own material supports an answer; CBT is
 * practice only and never feeds verification.
 */
import type {
  AskAnswerOut,
  AskSessionListOut,
  AskSessionOut,
  CbtAnswerOut,
  CbtQuizOut,
  CbtResultsOut,
  MaterialDetailOut,
  MaterialListOut,
  MaterialSearchOut,
  OnboardingStateOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Pressable } from 'react-native';

import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { useApi } from '../lib/useApi';
import {
  Badge,
  Body,
  Button,
  Card,
  ErrorText,
  Field,
  H2,
  Loading,
  Muted,
  Note,
  Row,
  Screen,
} from '../ui';

export function AcademiaHome({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  return (
    <Screen title="Academia" onBack={() => navigate({ name: 'home' })}>
      <Card>
        <H2>Study materials</H2>
        <Muted>Notes, textbooks and past questions for your enrolled courses. Nothing outside them is searchable.</Muted>
        <Button label="Open materials" onPress={() => navigate({ name: 'materials' })} />
      </Card>
      <Card>
        <H2>Ask Nelavista</H2>
        <Muted>
          Answers come only from your course material. If it is not there, the answer says so instead of guessing.
        </Muted>
        <Button label="Ask a question" onPress={() => navigate({ name: 'ask' })} tone="ghost" />
      </Card>
      <Card>
        <H2>Practice (CBT)</H2>
        <Muted>Practice tells you what to work on next. It is never verification, and a wrong answer costs nothing.</Muted>
        <Button label="Start practice" onPress={() => navigate({ name: 'cbt' })} tone="ghost" />
      </Card>
    </Screen>
  );
}

export function MaterialsScreen({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const list = useApi<MaterialListOut>('/academia/materials');
  const [query, setQuery] = React.useState('');
  const [search, setSearch] = React.useState<MaterialSearchOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function runSearch(): Promise<void> {
    const cleaned = query.trim();
    if (cleaned.length < 2) {
      setError('Type at least two characters.');
      return;
    }
    setBusy(true);
    setError(null);
    try {
      setSearch(await api.get<MaterialSearchOut>(`/academia/materials/search?q=${encodeURIComponent(cleaned)}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not search your materials.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Study materials" onBack={() => navigate({ name: 'academia' })}>
      <Muted>
        Notes, textbooks and past questions for the courses you are enrolled in. Nothing outside them is searchable.
      </Muted>
      <Card>
        <Field
          label="Search your courses"
          onChangeText={setQuery}
          placeholder="e.g. recursion, deadlock, cell cycle"
          value={query}
        />
        <Button label={busy ? 'Searching…' : 'Search'} onPress={() => void runSearch()} disabled={busy} />
        <ErrorText message={error} />
      </Card>

      {list.remote.status === 'loading' ? <Loading /> : null}
      {list.remote.status === 'error' ? <ErrorText message={list.remote.message} /> : null}
      {list.remote.status === 'ready' ? (
        <>
          {search ? (
            <Card>
              <H2>Results for “{search.query}”</H2>
              {search.results.length === 0 ? (
                <Muted>Nothing in your enrolled courses matches that. Try a topic from the course outline.</Muted>
              ) : (
                search.results.map((row) => (
                  <Pressable
                    key={row.material_id}
                    onPress={() => navigate({ name: 'material', id: row.material_id })}
                  >
                    <Card>
                      <H2>{row.title}</H2>
                      <Muted>
                        {row.course?.code ?? 'Course'} · relevance {row.score}
                      </Muted>
                      <Body>{row.snippet}</Body>
                    </Card>
                  </Pressable>
                ))
              )}
            </Card>
          ) : null}

          {list.remote.data.materials.length === 0 ? (
            <Muted>No material yet for your courses. Ask Nelavista can only answer from material that exists.</Muted>
          ) : (
            list.remote.data.materials.map((material) => (
              <Pressable key={material.id} onPress={() => navigate({ name: 'material', id: material.id })}>
                <Card>
                  <H2>{material.title}</H2>
                  <Badge label={material.course?.code ?? 'course'} />
                  <Muted>
                    {material.course?.title ?? 'Course'} · {material.source ?? 'source not stated'}
                  </Muted>
                </Card>
              </Pressable>
            ))
          )}
        </>
      ) : null}
      <Button label="Ask about this material" onPress={() => navigate({ name: 'ask' })} tone="ghost" />
    </Screen>
  );
}

export function MaterialScreen({
  id,
  navigate,
}: {
  id: number;
  navigate: (route: Route) => void;
}): JSX.Element {
  const material = useApi<MaterialDetailOut>(`/academia/materials/${id}`);
  return (
    <Screen title="Material" onBack={() => navigate({ name: 'materials' })}>
      {material.remote.status === 'loading' ? <Loading /> : null}
      {material.remote.status === 'error' ? (
        <>
          <Muted>This material is not available to you: it may belong to a course you are not enrolled in.</Muted>
          <ErrorText message={material.remote.message} />
        </>
      ) : null}
      {material.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{material.remote.data.title}</H2>
            <Muted>
              {material.remote.data.course?.code ?? 'Course'} · {material.remote.data.course?.title ?? ''}
            </Muted>
          </Card>
          {material.remote.data.chunks.length === 0 ? (
            <Muted>This material has no readable text yet.</Muted>
          ) : (
            material.remote.data.chunks.map((chunk) => (
              <Card key={chunk.id}>
                <Body>{chunk.content}</Body>
              </Card>
            ))
          )}
          <Button label="Ask about this" onPress={() => navigate({ name: 'ask' })} tone="ghost" />
        </>
      ) : null}
    </Screen>
  );
}

export function AskScreen({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const state = useApi<OnboardingStateOut>('/onboarding/state');
  const sessions = useApi<AskSessionListOut>('/academia/ask/sessions');
  const [courseId, setCourseId] = React.useState<number | null>(null);
  const [sessionId, setSessionId] = React.useState<number | null>(null);
  const [messages, setMessages] = React.useState<AskSessionOut['messages']>([]);
  const [question, setQuestion] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const courses = state.remote.status === 'ready' ? state.remote.data.enrolments : [];

  async function openSession(id: number): Promise<void> {
    setError(null);
    try {
      const row = await api.get<AskSessionOut>(`/academia/ask/sessions/${id}`);
      setSessionId(row.id);
      setMessages(row.messages);
      setCourseId(row.course_id ?? null);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not open that conversation.');
    }
  }

  function startNew(): void {
    setSessionId(null);
    setMessages([]);
    setQuestion('');
    setError(null);
  }

  async function ask(): Promise<void> {
    const cleaned = question.trim();
    if (cleaned.length < 5) {
      setError('Ask a little more than that.');
      return;
    }
    setBusy(true);
    setError(null);
    // Optimistic user row; a failed call removes it again.
    setMessages((current) => [
      ...current,
      {
        id: -Date.now(),
        role: 'user',
        content: cleaned,
        citations: [],
        declined: false,
        created_at: new Date().toISOString(),
      },
    ]);
    setQuestion('');
    try {
      const answer = await api.post<AskAnswerOut>('/academia/ask', {
        question: cleaned,
        course_id: courseId,
        session_id: sessionId,
      });
      setSessionId(answer.session_id);
      setMessages((current) => [
        ...current,
        {
          id: -Date.now() + 1,
          role: 'assistant',
          content: answer.answer,
          citations: answer.citations,
          declined: answer.declined,
          created_at: new Date().toISOString(),
        },
      ]);
      sessions.reload();
    } catch (err) {
      setMessages((current) => current.slice(0, -1));
      setError(err instanceof ApiError ? err.message : 'Could not ask that question.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Ask Nelavista" onBack={() => navigate({ name: 'academia' })}>
      <Muted>
        Answers come only from material in your enrolled courses. If it is not there, the answer says so instead of
        guessing.
      </Muted>

      <Card>
        <H2>Course</H2>
        <Row>
          <Button
            label="Any of my courses"
            tone={courseId === null ? 'primary' : 'ghost'}
            onPress={() => setCourseId(null)}
          />
          {courses.map((course) => (
            <Button
              key={course.course_id}
              label={course.code}
              tone={courseId === course.course_id ? 'primary' : 'ghost'}
              onPress={() => setCourseId(course.course_id)}
            />
          ))}
        </Row>
        {courses.length === 0 ? <Muted>Finish course setup on the web first.</Muted> : null}
        <Button label="New conversation" onPress={startNew} tone="ghost" />
      </Card>

      {sessions.remote.status === 'ready' && sessions.remote.data.sessions.length > 0 ? (
        <Card>
          <H2>Recent conversations</H2>
          {sessions.remote.data.sessions.map((row) => (
            <Button
              key={row.id}
              label={`${row.title ?? `Conversation #${row.id}`}${row.course ? ` · ${row.course.code}` : ''}`}
              onPress={() => void openSession(row.id)}
              tone="ghost"
            />
          ))}
        </Card>
      ) : null}

      <Card>
        <H2>Conversation</H2>
        {messages.length === 0 ? <Muted>Ask about a topic from one of your courses.</Muted> : null}
        {messages.map((message) => (
          <Card key={message.id}>
            <Muted>{message.role === 'user' ? 'You' : 'Nelavista'}</Muted>
            <Body>{message.content}</Body>
            {message.declined ? <Badge label="not in your material" tone="warn" /> : null}
            {message.citations.map((citation) => (
              <Pressable
                key={citation.chunk_id}
                onPress={() => navigate({ name: 'material', id: citation.material_id })}
              >
                <Muted>
                  source: {citation.material_title} · {citation.course_code}
                </Muted>
              </Pressable>
            ))}
          </Card>
        ))}
        <Field
          label="Your question"
          onChangeText={setQuestion}
          placeholder="e.g. Why does quicksort degrade on sorted input?"
          value={question}
        />
        <ErrorText message={error} />
        <Button label={busy ? 'Thinking…' : 'Ask'} onPress={() => void ask()} disabled={busy} />
      </Card>

      <Button label="Open your materials" onPress={() => navigate({ name: 'materials' })} tone="ghost" />
      <Note message={state.remote.status === 'error' ? state.remote.message : null} />
    </Screen>
  );
}

export function CbtScreen({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const state = useApi<OnboardingStateOut>('/onboarding/state');
  const [courseId, setCourseId] = React.useState<number | null>(null);
  const [quiz, setQuiz] = React.useState<CbtQuizOut | null>(null);
  const [index, setIndex] = React.useState(0);
  const [answers, setAnswers] = React.useState<Record<number, CbtAnswerOut>>({});
  const [selected, setSelected] = React.useState<string | null>(null);
  const [results, setResults] = React.useState<CbtResultsOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const courses = state.remote.status === 'ready' ? state.remote.data.enrolments : [];
  const current = quiz?.questions[index] ?? null;
  const answered = current ? answers[current.id] : undefined;

  async function start(): Promise<void> {
    if (courseId === null) return;
    setBusy(true);
    setError(null);
    setResults(null);
    setAnswers({});
    setIndex(0);
    setSelected(null);
    try {
      setQuiz(await api.post<CbtQuizOut>('/academia/cbt/quiz', { course_id: courseId, count: 10 }));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not start practice.');
    } finally {
      setBusy(false);
    }
  }

  async function submitAnswer(): Promise<void> {
    if (!current || !selected) return;
    setBusy(true);
    setError(null);
    try {
      const answer = await api.post<CbtAnswerOut>('/academia/cbt/answer', {
        question_id: current.id,
        selected_key: selected,
        client_key: `cbt-${current.id}-${Date.now()}`,
      });
      setAnswers((rows) => ({ ...rows, [current.id]: answer }));
      setSelected(null);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save that answer.');
    } finally {
      setBusy(false);
    }
  }

  async function loadResults(): Promise<void> {
    if (courseId === null) return;
    setBusy(true);
    setError(null);
    try {
      setResults(await api.get<CbtResultsOut>(`/academia/cbt/results?course_id=${courseId}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load your results.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Practice (CBT)" onBack={() => navigate({ name: 'academia' })}>
      <Muted>Practice tells you what to work on next. It is never verification, and a wrong answer costs nothing.</Muted>

      <Card>
        <H2>Course</H2>
        <Row>
          {courses.map((course) => (
            <Button
              key={course.course_id}
              label={course.code}
              tone={courseId === course.course_id ? 'primary' : 'ghost'}
              onPress={() => {
                setCourseId(course.course_id);
                setQuiz(null);
                setResults(null);
              }}
            />
          ))}
        </Row>
        {courses.length === 0 ? <Muted>Finish course setup on the web first.</Muted> : null}
        <Button
          label={busy ? 'Starting…' : 'Start 10 questions'}
          onPress={() => void start()}
          disabled={busy || courseId === null}
        />
        <Button
          label="See my results"
          onPress={() => void loadResults()}
          disabled={busy || courseId === null}
          tone="ghost"
        />
        <ErrorText message={error} />
      </Card>

      {quiz && current ? (
        <Card>
          <Muted>
            Question {index + 1} of {quiz.count} · {quiz.course.code ?? 'course'}
          </Muted>
          <H2>{current.prompt}</H2>
          {answered ? (
            <>
              <Badge label={answered.is_correct ? 'Correct' : 'Not yet'} tone={answered.is_correct ? 'ok' : 'warn'} />
              {answered.correct_key ? <Muted>Correct option {answered.correct_key}</Muted> : null}
              {answered.explanation ? <Body>{answered.explanation}</Body> : null}
              <Button
                label={index + 1 < quiz.questions.length ? 'Next question' : 'Finish and see results'}
                onPress={() => {
                  if (index + 1 < quiz.questions.length) setIndex(index + 1);
                  else void loadResults();
                }}
              />
            </>
          ) : (
            <>
              {current.options.map((option) => {
                const key = String(option.key ?? '');
                return (
                  <Button
                    key={key}
                    label={`${selected === key ? '● ' : '○ '}${String(option.text ?? option.label ?? key)}`}
                    tone={selected === key ? 'primary' : 'ghost'}
                    onPress={() => setSelected(key)}
                  />
                );
              })}
              <Button
                label={busy ? 'Saving…' : 'Check answer'}
                onPress={() => void submitAnswer()}
                disabled={busy || !selected}
              />
            </>
          )}
        </Card>
      ) : null}

      {results ? (
        <Card>
          <H2>Your results</H2>
          {results.topics.length === 0 ? <Muted>No answers in this course yet.</Muted> : null}
          {results.topics.map((topic) => (
            <Card key={`${topic.topic_id ?? 'general'}-${topic.topic}`}>
              <H2>{topic.topic}</H2>
              <Muted>
                {topic.attempts} attempt(s) · {topic.accuracy}% accurate
              </Muted>
              <Badge
                label={topic.strength ? 'strength' : topic.weakness ? 'work on this' : 'in progress'}
                tone={topic.strength ? 'ok' : topic.weakness ? 'warn' : 'muted'}
              />
            </Card>
          ))}
          {results.recommendations.length > 0 ? (
            <>
              <H2>What to practise next</H2>
              {results.recommendations.map((row) => (
                <Muted key={`${row.topic_id ?? 'general'}-${row.topic}`}>
                  {row.topic} · {row.accuracy}% — {row.action === 'practise' ? 'practise more' : row.action}
                </Muted>
              ))}
            </>
          ) : null}
        </Card>
      ) : null}

      <Button label="Read the material" onPress={() => navigate({ name: 'materials' })} tone="ghost" />
    </Screen>
  );
}
