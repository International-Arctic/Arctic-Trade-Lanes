# Shipyard ↔ city exact-stack lock (2026-09-15)

## Problem

`ARC-SHIP-069` Bergen Group Sevgiprorybflot (Murmansk) still shares the **exact** WGS84 pin of `ARC-CITY-001` Murmansk (`33.0827, 68.9585`). Client `filterGeoJson` quarantines it via `geo_quality=centroid_clone`.

## Overpass / Nominatim re-check (this cycle)

Murmansk bbox ~`68.85–69.10N, 32.85–33.40E` (mail.ru Overpass mirror; de/lz4 returned HTTP 406 from this runner):

| OSM | Name | Dist from city centroid | Use for SHIP-069? |
|-----|------|-------------------------|-------------------|
| way/86206897 | Мурманская Судоверфь | ~1.7 km | **No** — different yard |
| way/69708145 | Мурманский судоремонтный завод Морского флота | ~1.8 km | **No** |
| way/87161399 | СРЗ ММФ | ~1.8 km | **No** |
| node/4185374391 | 35 СРЗ | ~7.7 km | **No** |
| way/676358072 | ЦСКМС (industrial=shipyard) | ~14.7 km | **No** — Belokamenka |

Named `Севгипрорыбфлот|Sevgiprorybflot|Bergen Group` Overpass + Nominatim → **0**. Official host `sgrf-mur.com` did not resolve from the runner. **Do not invent** an office/yard offset; keep quarantine until a verifiable facility pin exists.

Ports `ARC-PORT-034` / `069` / `153` re-checked same cycle: harbour/pier/industrial=port Overpass → **0** (unchanged).

## CI

```bash
node scripts/check-shipyard-city-stack.mjs path/to/atlas.4326.geojson
bun scripts/check-shipyard-city-stack-filter.mjs path/to/atlas.4326.geojson
```

`filterGeoJson` also quarantines **unstamped** shipyards that share a city pin at 6-dp (defensive; SHIP-069 stamp still required by the node lock).


Asserts:

1. Exact shipyard↔city stacks (6-dp) are **only** the `EXPECTED_STACKS` map (today: SHIP-069↔CITY-001).
2. Each allowed stack carries `geo_quality=centroid_clone`.
3. Expected stacks are still present (forces EXPECTED update after a real densify).

Companion lock: `scripts/check-centroid-clone-remaining.mjs` (ports 034/069 + SHIP-069 (PORT-153 densified 2026-09-15)).

## Policy

- Prefer verifiable OSM `industrial=shipyard` / named facility nodes.
- Never borrow another Murmansk yard’s geometry for Sevgiprorybflot.
- Politically neutral OSINT; no invented offsets for HQ-only rows.
