# GIS Quality — gis-port053-0945 (~09:45 MSK Europe/Moscow, 2026-10-14)

## Site health
GET `/` → **200**; atlas **200** (1317 feats, gen 2026-10-14T06:25:01Z before rebuild).
UM home **200**. **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-053** Qaqortoq Port (Royal Arctic Line, South Greenland; UN/LOCODE **GLJJU**)
off soft 4-decimal `60.7288 / -46.0278` (~1.3 km NNE of the harbour, inland in the upper town)
onto the harbourfront port yard: OpenStreetMap **way/511853551** landuse=industrial (11.4k m²,
on coastline way/1476531377), shoelace centroid `60.7178523 / -46.0365644`. Moved **~1.31 km** SSW (bearing ~201°).

## Sources (neutral, public)
- OSM **way/511853551** landuse=industrial port yard; shares nodes with piers **way/598638435** + **way/598638436** and Arctic Umiaq Line ferry route **way/512918611**
- OSM **way/351129063** building=industrial `Royal Arctic Line` (Torvevej B-163) inside the yard (~33 m from centroid)
- OSM Konge Bro pier **way/378873667** + ferry_terminal **node/3822342850** ~0.10 km E (passenger quay; unused as anchor)
- Wikidata **Q221203** Qaqortoq town P625 60.7167/-46.0333 (1′ precision; settlement only, not reused); no Wikidata port item found
- UN/LOCODE GLJJU
- `position_quality=facility_site` (port yard polygon; not a surveyed berth)
- DISTINCT from **ARC-PORT-091** dual-use expansion (60.7225/-46.0335, ~0.54 km N, untouched) and **ARC-PORT-127** Nuupiluk (~11.2 km WNW, untouched); no collapse

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-053 (both builder copies)
- ports.csv: 13 copies lat/lon + densify sources note, confidence=90, last_verified=2026-10-14
- Patch `atlas-proj/_patch_port053_0945.py`; lock `atlas-proj/check_port053_qaqortoq.py` (also asserts 091 not collapsed); all prior port locks OK

## Live
- Atlas gen `2026-10-14T06:54:15.636695+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff = ARC-PORT-053 only
- Alias sync bad=0 (10 dirs) + 41 extra served copies; 0 stale manifests left
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-093 Alta Urnesbukta, PORT-039 Rankin Inlet, PORT-034 Obskaya LNG, PORT-065 Kokkola.
