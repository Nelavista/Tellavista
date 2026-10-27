/**
 * CBT practice and results (B14).
 *
 * Practice is feedback, not proof: answers are stored on `question_attempts`,
 * which no verification rule reads. The results panel is what feeds the
 * dashboard's strengths and weaknesses, so it names the topic and the next action
 * rather than only a score.
 */
import type { CbtAnswerOut, CbtQuizOut, CbtResultsOut, OnboardingStateOut } from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import { ArrowRight, ClipboardCheck } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

export function Cbt(): JSX.Element {
  const state = useApiResource<OnboardingStateOut>('/onboarding/state');
  const [courseId, setCourseId] = React.useState('');
  const [quiz, setQuiz] = React.useState<CbtQuizOut | null>(null);
  const [index, setIndex] = React.useState(0);
  const [answers, setAnswers] = React.useState<Record<number, CbtAnswerOut>>({});
  const [selected, setSelected] = React.useState<string | null>(null);
  const [results, setResults] = React.useState<CbtResultsOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const courses = state.resource.status === 'ready' ? state.resource.data.enrolments : [];
  const current = quiz?.questions[index] ?? null;
  const answered = current ? answers[current.id] : undefined;

  async function start(): Promise<void> {
    if (!courseId) return;
    setBusy(true);
    setError(null);
    setResults(null);
    setAnswers({});
    setIndex(0);
    setSelected(null);
    try {
      setQuiz(await http.post<CbtQuizOut>('/academia/cbt/quiz', { course_id: Number(courseId), count: 10 }));
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
      const answer = await http.post<CbtAnswerOut>('/academia/cbt/answer', {
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
    if (!courseId) return;
    setBusy(true);
    setError(null);
    try {
      setResults(await http.get<CbtResultsOut>(`/academia/cbt/results?course_id=${courseId}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load your results.');
    } finally {
      setBusy(false);
    }
  }

  if (state.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia" title="Practice (CBT)" />
        <Banner tone="info">
          <p>Academia is not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (state.resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading practice">
        <Skeleton height="2rem" width="35%" />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (state.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia" title="Practice (CBT)" />
        <ErrorState
          body={state.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={state.reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Academia"
        title="Practice (CBT)"
        description="Practice tells you what to work on next. It is never verification, and a wrong answer here costs nothing."
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/cbt/history">
              History
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/academia/materials">
              Materials
            </Link>
          </>
        }
      />

      <Panel title="Start a paper">
        <div className="nv-row" style={{ alignItems: 'flex-end' }}>
          <div style={{ minWidth: 280, flex: 1 }}>
            <Select
              label="Course"
              options={[
                { value: '', label: 'Select a course…' },
                ...courses.map((course) => ({
                  value: String(course.course_id),
                  label: `${course.code} — ${course.title}`,
                })),
              ]}
              value={courseId}
              onChange={(event) => {
                setCourseId(event.target.value);
                setQuiz(null);
                setResults(null);
              }}
            />
          </div>
          <Button disabled={busy || !courseId} type="button" onClick={() => void start()}>
            <ClipboardCheck aria-hidden="true" size={15} />
            Start 10 questions
          </Button>
          <Button
            disabled={busy || !courseId}
            type="button"
            variant="ghost"
            onClick={() => void loadResults()}
          >
            See my results
          </Button>
        </div>
        {courses.length === 0 ? (
          <Banner
            tone="warning"
            actions={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/onboarding">
                Finish setup
              </Link>
            }
          >
            <p>You are not enrolled in a course yet, so there are no questions to practise.</p>
          </Banner>
        ) : null}
        {error ? (
          <Banner tone="danger">
            <p>{error}</p>
          </Banner>
        ) : null}
      </Panel>

      {quiz && current ? (
        <Panel
          title={`Question ${index + 1} of ${quiz.count}`}
          actions={<Badge tone="neutral">{quiz.course.code ?? 'course'}</Badge>}
        >
          <div className="nv-stack" aria-live="polite">
            <h2 className="nv-h2">{current.prompt}</h2>
            {answered ? (
              <div className="nv-stack">
                <Banner tone={answered.is_correct ? 'success' : 'warning'}>
                  <p>
                    <strong>{answered.is_correct ? 'Correct' : 'Not yet'}</strong>
                    {answered.correct_key ? (
                      <span className="nv-muted"> · correct option {answered.correct_key}</span>
                    ) : null}
                  </p>
                  {answered.explanation ? <p>{answered.explanation}</p> : null}
                </Banner>
                <div>
                  <Button
                    type="button"
                    onClick={() => {
                      if (index + 1 < quiz.questions.length) {
                        setIndex(index + 1);
                      } else {
                        void loadResults();
                      }
                    }}
                  >
                    {index + 1 < quiz.questions.length ? 'Next question' : 'Finish and see results'}
                    <ArrowRight aria-hidden="true" size={15} />
                  </Button>
                </div>
              </div>
            ) : (
              <div className="nv-stack">
                <ul className="nv-list">
                  {current.options.map((option) => {
                    const key = String(option.key ?? '');
                    return (
                      <li key={key}>
                        <label className="nv-check">
                          <input
                            checked={selected === key}
                            name="cbt-option"
                            type="radio"
                            value={key}
                            onChange={() => setSelected(key)}
                          />
                          {String(option.text ?? option.label ?? key)}
                        </label>
                      </li>
                    );
                  })}
                </ul>
                <div>
                  <Button disabled={busy || !selected} type="button" onClick={() => void submitAnswer()}>
                    {busy ? 'Saving…' : 'Check answer'}
                  </Button>
                </div>
              </div>
            )}
          </div>
        </Panel>
      ) : null}

      {results ? (
        <Panel title="Your results" actions={<Badge tone="info">{results.topics.length} topics</Badge>}>
          {results.topics.length === 0 ? (
            <EmptyState
              body="Answer a few questions and this table fills in with the topics you should revise."
              icon={ClipboardCheck}
              title="No answers in this course yet"
            />
          ) : (
            <div className="nv-table-wrap">
              <table className="nv-table">
                <thead>
                  <tr>
                    <th>Topic</th>
                    <th>Attempts</th>
                    <th>Accuracy</th>
                    <th>Verdict</th>
                  </tr>
                </thead>
                <tbody>
                  {results.topics.map((topic) => (
                    <tr key={`${topic.topic_id ?? 'general'}-${topic.topic}`}>
                      <td>{topic.topic}</td>
                      <td className="nv-num">{topic.attempts}</td>
                      <td className="nv-num">{topic.accuracy}%</td>
                      <td>
                        <Badge tone={topic.strength ? 'success' : topic.weakness ? 'warning' : 'neutral'}>
                          {topic.strength ? 'Strength' : topic.weakness ? 'Work on this' : 'In progress'}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {results.recommendations.length > 0 ? (
            <div style={{ marginTop: 'var(--nv-space-xl)' }}>
              <h3 className="nv-h3">What to practise next</h3>
              <ul className="nv-list">
                {results.recommendations.map((row) => (
                  <li key={`${row.topic_id ?? 'general'}-${row.topic}`}>
                    {row.topic} · {row.accuracy}% — {row.action === 'practise' ? 'practise more' : row.action}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </Panel>
      ) : null}

      <p className="nv-muted">
        <Link to="/academia/materials">Read the material</Link> ·{' '}
        <Link to="/academia/ask">Ask a question</Link> · <Link to="/academia">Dashboard</Link>
      </p>
    </div>
  );
}
