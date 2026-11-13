/**
 * African Languages Lab hub (I1/I4).
 *
 * The lab is a programme, not a new catalogue: every track and skill here is a
 * normal seeded skill, so opening one goes to the same path, practice and
 * assessment screens. The hub only adds the language/level filters V1 has, and
 * the filters run on the API so web and mobile cannot disagree about them.
 *
 * A track is a suggested route through several skills. It never verifies
 * anything and never replaces a learning path.
 */
import type { CareerTrackListOut, CareerTrackOut, SkillsOut } from '@nelavista/api-client';
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
import { ArrowRight, Compass, Languages, Sparkles } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';

const LEVELS = [
  { value: '', label: 'Any level' },
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
];

function toQuery(params: Record<string, string>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value) search.set(key, value);
  }
  const text = search.toString();
  return text ? `?${text}` : '';
}

function TrackCard({ track }: { track: CareerTrackOut }): JSX.Element {
  return (
    <li className="nv-stack nv-stack--tight">
      <div>
        <p className="nv-h4">{track.title}</p>
        {track.tagline ? <p className="nv-muted">{track.tagline}</p> : null}
      </div>
      <ol className="nv-list nv-list--ruled">
        {(track.skills ?? []).map((skill, index) => (
          <li key={skill.id} className="nv-row nv-row--between">
            <span>
              <span className="nv-meta">{index + 1}. </span>
              <Link to={`/skills/${skill.slug}`}>{skill.name}</Link>
            </span>
            <span className="nv-row nv-row--tight">
              {skill.language_label ? <Badge tone="neutral">{skill.language_label}</Badge> : null}
              <Badge tone="info">{skill.category_slug ?? 'skill'}</Badge>
            </span>
          </li>
        ))}
      </ol>
    </li>
  );
}

export function AfricanLanguages(): JSX.Element {
  const [q, setQ] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [level, setLevel] = React.useState('');

  // Options come from the unfiltered programme so they never disappear while a
  // filter is applied.
  const catalog = useApiResource<SkillsOut>('/skills?program=all');
  const tracks = useApiResource<CareerTrackListOut>(
    `/skills/career-tracks${toQuery({ program: 'all', q, language })}`,
  );
  const skills = useApiResource<SkillsOut>(`/skills${toQuery({ program: 'all', q, language, level })}`);

  const languageOptions = React.useMemo(() => {
    const seen = new Map<string, string>();
    if (catalog.resource.status === 'ready') {
      for (const skill of catalog.resource.data.skills) {
        if (skill.language) {
          seen.set(skill.language, skill.language_label ?? skill.language);
        }
      }
    }
    return [
      { value: '', label: 'Any language' },
      ...[...seen.entries()]
        .sort((a, b) => a[1].localeCompare(b[1]))
        .map(([value, label]) => ({ value, label })),
    ];
  }, [catalog.resource]);

  if (skills.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="African Languages Lab" />
        <Banner tone="info">
          <p>The skills journey is not switched on for this environment yet.</p>
        </Banner>
      </div>
    );
  }

  if (skills.resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading the African Languages Lab">
        <Skeleton height="2rem" width="45%" />
        <Skeleton lines={4} />
        <Skeleton lines={6} />
      </div>
    );
  }

  if (skills.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="African Languages Lab" />
        <ErrorState
          body={skills.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={skills.reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const skillRows = skills.resource.data.skills;
  const trackRows = tracks.resource.status === 'ready' ? tracks.resource.data.tracks : [];
  const filtered = Boolean(q || language || level);

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Prove"
        title="African Languages Lab"
        description="Transcription, translation, speech and annotation work in African languages. Every skill ends in a scored assessment, so a language you work in can be proven, not just claimed."
        actions={
          <div className="nv-row">
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/skills/languages">
              <Languages aria-hidden="true" size={15} />
              Language profile
            </Link>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/skills">
              All skills
            </Link>
          </div>
        }
      />

      <Panel title="Find a skill" actions={<Compass aria-hidden="true" size={16} />}>
        <div className="nv-grid--3">
          <Field
            hint="Search titles, descriptions, tags and languages."
            label="Search"
            maxLength={120}
            placeholder="e.g. Yoruba transcription"
            value={q}
            onChange={(event) => setQ(event.target.value)}
          />
          <Select
            label="Language"
            options={languageOptions}
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
          />
          <Select
            label="Level"
            options={LEVELS}
            value={level}
            onChange={(event) => setLevel(event.target.value)}
          />
        </div>
        {filtered ? (
          <div className="nv-row nv-row--between">
            <p className="nv-muted">
              {skillRows.length} matching skill{skillRows.length === 1 ? '' : 's'}
            </p>
            <Button
              size="sm"
              type="button"
              variant="ghost"
              onClick={() => {
                setQ('');
                setLanguage('');
                setLevel('');
              }}
            >
              Clear filters
            </Button>
          </div>
        ) : null}
      </Panel>

      <Panel
        title="Career tracks"
        actions={<Badge tone="info">{trackRows.length}</Badge>}
      >
        <p className="nv-muted">
          A track is a suggested order through skills, not a replacement for a learning path. You
          can start any skill in it directly.
        </p>
        {trackRows.length === 0 ? (
          <EmptyState
            body={
              filtered
                ? 'No track matches those filters. Clear them to see every track.'
                : 'No tracks are published yet. This is content, not an app update.'
            }
            icon={Compass}
            title="No tracks here"
          />
        ) : (
          <ul className="nv-list">
            {trackRows.map((track) => (
              <TrackCard key={track.id} track={track} />
            ))}
          </ul>
        )}
      </Panel>

      <Panel
        title={filtered ? 'Matching skills' : 'Skills in the lab'}
        actions={<Badge tone="info">{skillRows.length}</Badge>}
      >
        {skillRows.length === 0 ? (
          <EmptyState
            body={
              filtered
                ? 'No skill matches those filters yet. Try a language on its own, or clear the level.'
                : 'No lab skills are published yet. This is content, not an app update.'
            }
            icon={Sparkles}
            image={EMPTY_IMAGES.skills}
            title={filtered ? 'No match' : 'No skills yet'}
            action={
              filtered ? (
                <Button
                  size="sm"
                  type="button"
                  variant="secondary"
                  onClick={() => {
                    setQ('');
                    setLanguage('');
                    setLevel('');
                  }}
                >
                  Clear filters
                </Button>
              ) : (
                <Link className="nv-button nv-button--secondary nv-button--sm" to="/skills">
                  Back to all skills
                </Link>
              )
            }
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {skillRows.map((skill) => (
              <li key={skill.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <Link className="nv-h3" to={`/skills/${skill.slug}`}>
                      {skill.name}
                    </Link>
                    <p className="nv-meta">
                      {[skill.category, skill.language_label, (skill.levels ?? []).join(', ')]
                        .filter(Boolean)
                        .join(' · ')}
                    </p>
                  </div>
                  <Badge tone={skill.published_paths > 0 ? 'success' : 'neutral'}>
                    {skill.published_paths === 0
                      ? 'No published path'
                      : `${skill.published_paths} path${skill.published_paths === 1 ? '' : 's'}`}
                  </Badge>
                </div>
                {skill.description ? <p className="nv-muted">{skill.description}</p> : null}
                {(skill.tags ?? []).length > 0 ? (
                  <div className="nv-row" style={{ flexWrap: 'wrap' }}>
                    {(skill.tags ?? []).slice(0, 5).map((tag) => (
                      <Badge key={tag} tone="neutral">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                ) : null}
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
