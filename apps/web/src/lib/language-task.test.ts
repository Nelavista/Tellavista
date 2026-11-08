import { describe, expect, it } from 'vitest';

import {
  buildLanguageAnswer,
  emptyResponses,
  hasEnoughToSubmit,
  languageTaskSpec,
  type LanguageTaskSpec,
} from './language-task';

const LABELING: LanguageTaskSpec = {
  kind: 'labeling',
  items: [
    {
      id: 'a1',
      text: 'This phone sweet well well!',
      fields: [
        {
          name: 'sentiment',
          label: 'Sentiment',
          type: 'choice',
          options: ['Positive', 'Negative'],
        },
      ],
    },
  ],
};

const TRANSCRIPTION: LanguageTaskSpec = {
  kind: 'transcription',
  segments: [
    { id: 's1', reference: 'Mo fe lo si oja' },
    { id: 's2', reference: 'E kaaro', speaker_required: true, start_required: true },
  ],
  speakers: ['SPEAKER_1', 'SPEAKER_2'],
};

describe('language task helpers', () => {
  it('reads the spec out of the template input schema', () => {
    expect(languageTaskSpec({ type: 'object', task_spec: LABELING })).toEqual(LABELING);
    expect(languageTaskSpec({ type: 'object' })).toBeNull();
    expect(languageTaskSpec({ task_spec: { kind: 'unknown' } })).toBeNull();
  });

  it('starts a labeling answer with one empty value per field', () => {
    const responses = emptyResponses(LABELING);
    expect(responses).toEqual({ a1: { sentiment: '' } });
    expect(hasEnoughToSubmit(LABELING, responses)).toBe(false);
    expect(hasEnoughToSubmit(LABELING, { a1: { sentiment: 'Positive' } })).toBe(true);
  });

  it('requires a report to reach its word minimum', () => {
    const spec: LanguageTaskSpec = {
      ...LABELING,
      report: { min_words: 3 },
    };
    expect(hasEnoughToSubmit(spec, { a1: { sentiment: 'Positive' }, report: 'too short' })).toBe(
      false,
    );
    expect(
      hasEnoughToSubmit(spec, { a1: { sentiment: 'Positive' }, report: 'this is enough' }),
    ).toBe(true);
  });

  it('submits a plain string per segment unless a speaker or start is scored', () => {
    const responses = emptyResponses(TRANSCRIPTION);
    expect(responses).toEqual({ s1: '', s2: '' });
    const answer = buildLanguageAnswer(TRANSCRIPTION, {
      s1: '  Mo fe lo si oja  ',
      s2: { text: ' E kaaro ', speaker: 'SPEAKER_1', start: '0:02' },
    });
    expect(answer.responses.s1).toBe('Mo fe lo si oja');
    expect(answer.responses.s2).toEqual({
      text: 'E kaaro',
      speaker: 'SPEAKER_1',
      start: '0:02',
    });
  });

  it('keeps recording metrics and metadata in the envelope', () => {
    const spec: LanguageTaskSpec = {
      kind: 'recording',
      prompts: [{ id: 'p1', text: 'Read this.' }],
      metadata_fields: [{ name: 'dialect', label: 'Dialect' }],
    };
    const responses = emptyResponses(spec);
    expect(responses).toEqual({ p1: null, metadata: { dialect: '' } });
    expect(hasEnoughToSubmit(spec, responses)).toBe(false);
    const metrics = {
      duration_seconds: 3,
      clip_pct: 0,
      rms_db: -20,
      silence_pct: 5,
    };
    expect(hasEnoughToSubmit(spec, { p1: metrics, metadata: { dialect: 'Ekiti' } })).toBe(true);
  });
});
