/**
 * Practice task (B6).
 *
 * The form is generated from the template's own schemas (`lib/practice.ts`), so a
 * new task type is content rather than a new screen. The verdict shown here is
 * feedback from the sandbox validator: the API returns
 * `counts_as_verification: false` and the page says the same thing in words, so a
 * correct practice answer is never mistaken for proof.
 */
import type { PracticeBriefOut, PracticeResultOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';

import { draftKey, useDraft } from '../lib/draft';
import { ApiError, http } from '../lib/http';
import { buildAnswer, isAnswerValue, practiceControl, type PracticeControl } from '../lib/practice';
import { useApiResource } from '../lib/resource';
import { useSessionOptional } from '../lib/session';
import { ErrorNote, Skeleton } from '../ui';

type Value = string | string[] | number | null;

function backLink(state: unknown): string {
  const from = (state as { from?: unknown } | null)?.from;
  return typeof from === 'string' && from.startsWith('/') ? from : '/skills';
}

function Ranking({
  items,
  value,
  onChange,
}: {
  items: string[];
  value: string[];
  onChange: (next: string[]) => void;
}): JSX.Element {
  function move(index: number, delta: number): void {
    const next = [...value];
    const target = index + delta;
    if (target < 0 || target >= next.length) return;
    const [item] = next.splice(index, 1);
    if (item === undefined) return;
    next.splice(target, 0, item);
    onChange(next);
  }

  return (
    <ol className="nv-list">
      {value.map((item, index) => (
        <li className="nv-row nv-row--between" key={item}>
          <span>
            {index + 1}. {item}
          </span>
          <span className="nv-row">
            <button
              className="nv-button nv-button--ghost"
              type="button"
              aria-label={`Move ${item} up`}
              disabled={index === 0}
              onClick={() => move(index, -1)}
            >
              ↑
            </button>
            <button
              className="nv-button nv-button--ghost"
              type="button"
              aria-label={`Move ${item} down`}
              disabled={index === value.length - 1}
              onClick={() => move(index, 1)}
            >
              ↓
            </button>
          </span>
        </li>
      ))}
      <li className="nv-muted">All {items.length} items must appear in your order.</li>
    </ol>
  );
}

function Control({
  control,
  value,
  onChange,
}: {
  control: PracticeControl;
  value: Value;
  onChange: (next: Value) => void;
}): JSX.Element {
  if (control.kind === 'unsupported') {
    return <p className="nv-banner">{control.reason}</p>;
  }

  if (control.kind === 'choice') {
    return (
      <fieldset className="nv-field">
        <legend className="nv-label">Choose one</legend>
        {control.options.map((option) => (
          <label className="nv-check" key={option.value}>
            <input
              checked={value === option.value}
              name="nv-practice-choice"
              type="radio"
              value={option.value}
              onChange={() => onChange(option.value)}
            />
            {option.label}
          </label>
        ))}
      </fieldset>
    );
  }

  if (control.kind === 'labels') {
    const selected = Array.isArray(value) ? value : [];
    return (
      <fieldset className="nv-field">
        <legend className="nv-label">Select every label that applies</legend>
        {control.options.map((option) => (
          <label className="nv-check" key={option}>
            <input
              checked={selected.includes(option)}
              type="checkbox"
              onChange={(event) =>
                onChange(
                  event.target.checked ? [...selected, option] : selected.filter((item) => item !== option),
                )
              }
            />
            {option}
          </label>
        ))}
      </fieldset>
    );
  }

  if (control.kind === 'ranking') {
    const order = Array.isArray(value) ? value : control.items;
    return <Ranking items={control.items} value={order} onChange={onChange} />;
  }

  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor="nv-practice-number">
        Answer (whole number)
      </label>
      <input
        className="nv-input"
        id="nv-practice-number"
        inputMode="numeric"
        type="number"
        value={typeof value === 'number' ? value : ''}
        onChange={(event) => onChange(event.target.value === '' ? null : Number(event.target.value))}
      />
    </div>
  );
}

export function Practice(): JSX.Element {
  const { templateId = '' } = useParams<{ templateId: string }>();
  const location = useLocation();
  const session = useSessionOptional();
  const { resource, reload } = useApiResource<PracticeBriefOut>(`/skills/tasks/${templateId}`);
  // The draft is keyed by student as well as task: a shared device must never
  // restore one student's answer into another's form.
  const draft = useDraft<Value>(
    draftKey('practice', session?.me?.id ?? 'anonymous', templateId),
    null,
    isAnswerValue,
  );
  const { value, setValue } = draft;
  const [result, setResult] = React.useState<PracticeResultOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const control = React.useMemo(
    () =>
      resource.status === 'ready'
        ? practiceControl(resource.data.input_schema, resource.data.answer_schema)
        : null,
    [resource],
  );

  const answer = control ? buildAnswer(control, value) : null;

  async function submit(): Promise<void> {
    if (!answer) return;
    setBusy(true);
    setError(null);
    try {
      const payload = await http.post<PracticeResultOut>(`/skills/tasks/${templateId}/practice`, {
        answer,
      });
      setResult(payload);
      // Only the server accepting the answer clears it. A failed send keeps the
      // draft, which is the whole point of writing it as the student types.
      draft.clear();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your answer. Try again.');
    } finally {
      setBusy(false);
    }
  }

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this practice task">
        <Skeleton height="2rem" width="50%" />
        <Skeleton lines={3} />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Practice</h1>
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

  const brief = resource.data;

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to={backLink(location.state)}>Back to the path</Link>
      </p>

      <h1 className="nv-h1">{brief.name}</h1>
      <p className="nv-muted">Practice — this does not count as verification.</p>

      {brief.instructions_md ? <p>{brief.instructions_md}</p> : null}

      {typeof brief.sample === 'string' ? (
        <section className="nv-card">
          <h2 className="nv-h2">Sample input</h2>
          <pre className="nv-code">{brief.sample}</pre>
        </section>
      ) : null}

      <ErrorNote message={error} />

      {result ? (
        <section className="nv-card" aria-live="polite">
          <h2 className="nv-h2">{result.is_correct ? 'Correct' : 'Not quite'}</h2>
          <p>{result.feedback}</p>
          <p className="nv-muted">Score: {result.score}/100 · not verification</p>
          <div className="nv-row">
            <button
              className="nv-button nv-button--ghost"
              type="button"
              onClick={() => {
                setResult(null);
                setValue(null);
              }}
            >
              Try again
            </button>
            <Link to={backLink(location.state)}>Back to the path</Link>
          </div>
        </section>
      ) : control ? (
        <>
          <Control control={control} value={value} onChange={setValue} />
          <div className="nv-row">
            <button
              className="nv-button"
              disabled={busy || !answer}
              type="button"
              onClick={() => void submit()}
            >
              {busy ? 'Checking…' : 'Check my answer'}
            </button>
            {!answer ? <span className="nv-muted">Answer first to see how you did.</span> : null}
          </div>
          {draft.savedAt ? (
            <p className="nv-muted" aria-live="polite">
              Answer saved on this device — it is still here if the connection drops.
            </p>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
