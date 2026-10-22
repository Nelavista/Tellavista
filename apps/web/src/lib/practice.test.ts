/**
 * The practice form is the only place a student's answer is shaped for the
 * server, so its rules are tested directly: which control a schema selects, and
 * that an incomplete answer is refused instead of submitted as a zero.
 */
import { describe, expect, it } from 'vitest';

import { buildAnswer, practiceControl, schemaFields } from './practice';

describe('schemaFields', () => {
  it('reads JSON Schema properties', () => {
    expect(
      schemaFields({ type: 'object', required: ['key'], properties: { key: { type: 'string' } } }),
    ).toEqual(['key']);
  });

  it('accepts the compact {field: type} form the ops API allows', () => {
    expect(schemaFields({ label: 'string', note: 'string' })).toEqual(['label', 'note']);
  });
});

describe('practiceControl', () => {
  it('selects a single choice when the answer is a key', () => {
    const control = practiceControl(
      { options: [{ key: 'a', label: 'First' }, 'b'] },
      { properties: { key: { type: 'string' } } },
    );
    expect(control).toEqual({
      kind: 'choice',
      field: 'key',
      options: [
        { value: 'a', label: 'First' },
        { value: 'b', label: 'b' },
      ],
    });
  });

  it('selects a label set with the labels to choose from', () => {
    const control = practiceControl(
      { labels: ['person', 'place'] },
      { properties: { labels: { type: 'array' } } },
    );
    expect(control).toEqual({ kind: 'labels', field: 'labels', options: ['person', 'place'] });
  });

  it('selects a ranking with the items to order', () => {
    const control = practiceControl({ items: ['x', 'y', 'z'] }, { properties: { order: { type: 'array' } } });
    expect(control).toEqual({ kind: 'ranking', field: 'order', items: ['x', 'y', 'z'] });
  });

  it('selects a number for a numeric answer', () => {
    expect(practiceControl({}, { properties: { value: { type: 'integer' } } })).toEqual({
      kind: 'number',
      field: 'value',
    });
  });

  it('declines span tagging rather than guessing', () => {
    const control = practiceControl({ text: 'some passage' }, { properties: { spans: { type: 'array' } } });
    expect(control.kind).toBe('unsupported');
  });

  it('declines a choice task that publishes no options', () => {
    const control = practiceControl({}, { properties: { key: { type: 'string' } } });
    expect(control.kind).toBe('unsupported');
  });
});

describe('buildAnswer', () => {
  it('builds each supported answer shape', () => {
    expect(buildAnswer({ kind: 'choice', field: 'key', options: [] }, 'positive')).toEqual({
      key: 'positive',
    });
    expect(buildAnswer({ kind: 'labels', field: 'labels', options: [] }, ['a', 'b'])).toEqual({
      labels: ['a', 'b'],
    });
    expect(buildAnswer({ kind: 'ranking', field: 'order', items: [] }, ['b', 'a'])).toEqual({
      order: ['b', 'a'],
    });
    expect(buildAnswer({ kind: 'number', field: 'value' }, 12)).toEqual({ value: 12 });
  });

  it('truncates a fractional number instead of sending a float', () => {
    expect(buildAnswer({ kind: 'number', field: 'value' }, 12.7)).toEqual({ value: 12 });
  });

  it('refuses an empty or missing answer', () => {
    expect(buildAnswer({ kind: 'choice', field: 'key', options: [] }, '')).toBeNull();
    expect(buildAnswer({ kind: 'labels', field: 'labels', options: [] }, [])).toBeNull();
    expect(buildAnswer({ kind: 'number', field: 'value' }, null)).toBeNull();
    expect(buildAnswer({ kind: 'unsupported', reason: 'nope' }, 'anything')).toBeNull();
  });
});
