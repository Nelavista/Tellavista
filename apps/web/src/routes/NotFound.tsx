import * as React from 'react';
import { Link } from 'react-router-dom';

import { EditorialImage } from '../components/EditorialImage';

export function NotFound(): JSX.Element {
  return (
    <section className="nv-container nv-section">
      <div className="nv-state-layout">
        <div className="nv-state-layout__copy">
          <p className="nv-404__code">404 / not found</p>
          <h1 className="nv-h1">That page is not part of the record.</h1>
          <p className="nv-lede">
            The link may be old, mistyped or from a product that is no longer switched on. Nothing was
            deleted from your account.
          </p>
          <div className="nv-row">
            <Link className="nv-button" to="/">
              Go to the home page
            </Link>
            <Link className="nv-button nv-button--secondary" to="/login">
              Sign in
            </Link>
          </div>
        </div>
        <EditorialImage
          alt="A blank signpost at a fork in a quiet path."
          height={1024}
          name="error-404"
          width={1024}
        />
      </div>
    </section>
  );
}
