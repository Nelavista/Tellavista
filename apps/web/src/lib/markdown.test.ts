/**
 * Lesson bodies are authored content rendered by the app, so the parser and the
 * link allow-list are tested directly: a lesson must never produce a
 * `javascript:` link, and unsupported syntax must stay literal text.
 */
import { describe, expect, it } from 'vitest';

import { parseInline, parseLessonBody, safeHref } from './markdown';

describe('safeHref', () => {
  it('allows http, https and root-relative links only', () => {
    expect(safeHref('https://example.com/a')).toBe('https://example.com/a');
    expect(safeHref('http://example.com')).toBe('http://example.com');
    expect(safeHref('/skills/paths/p1')).toBe('/skills/paths/p1');
  });

  it('refuses schemes that can execute or escape', () => {
    expect(safeHref('javascript:alert(1)')).toBeNull();
    expect(safeHref('data:text/html,<script>')).toBeNull();
    expect(safeHref('//evil.example.com')).toBeNull();
    expect(safeHref('mailto:ops@example.com')).toBeNull();
  });
});

describe('parseInline', () => {
  it('splits bold, code and links out of surrounding text', () => {
    expect(parseInline('a **b** c `d` e')).toEqual([
      { kind: 'text', text: 'a ' },
      { kind: 'strong', text: 'b' },
      { kind: 'text', text: ' c ' },
      { kind: 'code', text: 'd' },
      { kind: 'text', text: ' e' },
    ]);
  });

  it('keeps an unsafe link as literal text', () => {
    // A URL containing brackets is not a link at all, so it stays one text run.
    expect(parseInline('see [x](javascript:alert(1))')).toEqual([
      { kind: 'text', text: 'see [x](javascript:alert(1))' },
    ]);
    // A well-formed link that fails the scheme allow-list is not clickable either.
    expect(parseInline('see [x](javascript:alert)')).toEqual([
      { kind: 'text', text: 'see ' },
      { kind: 'text', text: '[x](javascript:alert)' },
    ]);
  });
});

describe('parseLessonBody', () => {
  it('parses headings, paragraphs, lists, quotes and code', () => {
    const blocks = parseLessonBody(
      [
        '# Title',
        '',
        'First paragraph',
        'continued here.',
        '',
        '- one',
        '- two',
        '',
        '> note',
        '',
        '```',
        'raw',
        '```',
      ].join('\n'),
    );

    expect(blocks.map((block) => block.kind)).toEqual(['heading', 'paragraph', 'list', 'quote', 'code']);
    expect(blocks[0]).toMatchObject({ kind: 'heading', level: 1 });
    expect(blocks[1]).toMatchObject({ kind: 'paragraph' });
    expect(blocks[2]).toMatchObject({ kind: 'list' });
    expect(blocks[4]).toMatchObject({ kind: 'code', text: 'raw' });
  });

  it('treats unsupported syntax as plain text', () => {
    const blocks = parseLessonBody('| table | style |');
    expect(blocks).toEqual([{ kind: 'paragraph', inline: [{ kind: 'text', text: '| table | style |' }] }]);
  });

  it('returns no blocks for an empty body', () => {
    expect(parseLessonBody('')).toEqual([]);
  });
});
