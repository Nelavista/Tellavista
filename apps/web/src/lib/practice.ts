/**
 * Practice forms are generated from the task template's own schemas.
 *
 * A task type is content, not code (PRD §4): the API stores `input_schema` (what
 * the student is shown), `answer_schema` (what they submit) and names a
 * validator. This module turns those two schemas into exactly one control, and
 * turns the student's choice back into the answer object the validator expects.
 *
 * It is deliberately narrow: five validators exist, four can be answered with a
 * single control. A task type we cannot render says so plainly instead of
 * submitting something meaningless — a false answer would be worse than a
 * missing screen.
 */

export type PracticeControl =
  | { kind: 'choice'; field: 'key'; options: Array<{ value: string; label: string }> }
  | { kind: 'labels'; field: 'labels'; options: string[] }
  | { kind: 'ranking'; field: 'order'; items: string[] }
  | { kind: 'number'; field: 'value' }
  | { kind: 'unsupported'; reason: string };

export type Schema = Record<string, unknown>;

const METADATA_KEYS = new Set(['type', 'required', 'description', 'title', 'additionalProperties']);

function asRecord(value: unknown): Schema | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value) ? (value as Schema) : null;
}

function asStringList(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => (typeof item === 'string' ? item : '')).filter((item) => item.length > 0);
}

/**
 * The field names of a schema. Real templates use JSON Schema (`properties`), but
 * a template authored as `{"label": "string"}` is accepted too, since that is how
 * the ops API lets an operator describe a quick task.
 */
export function schemaFields(schema: Schema): string[] {
  const properties = asRecord(schema.properties);
  if (properties) return Object.keys(properties);
  return Object.keys(schema).filter((key) => !METADATA_KEYS.has(key));
}

function labelOf(value: unknown): string {
  if (typeof value === 'string') return value;
  const record = asRecord(value);
  if (!record) return '';
  const text = record.label ?? record.title ?? record.name ?? record.text;
  return typeof text === 'string' ? text : '';
}

function choiceOptions(input: Schema): Array<{ value: string; label: string }> {
  const raw = input.options ?? input.choices;
  if (!Array.isArray(raw)) return [];
  return raw
    .map((option) => {
      if (typeof option === 'string') return { value: option, label: option };
      const record = asRecord(option);
      const value = record?.key ?? record?.value ?? record?.slug ?? record?.id;
      if (value === undefined || value === null) return null;
      return { value: String(value), label: labelOf(option) || String(value) };
    })
    .filter((option): option is { value: string; label: string } => option !== null);
}

/** Decide the one control this task needs, or why it cannot be rendered. */
export function practiceControl(input: Schema, answer: Schema): PracticeControl {
  const fields = schemaFields(answer);
  const has = (name: string): boolean => fields.includes(name);

  if (has('spans')) {
    return {
      kind: 'unsupported',
      reason:
        'This task needs a text-marker view, which is not built yet. Your progress is unaffected — practise another task meanwhile.',
    };
  }

  if (has('key')) {
    const options = choiceOptions(input);
    if (options.length === 0) {
      return {
        kind: 'unsupported',
        reason: 'This task has no answer options published yet.',
      };
    }
    return { kind: 'choice', field: 'key', options };
  }

  if (has('labels')) {
    const options = asStringList(input.labels ?? input.allowed_labels);
    if (options.length === 0) {
      return { kind: 'unsupported', reason: 'This task has no labels published yet.' };
    }
    return { kind: 'labels', field: 'labels', options };
  }

  if (has('order')) {
    const items = asStringList(input.items ?? input.rows);
    if (items.length === 0) {
      return { kind: 'unsupported', reason: 'This task has no items published yet.' };
    }
    return { kind: 'ranking', field: 'order', items };
  }

  if (has('value')) return { kind: 'number', field: 'value' };

  return {
    kind: 'unsupported',
    reason: 'This task type is not supported on the web yet. Try another practice task.',
  };
}

/**
 * Only the shapes the generated controls can produce are restored from a draft;
 * anything else is ignored rather than rendered into a form.
 */
export function isAnswerValue(value: unknown): boolean {
  return (
    typeof value === 'string' ||
    typeof value === 'number' ||
    (Array.isArray(value) && value.every((item) => typeof item === 'string'))
  );
}

/**
 * Turn a control value into the answer object, or `null` when nothing valid has
 * been given yet — the caller disables submit rather than sending an empty answer
 * the validator would score zero.
 */
export function buildAnswer(
  control: PracticeControl,
  value: string | string[] | number | null,
): Record<string, unknown> | null {
  switch (control.kind) {
    case 'choice':
      return typeof value === 'string' && value.length > 0 ? { key: value } : null;
    case 'labels': {
      const labels = Array.isArray(value) ? value.filter((item) => item.length > 0) : [];
      return labels.length > 0 ? { labels } : null;
    }
    case 'ranking': {
      const order = Array.isArray(value) ? value.filter((item) => item.length > 0) : [];
      return order.length > 0 ? { order } : null;
    }
    case 'number': {
      if (typeof value !== 'number' || !Number.isFinite(value)) return null;
      return { value: Math.trunc(value) };
    }
    default:
      return null;
  }
}
