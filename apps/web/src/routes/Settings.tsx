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
  NotificationListOut,
  ProfileOut,
  PushDeviceListOut,
} from '@nelavista/api-client';
import * as React from 'react';
import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';

import { formatDateTime } from '../lib/format';
import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { useSession } from '../lib/session';
import {
  Badge,
  Banner,
  Button,
  Checkbox,
  EmptyState,
  ErrorNote,
  ErrorState,
  Field,
  PageHeader,
  Panel,
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
  { value: 'private', label: 'Private - nobody sees my profile' },
  { value: 'link', label: 'Link only - someone with the link can see it' },
  { value: 'public', label: 'Public - discoverable by companies' },
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
          'The account, the sign-in and the recovery path. Password changes are a backend dependency.',
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
          onRemoveDevice={(deviceId) => void removePushDevice(deviceId)}
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
          displayName={displayName}
          setDisplayName={setDisplayName}
          bio={bio}
          setBio={setBio}
          location={locationValue}
          setLocation={setLocationValue}
          timezone={timezone}
          setTimezone={setTimezone}
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
          onRemoveLanguage={(language) =>
            void saveLanguages(rows.filter((item) => item.language !== language))
          }
          hours={hours}
          setHours={setHours}
          availableFrom={availableFrom}
          setAvailableFrom={setAvailableFrom}
          availabilityNote={availabilityNote}
          setAvailabilityNote={setAvailabilityNote}
          onSaveAvailability={() => void saveAvailability()}
        />
      )}
    </div>
  );
}

function ProfileSection(props: {
  meEmail: string;
  meVerified: boolean;
  displayName: string;
  setDisplayName: (value: string) => void;
  bio: string;
  setBio: (value: string) => void;
  location: string;
  setLocation: (value: string) => void;
  timezone: string;
  setTimezone: (value: string) => void;
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
    </div>
  );
}

function SecuritySection(): JSX.Element {
  const { me } = useSession();
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

      <Panel title="Password">
        <Banner tone="warning">
          <strong>Backend dependency.</strong> V2 does not expose a signed-in change-password endpoint yet. Do
          not show a form that cannot work. The route exists so the gap is visible, not so it can be faked.
        </Banner>
        <p className="nv-muted" style={{ marginTop: 'var(--nv-space-md)' }}>
          If you are signed out, use <Link to="/auth/reset">the reset flow</Link>. It revokes sessions after a
          successful reset.
        </p>
      </Panel>

      <Panel title="Sessions">
        <p className="nv-muted">
          Signing out on this device revokes the refresh cookie. A list of other sessions is not exposed by
          the current API, so this screen does not invent one.
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
          <Banner tone="info">
            <strong>Push is not available in this build.</strong> This browser cannot register a device, so
            email is the only active channel. A device registered by the mobile app appears below and can be
            removed here.
          </Banner>
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
