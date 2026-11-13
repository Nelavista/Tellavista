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

import { EMPTY_IMAGES } from '../lib/empty-images';
import { formatDateTime } from '../lib/format';
import { useApiResource } from '../lib/resource';

const SECTIONS: Array<{ kind: 'learned' | 'proved' | 'delivered'; title: string; note: string }> = [
  { kind: 'learned', title: 'Learned', note: 'Lessons you finished. Progress, not proof.' },
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

  // One row per skill, so a student or a reviewer can see which skill each piece
  // of evidence belongs to without reading three separate tables.
  const bySkill = new Map<
    string,
    {
      slug: string;
      name: string;
      learned: number;
      proved: number;
      delivered: number;
      latest: TranscriptEntryOut | null;
    }
  >();
  for (const entry of transcript.entries) {
    if (!entry.skill_slug) continue;
    const row = bySkill.get(entry.skill_slug) ?? {
      slug: entry.skill_slug,
      name: entry.skill ?? entry.skill_slug,
      learned: 0,
      proved: 0,
      delivered: 0,
      latest: null,
    };
    if (entry.kind === 'learned' || entry.kind === 'proved' || entry.kind === 'delivered') {
      row[entry.kind] += 1;
    }
    if (
      row.latest === null ||
      new Date(entry.occurred_at).getTime() > new Date(row.latest.occurred_at).getTime()
    ) {
      row.latest = entry;
    }
    bySkill.set(entry.skill_slug, row);
  }
  const skillRows = [...bySkill.values()].sort((a, b) => b.proved - a.proved || a.name.localeCompare(b.name));

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

      {total > 0 && skillRows.length > 0 ? (
        <Panel
          title="By skill"
          actions={<Badge tone="info">{skillRows.length}</Badge>}
        >
          <p className="nv-muted">
            Every line below names the record behind it. A skill is only “proved” from a passed
            assessment or reviewed practical task.
          </p>
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Learned</th>
                  <th>Proved</th>
                  <th>Delivered</th>
                  <th>Latest evidence</th>
                </tr>
              </thead>
              <tbody>
                {skillRows.map((row) => (
                  <tr key={row.slug}>
                    <td>
                      <Link to={`/skills/${row.slug}`}>{row.name}</Link>
                    </td>
                    <td>{row.learned}</td>
                    <td>{row.proved}</td>
                    <td>{row.delivered}</td>
                    <td className="nv-meta">
                      {row.latest ? (
                        <>
                          <span className="nv-mono">
                            {row.latest.evidence.type} #{row.latest.evidence.id}
                          </span>{' '}
                          · {formatDateTime(row.latest.occurred_at)}
                        </>
                      ) : (
                        '—'
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      ) : null}

      {total === 0 ? (
        <EmptyState
          body="Finish a lesson or pass an assessment and it appears here with its evidence."
          icon={FileCheck2}
          image={EMPTY_IMAGES.transcript}
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
