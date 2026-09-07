# Dataset schema (intended)

Mirrored from Zo `ArcticTradeLanes-Dataset`. Full dumps sync into `/dataset` when published.

| File | Purpose | Key columns (typical) |
|------|---------|------------------------|
| ports.csv | Arctic / NSR ports | id, name, lat, lon, country, unlocode |
| cities.csv | Arctic cities | id, name, lat, lon, country |
| lanes.csv | Sea lanes / corridors | id, name, waypoints, season |
| tankers.csv | Tanker registry pins | id, name, country, ice_class, route, year_built (atlas pins schematic) |
| icebreakers.csv | Icebreaker fleet | id, name, country, ice_class, route, year_built (atlas pins schematic) |
| shipbuilding_facilities.csv | Shipyards | id, name, lat, lon, country |
| entrepreneur_programs.csv | Grants / soft-landing | program_id (ARC-PROG-###), lat, lon, benefits, sources |
| arctic_industrial_facilities.csv | Industry pins | facility_id, lat, lon, sources |
| rail_corridors.csv | Rail overlays | id, name, geometry refs |
| arctic_airports.csv | Airports | id, name, lat, lon |
| arctic_rescue_centers.csv | Rescue | id, name, lat, lon |
| arctic_reference.csv | Arctic-8 country meta | iso2, currency, language, regime |

Verification rule for new rows: ≥2 independent sources including one official/institutional; confidence 0–100; `last_verified` date.
