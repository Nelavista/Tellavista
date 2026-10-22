/**
 * Talent profile and shares (B13), in lockstep with the web screen.
 *
 * The profile is evidence: verified skills, quality history, delivered work and
 * the transcript. Nothing is editable except the share links, because a claim a
 * student can type is not evidence a company can trust. A share token is shown
 * exactly once, at creation.
 */
import type {
  PlatformConfigOut,
  ShareCreatedOut,
  ShareListOut,
  TalentProfileOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Share } from 'react-native';

import type { Route } from '../lib/deepLink';
import { ApiError, api } from '../lib/api';
import { useApi } from '../lib/useApi';
import { Badge, Body, Button, Card, ErrorText, Field, H2, Loading, Muted, Note, Row, Screen } from '../ui';

const SCOPE_COPY: Record<string, string> = {
  academic: 'University, department and level',
  transcript: 'Transcript: what was learned, proved and delivered',
  quality: 'Review history and gold-task accuracy',
  work_history: 'Approved work and the projects it was for',
  availability: 'Hours, start date and languages',
};

function when(value: string | null | undefined): string {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : date.toLocaleDateString();
}

export function TalentScreen({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const profile = useApi<TalentProfileOut>('/talent/me');
  const shares = useApi<ShareListOut>('/talent/me/shares');
  const config = useApi<PlatformConfigOut>('/platform/config');

  const [label, setLabel] = React.useState('');
  const [ttlDays, setTtlDays] = React.useState('30');
  const [scopes, setScopes] = React.useState<string[]>(Object.keys(SCOPE_COPY));
  const [created, setCreated] = React.useState<ShareCreatedOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function createShare(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const share = await api.post<ShareCreatedOut>('/talent/me/shares', {
        label: label.trim() || null,
        scopes,
        ttl_days: Number(ttlDays) || 30,
      });
      setCreated(share);
      setLabel('');
      shares.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create that link.');
    } finally {
      setBusy(false);
    }
  }

  async function revoke(shareId: number): Promise<void> {
    setError(null);
    try {
      await api.post(`/talent/me/shares/${shareId}/revoke`, {});
      shares.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not revoke that link.');
    }
  }

  const shareUrl = created ? `https://nelavista.com/share/${created.token}` : null;

  return (
    <Screen title="Talent profile" onBack={() => navigate({ name: 'home' })}>
      {profile.remote.status === 'loading' ? <Loading /> : null}
      {profile.remote.status === 'error' ? <ErrorText message={profile.remote.message} /> : null}
      {profile.remote.status === 'ready' ? (
        <>
          <Card>
            <H2>{profile.remote.data.display_name ?? 'Your evidence profile'}</H2>
            <Badge
              label={profile.remote.data.visibility === 'private' ? 'private' : 'shared'}
              tone={profile.remote.data.visibility === 'private' ? 'muted' : 'ok'}
            />
            <Muted>
              Built from evidence only: verified skills, review history and delivered work. A company sees only the
              scopes you grant in a link, and a link can be revoked at any time.
            </Muted>
            {!profile.remote.data.display_name ? (
              <Muted>Add a display name in Settings on the web so a shared profile has a name on it.</Muted>
            ) : null}
          </Card>

          <Card>
            <H2>Verified skills</H2>
            {profile.remote.data.verified_skills.length === 0 ? (
              <Muted>No verified skill yet. Take a verification when you are ready.</Muted>
            ) : (
              profile.remote.data.verified_skills.map((skill) => (
                <Row key={skill.skill_id}>
                  <Body>{skill.skill ?? `Skill #${skill.skill_id}`}</Body>
                  <Badge label={skill.at_risk ? 'at risk' : 'verified'} tone={skill.at_risk ? 'warn' : 'ok'} />
                </Row>
              ))
            )}
          </Card>

          {profile.remote.data.academic ? (
            <Card>
              <H2>Academic</H2>
              <Body>
                {profile.remote.data.academic.university ?? 'University not set'} ·{' '}
                {profile.remote.data.academic.department ?? 'Department not set'}
                {profile.remote.data.academic.level ? ` · Level ${profile.remote.data.academic.level}` : ''}
              </Body>
            </Card>
          ) : null}

          {profile.remote.data.quality?.overall ? (
            <Card>
              <H2>Quality</H2>
              <Body>
                {profile.remote.data.quality.overall.reviews_count} review
                {profile.remote.data.quality.overall.reviews_count === 1 ? '' : 's'} ·{' '}
                {profile.remote.data.quality.overall.approvals} approved
                {profile.remote.data.quality.overall.average_score !== null
                  ? ` · ${profile.remote.data.quality.overall.average_score}% average`
                  : ''}
              </Body>
              <Muted>
                Gold checks: {profile.remote.data.quality.overall.gold_correct} of{' '}
                {profile.remote.data.quality.overall.gold_tasks} correct.
              </Muted>
            </Card>
          ) : null}

          {profile.remote.data.work_history && profile.remote.data.work_history.length > 0 ? (
            <Card>
              <H2>Delivered work</H2>
              {profile.remote.data.work_history.map((row) => (
                <Muted key={row.submission_id}>
                  {row.assignment} · {row.project.title} · approved {when(row.approved_at)}
                </Muted>
              ))}
            </Card>
          ) : null}

          {profile.remote.data.transcript ? (
            <Card>
              <H2>Transcript</H2>
              <Body>
                {profile.remote.data.transcript.counts.learned} learned ·{' '}
                {profile.remote.data.transcript.counts.proved} proved ·{' '}
                {profile.remote.data.transcript.counts.delivered} delivered
              </Body>
              <Button label="Open the full transcript" onPress={() => navigate({ name: 'transcript' })} tone="ghost" />
            </Card>
          ) : null}
        </>
      ) : null}

      <Card>
        <H2>Share a link</H2>
        <Muted>
          A link is the only way a company sees this profile. It expires automatically, and you can revoke it early;
          the token is shown once and never again.
        </Muted>
        <Field
          label="What is this link for?"
          maxLength={120}
          onChangeText={setLabel}
          placeholder="e.g. Client interview, October"
          value={label}
        />
        <Field
          keyboardType="number-pad"
          label="Days until it expires (1–90)"
          onChangeText={setTtlDays}
          value={ttlDays}
        />
        <Muted>What it includes</Muted>
        {Object.entries(SCOPE_COPY).map(([scope, copy]) => {
          const on = scopes.includes(scope);
          return (
            <Button
              key={scope}
              label={`${on ? '✓' : '○'} ${copy}`}
              onPress={() =>
                setScopes((current) =>
                  current.includes(scope) ? current.filter((value) => value !== scope) : [...current, scope],
                )
              }
              tone={on ? 'primary' : 'ghost'}
            />
          );
        })}
        <ErrorText message={error} />
        <Button
          label={busy ? 'Creating…' : 'Create link'}
          onPress={() => void createShare()}
          disabled={busy || scopes.length === 0}
        />
        {created && shareUrl ? (
          <Card>
            <H2>Copy this link now</H2>
            <Muted>It cannot be shown again.</Muted>
            <Body>{shareUrl}</Body>
            <Muted>Expires {when(created.expires_at)}.</Muted>
            <Button label="Share the link" onPress={() => void Share.share({ message: shareUrl })} />
          </Card>
        ) : null}
      </Card>

      <Card>
        <H2>Your links</H2>
        {shares.remote.status === 'error' ? <ErrorText message={shares.remote.message} /> : null}
        {shares.remote.status === 'ready' && shares.remote.data.shares.length === 0 ? (
          <Muted>No link yet.</Muted>
        ) : null}
        {shares.remote.status === 'ready'
          ? shares.remote.data.shares.map((share) => (
              <Card key={share.id}>
                <H2>{share.label ?? `Link #${share.id}`}</H2>
                <Muted>
                  {share.scopes.join(', ')} · expires {when(share.expires_at)}
                </Muted>
                {share.active ? (
                  <Button label="Revoke" onPress={() => void revoke(share.id)} tone="danger" />
                ) : (
                  <Badge label={share.revoked_at ? 'revoked' : 'expired'} />
                )}
              </Card>
            ))
          : null}
      </Card>

      <Card>
        <H2>Working with Nelavista</H2>
        <Muted>
          Curriculum owner: {config.remote.status === 'ready' ? config.remote.data.curriculum_owner : '—'} ·{' '}
          {config.remote.status === 'ready' ? config.remote.data.curriculum_license : '—'}
        </Muted>
        <Muted>
          Paid work starts at {config.remote.status === 'ready' ? config.remote.data.min_student_age : 16}; under{' '}
          {config.remote.status === 'ready' ? config.remote.data.guardian_consent_below_age : 18} needs guardian
          consent. Terms version{' '}
          {config.remote.status === 'ready' ? config.remote.data.contributor_terms_version : '—'}.
        </Muted>
      </Card>

      <Note message={null} />
    </Screen>
  );
}
