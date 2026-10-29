import { ClipboardCheck, History } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { Banner, EmptyState, PageHeader } from '../ui';

export function CbtHistory(): JSX.Element {
  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Academia · CBT"
        title="CBT history"
        description="The attempt trail is the part of practice that makes a score useful: what you answered, when, and what changed."
        actions={
          <Link className="nv-button" to="/academia/cbt">
            Start practice
          </Link>
        }
      />

      <Banner tone="warning">
        <strong>Backend dependency.</strong> V2 does not expose a CBT attempt-history endpoint yet. This
        screen is the agreed destination; it must not invent a history or hide the current practice summary
        behind a fake list.
      </Banner>

      <div className="nv-grid--2">
        <section className="nv-panel">
          <div className="nv-panel__head">
            <h2 className="nv-h3">What this screen will show</h2>
            <History aria-hidden="true" size={18} />
          </div>
          <div className="nv-panel__body">
            <ul className="nv-list">
              <li>
                <strong>Attempt list.</strong> Course, topic, date, score and duration for each sitting.
              </li>
              <li>
                <strong>Attempt review.</strong> The questions, your answer, the correct answer and the
                explanation.
              </li>
              <li>
                <strong>Trend.</strong> Topic-level change over time, not just the last score.
              </li>
              <li>
                <strong>Next action.</strong> A direct route back to the weak topic or the next practice set.
              </li>
            </ul>
          </div>
        </section>

        <section className="nv-panel">
          <div className="nv-panel__head">
            <h2 className="nv-h3">What works today</h2>
            <ClipboardCheck aria-hidden="true" size={18} />
          </div>
          <div className="nv-panel__body nv-stack">
            <p className="nv-muted">
              Current CBT practice returns a result, topic strengths and weaknesses, and a recommendation. Use
              that summary now; the history route will replace the gap when the API lands.
            </p>
            <Link className="nv-link-arrow" to="/academia/cbt">
              Open current CBT practice
            </Link>
          </div>
        </section>
      </div>

      <EmptyState
        title="No attempt history is available"
        body="This is a dependency state, not an empty student record. The API change is listed in the V2 UI parity map."
        image={EMPTY_IMAGES.cbt}
        action={
          <Link className="nv-button nv-button--secondary" to="/academia">
            Back to Academia
          </Link>
        }
      />
    </div>
  );
}
