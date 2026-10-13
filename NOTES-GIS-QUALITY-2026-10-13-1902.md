# GIS Quality — gis-port025-1902 (~19:02 MSK Europe/Moscow, 2026-10-13)

## Site health
GET `/` → **200**; atlas **200** (1317 feats, gen 2026-10-13T15:35:13Z before rebuild). **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-025** Port of Anchorage (Port of Alaska, Knik Arm / Cook Inlet, UN/LOCODE **USANC**) off soft 4-decimal
`61.2387 / -149.9076` (empty sources, no position_quality; Ship Creek / downtown edge) onto the main cargo dock:
OpenStreetMap **way/28577877** man_made=pier area=yes, centroid `61.2408396 / -149.8872591`. Moved **~1.11 km** ENE.

## Sources (neutral, public)
- OSM **way/28577877** man_made=pier (cargo dock face) centroid 61.2408396/-149.8872591
- OSM **relation/10511522** Port of Alaska landuse=industrial, operator/owner Municipality of Anchorage, wikidata Q3398440 (centroid 61.2446867/-149.8816953 — already used by ARC-PORT-113 Terminal 1 replacement, so not reused; PORT-025 now ~0.52 km SW of PORT-113)
- Wikidata **Q3398440** Port of Alaska P625 61.2403/-149.886 (~0.09 km from anchor), P1937 UN/LOCODE USANC
- OSM Terminal Road way/28577529; Alaska Railroad City Dock Track spurs way/319205158, way/1157471331
- Southern piers way/1047211551–1047211553 (~0.5 km S; petroleum/cement terminal area) not used as parent anchor
- `position_quality=facility_site` (cargo pier; not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-025 (schematic tags now 23)
- ports.csv: 13 copies lat/lon + densify sources note, confidence=92, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port025_1902.py`; lock `atlas-proj/check_port025_anchorage.py` (PORT-150/171/047/051/022/042 locks OK)
- Side effect: ARC-PROG-071 no longer co-site-nudged (PORT-025 left its pin); PROG-071 now plots at its own anchor 61.2387/-149.9076

## Live
- Atlas gen `2026-10-13T16:13:31.666462+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff = ARC-PORT-025 (+ PROG-071 nudge removal)
- Alias sync bad=0 (10 dirs) + 10 extra served copies; 0 left on previous gen
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.
