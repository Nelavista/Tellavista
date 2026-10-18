/**
 * Academia dashboard (B4): the five questions from PRD §8, answered with data.
 *
 * The API already words every answer, including empty states, so this page never
 * invents a generic prompt: if a section has no data the answer text explains
 * what would put something there. The page only decides how to lay it out.
 */
import type {
  AcademiaDashboard as Dashboard,
  NextAction,
  PracticeItem,
  TopicStat,
} from '@nelavista/contracts';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { ErrorNote, Skeleton } from '../ui';

type LoadState = 'loading' | 'ready' | 'unavailable' | 'error';

function whenLabel(value: string | null): string | null {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toLocaleDateString(undefined, { day: 'numeric', month: 'short' });
}

function accuracyLabel(value: number | null): string {
  return value === null ? 'not attempted' : `${value}% correct`;
}

function ActionCard({ action }: { action: NextAction }): JSX.Element {
  return (
    <section className="nv-action" aria-labelledby="nv-next-action">
      <p className="nv-label" id="nv-next-action">
        One thing to do next
      </p>
      <p className="nv-action__label">{action.label}</p>
      <p className="nv-muted">{action.reason}</p>
    </section>
  );
}

function TopicList({ items, empty }: { items: Array<PracticeItem | TopicStat>; empty: string }): JSX.Element {
  if (items.length === 0) return <p className="nv-muted">{empty}</p>;
  return (
    <ul className="nv-list">
      {items.map((item) => (
        <li className="nv-row nv-row--between" key={`${item.topic_id ?? 'general'}-${item.topic}`}>
          <span>{item.topic}</span>
          <span className="nv-muted">{accuracyLabel(item.accuracy)}</span>
        </li>
      ))}
    </ul>
  );
}

export function AcademiaDashboard(): JSX.Element {
  const [state, setState] = React.useState<LoadState>('loading');
  const [data, setData] = React.useState<Dashboard | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [attempt, setAttempt] = React.useState(0);

  React.useEffect(() => {
    let cancelled = false;
    setState('loading');
    setError(null);
    void (async () => {
      try {
        const dashboard = await http.get<Dashboard>('/academia/dashboard');
        if (cancelled) return;
        setData(dashboard);
        setState('ready');
      } catch (err) {
        if (cancelled) return;
        // The whole router is behind FLAG_ACADEMIA_CONNECT. A 404 here means the
        // feature is off in this environment, not that the student did anything
        // wrong, so say so instead of showing a scary error.
        if (err instanceof ApiError && err.status === 404) {
          setState('unavailable');
          return;
        }
        setState('error');
        setError(err instanceof ApiError ? err.message : 'Could not load your dashboard.');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [attempt]);

  if (state === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your dashboard">
        <Skeleton height="2rem" width="60%" />
        <Skeleton lines={3} />
        <Skeleton lines={2} />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (state === 'unavailable') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Academia dashboard</h1>
        <p className="nv-banner">
          Academia is not switched on for this environment yet. Your account, courses and path are unaffected.
        </p>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Academia dashboard</h1>
        <ErrorNote message={error} />
        <button className="nv-button" type="button" onClick={() => setAttempt((n) => n + 1)}>
          Try again
        </button>
      </div>
    );
  }

  if (!data) return <p className="nv-muted">Nothing to show yet.</p>;

  const questions = data.questions;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Academia dashboard</h1>

      <ActionCard action={questions.what_should_i_do_next.action} />

      <section className="nv-card" aria-labelledby="nv-q-studying">
        <h2 className="nv-h2" id="nv-q-studying">
          What am I studying?
        </h2>
        <p>{questions.what_am_i_studying.answer}</p>
        {questions.what_am_i_studying.courses.length > 0 ? (
          <ul className="nv-list">
            {questions.what_am_i_studying.courses.map((course) => (
              <li key={course.enrolment_id}>
                <strong>{course.code}</strong> — {course.title}
                <div className="nv-muted">
                  {course.department} · {course.faculty} · {course.university}
                </div>
                {data.materials_by_course[String(course.course_id)] ? (
                  <div className="nv-muted">
                    {data.materials_by_course[String(course.course_id)]} material(s) available
                  </div>
                ) : null}
              </li>
            ))}
          </ul>
        ) : (
          <p className="nv-muted">
            <Link to="/onboarding">Add your courses</Link>
          </p>
        )}
      </section>

      <section className="nv-card" aria-labelledby="nv-q-recent">
        <h2 className="nv-h2" id="nv-q-recent">
          What did I study recently?
        </h2>
        <p>{questions.what_did_i_study_recently.answer}</p>
        {questions.what_did_i_study_recently.items.length > 0 ? (
          <ul className="nv-list">
            {questions.what_did_i_study_recently.items.map((item) => {
              const label = whenLabel(item.when);
              return (
                <li className="nv-row nv-row--between" key={`${item.kind}-${item.title}`}>
                  <span>
                    {item.title}
                    <span className="nv-muted">
                      {item.kind === 'lesson_completed' ? ' · completed' : ' · in progress'}
                    </span>
                  </span>
                  {label && item.when ? (
                    <time className="nv-muted" dateTime={item.when}>
                      {label}
                    </time>
                  ) : null}
                </li>
              );
            })}
          </ul>
        ) : null}
      </section>

      <section className="nv-card" aria-labelledby="nv-q-practise">
        <h2 className="nv-h2" id="nv-q-practise">
          What should I practise?
        </h2>
        <p>{questions.what_should_i_practise.answer}</p>
        <TopicList
          items={questions.what_should_i_practise.items}
          empty="Nothing to practise yet — your courses do not have practice questions loaded."
        />
      </section>

      <section className="nv-card" aria-labelledby="nv-q-weak">
        <h2 className="nv-h2" id="nv-q-weak">
          Where am I weak?
        </h2>
        <p>{questions.where_am_i_weak.answer}</p>
        <TopicList
          items={questions.where_am_i_weak.items}
          empty="No weak topics right now. This fills in as you answer practice questions."
        />
      </section>

      <button className="nv-button nv-button--ghost" type="button" onClick={() => setAttempt((n) => n + 1)}>
        Refresh
      </button>
    </div>
  );
}
