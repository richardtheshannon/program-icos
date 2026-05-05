/*
 * frame.js — Phases C + D
 *
 * Wires the v2 Frame Studio chrome:
 *   - BR-corner menu button → accordion nav drawer (#nav-drawer)
 *   - TR-corner app drawer button → tile drawer (#app-drawer)
 *   - Shared scrim (#drawer-scrim) — clicking it closes whichever drawer is open
 *   - Escape closes whichever drawer is open OR the stub modal (Phase D)
 *   - Only one drawer open at a time (mutual exclusion)
 *   - Accordion: click an .acc-trigger button → expand its panel, collapse siblings
 *   - On open, the section matching the current surface auto-expands (CSS .open
 *     class is set server-side; this script just animates max-height to fit)
 *
 * Phase D additions:
 *   - Delegated click handler on .app for rail icons keyed by data-action="…"
 *   - Theme toggle (light ↔ dark) via window.Ritual.setTheme (preferences.js)
 *   - Density toggle (comfortable ↔ compact) via window.Ritual.setDensity
 *   - Quick-complete: proxies a click to the visible Now-event toggle button
 *     (.slot[data-state="now"] .slot-check or .crow .crow-check) when one
 *     exists; no-op tooltip otherwise.
 *   - View-mode: aria-pressed toggle (no behavior — Phase D stub)
 *   - Today / Settings: real navigations (`/`, `/settings` — Settings 404s
 *     until a future phase wires the route)
 *   - Search / Activity / Quick-note / Help: open the shared #stub-modal
 *     ("Coming soon" with the icon's name as the title)
 *   - Sign out: handled by a real <form method="post" action="/logout"> with
 *     CSRF inside frame_rails.twig — works without JS.
 *
 * Phase F additions:
 *   - Deconstruct: intercept clicks on a.nav-top-level (Dashboard leaf in the
 *     accordion drawer) and run the exit animation before navigating. Cmd /
 *     Ctrl / Shift / Alt-click bypass (let the browser open in a new tab).
 *     Reduced-motion + same-URL clicks bypass entirely.
 *   - Reconstruct: the inline <head> script in base.twig sets
 *     html.mode-entering BEFORE first paint when sessionStorage flagged a
 *     pending transition; this script removes the class after the entering
 *     keyframes finish (~1100ms).
 *   - htmx swaps + accordion expansion + drawer toggles do NOT trigger the
 *     transition (the click handler matches only a.nav-top-level with href).
 *
 * No dependencies. Loaded with `defer` so DOM is parsed before this runs.
 */

(function () {
    'use strict';

    const navDrawer  = document.getElementById('nav-drawer');
    const appDrawer  = document.getElementById('app-drawer');
    const scrim      = document.getElementById('drawer-scrim');
    const menuBtn    = document.getElementById('menu-btn');
    const appBtn     = document.getElementById('app-drawer-btn');
    const navClose   = document.getElementById('nav-drawer-close');
    const appClose   = document.getElementById('app-drawer-close');
    const navBody    = document.getElementById('nav-drawer-body');

    // scrim is required for either drawer's open/close animation + click-to-close.
    // nav-drawer (BR menu) and app-drawer (TR tile) are each independently optional —
    // pre-auth the login layout includes only the app-drawer, so frame.js binds
    // whichever drawer's required elements exist.
    if (!scrim) return;

    /* ---------- Drawer open / close ---------- */

    function openNav() {
        if (appDrawer?.classList.contains('open')) closeApp();
        navDrawer.classList.add('open');
        scrim.classList.add('open');
        navDrawer.setAttribute('aria-hidden', 'false');
        menuBtn.setAttribute('aria-expanded', 'true');
        // Recompute panel max-heights now that the drawer is laid out.
        navBody?.querySelectorAll('.acc-item.open').forEach(syncPanelHeight);
    }
    function closeNav() {
        navDrawer.classList.remove('open');
        if (!appDrawer?.classList.contains('open')) scrim.classList.remove('open');
        navDrawer.setAttribute('aria-hidden', 'true');
        menuBtn.setAttribute('aria-expanded', 'false');
    }
    function openApp() {
        if (navDrawer?.classList.contains('open')) closeNav();
        appDrawer.classList.add('open');
        scrim.classList.add('open');
        appDrawer.setAttribute('aria-hidden', 'false');
        appBtn.setAttribute('aria-expanded', 'true');
    }
    function closeApp() {
        appDrawer.classList.remove('open');
        if (!navDrawer?.classList.contains('open')) scrim.classList.remove('open');
        appDrawer.setAttribute('aria-hidden', 'true');
        appBtn.setAttribute('aria-expanded', 'false');
    }
    function closeAny() {
        if (navDrawer?.classList.contains('open')) closeNav();
        if (appDrawer?.classList.contains('open')) closeApp();
    }

    if (navDrawer && menuBtn) {
        menuBtn.addEventListener('click', () => {
            navDrawer.classList.contains('open') ? closeNav() : openNav();
        });
        navClose?.addEventListener('click', closeNav);
    }
    if (appDrawer && appBtn) {
        appBtn.addEventListener('click', () => {
            appDrawer.classList.contains('open') ? closeApp() : openApp();
        });
        appClose?.addEventListener('click', closeApp);
    }
    scrim.addEventListener('click', closeAny);
    document.addEventListener('keydown', (e) => {
        if (e.key !== 'Escape') return;
        // <dialog>'s native Escape handling already closes #stub-modal /
        // #quick-note-modal; only close drawers here so we don't fight the
        // dialog's own behavior.
        const stub = document.getElementById('stub-modal');
        if (stub && stub.open) return;
        const qn = document.getElementById('quick-note-modal');
        if (qn && qn.open) return;
        closeAny();
    });

    /* ---------- Accordion ---------- */

    function syncPanelHeight(item) {
        const panel = item.querySelector(':scope > .acc-panel');
        if (!panel) return;
        panel.style.maxHeight = panel.scrollHeight + 'px';
    }

    function collapse(item) {
        item.classList.remove('open');
        const panel   = item.querySelector(':scope > .acc-panel');
        const trigger = item.querySelector(':scope > .acc-trigger');
        if (panel)   panel.style.maxHeight = '0px';
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }

    function expand(item) {
        item.classList.add('open');
        const trigger = item.querySelector(':scope > .acc-trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
        syncPanelHeight(item);
    }

    if (navBody) {
        navBody.addEventListener('click', (e) => {
            const trigger = e.target.closest('.acc-trigger');
            if (!trigger) return;
            const item = trigger.closest('.acc-item');
            if (!item || item.classList.contains('acc-leaf')) return;
            // Trigger is a <button> for non-leaf sections; prevent default form/etc.
            e.preventDefault();
            const isOpen = item.classList.contains('open');
            navBody.querySelectorAll('.acc-item.open').forEach(collapse);
            if (!isOpen) expand(item);
        });

        // Server-side rendered .open items: animate to their measured height
        // on the next frame (after layout is settled).
        requestAnimationFrame(() => {
            navBody.querySelectorAll('.acc-item.open').forEach(syncPanelHeight);
        });

        // Recompute on viewport resize so collapsed-content reflows don't
        // leave a clipped panel.
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                navBody.querySelectorAll('.acc-item.open').forEach(syncPanelHeight);
            }, 120);
        });
    }

    /* ==========================================================================
       Phase D — Rail icon handlers
       ========================================================================== */

    const STUB_TITLES = {
        'search': 'Search',
        'help'  : 'Help',
    };

    const stubModal = document.getElementById('stub-modal');
    const quickNoteModal = document.getElementById('quick-note-modal');

    function openStub(action) {
        if (!stubModal) return;
        const titleEl = stubModal.querySelector('.stub-title');
        if (titleEl) titleEl.textContent = STUB_TITLES[action] || 'Coming soon';
        if (typeof stubModal.showModal === 'function') {
            stubModal.showModal();
        } else {
            stubModal.setAttribute('open', '');
        }
    }
    function closeStub() {
        if (!stubModal) return;
        if (typeof stubModal.close === 'function') stubModal.close();
        else stubModal.removeAttribute('open');
    }
    if (stubModal) {
        stubModal.addEventListener('click', (e) => {
            // Click on the .stub-close button OR the dialog's backdrop area
            // (clicks on the <dialog> element itself but not on its inner card).
            if (e.target.matches('.stub-close')) {
                closeStub();
                return;
            }
            const inner = stubModal.querySelector('.stub-modal-inner');
            if (inner && !inner.contains(e.target)) closeStub();
        });
    }

    function openQuickNote() {
        if (!quickNoteModal) return;
        if (typeof quickNoteModal.showModal === 'function') {
            quickNoteModal.showModal();
        } else {
            quickNoteModal.setAttribute('open', '');
        }
        // Defer focus so the dialog has laid out before we move the caret.
        requestAnimationFrame(() => {
            quickNoteModal.querySelector('.quick-note-input')?.focus();
        });
    }
    function closeQuickNote() {
        if (!quickNoteModal) return;
        if (typeof quickNoteModal.close === 'function') quickNoteModal.close();
        else quickNoteModal.removeAttribute('open');
        const ta = quickNoteModal.querySelector('.quick-note-input');
        if (ta) ta.value = '';
    }
    if (quickNoteModal) {
        quickNoteModal.addEventListener('click', (e) => {
            // Cancel button OR backdrop click closes; clicks inside the inner
            // card (form, textarea, Save) fall through to native handling.
            if (e.target.closest('[data-close-modal="quick-note-modal"]')) {
                e.preventDefault();
                closeQuickNote();
                return;
            }
            const inner = quickNoteModal.querySelector('.stub-modal-inner');
            if (inner && !inner.contains(e.target)) closeQuickNote();
        });
        // Server signals modal-close after a successful save via HX-Trigger.
        document.body.addEventListener('close-quick-note-modal', closeQuickNote);
    }

    function setMode(mode, btn) {
        const r = document.documentElement;
        if (window.Ritual && typeof window.Ritual.setAppMode === 'function') {
            window.Ritual.setAppMode(mode);
        } else {
            r.setAttribute('data-app-mode', mode);
        }
        // Sync aria-pressed across the 3 mode buttons (radio-group semantics)
        document.querySelectorAll('.region .ib[data-action="set-mode"]').forEach((el) => {
            el.setAttribute('aria-pressed', el === btn ? 'true' : 'false');
        });
    }

    function toggleDensity() {
        const r = document.documentElement;
        const next = r.getAttribute('data-density') === 'compact' ? 'comfortable' : 'compact';
        if (window.Ritual && typeof window.Ritual.setDensity === 'function') {
            window.Ritual.setDensity(next);
        } else {
            r.setAttribute('data-density', next);
        }
    }

    function quickComplete() {
        // Now-event toggle in the slot view, daily-row view, or weekly-cell view.
        // First match wins (each surface only renders one of these for the Now slot).
        const target =
              document.querySelector('.slot[data-state="now"]:not(.done) .slot-check')
           || document.querySelector('.crow:not(.done) .crow-check')
           || document.querySelector('.week-cell.is-today:not(.done) .crow-check');
        if (target) target.click();
        // No fallback action — the .tip tooltip + aria-label communicate that
        // there's nothing to complete right now.
    }

    function toggleViewMode(btn) {
        const r = document.documentElement;
        const next = r.getAttribute('data-view-mode') === 'dim' ? 'bright' : 'dim';
        if (window.Ritual && typeof window.Ritual.setViewMode === 'function') {
            window.Ritual.setViewMode(next);
        } else {
            r.setAttribute('data-view-mode', next);
        }
        btn.setAttribute('aria-pressed', next === 'dim' ? 'true' : 'false');
    }

    // Sync the eye-icon's aria-pressed with the persisted view-mode state on
    // page load. Twig markup hard-codes aria-pressed="false"; without this,
    // a user with viewMode=dim from a prior session would see the dim
    // applied but the icon rendering as "off".
    const viewBtn = document.querySelector('.region .ib[data-action="view-mode"]');
    if (viewBtn && document.documentElement.getAttribute('data-view-mode') === 'dim') {
        viewBtn.setAttribute('aria-pressed', 'true');
    }

    // Sync the 3 mode buttons' aria-pressed with the persisted app-mode on
    // page load. Twig markup hard-codes aria-pressed="false" on all three.
    const currentMode = document.documentElement.getAttribute('data-app-mode') || 'photo';
    document.querySelectorAll('.region .ib[data-action="set-mode"]').forEach((el) => {
        el.setAttribute('aria-pressed', el.dataset.mode === currentMode ? 'true' : 'false');
    });

    const appEl = document.querySelector('.app');
    if (appEl) {
        appEl.addEventListener('click', (e) => {
            const btn = e.target.closest('.region .ib[data-action]');
            if (!btn) return;
            const action = btn.dataset.action;

            switch (action) {
                case 'search':
                case 'help':
                    e.preventDefault();
                    openStub(action);
                    break;
                case 'quick-note':
                    e.preventDefault();
                    openQuickNote();
                    break;
                case 'today':
                    window.location.href = '/';
                    break;
                case 'activity':
                    window.location.href = '/focus';
                    break;
                case 'settings':
                    window.location.href = '/settings';
                    break;
                case 'set-mode':
                    setMode(btn.dataset.mode, btn);
                    break;
                case 'density':
                    toggleDensity();
                    break;
                case 'view-mode':
                    toggleViewMode(btn);
                    break;
                case 'quick-complete':
                    quickComplete();
                    break;
                case 'logout':
                    // The Sign-out icon is a <button type="submit"> inside the
                    // .rail-logout form — the browser handles POST /logout.
                    // No preventDefault here.
                    break;
                default:
                    break;
            }
        });
    }

    /* ==========================================================================
       Phase F — Page transitions (deconstruct / reconstruct)
       ========================================================================== */

    const REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const docEl = document.documentElement;

    // Reconstruct: the inline <head> script set html.mode-entering before paint
    // when sessionStorage flagged a pending transition. Strip the class after
    // the entering keyframes complete (~1100ms = max delay 340ms + max anim 0.75s).
    if (docEl.classList.contains('mode-entering')) {
        setTimeout(() => docEl.classList.remove('mode-entering'), 1100);
    }

    // Deconstruct: intercept top-level accordion <a class="nav-top-level"> clicks.
    // Currently only Dashboard's leaf matches (Focus / Analytics / Admin top-level
    // triggers are <button>s that expand the accordion). Modifier keys bypass so
    // the browser can open in new tab/window. Reduced-motion + same-URL bypass.
    document.addEventListener('click', (e) => {
        if (REDUCED_MOTION) return;
        if (docEl.classList.contains('mode-exiting')) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        if (typeof e.button === 'number' && e.button !== 0) return;
        const a = e.target.closest('a.nav-top-level');
        if (!a || !a.href) return;
        if (a.target && a.target !== '_self') return;
        if (a.hasAttribute('download')) return;
        if (a.href === window.location.href) return;
        e.preventDefault();
        try { sessionStorage.setItem('ritual:transitioning', '1'); } catch (err) {}
        docEl.classList.add('mode-exiting');
        setTimeout(() => { window.location.href = a.href; }, 600);
    });
})();
