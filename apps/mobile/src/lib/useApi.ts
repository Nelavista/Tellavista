/** One read, reloadable, with the API's own message on failure. */
import * as React from 'react';

import { ApiError, UpgradeRequired, api } from './api';

export type Remote<T> =
  | { status: 'loading' }
  | { status: 'ready'; data: T }
  | { status: 'error'; message: string; code?: string }
  | { status: 'upgrade'; minVersion?: string; storeUrl?: string };

export function useApi<T>(path: string | null): { remote: Remote<T>; reload: () => void } {
  const [remote, setRemote] = React.useState<Remote<T>>({ status: 'loading' });
  const [attempt, setAttempt] = React.useState(0);

  React.useEffect(() => {
    if (path === null) return;
    let cancelled = false;
    setRemote({ status: 'loading' });
    void (async () => {
      try {
        const data = await api.get<T>(path);
        if (!cancelled) setRemote({ status: 'ready', data });
      } catch (err) {
        if (cancelled) return;
        if (err instanceof UpgradeRequired) {
          setRemote({ status: 'upgrade', minVersion: err.minVersion, storeUrl: err.storeUrl });
          return;
        }
        setRemote({
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

  return { remote, reload: () => setAttempt((n) => n + 1) };
}
