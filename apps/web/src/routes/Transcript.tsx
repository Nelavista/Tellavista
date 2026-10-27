/**
 * The Skill Transcript (B7).
 *
 * Three kinds, always in the same order and always backed by evidence:
 * learned (a real lesson progress row), proved (a passed assessment or practical)
 * and delivered (approved work). Each line names its evidence, because a
 * transcript that a student cannot point at is a claim, not a record.
 */
import type { TranscriptEntryOut, TranscriptOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { FileCheck2 } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';

const SECTIONS: Array<{ kind: 'learned' | 'proved' | 'delivered'; title: string; note: string }> = [
  { kind: 'learned', title: 'Learned', note: 'Lessons you finished. Progress — not proof.' },
  { kind: 'proved', title: 'Proved', note: 'Assessments and practical work you passed.' },
  { kind: 'delivered', title: 'Delivered', note: 'Real work approved for a client, with its evidence.' },
];

function EntryRow({ entry }: { entry: TranscriptEntryOut }): JSX.Element {
  return (
    <tr>
      <td>
        <p>{entry.title}</p>
        {entry.skill && entry.skill_slug ? (
          <Link className="nv-meta" to={`/skills/${entry.skill_slug}`}>
            {entry.skill}
          </Link>
        ) : null}
      </td>
      <td className="nv-mono">
        {entry.evidence.type} #{entry.evidence.id}
      </td>
      <td>{formatDateTime(entry.occurred_at)}</td>
    </tr>
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
        <PageHeader eyebrow="Prove" title="Skill transcript" />
        <Banner tone="info">
          <p>Verification is not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="Skill transcript" />
        <ErrorState
          body={resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const transcript = resource.data;
  const total = transcript.entries.length;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Prove"
        title="Skill transcript"
        description="Every line is backed by a record you can open. Nothing here can be typed in by hand."
        actions={
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/verification">
            Verification
          </Link>
        }
      />

      {total === 0 ? (
        <EmptyState
          body="Finish a lesson or pass an assessment and it appears here with its evidence."
          icon={FileCheck2}
          title="Nothing recorded yet"
          action={
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/verification">
              Start an assessment
            </Link>
          }
        />
      ) : (
        SECTIONS.map((section) => {
          const entries = transcript[section.kind];
          return (
            <Panel
              key={section.kind}
              title={section.title}
              actions={
                <Badge tone={section.kind === 'proved' ? 'success' : 'neutral'}>
                  {transcript.counts[section.kind]}
                </Badge>
              }
            >
              <p className="nv-muted">{section.note}</p>
              {entries.length === 0 ? (
                <EmptyState body="Nothing in this group yet." icon={FileCheck2} title="Empty" />
              ) : (
                <div className="nv-table-wrap">
                  <table className="nv-table">
                    <thead>
                      <tr>
                        <th>Record</th>
                        <th>Evidence</th>
                        <th>When</th>
                      </tr>
                    </thead>
                    <tbody>
                      {entries.map((entry) => (
                        <EntryRow entry={entry} key={entry.id} />
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </Panel>
          );
        })
      )}
    </div>
  );
}
