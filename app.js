/* ============================================================
   Bruno Brief — app.js
   Fetches feed.json, groups stories by bucket, renders cards
   with real <a> deep-dive links, shows empty state gracefully.
   ============================================================ */

(function () {
  'use strict';

  // ----- Configuration ---------------------------------------------------

  // Canonical bucket order (icons in spec). Anything not listed falls in
  // "Blowing Up Today" so an unknown bucket still surfaces something.
  var BUCKET_ORDER = [
    { key: 'US Bond Market',     emoji: '🇺🇸' },
    { key: 'Australian Politics', emoji: '🦘' },
    { key: 'European Politics',  emoji: '🇪🇺' },
    { key: 'AI News',            emoji: '🤖' },
    { key: 'Conflicts',          emoji: '⚔️' },
    { key: 'Science/Tech',       emoji: '🔬' },
    { key: 'Blowing Up Today',   emoji: '🔥' }
  ];
  var FALLBACK_BUCKET_KEY = 'Blowing Up Today';
  var FALLBACK_BUCKET_EMOJI = '🔥';

  // Deep-dive Telegram URL — real link, not a JS callback.
  var DEEP_DIVE_BASE = 'https://t.me/bruno_baker_bot?start=deepdive_';

  // ----- DOM refs --------------------------------------------------------

  var storiesEl    = document.getElementById('stories');
  var emptyEl      = document.getElementById('empty-state');
  var errorEl      = document.getElementById('error-state');
  var dateEl       = document.getElementById('app-date');

  // ----- Helpers ---------------------------------------------------------

  function escapeHtml(s) {
    if (s == null) return '';
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // Slug helper — feed entries may already have a slug, but we sanitize
  // so the URL is always safe. Falls back to a slug derived from the headline.
  function toSlug(s) {
    var fallback = String(s || '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 60);
    return fallback || 'story';
  }

  function formatDate(iso) {
    if (!iso) return 'Today';
    // Parse YYYY-MM-DD as a local date (not UTC) to avoid off-by-one.
    var parts = iso.split('-').map(Number);
    var d;
    if (parts.length === 3 && parts.every(function (n) { return !isNaN(n); })) {
      d = new Date(parts[0], parts[1] - 1, parts[2]);
    } else {
      d = new Date(iso);
    }
    if (isNaN(d.getTime())) return iso;
    var opts = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    try {
      return d.toLocaleDateString(undefined, opts);
    } catch (e) {
      return iso;
    }
  }

  function findBucket(rawBucket) {
    if (!rawBucket) return null;
    for (var i = 0; i < BUCKET_ORDER.length; i++) {
      if (BUCKET_ORDER[i].key.toLowerCase() === String(rawBucket).toLowerCase()) {
        return BUCKET_ORDER[i];
      }
    }
    return null;
  }

  function groupStories(stories) {
    var groups = {};
    BUCKET_ORDER.forEach(function (b) { groups[b.key] = []; });

    stories.forEach(function (story) {
      var bucket = findBucket(story.bucket) || {
        key: story.bucket || FALLBACK_BUCKET_KEY,
        emoji: story.emoji || FALLBACK_BUCKET_EMOJI
      };
      if (!groups[bucket.key]) {
        groups[bucket.key] = [];
        // Promote ad-hoc buckets into BUCKET_ORDER at render time
        BUCKET_ORDER.push(bucket);
      }
      groups[bucket.key].push(story);
    });
    return groups;
  }

  // ----- Rendering -------------------------------------------------------

  function renderStoryCard(story) {
    var emoji     = story.emoji || '';
    var bucket    = story.bucket || '';
    var headline  = story.headline || 'Untitled';
    var summary   = story.summary || '';
    var sources   = Array.isArray(story.sources) ? story.sources : [];
    var slug      = toSlug(story.slug || headline);

    var deepDiveUrl = DEEP_DIVE_BASE + encodeURIComponent(slug);

    var sourceTags = sources.map(function (s) {
      return '<span class="source-tag">' + escapeHtml(s) + '</span>';
    }).join('');

    return ''
      + '<article class="card">'
      +   '<h3 class="card-headline">'
      +     '<span class="card-emoji" aria-hidden="true">' + escapeHtml(emoji) + '</span>'
      +     escapeHtml(bucket ? bucket + ' · ' : '')
      +     escapeHtml(headline)
      +   '</h3>'
      +   (summary ? '<p class="card-summary">' + escapeHtml(summary) + '</p>' : '')
      +   '<div class="card-meta">'
      +     '<div class="card-sources">' + sourceTags + '</div>'
      +     '<a class="deep-dive" href="' + escapeHtml(deepDiveUrl) + '" '
      +        'rel="noopener" target="_blank">Deep dive →</a>'
      +   '</div>'
      + '</article>';
  }

  function renderBucketSection(bucket, stories) {
    if (!stories || stories.length === 0) return '';
    var cards = stories.map(renderStoryCard).join('');
    return ''
      + '<section class="bucket" aria-label="' + escapeHtml(bucket.key) + '">'
      +   '<h2 class="bucket-header">'
      +     '<span class="bucket-emoji" aria-hidden="true">' + escapeHtml(bucket.emoji) + '</span>'
      +     escapeHtml(bucket.key)
      +   '</h2>'
      +   cards
      + '</section>';
  }

  function render(feed) {
    var stories = (feed && Array.isArray(feed.stories)) ? feed.stories : [];
    dateEl.textContent = formatDate(feed && feed.date);

    if (stories.length === 0) {
      storiesEl.innerHTML = '';
      storiesEl.hidden = true;
      emptyEl.hidden = false;
      errorEl.hidden = true;
      return;
    }

    emptyEl.hidden = true;
    errorEl.hidden = true;
    storiesEl.hidden = false;

    var groups = groupStories(stories);
    var html = '';
    BUCKET_ORDER.forEach(function (bucket) {
      html += renderBucketSection(bucket, groups[bucket.key] || []);
    });
    storiesEl.innerHTML = html;
  }

  function showError() {
    storiesEl.hidden = true;
    emptyEl.hidden = true;
    errorEl.hidden = false;
    dateEl.textContent = '—';
  }

  // ----- Network ---------------------------------------------------------

  function loadFeed() {
    // Try network first; fall back to cache if the SW cached a previous feed.
    // If both fail, show the error state.
    var url = 'feed.json?_=' + Date.now(); // bypass HTTP cache so we always try network
    return fetch(url, { cache: 'no-store' })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .catch(function () {
        return caches.match('feed.json').then(function (cached) {
          if (!cached) throw new Error('no cached feed');
          return cached.json();
        });
      })
      .then(function (feed) {
        render(feed || { date: '', stories: [] });
      })
      .catch(function () {
        showError();
      });
  }

  // ----- Service worker --------------------------------------------------

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('sw.js').then(function (reg) {
        // iOS Safari caches SW updates aggressively — re-trigger the update
        // check on every launch so new shells/versions get picked up.
        if (reg && reg.update) reg.update();
      }).catch(function (err) {
        // Non-fatal: app still works, just no offline cache.
        console.warn('Service worker registration failed:', err);
      });
    });
  }

  // ----- Boot ------------------------------------------------------------

  loadFeed();
})();
