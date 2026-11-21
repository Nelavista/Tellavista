/* eslint-env serviceworker */
/**
 * Web Push delivery for the app shell.
 *
 * This file is imported by the generated Workbox service worker
 * (`workbox.importScripts` in vite.config.ts), so it shares that worker's scope
 * and lifecycle. It deliberately does nothing else: caching is Workbox's job,
 * and a second `fetch` handler here would make offline behaviour depend on load
 * order between two scripts.
 *
 * The payload comes from `app/worker/tasks.py::_send_web_push`. Every field is
 * treated as optional because a push is delivered by the browser, not by us: an
 * OS-level test message has no title and must still render something readable.
 */
self.addEventListener('push', function (event) {
  var payload = {};
  try {
    payload = event.data ? event.data.json() : {};
  } catch (error) {
    payload = { body: event.data ? event.data.text() : '' };
  }

  var data = payload.data && typeof payload.data === 'object' ? payload.data : {};
  var url = typeof data.url === 'string' && data.url ? data.url : '/notifications';
  var title = payload.title || 'Nelavista';

  event.waitUntil(
    self.registration.showNotification(title, {
      body: payload.body || '',
      icon: '/icons/icon-192.png',
      badge: '/icons/icon-192.png',
      // A stable tag per notification means a retry replaces the banner instead
      // of stacking a duplicate of the same event.
      tag: payload.notification_id ? 'notification-' + payload.notification_id : undefined,
      data: { url: url, notificationId: payload.notification_id || null },
    }),
  );
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  var url = (event.notification.data && event.notification.data.url) || '/notifications';

  event.waitUntil(
    self.clients
      .matchAll({ type: 'window', includeUncontrolled: true })
      .then(function (clients) {
        // Reuse an open tab when there is one: a second copy of the app would
        // make the student sign in again and lose unsaved state.
        for (var index = 0; index < clients.length; index += 1) {
          var client = clients[index];
          if ('focus' in client) {
            if ('navigate' in client) {
              return client.navigate(url).then(function () {
                return client.focus();
              });
            }
            return client.focus();
          }
        }
        return self.clients.openWindow(url);
      }),
  );
});
