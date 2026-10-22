/**
 * Skills catalog (B6): every skill the student can start, plus the way back into
 * what they have already begun.
 *
 * The page never invents a course: it lists what is published and says plainly
 * when nothing is published yet. `published_paths` is shown because a skill with
 * no published path is openable but empty, and the student should know that
 * before tapping it.
 */
import type { SkillsOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

export function Skills(): JSX.Element {
  const { resource, reload } = useApiResource<SkillsOut>('/skills');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading skills">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Skills</h1>
        <p className="nv-banner">
          The skills journey is not switched on for this environment yet. Your account and courses are
          unaffected.
        </p>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Skills</h1>
        <ErrorNote message={resource.message} />
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
      </div>
    );
  }

  const skills = resource.data.skills;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Skills</h1>
      <p className="nv-muted">
        Learn it, practise it, then prove it. A finished lesson is progress — never proof.
      </p>

      <p className="nv-muted">
        <Link to="/skills/my-learning">Continue where you left off</Link>
      </p>

      {skills.length === 0 ? (
        <p className="nv-banner">
          No skills are published yet. This is content, not an app update, so it appears here as soon as it is
          published.
        </p>
      ) : (
        <ul className="nv-list">
          {skills.map((skill) => (
            <li className="nv-card" key={skill.id}>
              <h2 className="nv-h2">
                <Link to={`/skills/${skill.slug}`}>{skill.name}</Link>
              </h2>
              {skill.category ? <p className="nv-muted">{skill.category}</p> : null}
              {skill.description ? <p>{skill.description}</p> : null}
              <p className="nv-muted">
                {skill.published_paths === 0
                  ? 'No published path yet.'
                  : `${skill.published_paths} path${skill.published_paths === 1 ? '' : 's'} available`}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
