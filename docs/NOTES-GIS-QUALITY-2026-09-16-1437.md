# GIS Quality Loop — 2026-09-16 ~14:37 MSK

## Win
- Densified **ARC-SHIP-020** Halifax Shipyard off soft city pin `44.6500,-63.5700` onto OSM way/358578623 (`building=industrial`, name Halifax Shipyard, 3099 Barrington St) Nominatim centroid `44.6672758,-63.5966057`; Wikidata Q1442711.
- Rebuilt + synced live static atlas so prior **ARC-SHIP-032** Orskov densify (`57.4368155,10.5474498`) and **ARC-SHIP-024** Ulstein id fix (was ARC-SSHIP-024) actually reach apex/www (live had been stuck on generated 2026-09-16T10:36:46Z).

## Skipped / quarantine unchanged
- ARC-PORT-034/069 + ARC-SHIP-069 centroid_clone stamped (3)
- Ulstein Verft soft pin densify still deferred (Issue #37)
- Arctech / Zvezda / Wrangell untouched

## Atlas
- rebuild via `atlas-proj/build_atlas.py`; sync static Dataset + www/public/data only (no App.tsx / no SPA redeploy)
- features 1321 / shipyards 70 / ports 156 / crs_primary EPSG:3996 / generated 2026-09-16T11:46:11Z

## Checks
- check-ship020-halifax-densify.mjs OK
- UM pin filter smoke: accepted 4 / dropped 6
