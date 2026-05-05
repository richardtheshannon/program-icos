/* pull-to-refresh.js — touch-only PTR for the .workspace scroll container.
 *
 * Trigger: drag down past 70px when scrollTop === 0 → location.reload().
 * Below threshold = snap back. Cancelled if a drawer or dialog is open.
 * Reload semantics rely on the SW's network-first nav strategy
 * (service-worker.js — non-asset GETs go straight to network), so a reload
 * actually re-renders server-derived state (now_event, day rollover, etc.).
 */
(function () {
    if (!('ontouchstart' in window)) return;

    var THRESHOLD = 70;
    var MAX_PULL  = 140;
    var ACTIVATE_DELAY = 180;

    function init() {
        var ws = document.querySelector('.workspace');
        if (!ws) return;

        var indicator = document.createElement('div');
        indicator.className = 'ptr-indicator';
        indicator.setAttribute('aria-hidden', 'true');
        indicator.innerHTML = '<span class="ptr-spinner"></span>';
        ws.prepend(indicator);

        var startY = 0;
        var pullDistance = 0;
        var tracking = false;
        var refreshing = false;

        function isBlocked() {
            if (refreshing) return true;
            if (document.querySelector('#nav-drawer[aria-hidden="false"]')) return true;
            if (document.querySelector('#app-drawer[aria-hidden="false"]')) return true;
            if (document.querySelector('dialog[open]')) return true;
            return false;
        }

        function setProgress(d) {
            var p = Math.min(d / THRESHOLD, 1);
            indicator.style.setProperty('--ptr-progress', p.toFixed(3));
            indicator.style.transform = 'translate3d(-50%,' + (d * 0.5) + 'px,0)';
            indicator.classList.add('is-pulling');
            indicator.classList.toggle('is-armed', d >= THRESHOLD);
        }

        function reset() {
            // Drop is-pulling so the CSS transition animates the snap-back.
            indicator.classList.remove('is-pulling');
            indicator.classList.remove('is-armed');
            indicator.style.transform = '';
            indicator.style.setProperty('--ptr-progress', '0');
        }

        ws.addEventListener('touchstart', function (e) {
            if (isBlocked()) return;
            if (ws.scrollTop > 0) return;
            if (!e.touches || e.touches.length !== 1) return;
            startY = e.touches[0].clientY;
            pullDistance = 0;
            tracking = true;
        }, { passive: true });

        ws.addEventListener('touchmove', function (e) {
            if (!tracking) return;
            if (ws.scrollTop > 0) { tracking = false; reset(); return; }
            var dy = e.touches[0].clientY - startY;
            if (dy <= 0) { pullDistance = 0; reset(); return; }
            pullDistance = Math.min(dy, MAX_PULL);
            if (e.cancelable) e.preventDefault();
            setProgress(pullDistance);
        }, { passive: false });

        ws.addEventListener('touchend', function () {
            if (!tracking) return;
            tracking = false;
            if (pullDistance >= THRESHOLD) {
                refreshing = true;
                indicator.classList.add('is-refreshing');
                setTimeout(function () { location.reload(); }, ACTIVATE_DELAY);
            } else {
                reset();
            }
        }, { passive: true });

        ws.addEventListener('touchcancel', function () {
            tracking = false;
            reset();
        }, { passive: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
