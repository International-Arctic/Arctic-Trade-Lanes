# GIS Quality Loop — gis-npra-1123 (2026-10-12 ~11:23 MSK)

## A) ARC-PROG-717 densify
BLM NPR-A Oil & Gas Lease Sale 2026 moved off round soft `69.0 / -152.0` (~201 km east of the reserve centre) to OpenStreetMap protected_area relation/8870643 Nominatim centroid `69.7266466 / -156.7005363`. Sources: OSM R8870643 (wikidata=Q6974897); Wikidata Q6974897 P625 `70 / -157`; Wikipedia National Petroleum Reserve–Alaska `70°N 157°W`. `position_quality=area_centroid` + `position_anchor`. DISTINCT from ARC-PROG-626 Anchorage admin seat and ARC-PROG-734 Deadhorse (~316 km).

## B) Schematic tags (coords unchanged)
- **ARC-FAC-354** BURO 1440 NSR space-comms: keep `73.0 / 80.0`; `position_quality=schematic_corridor_center` (corridor-wide approx centre — do not invent HQ).
- **ARC-FAC-370** North Pole drift-ice base: keep `89.5 / 0.0`; `position_quality=schematic_north_pole` (intentional polar schematic).

## Live
- Atlas gen `2026-10-12T08:27:49Z`, **1319** features; geometry diff **ARC-PROG-717 only**; property diffs FAC-354 / FAC-370 / PROG-717 only.
- Soft-pin audit (integer coords without `position_quality`): **0** remaining.
- Dataset CSV: `entrepreneur_programs.csv` (backup `*.bak-gis-npra-1123-*`).
- Builder: `atlas-proj/build_atlas.py` schematic allowlist (`ATL_SCHEMATIC_POSITION`).
- Locks: `scripts/check_prog717_npra.py`, `scripts/check_fac354_370_schematic.py`.
