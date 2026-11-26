/**
 * Settings (B11) and its subroutes.
 *
 * One page per job: profile and matching signals, security, notification
 * choices, and the data controls. The API calls are the existing ones; the
 * split is a route decision, not a second source of truth.
 */
import type {
  AvailabilityOut,
  ConsentListOut,
  LanguagesOut,
  NewsletterStatusOut,
  NotificationListOut,
  ProfileOut,
  PlatformConfigOut,
  PushDeviceListOut,
  TokenOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';

import { formatDateTime } from '../lib/format';
import { ApiError, http, setAccessToken } from '../lib/http';
import { disablePush, enablePush, readPushStatus, type PushStatus } from '../lib/push';
import { useApiResource } from '../lib/resource';
import { useSession } from '../lib/session';
import { useTheme } from '../lib/theme-context';
import {
  Badge,
  Banner,
  Button,
  Checkbox,
  ConfirmDialog,
  EmptyState,
  ErrorNote,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  PasswordField,
  Select,
  Skeleton,
  Textarea,
} from '../ui';

const LEVELS = [
  { value: 'basic', label: 'Basic' },
  { value: 'conversational', label: 'Conversational' },
  { value: 'fluent', label: 'Fluent' },
  { value: 'native', label: 'Native' },
];

const VISIBILITY = [
  { value: 'private', label: 'Private: nobody sees my profile' },
  { value: 'link', label: 'Link only: someone with the link can see it' },
  { value: 'public', label: 'Public: discoverable by companies' },
];

const NAV = [
  { to: '/settings', label: 'Profile' },
  { to: '/settings/security', label: 'Security' },
  { to: '/settings/notifications', label: 'Notifications' },
  { to: '/settings/data', label: 'Your data' },
];

type Language = { language: string; level: string };

function sectionTitle(section: string): { title: string; description: string } {
  switch (section) {
    case 'security':
      return {
        title: 'Security',
        description:
          'The account, the password and the recovery path. Change the password here without leaving the app.',
      };
    case 'notifications':
      return {
        title: 'Notifications',
        description: 'Choose which channels can reach you, and review what has already arrived.',
      };
    case 'data':
      return {
        title: 'Your data',
        description: 'Export what V2 holds, or delete the account and understand exactly what survives.',
      };
    default:
      return {
        title: 'Profile',
        description: 'The context that makes matching and your Talent profile useful.',
      };
  }
}

export function Settings(): JSX.Element {
  const { me, profile: sessionProfile, reload, logout } = useSession();
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const section = location.pathname.split('/')[2] ?? 'profile';
  const heading = sectionTitle(section);

  const languages = useApiResource<LanguagesOut>('/me/languages');
  const availability = useApiResource<AvailabilityOut>('/me/availability');
  const notifications = useApiResource<NotificationListOut>('/me/notifications');
  const consents = useApiResource<ConsentListOut>('/me/consents');
  const pushDevices = useApiResource<PushDeviceListOut>('/me/push-devices');

  const [displayName, setDisplayName] = React.useState(sessionProfile?.display_name ?? '');
  const [bio, setBio] = React.useState(sessionProfile?.bio ?? '');
  const [locationValue, setLocationValue] = React.useState(sessionProfile?.location ?? '');
  const [timezone, setTimezone] = React.useState(sessionProfile?.timezone ?? '');
  const [dateOfBirth, setDateOfBirth] = React.useState(sessionProfile?.date_of_birth ?? '');
  const [visibility, setVisibility] = React.useState(sessionProfile?.profile_visibility ?? 'private');
  const [notifyEmail, setNotifyEmail] = React.useState(sessionProfile?.notify_email ?? true);
  const notifyPush = sessionProfile?.notify_push ?? true;

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
  const [pendingDeviceId, setPendingDeviceId] = React.useState<number | null>(null);
  const [pendingLanguage, setPendingLanguage] = React.useState<string | null>(null);

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
    setError(null);
    try {
      await http.patch<ProfileOut>('/me', {
        display_name: displayName.trim(),
        bio: bio.trim(),
        location: locationValue.trim(),
        timezone: timezone.trim(),
        // Empty means "not given": the API keeps null and no age rule is applied.
        date_of_birth: dateOfBirth || null,
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
    setError(null);
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
    setError(null);
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

  async function removePushDevice(deviceId: number): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.del(`/me/push-devices/${deviceId}`);
      pushDevices.reload();
      flash('Device removed.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not remove that device.');
    } finally {
      setBusy(false);
    }
  }

  async function markNotificationsRead(): Promise<void> {
    const unread =
      notifications.resource.status === 'ready'
        ? notifications.resource.data.notifications.filter((row) => row.read_at === null)
        : [];
    if (unread.length === 0) return;
    setBusy(true);
    setError(null);
    try {
      await http.post('/me/notifications/read', { ids: unread.map((row) => row.id) });
      notifications.reload();
      flash('Notifications marked read.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not update notifications.');
    } finally {
      setBusy(false);
    }
  }

  async function exportData(): Promise<void> {
    setBusy(true);
    setError(null);
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
    } finally {
      setBusy(false);
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

  const resourceError =
    languages.resource.status === 'error'
      ? languages.resource.message
      : availability.resource.status === 'error'
        ? availability.resource.message
        : notifications.resource.status === 'error'
          ? notifications.resource.message
          : null;

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader eyebrow="Account" title={heading.title} description={heading.description} />
      <nav className="nv-settings-nav" aria-label="Settings sections">
        {NAV.map((item) => (
          <NavLink key={item.to} to={item.to} end={item.to === '/settings'}>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <ErrorNote message={error} />
      {resourceError ? <Banner tone="danger">{resourceError}</Banner> : null}
      {saved ? <Banner tone="success">{saved}</Banner> : null}

      {section === 'security' ? (
        <SecuritySection />
      ) : section === 'notifications' ? (
        <NotificationsSection
          notifyEmail={notifyEmail}
          setNotifyEmail={setNotifyEmail}
          busy={busy}
          onSave={() => void saveProfile()}
          notifications={notifications.resource}
          devices={pushDevices.resource}
          onRemoveDevice={(deviceId) => setPendingDeviceId(deviceId)}
          onMarkRead={() => void markNotificationsRead()}
        />
      ) : section === 'data' ? (
        <DataSection
          busy={busy}
          confirmDelete={confirmDelete}
          setConfirmDelete={setConfirmDelete}
          onExport={() => void exportData()}
          onDelete={() => void deleteAccount()}
          consents={consents.resource}
        />
      ) : (
        <ProfileSection
          meEmail={me?.email ?? ''}
          meVerified={Boolean(me?.email_verified)}
          theme={theme}
          setTheme={setTheme}
          displayName={displayName}
          setDisplayName={setDisplayName}
          bio={bio}
          setBio={setBio}
          location={locationValue}
          setLocation={setLocationValue}
          timezone={timezone}
          setTimezone={setTimezone}
          dateOfBirth={dateOfBirth}
          setDateOfBirth={setDateOfBirth}
          visibility={visibility}
          setVisibility={setVisibility}
          busy={busy}
          onSaveProfile={() => void saveProfile()}
          rows={rows}
          newLanguage={newLanguage}
          setNewLanguage={setNewLanguage}
          newLevel={newLevel}
          setNewLevel={setNewLevel}
          onAddLanguage={addLanguage}
          onRemoveLanguage={(language) => setPendingLanguage(language)}
          hours={hours}
          setHours={setHours}
          availableFrom={availableFrom}
          setAvailableFrom={setAvailableFrom}
          availabilityNote={availabilityNote}
          setAvailabilityNote={setAvailabilityNote}
          onSaveAvailability={() => void saveAvailability()}
        />
      )}

      <ConfirmDialog
        body={
          <p>
            Push notifications stop for that install. Your email preference and account record are not
            changed.
          </p>
        }
        busy={busy}
        confirmLabel="Remove device"
        onCancel={() => setPendingDeviceId(null)}
        tone="danger"
        onConfirm={() => {
          if (pendingDeviceId !== null) {
            void removePushDevice(pendingDeviceId).finally(() => setPendingDeviceId(null));
          }
        }}
        open={pendingDeviceId !== null}
        title="Remove this device?"
      />

      <ConfirmDialog
        body={
          <p>Matching will no longer treat {pendingLanguage ?? 'this language'} as one you can work in.</p>
        }
        busy={busy}
        confirmLabel="Remove language"
        onCancel={() => setPendingLanguage(null)}
        tone="danger"
        onConfirm={() => {
          if (pendingLanguage) {
            void saveLanguages(rows.filter((item) => item.language !== pendingLanguage)).finally(() =>
              setPendingLanguage(null),
            );
          }
        }}
        open={pendingLanguage !== null}
        title="Remove this language?"
      />
    </div>
  );
}

function ProfileSection(props: {
  meEmail: string;
  meVerified: boolean;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  displayName: string;
  setDisplayName: (value: string) => void;
  bio: string;
  setBio: (value: string) => void;
  location: string;
  setLocation: (value: string) => void;
  timezone: string;
  setTimezone: (value: string) => void;
  dateOfBirth: string;
  setDateOfBirth: (value: string) => void;
  visibility: string;
  setVisibility: (value: string) => void;
  busy: boolean;
  onSaveProfile: () => void;
  rows: Language[];
  newLanguage: string;
  setNewLanguage: (value: string) => void;
  newLevel: string;
  setNewLevel: (value: string) => void;
  onAddLanguage: () => void;
  onRemoveLanguage: (language: string) => void;
  hours: string;
  setHours: (value: string) => void;
  availableFrom: string;
  setAvailableFrom: (value: string) => void;
  availabilityNote: string;
  setAvailabilityNote: (value: string) => void;
  onSaveAvailability: () => void;
}): JSX.Element {
  return (
    <div className="nv-stack nv-stack--loose">
      <Panel
        title="Profile"
        actions={
          <span className="nv-meta">
            {props.meEmail} {props.meVerified ? '· confirmed' : '· not confirmed'}
          </span>
        }
      >
        <div className="nv-stack">
          <Field
            label="Display name"
            maxLength={150}
            value={props.displayName}
            onChange={(event) => props.setDisplayName(event.target.value)}
          />
          <Textarea
            label="Short bio"
            maxLength={500}
            rows={3}
            value={props.bio}
            onChange={(event) => props.setBio(event.target.value)}
          />
          <Field
            label="Location"
            maxLength={120}
            value={props.location}
            onChange={(event) => props.setLocation(event.target.value)}
          />
          <Field
            hint="e.g. Africa/Lagos. Used to show deadlines in your time."
            label="Time zone"
            maxLength={64}
            value={props.timezone}
            onChange={(event) => props.setTimezone(event.target.value)}
          />
          <Field
            hint="Only used for the paid-work age rules. Never shown on your public profile."
            label="Date of birth"
            type="date"
            value={props.dateOfBirth}
            onChange={(event) => props.setDateOfBirth(event.target.value)}
          />
          <Select
            label="Who can see your Talent profile"
            value={props.visibility}
            onChange={(event) => props.setVisibility(event.target.value)}
            options={VISIBILITY}
          />
          <div className="nv-row nv-row--end">
            <Button
              type="button"
              disabled={props.busy || !props.displayName.trim()}
              onClick={props.onSaveProfile}
            >
              {props.busy ? 'Saving' : 'Save profile'}
            </Button>
          </div>
        </div>
      </Panel>

      <Panel title="Languages you can work in">
        <div className="nv-stack">
          <p className="nv-muted">Matching uses these when an opportunity names a language.</p>
          {props.rows.length === 0 ? (
            <EmptyState title="No language added yet" body="Add the languages you can actually work in." />
          ) : (
            <ul className="nv-list">
              {props.rows.map((row) => (
                <li className="nv-row nv-row--between" key={row.language}>
                  <span>
                    {row.language} <span className="nv-muted">· {row.level}</span>
                  </span>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => props.onRemoveLanguage(row.language)}
                  >
                    Remove
                  </Button>
                </li>
              ))}
            </ul>
          )}
          <div className="nv-row" style={{ alignItems: 'flex-end' }}>
            <div style={{ flex: '1 1 14rem' }}>
              <Field
                label="Add a language"
                maxLength={60}
                value={props.newLanguage}
                onChange={(event) => props.setNewLanguage(event.target.value)}
              />
            </div>
            <div style={{ flex: '0 1 12rem' }}>
              <Select
                label="Level"
                value={props.newLevel}
                onChange={(event) => props.setNewLevel(event.target.value)}
                options={LEVELS}
              />
            </div>
            <Button
              type="button"
              variant="secondary"
              disabled={props.busy || !props.newLanguage.trim()}
              onClick={props.onAddLanguage}
            >
              Add
            </Button>
          </div>
        </div>
      </Panel>

      <Panel title="Availability">
        <div className="nv-stack">
          <p className="nv-muted">Stated availability is a matching signal, not a contract.</p>
          <div className="nv-grid--2">
            <Field
              label="Hours per week"
              max={168}
              min={0}
              type="number"
              value={props.hours}
              onChange={(event) => props.setHours(event.target.value)}
            />
            <Field
              label="Available from"
              type="date"
              value={props.availableFrom}
              onChange={(event) => props.setAvailableFrom(event.target.value)}
            />
          </div>
          <Field
            label="Note (optional)"
            maxLength={255}
            value={props.availabilityNote}
            onChange={(event) => props.setAvailabilityNote(event.target.value)}
          />
          <div className="nv-row nv-row--end">
            <Button type="button" disabled={props.busy} onClick={props.onSaveAvailability}>
              {props.busy ? 'Saving' : 'Save availability'}
            </Button>
          </div>
        </div>
      </Panel>

      <Panel title="Appearance">
        <p className="nv-muted">
          The signed-in app opens in dark by default. A saved choice applies on this device across every page.
        </p>
        <div className="nv-row" role="group" aria-label="Theme">
          <Button
            aria-pressed={props.theme === 'light'}
            type="button"
            variant={props.theme === 'light' ? 'primary' : 'secondary'}
            onClick={() => props.setTheme('light')}
          >
            Light
          </Button>
          <Button
            aria-pressed={props.theme === 'dark'}
            type="button"
            variant={props.theme === 'dark' ? 'primary' : 'secondary'}
            onClick={() => props.setTheme('dark')}
          >
            Dark
          </Button>
        </div>
      </Panel>
    </div>
  );
}

function SecuritySection(): JSX.Element {
  const { me } = useSession();
  const [currentPassword, setCurrentPassword] = React.useState('');
  const [newPassword, setNewPassword] = React.useState('');
  const [confirmPassword, setConfirmPassword] = React.useState('');
  const [changeBusy, setChangeBusy] = React.useState(false);
  const [changeMessage, setChangeMessage] = React.useState<string | null>(null);
  const [changeError, setChangeError] = React.useState<string | null>(null);
  const [resetBusy, setResetBusy] = React.useState(false);
  const [resetMessage, setResetMessage] = React.useState<string | null>(null);
  const [resetError, setResetError] = React.useState<string | null>(null);

  async function changePassword(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setChangeError(null);
    setChangeMessage(null);
    if (newPassword.length < 10) {
      setChangeError('Use at least 10 characters for the new password.');
      return;
    }
    if (newPassword !== confirmPassword) {
      setChangeError('The new password and confirmation do not match.');
      return;
    }
    setChangeBusy(true);
    try {
      const session = await http.post<TokenOut>('/auth/password/change', {
        current_password: currentPassword,
        new_password: newPassword,
        platform: 'web',
      });
      setAccessToken(session.access_token);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setChangeMessage('Password changed. Other devices were signed out; this session stays signed in.');
    } catch (err) {
      setChangeError(err instanceof ApiError ? err.message : 'Could not change your password.');
    } finally {
      setChangeBusy(false);
    }
  }

  async function sendResetLink(): Promise<void> {
    if (!me?.email) return;
    setResetBusy(true);
    setResetError(null);
    setResetMessage(null);
    try {
      const result = await http.post<{ message: string }>('/auth/password/reset-request', {
        email: me.email,
      });
      setResetMessage(result.message);
    } catch (err) {
      setResetError(err instanceof ApiError ? err.message : 'Could not send the reset link.');
    } finally {
      setResetBusy(false);
    }
  }

  return (
    <div className="nv-stack nv-stack--loose">
      <Panel title="Account">
        <dl className="nv-stack nv-stack--tight">
          <div className="nv-row nv-row--between">
            <dt className="nv-muted">Email</dt>
            <dd>{me?.email}</dd>
          </div>
          <div className="nv-row nv-row--between">
            <dt className="nv-muted">Email status</dt>
            <dd>
              <Badge tone={me?.email_verified ? 'success' : 'warning'}>
                {me?.email_verified ? 'Confirmed' : 'Not confirmed'}
              </Badge>
            </dd>
          </div>
          <div className="nv-row nv-row--between">
            <dt className="nv-muted">Two-factor authentication</dt>
            <dd>
              <Badge tone={me?.mfa_enabled ? 'success' : 'neutral'}>
                {me?.mfa_enabled ? 'Enabled' : 'Not enabled'}
              </Badge>
            </dd>
          </div>
        </dl>
      </Panel>

      <Panel title="Change password">
        <form className="nv-stack" onSubmit={(event) => void changePassword(event)}>
          <p className="nv-muted">
            Changing the password signs out every other device and keeps this one signed in. Use at least 10
            characters.
          </p>
          <PasswordField
            autoComplete="current-password"
            label="Current password"
            maxLength={200}
            required
            value={currentPassword}
            onChange={(event) => setCurrentPassword(event.target.value)}
          />
          <div className="nv-grid--2">
            <PasswordField
              autoComplete="new-password"
              hint="At least 10 characters."
              label="New password"
              maxLength={200}
              required
              value={newPassword}
              onChange={(event) => setNewPassword(event.target.value)}
            />
            <PasswordField
              autoComplete="new-password"
              label="Confirm new password"
              maxLength={200}
              required
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
            />
          </div>
          {changeError ? (
            <Banner tone="danger">
              <p>{changeError}</p>
            </Banner>
          ) : null}
          {changeMessage ? (
            <Banner tone="success">
              <p>{changeMessage}</p>
            </Banner>
          ) : null}
          <div className="nv-row nv-row--end">
            <Button
              disabled={changeBusy || !currentPassword || newPassword.length < 10 || !confirmPassword}
              type="submit"
            >
              {changeBusy ? 'Changing' : 'Change password'}
            </Button>
          </div>
        </form>
      </Panel>

      <Panel title="Forgot the current password?">
        <p className="nv-muted">
          Send a single-use reset link to <strong>{me?.email}</strong>. A successful reset revokes sessions.
          If you are signed out, use <Link to="/auth/reset">the reset flow</Link>.
        </p>
        <div className="nv-row" style={{ marginTop: 'var(--nv-space-md)' }}>
          <Button
            disabled={resetBusy || !me?.email}
            onClick={() => void sendResetLink()}
            type="button"
            variant="secondary"
          >
            {resetBusy ? 'Sending' : 'Send password reset link'}
          </Button>
        </div>
        {resetMessage ? (
          <Banner tone="success">
            <p>{resetMessage}</p>
          </Banner>
        ) : null}
        {resetError ? (
          <Banner tone="danger">
            <p>{resetError}</p>
          </Banner>
        ) : null}
      </Panel>

      <Panel title="Sessions">
        <p className="nv-muted">
          Signing out revokes the refresh cookie for this device. Changing the password revokes every other
          refresh token at the same time.
        </p>
      </Panel>
    </div>
  );
}

function NotificationsSection({
  notifyEmail,
  setNotifyEmail,
  busy,
  onSave,
  notifications,
  devices,
  onRemoveDevice,
  onMarkRead,
}: {
  notifyEmail: boolean;
  setNotifyEmail: (value: boolean) => void;
  busy: boolean;
  onSave: () => void;
  notifications: ReturnType<typeof useApiResource<NotificationListOut>>['resource'];
  devices: ReturnType<typeof useApiResource<PushDeviceListOut>>['resource'];
  onRemoveDevice: (deviceId: number) => void;
  onMarkRead: () => void;
}): JSX.Element {
  const unread =
    notifications.status === 'ready'
      ? notifications.data.notifications.filter((row) => row.read_at === null)
      : [];

  return (
    <div className="nv-stack nv-stack--loose">
      <Panel title="Channels">
        <div className="nv-stack">
          <Checkbox
            checked={notifyEmail}
            onChange={(event) => setNotifyEmail(event.target.checked)}
            label="Email me about review, payouts and deadlines"
          />
          <BrowserPushPanel />
          <div className="nv-row nv-row--between">
            <Link className="nv-link-arrow" to="/notifications">
              Open the full inbox
            </Link>
            <Button type="button" disabled={busy} onClick={onSave}>
              {busy ? 'Saving' : 'Save choices'}
            </Button>
          </div>
        </div>
      </Panel>

      <NewsletterPanel />

      <PushDevicesPanel devices={devices} busy={busy} onRemove={onRemoveDevice} />

      <Panel
        title="Recent notifications"
        actions={
          unread.length > 0 ? (
            <Button type="button" variant="secondary" size="sm" disabled={busy} onClick={onMarkRead}>
              Mark all read
            </Button>
          ) : null
        }
      >
        {notifications.status === 'loading' ? (
          <Skeleton lines={3} />
        ) : notifications.status === 'off' ? (
          <EmptyState
            title="Notifications are not switched on here"
            body="This environment has the feature off."
          />
        ) : notifications.status === 'missing' || notifications.status === 'error' ? (
          <ErrorState title="Notifications did not load" body={notifications.message} />
        ) : notifications.data.notifications.length === 0 ? (
          <EmptyState title="Nothing yet" body="Review results, rework requests and payouts appear here." />
        ) : (
          <ul className="nv-list">
            {notifications.data.notifications.slice(0, 8).map((row) => (
              <li key={row.id} className="nv-stack nv-stack--tight">
                <div className="nv-row nv-row--between">
                  <strong>{row.title}</strong>
                  <span className="nv-meta">{formatDateTime(row.created_at)}</span>
                </div>
                <p className="nv-muted">{row.body}</p>
                {row.read_at === null ? <Badge tone="info">Unread</Badge> : null}
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}

/**
 * The newsletter choice, on the page where the email choice lives.
 *
 * Subscribing is double opt-in, so the pending state is shown as its own state
 * rather than as "on": the address is not on the list until the reader opens the
 * link we mailed. Leaving is immediate and reversible by subscribing again.
 */
function NewsletterPanel(): JSX.Element {
  const [status, setStatus] = React.useState<NewsletterStatusOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let live = true;
    http
      .get<NewsletterStatusOut>('/me/newsletter')
      .then((data) => {
        if (live) setStatus(data);
      })
      .catch(() => {
        if (live) setStatus(null);
      });
    return () => {
      live = false;
    };
  }, []);

  async function subscribe(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      setStatus(await http.post<NewsletterStatusOut>('/me/newsletter', {}));
      setNote('Confirmation sent. Open the link in that email to finish.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not subscribe this address.');
    } finally {
      setBusy(false);
    }
  }

  async function leave(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      setStatus(await http.del<NewsletterStatusOut>('/me/newsletter'));
      setNote('You are off the newsletter list.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not leave the list.');
    } finally {
      setBusy(false);
    }
  }

  const badge = !status ? null : status.subscribed ? (
    <Badge tone="success">On</Badge>
  ) : status.pending ? (
    <Badge tone="warning">Pending</Badge>
  ) : (
    <Badge tone="neutral">Off</Badge>
  );

  return (
    <Panel title="Monthly newsletter" actions={badge}>
      <div className="nv-stack">
        {status === null ? (
          <Skeleton lines={2} />
        ) : (
          <>
            <p className="nv-muted">
              {status.subscribed
                ? `One note a month to ${status.email}: new material, open opportunities and what changed on the platform. Every issue carries its own unsubscribe link.`
                : status.pending
                  ? `We emailed a confirmation link to ${status.email}. The address is not on the list until you open it.`
                  : `Add ${status.email} to the list for one note a month. We send a confirmation link first; nothing is sent until you click it.`}
            </p>
            <div className="nv-row">
              {status.subscribed || status.pending ? (
                <Button disabled={busy} onClick={() => void leave()} type="button" variant="secondary">
                  {busy ? 'Leaving' : 'Leave the newsletter'}
                </Button>
              ) : (
                <Button disabled={busy} onClick={() => void subscribe()} type="button">
                  {busy ? 'Sending' : 'Subscribe'}
                </Button>
              )}
            </div>
          </>
        )}
        {note ? <p role="status">{note}</p> : null}
        {error ? (
          <p className="nv-error" role="alert">
            {error}
          </p>
        ) : null}
      </div>
    </Panel>
  );
}

/**
 * Browser push, on the page where the email choice lives.
 *
 * Every state is explained rather than hidden: a student who sees no button is
 * owed the reason (no service worker, no VAPID key here, blocklisted permission),
 * and a blocklisted permission can only be undone in browser settings.
 */
function BrowserPushPanel(): JSX.Element {
  const config = useApiResource<PlatformConfigOut>('/platform/config');
  const [status, setStatus] = React.useState<PushStatus | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    void readPushStatus()
      .then(setStatus)
      .catch(() => setStatus({ supported: false, ready: false, permission: 'unsupported', endpoint: null }));
  }, []);

  const publicKey = config.resource.status === 'ready' ? config.resource.data.push_public_key : null;

  async function refresh(): Promise<void> {
    setStatus(await readPushStatus());
  }

  async function turnOn(): Promise<void> {
    if (!publicKey) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      await enablePush(publicKey);
      await refresh();
      setNote('This browser will now receive push notifications.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not register this browser.');
      await refresh().catch(() => undefined);
    } finally {
      setBusy(false);
    }
  }

  async function turnOff(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      await disablePush();
      await refresh();
      setNote('This browser will no longer receive push notifications.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not remove this browser.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Panel
      title="Push on this browser"
      actions={status?.endpoint ? <Badge tone="success">On</Badge> : <Badge tone="neutral">Off</Badge>}
    >
      <div className="nv-stack">
        {status === null ? (
          <Skeleton lines={2} />
        ) : !status.supported ? (
          <Banner tone="info">
            This browser cannot receive push notifications. Email is the working channel here; the mobile app
            registers a device on its own.
          </Banner>
        ) : !status.ready ? (
          <Banner tone="info">
            Push becomes available once this build has its service worker registered. Reload the app, or
            install it, and this panel will offer the switch.
          </Banner>
        ) : !publicKey ? (
          <Banner tone="info">
            Web push is not configured for this environment, so this browser cannot be registered. Email still
            works.
          </Banner>
        ) : status.permission === 'denied' ? (
          <Banner tone="warning">
            Notifications are blocked for this site. Allow them in your browser settings, then reload this
            page.
          </Banner>
        ) : status.endpoint ? (
          <div className="nv-row nv-row--between">
            <p className="nv-muted">
              This browser is registered. Notifications appear here even when the app is closed.
            </p>
            <Button
              disabled={busy}
              onClick={() => void turnOff()}
              size="sm"
              type="button"
              variant="secondary"
            >
              {busy ? 'Removing' : 'Turn off'}
            </Button>
          </div>
        ) : (
          <div className="nv-row nv-row--between">
            <p className="nv-muted">
              Register this browser as a device. The browser will ask for permission; nothing is registered
              unless you allow it.
            </p>
            <Button disabled={busy} onClick={() => void turnOn()} size="sm" type="button">
              {busy ? 'Registering' : 'Turn on push'}
            </Button>
          </div>
        )}
        {note ? <p role="status">{note}</p> : null}
        {error ? (
          <p className="nv-error" role="alert">
            {error}
          </p>
        ) : null}
      </div>
    </Panel>
  );
}

function PushDevicesPanel({
  devices,
  busy,
  onRemove,
}: {
  devices: ReturnType<typeof useApiResource<PushDeviceListOut>>['resource'];
  busy: boolean;
  onRemove: (deviceId: number) => void;
}): JSX.Element {
  const count = devices.status === 'ready' ? devices.data.devices.length : null;

  return (
    <Panel
      title="Push devices"
      actions={
        count === null ? null : <Badge tone={count === 0 ? 'neutral' : 'info'}>{count} registered</Badge>
      }
    >
      <p className="nv-muted">
        A registered device is a specific install, not a preference. Removing one stops push to that install;
        it does not change your email choice.
      </p>
      {devices.status === 'loading' ? (
        <Skeleton lines={2} />
      ) : devices.status === 'off' ? (
        <EmptyState
          title="Push devices are not switched on here"
          body="This environment has the feature off."
        />
      ) : devices.status === 'missing' || devices.status === 'error' ? (
        <ErrorState title="Devices did not load" body={devices.message} />
      ) : devices.data.devices.length === 0 ? (
        <EmptyState
          title="No devices registered"
          body="The mobile app registers a device when push is enabled there. This browser does not."
        />
      ) : (
        <ul className="nv-list nv-list--ruled">
          {devices.data.devices.map((device) => (
            <li key={device.id} className="nv-row nv-row--between">
              <div className="nv-stack nv-stack--tight">
                <strong>{device.platform}</strong>
                <span className="nv-meta">
                  Ending {device.token.slice(-6)} ·{' '}
                  {device.last_seen_at ? `last seen ${formatDateTime(device.last_seen_at)}` : 'never seen'}
                </span>
              </div>
              <Button
                type="button"
                variant="secondary"
                size="sm"
                disabled={busy}
                onClick={() => onRemove(device.id)}
              >
                Remove
              </Button>
            </li>
          ))}
        </ul>
      )}
    </Panel>
  );
}

function DataSection({
  busy,
  confirmDelete,
  setConfirmDelete,
  onExport,
  onDelete,
  consents,
}: {
  busy: boolean;
  confirmDelete: string;
  setConfirmDelete: (value: string) => void;
  onExport: () => void;
  onDelete: () => void;
  consents: ReturnType<typeof useApiResource<ConsentListOut>>['resource'];
}): JSX.Element {
  return (
    <div className="nv-stack nv-stack--loose">
      <Panel title="Export">
        <div className="nv-stack">
          <p className="nv-muted">
            Download everything V2 holds about you as JSON. Money and audit evidence is included because it
            explains your earnings; other students&apos; details never are.
          </p>
          <div className="nv-row">
            <Button type="button" variant="secondary" disabled={busy} onClick={onExport}>
              {busy ? 'Building export' : 'Download my data'}
            </Button>
          </div>
        </div>
      </Panel>

      <Panel title="Consent history">
        <p className="nv-muted">
          Each agreement is recorded with the document version and the time you accepted it. The history is
          append-only; a later change adds a row instead of rewriting the past.
        </p>
        {consents.status === 'loading' ? (
          <Skeleton lines={3} />
        ) : consents.status === 'off' ? (
          <EmptyState
            title="Consent history is not switched on here"
            body="This environment has the feature off."
          />
        ) : consents.status === 'missing' || consents.status === 'error' ? (
          <ErrorState title="Consent history did not load" body={consents.message} />
        ) : consents.data.consents.length === 0 ? (
          <EmptyState
            title="No consent recorded yet"
            body="Accepting the terms or a contributor agreement will add the first entry."
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <caption className="nv-sr-only">Consent history</caption>
              <thead>
                <tr>
                  <th scope="col">Agreement</th>
                  <th scope="col">Version</th>
                  <th scope="col">State</th>
                  <th scope="col">Recorded</th>
                </tr>
              </thead>
              <tbody>
                {consents.data.consents.map((row) => (
                  <tr key={row.id}>
                    <td>{row.kind}</td>
                    <td className="nv-mono">{row.document_version}</td>
                    <td>
                      <Badge tone={row.granted ? 'success' : 'warning'}>
                        {row.granted ? 'Granted' : 'Withdrawn'}
                      </Badge>
                    </td>
                    <td>{formatDateTime(row.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <Panel title="Delete your account">
        <div className="nv-stack">
          <p className="nv-muted">
            This anonymises your account and signs out every device. Learning, proof and earnings stop being
            visible to you; the money and audit records needed to explain a payout remain, without your name
            or email.
          </p>
          <Field
            label="Type DELETE to confirm"
            value={confirmDelete}
            onChange={(event) => setConfirmDelete(event.target.value)}
          />
          <div className="nv-row">
            <Button
              type="button"
              variant="danger"
              disabled={busy || confirmDelete !== 'DELETE'}
              onClick={onDelete}
            >
              Delete my account
            </Button>
            <Link className="nv-button nv-button--ghost" to="/home">
              Back to your home
            </Link>
          </div>
        </div>
      </Panel>
    </div>
  );
}
