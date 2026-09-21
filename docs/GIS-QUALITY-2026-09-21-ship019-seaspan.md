# GIS Quality — ARC-SHIP-019 Seaspan Vancouver Shipyards densify (2026-09-21 ~13:37 MSK)

## Change
Moved **ARC-SHIP-019** (Seaspan Vancouver Shipyards) off soft pin `49.2900,-123.1200` onto Nominatim centroid of OSM **way/709281886** (`landuse=industrial`, `industrial=shipyard`, name **Seaspan Vancouver Shipyard**, operator Seaspan):

- **WGS84:** `49.3139099, -123.1070059`
- **Overpass center:** ~`49.3139001/-123.1054270`
- **Addr:** 2 Pemberton Avenue, District of North Vancouver, BC
- **Sources cite:** OSM way id + `industrial=shipyard` + densify tag `gis-densify-1337`
- **Wikidata:** no P625 found — OSM shipyard polygon preferred (same pattern as ARC-SHIP-045 / ARC-SHIP-030)
- **Location label:** Vancouver → North Vancouver

## Atlas
- Rebuilt EPSG:3996 atlas `generated` `2026-09-21T10:38:04Z`
- Features 1321; shipyards 70; ports 156
- Quarantine untouched: PORT-034/069, SHIP-069, Zvezda, Wrangell, Ulstein #37

## Softish shipyards
20 → 19 (2dp-only heuristic on CSV)

## CI
`check-ship019-seaspan-densify.mjs` locks CSV coords + sources.
