# GIS Quality — gis-port036-1444 (~14:44 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-036** Tiksi East Port off soft approximate `71.6800 / 128.9500`, which sat in Tiksi Bay water on the
northern edge of anchorage district No.1, onto **East Pier No.1** of Tiksi seaport: OSM **way/1081390287**
`man_made=pier` "Восточный пирс I", vertex centroid `71.6448592 / 128.8963706`. Moved **~4.33 km** SSW.

## Sources (neutral, public)
- Mintrans order No.50 of 14.02.2017 "Obligatory Regulations in seaport Tiksi" (legalacts.ru / consultant.ru): port on the west
  shore of Tiksi Bay; Annex 3: only operating berths are No.11 + No.12 on **Vostochny pirs No.1** (157.5 m each, 5.8 m depth);
  East Pier No.2 (berths 1-4, 13, 14) decommissioned. Annex coords `71°38'65" / 128°53'30"` are malformed (65"), so OSM is the anchor.
- OSM seamark berth nodes 9911507906 ("11") + 9911507905 ("12", min depth 5.8) on East Pier I; East Pier II way/1081390288 ~0.12 km SE;
  harbour area way/233652114 "Морской торговый порт Тикси"
- morvesti.ru/exclusive/81615: only 2 berths of one crane-equipped pier work (157 m, 5.8 m); the second similar pier is not accepted into service
- Wikidata: Tiksi town Q500895, Tiksi Bay Q2152754 (no Wikidata item for the port itself)
- No public source names a separate "Tiksi East Port"; identity inferred = the East piers of Tiksi seaport, so
  `position_quality=facility_site`. CSV code RUTIE and operator "Rosatom" left as-is but flagged unverified in the sources note.
- ARC-PORT-006 Tiksi Sea Port stays on way/1081390289 "Портовый флот" pier (~0.21 km W); not a co-site clash.

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-036 (schematic tags now 15)
- ports.csv: every copy (16) lat/lon + sources note (was empty), confidence=85, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port036_1444.py`; lock check `atlas-proj/check_port036_tiksi_east.py` (all prior port locks still OK)

## Live
- Atlas gen `2026-10-13T11:52:37.045706+00:00`, **1317** features (unchanged)
- Diff vs previous build: ARC-PORT-036 + its two dependent lanes only: ARC-LANE-002 NSR Eastern Section end vertex follows the
  port; ARC-LANE-003 NSR Full Transit end now equals waypoint #4, so the existing endpoint-revisit rule drops the 2-vertex tail (45 -> 43)
- 10 alias dirs synced (bad=0) + 9 extra served copies; 20 copies at new md5, 0 left on previous gen
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson, /atlas/atlas.3996.geojson verified
- No SPA redeploy / App.tsx / DNS change. UM: skipped (no patterned client-side geo-filter win this cycle)

## Next candidates
- ARC-PORT-075 Nuuk Qeqertat quay (64.17/-51.71; last 2-decimal soft port; need the new quay site from a public source)
- Then re-audit soft 4-decimal ports without OSM/WD refs in the sources field
