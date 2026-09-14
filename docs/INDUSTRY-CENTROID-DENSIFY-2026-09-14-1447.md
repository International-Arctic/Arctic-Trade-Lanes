# Industry densify — 2026-09-14 (~14:47–14:57 MSK)

GIS Quality Loop. Industry↔city exact stacks **7 → 4**.

## Densified (verifiable)

| ID | Name | Was (city) | New WGS84 | Source |
|----|------|------------|-----------|--------|
| ARC-FAC-335 | ARCAN Construction (Yellowknife) | 62.454, -114.3718 | 62.4238429, -114.4226383 | OSM way/976735297 Arcan Roofing And Cladding @ 88 Enterprise Drive (arcan.nt.ca HQ) |
| ARC-FAC-337 | Arva AS Northern Norway Power Grid | 68.4385, 17.4273 (Narvik) | 67.2916525, 14.4076229 | Arva AS HQ Bodø (grid operator seat; NIB loan company-level) |
| ARC-FAC-342 | Severny Proekt (Arkhangelsk) | 64.5393, 40.5185 | 64.5325868, 40.5171670 | Match densified ARC-PORT-002 harbour OSM way/1074548530 (AZRF fleet at seaport) |

## Remaining (quarantine `centroid_clone`)

315 Sabetta remote terminal, 362 Liinakhamari (planned), 363 Alyeschem Prudhoe, 378 Sapujjijiit Iqaluit.

## Live

- https://arctictradelanes.com/atlas.geojson — generated `2026-09-14T11:57:34Z`, **1321** features
- Static public+dist sync only — no SPA redeploy
- UM client filters `null_island` / `out_of_bounds` / `swapped_lat` present in live bundle
