# GIS Quality — gis-port089-0918 (~09:18 MSK Europe/Moscow, 2026-10-14)

## Site health
GET `/` → **200** (3482B); atlas **200** (1317 feats, gen 2026-10-13T16:13:31Z before rebuild).
UM home **200**. **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-089** Grundarfjarðarhöfn (Grundarfjörður Harbour, Snæfellsnes, Iceland;
UN/LOCODE **ISGRU**) off soft 4-decimal `64.9183 / -23.2503` (= grundport.is harbour position
64d55m6s N 23d15m1s W, not the pier face) onto the Norðurgarður main pier:
OpenStreetMap **way/51858019** man_made=pier area=yes, shoelace centroid `64.9231680 / -23.2469906`.
Moved **~0.56 km** NNE.

## Sources (neutral, public)
- OSM **way/51858019** man_made=pier area=yes centroid 64.9231680/-23.2469906 (longest pier polygon in basin; maxspan ~319 m; official Norðurgarður 365 m / 40 m wide, Berth 1+2)
- OSM **way/51858020** secondary pier ~0.92 km N (unused)
- OSM industrial hinterland **way/203802229**
- Official port: grundport.is harbour position / Norðurgarður berth specs
- Wikidata **Q27014314** Grundarfjörður town P625 64.92427/-23.26313 (settlement only; not reused)
- UN/LOCODE ISGRU
- `position_quality=facility_site` (pier polygon; not a surveyed berth)
- DISTINCT from ARC-CITY-082 (~0.81 km from soft); no other ARC-PORT within 5 km

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-089 (schematic tags now 24)
- ports.csv: 13 copies lat/lon + densify sources note, confidence=92, last_verified=2026-10-14
- Patch `atlas-proj/_patch_port089_0918.py`; lock `atlas-proj/check_port089_grundarfjordur.py` (PORT-025/150 locks OK)

## Live
- Atlas gen `2026-10-14T06:25:01.318011+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff = ARC-PORT-089
- Alias sync to 59 served copies; no App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
Soft 4-decimal ports lacking OSM/WD in sources: PORT-053 Qaqortoq, PORT-093 Alta Urnesbukta, PORT-039 Rankin Inlet, PORT-034 Obskaya LNG, PORT-065 Kokkola (re-scan after this cycle).
