import * as React from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';

import { Layout } from './components/Layout';
import { SessionProvider, useSession } from './lib/session';
import { Home } from './routes/Home';
import { Landing } from './routes/Landing';
import { Login } from './routes/Login';
import { Onboarding } from './routes/Onboarding';
import { Signup } from './routes/Signup';

function Loading(): JSX.Element {
  return (
    <div className="nv-card nv-card--narrow">
      <p className="nv-muted" role="status">
        Loading…
      </p>
    </div>
  );
}

/** Guards the signed-in area; keeps the attempted URL so login can return to it. */
function RequireAuth({ children }: { children: React.ReactNode }): JSX.Element {
  const { status } = useSession();
  const location = useLocation();
  if (status === 'loading') return <Loading />;
  if (status === 'anonymous') {
    return <Navigate to="/login" replace state={{ from: `${location.pathname}${location.search}` }} />;
  }
  return <>{children}</>;
}

/** Signed-in users never need the auth screens. */
function PublicOnly({ children }: { children: React.ReactNode }): JSX.Element {
  const { status } = useSession();
  if (status === 'loading') return <Loading />;
  if (status === 'authenticated') return <Navigate to="/home" replace />;
  return <>{children}</>;
}

function RouteTable(): JSX.Element {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route
          path="/signup"
          element={
            <PublicOnly>
              <Signup />
            </PublicOnly>
          }
        />
        <Route
          path="/login"
          element={
            <PublicOnly>
              <Login />
            </PublicOnly>
          }
        />
        <Route
          path="/onboarding"
          element={
            <RequireAuth>
              <Onboarding />
            </RequireAuth>
          }
        />
        <Route
          path="/home"
          element={
            <RequireAuth>
              <Home />
            </RequireAuth>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}

export function App(): JSX.Element {
  return (
    <SessionProvider>
      <RouteTable />
    </SessionProvider>
  );
}
