# GIS Quality — gis-port157-0943 (~09:43 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-157** Murmansk Arctic Gate Marine Terminal (Mishukovo) off soft `68.9800 / 33.0000` (~7.4 km) onto OpenStreetMap **way/129872684** Mishukovo hamlet Nominatim `69.0451678 / 33.0406397` (Kola Bay west shore).

## Sources (politically neutral gazetteer)
- OSM way/129872684 Mishukovo / Мишуково place=hamlet (Nominatim)
- Terminal is pre-investment / first cargo ~2028; no dedicated pier OSM yet — settlement_site is the cited site
- Distinct from ARC-PORT-031 Lavna Coal Terminal (east shore)

## Builder
- `atlas-proj/build_atlas.py` stamps `position_quality=settlement_site` + `position_anchor` (ATL_SCHEMATIC_POSITION allowlist; schematic tags now 5)
- ports.csv (3 copies): lat/lon/sources/confidence=88/last_verified=2026-10-13

## Live
- Atlas gen `2026-10-13T06:48:49Z`, **1317** features (count unchanged)
- Geometry change: **ARC-PORT-157 only** (coords soft→settlement)

## Skipped this cycle
- RSC-006 Anadyr / FAC-324 — next soft densify candidates
- UM — no cheap second win
