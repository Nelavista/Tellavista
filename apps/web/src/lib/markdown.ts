/**
 * The markdown subset a lesson body uses, parsed into blocks and inline runs.
 *
 * Lesson bodies are content, authored by ops (PRD §4), so they arrive as
 * markdown. The app renders them itself rather than pulling in a markdown
 * library plus a sanitiser: the bundle is a budget (B12), lesson markdown is a
 * small, known subset, and building elements directly means there is no HTML
 * string to sanitise in the first place.
 *
 * Supported: `#`–`###` headings, paragraphs, `-`/`*` lists, `>` quotes, fenced
 * code, and inline `**bold**`, `` `code` `` and `[text](url)` links. Anything
 * else renders as its own text, never as markup.
 */

export type Inline =
  { kind: 'text' | 'strong' | 'code'; text: string } | { kind: 'link'; text: string; href: string };

export type Block =
  | { kind: 'heading'; level: number; inline: Inline[] }
  | { kind: 'paragraph'; inline: Inline[] }
  | { kind: 'list'; items: Inline[][] }
  | { kind: 'quote'; inline: Inline[] }
  | { kind: 'code'; text: string };

/** Only these schemes are ever made clickable; a lesson cannot link to `javascript:`. */
export function safeHref(raw: string): string | null {
  const href = raw.trim();
  if (href.startsWith('https://') || href.startsWith('http://')) return href;
  if (href.startsWith('/') && !href.startsWith('//')) return href;
  return null;
}

const STRONG = /\*\*([^*]+)\*\*/;
const CODE = /`([^`]+)`/;
// A URL here may not contain brackets or whitespace: lessons do not need
// parenthesised URLs, and refusing them keeps a trailing ")" from being eaten.
const LINK = /\[([^\]]+)\]\(([^()\s]+)\)/;

/** A matched inline token, with where it starts in the text being scanned. */
type Token = {
  start: number;
  value: string;
  kind: 'link' | 'strong' | 'code';
  match: RegExpExecArray;
};

export function parseInline(text: string): Inline[] {
  const runs: Inline[] = [];
  let rest = text;

  while (rest.length > 0) {
    const link = LINK.exec(rest);
    const strong = STRONG.exec(rest);
    const code = CODE.exec(rest);

    // Take whichever token starts earliest.
    const candidates: Token[] = [];
    if (link) candidates.push({ start: link.index, value: link[0], kind: 'link', match: link });
    if (strong) candidates.push({ start: strong.index, value: strong[0], kind: 'strong', match: strong });
    if (code) candidates.push({ start: code.index, value: code[0], kind: 'code', match: code });

    if (candidates.length === 0) {
      runs.push({ kind: 'text', text: rest });
      break;
    }

    const next = candidates.reduce((a, b) => (b.start < a.start ? b : a));
    if (next.start > 0) runs.push({ kind: 'text', text: rest.slice(0, next.start) });

    if (next.kind === 'link') {
      const href = safeHref(next.match[2] ?? '');
      runs.push(
        href ? { kind: 'link', text: next.match[1] ?? '', href } : { kind: 'text', text: next.value },
      );
    } else if (next.kind === 'strong') {
      runs.push({ kind: 'strong', text: next.match[1] ?? '' });
    } else {
      runs.push({ kind: 'code', text: next.match[1] ?? '' });
    }
    rest = rest.slice(next.start + next.value.length);
  }

  return runs;
}

export function parseLessonBody(body: string): Block[] {
  const blocks: Block[] = [];
  const lines = body.replace(/\r\n/g, '\n').split('\n');

  let paragraph: string[] = [];
  let list: string[] = [];
  let quote: string[] = [];
  let fence: string[] | null = null;

  function flush(): void {
    if (paragraph.length > 0) {
      blocks.push({ kind: 'paragraph', inline: parseInline(paragraph.join(' ')) });
      paragraph = [];
    }
    if (list.length > 0) {
      blocks.push({ kind: 'list', items: list.map((item) => parseInline(item)) });
      list = [];
    }
    if (quote.length > 0) {
      blocks.push({ kind: 'quote', inline: parseInline(quote.join(' ')) });
      quote = [];
    }
  }

  for (const line of lines) {
    if (fence !== null) {
      if (line.trim().startsWith('```')) {
        blocks.push({ kind: 'code', text: fence.join('\n') });
        fence = null;
      } else {
        fence.push(line);
      }
      continue;
    }

    const trimmed = line.trim();
    if (trimmed.startsWith('```')) {
      flush();
      fence = [];
      continue;
    }

    if (trimmed.length === 0) {
      flush();
      continue;
    }

    const heading = /^(#{1,3})\s+(.*)$/.exec(trimmed);
    if (heading) {
      flush();
      blocks.push({
        kind: 'heading',
        level: (heading[1] ?? '#').length,
        inline: parseInline(heading[2] ?? ''),
      });
      continue;
    }

    const bullet = /^[-*]\s+(.*)$/.exec(trimmed);
    if (bullet) {
      if (paragraph.length > 0 || quote.length > 0) flush();
      list.push(bullet[1] ?? '');
      continue;
    }

    const quoted = /^>\s?(.*)$/.exec(trimmed);
    if (quoted) {
      if (paragraph.length > 0 || list.length > 0) flush();
      quote.push(quoted[1] ?? '');
      continue;
    }

    if (list.length > 0 || quote.length > 0) flush();
    paragraph.push(trimmed);
  }

  // An unclosed fence still renders as code: dropping the text would be worse.
  if (fence !== null) blocks.push({ kind: 'code', text: fence.join('\n') });
  flush();
  return blocks;
}
