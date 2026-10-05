# GIS Quality Loop — gis-fjlport-1850 (2026-10-05 ~18:50 MSK)

A land/water audit of the live atlas against Natural Earth 10m land found ARC-PORT-049 "Franz Josef Land Ports" on a round soft coordinate, 80.0000 / 55.0000, in open water about 25 km from the nearest island.

## Win
| ID | Name | Before | After | Source | Shift |
|---|---|---|---|---|---|
| ARC-PORT-049 | Franz Josef Land Ports | 80.0000 / 55.0000 (open water, soft) | 80.7975 / 47.5568 | OSM way/1549655114 place=village Нагурское (80.7975295 / 47.5567856), Alexandra Land; Wikidata Q1529324 Nagurskoye airfield 80.80232778 / 47.66945 (~2 km) | ~174 km |

This is a settlement-level anchor, the same rule used for ARC-PORT-050 (Belushya Guba). Nagurskoye is the main year-round base on Franz Josef Land and matches the row's operator column ("Russian Navy/Research"). It is not a mapped commercial quay, so identity confidence stays moderate. Name, UNLOCODE and all other columns are unchanged.

ARC-LANE-015 (Lena River Route) and ARC-LANE-024 (Spitsbergen Research Route) end at this port, so their last vertex now ends at Nagurskoye. `/bathy/lane-depth.json` was re-scored: ARC-LANE-024 went from 1,359 to 1,405 km (ocean coverage 78.6% to 75.7%) and ARC-LANE-015 from 4,279 to 4,409 km. Both lanes already carry the "synthetic straight-line apex crosses land" QA flag.

## Live
- Atlas generation 2026-10-05T15:55:28Z, 1,320 features. Geometry changed only for ARC-PORT-049, ARC-LANE-015 and ARC-LANE-024. All served aliases synced.
- Lane depth generation 2026-10-05T15:56:06Z.
- `ports.csv` patched in every copy; row counts unchanged.
- Lock check: `python3 scripts/check_port049_fjl.py`.
- No SPA redeploy, no DNS change.

## Help wanted
Franz Josef Land has no mapped commercial quay in OSM. If you know a verifiable landing or berth location (Nagurskoye or Tikhaya Bay), please comment on issue #55 with a source.
