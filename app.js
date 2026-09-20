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

  // Deep-dive overlay refs
  var overlayEl    = document.getElementById('deepdive-overlay');
  var ddHeadline   = document.getElementById('dd-headline');
  var ddSummary    = document.getElementById('dd-summary');
  var ddUpdated    = document.getElementById('dd-updated');
  var ddDetail     = document.getElementById('dd-detail');
  var ddSources    = document.getElementById('dd-sources');
  var ddBucket     = document.getElementById('dd-bucket');

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

  function renderStoryCard(story, dayDate) {
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
      +        'data-slug="' + escapeHtml(slug) + '" '
      +        'data-date="' + escapeHtml(dayDate || '') + '" '
      +        'data-bucket="' + escapeHtml(bucket) + '" '
      +        'data-emoji="' + escapeHtml(emoji) + '" '
      +        'rel="noopener" target="_blank">Deep dive →</a>'
      +   '</div>'
      + '</article>';
  }

  function renderBucketSection(bucket, stories, dayDate) {
    if (!stories || stories.length === 0) return '';
    var cards = stories.map(function (s) { return renderStoryCard(s, dayDate); }).join('');
    return ''
      + '<section class="bucket" aria-label="' + escapeHtml(bucket.key) + '">'
      +   '<h2 class="bucket-header">'
      +     '<span class="bucket-emoji" aria-hidden="true">' + escapeHtml(bucket.emoji) + '</span>'
      +     escapeHtml(bucket.key)
      +   '</h2>'
      +   cards
      + '</section>';
  }

  // Parse YYYY-MM-DD (local) -> Date or null.
  function parseLocalDate(iso) {
    if (!iso) return null;
    var parts = String(iso).split('-').map(Number);
    if (parts.length !== 3 || parts.some(function (n) { return isNaN(n); })) {
      var d = new Date(iso);
      return isNaN(d.getTime()) ? null : d;
    }
    return new Date(parts[0], parts[1] - 1, parts[2]);
  }

  // Whole-day diff between two local dates (a - b).
  function wholeDaysBetween(a, b) {
    if (!a || !b) return 0;
    var ms = a.getTime() - b.getTime();
    return Math.round(ms / 86400000);
  }

  // Normalize a feed into an array of {date, stories[]} (newest-first).
  // Supports both the multi-day {days:[...]} shape and the legacy single-day
  // {date, stories[]} shape.
  function normalizeDays(feed) {
    if (!feed || typeof feed !== 'object') return [];
    if (Array.isArray(feed.days)) {
      return feed.days
        .filter(function (d) { return d && Array.isArray(d.stories); })
        .map(function (d) { return { date: d.date || '', stories: d.stories }; });
    }
    // Backwards-compat: legacy single-day shape.
    if (Array.isArray(feed.stories)) {
      return [{ date: feed.date || '', stories: feed.stories }];
    }
    return [];
  }

  function renderDaySection(day, isNewest, daysAgo) {
    var dateLabel = formatDate(day.date);
    var pill = '';
    if (isNewest) {
      pill = '<span class="day-header-pill" aria-label="Newest">Newest</span>';
    } else if (daysAgo === 1) {
      pill = '<span class="day-header-ago">Yesterday</span>';
    } else if (daysAgo > 1) {
      pill = '<span class="day-header-ago">' + escapeHtml(daysAgo) + ' days ago</span>';
    }
    var groups = groupStories(day.stories);
    var body = '';
    BUCKET_ORDER.forEach(function (bucket) {
      body += renderBucketSection(bucket, groups[bucket.key] || [], day.date);
    });
    return ''
      + '<section class="day-section" data-date="' + escapeHtml(day.date || '') + '" '
      +           'aria-label="Briefing for ' + escapeHtml(dateLabel) + '">'
      +   '<header class="day-header">'
      +     '<h2 class="day-header-date">' + escapeHtml(dateLabel) + '</h2>'
      +     pill
      +   '</header>'
      +   body
      + '</section>';
  }

  function render(feed) {
    var days = normalizeDays(feed);

    // Header date shows the newest day for backwards display compat.
    var headerDate = days.length ? (days[0].date || '') : (feed && feed.date) || '';
    dateEl.textContent = formatDate(headerDate);

    var totalStories = days.reduce(function (n, d) { return n + d.stories.length; }, 0);

    if (totalStories === 0) {
      storiesEl.innerHTML = '';
      storiesEl.hidden = true;
      emptyEl.hidden = false;
      errorEl.hidden = true;
      return;
    }

    emptyEl.hidden = true;
    errorEl.hidden = true;
    storiesEl.hidden = false;

    var latestDate = parseLocalDate(days[0].date);
    var html = '';
    for (var i = 0; i < days.length; i++) {
      var day = days[i];
      var daysAgo = i === 0 ? 0 : wholeDaysBetween(latestDate, parseLocalDate(day.date));
      html += renderDaySection(day, i === 0, daysAgo);
    }
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

  // ----- Deep dive (in-app detail) ---------------------------------------

  var deepCache = null; // lazy singleton: {deepdives: {slug: {...}}}

  function loadDeepDives(force) {
    // Return a cached promise of deepdives.json (network-first, cache fallback).
    if (deepCache && !force) return deepCache;
    var url = 'deepdives.json?_=' + Date.now();
    deepCache = fetch(url, { cache: 'no-store' })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .catch(function () {
        return caches.match('deepdives.json').then(function (cached) {
          if (!cached) throw new Error('no cached deepdives');
          return cached.json();
        });
      })
      .then(function (data) {
        return (data && data.deepdives) ? data : { deepdives: {} };
      })
      .catch(function () {
        return { deepdives: {} };
      });
    return deepCache;
  }

  function openDeepDive(slug, dateIso, meta) {
    var dd = null;
    loadDeepDives().then(function (d) {
      var byDate = (d && d.deepdives) || {};
      if (dateIso) {
        var bucket = byDate[dateIso];
        if (bucket && Object.prototype.hasOwnProperty.call(bucket, slug)) {
          dd = bucket[slug];
        }
      }
    }).then(function () {
      if (!dd) {
        // No in-app detail — fall back to the Telegram deepdive link.
        var fallback = DEEP_DIVE_BASE + encodeURIComponent(slug);
        window.open(fallback, '_blank');
        return;
      }
      renderDeepDive(dd, meta);
    });
  }

  function renderDeepDive(dd, meta) {
    ddHeadline.textContent = dd.headline || (meta && meta.headline) || 'Deep dive';
    ddSummary.textContent  = dd.summary || '';
    ddUpdated.textContent  = dd.updated ? ('Updated ' + formatDate(dd.updated)) : '';

    var bodyText = dd.detail || dd.content || '';
    var paragraphs = String(bodyText).split(/\n{2,}|\n/).filter(Boolean);
    var detailHtml = paragraphs.map(function (p) {
      return '<p>' + escapeHtml(p.trim()) + '</p>';
    }).join('');
    ddDetail.innerHTML = detailHtml || '<p>No detail available yet.</p>';

    var srcNames = Array.isArray(dd.sources) ? dd.sources : [];
    var urlList = Array.isArray(dd.source_urls) ? dd.source_urls : [];
    // If sources has no names but source_urls exists, show the URLs as labels.
    if (!srcNames.length && urlList.length) {
      srcNames = urlList;
    }
    var srcHtml = '';
    for (var i = 0; i < srcNames.length; i++) {
      var lbl = escapeHtml(srcNames[i]);
      if (urlList[i]) {
        srcHtml += '<a class="dd-source-link" href="' + escapeHtml(urlList[i]) + '" rel="noopener" target="_blank">' + lbl + ' ↗</a>';
      } else {
        srcHtml += '<span class="dd-source-link">' + lbl + '</span>';
      }
    }
    ddSources.innerHTML = srcHtml;

    ddBucket.textContent = (meta && (meta.bucket || meta.emoji))
      ? (meta.emoji ? meta.emoji + ' ' : '') + (meta.bucket || '')
      : '';
    showOverlay();
  }

  function showOverlay() {
    overlayEl.hidden = false;
    overlayEl.setAttribute('aria-hidden', 'false');
    if (document.body) document.body.classList.add('dd-open');
    var f = overlayEl.querySelector('.deepdive-back, .deepdive-close, button');
    if (f && f.focus) f.focus();
  }

  function closeOverlay() {
    overlayEl.hidden = true;
    overlayEl.setAttribute('aria-hidden', 'true');
    if (document.body) document.body.classList.remove('dd-open');
  }

  function bindDeepDiveEvents() {
    // Intercept every "Deep dive" tap on the stories list.
    storiesEl.addEventListener('click', function (ev) {
      var target = ev.target;
      var anchor = target.closest ? target.closest('a.deep-dive') : null;
      if (!anchor) return;
      var slug = anchor.getAttribute('data-slug') || '';
      if (!slug) return;
      var dateIso = anchor.getAttribute('data-date') || '';
      var meta = {
        headline: (anchor.closest('.card') && anchor.closest('.card').querySelector('.card-headline'))
            ? anchor.closest('.card').querySelector('.card-headline').textContent.trim() : null,
        bucket: anchor.getAttribute('data-bucket') || '',
        emoji: anchor.getAttribute('data-emoji') || ''
      };
      ev.preventDefault();
      ev.stopPropagation();
      openDeepDive(slug, dateIso, meta);
      return false;
    });

    // Close affordances: backdrop tap, back button, Escape key.
    var closeEls = overlayEl ? Array.prototype.slice.call(overlayEl.querySelectorAll('[data-dd-close]')) : [];
    closeEls.forEach(function (el) {
      el.addEventListener('click', closeOverlay);
    });
    window.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && overlayEl && overlayEl.hidden === false) closeOverlay();
    });
  }
  bindDeepDiveEvents();

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
