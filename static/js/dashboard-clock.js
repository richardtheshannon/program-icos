/*
 * dashboard-clock.js — Phase D
 *
 * Drives the top-rail clock label (#rail-clock-time + #rail-clock-date inside
 * frame_rails.twig). Phase A retained the v1 file name for service-worker
 * cache stability — the contents are repurposed to target the rail slot
 * instead of v1's .dash-date .num element.
 *
 * Format matches Frame Studio:
 *   time : 24-hour HH:MM (zero-padded)
 *   date : DAY · MON D    (uppercase 3-letter day + 3-letter month)
 *
 * Tick cadence is 30s — minute-resolution display, half-minute polling so the
 * displayed minute settles within ~30s of the wall clock rolling over.
 *
 * Loaded globally from base.twig so the clock is present on every authed
 * surface (the rail is part of the frame, not a per-page widget).
 */
(function () {
    const timeEl = document.getElementById('rail-clock-time');
    const dateEl = document.getElementById('rail-clock-date');
    if (!timeEl || !dateEl) return;

    const DAYS   = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    const MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

    function pad(n) { return n < 10 ? '0' + n : '' + n; }

    function tick() {
        const d = new Date();
        timeEl.textContent = pad(d.getHours()) + ':' + pad(d.getMinutes());
        dateEl.textContent = DAYS[d.getDay()] + ' · ' + MONTHS[d.getMonth()] + ' ' + d.getDate();
    }

    tick();
    setInterval(tick, 30000);
})();
