# ARC-SHIP-016 BAE Systems (Naval Ships) — Scotstoun densify (2026-09-22 ~09:43 MSK)

## Change
- Soft city pin `55.8600,-4.2500` (Glasgow) → OSM **way/1310629676** Nominatim centroid `55.8816399,-4.3656145`.
- Tags: `landuse=industrial` + **`industrial=shipyard`**, name BAE Systems (Scotstoun / Blawarthill / Garscadden).
- Secondary: Govan **way/133174308** also named BAE Systems but `landuse=industrial` only (no `industrial=shipyard`) — not used per densify bar.
- Location label: **Glasgow (Scotstoun / Blawarthill)**. Tag `gis-densify-0943`. Softish shipyards **14→13**.

## Live / Dataset
- Atlas `generated` **2026-09-22T06:51:31Z**, 1321 features / 70 shipyards / 156 ports, EPSG:3996 primary.
- Live: https://arctictradelanes.com/data/atlas.geojson — ARC-SHIP-016 `[-4.365615, 55.88164]`.
- Dataset commit: `International-Arctic/ArcticTradeLanes-Dataset` (notes `NOTES-GIS-QUALITY-2026-09-22-0943.md`, CI `scripts/check-ship016-bae-scotstoun-densify.mjs`).

## Community next
- Vigor ARC-SHIP-021 Seattle, VT Halter ARC-SHIP-022 Pascagoula, Eastern ARC-SHIP-023 Panama City (US soft `.xx00` pins).
- Still blocked: Wuchang ARC-SHIP-039, Sembcorp ARC-SHIP-033 (need `industrial=shipyard`); Hyundai ARC-SHIP-034 avoid dup vs ARC-SHIP-058.
