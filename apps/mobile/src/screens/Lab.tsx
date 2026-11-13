import type {
  CareerTrackListOut,
  LanguageProfileListOut,
  LanguageProfileOut,
  SkillsOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Pressable } from 'react-native';

import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { useApi } from '../lib/useApi';
import { Badge, Body, Button, Card, ErrorText, Field, H2, Loading, Muted, Note, Row, Screen } from '../ui';

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

const CAPABILITY_KEYS = ['can_speak', 'can_read', 'can_write', 'can_transcribe', 'can_translate'] as const;

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

export function Lab({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const catalog = useApi<SkillsOut>('/skills?program=all');
  const tracks = useApi<CareerTrackListOut>('/skills/career-tracks?program=all');
  const [language, setLanguage] = React.useState('');

  const languages = React.useMemo(() => {
    const seen = new Map<string, string>();
    if (catalog.remote.status === 'ready') {
      for (const skill of catalog.remote.data.skills) {
        if (skill.language) seen.set(skill.language, skill.language_label ?? skill.language);
      }
    }
    return [...seen.entries()].sort((a, b) => a[1].localeCompare(b[1]));
  }, [catalog.remote]);

  const skills =
    catalog.remote.status === 'ready'
      ? catalog.remote.data.skills.filter(
          (skill) => !language || skill.language === language,
        )
      : [];
  const trackRows =
    tracks.remote.status === 'ready'
      ? tracks.remote.data.tracks.filter(
          (track) =>
            !language || (track.skills ?? []).some((skill) => skill.language === language),
        )
      : [];

  return (
    <Screen title="African Languages Lab" onBack={() => navigate({ name: 'home' })}>
      <Muted>
        Transcription, translation, speech and annotation in African languages. Every skill ends in a
        scored assessment, so the language you work in can be proven — not just claimed.
      </Muted>

      <Button
        label="Language profile"
        onPress={() => navigate({ name: 'languages' })}
        tone="ghost"
      />

      <Row>
        <Pressable onPress={() => setLanguage('')}>
          <Badge label="All languages" tone={language === '' ? 'ok' : 'muted'} />
        </Pressable>
        {languages.map(([value, label]) => (
          <Pressable key={value} onPress={() => setLanguage(value)}>
            <Badge label={label} tone={language === value ? 'ok' : 'muted'} />
          </Pressable>
        ))}
      </Row>

      <H2>Career tracks</H2>
      {tracks.remote.status === 'loading' ? <Loading /> : null}
      {tracks.remote.status === 'error' ? <ErrorText message={tracks.remote.message} /> : null}
      {tracks.remote.status === 'ready' && trackRows.length === 0 ? (
        <Muted>
          {language
            ? 'No track matches that language yet.'
            : 'No tracks are published yet. This is content, not an app update.'}
        </Muted>
      ) : null}
      {trackRows.map((track) => (
        <Card key={track.id}>
          <H2>{track.title}</H2>
          {track.tagline ? <Muted>{track.tagline}</Muted> : null}
          {(track.skills ?? []).map((skill, index) => (
            <Pressable key={skill.id} onPress={() => navigate({ name: 'skill', slug: skill.slug })}>
              <Body>
                {index + 1}. {skill.name}
                {skill.language_label ? ` · ${skill.language_label}` : ''}
              </Body>
            </Pressable>
          ))}
          <Muted>A track is a suggested order. You can open any skill in it directly.</Muted>
        </Card>
      ))}

      <H2>Skills in the lab</H2>
      {catalog.remote.status === 'loading' ? <Loading /> : null}
      {catalog.remote.status === 'error' ? <ErrorText message={catalog.remote.message} /> : null}
      {catalog.remote.status === 'ready' && skills.length === 0 ? (
        <Muted>No lab skill matches that language yet.</Muted>
      ) : null}
      {skills.map((skill) => (
        <Pressable key={skill.id} onPress={() => navigate({ name: 'skill', slug: skill.slug })}>
          <Card>
            <H2>{skill.name}</H2>
            <Muted>
              {[skill.category, skill.language_label, (skill.levels ?? []).join(', ')]
                .filter(Boolean)
                .join(' · ')}
            </Muted>
            {skill.description ? <Muted>{skill.description}</Muted> : null}
            <Muted>
              {skill.published_paths} published path{skill.published_paths === 1 ? '' : 's'}
            </Muted>
          </Card>
        </Pressable>
      ))}
    </Screen>
  );
}

export function LanguageProfile({
  navigate,
}: {
  navigate: (route: Route) => void;
}): JSX.Element {
  const profile = useApi<LanguageProfileListOut>('/skills/languages');
  const [rows, setRows] = React.useState<DraftLanguage[]>([]);
  const [newLanguage, setNewLanguage] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [saved, setSaved] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (profile.remote.status === 'ready') setRows(profile.remote.data.languages.map(toDraft));
  }, [profile.remote]);

  const capabilities =
    profile.remote.status === 'ready' ? profile.remote.data.capabilities : [];
  const verifiedByLanguage = new Map(
    profile.remote.status === 'ready'
      ? profile.remote.data.languages.map((row) => [row.language, row] as const)
      : [],
  );

  async function save(next: DraftLanguage[]): Promise<void> {
    setBusy(true);
    setError(null);
    setSaved(null);
    try {
      await api.put<LanguageProfileListOut>('/skills/languages', {
        languages: next.map((row) => ({
          language: row.language,
          level: row.level,
          dialect: row.dialect.trim() || null,
          ...Object.fromEntries(CAPABILITY_KEYS.map((key) => [key, row[key]])),
        })),
      });
      setRows(next);
      setSaved('Saved. Nothing here is verified until an assessment is passed.');
      profile.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your language profile.');
    } finally {
      setBusy(false);
    }
  }

  function toggle(index: number, key: (typeof CAPABILITY_KEYS)[number]): void {
    setRows((current) =>
      current.map((row, position) =>
        position === index ? { ...row, [key]: !row[key] } : row,
      ),
    );
  }

  return (
    <Screen title="Language profile" onBack={() => navigate({ name: 'home' })}>
      <Muted>
        What you say you can do is self-reported. What is verified comes from passed assessments and
        cannot be edited here.
      </Muted>

      {profile.remote.status === 'loading' ? <Loading /> : null}
      {profile.remote.status === 'error' ? <ErrorText message={profile.remote.message} /> : null}
      <ErrorText message={error} />
      <Note message={saved} />

      {rows.length === 0 && profile.remote.status === 'ready' ? (
        <Muted>No language added yet. Add the languages you can work in.</Muted>
      ) : null}

      {rows.map((row, index) => {
        const verified = verifiedByLanguage.get(row.language)?.verified ?? [];
        const verifiedSkills = verifiedByLanguage.get(row.language)?.verified_skills ?? [];
        return (
          <Card key={row.language}>
            <H2>{row.label ?? row.language}</H2>
            {row.dialect ? <Muted>Dialect: {row.dialect}</Muted> : null}
            <Muted>Self-reported capabilities</Muted>
            <Row>
              {capabilities.map((capability) => {
                const key = capability.key as (typeof CAPABILITY_KEYS)[number];
                const on = row[key];
                return (
                  <Pressable
                    accessibilityRole="checkbox"
                    accessibilityState={{ checked: on }}
                    key={capability.key}
                    onPress={() => toggle(index, key)}
                  >
                    <Badge label={`${on ? '☑' : '☐'} ${capability.label}`} tone={on ? 'ok' : 'muted'} />
                  </Pressable>
                );
              })}
            </Row>
            <Muted>Verified from passed assessments</Muted>
            {verified.length === 0 ? (
              <Muted>Nothing verified in this language yet.</Muted>
            ) : (
              <>
                <Row>
                  {verified.map((key) => (
                    <Badge key={key} label={key.replace('can_', '')} tone="ok" />
                  ))}
                </Row>
                {verifiedSkills.map((skill) => (
                  <Pressable key={skill.id} onPress={() => navigate({ name: 'skill', slug: skill.slug })}>
                    <Muted>{skill.name}</Muted>
                  </Pressable>
                ))}
              </>
            )}
            <Button
              label="Remove this language"
              onPress={() => void save(rows.filter((_, position) => position !== index))}
              tone="ghost"
              disabled={busy}
            />
          </Card>
        );
      })}

      <Card>
        <H2>Add a language</H2>
        <Field
          autoCapitalize="words"
          label="Language"
          onChangeText={setNewLanguage}
          placeholder="e.g. Yoruba"
          value={newLanguage}
        />
        <Button
          disabled={busy || !newLanguage.trim()}
          label="Add"
          onPress={() => {
            const name = newLanguage.trim();
            if (!name) return;
            if (rows.some((row) => row.language.toLowerCase() === name.toLowerCase())) {
              setError(`${name} is already on your profile.`);
              return;
            }
            setNewLanguage('');
            void save([
              ...rows,
              {
                language: name,
                label: null,
                level: 'fluent',
                dialect: '',
                can_speak: false,
                can_read: false,
                can_write: false,
                can_transcribe: false,
                can_translate: false,
              },
            ]);
          }}
          tone="ghost"
        />
        <Muted>Proficiency and dialect are editable on the web app.</Muted>
      </Card>

      <Button
        disabled={busy || rows.length === 0}
        label={busy ? 'Saving…' : 'Save language profile'}
        onPress={() => void save(rows)}
      />
    </Screen>
  );
}
