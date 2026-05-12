const CACHE_VERSION = '2.0';
const CACHE_NAME = `nelavista-v${CACHE_VERSION}`;
const RUNTIME_CACHE = `${CACHE_NAME}-runtime`;
const API_CACHE = `${CACHE_NAME}-api`;

// ===== PRECACHE: Critical files that must be available offline =====
const PRECACHE_URLS = [
  // Core pages
  '/',
  '/offline',
  
  // Critical icons (all sizes for PWA installation)
  '/static/icons/nelavista-16x16.png',
  '/static/icons/nelavista-32x32.png',
  '/static/icons/nelavista-72x72.png',
  '/static/icons/nelavista-96x96.png',
  '/static/icons/nelavista-128x128.png',
  '/static/icons/nelavista-144x144.png',
  '/static/icons/nelavista-152x152.png',
  '/static/icons/nelavista-167x167.png',
  '/static/icons/nelavista-180x180.png',
  '/static/icons/nelavista-192x192.png',
  '/static/icons/nelavista-384x384.png',
  '/static/icons/nelavista-512x512.png',
  '/static/icons/favicon.ico',
  
  // PWA manifest
  '/manifest.json',
  
  // CSS files (update paths to match your actual files)
  '/static/css/main.css',
  '/static/css/dashboard.css',
  
  // JS files (update paths to match your actual files)
  '/static/js/main.js',
  '/static/js/pwa-install.js',
  
  // External dependencies needed offline
  'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
];

// ===== INSTALL EVENT =====
self.addEventListener('install', event => {
  console.log('🔧 [SW] Installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 [SW] Pre-caching critical assets...');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => {
        console.log('✅ [SW] Pre-cache complete');
        return self.skipWaiting();
      })
      .catch(err => {
        console.error('❌ [SW] Pre-cache failed:', err);
        // Don't fail installation - app can still work online
      })
  );
});

// ===== ACTIVATE EVENT =====
self.addEventListener('activate', event => {
  console.log('⚡ [SW] Activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            // Delete any cache that isn't current version
            if (cacheName !== CACHE_NAME && 
                cacheName !== RUNTIME_CACHE && 
                cacheName !== API_CACHE) {
              console.log('🗑️ [SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ [SW] Activation complete');
        return self.clients.claim();
      })
  );
});

// ===== FETCH EVENT =====
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') return;
  
  // Skip non-http(s) requests (chrome-extension://, etc.)
  if (!url.protocol.startsWith('http')) return;
  
  // ===== STRATEGY 1: API calls - Network only (no caching) =====
  if (url.pathname.startsWith('/api/') || 
      url.hostname.includes('openrouter.ai') ||
      url.hostname.includes('google-analytics.com') ||
      url.hostname.includes('googletagmanager.com')) {
    
    event.respondWith(fetch(request).catch(() => {
      return new Response(
        JSON.stringify({ 
          error: 'You are offline', 
          message: 'This feature requires internet connection' 
        }),
        { 
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }));
    return;
  }
  
  // ===== STRATEGY 2: HTML/Navigation - Network first, cache fallback =====
  if (request.mode === 'navigate' || 
      request.headers.get('Accept')?.includes('text/html')) {
    
    event.respondWith(
      networkFirstWithTimeout(request, 5000)
        .catch(() => {
          return caches.match(request)
            .then(cachedResponse => {
              if (cachedResponse) {
                console.log('📦 [SW] Serving from cache:', url.pathname);
                return cachedResponse;
              }
              // Ultimate fallback: offline page
              return caches.match('/offline');
            });
        })
    );
    return;
  }
  
  // ===== STRATEGY 3: Static assets - Cache first, network update =====
  if (url.pathname.startsWith('/static/') ||
      url.hostname === 'cdn.jsdelivr.net' ||
      url.hostname === 'fonts.googleapis.com' ||
      url.hostname === 'fonts.gstatic.com') {
    
    event.respondWith(
      staleWhileRevalidate(request)
    );
    return;
  }
  
  // ===== STRATEGY 4: Everything else - Network first, cache fallback =====
  event.respondWith(
    networkFirstWithTimeout(request, 3000)
      .then(response => {
        // Cache successful responses
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(RUNTIME_CACHE).then(cache => {
            cache.put(request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(request)
          .then(cached => cached || new Response('Offline', { status: 503 }));
      })
  );
});

// ===== MESSAGE EVENT: Handle messages from the main thread =====
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    clearAllCaches();
  }
});

// ===== BACKGROUND SYNC: Retry failed requests when back online =====
self.addEventListener('sync', event => {
  if (event.tag === 'sync-offline-messages') {
    event.waitUntil(syncFailedMessages());
  }
  
  if (event.tag === 'sync-study-progress') {
    event.waitUntil(syncStudyProgress());
  }
});

// ===== PUSH NOTIFICATIONS =====
self.addEventListener('push', event => {
  let notificationData = {};
  
  if (event.data) {
    try {
      notificationData = event.data.json();
    } catch {
      notificationData = {
        title: 'Nelavista',
        body: event.data.text() || 'New notification from Nelavista'
      };
    }
  }
  
  const options = {
    body: notificationData.body || 'You have an update from Nelavista',
    icon: '/static/icons/nelavista-192x192.png',
    badge: '/static/icons/nelavista-72x72.png',
    vibrate: [200, 100, 200],
    data: notificationData.data || {},
    actions: [
      {
        action: 'open',
        title: 'Open Nelavista',
        icon: '/static/icons/nelavista-32x32.png'
      },
      {
        action: 'close',
        title: 'Dismiss'
      }
    ],
    tag: notificationData.tag || 'nelavista-notification',
    renotify: true,
    requireInteraction: false
  };
  
  event.waitUntil(
    self.registration.showNotification(
      notificationData.title || 'Nelavista',
      options
    )
  );
});

// ===== NOTIFICATION CLICK =====
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.action === 'close') return;
  
  const urlToOpen = event.notification.data?.url || '/';
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(clientList => {
        // Check if there's already a window open
        for (const client of clientList) {
          if (client.url.includes(self.registration.scope) && 'focus' in client) {
            return client.focus();
          }
        }
        // Open new window
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});

// ===== HELPER FUNCTIONS =====

// Network-first strategy with timeout
function networkFirstWithTimeout(request, timeoutMs) {
  return new Promise((resolve, reject) => {
    let timeoutId;
    
    // Set timeout
    const timeout = new Promise((_, reject) => {
      timeoutId = setTimeout(() => {
        reject(new Error(`Request timeout: ${request.url}`));
      }, timeoutMs);
    });
    
    // Race between network and timeout
    Promise.race([
      fetch(request),
      timeout
    ])
    .then(response => {
      clearTimeout(timeoutId);
      resolve(response);
    })
    .catch(error => {
      clearTimeout(timeoutId);
      reject(error);
    });
  });
}

// Stale-while-revalidate strategy (serve cached, update in background)
function staleWhileRevalidate(request) {
  return caches.open(RUNTIME_CACHE).then(cache => {
    return cache.match(request).then(cachedResponse => {
      // Start network fetch in background
      const fetchPromise = fetch(request)
        .then(networkResponse => {
          // Update cache
          if (networkResponse.status === 200) {
            cache.put(request, networkResponse.clone());
          }
          return networkResponse;
        })
        .catch(err => console.log('Background fetch failed:', err));
      
      // Return cached response immediately, or wait for network
      return cachedResponse || fetchPromise;
    });
  });
}

// Clear all caches
async function clearAllCaches() {
  const cacheNames = await caches.keys();
  console.log('🗑️ [SW] Clearing all caches:', cacheNames);
  
  await Promise.all(
    cacheNames.map(name => caches.delete(name))
  );
  
  console.log('✅ [SW] All caches cleared');
  
  // Notify all clients
  const clients = await self.clients.matchAll();
  clients.forEach(client => {
    client.postMessage({ type: 'CACHES_CLEARED' });
  });
}

// Sync failed messages when back online
async function syncFailedMessages() {
  console.log('🔄 [SW] Syncing failed messages...');
  
  try {
    // Open IndexedDB to get queued messages
    const db = await openQueueDatabase();
    const messages = await getAllQueuedMessages(db);
    
    for (const message of messages) {
      try {
        const response = await fetch(message.url, {
          method: message.method,
          headers: message.headers,
          body: message.body
        });
        
        if (response.ok) {
          await deleteQueuedMessage(db, message.id);
          console.log('✅ [SW] Synced message:', message.id);
        }
      } catch (err) {
        console.error('❌ [SW] Failed to sync message:', message.id, err);
      }
    }
  } catch (err) {
    console.error('❌ [SW] Sync failed:', err);
  }
}

// Sync study progress when back online
async function syncStudyProgress() {
  console.log('🔄 [SW] Syncing study progress...');
  
  const openDB = indexedDB.open('NelavistaOffline', 1);
  
  return new Promise((resolve, reject) => {
    openDB.onsuccess = async (event) => {
      const db = event.target.result;
      const transaction = db.transaction(['progress'], 'readonly');
      const store = transaction.objectStore('progress');
      const progress = await store.getAll();
      
      if (progress.length > 0) {
        try {
          await fetch('/api/track-session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ offline_sessions: progress })
          });
          
          // Clear synced progress
          const clearTransaction = db.transaction(['progress'], 'readwrite');
          const clearStore = clearTransaction.objectStore('progress');
          await clearStore.clear();
          
          console.log('✅ [SW] Progress synced');
        } catch (err) {
          console.error('❌ [SW] Progress sync failed:', err);
        }
      }
      
      resolve();
    };
    
    openDB.onerror = () => reject(openDB.error);
  });
}

// IndexedDB helpers for offline queue
function openQueueDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('NelavistaQueue', 1);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('messages')) {
        db.createObjectStore('messages', { 
          keyPath: 'id', 
          autoIncrement: true 
        });
      }
    };
    
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function getAllQueuedMessages(db) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(['messages'], 'readonly');
    const store = transaction.objectStore('messages');
    const request = store.getAll();
    
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function deleteQueuedMessage(db, id) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(['messages'], 'readwrite');
    const store = transaction.objectStore('messages');
    const request = store.delete(id);
    
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

// ===== LIFECYCLE LOGGING =====
console.log('📱 Nelavista Service Worker v2.0 loaded');
console.log('📦 Cache name:', CACHE_NAME);
console.log('🎯 Pre-cached URLs:', PRECACHE_URLS.length);
