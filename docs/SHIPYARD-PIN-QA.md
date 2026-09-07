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

## 2026-09-07 ~18:55 MSK — CSV column-shift realign

Three `shipbuilding_facilities.csv` rows were mis-aligned so the atlas builder (`_f64`) dropped them or would have plotted nonsense:

| id | problem | fix |
|---|---|---|
| `ARC-SHIP-033` | Sembcorp Marine — `country` held lat `1.2600`, `latitude` held lon `103.8300`, `longitude` held specialization text | Realign to Singapore HQ pin `1.2600, 103.8300` |
| `ARC-SHIP-052` | Kolskaya sports/pleasure workshop — same shift pattern (`country=69.06`, `lat=33.2`) | Realign to Kola Bay `69.0600, 33.2000` |
| `ARC-SHIP-025` | Vard Shipyards (Multiple) — `latitude`/`longitude` = `Various` | Quarantine blank coords (multi-site; prefer per-yard rows) |

Also stripped a UTF-8 BOM from `lanes.csv` (`lane_id` header) for non-`utf-8-sig` consumers (builder already used `utf-8-sig`).

### Live

- https://arctictradelanes.com/atlas.manifest.json — shipyards **68→70**, features **1314→1317**, `generated` `2026-09-07T15:55:37Z`, `crs_primary` 3996
- CI: `node scripts/check-shipyard-column-shift.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, no SPA redeploy.
