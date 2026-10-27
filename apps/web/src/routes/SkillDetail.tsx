/**
 * One skill and the paths inside it (B6). Only published paths are listed, so
 * every link here opens.
 */
import type { SkillDetailOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { BookOpen, Clock } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';

export function SkillDetail(): JSX.Element {
  const { skillSlug = '' } = useParams<{ skillSlug: string }>();
  const { resource, reload } = useApiResource<SkillDetailOut>(`/skills/${skillSlug}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading this skill">
        <Skeleton height="2rem" width="50%" />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Skills" title="Skill" />
        {resource.status === 'off' ? (
          <Banner tone="info">
            <p>The skills journey is not switched on for this environment yet.</p>
          </Banner>
        ) : (
          <ErrorState
            body={resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={reload}>
                Try again
              </Button>
            }
          />
        )}
        <p className="nv-muted">
          <Link to="/skills">All skills</Link>
        </p>
      </div>
    );
  }

  const skill = resource.data;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Skill"
        title={skill.name}
        description={skill.description ?? undefined}
        actions={
          <Badge tone="neutral">
            {skill.paths.length} path{skill.paths.length === 1 ? '' : 's'}
          </Badge>
        }
      />

      <p className="nv-muted">
        <Link to="/skills">All skills</Link>
      </p>

      <Panel title="Learning paths">
        {skill.paths.length === 0 ? (
          <EmptyState
            body="This skill has no published learning path yet. Nothing to do here until one is published."
            icon={BookOpen}
            title="No published path"
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {skill.paths.map((path) => (
              <li key={path.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <h2 className="nv-h3">
                      <Link to={`/skills/paths/${path.slug}`}>{path.title}</Link>
                    </h2>
                    <p className="nv-muted">
                      {path.level}
                      {path.estimated_hours ? (
                        <span>
                          {' '}
                          · <Clock aria-hidden="true" size={12} /> about {path.estimated_hours} hour
                          {path.estimated_hours === 1 ? '' : 's'}
                        </span>
                      ) : null}
                    </p>
                    {path.summary ? <p>{path.summary}</p> : null}
                  </div>
                  <Link
                    className="nv-button nv-button--secondary nv-button--sm"
                    to={`/skills/paths/${path.slug}`}
                  >
                    Open path
                  </Link>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}
