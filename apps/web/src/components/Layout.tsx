import { VersionSwitcher } from '@nelavista/ui';
import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useSession } from '../lib/session';

export function Layout({ children }: { children: React.ReactNode }): JSX.Element {
  const { status, logout } = useSession();
  const navigate = useNavigate();

  async function onSignOut(): Promise<void> {
    await logout();
    navigate('/');
  }

  return (
    <div className="nv-page">
      <nav className="nv-nav">
        <Link className="nv-brand" to="/">
          Nelavista
        </Link>
        <div className="nv-row">
          <VersionSwitcher />
          {status === 'authenticated' ? (
            <>
              <Link to="/home">Home</Link>
              <Link to="/academia">Academia</Link>
              <Link to="/skills">Skills</Link>
              <Link to="/skills/my-learning">My learning</Link>
              <Link to="/verification">Verification</Link>
              <Link to="/opportunities">Opportunities</Link>
              <Link to="/work">Work</Link>
              <Link to="/earnings">Earnings</Link>
              <Link to="/transcript">Transcript</Link>
              <Link to="/campus">Campus</Link>
              <Link to="/settings">Settings</Link>
              <button className="nv-button nv-button--ghost" type="button" onClick={onSignOut}>
                Sign out
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Sign in</Link>
              <Link className="nv-button" to="/signup">
                Create account
              </Link>
            </>
          )}
        </div>
      </nav>
      <main className="nv-main">{children}</main>
    </div>
  );
}
