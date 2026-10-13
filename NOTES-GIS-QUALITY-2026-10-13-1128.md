# GIS Quality — gis-port110-1128 (~11:28 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-110** Galtarhöfn Deep-Water Harbour & Green Industrial Park (GH Harbour, planned) off soft
approximate `64.32 / -21.85` (~0.56 km off OSM coastline, SW of the zoned land) onto the **Galtarlækur farmstead**
OSM **way/560639791** (building; Nominatim `64.3470050 / -21.8087513`). Moved **~3.6 km** NE.

## Sources (neutral gazetteer / official planning)
- Hvalfjarðarsveit official notice 2025-10-14 *Kynningarfundur – Galtarlækur – Galtarhöfn*: aðalskipulag 2020-2032
  amendment, planning area ~102 ha "neðan þjóðvegar 1 í landi Galtarlækjar" (below Route 1 in the land of Galtarlækur)
- ghharbour.com (official project site): "deep water and room to grow at Galtarlækur", beside Grundartangi, 40 km from Reykjavík
- OSM way/560639791 Galtarlækur building + driveways way/560639793 / 560639794 / 560639795
- OSM checks: farmstead 0.24 km from OSM Route 1, 0.57 km from OSM coastline (i.e. inside the seaward strip the notice describes);
  ~2.0 km WSW of Grundartangi locality OSM node/2876959423 (WD Q1550445)
- Alternative checked: OSM way/249515549 *Galtarvík* is a road (highway=unclassified, ref 5049; centroid 64.3390/-21.8227,
  ~2.5 km from soft pin) — not the named land parcel, so not used as anchor
- No Wikidata item for Galtarhöfn/Galtarlækur found (wbsearchentities)
- Quay line not yet fixed (EIA pending) → `position_quality=facility_site` (planned)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION allowlist + ARC-PORT-110 (schematic tags now 8)
- ports.csv: every copy (16) lat/lon + sources note, last_verified=2026-10-13 (confidence 88 kept)
- Lock check `atlas-proj/check_port110_galtarhofn.py`

## Live
- Atlas gen `2026-10-13T08:27:30.318947+00:00`, **1317** features (unchanged), 10 alias dirs bad=0
- Live diff vs previous gen 07:59:24Z: **ARC-PORT-110 only**

## Next candidates
- ARC-PORT-045 Ambarchik 69.65/162.35 → OSM way/655223046 ~2.7 km (verify)
- ARC-PORT-041 Mys Shmidta 68.87/-179.40 → OSM way/93613726 ~2.7 km (verify)
- ARC-PORT-136 Narvik Terminal Nord ~1.3 km (low value)
- UM: skipped
