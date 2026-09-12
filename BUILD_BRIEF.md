# BUILD BRIEF — iPhone "app icon" PWA: World News Daily Brief

**Goal:** A self-contained PWA (Progressive Web App) that installs to an iPhone home screen and feels like a native news app. It displays the daily world-news briefing (produced by Bruno's cron each morning), with a "deepdive" action per story.

## Deliverable — static site in `/home/rory/Projects/news-pwa/` (create dirs as needed)

Be self-contained: NO frameworks, NO build step, NO npm. Just plain HTML/CSS/JS that works when served statically over HTTPS.

## Files to produce

1. `index.html` — the app shell.
   - Title "Bruno Brief" (display name).
   - Reads the feed from `feed.json` (same directory) at load.
   - Layout: an app header, the date, then the stories grouped by the standard buckets.
2. `style.css` — clean, native-feeling iOS aesthetic. Dark-mode friendly. Support `safe-area-inset-*` for the notch/home bar. System font stack. Compact cards per story.
3. `app.js` — fetch `feed.json`, render stories. Each story card shows: emoji + bucket label, headline, 1–2 line summary, source tag(s). A **"Deep dive →"** button per story opens a Telegram link: `https://t.me/bruno_baker_bot?start=deepdive_<slug>` where `<slug>` is a url-safe topic slug. (This routes back to Bruno for the full-depth pull.)
4. `manifest.webmanifest` — PWA manifest: name/short_name "Bruno Brief", `display: standalone`, background/theme colors, and icons (see below). `start_url: ./` and `scope: ./`.
5. `sw.js` — service worker: cache the app shell (index.html, style.css, app.js, manifest, icons) on install; network-first for `feed.json` with cache fallback; basic offline support.
6. Icons — generate via Bruno (he will handle). The brief assumes `icons/icon-192.png` and `icons/icon-512.png` will exist; reference them in the manifest and as `<link rel=apple-touch-icon>`.
7. `feed.json` — an empty-but-valid feed: `{"date":"", "stories":[]}` so the app renders an "empty state" gracefully before the first real feed lands. The app must handle an empty feed without crashing.

## feed.json contract (what the daily cron will write later)

```json
{
  "date": "2026-09-13",
  "stories": [
    {
      "bucket": "US Bond Market",
      "emoji": "🇺🇸",
      "headline": "...",
      "summary": "...",
      "sources": ["Reuters", "CNBC"],
      "slug": "us-bond-market"
    }
  ]
}
```
Buckets the app should label: US Bond Market, Australian Politics, Conflicts, Science/Tech, Blowing Up Today.

## Behaviour requirements (acceptance criteria)

- `spa` deep-dive buttons are real links (`<a href="https://t.me/bruno_baker_bot?start=deepdive_...">`), not JS-only.
- App still renders (with a friendly "No briefing yet today" message) when feed.json has no stories.
- Service worker registers without errors; shell is cached; app works offline after first visit.
- `manifest.webmanifest` passes a PWA linter (display standalone, has icons, name present).
- No console errors when opening index.html via a local static server.
- iPhone install readiness: meta tags `apple-mobile-web-app-capable` / `mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `apple-touch-icon` link present.

## Constraints for the agent

- Write real, working files. Do not stub.
- Keep it visually clean — this will run on an iPhone. Avoid clutter.
- Do NOT attempt network calls to anything but `feed.json` (relative path).
- Do NOT include any analytics, tracking, or third-party scripts.
