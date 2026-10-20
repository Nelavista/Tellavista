/**
 * CBT practice and results (B14).
 *
 * Practice is feedback, not proof: answers are stored on `question_attempts`,
 * which no verification rule reads. The results panel is what feeds the
 * dashboard's strengths and weaknesses, so it names the topic and the next action
 * rather than only a score.
 */
import type {
  CbtAnswerOut,
  CbtQuizOut,
  CbtResultsOut,
  OnboardingStateOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

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
        <h1 className="nv-h1">Practice (CBT)</h1>
        <p className="nv-banner">Academia is not switched on for this environment yet.</p>
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

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Practice (CBT)</h1>
      <p className="nv-muted">
        Practice tells you what to work on next. It is never verification, and a wrong answer here costs
        nothing.
      </p>

      <section className="nv-card">
        <div className="nv-row">
          <div style={{ minWidth: 280 }}>
            <label className="nv-label" htmlFor="cbt-course">Course</label>
            <select
              className="nv-select"
              id="cbt-course"
              value={courseId}
              onChange={(event) => {
                setCourseId(event.target.value);
                setQuiz(null);
                setResults(null);
              }}
            >
              <option value="">Select a course…</option>
              {courses.map((course) => (
                <option key={course.course_id} value={course.course_id}>
                  {course.code} — {course.title}
                </option>
              ))}
            </select>
          </div>
          <button className="nv-button" disabled={busy || !courseId} type="button" onClick={() => void start()}>
            Start 10 questions
          </button>
          <button
            className="nv-button nv-button--ghost"
            disabled={busy || !courseId}
            type="button"
            onClick={() => void loadResults()}
          >
            See my results
          </button>
        </div>
        {courses.length === 0 ? (
          <p className="nv-muted">
            You are not enrolled in a course yet. <Link to="/onboarding">Finish setup</Link> first.
          </p>
        ) : null}
        <ErrorNote message={error} />
      </section>

      {quiz && current ? (
        <section className="nv-card">
          <p className="nv-muted">
            Question {index + 1} of {quiz.count} · {quiz.course.code ?? 'course'}
          </p>
          <h2 className="nv-h2">{current.prompt}</h2>
          {answered ? (
            <div>
              <p>
                <strong>{answered.is_correct ? 'Correct' : 'Not yet'}</strong>
                {answered.correct_key ? (
                  <span className="nv-muted"> · correct option {answered.correct_key}</span>
                ) : null}
              </p>
              {answered.explanation ? <p>{answered.explanation}</p> : null}
              <button
                className="nv-button"
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
              </button>
            </div>
          ) : (
            <div>
              <ul className="nv-list">
                {current.options.map((option) => {
                  const key = String(option.key ?? '');
                  return (
                    <li key={key}>
                      <label className="nv-check">
                        <input
                          type="radio"
                          name="cbt-option"
                          checked={selected === key}
                          value={key}
                          onChange={() => setSelected(key)}
                        />
                        {String(option.text ?? option.label ?? key)}
                      </label>
                    </li>
                  );
                })}
              </ul>
              <button
                className="nv-button"
                disabled={busy || !selected}
                type="button"
                onClick={() => void submitAnswer()}
              >
                {busy ? 'Saving…' : 'Check answer'}
              </button>
            </div>
          )}
        </section>
      ) : null}

      {results ? (
        <section className="nv-card">
          <h2 className="nv-h2">Your results</h2>
          {results.topics.length === 0 ? (
            <p className="nv-muted">No answers in this course yet.</p>
          ) : (
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
                    <td>{topic.attempts}</td>
                    <td>{topic.accuracy}%</td>
                    <td>
                      {topic.strength ? 'strength' : topic.weakness ? 'work on this' : 'in progress'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {results.recommendations.length > 0 ? (
            <>
              <h3 className="nv-h2">What to practise next</h3>
              <ul className="nv-list">
                {results.recommendations.map((row) => (
                  <li key={`${row.topic_id ?? 'general'}-${row.topic}`}>
                    {row.topic} · {row.accuracy}% — {row.action === 'practise' ? 'practise more' : row.action}
                  </li>
                ))}
              </ul>
            </>
          ) : null}
        </section>
      ) : null}

      <p className="nv-muted">
        <Link to="/academia/materials">Read the material</Link> · <Link to="/academia/ask">Ask a question</Link> ·{' '}
        <Link to="/academia">Dashboard</Link>
      </p>
    </div>
  );
}
