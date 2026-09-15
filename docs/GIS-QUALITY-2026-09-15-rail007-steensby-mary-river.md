# GIS Quality — ARC-RAIL-007 Steensby densify (2026-09-15 ~13:11 MSK)

Densified **ARC-RAIL-007** (Steensby Railway, Mary River mine → Steensby Inlet) off **ARC-CITY-100** centroid_clone onto OSM `place=village` Mary River ([node/5324804093](https://www.openstreetmap.org/node/5324804093)) at `71.3144708, -79.2931755` (Mary River Mine Logistics / northern terminus).

| | Before | After |
|--|--------|-------|
| coords | `71.9600, -79.6000` (CITY-100 stack) | `71.3144708, -79.2931755` |

Cross-check: Mary River Airport [node/5324804092](https://www.openstreetmap.org/node/5324804092) `71.3224319,-79.3448993`. Distinct from densified **ARC-PORT-153** Steensby Inlet bay `70.3851175,-79.0793288`.

- Live atlas: `generated` `2026-09-15T10:15:08Z`, **1321** features / **156** ports / **14** rail / CRS **EPSG:3996**
- CI lock: `scripts/check-rail007-steensby-mary-river-densify.mjs`
- Dataset: densify commit on `International-Arctic/ArcticTradeLanes-Dataset`

Neutral OSM/Nominatim sourcing only. Hard quarantine unchanged (PORT-034 / PORT-069 / SHIP-069).
