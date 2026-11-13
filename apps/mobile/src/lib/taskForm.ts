/**
 * The same schema-to-control rules as the web (`apps/web/src/lib/practice.ts`),
 * kept as a small shared-logic port rather than a shared component: the two
 * platforms render differently, but a task must accept the same answer object.
 */
/**
 * One field of a structured (ALL) task. `field` names the key inside the item's
 * answer: `text` for a transcript or translation, `speaker`/`start` when the spec
 * asks for them, and a label field name for labeling items. A null `field` means
 * the answer for that item is the bare string.
 */
export type ResponseRow = {
  item: string;
  field: string | null;
  label: string;
  hint?: string;
  multiline: boolean;
};

export type Control =
  | { kind: 'choice'; options: Array<{ value: string; label: string }> }
  | { kind: 'labels'; options: string[] }
  | { kind: 'ranking'; items: string[] }
  | { kind: 'responses'; rows: ResponseRow[] }
  | { kind: 'number' }
  | { kind: 'unsupported'; reason: string };

export type Schema = Record<string, unknown>;

const META = new Set(['type', 'required', 'description', 'title', 'additionalProperties']);

function record(value: unknown): Schema | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value) ? (value as Schema) : null;
}

function strings(value: unknown): string[] {
  return Array.isArray(value)
    ? value.map((item) => (typeof item === 'string' ? item : '')).filter((item) => item.length > 0)
    : [];
}

export function fields(schema: Schema): string[] {
  const properties = record(schema.properties);
  if (properties) return Object.keys(properties);
  return Object.keys(schema).filter((key) => !META.has(key));
}

export function controlFor(input: Schema | null | undefined, answer: Schema | null | undefined): Control {
  if (!input || !answer) {
    return { kind: 'unsupported', reason: 'This task has no published form yet.' };
  }
  const names = fields(answer);
  if (names.includes('spans')) {
    return { kind: 'unsupported', reason: 'Marking a text is not supported on mobile yet. Use the web app for this task.' };
  }
  if (names.includes('key')) {
    const raw = input.options ?? input.choices;
    const options = Array.isArray(raw)
      ? raw
          .map((option) => {
            if (typeof option === 'string') return { value: option, label: option };
            const item = record(option);
            const value = item?.key ?? item?.value ?? item?.id;
            if (value === undefined || value === null) return null;
            const label = item?.label ?? item?.title ?? item?.name ?? value;
            return { value: String(value), label: String(label) };
          })
          .filter((option): option is { value: string; label: string } => option !== null)
      : [];
    return options.length > 0
      ? { kind: 'choice', options }
      : { kind: 'unsupported', reason: 'This task has no answer options published yet.' };
  }
  if (names.includes('labels')) {
    const options = strings(input.labels ?? input.allowed_labels);
    return options.length > 0
      ? { kind: 'labels', options }
      : { kind: 'unsupported', reason: 'This task has no labels published yet.' };
  }
  if (names.includes('order')) {
    const items = strings(input.items ?? input.rows);
    return items.length > 0
      ? { kind: 'ranking', items }
      : { kind: 'unsupported', reason: 'This task has no items published yet.' };
  }
  if (names.includes('responses')) {
    return structuredControl(input.task_spec);
  }
  if (names.includes('value')) return { kind: 'number' };
  return { kind: 'unsupported', reason: 'This task type is not supported on mobile yet.' };
}

function structuredControl(spec: unknown): Control {
  const task = record(spec);
  if (!task) return { kind: 'unsupported', reason: 'This task has no published form yet.' };
  const kind = task.kind;
  if (kind === 'recording') {
    return {
      kind: 'unsupported',
      reason:
        'Recording needs a device microphone, so it is only available on the web app for now. Your other practice is unaffected.',
    };
  }
  const rows: ResponseRow[] = [];
  if (kind === 'labeling') {
    for (const raw of Array.isArray(task.items) ? task.items : []) {
      const item = record(raw);
      const id = item?.id;
      if (id === undefined || id === null) continue;
      for (const rawField of Array.isArray(item?.fields) ? item.fields : []) {
        const taskField = record(rawField);
        const name = taskField?.name;
        if (typeof name !== 'string') continue;
        rows.push({
          item: String(id),
          field: name,
          label: String(taskField?.label ?? name),
          hint: typeof item?.text === 'string' ? item.text : undefined,
          multiline: false,
        });
      }
    }
  } else if (kind === 'transcription') {
    for (const raw of Array.isArray(task.segments) ? task.segments : []) {
      const segment = record(raw);
      const id = segment?.id;
      if (id === undefined || id === null) continue;
      rows.push({
        item: String(id),
        field: 'text',
        label: `Segment ${String(id)}`,
        hint: typeof segment?.context === 'string' ? segment.context : undefined,
        multiline: true,
      });
      if (segment?.speaker_required) {
        rows.push({
          item: String(id),
          field: 'speaker',
          label: `Speaker for ${String(id)}`,
          hint: 'Use the speaker name from the brief, e.g. Speaker 1.',
          multiline: false,
        });
      }
      if (segment?.start_required) {
        rows.push({
          item: String(id),
          field: 'start',
          label: `Start of ${String(id)}`,
          hint: 'm:ss or seconds.',
          multiline: false,
        });
      }
    }
  } else if (kind === 'translation') {
    for (const raw of Array.isArray(task.items) ? task.items : []) {
      const item = record(raw);
      const id = item?.id;
      if (id === undefined || id === null) continue;
      rows.push({
        item: String(id),
        field: null,
        label: `Translate ${String(id)}`,
        hint: typeof item?.source === 'string' ? item.source : undefined,
        multiline: true,
      });
    }
  } else {
    return { kind: 'unsupported', reason: 'This task type is not supported on mobile yet.' };
  }
  return rows.length > 0
    ? { kind: 'responses', rows }
    : { kind: 'unsupported', reason: 'This task has no items published yet.' };
}

export function answerFor(
  control: Control,
  value: string | string[] | number | null,
): Record<string, unknown> | null {
  switch (control.kind) {
    case 'responses': {
      const texts = Array.isArray(value) ? value : [];
      const responses: Record<string, unknown> = {};
      control.rows.forEach((row, index) => {
        const text = (texts[index] ?? '').trim();
        if (!text) return;
        if (row.field === null) {
          responses[row.item] = text;
          return;
        }
        const existing = record(responses[row.item]) ?? {};
        existing[row.field] = text;
        responses[row.item] = existing;
      });
      return Object.keys(responses).length > 0 ? { responses } : null;
    }
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
    case 'number':
      return typeof value === 'number' && Number.isFinite(value) ? { value: Math.trunc(value) } : null;
    default:
      return null;
  }
}
