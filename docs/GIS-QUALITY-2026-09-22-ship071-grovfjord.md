# GIS Quality Loop — 2026-09-22 ~13:12 MSK

## Outcome
- **Densified ARC-SHIP-071 Grovfjord Mek. Verksted AS (GMV)** off soft `68.5830,17.3700` onto OSM **node/9016226127** Nominatim `68.6807150,17.1188960` (place=house addr **Astafjordveien 566, 9446 Grovfjord** — matches official gmv.no/kontakt-oss).
- Tag `gis-densify-1312`. Softish preferred blocked set unchanged (**13–14**); **open softish Grovfjord closed** — no remaining preferred open softish shipyards.
- Did **not** merge ARC-PORT-164 Lavna/MTU soft; quarantine untouched.
- Overpass (de/lz4/kumi) flaky/timeout; Wikidata Q116766227 has no P625 — Nominatim address node used.

## Soft shipyards (still blocked / quarantine)
Vigor-021, VT Halter-022, Eastern-023, Ulstein-024, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002, Naval Group-015, Waigaoqiao-036.

Open softish remaining: **none** (Grovfjord densified).

## Quarantine untouched
PORT-034/069, SHIP-069, ARC-PORT-164 (community review before merge).

## Atlas
- Rebuilt via Zo `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T10:21:06Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Synced Zo live paths — **no SPA redeploy / App.tsx**.

## UM
- No package bump (geo-filter already **0.1.4**); no new sentinel evidence this cycle.
