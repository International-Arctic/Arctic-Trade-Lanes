# GIS Quality Loop — 2026-09-21 ~09:15 MSK

## Win
- Densified **ARC-SHIP-044** Havyard Group / Havyard Ship Technology off soft pin `61.1800,6.0800` onto Wikidata [Q55947781](https://www.wikidata.org/wiki/Q55947781) P625 `61.1245683,5.3234446` (Leirvik/Hyllestad, Vestland). P452 shipbuilding; official https://www.havyard.com/. No OSM P402/industrial polygon — WD coordinate densify (≈40 km east erroneous soft lon).

## Skipped / quarantine unchanged
- ARC-PORT-034 / ARC-PORT-069 / ARC-SHIP-069 centroid_clone stamped (3)
- Ulstein Verft ARC-SHIP-024 still deferred (Issue #37 — WD P625 exists but no OSM industrial polygon)
- Zvezda / Wrangell / Fayard / Fosen / Larsnes / Kleven / Arctech / Damen Galati soft pins left for later (Damen has OSM way/888306100 ready)

## Atlas
- rebuild via `atlas-proj/build_atlas.py`; sync static Dataset + www/public/data + Zo space assets (no App.tsx / no SPA redeploy)
- features 1321 / shipyards 70 / ports 156 / crs_primary EPSG:3996 / generated 2026-09-21T06:12:05Z
