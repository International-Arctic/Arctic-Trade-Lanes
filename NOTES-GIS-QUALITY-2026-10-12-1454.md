# GIS Quality Loop — gis-port037-1454 (2026-10-12 ~14:54 MSK)

## Win: missing ARC-PORT-037 retargeted to real Alaska ports

Five `lanes.csv` rows referenced **ARC-PORT-037**, which has never existed in `ports.csv`.
The builder silently dropped the end/start port and fell back to GAZETTEER / city tokens:

| Lane | Before end/start | Symptom |
|---|---|---|
| ARC-LANE-025 Transpolar | Harrison Bay coast 70.444693/-151.360895 (after Alaska landlocked snap) | Future NSR–Alaska route missed Utqiagvik by ~218 km |
| ARC-LANE-005 NWP Deep Water | schematic Beaufort **-135.0 / 72.0** | Endpoint ~761 km from any Alaska port |
| ARC-LANE-018 Chukchi | city centroid Barrow 71.2906/-156.7887 | Not the densified harbour pin |
| ARC-LANE-019 Bering Strait | city centroid Barrow | Same |
| ARC-LANE-016 Alaska Coastal | city Nome 64.5011/-165.4064 | Waypoints end at Nome; missing port id |

## Fix (Dataset `lanes.csv`, additive)

| Lane | Field | After |
|---|---|---|
| ARC-LANE-005 / 018 / 019 / 025 | end or start | **ARC-PORT-056** Utqiagvik (Barrow) Port 71.304296/-156.756832 (OSM node/846364136, densify 2026-09-14) |
| ARC-LANE-016 | end | **ARC-PORT-026** Nome Harbor 64.496022/-165.437672 (waypoints: …-Nome) |

No new port row; CSV untouched except those 5 id cells. Atlas rebuild only changes those 5 lane geometries (1318 feats). Prior locks (lane waypoint water, river order, ship single-water) still OK.

## Live
- Atlas gen `2026-10-12T11:59:58.696950+00:00`, **1318** features
- Lock: `scripts/check_port037_utqiagvik.py`
- Help wanted: LANE-019 still carries ~400 km land-on-line mid-route (Chukotka / Wales vertices); finer coastal waypoint densify is next.
