# GIS Quality Loop — 2026-09-21 ~11:43 MSK

## Win (ATL)
- Densified **ARC-SHIP-009** Arctech Helsinki Shipyard off soft pin `60.1700,24.9400` onto Wikidata **Q4117007** Hietalahti shipyard P625 `60.158,24.929`.
- Company item Q1278953 has no P625; P159 HQ is Helsinki city centroid (~soft pin) — **not used**.
- Cross-check OSM way/4260855 Helsinki Shipyard Nominatim `60.1560341/24.9280005` / Overpass center `60.1560853/24.9279201` (successor **ARC-SHIP-010** same Hietalahti complex; keep distinct polygon centroid ~192 m). No OSM `industrial=shipyard` tag (WD place densify).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T08:43:31Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins`: coerce numeric-string lat/lng ("69.1"); smoke accepted 5 dropped 6 (Zo). No SPA redeploy / i18n untouched.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards (no-sources) 25→24.
- Remaining soft preferred queue: Ulstein ARC-SHIP-024 leave #37 unless OSM industrial=shipyard found; Damen Galati ARC-SHIP-013 (OSM way/888306100 noted ready).
