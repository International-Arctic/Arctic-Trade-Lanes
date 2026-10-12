# GIS Quality Loop — gis-ice043-1535 (2026-10-12 ~15:35 MSK)

## Win: ARC-ICE-043 duplicate Oden quarantined

`icebreakers.csv` carried **ARC-ICE-043** `I/B Oden (same as ARC-ICE-033)` — the same
Swedish Maritime Administration Polar Class 2 icebreaker **Oden** (built 1988) as
**ARC-ICE-033**. Atlas fanned both onto the Svalbard "research" route anchor, so the
map showed two Oden pins (~15.77/78.40 and ~14.73/78.34).

## Fix (additive)

1. **`build_atlas.py`**: drop any icebreaker whose `vessel_name` matches
   `same as ARC-ICE-\\d+` (toggle `ATL_ICE_SAME_AS_DROP=0`). Manifest records
   `icebreaker_id_drops`.
2. **`icebreakers.csv`**: annotate ARC-ICE-043 `primary_service_route` with
   `[gis-ice043-1535 DUPLICATE QUARANTINE …]`; row kept for provenance; name keeps
   the same-as token for the builder regex.
3. **Lock**: `scripts/check_ice043_oden_quarantine.py`

## Live

| | Before | After |
|---|---|---|
| Features | 1318 | **1317** |
| Icebreakers | 56 | **55** |
| ARC-ICE-043 | present (fan pin) | **absent** |
| ARC-ICE-033 | Oden kept | Oden kept |

- Atlas gen stamped on rebuild this cycle
- Soft-integer / half-degree industry audits still only FAC-354/370 schematic (left alone)
- Orphan lane port refs: 0 (PORT-037 retarget still good)
- Help wanted: LANE-019 mid-route land-on-line (~400 km Chukotka/Wales); FAC-324/365 coarse 2-decimal city pins need verifiable OSM densify
