// program.icos.dev (PS01) — app-shell service worker.
// Cache-first for /static/**, network-first (no-cache) for everything else.
// Dynamic routes (/admin/**, /login/, /logout/, mutation endpoints), non-GET,
// and any request carrying an Authorization header bypass the worker entirely.

const CACHE_NAME = 'ps01-v1';
const APP_SHELL = [
    '/static/css/tokens.css',
    '/static/css/app.css',
    '/static/js/htmx.min.js',
    '/static/js/preferences.js',
    '/static/js/drawer.js',
    '/static/js/frame.js',
    '/static/js/dashboard-clock.js',
    '/static/js/pull-to-refresh.js',
    '/static/js/sw-register.js',
    '/static/images/hero-forest.jpg',
    '/static/icons/icon-192.png',
    '/static/icons/icon-512.png',
    '/static/icons/icon-maskable.png',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(APP_SHELL))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(
                keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
            ))
            .then(() => self.clients.claim())
    );
});

function isBypass(req, url) {
    if (req.method !== 'GET') return true;
    if (req.headers.has('Authorization')) return true;
    const p = url.pathname;
    if (p === '/login/' || p === '/logout/') return true;
    if (p.startsWith('/admin/') || p === '/admin') return true;
    if (p.startsWith('/steps/auto-save/')) return true;
    if (p.startsWith('/journal/gratitude/')) return true;
    if (p.startsWith('/amends/')) return true;
    return false;
}

self.addEventListener('fetch', (event) => {
    const req = event.request;
    const url = new URL(req.url);

    if (url.origin !== self.location.origin) return;
    if (isBypass(req, url)) {
        event.respondWith(fetch(req));
        return;
    }

    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(req).then((hit) => hit || fetch(req))
        );
        return;
    }

    event.respondWith(fetch(req));
});
