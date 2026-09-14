# Industry densify — 2026-09-14 (~16:00 MSK)

GIS Quality Loop. Industry↔city exact stacks **4 → 0**.

## Densified (verifiable OSM / densified port match)

| ID | Name | Was (city) | New WGS84 | OSM / source |
|----|------|------------|-----------|--------------|
| ARC-FAC-315 | Arctic LNG 1 Sabetta remote cargo terminal | 71.256, 72.052 | 71.2804697, 72.0611660 | Match densified ARC-PORT-004 industrial=port way/533105947 |
| ARC-FAC-362 | Liinakhamari Western Gate | 69.6333, 31.25 | 69.6422303, 31.3600764 | Match densified ARC-PORT-156 pier way/85396490 (planned site) |
| ARC-FAC-363 | Alyeschem North Slope | 70.2554, -148.3816 | 70.2560243, -148.4360072 | OSM way/221072677 industrial=oil (named Alyeschem geom absent) |
| ARC-FAC-378 | Sapujjijiit Inc. (Iqaluit) | 63.7467, -68.517 | 63.7477468, -68.5109165 | Astro Hill Complex way/298013944 (QCorp hub) |

## Remaining

None at exact 3dp industry↔city. Proposed ports still quarantine-stamped (024/034/052/063/069/153).

## Live

- https://arctictradelanes.com/atlas.geojson — generated `2026-09-14T13:06:45Z`, **1321** features, industry 110
- Backup on Zo: `arctic_industrial_facilities.csv.bak-gis-1600`
- Static public+dist atlas sync only — no SPA redeploy
- UM: live bundle still has `null_island` / `out_of_bounds` / `swapped_lat` client filters (no SPA redeploy)
