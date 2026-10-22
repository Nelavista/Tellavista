/**
 * Ask Nelavista (B14).
 *
 * Course-aware and material-grounded. When nothing in the student's own material
 * supports an answer the API declines, and this screen shows that refusal as a
 * normal answer rather than an error: guessing would be worse than saying so.
 *
 * Every answer shows the chunks it was built from, linked to the reader.
 */
import type {
  AskAnswerOut,
  AskSessionListOut,
  AskSessionOut,
  OnboardingStateOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { ErrorNote } from '../ui';

export function AskNelavista(): JSX.Element {
  const state = useApiResource<OnboardingStateOut>('/onboarding/state');
  const sessions = useApiResource<AskSessionListOut>('/academia/ask/sessions');
  const [courseId, setCourseId] = React.useState('');
  const [sessionId, setSessionId] = React.useState<number | null>(null);
  const [messages, setMessages] = React.useState<AskSessionOut['messages']>([]);
  const [question, setQuestion] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function openSession(id: number): Promise<void> {
    setError(null);
    try {
      const row = await http.get<AskSessionOut>(`/academia/ask/sessions/${id}`);
      setSessionId(row.id);
      setMessages(row.messages);
      setCourseId(row.course_id ? String(row.course_id) : '');
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
    // Optimistic user row: the answer is what matters, and a failed call removes it.
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
      const answer = await http.post<AskAnswerOut>('/academia/ask', {
        question: cleaned,
        course_id: courseId ? Number(courseId) : null,
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

  const courses = state.resource.status === 'ready' ? state.resource.data.enrolments : [];

  if (state.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Ask Nelavista</h1>
        <p className="nv-banner">Academia is not switched on for this environment yet.</p>
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Ask Nelavista</h1>
      <p className="nv-muted">
        Answers come only from material in your enrolled courses. If it is not there, the answer says so
        instead of guessing.
      </p>

      <section className="nv-card">
        <div className="nv-row">
          <div style={{ minWidth: 260 }}>
            <label className="nv-label" htmlFor="ask-course">Course</label>
            <select
              className="nv-select"
              id="ask-course"
              value={courseId}
              onChange={(event) => setCourseId(event.target.value)}
            >
              <option value="">Any of my courses</option>
              {courses.map((course) => (
                <option key={course.course_id} value={course.course_id}>
                  {course.code} — {course.title}
                </option>
              ))}
            </select>
          </div>
          <button className="nv-button nv-button--ghost" type="button" onClick={startNew}>
            New conversation
          </button>
        </div>
        {courses.length === 0 ? (
          <p className="nv-muted">
            You are not enrolled in a course yet. <Link to="/onboarding">Finish setup</Link> first.
          </p>
        ) : null}
      </section>

      {sessions.resource.status === 'ready' && sessions.resource.data.sessions.length > 0 ? (
        <section className="nv-card">
          <h2 className="nv-h2">Recent conversations</h2>
          <ul className="nv-list">
            {sessions.resource.data.sessions.map((row) => (
              <li key={row.id}>
                <button
                  className="nv-button nv-button--ghost"
                  type="button"
                  onClick={() => void openSession(row.id)}
                >
                  {row.title ?? `Conversation #${row.id}`}
                </button>
                {row.course ? <span className="nv-muted"> · {row.course.code}</span> : null}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section className="nv-card">
        <h2 className="nv-h2">Conversation</h2>
        {messages.length === 0 ? (
          <p className="nv-muted">Ask about a topic from one of your courses.</p>
        ) : (
          <ul className="nv-list">
            {messages.map((message) => (
              <li className="nv-card" key={message.id}>
                <p className="nv-muted">{message.role === 'user' ? 'You' : 'Nelavista'}</p>
                <p style={{ whiteSpace: 'pre-line' }}>{message.content}</p>
                {message.declined ? (
                  <p className="nv-tag" data-tone="warn">not in your material</p>
                ) : null}
                {message.citations.length > 0 ? (
                  <div>
                    <p className="nv-muted">Where this came from</p>
                    <ul className="nv-list">
                      {message.citations.map((citation) => (
                        <li key={citation.chunk_id}>
                          <Link to={`/academia/materials/${citation.material_id}`}>
                            {citation.material_title}
                          </Link>
                          <span className="nv-muted"> · {citation.course_code}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </li>
            ))}
          </ul>
        )}
        <ErrorNote message={error} />
        <form
          className="nv-row"
          onSubmit={(event) => {
            event.preventDefault();
            void ask();
          }}
        >
          <div style={{ flex: 1, minWidth: 240 }}>
            <label className="nv-label" htmlFor="ask-question">Your question</label>
            <input
              className="nv-input"
              id="ask-question"
              maxLength={1000}
              placeholder="e.g. Why does quicksort degrade on sorted input?"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
            />
          </div>
          <button className="nv-button" disabled={busy} type="submit">
            {busy ? 'Thinking…' : 'Ask'}
          </button>
        </form>
      </section>

      <p className="nv-muted">
        <Link to="/academia/materials">Open your materials</Link> · <Link to="/academia">Dashboard</Link>
      </p>
    </div>
  );
}
