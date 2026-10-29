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
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { ArrowRight, BookOpen, Sparkles } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';

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
        <PageHeader eyebrow="Prove" title="Skills" />
        <Banner tone="info">
          <p>
            The skills journey is not switched on for this environment yet. Your account and courses are
            unaffected.
          </p>
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
        <PageHeader eyebrow="Prove" title="Skills" />
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

  const skills = resource.data.skills;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Prove"
        title="Skills"
        description="Learn it, practise it, then prove it. A finished lesson is progress, never proof."
        actions={
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/skills/my-learning">
            <BookOpen aria-hidden="true" size={15} />
            Continue learning
          </Link>
        }
      />

      <Panel title="Published skills" actions={<Badge tone="info">{skills.length}</Badge>}>
        {skills.length === 0 ? (
          <EmptyState
            body="No skills are published yet. This is content, not an app update, so it appears here as soon as it is published."
            icon={Sparkles}
            image={EMPTY_IMAGES.skills}
            title="No skills yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/home">
                Back to your home
              </Link>
            }
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {skills.map((skill) => (
              <li key={skill.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <Link className="nv-h3" to={`/skills/${skill.slug}`}>
                      {skill.name}
                    </Link>
                    {skill.category ? <p className="nv-meta">{skill.category}</p> : null}
                  </div>
                  <Badge tone={skill.published_paths > 0 ? 'success' : 'neutral'}>
                    {skill.published_paths === 0
                      ? 'No published path'
                      : `${skill.published_paths} path${skill.published_paths === 1 ? '' : 's'} available`}
                  </Badge>
                </div>
                {skill.description ? <p className="nv-muted">{skill.description}</p> : null}
                <div style={{ marginTop: 'var(--nv-space-sm)' }}>
                  <Link className="nv-button nv-button--ghost nv-button--sm" to={`/skills/${skill.slug}`}>
                    Open skill
                    <ArrowRight aria-hidden="true" size={14} />
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
