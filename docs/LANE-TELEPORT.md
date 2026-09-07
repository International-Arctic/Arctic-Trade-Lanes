# Lane start/end teleport QA

Schematic lane polylines prepend `start_port_id` / append `end_port_id` coords from `ports.csv`, then insert gazetteer waypoints. A **wrong port id** can teleport the polyline across an ocean before the first real waypoint.

## Incident (2026-09-07 GIS Quality Loop)

| Lane | Bug | Symptom |
|------|-----|---------|
| ARC-LANE-026 Kristiansand–Kirkenes | `start_port_id=ARC-PORT-067` (Homer Harbor, Alaska `USHOM`) | First vertex `[-151.5483, 59.6425]` then jumped to Kristiansand `[8.0, 58.15]` |
| ARC-LANE-027 NSR China–Europe | `start_port_id=ARC-PORT-044` (Provideniya/Anadyr) while waypoints begin at Ningbo | Bering tip before Ningbo |
| ARC-PORT-015 Kirkenes Port | latitude `70.7269` (1° north of city `69.7269`) | Port pin ~110 km offshore / inland error |

## Fix (live on apex + www)

1. Added **ARC-PORT-172** Kristiansand Port (`NOKRS`, `58.1467, 7.9956`) and set LANE-026 `start_port_id` → `ARC-PORT-172`.
2. Added **ARC-PORT-173** Ningbo-Zhoushan schematic gateway (`CNNGB`) and set LANE-027 `start_port_id` → `ARC-PORT-173`.
3. Corrected Kirkenes Port lat `70.7269` → `69.7269` (matches city + other Kirkenes port rows).
4. Builder guard in Zo `atlas-proj/build_atlas.py`:
   - `_haversine_km` + `LANE_TELEPORT_MAX_KM = 5000`
   - Drop start if &gt;5 000 km from **first** waypoint; drop end if &gt;5 000 km from **last** waypoint
   - Emit `lane_teleport_drops` on `atlas.manifest.json` (should be `[]` when ids are correct)
5. Dedupe consecutive identical vertices after merge.

**Verified live:** `ports=173`, `unresolved_lane_waypoints=[]`, `lane_teleport_drops=[]`,  
LANE-026 tip `[7.9956, 58.1467]` → Kirkenes `[30.0456, 69.7269]`,  
LANE-027 tip Ningbo `[121.55, 29.87]`.  
Manifest generated `2026-09-07T10:49:58Z`.

## How to help (good first issue)

- CI: fail if `lane_teleport_drops` non-empty; fail if a non-Americas/NSR lane has any `lon < -100` vertex (catches Homer tip on Norway corridors); consecutive jump &gt;7 500 km as backup.
- CI: fail if `lane_teleport_drops` is non-empty after `build_atlas`.
- Audit remaining `lanes.csv` `start_port_id` / `end_port_id` against first/last waypoint names (neutral, source-cited).
- Optional: prefer gazetteer-only geometry when start/end port names do not fuzzy-match the first/last waypoint tokens.

Stay schematic — no fake AIS precision; politically neutral labels.
