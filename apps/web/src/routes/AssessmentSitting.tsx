/**
 * An assessment sitting (B7).
 *
 * The rules the API enforces are visible on the screen instead of being hidden:
 *
 * * starting is a POST, and the API resumes an open sitting rather than drawing a
 *   new (easier) set - so a lost connection is not a lost attempt;
 * * the expected answer is never sent while the attempt is open, so this screen
 *   cannot grade locally even if it wanted to;
 * * the form is generated from the template's own schemas, exactly like practice.
 *   A task whose type cannot be rendered says so instead of submitting noise.
 *
 * Unanswered tasks score zero rather than blocking submit: a student whose one
 * unrenderable task is first should still be able to finish the rest.
 */
import type { AttemptOut, AttemptResultOut, AttemptTaskOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import {
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  ClipboardList,
  Clock,
  XCircle,
} from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { draftKey, useDraft } from '../lib/draft';
import { ApiError, http } from '../lib/http';
import { buildAnswer, isAnswerValue, practiceControl, type PracticeControl } from '../lib/practice';
import { formatDateTime } from '../lib/format';
import { useSessionOptional } from '../lib/session';

type Value = string | string[] | number | null;

/** A saved answer map, as JSON gives it back: task ids are strings. */
function isValueMap(value: unknown): boolean {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  return Object.values(value as Record<string, unknown>).every(
    (item) => item === null || isAnswerValue(item),
  );
}

type Sitting =
  | { status: 'starting' }
  | { status: 'ready'; attempt: AttemptOut }
  | { status: 'off' }
  | { status: 'error'; message: string };

/** Keys the generated control consumes; the rest of the payload is the prompt. */
const CONTROL_KEYS = new Set(['options', 'choices', 'labels', 'allowed_labels', 'items', 'rows']);

function promptEntries(payload: Record<string, unknown>): Array<[string, string]> {
  return Object.entries(payload)
    .filter(
      ([key, value]) => !CONTROL_KEYS.has(key) && (typeof value === 'string' || typeof value === 'number'),
    )
    .map(([key, value]) => [key, String(value)]);
}

function TaskPrompt({ payload }: { payload: Record<string, unknown> }): JSX.Element {
  const entries = promptEntries(payload);
  if (entries.length === 0) {
    return <p className="nv-muted">This task has no readable input yet.</p>;
  }
  if (entries.length === 1) {
    return <p>{entries[0]?.[1]}</p>;
  }
  return (
    <ul className="nv-list">
      {entries.map(([key, value]) => (
        <li key={key}>
          <span className="nv-muted">{key.replace(/_/g, ' ')}: </span>
          {value}
        </li>
      ))}
    </ul>
  );
}

function controlFor(task: AttemptTaskOut): PracticeControl {
  if (!task.input_schema || !task.answer_schema) {
    return {
      kind: 'unsupported',
      reason:
        'This task is not attached to a task template, so there is no form to answer it with yet. Your other answers still count.',
    };
  }
  return practiceControl(task.input_schema, task.answer_schema);
}

function Choice({
  control,
  value,
  onChange,
}: {
  control: PracticeControl;
  value: Value;
  onChange: (next: Value) => void;
}): JSX.Element {
  const groupName = React.useId();
  if (control.kind === 'unsupported') {
    return (
      <Banner tone="warning">
        <p>{control.reason}</p>
      </Banner>
    );
  }

  if (control.kind === 'choice') {
    const name = groupName;
    return (
      <fieldset className="nv-field">
        <legend className="nv-label">Choose one</legend>
        {control.options.map((option) => (
          <label className="nv-check" key={option.value}>
            <input
              checked={value === option.value}
              name={name}
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
    const order = Array.isArray(value) && value.length > 0 ? value : control.items;
    return (
      <ol className="nv-list nv-list--ruled">
        {order.map((item, index) => (
          <li className="nv-row nv-row--between" key={item}>
            <span>
              <span className="nv-muted nv-num">{index + 1}.</span> {item}
            </span>
            <span className="nv-row">
              <Button
                aria-label={`Move ${item} up`}
                disabled={index === 0}
                size="sm"
                type="button"
                variant="ghost"
                onClick={() => {
                  const next = [...order];
                  const [moved] = next.splice(index, 1);
                  if (moved === undefined) return;
                  next.splice(index - 1, 0, moved);
                  onChange(next);
                }}
              >
                <ChevronUp aria-hidden="true" size={15} />
              </Button>
              <Button
                aria-label={`Move ${item} down`}
                disabled={index === order.length - 1}
                size="sm"
                type="button"
                variant="ghost"
                onClick={() => {
                  const next = [...order];
                  const [moved] = next.splice(index, 1);
                  if (moved === undefined) return;
                  next.splice(index + 1, 0, moved);
                  onChange(next);
                }}
              >
                <ChevronDown aria-hidden="true" size={15} />
              </Button>
            </span>
          </li>
        ))}
      </ol>
    );
  }

  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor="nv-assessment-number">
        Answer (whole number)
      </label>
      <input
        className="nv-input"
        id="nv-assessment-number"
        inputMode="numeric"
        type="number"
        value={typeof value === 'number' ? value : ''}
        onChange={(event) => onChange(event.target.value === '' ? null : Number(event.target.value))}
      />
    </div>
  );
}

function Result({ result }: { result: AttemptResultOut }): JSX.Element {
  return (
    <Panel
      title={result.expired ? 'This attempt expired' : result.passed ? 'Proved' : 'Not passed yet'}
      actions={
        <Badge
          status={result.passed ? 'verified' : 'at_risk'}
          tone={result.expired ? 'warning' : result.passed ? 'success' : 'danger'}
        >
          {result.expired ? 'Expired' : result.passed ? 'Passed' : 'Not passed'}
        </Badge>
      }
    >
      <div className="nv-stack" aria-live="polite">
        <p>
          Score: {result.score}
          {result.pass_threshold !== null && result.pass_threshold !== undefined
            ? ` · pass mark ${result.pass_threshold}%`
            : ''}
        </p>
        {result.expired ? (
          <p className="nv-muted">
            {result.message ??
              'The sitting ran out of time and was graded as zero. Start a new one when you are ready.'}
          </p>
        ) : result.passed ? (
          <p className="nv-muted">
            Your badge is {result.verification_status ?? 'updated'} and a proved line was written to your
            transcript.
          </p>
        ) : (
          <p className="nv-muted">
            A failed sitting never removes a badge you already hold, but it does use one of your attempts.
            Review the answers below before trying again.
          </p>
        )}

        {result.tasks.length > 0 ? (
          <ul className="nv-list nv-list--ruled">
            {result.tasks.map((task) => (
              <li key={task.task_id}>
                <div className="nv-row nv-row--between">
                  <Badge
                    status={task.correct ? 'verified' : 'at_risk'}
                    tone={task.correct ? 'success' : 'danger'}
                  >
                    {task.correct ? (
                      <>
                        <CheckCircle2 aria-hidden="true" size={13} /> Correct
                      </>
                    ) : (
                      <>
                        <XCircle aria-hidden="true" size={13} /> Incorrect
                      </>
                    )}
                  </Badge>
                  <span className="nv-num">
                    {task.points}/{task.max_points}
                  </span>
                </div>
                {task.feedback ? <p className="nv-muted">{task.feedback}</p> : null}
              </li>
            ))}
          </ul>
        ) : null}

        <div className="nv-row">
          <Link className="nv-button" to={`/verification/attempts/${result.attempt_id}`}>
            Review the answers
            <ArrowRight aria-hidden="true" size={15} />
          </Link>
          <Link to="/verification">Back to verification</Link>
        </div>
      </div>
    </Panel>
  );
}

export function AssessmentSitting(): JSX.Element {
  const { assessmentSlug = '' } = useParams<{ assessmentSlug: string }>();
  const session = useSessionOptional();
  const [sitting, setSitting] = React.useState<Sitting>({ status: 'starting' });
  const attemptId = sitting.status === 'ready' ? sitting.attempt.attempt_id : null;
  // A sitting is timed; losing typed answers to a reload is not acceptable. The
  // key carries the attempt id, so a new sitting never inherits old answers.
  const draft = useDraft<Record<string, Value>>(
    draftKey('sitting', session?.me?.id ?? 'anonymous', attemptId ?? 'pending'),
    {},
    isValueMap,
  );
  const values = attemptId === null ? {} : draft.value;
  const [result, setResult] = React.useState<AttemptResultOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const started = React.useRef(false);

  React.useEffect(() => {
    if (started.current) return;
    started.current = true;
    void (async () => {
      try {
        const attempt = await http.post<AttemptOut>(`/verification/assessments/${assessmentSlug}/start`);
        setSitting({ status: 'ready', attempt });
      } catch (err) {
        if (err instanceof ApiError && err.status === 404 && err.code === 'not_found') {
          setSitting({ status: 'off' });
          return;
        }
        setSitting({
          status: 'error',
          message: err instanceof ApiError ? err.message : 'Could not start this assessment.',
        });
      }
    })();
  }, [assessmentSlug]);

  if (sitting.status === 'starting') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Opening this assessment">
        <Skeleton height="2rem" width="45%" />
        <Skeleton lines={3} />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (sitting.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Verification" title="Assessment" />
        <Banner tone="info">
          <p>Verification is not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (sitting.status === 'error') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Verification" title="Assessment" />
        <ErrorState body={sitting.message} />
        <p className="nv-muted">
          <Link to="/verification">Back to verification</Link>
        </p>
      </div>
    );
  }

  const { attempt } = sitting;
  const controls = attempt.tasks.map((task) => controlFor(task));
  const answers = attempt.tasks
    .map((task, index) => {
      const control = controls[index];
      const value = values[String(task.task_id)] ?? null;
      const answer = control ? buildAnswer(control, value) : null;
      return answer ? ([String(task.task_id), answer] as const) : null;
    })
    .filter((entry): entry is readonly [string, Record<string, unknown>] => entry !== null);

  async function submit(): Promise<void> {
    if (answers.length === 0) return;
    setBusy(true);
    setError(null);
    try {
      const payload = await http.post<AttemptResultOut>(
        `/verification/attempts/${attempt.attempt_id}/submit`,
        {
          answers: Object.fromEntries(answers),
        },
      );
      setResult(payload);
      draft.clear();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send your answers. Try again.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to="/verification">Verification</Link>
      </p>

      {result ? (
        <Result result={result} />
      ) : (
        <>
          <PageHeader
            eyebrow="Assessment"
            title="Assessment"
            description={`${attempt.tasks.length} task${
              attempt.tasks.length === 1 ? '' : 's'
            } · expires ${formatDateTime(attempt.expires_at) || 'in 24 hours'}. Leaving this page does not lose the sitting: it resumes exactly these tasks.`}
            actions={
              <Badge tone="info">
                <Clock aria-hidden="true" size={13} /> Timed
              </Badge>
            }
          />

          {error ? (
            <Banner tone="danger">
              <p>{error}</p>
            </Banner>
          ) : null}

          {attempt.tasks.length === 0 ? (
            <EmptyState
              body="This assessment has no tasks. If that looks wrong, go back and contact support."
              icon={ClipboardList}
              title="No tasks in this sitting"
            />
          ) : (
            <div className="nv-stack">
              {attempt.tasks.map((task, index) => (
                <Panel
                  key={task.task_id}
                  title={`Task ${task.ordinal}`}
                  actions={
                    <Badge tone="neutral">
                      {task.points} point{task.points === 1 ? '' : 's'}
                    </Badge>
                  }
                >
                  <div className="nv-stack">
                    <TaskPrompt payload={task.payload} />
                    <Choice
                      control={controls[index] ?? { kind: 'unsupported', reason: '' }}
                      value={values[String(task.task_id)] ?? null}
                      onChange={(next) =>
                        draft.setValue((current) => ({ ...current, [String(task.task_id)]: next }))
                      }
                    />
                  </div>
                </Panel>
              ))}
            </div>
          )}

          <Panel title="Submit">
            <div className="nv-row nv-row--between">
              <span className="nv-muted">
                {answers.length} of {attempt.tasks.length} answered. Unanswered tasks score zero.
              </span>
              <Button disabled={busy || answers.length === 0} type="button" onClick={() => void submit()}>
                {busy ? 'Submitting…' : 'Submit this sitting'}
              </Button>
            </div>
            {draft.savedAt ? (
              <p className="nv-muted" aria-live="polite">
                Answers saved on this device. Reloading or losing the connection does not lose them.
              </p>
            ) : null}
          </Panel>
        </>
      )}
    </div>
  );
}
