# Port↔city densify — 2026-09-14 (~17:45 MSK)

GIS Quality Loop. Verified densify for **1** remaining stack using Wikidata (politically neutral waterbody pin; no invented pier offset).

| ID | Change |
|----|--------|
| ARC-PORT-024 | Prudhoe Bay Oil Terminal → Wikidata Q49388893 P625 `70.335833333333,-148.36222222222` (Prudhoe Bay waterbody, not CDP) |

Exact 3-dp port↔city stacks among the tracked five: **5 → 4**. PORT-024 no longer stamped `centroid_clone`.

## Still centroid_clone / help wanted

| ID | Name | Notes |
|----|------|-------|
| ARC-PORT-034 | Obskaya LNG Terminal | Inland Novy Urengoy pin; do **not** clone Sabetta; do **not** use Obskaya railway Q4330011 |
| ARC-PORT-052 | Grays Bay Deep-Water Port (proposed) | Proposed = city row |
| ARC-PORT-069 | Chevak Barge Landing (planned) | Planned |
| ARC-PORT-153 | Steensby Inlet (proposed) | Mary River mineral port site; OSM bay relation R13745622 is far south of synthetic site — skip without site plan |

Client `filterGeoJson` continues to quarantine remaining `geo_quality=centroid_clone` ports (cities stay visible).
