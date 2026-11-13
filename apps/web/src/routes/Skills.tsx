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
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import { ArrowRight, BookOpen, Globe2, Languages, SlidersHorizontal, Sparkles } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';

export function Skills(): JSX.Element {
  const { resource, reload } = useApiResource<SkillsOut>('/skills');
  const [search, setSearch] = React.useState('');
  const [programme, setProgramme] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [level, setLevel] = React.useState('');

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
  const programmes = Array.from(new Set(skills.map((skill) => skill.program ?? 'core'))).sort();
  const languages = Array.from(
    new Map(
      skills
        .filter((skill) => skill.language)
        .map((skill) => [skill.language as string, skill.language_label ?? (skill.language as string)]),
    ).entries(),
  ).sort((a, b) => a[1].localeCompare(b[1]));
  const filteredSkills = skills.filter((skill) => {
    const needle = search.trim().toLowerCase();
    if (needle) {
      const haystack = [
        skill.name,
        skill.description ?? '',
        skill.category ?? '',
        ...(skill.tags ?? []),
      ]
        .join(' ')
        .toLowerCase();
      if (!haystack.includes(needle)) return false;
    }
    if (programme && skill.program !== programme) return false;
    if (language && skill.language !== language) return false;
    if (level && !(skill.levels ?? []).includes(level)) return false;
    return true;
  });
  const filtering = Boolean(search || programme || language || level);

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Prove"
        title="Skills"
        description="Learn it, practise it, then prove it. A finished lesson is progress, never proof."
        actions={
          <div className="nv-row">
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/skills/languages">
              <Languages aria-hidden="true" size={15} />
              Language profile
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/skills/african-languages">
              <Globe2 aria-hidden="true" size={15} />
              African Languages Lab
            </Link>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/skills/my-learning">
              <BookOpen aria-hidden="true" size={15} />
              Continue learning
            </Link>
          </div>
        }
      />

      {skills.length > 0 ? (
        <Panel title="Filter" actions={<SlidersHorizontal aria-hidden="true" size={16} />}>
          <div className="nv-grid--4">
            <Field
              hint="Titles, descriptions and tags."
              id="skills-search"
              label="Search"
              maxLength={120}
              placeholder="e.g. transcription"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <Select
              label="Programme"
              options={[
                { value: '', label: 'Every programme' },
                ...programmes.map((value) => ({
                  value,
                  label: value === 'all' ? 'African Languages Lab' : value === 'core' ? 'Core' : value,
                })),
              ]}
              value={programme}
              onChange={(event) => setProgramme(event.target.value)}
            />
            <Select
              label="Language"
              options={[
                { value: '', label: 'Any language' },
                ...languages.map(([value, label]) => ({ value, label })),
              ]}
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
            />
            <Select
              label="Level"
              options={[
                { value: '', label: 'Any level' },
                { value: 'beginner', label: 'Beginner' },
                { value: 'intermediate', label: 'Intermediate' },
                { value: 'advanced', label: 'Advanced' },
              ]}
              value={level}
              onChange={(event) => setLevel(event.target.value)}
            />
          </div>
          {filtering ? (
            <div className="nv-row nv-row--between">
              <p className="nv-muted">
                {filteredSkills.length} of {skills.length} skills match.
              </p>
              <Button
                size="sm"
                type="button"
                variant="ghost"
                onClick={() => {
                  setSearch('');
                  setProgramme('');
                  setLanguage('');
                  setLevel('');
                }}
              >
                Clear filters
              </Button>
            </div>
          ) : null}
        </Panel>
      ) : null}

      <Panel title="Published skills" actions={<Badge tone="info">{filteredSkills.length}</Badge>}>
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
        ) : filteredSkills.length === 0 ? (
          <EmptyState
            body="No published skill matches those filters yet."
            icon={Sparkles}
            title="No match"
            action={
              <Button
                size="sm"
                type="button"
                variant="secondary"
                onClick={() => {
                  setSearch('');
                  setProgramme('');
                  setLanguage('');
                  setLevel('');
                }}
              >
                Clear filters
              </Button>
            }
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {filteredSkills.map((skill) => (
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
