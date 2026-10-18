import * as React from 'react';
import { Link } from 'react-router-dom';

export function Landing(): JSX.Element {
  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Learn it. Prove it. Get paid for it.</h1>
      <p className="nv-muted">
        Nelavista verifies what you actually know, then matches you to paid work you can do from your phone.
      </p>
      <div className="nv-row">
        <Link className="nv-button" to="/signup">
          Create your account
        </Link>
        <Link className="nv-button nv-button--ghost" to="/login">
          I already have one
        </Link>
      </div>

      <section className="nv-card">
        <h2 className="nv-h2">Two ways in, one account</h2>
        <ul className="nv-list">
          <li>
            <strong>Academia</strong> — your courses, materials and CBT practice, plus verified academic work.
          </li>
          <li>
            <strong>Skills</strong> — short lessons, tasks and a public proof of your ability.
          </li>
        </ul>
        <p className="nv-muted">
          You can switch path at any time. Switching never deletes your learning, proof or earnings.
        </p>
      </section>
    </div>
  );
}
