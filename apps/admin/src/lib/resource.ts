/** One read with an honest error, shared by every ops screen. */
import * as React from 'react';

import { ApiError, http } from './http';

export type Resource<T> =
  | { status: 'loading' }
  | { status: 'ready'; data: T }
  | { status: 'error'; message: string; code?: string };

export function useResource<T>(path: string | null): {
  resource: Resource<T>;
  reload: () => void;
} {
  const [resource, setResource] = React.useState<Resource<T>>({ status: 'loading' });
  const [attempt, setAttempt] = React.useState(0);

  React.useEffect(() => {
    if (path === null) return;
    let cancelled = false;
    setResource({ status: 'loading' });
    void (async () => {
      try {
        const data = await http.get<T>(path);
        if (!cancelled) setResource({ status: 'ready', data });
      } catch (err) {
        if (cancelled) return;
        setResource({
          status: 'error',
          message: err instanceof ApiError ? err.message : 'Could not load this screen.',
          code: err instanceof ApiError ? err.code : undefined,
        });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [path, attempt]);

  return { resource, reload: () => setAttempt((n) => n + 1) };
}
