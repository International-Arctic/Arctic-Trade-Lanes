# Port + industry pin densify (2026-09-07)

## Problem
1. **Lumina White Mountain Mine Port** (`ARC-PORT-083`, Qaqortorsuaq) shared Kangerlussuaq’s WGS84 pin and wrongly carried UNECE **`GLKAN`** (Kangerlussuaq Havn). Map users saw Greenland’s only full-time mine port stacked on the inland airport town.
2. **Whittier** Delong Dock (`ARC-PORT-068`) and ARRC tunnel upgrade (`ARC-PORT-082`) shared one waterfront centroid.
3. **Norterminal Gamneset** (`ARC-FAC-372`) and **KILA** (`ARC-FAC-314`) sat on the Kirkenes town centroid with four other Sør-Varanger rows.

## Fixes (dataset)
| ID | Change | Sources |
|----|--------|---------|
| `ARC-PORT-083` | → `66.5369, -52.3091`; clear LOCODE | OSM `Qaqortorsuaq` peak; lumina.gl; GlobeNewswire “50 miles west of Kangerlussuaq” |
| `ARC-PORT-151` | LOCODE `GLSFJ` → **`GLKAN`** | UNECE `datasets/un-locode` (KAN = Kangerlussuaq Havn; SFJ = airport-only) |
| `ARC-PORT-068` | → `60.7785, -148.6680` | alaskarails Whittier waterfront order (Delong Dock east) |
| `ARC-PORT-082` | → `60.7768, -148.7210` | Whittier tunnel approach / portal (distinct from dock) |
| `ARC-FAC-372` | → `69.7607, 29.9581` | Photon/OSM Gamnes (Korsfjord); norterminal.no/terminal/location |
| `ARC-FAC-314` | → `69.7220, 30.0550` | KILA industrial area south of centrum |
| shipyards | drop blank CSV row | hygiene |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/data/atlas.manifest.json` — ports **148→149**, features **1314→1315**, `generated` `2026-09-07T15:21:27Z`, `crs_primary` 3996
- CI: `node scripts/check-port-industry-densify.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, no SPA redeploy.
