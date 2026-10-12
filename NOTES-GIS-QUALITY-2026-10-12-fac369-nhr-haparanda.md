# GIS Quality Loop — gis-nhr-1025 (2026-10-12 ~10:25 MSK)

Round-coordinate audit of the live atlas (ports, shipyards, industry, icebreakers with both coords on a 0.1° grid) plus a Natural Earth 10m land test flagged **ARC-FAC-369 Nordic Hydrogen Route (NHR)** sitting on a soft `59.8 / 20.8` in open water south-east of the Åland islands, about 690 km south of the Bothnian Bay corridor the row describes.

## Win
| ID | Name | Before | After | Source | Shift |
|---|---|---|---|---|---|
| ARC-FAC-369 | Nordic Hydrogen Route (Gasgrid Finland + Nordion Energi) | 59.8000 / 20.8000 (open water, soft) | 65.834178 / 24.117033 | Wikidata Q588976 Haparanda urban area (P625) | ~692 km |

Why Haparanda/Tornio: NHR is a buried coastal pipeline round the Bothnian Bay (Vaasa to Örnsköldsvik, branch Luleå to Gällivare/Kiruna). Nordion Energi's public consultation names Haparanda as the node joining the Haparanda–Örnsköldsvik and Haparanda–Vaasa sections, and Gasgrid's H2 information package (Sep 2025) describes the cross-border engineering and permitting work in the Tornio River. The pin is a corridor anchor at the FI/SE crossing, not a built asset; name and all other columns unchanged (additive).

- https://nordichydrogenroute.com/news/nordion-energi-launches-public-consultation-for-hydrogen-pipeline-between-haparanda-and-ornskoldsvik/
- https://gasgrid.fi/wp-content/uploads/Gasgrid_H2-Information-Package-for-Market-Participants_V1_Sep-2025_Final.pdf
- https://nordionenergi.se/projekt/vatgasinfrastruktur/nordic-hydrogen-route

## Live
- atlas gen **2026-10-12T07:29:41Z**, 1319 features, geometry changed: ARC-FAC-369 only (baseline rebuild was byte-identical in features to the previous live gen before the patch); aliases synced 10 dirs bad=0; `/atlas.geojson`, `/atlas/*`, `/data/*`, `/atlas.3996.geojson` verified live.
- `arctic_industrial_facilities.csv` patched in 10 Zo copies + Dataset (row counts unchanged, 110).
- No SPA redeploy, no DNS change.

## Lock
`python3 scripts/check_fac369_nhr.py atlas.wgs84.geojson`

## Remaining round-grid pins (for contributors)
ARC-FAC-354 BURO 1440 NSR space-comms layer (73.0/80.0, an abstract service layer) and ARC-FAC-370 North Pole drift base (89.5/0.0) are deliberate schematic anchors; ARC-ICE-010/016/018/023/027/034/046 already carry `position_quality=schematic_route_anchor`/`route_anchor`.
