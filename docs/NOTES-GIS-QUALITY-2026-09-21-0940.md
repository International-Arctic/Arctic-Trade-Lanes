# GIS Quality Loop — 2026-09-21 ~09:40 MSK

## Win
- Densified **ARC-SHIP-043** Fosen Yard off soft pin `64.2500,10.4500` onto Wikidata [Q1439358](https://www.wikidata.org/wiki/Q1439358) P159/P625 `63.5649722,9.8986944` (Kvithyllveien 171, 7100 Rissa, Indre Fosen / Trøndelag).
- P452 industry present; official https://fosenyard.com/. Nominatim address node/3552488486 `63.5654829,9.9006010` cross-check. No named OSM `industrial=shipyard` polygon found — WD HQ coordinate densify (≈80+ km south/west of erroneous soft pin).
- Softish shipyard heuristic count ~28→27 after this densify (CSV total 73 rows).

## Skipped / quarantine unchanged
- ARC-PORT-034 / ARC-PORT-069 / ARC-SHIP-069
- Ulstein Verft ARC-SHIP-024 still deferred (Issue #37)
- Zvezda / Wrangell / Fayard / Larsnes / Kleven / Arctech soft pins left for later
- Damen Galati GFI #39 still open (OSM way/888306100 ready)

## Checks
- `check-ship043-fosen-densify.mjs` locks lat/lon + Q1439358 + `gis-densify-0940` source stamp

## Atlas / UM
- Rebuild+sync expected via Zo `atlas-proj/build_atlas.py` → static Dataset + www/public/data + Zo space assets (no App.tsx / no SPA redeploy)
- UM pin-filter smoke to follow same cycle
