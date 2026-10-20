import type { MeOut, NotificationListOut, ProfileOut } from '@nelavista/api-client';
import * as React from 'react';
import { Alert, Share } from 'react-native';

import type { Route } from '../lib/deepLink';
import { ApiError, api, logout } from '../lib/api';
import { registerForPush } from '../lib/notifications';
import { useApi } from '../lib/useApi';
import { Body, Button, Card, ErrorText, H2, Loading, Muted, Note, Screen } from '../ui';

export function Notifications({ navigate }: { navigate: (route: Route) => void }): JSX.Element {
  const list = useApi<NotificationListOut>('/me/notifications');
  const [note, setNote] = React.useState<string | null>(null);

  async function readAll(): Promise<void> {
    if (list.remote.status !== 'ready') return;
    const unread = list.remote.data.notifications.filter((row) => row.read_at === null).map((row) => row.id);
    if (unread.length === 0) return;
    await api.post('/me/notifications/read', { ids: unread });
    setNote('Marked read.');
    list.reload();
  }

  return (
    <Screen title="Notifications" onBack={() => navigate({ name: 'home' })}>
      <Note message={note} />
      {list.remote.status === 'loading' ? <Loading /> : null}
      {list.remote.status === 'error' ? <ErrorText message={list.remote.message} /> : null}
      {list.remote.status === 'ready' ? (
        <>
          {list.remote.data.notifications.map((row) => (
            <Card key={row.id}>
              <H2>{row.title}</H2>
              <Body>{row.body}</Body>
              <Muted>
                {row.kind} · {row.created_at.slice(0, 16).replace('T', ' ')}
                {row.read_at === null ? ' · unread' : ''}
              </Muted>
            </Card>
          ))}
          {list.remote.data.notifications.length === 0 ? (
            <Muted>Nothing yet. Review results, rework and payouts appear here.</Muted>
          ) : (
            <Button label="Mark all read" onPress={() => void readAll()} tone="ghost" />
          )}
        </>
      ) : null}
    </Screen>
  );
}

export function Settings({
  me,
  navigate,
  onSignedOut,
}: {
  me: MeOut;
  navigate: (route: Route) => void;
  onSignedOut: () => void;
}): JSX.Element {
  const profile = useApi<ProfileOut>('/me');
  const [note, setNote] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  async function setPreference(field: 'notify_email' | 'notify_push', value: boolean): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await api.patch<ProfileOut>('/me', { [field]: value });
      setNote('Preference saved.');
      profile.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save that preference.');
    } finally {
      setBusy(false);
    }
  }

  async function enablePush(): Promise<void> {
    setBusy(true);
    try {
      const token = await registerForPush();
      setNote(token ? 'This device will receive notifications.' : 'Push is not available on this device or permission was declined.');
    } finally {
      setBusy(false);
    }
  }

  async function exportData(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const data = await api.get<Record<string, unknown>>('/me/export');
      await Share.share({ message: JSON.stringify(data, null, 2), title: 'Nelavista data export' });
      setNote('Your export is ready in the share sheet.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not build your export.');
    } finally {
      setBusy(false);
    }
  }

  function confirmDelete(): void {
    Alert.alert(
      'Delete your account?',
      'This anonymises your account and signs out every device. Money and audit evidence stays to explain payouts, without your name or email.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: () => {
            void (async () => {
              try {
                await api.del('/auth/account');
                await logout();
                onSignedOut();
              } catch (err) {
                setError(err instanceof ApiError ? err.message : 'Could not delete your account.');
              }
            })();
          },
        },
      ],
    );
  }

  // Bind the loaded profile once: the notification toggles read it inside event
  // handlers, where the compiler cannot keep the union narrowed.
  const profileData = profile.remote.status === 'ready' ? profile.remote.data : null;

  return (
    <Screen title="Settings" onBack={() => navigate({ name: 'home' })}>
      <Card>
        <H2>{me.name ?? me.username}</H2>
        <Muted>
          {me.email} · {me.email_verified ? 'confirmed' : 'not confirmed'}
        </Muted>
        {me.email_verified ? null : (
          <Button
            label="Resend the confirmation link"
            tone="ghost"
            onPress={() => {
              void (async () => {
                try {
                  const result = await api.post<{ message: string }>('/auth/email/verify/resend');
                  setNote(result.message);
                } catch (err) {
                  setError(err instanceof ApiError ? err.message : 'Could not send the email.');
                }
              })();
            }}
          />
        )}
      </Card>

      {profile.remote.status === 'loading' ? <Loading /> : null}
      {profile.remote.status === 'error' ? <ErrorText message={profile.remote.message} /> : null}
      {profileData ? (
        <Card>
          <H2>Notifications</H2>
          <Body>Email notices: {profileData.notify_email ? 'on' : 'off'}</Body>
          <Button
            label={profileData.notify_email ? 'Turn email notices off' : 'Turn email notices on'}
            tone="ghost"
            onPress={() => void setPreference('notify_email', !profileData.notify_email)}
            disabled={busy}
          />
          <Body>Push notices: {profileData.notify_push ? 'on' : 'off'}</Body>
          <Button
            label={profileData.notify_push ? 'Turn push notices off' : 'Turn push notices on'}
            tone="ghost"
            onPress={() => void setPreference('notify_push', !profileData.notify_push)}
            disabled={busy}
          />
          <Button label="Register this device for push" onPress={() => void enablePush()} disabled={busy} />
        </Card>
      ) : null}

      <Note message={note} />
      <ErrorText message={error} />

      <Card>
        <H2>Your data</H2>
        <Muted>Share a machine-readable copy of everything V2 holds about you.</Muted>
        <Button label="Prepare my data export" tone="ghost" onPress={() => void exportData()} disabled={busy} />
      </Card>

      <Card>
        <H2>Delete account</H2>
        <Muted>Required by the app stores, and yours by right. This cannot be undone.</Muted>
        <Button label="Delete my account" tone="danger" onPress={confirmDelete} />
      </Card>

      <Button
        label="Sign out"
        tone="ghost"
        onPress={() => {
          void (async () => {
            await logout();
            onSignedOut();
          })();
        }}
      />
    </Screen>
  );
}
