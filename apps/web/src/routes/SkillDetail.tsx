/**
 * One skill and the paths inside it (B6). Only published paths are listed, so
 * every link here opens.
 */
import type { SkillDetailOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

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
        <h1 className="nv-h1">Skill</h1>
        {resource.status === 'off' ? (
          <p className="nv-banner">The skills journey is not switched on for this environment yet.</p>
        ) : (
          <>
            <ErrorNote message={resource.message} />
            <button className="nv-button" type="button" onClick={reload}>
              Try again
            </button>
          </>
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
      <p className="nv-muted">
        <Link to="/skills">All skills</Link>
      </p>
      <h1 className="nv-h1">{skill.name}</h1>
      {skill.description ? <p>{skill.description}</p> : null}

      {skill.paths.length === 0 ? (
        <p className="nv-banner">
          This skill has no published learning path yet. Nothing to do here until one is published.
        </p>
      ) : (
        <ul className="nv-list">
          {skill.paths.map((path) => (
            <li className="nv-card" key={path.id}>
              <h2 className="nv-h2">
                <Link to={`/skills/paths/${path.slug}`}>{path.title}</Link>
              </h2>
              <p className="nv-muted">
                {path.level}
                {path.estimated_hours ? ` · about ${path.estimated_hours} hour(s)` : ''}
              </p>
              {path.summary ? <p>{path.summary}</p> : null}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
