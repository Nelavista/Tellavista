import { TriangleAlert } from 'lucide-react';
import * as React from 'react';

interface State {
  error: Error | null;
}

export class ErrorBoundary extends React.Component<{ children: React.ReactNode }, State> {
  override state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  override componentDidCatch(error: Error, info: React.ErrorInfo): void {
    // Keep the console useful in local/dev. A real error tracker is a launch
    // dependency; do not pretend this is one.
    console.error('Nelavista UI error', error, info.componentStack);
  }

  override render(): React.ReactNode {
    if (!this.state.error) return this.props.children;
    return (
      <main className="nv-container nv-404" id="main">
        <TriangleAlert aria-hidden="true" size={24} />
        <p className="nv-404__code">Something broke</p>
        <h1 className="nv-h1">This screen did not finish loading.</h1>
        <p className="nv-lede">
          Your account and saved work are safe. Reload the page. If it keeps happening, send the reference
          below to support.
        </p>
        <pre className="nv-code" aria-label="Error reference">
          <code>{this.state.error.message || 'Unknown UI error'}</code>
        </pre>
        <div className="nv-row">
          <button className="nv-button" type="button" onClick={() => window.location.reload()}>
            Reload the page
          </button>
          <a className="nv-button nv-button--secondary" href="/">
            Go to the home page
          </a>
        </div>
      </main>
    );
  }
}
