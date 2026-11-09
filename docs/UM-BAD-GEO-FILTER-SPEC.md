# UM-style client-side bad-geo filter: spec and audit (2026-11-09)

This is a read-only audit of the coordinates the UnicornsMap.com map serves. It covers the main bundle `assets/index-CuvrFAFf.js` and `/data/profiles-rail.json`, both fetched 2026-11-09 12:48 MSK. No UM data or code was changed. The fix needs a bundle rebuild, and the UM rails rules allow no SPA redeploy and no App.tsx change, so it is documented here and not shipped.

## Findings

Records: 983 coordinate-bearing records, 897 from the bundle and 86 from rail. 409 distinct coordinates.

| Check | Count | Examples |
|---|---|---|
| Null island (0,0) | 0 | none |
| Null or non-numeric lat/lng | 50 | profiles-rail.json: nadia-attia, nkosenye-zulu, mark-nuttall, conor-finnegan, kendrick-white. These are not plotted, so they are only a data gap. |
| Out of range or lat/lng swapped | 22 | The EMERGENCE 2026 Sydney speaker personas in the main bundle. 15 have `lat:151.2093,lng:-33.8688` (location "Sydney, Australia"), 6 have `lat:144.9631,lng:-37.8136` (Melbourne) and 1 has `lat:138.6007,lng:-34.9285` (Adelaide). The location strings show these are swapped. In MapLibre, latitude 151° goes through sin() and renders at about 29°N, -34°E (Atlantic, near the Canaries). Any `fitBounds` that includes them can throw "Invalid LngLat". The lazy chunk `Emergence2026SydneyPage` has correct coordinates (20 records, 0 bad). |
| Coarse placeholder | 1 | "Arctic Trade" persona `lat:69,lng:40`, location "Murmansk / Arctic, Russia". It uses integer degrees and does not sit on Murmansk (68.97, 33.08). |
| Country-centroid placeholders | 0 | The only hit was Madrid at 40.4168,-3.7038, which is a city, not Spain's centroid. |
| Exact-duplicate stacks (city-level) | 93 coordinates hold 617 records | Agentic AI Summit Berkeley has 50 at 37.8716,-122.2727. New York City has 48 at 40.7128,-74.006. San Francisco has 41 at 37.7749,-122.4194. Moscow has 33 at 55.7558,37.6173. M&A for Startups Tokyo has 26. Dubai has 24 and Abu Dhabi 20. These are deliberate city or venue pins, so they need clustering or spiderfy, not deletion. |

Lazy chunks (25 with coordinates, including emergency-markets v22–v75, abramovich-network, kommersant-regatta, ukrainian-uhnw and EnterpriseGISMap) had 0 out-of-range and 0 null-island coordinates.

## Proposed filter, for the next allowed UM build only

This is an additive, pure function applied where features are built (before `[lng,lat]` is formed):

```js
// returns {lat,lng} or null; never invents a location
export function sanitizeLatLng(p) {
  const lat = Number(p.lat), lng = Number(p.lng);
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) return null;   // null/NaN -> unplotted
  if (Math.abs(lat) < 1e-6 && Math.abs(lng) < 1e-6) return null;      // null island
  if (Math.abs(lat) <= 90 && Math.abs(lng) <= 180) return { lat, lng };
  // unambiguous swap: lat out of range but valid as lng, and lng valid as lat
  if (Math.abs(lat) <= 180 && Math.abs(lng) <= 90) return { lat: lng, lng: lat, swapped: true };
  return null;
}
```

Rules:

- Log swaps with `console.warn` so the source data gets fixed. Do not change stats counters silently.
- Report geoPinned and peopleOnMap before and after any build that includes the filter. Today's values are 569 and 464.
- The source-data fix is better than the filter: swap the 22 EMERGENCE persona literals.

Audit script: `scripts/um_bad_geo_audit.py`. It is read-only and reproduces the counts above.
