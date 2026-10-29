/**
 * Academia dashboard (B4): the five questions from PRD §8, answered with data.
 *
 * The API already words every answer, including empty states, so this page never
 * invents a generic prompt: if a section has no data the answer text explains
 * what would put something there. The page only decides how to lay it out.
 */
import type { DashboardOut, NextActionOut, PracticeItemOut, TopicStatOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowRight, BookOpen, ClipboardCheck, GraduationCap, Sparkles } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';

type LoadState = 'loading' | 'ready' | 'unavailable' | 'error';

function whenLabel(value: string | null | undefined): string | null {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toLocaleDateString(undefined, { day: 'numeric', month: 'short' });
}

function accuracyLabel(value: number | null | undefined): string {
  return value === null ? 'not attempted' : `${value}% correct`;
}

function actionHref(action: NextActionOut): string {
  if (action.material_id) return `/academia/materials/${action.material_id}`;
  if (action.lesson_id) return '/skills/my-learning';
  if (action.topic_id) return '/academia/cbt';
  return '/academia';
}

function ActionBlock({ action }: { action: NextActionOut }): JSX.Element {
  return (
    <section className="nv-action" aria-labelledby="nv-next-action">
      <p className="nv-label" id="nv-next-action">
        One thing to do next
      </p>
      <p className="nv-action__label">{action.label}</p>
      <p className="nv-muted">{action.reason}</p>
      <div className="nv-row">
        <Link className="nv-button" to={actionHref(action)}>
          Start this
          <ArrowRight aria-hidden="true" size={15} />
        </Link>
        <Link className="nv-button nv-button--ghost" to="/academia/cbt">
          Practise instead
        </Link>
      </div>
    </section>
  );
}

function TopicList({
  items,
  empty,
}: {
  items: Array<PracticeItemOut | TopicStatOut>;
  empty: string;
}): JSX.Element {
  if (items.length === 0) return <EmptyState body={empty} icon={Sparkles} title="Nothing to rank yet" />;
  return (
    <ul className="nv-list nv-list--ruled">
      {items.map((item) => (
        <li className="nv-row nv-row--between" key={`${item.topic_id ?? 'general'}-${item.topic}`}>
          <span>{item.topic}</span>
          <span className="nv-mono">{accuracyLabel(item.accuracy)}</span>
        </li>
      ))}
    </ul>
  );
}

export function AcademiaDashboard(): JSX.Element {
  const [state, setState] = React.useState<LoadState>('loading');
  const [data, setData] = React.useState<DashboardOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [attempt, setAttempt] = React.useState(0);

  React.useEffect(() => {
    let cancelled = false;
    setState('loading');
    setError(null);
    void (async () => {
      try {
        const dashboard = await http.get<DashboardOut>('/academia/dashboard');
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
        <PageHeader eyebrow="Academia" title="Academia dashboard" />
        <Banner tone="info">
          <p>
            Academia is not switched on for this environment yet. Your account, courses and path are
            unaffected.
          </p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia" title="Academia dashboard" />
        <ErrorState
          body={error ?? undefined}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={() => setAttempt((n) => n + 1)}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia" title="Academia dashboard" />
        <EmptyState
          body="The dashboard returned no questions. Refresh to try again."
          icon={GraduationCap}
          title="Nothing to show yet"
        />
      </div>
    );
  }

  const questions = data.questions;
  const courses = questions.what_am_i_studying.courses;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Academia"
        title="Academia dashboard"
        description="What you are studying, what you studied recently, what to practise, and where you are weak."
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/materials">
              <BookOpen aria-hidden="true" size={15} />
              Materials
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/academia/ask">
              <Sparkles aria-hidden="true" size={15} />
              Ask
            </Link>
          </>
        }
      />

      <ActionBlock action={questions.what_should_i_do_next.action} />

      <Panel title="What am I studying?" actions={<Badge tone="info">{data.enrolment_count} courses</Badge>}>
        <p>{questions.what_am_i_studying.answer}</p>
        {courses.length === 0 ? (
          <EmptyState
            body="Your courses decide which materials, practice and CBT papers are available."
            icon={BookOpen}
            title="No courses yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/onboarding">
                Add your courses
              </Link>
            }
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Course</th>
                  <th>Department</th>
                  <th>Materials</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((course) => (
                  <tr key={course.enrolment_id}>
                    <td className="nv-mono">{course.code}</td>
                    <td>{course.title}</td>
                    <td>
                      {course.department}
                      <div className="nv-muted">{course.faculty}</div>
                    </td>
                    <td className="nv-num">{data.materials_by_course[String(course.course_id)] ?? 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <div className="nv-split">
        <Panel title="What did I study recently?">
          <p>{questions.what_did_i_study_recently.answer}</p>
          {questions.what_did_i_study_recently.items.length === 0 ? (
            <EmptyState
              body="Open a lesson or a material and it will appear here."
              icon={BookOpen}
              title="Nothing recent"
              action={
                <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/materials">
                  Open materials
                </Link>
              }
            />
          ) : (
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
                      <time className="nv-meta" dateTime={item.when}>
                        {label}
                      </time>
                    ) : null}
                  </li>
                );
              })}
            </ul>
          )}
        </Panel>

        <Panel title="What should I practise?">
          <p>{questions.what_should_i_practise.answer}</p>
          <TopicList
            empty="Nothing to practise yet. Your courses do not have practice questions loaded."
            items={questions.what_should_i_practise.items}
          />
        </Panel>
      </div>

      <Panel title="Where am I weak?">
        <p>{questions.where_am_i_weak.answer}</p>
        <TopicList
          empty="No weak topics right now. This fills in as you answer practice questions."
          items={questions.where_am_i_weak.items}
        />
      </Panel>

      <Panel title="Go deeper">
        <div className="nv-row">
          <Link className="nv-button nv-button--ghost" to="/academia/materials">
            <BookOpen aria-hidden="true" size={15} />
            Study materials
          </Link>
          <Link className="nv-button nv-button--ghost" to="/academia/ask">
            <Sparkles aria-hidden="true" size={15} />
            Ask Nelavista
          </Link>
          <Link className="nv-button nv-button--ghost" to="/academia/cbt">
            <ClipboardCheck aria-hidden="true" size={15} />
            Practice (CBT)
          </Link>
        </div>
      </Panel>

      <div className="nv-row nv-row--end">
        <Button size="sm" type="button" variant="ghost" onClick={() => setAttempt((n) => n + 1)}>
          Refresh
        </Button>
      </div>
    </div>
  );
}
