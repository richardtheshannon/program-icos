/*
 * drawer.js — JSON-driven app drawer renderer.
 *
 * Single source of truth for the app drawer is apps.json (hosted at the apex,
 * https://icos.dev/apps.json). Every site in the icos.dev family ships this
 * same file; on page load it fetches the JSON and rebuilds the .drawer-body
 * + .drawer-foot label from it. The tile whose `id` matches <meta name="app-id">
 * gets the .accent class so the user sees "you are here" highlighted.
 *
 * Render pipeline:
 *   1. Read meta tags: app-id (required) + apps-json-url (optional, defaults
 *      to https://icos.dev/apps.json).
 *   2. Cache-first render from localStorage["icos_apps_v1"] if present and
 *      schema version matches — no FOUC on repeat visits.
 *   3. Background fetch the JSON. If fresh differs from cached, update both
 *      the DOM and the cache. If fetch fails and there is no cache, render
 *      an empty drawer body and log a warning.
 *
 * Open/close behaviour stays in frame.js — drawer.js only fills in contents.
 * The shell (<aside id="app-drawer">, drawer-head with #app-drawer-close,
 * empty .drawer-body, .drawer-foot) lives in static markup so frame.js's
 * getElementById lookups resolve at parse time regardless of fetch latency.
 *
 * No dependencies. Loaded with `defer`.
 */

(function () {
    'use strict';

    var SCHEMA_VERSION = 1;
    var CACHE_KEY = 'icos_apps_v1';
    var DEFAULT_URL = 'https://icos.dev/apps.json';

    var meta = {
        appId: getMeta('app-id') || '',
        jsonUrl: getMeta('apps-json-url') || DEFAULT_URL
    };

    var body = document.querySelector('#app-drawer .drawer-body');
    var footLabel = document.querySelector('#app-drawer .drawer-foot > span');
    if (!body) return; // No drawer on this page; nothing to do.

    // Step 1: render from cache instantly if valid.
    var cached = readCache();
    if (cached) render(cached);

    // Step 2: fetch fresh JSON in the background.
    fetch(meta.jsonUrl, { credentials: 'omit', cache: 'no-store' })
        .then(function (res) {
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return res.json();
        })
        .then(function (data) {
            if (!data || data.version !== SCHEMA_VERSION) {
                console.warn('[drawer] apps.json schema mismatch:', data && data.version);
                return;
            }
            writeCache(data);
            // Only re-render if the new payload differs from what's already shown.
            if (!cached || JSON.stringify(data) !== JSON.stringify(cached)) {
                render(data);
            }
        })
        .catch(function (err) {
            console.warn('[drawer] apps.json fetch failed:', err && err.message);
            if (!cached) renderEmpty();
        });

    // ---- helpers ----

    function getMeta(name) {
        var el = document.querySelector('meta[name="' + name + '"]');
        return el ? el.getAttribute('content') : null;
    }

    function readCache() {
        try {
            var raw = localStorage.getItem(CACHE_KEY);
            if (!raw) return null;
            var obj = JSON.parse(raw);
            if (!obj || obj.version !== SCHEMA_VERSION) return null;
            return obj;
        } catch (e) { return null; }
    }

    function writeCache(data) {
        try { localStorage.setItem(CACHE_KEY, JSON.stringify(data)); } catch (e) {}
    }

    function render(data) {
        body.innerHTML = '';
        (data.sections || []).forEach(function (section) {
            body.appendChild(renderSection(section));
        });
        if (footLabel && data.footer && typeof data.footer.label === 'string') {
            footLabel.textContent = data.footer.label;
        }
    }

    function renderEmpty() {
        body.innerHTML = '';
    }

    function renderSection(section) {
        var wrap = document.createElement('div');
        wrap.className = 'drawer-section';
        var h = document.createElement('h6');
        h.textContent = section.title || '';
        wrap.appendChild(h);
        var grid = document.createElement('div');
        grid.className = 'drawer-grid';
        (section.tiles || []).forEach(function (tile) {
            grid.appendChild(renderTile(tile));
        });
        wrap.appendChild(grid);
        return wrap;
    }

    function renderTile(tile) {
        var isCurrent = tile.id && tile.id === meta.appId;
        var clickable = !tile.disabled && !!tile.url;
        var el;

        if (clickable) {
            el = document.createElement('a');
            el.href = tile.url;
            if (tile.id) el.setAttribute('data-id', tile.id);
        } else {
            el = document.createElement('button');
            el.type = 'button';
            el.disabled = true;
        }

        el.className = isCurrent ? 'app-tile accent' : 'app-tile';

        var glyph = document.createElement('span');
        glyph.className = 'glyph';
        glyph.innerHTML = tile.icon || '';
        el.appendChild(glyph);

        var lbl = document.createElement('span');
        lbl.className = 'lbl';
        lbl.textContent = tile.label || '';
        el.appendChild(lbl);

        return el;
    }
})();
