# Port expansion densify (restore soft-deduped berths) — 2026-09-08

## Problem
`build_atlas` soft-dedupes ports that share identical cleaned UN/LOCODE + rounded WGS84 pin, keeping the lowest `port_id`. Seven expansion / project harbour rows were therefore **absent from the live atlas** even though they remained in `ports.csv`:

| Dropped id | Parent (kept) | LOCODE |
|---|---|---|
| `ARC-PORT-073` Arkhangelsk Deep-Water | `ARC-PORT-002` | RUARH |
| `ARC-PORT-132` Murmansk NSR container | `ARC-PORT-001` | RUMMK |
| `ARC-PORT-104` Narvik Dock 5 LKAB | `ARC-PORT-019` | NONVK |
| `ARC-PORT-113` Anchorage Cargo Terminal 1 | `ARC-PORT-025` | USANC |
| `ARC-PORT-165` Vardø fiskerihavn | `ARC-PORT-032` | NOVAO |
| `ARC-PORT-140` Ísafjörður pier extension | `ARC-PORT-077` | ISISA |
| `ARC-PORT-091` Qaqortoq dual-use | `ARC-PORT-053` | GLJJU |

Map UX: users only saw the parent operational harbour; expansion/project pins never rendered.

## Fixes (dataset)
Densified expansion rows onto verifiable berth / corridor coordinates (OSM Nominatim 2026-09-08, User-Agent `ArcticTradeLanes-GIS-QA/1.0`), then rebuilt atlas (`port_alias_drops` → 0 for these).

| ID | New lat,lon | Source note |
|----|-------------|-------------|
| `ARC-PORT-073` | 64.7083, 40.5135 | OSM Экономия cargo terminal |
| `ARC-PORT-132` | 68.9783, 33.0680 | OSM Portovyy proyezd 22 / MCSP container zone |
| `ARC-PORT-104` | 68.4205, 17.4332 | OSM Fagernesveien / LKAB Fagernes ore corridor |
| `ARC-PORT-113` | 61.2447, -149.8817 | OSM Port of Alaska place |
| `ARC-PORT-165` | 70.3740, 31.1019 | OSM Vardø havn |
| `ARC-PORT-140` | 66.0755, -23.1080 | Pier offset from ISISA parent toward Skutulsfjörður |
| `ARC-PORT-091` | 60.7225, -46.0335 | Between Qaqortoq town OSM and GLJJU parent |
| `ARC-FAC-365` | 68.9800, 33.0700 | Port Alliance off exact MCSP / FAC-336 pin |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/data/atlas.manifest.json`
- ports **149→156**, features **1317→1324**, `generated` `2026-09-08T07:48:16Z`, `crs_primary` 3996, `port_alias_drops` empty for these ids
- CI: `node scripts/check-port-expansion-densify.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, no SPA redeploy, commercial rails untouched.
