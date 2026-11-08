/**
 * Structured language-data tasks (African Languages Lab).
 *
 * These four task kinds do not fit the single-control practice generator: they
 * submit a `responses` map keyed by item id. This module reads the task spec out
 * of the template's input schema and shapes the answer envelope the API scores.
 */

export type LanguageTaskKind = 'transcription' | 'translation' | 'labeling' | 'recording';

export type LanguageTaskSpec = {
  kind: LanguageTaskKind;
  brief?: string;
  guidelines?: string[];
  mode?: string;
  speakers?: string[];
  timestamp_tolerance?: number;
  segments?: Array<{
    id: string;
    reference?: string;
    draft?: string;
    context?: string;
    speaker_required?: boolean;
    start_required?: boolean;
  }>;
  source_lang?: string;
  target_lang?: string;
  items?: Array<{
    id: string;
    source?: string;
    text?: string;
    context?: string;
    repeat_of?: string;
    references?: string[];
    key_terms?: string[];
    fields?: Array<{
      name: string;
      label?: string;
      type?: 'choice' | 'number' | 'text';
      options?: string[];
      tolerance?: number;
    }>;
  }>;
  report?: { label?: string; min_words?: number };
  prompts?: Array<{ id: string; text: string }>;
  requirements?: {
    min_seconds?: number;
    max_seconds?: number;
    max_clip_pct?: number;
    min_rms_db?: number;
    max_silence_pct?: number;
  };
  metadata_fields?: Array<{ name: string; label?: string; type?: string; options?: string[] }>;
};

export type RecordingMetrics = {
  duration_seconds: number;
  clip_pct: number;
  rms_db: number;
  silence_pct: number;
};

export type LanguageResponses = Record<string, unknown>;

function asRecord(value: unknown): Record<string, unknown> | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}

/** The spec lives at `input_schema.task_spec` for ALL templates. */
export function languageTaskSpec(inputSchema: Record<string, unknown>): LanguageTaskSpec | null {
  const raw = asRecord(inputSchema.task_spec);
  if (!raw) return null;
  const kind = raw.kind;
  if (kind !== 'transcription' && kind !== 'translation' && kind !== 'labeling' && kind !== 'recording') {
    return null;
  }
  return raw as unknown as LanguageTaskSpec;
}

export function emptyResponses(spec: LanguageTaskSpec): LanguageResponses {
  const responses: LanguageResponses = {};
  if (spec.kind === 'recording') {
    for (const prompt of spec.prompts ?? []) responses[prompt.id] = null;
    const metadata: Record<string, string> = {};
    for (const field of spec.metadata_fields ?? []) metadata[field.name] = '';
    if (Object.keys(metadata).length > 0) responses.metadata = metadata;
    return responses;
  }
  if (spec.kind === 'labeling') {
    for (const item of spec.items ?? []) {
      const fields: Record<string, string> = {};
      for (const field of item.fields ?? []) fields[field.name] = '';
      responses[item.id] = fields;
    }
    if (spec.report) responses.report = '';
    return responses;
  }
  for (const item of spec.items ?? spec.segments ?? []) responses[item.id] = '';
  return responses;
}

/** Whether every required input has a value; the API still does the scoring. */
export function hasEnoughToSubmit(spec: LanguageTaskSpec, responses: LanguageResponses): boolean {
  if (spec.kind === 'labeling') {
    const items = spec.items ?? [];
    const fields = items.flatMap((item) => item.fields ?? []);
    const values = items.flatMap((item) => Object.values(asRecord(responses[item.id]) ?? {}));
    const filled = values.filter((value) => String(value ?? '').trim()).length;
    if (filled < fields.length) return false;
    if (spec.report) {
      const report = String(responses.report ?? '').trim();
      if (report.split(/\s+/).filter(Boolean).length < (spec.report.min_words ?? 15)) return false;
    }
    return true;
  }
  if (spec.kind === 'recording') {
    const prompts = spec.prompts ?? [];
    if (!prompts.every((prompt) => Boolean(responses[prompt.id]))) return false;
    const metadata = asRecord(responses.metadata) ?? {};
    return (spec.metadata_fields ?? []).every((field) => String(metadata[field.name] ?? '').trim());
  }
  const items = spec.items ?? spec.segments ?? [];
  return items.every((item) => String(responses[item.id] ?? '').trim().length > 0);
}

export function buildLanguageAnswer(
  spec: LanguageTaskSpec,
  responses: LanguageResponses,
): { responses: LanguageResponses } {
  const cleaned: LanguageResponses = {};
  for (const [key, value] of Object.entries(responses)) {
    if (value === null || value === undefined) continue;
    if (typeof value === 'string') {
      cleaned[key] = value.trim();
    } else if (typeof value === 'object' && !Array.isArray(value)) {
      const record = asRecord(value);
      if (record) {
        cleaned[key] = Object.fromEntries(
          Object.entries(record).map(([field, fieldValue]) => [
            field,
            typeof fieldValue === 'string' ? fieldValue.trim() : fieldValue,
          ]),
        );
      }
    } else {
      cleaned[key] = value;
    }
  }
  // The transcription API accepts a string per segment; the richer object shape
  // is only needed when the spec asks for a speaker or start time.
  for (const segment of spec.segments ?? []) {
    const value = cleaned[segment.id];
    if (typeof value !== 'object' || value === null) continue;
    const record = asRecord(value);
    if (!record) continue;
    const hasSpeaker = Boolean(segment.speaker_required);
    const hasStart = Boolean(segment.start_required);
    if (!hasSpeaker && !hasStart) cleaned[segment.id] = String(record.text ?? '');
  }
  return { responses: cleaned };
}
