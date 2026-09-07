# Shipyard pin QA (2026-09-07 ~16:12 MSK)

Neutral GIS pin QA for ArcticTradeLanes shipyards. Prefer verifiable facility coordinates; do not invent pins for “site TBD” rows.

## Fixes this cycle

| id | action | reason |
|---|---|---|
| `ARC-SHIP-059` | dropped | Davie Helsinki Yard — same physical Helsinki Shipyard pin as `ARC-SHIP-010` |
| `ARC-SHIP-028` | dropped | Nuuk Shipyard — stacked on `ARC-SHIP-027` Greenland Dockyards city centroid |
| `ARC-SHIP-075` | cleared lat/lon | Rosatom / Rusatomenergo planned PEB assembly yard — exact site TBD (was fake-pinned on Sevgiprorybflot Murmansk) |
| `ARC-SHIP-014` | densified | Aker Arctic Technology HQ → Merenkulkijankatu 6, Helsinki (~60.2104, 25.0808) — no longer stacked on Arctech |

## Policy

- Do **not** coord-only-dedupe all shipyards (distinct operators can share a city HQ).
- Do drop **true same-yard rebrands** and **TBD-site** rows that borrow another facility’s coordinates.
- Quarantine planned yards without published coordinates (blank lat/lon; builder skips).

## CI

```bash
node scripts/check-shipyard-pins.mjs path/to/atlas.4326.geojson
```

Live after rebuild: shipyards **71→68**, atlas **1340→1337** features, apex+www verified.
