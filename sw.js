/* ============================================================
   Bruno Brief — service worker
   Network-first for EVERYTHING (with cache fallback).
   Rationale: this is a daily-changing news app. Opening the app
   must always try the network for the latest build + feed, and only
   fall back to the cache when offline. This means app-code updates
   and new daily stories appear WITHOUT the user having to re-add the
   home-screen icon or clear cache — the previous cache-first shell
   caused stale builds that required a manual re-add to fix.
   ============================================================ */

const CACHE_VERSION = 'bruno-brief-v4';
const SHELL_ASSETS = [
  './',
  'index.html',
  'style.css',
  'app.js',
  'manifest.webmanifest',
  'deepdives.json',
  'icons/icon-180.png',
  'icons/icon-192.png',
  'icons/icon-512.png'
];

// ----- Install: pre-cache the shell ----------------------------------
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      // Use { cache: 'reload' } so first install always gets the latest.
      return Promise.all(
        SHELL_ASSETS.map((url) =>
          fetch(url, { cache: 'reload' })
            .then((res) => {
              if (res && res.ok) return cache.put(url, res.clone());
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

// ----- Fetch: NETWORK-FIRST for all same-origin GETs ------------------
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Network-first for everything — latest app + feed always tried first.
  event.respondWith(networkFirst(req));
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
    // Offline navigation fallback: serve the cached index if we have it.
    if (req.mode === 'navigate') {
      const index = await caches.match('index.html');
      if (index) return index;
    }
    // Last resort for data files: minimal offline response.
    if (req.url.includes('feed.json') || req.url.includes('deepdives.json')) {
      return new Response(
        JSON.stringify({ days: [], deepdives: {} }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }
    throw err;
  }
}