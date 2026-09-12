/* ============================================================
   Bruno Brief — service worker
   - Pre-cache the app shell on install.
   - Network-first for feed.json with cache fallback.
   - Cache-first for everything else in the shell.
   ============================================================ */

const CACHE_VERSION = 'bruno-brief-v1';
const SHELL_ASSETS = [
  './',
  'index.html',
  'style.css',
  'app.js',
  'manifest.webmanifest',
  'icons/icon-180.png',
  'icons/icon-192.png',
  'icons/icon-512.png'
];

// ----- Install: pre-cache the shell ----------------------------------
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      // Use { cache: 'reload' } so we always get the latest from the server
      // for the first install, even if HTTP cache would otherwise 304 us.
      return Promise.all(
        SHELL_ASSETS.map((url) =>
          fetch(url, { cache: 'reload' })
            .then((res) => {
              if (res && res.ok) {
                return cache.put(url, res.clone());
              }
              return null;
            })
            .catch(() => null) // best-effort: missing icons shouldn't block install
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// ----- Activate: clean up old caches ---------------------------------
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_VERSION)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// ----- Fetch: routing -------------------------------------------------
self.addEventListener('fetch', (event) => {
  const req = event.request;

  // Only handle GET requests on our own scope.
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Network-first for feed.json, with cache fallback.
  if (url.pathname.endsWith('/feed.json') || url.pathname.endsWith('feed.json')) {
    event.respondWith(networkFirst(req));
    return;
  }

  // Cache-first for shell assets (index, css, js, manifest, icons).
  event.respondWith(cacheFirst(req));
});

async function networkFirst(req) {
  try {
    const fresh = await fetch(req);
    if (fresh && fresh.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(req, fresh.clone());
    }
    return fresh;
  } catch (err) {
    const cached = await caches.match(req);
    if (cached) return cached;
    // Last resort: return a minimal offline feed so the UI shows empty state
    // rather than crashing.
    return new Response(
      JSON.stringify({ date: '', stories: [] }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

async function cacheFirst(req) {
  const cached = await caches.match(req);
  if (cached) return cached;
  try {
    const fresh = await fetch(req);
    if (fresh && fresh.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(req, fresh.clone());
    }
    return fresh;
  } catch (err) {
    // Offline navigation fallback: serve the cached index if we have it.
    if (req.mode === 'navigate') {
      const index = await caches.match('index.html');
      if (index) return index;
    }
    throw err;
  }
}
