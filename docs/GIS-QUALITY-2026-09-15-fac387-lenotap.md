# GIS Quality — FAC-387 Lenotap densify (2026-09-15 ~10:45 MSK)

## Problem
`ARC-FAC-387` Nordgold Lenotap ore-field GOK (Chukotka) shared an exact WGS84 pin with `ARC-PORT-042` Egvekinot Port (`-179.1167, 66.3167`). A mining GOK ~180 km inland must not stack on the Bering Sea harbour pin.

## Fix
Densified onto verifiable OSM waterway **Ленотап** ([way/649821635](https://www.openstreetmap.org/way/649821635)) via Nominatim (`ArcticTradeLanes-GIS/1.0`). Cross-check: Iultin locality ([way/649821750](https://www.openstreetmap.org/way/649821750)) ~11 km — historic mining settlement in the same district.

| id | was | now |
|----|-----|-----|
| ARC-FAC-387 | Egvekinot harbour `-179.1167, 66.3167` | Lenotap `-178.9312504, 67.9381457` |

Dataset: `arctic_industrial_facilities.csv`. Builder: Zo `atlas-proj/build_atlas.py`. Static atlas aliases only — no App.tsx / SPA redeploy.

Live atlas `generated` `2026-09-15T07:49:49Z`, 1321 features / 156 ports.

## CI
```bash
node scripts/check-fac387-lenotap-densify.mjs [atlas.4326.geojson]
```

## Not densified this cycle
Remaining `centroid_clone` PORT-034 / PORT-069 / PORT-153 / SHIP-069 — still no verifiable harbour/pier/yard OSM (quarantine unchanged).
