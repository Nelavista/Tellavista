/**
 * The Skill Transcript (B7).
 *
 * Three kinds, always in the same order and always backed by evidence:
 * learned (a real lesson progress row), proved (a passed assessment or practical)
 * and delivered (approved work). Each line names its evidence, because a
 * transcript that a student cannot point at is a claim, not a record.
 */
import type { TranscriptEntryOut, TranscriptOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

const SECTIONS: Array<{ kind: 'learned' | 'proved' | 'delivered'; title: string; note: string }> = [
  { kind: 'learned', title: 'Learned', note: 'Lessons you finished. Progress — not proof.' },
  { kind: 'proved', title: 'Proved', note: 'Assessments and practical work you passed.' },
  { kind: 'delivered', title: 'Delivered', note: 'Real work approved for a client, with its evidence.' },
];

function Entry({ entry }: { entry: TranscriptEntryOut }): JSX.Element {
  return (
    <li className="nv-card">
      <div className="nv-row nv-row--between">
        <h3 className="nv-h2">{entry.title}</h3>
        <span className="nv-muted">{formatDateTime(entry.occurred_at)}</span>
      </div>
      <p className="nv-muted">
        {entry.skill && entry.skill_slug ? (
          <>
            <Link to={`/skills/${entry.skill_slug}`}>{entry.skill}</Link>
            {' · '}
          </>
        ) : null}
        evidence: {entry.evidence.type} #{entry.evidence.id}
      </p>
    </li>
  );
}

export function Transcript(): JSX.Element {
  const { resource, reload } = useApiResource<TranscriptOut>('/verification/transcript');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your transcript">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Skill transcript</h1>
        <p className="nv-banner">Verification is not switched on for this environment yet.</p>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Skill transcript</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
      </div>
    );
  }

  const transcript = resource.data;
  const total = transcript.entries.length;

  return (
    <div className="nv-stack">
      <p className="nv-muted">
        <Link to="/verification">Verification</Link>
      </p>
      <h1 className="nv-h1">Skill transcript</h1>
      <p className="nv-muted">
        Every line is backed by a record you can open. Nothing here can be typed in by hand.
      </p>

      {total === 0 ? (
        <p className="nv-banner">
          Nothing recorded yet. Finish a lesson or pass an assessment and it appears here with its evidence.
        </p>
      ) : (
        SECTIONS.map((section) => {
          const entries = transcript[section.kind];
          return (
            <section className="nv-stack" key={section.kind}>
              <h2 className="nv-h2">
                {section.title} <span className="nv-muted">({transcript.counts[section.kind]})</span>
              </h2>
              <p className="nv-muted">{section.note}</p>
              {entries.length === 0 ? (
                <p className="nv-muted">Nothing in this group yet.</p>
              ) : (
                <ul className="nv-list">
                  {entries.map((entry) => (
                    <Entry entry={entry} key={entry.id} />
                  ))}
                </ul>
              )}
            </section>
          );
        })
      )}
    </div>
  );
}
