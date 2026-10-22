/**
 * Lesson reader (B6).
 *
 * Two honesty rules are enforced by the API and shown by this page, not softened:
 * a lesson can only be completed when the step before it is done, and completing
 * it is progress — the completion response says `verified: false`, and the page
 * repeats that in the student's own words. Reading is never blocked; only the
 * completion button is.
 */
import type { LessonCompletedOut, LessonOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { parseLessonBody, type Block, type Inline } from '../lib/markdown';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

function InlineRuns({ runs }: { runs: Inline[] }): JSX.Element {
  return (
    <>
      {runs.map((run, index) => {
        if (run.kind === 'strong') return <strong key={index}>{run.text}</strong>;
        if (run.kind === 'code') return <code key={index}>{run.text}</code>;
        if (run.kind === 'link') {
          return (
            <a href={run.href} key={index} rel="noreferrer noopener" target="_blank">
              {run.text}
            </a>
          );
        }
        return <React.Fragment key={index}>{run.text}</React.Fragment>;
      })}
    </>
  );
}

function Body({ blocks }: { blocks: Block[] }): JSX.Element {
  return (
    <>
      {blocks.map((block, index) => {
        if (block.kind === 'heading') {
          // Lesson headings are one level below the page title so the outline
          // stays sane for screen readers.
          return (
            <h2 className="nv-h2" key={index}>
              <InlineRuns runs={block.inline} />
            </h2>
          );
        }
        if (block.kind === 'list') {
          return (
            <ul className="nv-list" key={index}>
              {block.items.map((item, itemIndex) => (
                <li key={itemIndex}>
                  <InlineRuns runs={item} />
                </li>
              ))}
            </ul>
          );
        }
        if (block.kind === 'quote') {
          return (
            <blockquote className="nv-quote" key={index}>
              <InlineRuns runs={block.inline} />
            </blockquote>
          );
        }
        if (block.kind === 'code') {
          return (
            <pre className="nv-code" key={index}>
              {block.text}
            </pre>
          );
        }
        return (
          <p key={index}>
            <InlineRuns runs={block.inline} />
          </p>
        );
      })}
    </>
  );
}

/** Where the student came from, so a reader and a practice task can offer a way back. */
function backLink(state: unknown): string {
  const from = (state as { from?: unknown } | null)?.from;
  return typeof from === 'string' && from.startsWith('/') ? from : '/skills';
}

export function LessonReader(): JSX.Element {
  const { lessonSlug = '' } = useParams<{ lessonSlug: string }>();
  const location = useLocation();
  const { resource, reload } = useApiResource<LessonOut>(`/skills/lessons/${lessonSlug}`);
  const [status, setStatus] = React.useState<string | null>(null);
  const [completion, setCompletion] = React.useState<LessonCompletedOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const lesson = resource.status === 'ready' ? resource.data : null;
  const currentStatus = status ?? lesson?.status ?? 'not_started';

  async function act(action: 'start' | 'complete', lessonId: number): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      if (action === 'start') {
        const started = await http.post<{ lesson_id: number; status: string }>(
          `/skills/lessons/${lessonId}/start`,
        );
        setStatus(started.status);
      } else {
        const completed = await http.post<LessonCompletedOut>(`/skills/lessons/${lessonId}/complete`);
        setStatus(completed.status);
        setCompletion(completed);
      }
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'That did not go through. Try again.');
    } finally {
      setBusy(false);
    }
  }

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this lesson">
        <Skeleton height="2rem" width="55%" />
        <Skeleton lines={6} />
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Lesson</h1>
        {resource.status === 'off' ? (
          <p className="nv-banner">The skills journey is not switched on for this environment yet.</p>
        ) : (
          <>
            <ErrorNote message={resource.message} />
            <button className="nv-button" type="button" onClick={reload}>
              Try again
            </button>
          </>
        )}
        <p className="nv-muted">
          <Link to="/skills">All skills</Link>
        </p>
      </div>
    );
  }

  const back = backLink(location.state);

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to={back}>Back to the path</Link>
      </p>

      <h1 className="nv-h1">{lesson?.title}</h1>
      {lesson?.estimated_minutes ? (
        <p className="nv-muted">About {lesson.estimated_minutes} minutes</p>
      ) : null}

      {error ? <ErrorNote message={error} /> : null}

      {!lesson?.unlocked ? (
        <p className="nv-banner">
          This lesson is locked: finish the step before it in the path. You can still read it.
        </p>
      ) : null}

      <article className="nv-stack">
        <Body blocks={parseLessonBody(lesson?.body_md ?? '')} />
      </article>

      {completion ? (
        <section className="nv-card">
          <h2 className="nv-h2">Lesson complete</h2>
          <p className="nv-muted">{completion.note}</p>
          <p>
            <Link to="/skills/my-learning">See your progress</Link>
          </p>
        </section>
      ) : lesson?.unlocked ? (
        <div className="nv-row">
          {currentStatus === 'not_started' ? (
            <button
              className="nv-button"
              disabled={busy}
              type="button"
              onClick={() => lesson && void act('start', lesson.id)}
            >
              {busy ? 'Starting…' : 'Start this lesson'}
            </button>
          ) : (
            <button
              className="nv-button"
              disabled={busy}
              type="button"
              onClick={() => lesson && void act('complete', lesson.id)}
            >
              {busy ? 'Saving…' : 'Mark as complete'}
            </button>
          )}
          <span className="nv-muted">
            {currentStatus === 'in_progress' && !completion
              ? 'Finish it when you are ready — finishing is progress, not proof.'
              : 'A finished lesson counts as learning, never as verification.'}
          </span>
        </div>
      ) : null}
    </div>
  );
}
