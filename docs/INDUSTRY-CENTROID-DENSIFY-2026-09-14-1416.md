# Industry densify + centroid_clone stamp — 2026-09-14 (~14:16 MSK)

GIS Quality Loop (map UX / geo quality). Industry↔city exact stacks **9 → 7**.

## Densified (OSM-verified)

| ID | Name | Was (city) | New WGS84 | OSM |
|----|------|------------|-----------|-----|
| ARC-FAC-012 | BSNC Nome Arctic logistics | 64.5011, -165.4064 | 64.4976121, -165.40514 | way/287815378 BSNC Building |
| ARC-FAC-351 | Adak Bulk Fuel hub | 51.8815, -176.6581 | 51.8692789, -176.6701699 | way/480643014 Tank |

## Quarantine stamp

`build_atlas.py` now stamps `geo_quality=centroid_clone` on **ports**, **shipyards**, and **industry** when the pin matches a city at 7 decimal places. `packages/geo-filter` quarantines those layers (default on).

Stamped this cycle (14): ARC-PORT-024/034/052/063/069/153, ARC-SHIP-069, ARC-FAC-315/335/337/342/362/363/378.

## Remaining (help wanted)

| ID | Notes |
|----|-------|
| ARC-FAC-315 | Sabetta / Geofizicheskoye remote terminal — prefer industrial=port, not city |
| ARC-FAC-335 | ARCAN Yellowknife — office/yard OSM |
| ARC-FAC-337 | Arva AS Narvik grid — substation/power |
| ARC-FAC-342 | Severny Proekt Arkhangelsk — office (not seaport clone) |
| ARC-FAC-362 | Liinakhamari Western Gate — pier/industrial |
| ARC-FAC-363 | Alyeschem Prudhoe — industrial pad |
| ARC-FAC-378 | Sapujjijiit Iqaluit — office |

Politically neutral labels only. No invented offsets.

## Live

https://arctictradelanes.com/atlas.geojson generated `2026-09-14T11:27:04Z` (1321 features).
