# Port↔city densify — 2026-09-14 (~18:45 MSK)

GIS Quality Loop. Verified densify for **1** remaining stack using OSM bay geometry (politically neutral; no invented pier offset).

| ID | Change |
|----|--------|
| ARC-PORT-052 | Grays Bay Deep-Water Port (proposed) → OSM [relation/13884530](https://www.openstreetmap.org/relation/13884530) Grays Bay center `67.7938459,-111.0127848` (cross-check Wikidata [Q5598339](https://www.wikidata.org/wiki/Q5598339) P625) |

Exact 5-dp port↔city stacks among the tracked four: **4 → 3**. PORT-052 no longer stamped `centroid_clone`.

## Still centroid_clone / help wanted

| ID | Name | Notes |
|----|------|-------|
| ARC-PORT-034 | Obskaya LNG Terminal | Inland Novy Urengoy pin; do **not** clone Sabetta; do **not** use Obskaya railway Q4330011; Ob Bay gulf node is not an LNG terminal |
| ARC-PORT-069 | Chevak Barge Landing (planned) | Overpass ~12 km: silos/storage_tank only — no pier/harbour/ferry_terminal |
| ARC-PORT-153 | Steensby Inlet (proposed) | Mary River mineral port site; OSM/Wikidata inlet geometry far from synthetic site — skip without site plan |

Client `filterGeoJson` continues to quarantine remaining `geo_quality=centroid_clone` ports (cities stay visible). Atlas companion CRS: EPSG:3996 polar stereographic (do not stretch WGS84 Mercator for polar views).
