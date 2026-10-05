/* ArcticTradeLanes.com — ad slot -> Yandex RTB block mapping (owner-approved 2026-10-05).
 * A slot renders a Yandex RTB block ONLY if it has an id here. Unmapped slots keep their reserved
 * space with a small "Advertisement" label (inline slots) or stay collapsed (sidebar / mobile sticky).
 * Keys: exact slot id; "<id>:mobile" = variant used under 1024px; a family key ("atl-ad-inc" or
 * "atl-ad-home-inc") is used for numbered slots that have no exact id (pageNumber = n).
 * Edit public/ads-config.js (and dist/ads-config.js for an instant live change), no rebuild needed. */
window.ATL_AD_SLOTS = window.ATL_AD_SLOTS || {
  // Content pages
  // "atl-ad-top":        "R-A-XXXXXXX-1",  // desktop top banner 728x90
  // "atl-ad-top:mobile": "R-A-XXXXXXX-2",  // mobile top banner 320x100
  // "atl-ad-inc-1":      "R-A-XXXXXXX-3",  // in-content 300x250 / responsive
  // "atl-ad-inc-2":      "R-A-XXXXXXX-4",
  // "atl-ad-inc-3":      "R-A-XXXXXXX-5",
  // "atl-ad-side":       "R-A-XXXXXXX-6",  // desktop sticky sidebar 300x600
  // "atl-ad-mstick":     "R-A-XXXXXXX-7",  // mobile sticky bottom 320x50
  // Home map page (outside the map canvas — do not overlay zoom / map controls)
  // "atl-ad-home-top":        "R-A-XXXXXXX-8",  // under H1 / above map, 728x90
  // "atl-ad-home-top:mobile": "R-A-XXXXXXX-9",  // 320x100
  // "atl-ad-home-inc-1":      "R-A-XXXXXXX-10", // below-map strip, banner/adaptive
  // "atl-ad-home-inc-2":      "R-A-XXXXXXX-11",
  // "atl-ad-home-providers":  "R-A-XXXXXXX-12", // slim partner / sold logo strip
};
/* inline: keep reserved space for unmapped top/in-content/home slots; rails: show empty sidebar/sticky bar. */
window.ATL_AD_RESERVE = window.ATL_AD_RESERVE || { inline: true, rails: false };
