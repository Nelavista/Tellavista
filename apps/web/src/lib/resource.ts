/**
 * One read, four honest outcomes.
 *
 * Every journey screen distinguishes the same cases, and the difference matters
 * to the student:
 *
 * * `loading` — say nothing yet, keep the page's shape (skeletons, not spinners);
 * * `ready`   — render the data;
 * * `off`     — the whole feature is behind a server flag in this environment
 *               (the API answers 404), so say "not switched on here", not "error";
 * * `missing` — the feature is on but this row does not exist or is not the
 *               student's; show the API's own wording.
 */
import * as React from 'react';

import { ApiError, http } from './http';

export type Resource<T> =
  | { status: 'loading' }
  | { status: 'ready'; data: T }
  | { status: 'off' }
  | { status: 'missing'; message: string }
  | { status: 'error'; message: string };

export function useApiResource<T>(path: string): {
  resource: Resource<T>;
  reload: () => void;
} {
  const [resource, setResource] = React.useState<Resource<T>>({ status: 'loading' });
  const [attempt, setAttempt] = React.useState(0);

  React.useEffect(() => {
    let cancelled = false;
    setResource({ status: 'loading' });
    void (async () => {
      try {
        const data = await http.get<T>(path);
        if (!cancelled) setResource({ status: 'ready', data });
      } catch (err) {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 404) {
          // A flagged-out router answers 404 "not_found" for every path under it.
          if (err.code === 'not_found') {
            setResource({ status: 'off' });
            return;
          }
          setResource({ status: 'missing', message: err.message });
          return;
        }
        setResource({
          status: 'error',
          message: err instanceof ApiError ? err.message : 'Could not load this page.',
        });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [path, attempt]);

  const reload = React.useCallback(() => setAttempt((n) => n + 1), []);
  return { resource, reload };
}
