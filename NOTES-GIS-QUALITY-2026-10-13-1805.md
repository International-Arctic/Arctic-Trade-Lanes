# GIS Quality — gis-port171-1805 (~18:05 MSK Europe/Moscow, 2026-10-13)

## Site health
GET apex `/` → **200** (self-contained `dist/index.html`); Atlas GET **200**. **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-171** Port Elga — Manorsky Cape Coal Marine Terminal off soft 4-decimal `55.1167 / 135.7000`
(Wikipedia-class ~55°07′N 135°42′E = Wikidata **Q115763861** Эльга port P625 55.11667/135.7)
onto OpenStreetMap **way/1316635669** landuse=construction construction=industrial name=Порт Эльга
(wikipedia=ru:Эльга (порт)) shoelace centroid `55.1173682 / 135.6970483`. Moved **~0.20 km** WNW.
No OSM pier/quay mapped yet on Uda Bay / мыс Манорский shore.

## Sources (neutral, public)
- OSM **way/1316635669** Порт Эльга — landuse=construction; construction=industrial; wikipedia=ru:Эльга (порт); shoelace 55.1173682/135.6970483
- OSM **node/2643962546** мыс Манорский natural=cape 55.1142092/135.6950826 (~0.37 km SW)
- Wikidata **Q37884830** Cape Manorsky / Мыс Манорский P625 55.117222/135.6925 (~0.29 km W)
- Wikidata **Q115763861** Эльга (морской порт) P625 55.11667/135.7 (soft Wikipedia import; superseded by OSM facility)
- UN/LOCODE **RUVNN** (terminal water area within Vanino seaport boundaries)
- `position_quality=facility_site` (mapped terminal construction area; not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-171 (schematic tags now 21)
- ports.csv: 13 copies lat/lon + densify sources note, confidence=92, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port171_1805.py`; lock `atlas-proj/check_port171_manorsky.py`

## Live
- Atlas gen `2026-10-13T15:13:10.032313+00:00`, **1317** features; EPSG:3996 kept
- Alias sync bad=0 + extra served copies
- No App.tsx smash / SPA redeploy / DNS / x402 / restart. UM health check only.

## Next candidates
- ARC-PORT-150 Pyramiden (soft 78.6567/16.325)
