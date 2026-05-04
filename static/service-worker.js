// service-worker.js
// Nelavista PWA Service Worker
// Network-first with cache fallback strategy

const CACHE_NAME = 'nelavista-v1';

// Files to precache (add all critical assets)
const PRECACHE_URLS = [
  '/',
  '/offline',
  '/static/css/main.css',         // adjust to your actual CSS file
  '/static/js/main.js',           // adjust to your main JS bundle
  '/static/icons/nelavista-72x72.png',
  '/static/icons/nelavista-96x96.png',
  '/static/icons/nelavista-128x128.png',
  '/static/icons/nelavista-144x144.png',
  '/static/icons/nelavista-152x152.png',
  '/static/icons/nelavista-192x192.png',
  '/static/icons/nelavista-384x384.png',
  '/static/icons/nelavista-512x512.png'
];

// Install event: precache essential files and take control immediately
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(PRECACHE_URLS);
      })
      .catch(err => console.error('Precache failed:', err))
  );
  self.skipWaiting();
});

// Activate event: delete old caches and claim clients
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event: network-first with timeout, fallback to cache, then offline page
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Skip chrome-extension requests, etc.
  const url = new URL(event.request.url);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  event.respondWith(
    // Try network with a 3-second timeout
    networkTimeout(event.request, 3000)
      .then(networkResponse => {
        // Update cache with fresh response (if valid)
        const clonedResponse = networkResponse.clone();
        caches.open(CACHE_NAME).then(cache => {
          if (networkResponse.status === 200) {
            cache.put(event.request, clonedResponse);
          }
        });
        return networkResponse;
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(event.request).then(cachedResponse => {
          if (cachedResponse) return cachedResponse;
          // If requesting a page (navigate), return the offline page
          if (event.request.mode === 'navigate') {
            return caches.match('/offline');
          }
          // For other resources, return a simple error (or nothing)
          return new Response('Offline', { status: 503 });
        });
      })
  );
});

// Helper: fetch with timeout
function networkTimeout(request, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timeoutId = setTimeout(() => reject(new Error('Network timeout')), timeoutMs);
    fetch(request).then(response => {
      clearTimeout(timeoutId);
      resolve(response);
    }).catch(err => {
      clearTimeout(timeoutId);
      reject(err);
    });
  });
}