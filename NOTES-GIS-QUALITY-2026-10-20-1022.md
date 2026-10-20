# GIS Quality Loop gis-loop-1020-1022 (~10:22 MSK, 2026-10-20)

## ARC-PORT-135 Kalvåg New Fishing Harbor (Bremanger, NOKVG): moved onto the Kystverket harbour point
- Old pin 61.7625 / 4.8763 (4 decimals) sat on land: it reverse-geocodes to the Bontlabo service road, Liset, Kalvåg (OSM way/518544959).
- New pin **61.764832 / 4.8758683** = OSM node/5359785046 `harbour=yes`, `seamark:type=harbour`, `seamark:harbour:category=fishing`, `seamark:name=Kalvåg`, `source=Kystverket` (Norwegian Coastal Administration import). It sits inside the Kalvåg harbour basin among the mapped OSM `man_made=pier` ways (1307682631–1307682642, 1331485463–1331485472, 571341676). The move is about 0.26 km N (bearing ~355°).
- `position_quality=facility_site` (a harbour reference point, not a surveyed berth line). Confidence stays at 88, `last_verified` is now 2026-10-20, all other attributes unchanged (UN/LOCODE NOKVG not changed).

## Atlas regression gate
- Built from the canonical Zo `atlas-proj` with `ref/ne_10m_land.geojson` against the Dataset.
- 1317 features; IDs, order and top level identical to the 06:55:31Z gen; the only differing feature is ARC-PORT-135 (geometry, position_quality, position_note, position_anchor).
- 25/25 lanes water-routed, land-mask fan 563, ship water fan 101 (display_offset 131 = live).
- Previously fixed ports did not move (including 036, 039, 053, 065, 066, 079, 083, 089, 093, 113, 119, 132, 157); PORT-066/079 still separate and cross-referenced.

## Live
- Atlas gen `2026-10-20T07:31:40Z`, 1317 features, EPSG:3996 (md5 3996 43cc242a, 4326 90b4cad5).
