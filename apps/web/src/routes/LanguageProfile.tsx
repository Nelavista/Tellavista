/**
 * Language profile (African Languages Lab).
 *
 * Two columns that must never be confused: what the student says they can do is
 * editable here and labelled self-reported; what is verified comes from passed
 * language-specific assessments and is read-only. Saving a language never makes
 * anything verified.
 */
import type { LanguageProfileListOut, LanguageProfileOut } from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  Checkbox,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import { BadgeCheck, Languages, Loader2, Plus, Trash2 } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

const LEVELS = [
  { value: 'basic', label: 'Basic' },
  { value: 'conversational', label: 'Conversational' },
  { value: 'fluent', label: 'Fluent' },
  { value: 'native', label: 'Native / first language' },
];

type DraftLanguage = {
  language: string;
  label: string | null;
  level: string;
  dialect: string;
  can_speak: boolean;
  can_read: boolean;
  can_write: boolean;
  can_transcribe: boolean;
  can_translate: boolean;
};

function toDraft(row: LanguageProfileOut): DraftLanguage {
  return {
    language: row.language,
    label: row.label ?? null,
    level: row.proficiency,
    dialect: row.dialect ?? '',
    can_speak: row.self_reported.includes('can_speak'),
    can_read: row.self_reported.includes('can_read'),
    can_write: row.self_reported.includes('can_write'),
    can_transcribe: row.self_reported.includes('can_transcribe'),
    can_translate: row.self_reported.includes('can_translate'),
  };
}

export function LanguageProfile(): JSX.Element {
  const { resource, reload } = useApiResource<LanguageProfileListOut>('/skills/languages');
  const [rows, setRows] = React.useState<DraftLanguage[]>([]);
  const [newLanguage, setNewLanguage] = React.useState('');
  const [newLevel, setNewLevel] = React.useState('fluent');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [saved, setSaved] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (resource.status === 'ready') setRows(resource.data.languages.map(toDraft));
  }, [resource]);

  async function save(next: DraftLanguage[]): Promise<void> {
    setBusy(true);
    setError(null);
    setSaved(null);
    try {
      await http.put<LanguageProfileListOut>('/skills/languages', {
        languages: next.map((row) => ({
          language: row.language,
          level: row.level,
          dialect: row.dialect.trim() || null,
          can_speak: row.can_speak,
          can_read: row.can_read,
          can_write: row.can_write,
          can_transcribe: row.can_transcribe,
          can_translate: row.can_translate,
        })),
      });
      setRows(next);
      setSaved('Language profile saved. Nothing here is verified until an assessment is passed.');
      reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your language profile.');
    } finally {
      setBusy(false);
    }
  }

  function update(index: number, patch: Partial<DraftLanguage>): void {
    setRows((current) =>
      current.map((row, position) => (position === index ? { ...row, ...patch } : row)),
    );
  }

  function addLanguage(): void {
    const name = newLanguage.trim();
    if (!name) return;
    if (rows.some((row) => row.language.toLowerCase() === name.toLowerCase())) {
      setError(`${name} is already on your profile.`);
      return;
    }
    const next = [
      ...rows,
      {
        language: name,
        label: null,
        level: newLevel,
        dialect: '',
        can_speak: false,
        can_read: false,
        can_write: false,
        can_transcribe: false,
        can_translate: false,
      },
    ];
    setNewLanguage('');
    void save(next);
  }

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your language profile">
        <Skeleton height="2rem" width="40%" />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="Language profile" />
        <Banner tone="info">
          <p>The skills journey is not switched on for this environment yet.</p>
        </Banner>
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Prove" title="Language profile" />
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

  const data = resource.data;
  const verifiedByLanguage = new Map(
    data.languages.map((row) => [row.language, row] as const),
  );

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Prove"
        title="Language profile"
        description="Tell us what you can do in each language. Claims stay claims; only a passed assessment makes a capability verified."
        actions={
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/skills">
            All skills
          </Link>
        }
      />

      {error ? <ErrorState title="Your language profile did not save" body={error} /> : null}
      {saved ? <Banner tone="success">{saved}</Banner> : null}

      <Panel
        title="Your languages"
        actions={
          <Badge tone="info">
            {rows.length} language{rows.length === 1 ? '' : 's'}
          </Badge>
        }
      >
        {rows.length === 0 ? (
          <EmptyState
            icon={Languages}
            title="No language added yet"
            body="Add the languages you can work in and tick what you can actually do in each one."
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {rows.map((row, index) => {
              const verified = verifiedByLanguage.get(row.language)?.verified ?? [];
              const verifiedSkills = verifiedByLanguage.get(row.language)?.verified_skills ?? [];
              return (
                <li className="nv-stack" key={row.language}>
                  <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                    <div>
                      <p className="nv-h4">{row.label ?? row.language}</p>
                      <p className="nv-meta">Self-reported profile</p>
                    </div>
                    <Button
                      aria-label={`Remove ${row.language}`}
                      size="sm"
                      type="button"
                      variant="ghost"
                      onClick={() => void save(rows.filter((_, position) => position !== index))}
                    >
                      <Trash2 aria-hidden="true" size={15} />
                      Remove
                    </Button>
                  </div>

                  <div className="nv-grid--2">
                    <Field
                      label="Dialect (optional)"
                      maxLength={60}
                      value={row.dialect}
                      onChange={(event) => update(index, { dialect: event.target.value })}
                    />
                    <Select
                      label="Proficiency"
                      options={LEVELS}
                      value={row.level}
                      onChange={(event) => update(index, { level: event.target.value })}
                    />
                  </div>

                  <fieldset className="nv-field">
                    <legend className="nv-label">What you can do (self-reported)</legend>
                    <div className="nv-row" style={{ flexWrap: 'wrap', gap: 'var(--nv-space-md)' }}>
                      {data.capabilities.map((capability) => (
                        <Checkbox
                          key={capability.key}
                          checked={row[capability.key as keyof DraftLanguage] as boolean}
                          label={capability.label}
                          onChange={(event) =>
                            update(index, {
                              [capability.key]: event.target.checked,
                            } as Partial<DraftLanguage>)
                          }
                        />
                      ))}
                    </div>
                    <p className="nv-muted">
                      These are your claims. They help matching; they are not proof.
                    </p>
                  </fieldset>

                  <div className="nv-stack nv-stack--tight">
                    <p className="nv-label">Verified from passed assessments</p>
                    {verified.length === 0 ? (
                      <p className="nv-muted">
                        Nothing verified in this language yet. Pass a language-specific assessment to
                        prove a capability.
                      </p>
                    ) : (
                      <>
                        <div className="nv-row" style={{ flexWrap: 'wrap' }}>
                          {verified.map((key) => {
                            const capability = data.capabilities.find((item) => item.key === key);
                            return (
                              <Badge key={key} tone="success">
                                <BadgeCheck aria-hidden="true" size={12} />
                                {capability?.label ?? key}
                              </Badge>
                            );
                          })}
                        </div>
                        <ul className="nv-list">
                          {verifiedSkills.map((skill) => (
                            <li key={skill.id}>
                              <Link to={`/skills/${skill.slug}`}>{skill.name}</Link>
                            </li>
                          ))}
                        </ul>
                      </>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        )}

        <div className="nv-row" style={{ alignItems: 'flex-end', marginTop: 'var(--nv-space-lg)' }}>
          <div style={{ flex: '1 1 16rem' }}>
            <Field
              hint="For example Yoruba, Igbo, Hausa or Nigerian Pidgin."
              label="Add a language"
              list="nv-language-options"
              maxLength={60}
              value={newLanguage}
              onChange={(event) => setNewLanguage(event.target.value)}
            />
            <datalist id="nv-language-options">
              {data.catalog.map((option) => (
                <option key={option.key} value={option.label} />
              ))}
            </datalist>
          </div>
          <div style={{ flex: '0 1 13rem' }}>
            <Select
              label="Proficiency"
              options={LEVELS}
              value={newLevel}
              onChange={(event) => setNewLevel(event.target.value)}
            />
          </div>
          <Button
            disabled={busy || !newLanguage.trim()}
            type="button"
            variant="secondary"
            onClick={addLanguage}
          >
            {busy ? <Loader2 aria-hidden="true" size={15} /> : <Plus aria-hidden="true" size={15} />}
            Add
          </Button>
        </div>
        <div className="nv-row nv-row--end" style={{ marginTop: 'var(--nv-space-md)' }}>
          <Button disabled={busy} type="button" onClick={() => void save(rows)}>
            {busy ? 'Saving' : 'Save language profile'}
          </Button>
        </div>
      </Panel>
    </div>
  );
}
