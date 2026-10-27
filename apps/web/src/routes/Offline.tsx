import * as React from 'react';
import { Link } from 'react-router-dom';

export function Offline(): JSX.Element {
  return (
    <section className="nv-container nv-offline">
      <p className="nv-404__code">Offline</p>
      <h1 className="nv-h1">The shell is here. The data is not.</h1>
      <p className="nv-lede">
        Nelavista does not cache signed-in API data, so a stale balance or a previous account&apos;s record
        cannot appear offline. Reconnect and the screen will load again.
      </p>
      <div className="nv-row">
        <button className="nv-button" type="button" onClick={() => window.location.reload()}>
          Try again
        </button>
        <Link className="nv-button nv-button--secondary" to="/">
          Home
        </Link>
      </div>
    </section>
  );
}
