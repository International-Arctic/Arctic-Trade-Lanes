# GIS Quality Loop — 2026-09-16 ~13:31 MSK

## Win
- Densified **ARC-SHIP-018** Davie Shipbuilding / Chantier Davie off soft Lévis city pin `46.8000,-71.1800` onto OSM [way/169057674](https://www.openstreetmap.org/way/169057674) Nominatim centroid `46.8300382,-71.1603630` (`landuse=industrial` `industrial=shipyard` `seamark:harbour:category=shipyard` website=davie.ca; Wikidata [Q2956389](https://www.wikidata.org/wiki/Q2956389)).

## Skipped / quarantine unchanged
- ARC-PORT-034 Obskaya, ARC-PORT-069 Chevak, ARC-SHIP-069 Sevgiprorybflot
- ARC-SHIP-002 Zvezda — still no strong Nominatim industrial hit
- ARC-SHIP-009 Arctech Helsinki — leave (same Hietalahti complex as SHIP-010)
- ARC-SHIP-024 Ulstein Verft — Nominatim only bus stop / defibrillator named Ulstein Verft (~62.341/5.823); need industrial polygon (help wanted)
- Wrangell PORT-086/SHIP-051 planned-only

## Atlas
- rebuild after CSV densify; sync live static dist/public/www only (no App.tsx / no SPA redeploy)
- features 1321 / shipyards 70 / ports 156 / crs_primary EPSG:3996
- centroid_clone remaining: ARC-PORT-034, ARC-PORT-069, ARC-SHIP-069

## Checks
- `check-ship018-davie-chantier-densify.mjs`
- UM pin filter smoke: accepted 4 / dropped 6
