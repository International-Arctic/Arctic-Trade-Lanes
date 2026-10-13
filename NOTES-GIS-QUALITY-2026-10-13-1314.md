# GIS Quality — gis-port105-1314 (~13:14 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-105** Cascade Point Ferry Terminal (planned Alaska Marine Highway System terminal, Lynn Canal north of Juneau)
off soft approximate `58.8500 / -135.0200` onto the **north terminus of Glacier Highway**, OSM **node/2835378419**
`58.7001371 / -134.9378631` (end node of way/217384152, joined by the turnaround way/1033357934).
Moved **~17.3 km** S/SE; the old pin sat in open water in upper Berners Bay, far from any road or shore facility.

## Sources (neutral, public)
- Alaska DOT&PF press release PR25-0020: terminal at Cascade Point (Mile 42, Glacier Highway), Goldbelt-owned surrounding land
- Alaska DOT&PF PR23-0010 (2023 DOT&PF + Goldbelt MOU, "approximately MP 42 of Glacier Highway")
- KTOO 2013-06-25: Glacier Highway extension ribbon-cutting, Echo Cove → Cascade Point (road ends at the Goldbelt gate)
- DOT&PF 35% design planset HSHWY00015 ("Cascade Point Terminal") site map: east shore of Berners Bay, north of Point Bridget / Echo Cove
- OSM API: Glacier Highway way/217384152 north end node/2835378419; Point Bridget node/7770571099 and Echo Cove relation/15904788 to the south
- No OSM pier / ferry_terminal mapped yet (terminal not built) — `position_quality=facility_site`
- Rejected: Slate Cove Marine Terminal piers (way/1347841780, way/344331768) — that is the Kensington mine landing on the west side of Berners Bay, a different facility

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-105 (schematic tags now 12)
- ports.csv: every copy (16) lat/lon + sources note appended, confidence=90, last_verified=2026-10-13 (CRLF copies preserved)
- Patch `atlas-proj/_patch_port105_1314.py`; lock check `atlas-proj/check_port105_cascade_point.py` (prior PORT-046/041/045/110/078 locks still OK)

## Live
- Atlas gen `2026-10-13T10:24:06.124550+00:00`, **1317** features (unchanged); diff vs previous served atlas: **ARC-PORT-105 geometry only**
- 10 alias dirs synced (bad=0) + 10 extra served copies, stale copies 0
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson verified PORT-105 at Glacier Hwy north end + facility_site
- No SPA redeploy / App.tsx / DNS change

## Help wanted
When DOT&PF publishes final terminal drawings (or the causeway / loading ramp is built and mapped in OSM), a PR moving this pin onto the
ramp or berth would make it a surveyed site. Please cite a public source.

## Next candidates
- ARC-PORT-036 Tiksi East Port (71.68/128.95, ~5 km from OSM Tiksi seaport landuse=harbour way/233652114 — need a source that "East Port" is that harbour, not a separate site)
- ARC-PORT-075 Nuuk Qeqertat quay (64.17/-51.71 — need the Qeqertat quay site from sikuki.gl)
- ARC-PORT-136 Narvik Terminal Nord ~1.3 km (low value)
- UM: skipped (time)
