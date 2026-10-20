/**
 * Deep links and universal links (D1).
 *
 * Two shapes reach the app: `nelavista://skills/…` and
 * `https://nelavista.com/skills/…`. Both resolve to the same typed route, so a
 * shared link from an email opens the same screen as an in-app tap. Unknown
 * paths return null rather than a crash or a silent home redirect.
 */

export type Route =
  | { name: 'home' }
  | { name: 'skills' }
  | { name: 'skill'; slug: string }
  | { name: 'path'; slug: string }
  | { name: 'lesson'; slug: string }
  | { name: 'practice'; id: number }
  | { name: 'verification' }
  | { name: 'assessment'; slug: string }
  | { name: 'transcript' }
  | { name: 'opportunities' }
  | { name: 'opportunity'; slug: string }
  | { name: 'work' }
  | { name: 'assignment'; id: number }
  | { name: 'earnings' }
  | { name: 'notifications' }
  | { name: 'settings' };

const HOSTS = new Set(['nelavista.com', 'www.nelavista.com', 'api-dev.nelavista.com']);

function pathOf(url: string): string[] | null {
  let pathname: string;
  try {
    const parsed = new URL(url);
    if (parsed.protocol === 'nelavista:') {
      // `nelavista://skills/lesson` puts "skills" in the host position.
      pathname = `${parsed.host}${parsed.pathname}`;
    } else if (HOSTS.has(parsed.host) && parsed.protocol === 'https:') {
      pathname = parsed.pathname;
    } else {
      return null;
    }
  } catch {
    return null;
  }
  return pathname.split('/').filter((part) => part.length > 0);
}

export function parseDeepLink(url: string): Route | null {
  const parts = pathOf(url);
  if (parts === null) return null;
  const [head, second, third] = parts;

  if (!head || head === 'home') return { name: 'home' };
  if (head === 'practice' && second && Number.isInteger(Number(second))) {
    return { name: 'practice', id: Number(second) };
  }
  if (head === 'skills') {
    if (second === 'paths' && third) return { name: 'path', slug: third };
    if (second === 'lessons' && third) return { name: 'lesson', slug: third };
    if (second === 'tasks' && third && Number.isInteger(Number(third))) {
      return { name: 'practice', id: Number(third) };
    }
    if (second) return { name: 'skill', slug: second };
    return { name: 'skills' };
  }
  if (head === 'verification') {
    if (second === 'assessments' && third) return { name: 'assessment', slug: third };
    return { name: 'verification' };
  }
  if (head === 'transcript') return { name: 'transcript' };
  if (head === 'opportunities') {
    return second ? { name: 'opportunity', slug: second } : { name: 'opportunities' };
  }
  if (head === 'work') {
    if (second === 'assignments' && third && Number.isInteger(Number(third))) {
      return { name: 'assignment', id: Number(third) };
    }
    return { name: 'work' };
  }
  if (head === 'earnings') return { name: 'earnings' };
  if (head === 'notifications') return { name: 'notifications' };
  if (head === 'settings') return { name: 'settings' };
  return null;
}
