(function () {
  var KEY = "ritual_state";
  var root = document.documentElement;

  function readState() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return {};
      var obj = JSON.parse(raw);
      return (obj && typeof obj === "object") ? obj : {};
    } catch (e) { return {}; }
  }

  function writeState(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
  }

  function apply() {
    var s = readState();
    var dirty = false;
    // Legacy keys: drop on first load (old accent picker, old theme toggle).
    if (Object.prototype.hasOwnProperty.call(s, "accent")) { delete s.accent; dirty = true; }
    if (Object.prototype.hasOwnProperty.call(s, "theme"))  { delete s.theme;  dirty = true; }
    if (dirty) writeState(s);

    root.setAttribute("data-app-mode", s.appMode || "photo");
    root.setAttribute("data-density", s.density || "comfortable");
    root.setAttribute("data-view-mode", s.viewMode || "bright");
  }

  apply();

  window.Ritual = {
    setAppMode: function (m) { var s = readState(); s.appMode = m; writeState(s); apply(); },
    setDensity: function (d) { var s = readState(); s.density = d; writeState(s); apply(); },
    setViewMode: function (v) { var s = readState(); s.viewMode = v; writeState(s); apply(); }
  };
})();
