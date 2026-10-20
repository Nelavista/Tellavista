/**
 * Push registration (D1, F4).
 *
 * The token is registered against the signed-in account, so a shared phone
 * reassigns it rather than leaking another student's notifications. Permission
 * denial is not an error: the in-app notification list still works.
 */
import Constants from 'expo-constants';
import * as Notifications from 'expo-notifications';

import { PLATFORM, api } from './api';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: true,
  }),
});

export async function registerForPush(): Promise<string | null> {
  const existing = await Notifications.getPermissionsAsync();
  let granted = existing.granted;
  if (!granted) {
    const requested = await Notifications.requestPermissionsAsync();
    granted = requested.granted;
  }
  if (!granted) return null;

  const projectId =
    (Constants.expoConfig?.extra as { eas?: { projectId?: string } } | undefined)?.eas?.projectId ??
    undefined;
  try {
    const token = await Notifications.getExpoPushTokenAsync(projectId ? { projectId } : undefined);
    await api.post('/me/push-devices', { token: token.data, platform: PLATFORM });
    return token.data;
  } catch {
    // A simulator has no push token; the account is still usable.
    return null;
  }
}

export function onNotificationTapped(
  handler: (data: Record<string, unknown>) => void,
): () => void {
  const subscription = Notifications.addNotificationResponseReceivedListener((response) => {
    handler((response.notification.request.content.data ?? {}) as Record<string, unknown>);
  });
  return () => subscription.remove();
}
