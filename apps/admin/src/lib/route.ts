/**
 * A tiny hash router.
 *
 * The admin app has a handful of flat screens and no need for a routing
 * dependency: `#/overview` is the whole protocol. Keeping it in-repo means the
 * ops bundle has one fewer package and no second source of route truth.
 */
import * as React from 'react';

export function useHashRoute(): [string, (next: string) => void] {
  const read = (): string => {
    const raw = window.location.hash.replace(/^#/, '');
    return raw === '' ? '/overview' : raw;
  };
  const [route, setRoute] = React.useState(read);

  React.useEffect(() => {
    const onChange = (): void => setRoute(read());
    window.addEventListener('hashchange', onChange);
    return () => window.removeEventListener('hashchange', onChange);
  }, []);

  const go = React.useCallback((next: string) => {
    window.location.hash = next.startsWith('/') ? next : `/${next}`;
    setRoute(next.startsWith('/') ? next : `/${next}`);
  }, []);

  return [route, go];
}
