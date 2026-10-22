/**
 * Session state for the whole app. One provider, one bootstrap.
 *
 * On load we try a single refresh (the httpOnly cookie may still be valid) and
 * then fetch /me. Anything else stays anonymous — no flash of a signed-in shell,
 * and a dead cookie cannot wedge the UI in a retry loop.
 */
import type { MeOut, TokenOut } from '@nelavista/api-client';
import type { Profile } from '@nelavista/contracts';
import * as React from 'react';

import { http, refreshSession, setAccessToken } from './http';
import { clearApiCache } from './offline';

export type SessionStatus = 'loading' | 'anonymous' | 'authenticated';

export interface SignupInput {
  name?: string;
  email: string;
  username: string;
  password: string;
}

interface SessionValue {
  status: SessionStatus;
  me: MeOut | null;
  profile: Profile | null;
  signup: (input: SignupInput) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  reload: () => Promise<void>;
}

const SessionContext = React.createContext<SessionValue | null>(null);

export function SessionProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const [status, setStatus] = React.useState<SessionStatus>('loading');
  const [me, setMe] = React.useState<MeOut | null>(null);
  const [profile, setProfile] = React.useState<Profile | null>(null);

  const load = React.useCallback(async (): Promise<void> => {
    const [user, prof] = await Promise.all([http.get<MeOut>('/auth/me'), http.get<Profile>('/me')]);
    setMe(user);
    setProfile(prof);
    setStatus('authenticated');
  }, []);

  React.useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        // Purge any API cache written by an older build before restoring a
        // session, so a previous account's data cannot be read offline.
        await clearApiCache();
        const restored = await refreshSession();
        if (!restored) {
          if (!cancelled) setStatus('anonymous');
          return;
        }
        const [user, prof] = await Promise.all([http.get<MeOut>('/auth/me'), http.get<Profile>('/me')]);
        if (cancelled) return;
        setMe(user);
        setProfile(prof);
        setStatus('authenticated');
      } catch {
        if (!cancelled) setStatus('anonymous');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const signup = React.useCallback(
    async (input: SignupInput): Promise<void> => {
      const token = await http.post<TokenOut>('/auth/signup', {
        ...input,
        accept_terms: true,
        platform: 'web',
      });
      setAccessToken(token.access_token);
      await clearApiCache();
      await load();
    },
    [load],
  );

  const login = React.useCallback(
    async (email: string, password: string): Promise<void> => {
      const token = await http.post<TokenOut>('/auth/login', {
        email,
        password,
        platform: 'web',
      });
      setAccessToken(token.access_token);
      await clearApiCache();
      await load();
    },
    [load],
  );

  const logout = React.useCallback(async (): Promise<void> => {
    try {
      await http.post('/auth/logout');
    } finally {
      // A different account may sign in on this device; no cached response may
      // outlive the previous session.
      await clearApiCache();
      setAccessToken(null);
      setMe(null);
      setProfile(null);
      setStatus('anonymous');
    }
  }, []);

  const value = React.useMemo<SessionValue>(
    () => ({ status, me, profile, signup, login, logout, reload: load }),
    [status, me, profile, signup, login, logout, load],
  );

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession(): SessionValue {
  const value = React.useContext(SessionContext);
  if (!value) throw new Error('useSession must be used inside <SessionProvider>');
  return value;
}

/**
 * The session when a provider is present, otherwise null. Screens that only need
 * an identity for a storage key use this so they can still render in isolation
 * (the route tests mount a single screen, not the whole app).
 */
export function useSessionOptional(): SessionValue | null {
  return React.useContext(SessionContext);
}
