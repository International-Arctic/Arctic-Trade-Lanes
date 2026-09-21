# GIS Quality — ARC-SHIP-045 Sefine Shipyard densify (2026-09-21 ~13:19 MSK)

## Change
Moved **ARC-SHIP-045** (Sefine Shipyard, Altınova, Turkey) off soft pin `40.7000,29.5200` onto Nominatim centroid of OSM **way/1124414309** (`landuse=industrial`, `industrial=shipyard`, name **Sefine Tersanesi** / `name:en=Sefine Shipyard`):

- **WGS84:** `40.7303284, 29.5040636`
- **Sources cite:** OSM way id + `industrial=shipyard` + densify tag `gis-densify-1319`
- **Wikidata:** Q55998846 (no P625) — OSM shipyard polygon preferred (same pattern as ARC-SHIP-030)

## Atlas
- Rebuilt EPSG:3996 atlas `generated` `2026-09-21T10:24:31Z`
- Features 1321; shipyards 70; ports 156
- Quarantine untouched: PORT-034/069, SHIP-069, Zvezda, Wrangell, Ulstein #37

## Softish shipyards
21 → 20 (2dp-only heuristic on CSV)

## CI
`check-ship045-sefine-densify.mjs` locks CSV coords + sources.

## Related
Closes community GFI https://github.com/International-Arctic/Arctic-Trade-Lanes/issues/42
