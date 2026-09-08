# Port soft-stack densify + industry city-centroid offs (2026-09-08)

## Problem
Four expansion / project harbour rows still shared a **3-dp WGS84 stack** with their parent operational ports, so map UX looked like duplicate pins:

| Child (project) | Parent | Shared ~3dp pin |
|---|---|---|
| `ARC-PORT-096` Honningsvåg new fixed quay | `ARC-PORT-040` | `25.970 / 70.982` |
| `ARC-PORT-097` Kirkenes tugboat services | `ARC-PORT-015` | `30.046 / 69.727` |
| `ARC-PORT-100` Utqiaġvik coastal revetment | `ARC-PORT-056` | `-156.789 / 71.291` |
| `ARC-PORT-146` Kemi Ajos deepening / quay | `ARC-PORT-027` | `24.564 / 65.736` |

Separately, three industry facilities still sat on **city centroids** despite harbour / industrial site names:

| id | was (city centroid) |
|---|---|
| `ARC-FAC-320` Luleå Industripark | Luleå `22.1567 / 65.5848` |
| `ARC-FAC-333` Bodø PostNord logistics | Bodø `14.4049 / 67.2804` |
| `ARC-FAC-340` Eimskip Greenland / ex-RAL agency | Nuuk `−51.6941 / 64.1814` |

## Fixes (dataset)
Densified onto verifiable OSM / Photon anchors (User-Agent `ArcticTradeLanes-GIS-QA/1.0`), then rebuilt Zo atlas (static aliases only — no App.tsx / SPA redeploy).

| ID | New lat, lon | Source note |
|----|-------------|-------------|
| `ARC-PORT-096` | 70.9809100, 25.9689880 | OSM Nominatim `Honningsvåg kystrutekai` (Holmen/Holmbukt ferry quay) |
| `ARC-PORT-097` | 69.7267740, 30.0348534 | OSM `Sydvaranger kai` / Shipyard Kimek (Sydvaranger Drift tug ops) |
| `ARC-PORT-100` | 71.290224, −156.794962 | OSM Photon Stevenson Street coastal tertiary (USACE Barrow Coastal Storm Damage Reduction / Stevenson Street raise) |
| `ARC-PORT-146` | 65.663578, 24.530333 | OSM Photon `landuse=industrial` Kemin satama (Ajos deep-water peninsula) |
| `ARC-FAC-320` | 65.562638, 22.200160 | OSM Photon LKAB Svartön / Svartövägen (Luleå Industripark band) |
| `ARC-FAC-333` | 67.288803, 14.396978 | OSM Photon Bodø havn døgnhvileplass (harbour logistics zone) |
| `ARC-FAC-340` | 64.171378, −51.720590 | OSM Photon Royal Arctic Line Hovedkontor (Nuuk harbour freight HQ / Eimskip agency band) |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/data/atlas.manifest.json`
- features **1324**, ports **156**, industry **110**, `generated` `2026-09-08T10:41:07Z`, `crs_primary` 3996
- remaining **port 3-dp stacks: 0**
- CI: `node scripts/check-port-soft-stack-densify.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, commercial rails untouched.
