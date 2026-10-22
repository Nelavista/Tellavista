/**
 * Settings (B11).
 *
 * Everything the app stores about a student is visible and editable here:
 * profile, languages, availability, notification choices — plus the two store
 * requirements, a machine-readable export and in-app deletion.
 *
 * Deletion is not a button that silently does nothing: it anonymises the account
 * and revokes every session, and the screen says what survives (money and audit
 * evidence, because a payout must stay explainable).
 */
import type {
  AvailabilityOut,
  LanguagesOut,
  NotificationListOut,
  ProfileOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';
import { useApiResource } from '../lib/resource';
import { Button, ErrorNote, Field, Select, Skeleton } from '../ui';

const LEVELS = [
  { value: 'basic', label: 'Basic' },
  { value: 'conversational', label: 'Conversational' },
  { value: 'fluent', label: 'Fluent' },
  { value: 'native', label: 'Native' },
];

const VISIBILITY = [
  { value: 'private', label: 'Private — nobody sees my profile' },
  { value: 'link', label: 'Link only — someone with the link can see it' },
  { value: 'public', label: 'Public — discoverable by companies' },
];

type Language = { language: string; level: string };

export function Settings(): JSX.Element {
  const { me, profile: sessionProfile, reload, logout } = useSession();
  const navigate = useNavigate();
  const languages = useApiResource<LanguagesOut>('/me/languages');
  const availability = useApiResource<AvailabilityOut>('/me/availability');
  const notifications = useApiResource<NotificationListOut>('/me/notifications');

  const [displayName, setDisplayName] = React.useState(sessionProfile?.display_name ?? '');
  const [bio, setBio] = React.useState(sessionProfile?.bio ?? '');
  const [location, setLocation] = React.useState(sessionProfile?.location ?? '');
  const [timezone, setTimezone] = React.useState(sessionProfile?.timezone ?? '');
  const [visibility, setVisibility] = React.useState(sessionProfile?.profile_visibility ?? 'private');
  const [notifyEmail, setNotifyEmail] = React.useState(sessionProfile?.notify_email ?? true);
  const [notifyPush, setNotifyPush] = React.useState(sessionProfile?.notify_push ?? true);

  const [rows, setRows] = React.useState<Language[]>([]);
  const [newLanguage, setNewLanguage] = React.useState('');
  const [newLevel, setNewLevel] = React.useState('fluent');

  const [hours, setHours] = React.useState('');
  const [availableFrom, setAvailableFrom] = React.useState('');
  const [availabilityNote, setAvailabilityNote] = React.useState('');

  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [saved, setSaved] = React.useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = React.useState('');

  React.useEffect(() => {
    if (languages.resource.status === 'ready') setRows(languages.resource.data.languages);
  }, [languages.resource]);

  React.useEffect(() => {
    if (availability.resource.status === 'ready') {
      const data = availability.resource.data;
      setHours(data.hours_per_week === null ? '' : String(data.hours_per_week));
      setAvailableFrom(data.available_from ?? '');
      setAvailabilityNote(data.note ?? '');
    }
  }, [availability.resource]);

  function flash(message: string): void {
    setSaved(message);
    setError(null);
  }

  async function saveProfile(): Promise<void> {
    setBusy(true);
    try {
      await http.patch<ProfileOut>('/me', {
        display_name: displayName.trim(),
        bio: bio.trim(),
        location: location.trim(),
        timezone: timezone.trim(),
        profile_visibility: visibility,
        notify_email: notifyEmail,
        notify_push: notifyPush,
      });
      await reload();
      flash('Profile saved.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your profile.');
    } finally {
      setBusy(false);
    }
  }

  async function saveLanguages(next: Language[]): Promise<void> {
    setBusy(true);
    try {
      const result = await http.put<LanguagesOut>('/me/languages', { languages: next });
      setRows(result.languages);
      flash('Languages saved.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your languages.');
    } finally {
      setBusy(false);
    }
  }

  function addLanguage(): void {
    const name = newLanguage.trim();
    if (!name) return;
    if (rows.some((row) => row.language.toLowerCase() === name.toLowerCase())) {
      setError(`${name} is already listed.`);
      return;
    }
    const next = [...rows, { language: name, level: newLevel }];
    setRows(next);
    setNewLanguage('');
    void saveLanguages(next);
  }

  async function saveAvailability(): Promise<void> {
    setBusy(true);
    try {
      await http.put<AvailabilityOut>('/me/availability', {
        hours_per_week: hours === '' ? null : Number(hours),
        available_from: availableFrom || null,
        note: availabilityNote.trim() || null,
      });
      flash('Availability saved.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your availability.');
    } finally {
      setBusy(false);
    }
  }

  async function markNotificationsRead(): Promise<void> {
    const unread = notifications.resource.status === 'ready'
      ? notifications.resource.data.notifications.filter((row) => row.read_at === null)
      : [];
    if (unread.length === 0) return;
    try {
      await http.post('/me/notifications/read', { ids: unread.map((row) => row.id) });
      notifications.reload();
      flash('Notifications marked read.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not update notifications.');
    }
  }

  async function exportData(): Promise<void> {
    try {
      const data = await http.get<Record<string, unknown>>('/me/export');
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'nelavista-export.json';
      link.click();
      URL.revokeObjectURL(url);
      flash('Your export was downloaded.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not build your export.');
    }
  }

  async function deleteAccount(): Promise<void> {
    if (confirmDelete !== 'DELETE') {
      setError('Type DELETE to confirm.');
      return;
    }
    setBusy(true);
    try {
      await http.del('/auth/account');
      await logout();
      navigate('/', { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not delete your account.');
      setBusy(false);
    }
  }

  if (
    languages.resource.status === 'loading' ||
    availability.resource.status === 'loading' ||
    notifications.resource.status === 'loading'
  ) {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your settings">
        <Skeleton height="2rem" width="35%" />
        <Skeleton lines={4} />
        <Skeleton lines={3} />
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Settings</h1>
      <ErrorNote message={error} />
      {saved ? (
        <p className="nv-banner" role="status">
          {saved}
        </p>
      ) : null}

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">Profile</h2>
        <p className="nv-muted">Signed in as {me?.email}{me?.email_verified ? ' (confirmed)' : ' (not confirmed)'}</p>
        <Field label="Display name" maxLength={150} value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
        <div className="nv-field">
          <label className="nv-label" htmlFor="nv-bio">
            Short bio
          </label>
          <textarea
            className="nv-input"
            id="nv-bio"
            maxLength={500}
            rows={3}
            value={bio}
            onChange={(event) => setBio(event.target.value)}
          />
        </div>
        <Field label="Location" maxLength={120} value={location} onChange={(e) => setLocation(e.target.value)} />
        <Field
          hint="e.g. Africa/Lagos. Used to show deadlines in your time."
          label="Time zone"
          maxLength={64}
          value={timezone}
          onChange={(e) => setTimezone(e.target.value)}
        />
        <Select
          label="Who can see your Talent profile"
          value={visibility}
          onChange={(e) => setVisibility(e.target.value)}
          options={VISIBILITY}
        />
        <label className="nv-check">
          <input type="checkbox" checked={notifyEmail} onChange={(e) => setNotifyEmail(e.target.checked)} />
          Email me about review, payouts and deadlines
        </label>
        <label className="nv-check">
          <input type="checkbox" checked={notifyPush} onChange={(e) => setNotifyPush(e.target.checked)} />
          Send push notifications to my devices
        </label>
        <Button type="button" disabled={busy || !displayName.trim()} onClick={() => void saveProfile()}>
          {busy ? 'Saving…' : 'Save profile'}
        </Button>
      </section>

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">Languages you can work in</h2>
        <p className="nv-muted">Matching uses these when an opportunity names a language.</p>
        {rows.length === 0 ? <p className="nv-muted">No language added yet.</p> : null}
        <ul className="nv-list">
          {rows.map((row) => (
            <li className="nv-row nv-row--between" key={row.language}>
              <span>
                {row.language} <span className="nv-muted">· {row.level}</span>
              </span>
              <button
                className="nv-button nv-button--ghost"
                type="button"
                onClick={() => void saveLanguages(rows.filter((item) => item.language !== row.language))}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
        <div className="nv-row">
          <Field
            label="Add a language"
            maxLength={60}
            value={newLanguage}
            onChange={(event) => setNewLanguage(event.target.value)}
          />
          <Select label="Level" value={newLevel} onChange={(e) => setNewLevel(e.target.value)} options={LEVELS} />
          <Button type="button" variant="ghost" disabled={busy || !newLanguage.trim()} onClick={addLanguage}>
            Add
          </Button>
        </div>
      </section>

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">Availability</h2>
        <p className="nv-muted">Stated availability is a matching signal, not a contract.</p>
        <Field
          label="Hours per week"
          max={168}
          min={0}
          type="number"
          value={hours}
          onChange={(event) => setHours(event.target.value)}
        />
        <Field
          label="Available from"
          type="date"
          value={availableFrom}
          onChange={(event) => setAvailableFrom(event.target.value)}
        />
        <Field
          label="Note (optional)"
          maxLength={255}
          value={availabilityNote}
          onChange={(event) => setAvailabilityNote(event.target.value)}
        />
        <Button type="button" disabled={busy} onClick={() => void saveAvailability()}>
          {busy ? 'Saving…' : 'Save availability'}
        </Button>
      </section>

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">Notifications</h2>
        {notifications.resource.status === 'ready' && notifications.resource.data.notifications.length > 0 ? (
          <>
            <ul className="nv-list">
              {notifications.resource.data.notifications.slice(0, 10).map((row) => {
                const assessmentSlug = row.data?.['assessment_slug'];
                return (
                  <li key={row.id}>
                    <strong>{row.title}</strong>
                    <p className="nv-muted">{row.body}</p>
                    {typeof assessmentSlug === 'string' ? (
                      <p>
                        <Link className="nv-button nv-button--ghost" to={`/verification/assessments/${assessmentSlug}`}>
                          Re-verify now
                        </Link>
                      </p>
                    ) : null}
                    {row.read_at === null ? (
                      <span className="nv-badge" data-status="unverified">
                        Unread
                      </span>
                    ) : null}
                  </li>
                );
              })}
            </ul>
            <Button type="button" variant="ghost" onClick={() => void markNotificationsRead()}>
              Mark all read
            </Button>
          </>
        ) : (
          <p className="nv-muted">Nothing yet. Review results, rework requests and payouts appear here.</p>
        )}
      </section>

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">Your data</h2>
        <p className="nv-muted">
          Download everything V2 holds about you as JSON. Money and audit evidence is included because it
          explains your earnings; other students&apos; details never are.
        </p>
        <Button type="button" variant="ghost" onClick={() => void exportData()}>
          Download my data
        </Button>
      </section>

      <section className="nv-card nv-stack">
        <h2 className="nv-h2">Delete your account</h2>
        <p>
          This anonymises your account and signs out every device. Learning, proof and earnings stop
          being visible to you; the money and audit records needed to explain a payout remain, without
          your name or email.
        </p>
        <Field
          label="Type DELETE to confirm"
          value={confirmDelete}
          onChange={(event) => setConfirmDelete(event.target.value)}
        />
        <Button
          type="button"
          disabled={busy || confirmDelete !== 'DELETE'}
          onClick={() => void deleteAccount()}
        >
          Delete my account
        </Button>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </section>
    </div>
  );
}
