import { BrandLoader, ConfirmDialog } from '@nelavista/ui';
import * as React from 'react';

import { Shell } from './components/Shell';
import { useHashRoute } from './lib/route';
import { SessionProvider, useSession } from './lib/session';
import { AdminNotFound } from './routes/AdminNotFound';
import { Audit } from './routes/Audit';
import { Campus } from './routes/Campus';
import { Content } from './routes/Content';
import { Imports } from './routes/Imports';
import { Login } from './routes/Login';
import { Money } from './routes/Money';
import { Opportunities } from './routes/Opportunities';
import { Overview } from './routes/Overview';
import { Platform } from './routes/Platform';
import { Projects } from './routes/Projects';
import { Review } from './routes/Review';
import { Security } from './routes/Security';
import { TwoFactor } from './routes/TwoFactor';
import { Users } from './routes/Users';
import { Waitlist } from './routes/Waitlist';

function Screen({ route }: { route: string }): JSX.Element {
  if (route.startsWith('/overview')) return <Overview />;
  if (route.startsWith('/imports')) return <Imports />;
  if (route.startsWith('/users')) return <Users />;
  if (route.startsWith('/waitlist')) return <Waitlist />;
  if (route.startsWith('/opportunities')) return <Opportunities />;
  if (route.startsWith('/work')) return <Projects />;
  if (route.startsWith('/review')) return <Review />;
  if (route.startsWith('/money')) return <Money />;
  if (route.startsWith('/content')) return <Content />;
  if (route.startsWith('/campus')) return <Campus />;
  if (route.startsWith('/platform')) return <Platform />;
  if (route.startsWith('/security')) return <Security />;
  if (route.startsWith('/audit')) return <Audit />;
  return <AdminNotFound route={route} />;
}

function Body(): JSX.Element {
  const { status, me, mfa } = useSession();
  const [route, go] = useHashRoute();

  if (status === 'loading') {
    return <BrandLoader full label="Loading Nelavista Admin" />;
  }

  if (status === 'anonymous') return <Login />;

  if (me && me.role === 'student') {
    return (
      <div className="nv-card nv-login">
        <h1 className="nv-h1">Staff only</h1>
        <p>
          This account is a student account. The ops tools are not available to it; use the student web app
          instead.
        </p>
        <SignOut />
      </div>
    );
  }

  // C8: no ops screen renders until a second factor is enrolled.
  if (!mfa?.enabled) {
    return (
      <div className="nv-login">
        <TwoFactor />
      </div>
    );
  }

  return (
    <Shell route={route} go={go}>
      <Screen route={route} />
    </Shell>
  );
}

function SignOut(): JSX.Element {
  const { logout } = useSession();
  const [confirmOpen, setConfirmOpen] = React.useState(false);
  const [busy, setBusy] = React.useState(false);

  async function signOut(): Promise<void> {
    setBusy(true);
    try {
      await logout();
      setConfirmOpen(false);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <button className="nv-button nv-button--ghost" type="button" onClick={() => setConfirmOpen(true)}>
        Sign out
      </button>
      <ConfirmDialog
        body={<p>This staff-only screen will close. You will need your password to sign in again.</p>}
        busy={busy}
        busyLabel="Signing out"
        confirmLabel="Sign out"
        onCancel={() => setConfirmOpen(false)}
        onConfirm={() => void signOut()}
        open={confirmOpen}
        title="Are you sure you want to sign out?"
      />
    </>
  );
}

export function App(): JSX.Element {
  return (
    <SessionProvider>
      <Body />
    </SessionProvider>
  );
}
