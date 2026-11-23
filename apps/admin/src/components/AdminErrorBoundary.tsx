import * as React from 'react';

import { reportError } from '../lib/telemetry';

interface State {
  error: Error | null;
}

/**
 * Last resort for a render crash in the ops app.
 *
 * The shell is a tool, not a student screen: the most useful thing it can do is
 * keep the navigation usable and name the error. The report is best effort and
 * never replaces the message.
 */
export class AdminErrorBoundary extends React.Component<{ children: React.ReactNode }, State> {
  override state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  override componentDidCatch(error: Error, info: React.ErrorInfo): void {
    console.error('Nelavista admin UI error', error, info.componentStack);
    reportError(error, {
      source: 'admin-react-error-boundary',
      component_stack: info.componentStack ?? '',
      route: window.location.hash.replace(/^#/, '') || '/',
    });
  }

  override render(): React.ReactNode {
    if (!this.state.error) return this.props.children;
    return (
      <div className="nv-login">
        <div className="nv-card nv-login__card">
          <p className="nv-eyebrow">Something broke</p>
          <h1 className="nv-h1">This ops screen did not finish loading.</h1>
          <p>
            The failure has been logged with its route. Reload the screen to try again; if it keeps happening,
            use the audit trail to check whether the write before it completed.
          </p>
          <pre className="nv-code" aria-label="Error reference">
            <code>{this.state.error.message || 'Unknown admin UI error'}</code>
          </pre>
          <div className="nv-row">
            <button className="nv-button" type="button" onClick={() => window.location.reload()}>
              Reload
            </button>
            <a className="nv-button nv-button--secondary" href="#/overview">
              Back to operations
            </a>
          </div>
        </div>
      </div>
    );
  }
}
