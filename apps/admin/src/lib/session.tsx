/**
 * Admin session. A staff account, an access token in memory, and the MFA state
 * the shell blocks on.
 */
import type { MeOut, MfaStatusOut, TokenOut } from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http, refreshSession, setAccessToken } from './http';

type Status = 'loading' | 'anonymous' | 'authenticated';

interface SessionValue {
  status: Status;
  me: MeOut | null;
  mfa: MfaStatusOut | null;
  login: (email: string, password: string) => Promise<void>;
  verifyMfa: (challenge: string, code: string) => Promise<void>;
  logout: () => Promise<void>;
  reload: () => Promise<void>;
}

const Context = React.createContext<SessionValue | null>(null);

export function SessionProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const [status, setStatus] = React.useState<Status>('loading');
  const [me, setMe] = React.useState<MeOut | null>(null);
  const [mfa, setMfa] = React.useState<MfaStatusOut | null>(null);

  const load = React.useCallback(async (): Promise<void> => {
    const [user, mfaStatus] = await Promise.all([
      http.get<MeOut>('/auth/me'),
      http.get<MfaStatusOut>('/auth/2fa'),
    ]);
    setMe(user);
    setMfa(mfaStatus);
    setStatus('authenticated');
  }, []);

  React.useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        if (!(await refreshSession())) {
          if (!cancelled) setStatus('anonymous');
          return;
        }
        const [user, mfaStatus] = await Promise.all([
          http.get<MeOut>('/auth/me'),
          http.get<MfaStatusOut>('/auth/2fa'),
        ]);
        if (cancelled) return;
        setMe(user);
        setMfa(mfaStatus);
        setStatus('authenticated');
      } catch {
        if (!cancelled) setStatus('anonymous');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = React.useCallback(
    async (email: string, password: string): Promise<void> => {
      const token = await http.post<TokenOut>('/auth/login', {
        email,
        password,
        platform: 'admin',
      });
      setAccessToken(token.access_token);
      await load();
    },
    [load],
  );

  const verifyMfa = React.useCallback(
    async (challenge: string, code: string): Promise<void> => {
      const token = await http.post<TokenOut>('/auth/2fa/verify', {
        mfa_token: challenge,
        code,
      });
      setAccessToken(token.access_token);
      await load();
    },
    [load],
  );

  const logout = React.useCallback(async (): Promise<void> => {
    try {
      await http.post('/auth/logout');
    } catch {
      // A dead session is still a signed-out session.
    } finally {
      setAccessToken(null);
      setMe(null);
      setMfa(null);
      setStatus('anonymous');
    }
  }, []);

  const value = React.useMemo<SessionValue>(
    () => ({ status, me, mfa, login, verifyMfa, logout, reload: load }),
    [status, me, mfa, login, verifyMfa, logout, load],
  );
  return <Context.Provider value={value}>{children}</Context.Provider>;
}

export function useSession(): SessionValue {
  const value = React.useContext(Context);
  if (!value) throw new Error('useSession must be used inside <SessionProvider>');
  return value;
}

/** Re-exported so the login screen can surface the challenge without guessing. */
export { ApiError };
