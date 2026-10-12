# GIS Quality — ARC-SHIP-022 VT Halter Marine duplicate quarantine (2026-10-12 ~09:30 MSK)

## Finding
Live atlas still rendered soft **ARC-SHIP-022** VT Halter Marine at Pascagoula city centroid `30.3700/-88.5600` (~2 dp) while **ARC-SHIP-068** Bollinger Mississippi Yard (Polar Sentinel WMSP-21) already pins the same physical yard at `30.3470/-88.5430` (~3.0 km apart).

## Evidence
- Wikidata **Q29093553** “Bollinger Mississippi Shipbuilding” (shipyard in Pascagoula, MS) lists aliases **VT Halter Marine** / **Halter Marine** (no P625 on the item).
- Bollinger acquired VT Halter Marine in 2022 (USNI / MarineLink coverage already cited on ARC-SHIP-068 sources).
- OSM around the soft pin is dominated by Huntington Ingalls / Ingalls Shipbuilding polygons — no named Halter/Bollinger `industrial=shipyard` way found this cycle for a fresh densify.

## Change
Cleared lat/lon on ARC-SHIP-022 (Vard-025 empty-coord quarantine pattern) so `build_atlas` omits the alias pin. Row kept for provenance + fact-page slug `vt-halter-marine`. Location label notes the ARC-SHIP-068 alias.

## CI
`node scripts/check-ship022-halter-quarantine.mjs [atlas.wgs84.geojson]`

## Related
Issue #46 (US soft shipyards Vigor/Halter/Eastern) — Vigor-021 and Eastern-023 already densified earlier; Halter closed via quarantine onto 068.
