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
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import { ArrowRight, MessageSquare, Sparkles } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

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
        <PageHeader eyebrow="Academia" title="Ask Nelavista" />
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
      <div className="nv-stack" aria-busy="true" aria-label="Loading Ask Nelavista">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (state.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia" title="Ask Nelavista" />
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
        title="Ask Nelavista"
        description="Answers come only from material in your enrolled courses. If it is not there, the answer says so instead of guessing."
        actions={
          <Button size="sm" type="button" variant="ghost" onClick={startNew}>
            New conversation
          </Button>
        }
      />

      <div className="nv-split">
        <div className="nv-stack">
          <Panel
            title="Conversation"
            actions={
              sessionId ? <Badge tone="neutral">Session #{sessionId}</Badge> : <Badge tone="info">New</Badge>
            }
          >
            {messages.length === 0 ? (
              <EmptyState
                body="Ask about a topic from one of your courses. The answer will name the material it came from."
                icon={MessageSquare}
                title="Nothing asked yet"
              />
            ) : (
              <ul className="nv-list nv-list--ruled">
                {messages.map((message) => (
                  <li key={message.id}>
                    <div className="nv-row nv-row--between">
                      <Badge tone={message.role === 'user' ? 'neutral' : 'info'}>
                        {message.role === 'user' ? 'You' : 'Nelavista'}
                      </Badge>
                      {message.declined ? (
                        <Badge status="declined" tone="warning">
                          Not in your material
                        </Badge>
                      ) : null}
                    </div>
                    <p style={{ whiteSpace: 'pre-line' }}>{message.content}</p>
                    {message.citations.length > 0 ? (
                      <div style={{ marginTop: 'var(--nv-space-sm)' }}>
                        <p className="nv-label">Where this came from</p>
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

            {error ? (
              <Banner tone="danger">
                <p>{error}</p>
              </Banner>
            ) : null}

            <form
              className="nv-row"
              style={{ alignItems: 'flex-end', marginTop: 'var(--nv-space-lg)' }}
              onSubmit={(event) => {
                event.preventDefault();
                void ask();
              }}
            >
              <div style={{ flex: 1, minWidth: 240 }}>
                <Field
                  hint="At least 5 characters. Up to 1,000."
                  id="ask-question"
                  label="Your question"
                  maxLength={1000}
                  placeholder="e.g. Why does quicksort degrade on sorted input?"
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                />
              </div>
              <Button disabled={busy} type="submit">
                <Sparkles aria-hidden="true" size={15} />
                {busy ? 'Thinking…' : 'Ask'}
              </Button>
            </form>
          </Panel>
        </div>

        <div className="nv-stack">
          <Panel title="Scope">
            <Select
              hint="Narrows the answer to one course."
              label="Course"
              options={[
                { value: '', label: 'Any of my courses' },
                ...courses.map((course) => ({
                  value: String(course.course_id),
                  label: `${course.code} — ${course.title}`,
                })),
              ]}
              value={courseId}
              onChange={(event) => setCourseId(event.target.value)}
            />
            {courses.length === 0 ? (
              <Banner tone="warning">
                <p>
                  You are not enrolled in a course yet, so there is nothing to ground an answer in.{' '}
                  <Link to="/onboarding">Finish setup</Link> first.
                </p>
              </Banner>
            ) : (
              <p className="nv-muted">
                {courses.length} course{courses.length === 1 ? '' : 's'} available to search.
              </p>
            )}
          </Panel>

          <Panel
            title="Recent conversations"
            actions={
              <Badge tone="neutral">
                {sessions.resource.status === 'ready' ? sessions.resource.data.sessions.length : '—'}
              </Badge>
            }
          >
            {sessions.resource.status === 'loading' ? <Skeleton lines={3} /> : null}
            {sessions.resource.status === 'error' ? (
              <ErrorState
                body={sessions.resource.message}
                action={
                  <Button size="sm" type="button" variant="secondary" onClick={sessions.reload}>
                    Try again
                  </Button>
                }
              />
            ) : null}
            {sessions.resource.status === 'ready' ? (
              sessions.resource.data.sessions.length === 0 ? (
                <EmptyState
                  body="Your first question creates a conversation here so you can return to it."
                  icon={MessageSquare}
                  title="No conversations yet"
                />
              ) : (
                <ul className="nv-list">
                  {sessions.resource.data.sessions.map((row) => (
                    <li key={row.id}>
                      <button
                        className="nv-button nv-button--ghost nv-button--sm"
                        type="button"
                        onClick={() => void openSession(row.id)}
                      >
                        {row.title ?? `Conversation #${row.id}`}
                        <ArrowRight aria-hidden="true" size={14} />
                      </button>
                      {row.course ? <span className="nv-muted"> · {row.course.code}</span> : null}
                    </li>
                  ))}
                </ul>
              )
            ) : null}
          </Panel>

          <p className="nv-muted">
            <Link to="/academia/materials">Open your materials</Link> · <Link to="/academia">Dashboard</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
