/**
 * The generated task control, shared by practice, assessments and work.
 *
 * The API owns the task type: `input_schema` is what is shown, `answer_schema`
 * is what is submitted. `lib/practice.ts` turns those two into one control, and
 * this component renders it. A task type that cannot be rendered says so - it
 * never submits a made-up answer.
 */
import * as React from 'react';

import { buildAnswer, practiceControl, type PracticeControl, type Schema } from '../lib/practice';

export type TaskValue = string | string[] | number | null;

const CONTROL_KEYS = new Set(['options', 'choices', 'labels', 'allowed_labels', 'items', 'rows']);

export function promptEntries(payload: Record<string, unknown>): Array<[string, string]> {
  return Object.entries(payload)
    .filter(
      ([key, value]) => !CONTROL_KEYS.has(key) && (typeof value === 'string' || typeof value === 'number'),
    )
    .map(([key, value]) => [key, String(value)]);
}

export function TaskPrompt({ payload }: { payload: Record<string, unknown> }): JSX.Element {
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

export function TaskControl({
  control,
  value,
  onChange,
}: {
  control: PracticeControl;
  value: TaskValue;
  onChange: (next: TaskValue) => void;
}): JSX.Element {
  const groupName = React.useId();
  if (control.kind === 'unsupported') return <p className="nv-banner">{control.reason}</p>;

  if (control.kind === 'choice') {
    return (
      <fieldset className="nv-field">
        <legend className="nv-label">Choose one</legend>
        {control.options.map((option) => (
          <label className="nv-check" key={option.value}>
            <input
              checked={value === option.value}
              name={groupName}
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
    const move = (index: number, offset: number): void => {
      const next = [...order];
      const [moved] = next.splice(index, 1);
      if (moved === undefined) return;
      next.splice(index + offset, 0, moved);
      onChange(next);
    };
    return (
      <ol className="nv-list">
        {order.map((item, index) => (
          <li className="nv-row nv-row--between" key={item}>
            <span>
              {index + 1}. {item}
            </span>
            <span className="nv-row">
              <button
                aria-label={`Move ${item} up`}
                className="nv-button nv-button--ghost"
                disabled={index === 0}
                type="button"
                onClick={() => move(index, -1)}
              >
                ↑
              </button>
              <button
                aria-label={`Move ${item} down`}
                className="nv-button nv-button--ghost"
                disabled={index === order.length - 1}
                type="button"
                onClick={() => move(index, 1)}
              >
                ↓
              </button>
            </span>
          </li>
        ))}
      </ol>
    );
  }

  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor={`${groupName}-number`}>
        Answer (whole number)
      </label>
      <input
        className="nv-input"
        id={`${groupName}-number`}
        inputMode="numeric"
        type="number"
        value={typeof value === 'number' ? value : ''}
        onChange={(event) => onChange(event.target.value === '' ? null : Number(event.target.value))}
      />
    </div>
  );
}

/** Schema pair → control. Exported so a page can disable submit honestly. */
export function controlFor(
  inputSchema: Schema | null | undefined,
  answerSchema: Schema | null | undefined,
  unsupportedReason = 'This task has no form published yet.',
): PracticeControl {
  if (!inputSchema || !answerSchema) {
    return { kind: 'unsupported', reason: unsupportedReason };
  }
  return practiceControl(inputSchema, answerSchema);
}

export { buildAnswer };
