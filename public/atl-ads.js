/* ATL ad-slot loader (2026-10-05): renders a Yandex RTB block into [data-yandex-rtb-slot] containers
 * only when window.ATL_AD_SLOTS (/ads-config.js) maps the slot id. Never touches Autoplacement. */
(function () {
  var w = window, d = document;
  w.yaContextCb = w.yaContextCb || [];
  var MOBILE = "(max-width: 1023px)", RA = /^R-A-\d+-\d+$/;
  function isMobile() { return !!(w.matchMedia && w.matchMedia(MOBILE).matches); }
  function blockFor(id) {
    var m = w.ATL_AD_SLOTS || {}, mob = isMobile(), fam = id.replace(/-\d+$/, "");
    var b = (mob && m[id + ":mobile"]) || m[id];
    if (b) return { blockId: b };
    if (fam !== id) {
      b = (mob && m[fam + ":mobile"]) || m[fam];
      if (b) return { blockId: b, pageNumber: parseInt(id.slice(fam.length + 1), 10) || 1 };
    }
    return null;
  }
  function render(id) {
    var el = d.getElementById(id), box = d.getElementById("yandex_rtb_" + id);
    if (!el || !box || el.getAttribute("data-atl-rendered")) return;
    var b = blockFor(id);
    if (!b || !RA.test(b.blockId)) return;
    if (w.getComputedStyle && w.getComputedStyle(el).display === "none") return;
    el.setAttribute("data-atl-rendered", b.blockId);
    var o = { blockId: b.blockId, renderTo: box.id };
    if (b.pageNumber) o.pageNumber = b.pageNumber;
    w.yaContextCb.push(function () { try { w.Ya.Context.AdvManager.render(o); } catch (e) { /* ad blocked */ } });
  }
  function scan() {
    var n = d.querySelectorAll("[data-yandex-rtb-slot]");
    for (var i = 0; i < n.length; i++) render(n[i].id);
  }
  w.atlAds = { render: render, scan: scan, blockFor: blockFor };
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", scan); else scan();
})();
