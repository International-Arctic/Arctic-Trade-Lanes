# GIS Quality — ARC-RAIL-008 Stegra–Boden densify (2026-09-15 ~13:45 MSK)

Densified **ARC-RAIL-008** (Stegra – Boden Industrial Park Rail Connection to Malmbanan/Ore Line) off **ARC-FAC-368** Boden Industrial Park soft-stack onto OSM `landuse=construction` STEGRA stålverk Boden ([way/1388001960](https://www.openstreetmap.org/way/1388001960)) centroid `65.8050320, 21.7936653`.

| | Before | After |
|--|--------|-------|
| coords | `65.8252, 21.6893` (FAC-368 stack) | `65.8050320, 21.7936653` |

Cross-check: Boden C railway station [node/8930884280](https://www.openstreetmap.org/node/8930884280) `65.8288537,21.7082307` (Malmbanan hub, ~5.3 km NW of Stegra); Stegra HMP [way/1481669820](https://www.openstreetmap.org/way/1481669820). Distinct from densified **ARC-RAIL-002** (Narvik) / **ARC-RAIL-005** (Norrbotniabanan).

- Live atlas: `generated` `2026-09-15T10:44:45Z`, **1321** features / **156** ports / **14** rail / CRS **EPSG:3996**
- CI lock: `scripts/check-rail008-stegra-boden-densify.mjs`
- Dataset: densify commit on `International-Arctic/ArcticTradeLanes-Dataset`

Neutral OSM/Nominatim sourcing only. Hard quarantine unchanged (PORT-034 / PORT-069 / SHIP-069).
