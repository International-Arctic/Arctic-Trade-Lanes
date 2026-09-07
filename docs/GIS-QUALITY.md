# GIS quality bar (OSS)

Standing goal: **maps users do not bounce from** — UnicornsMap.com (people / event pins + toggles) and ArcticTradeLanes.com (EPSG:3996 ships / ports / lanes).

## Principles

1. **Correct projection** — ATL polar views use **EPSG:3996** (IBCAO Polar Stereographic). Do not stretch WGS84 Web Mercator for high-Arctic UX.
2. **Backend ↔ frontend sync** — Zo remains production control plane; this repo mirrors schemas, filters, and verified samples. Dataset companion: [ArcticTradeLanes-Dataset](https://github.com/International-Arctic/ArcticTradeLanes-Dataset).
3. **Client-side bad-data filter** — cheap, offline-capable quarantine of null islands, out-of-bounds, duplicate ids, NaN coords. Prefer browser/edge filters over paid GIS SaaS.
4. **Almost free to serve** — static GeoJSON / future vector tiles on edge; no heavy server GIS in the hot path.
5. **No political bias** — neutral labels and sources; ≥2 verifiable sources (one institutional) for densified rows; no editorial slant in layer copy.

## ATL layers in scope

Ports · ships / tankers · icebreakers · lanes · cities · industrial / shipbuilding · entrepreneur programs (atlas pins).

## UM layers in scope

People pins · event locations · people-layer toggles · dedupe / geo QA.

## How to help

See open Issues labeled `help wanted` / `good first issue`. Additive PRs only — see [CONTRIBUTING.md](../CONTRIBUTING.md).


## Atlas download aliases (2026-09-07)

Broken schema.org `DataDownload` URLs (`/data/atlas.*.geojson`, missing `atlas.4326.geojson`) returned SPA HTML and bounced agent/crawler clients. Fixed with static aliases — see [ATLAS-DOWNLOAD-ALIASES.md](./ATLAS-DOWNLOAD-ALIASES.md).

## 2026-09-07 — WGS84 atlas projection stamp

Live `atlas.4326` / `atlas.wgs84` now declare `projection.epsg=4326` (coords were already lon/lat). Builder `build_atlas.py` stamps CRS after inverse so rebuilds do not regress. See [ATLAS-DOWNLOAD-ALIASES.md](./ATLAS-DOWNLOAD-ALIASES.md).


## 2026-09-07 — Ship fleet densify + country props

Icebreaker schematic pins no longer collapse onto one NSR centroid (max `position_stack_size` 53 → ≤17). Atlas ship features now carry `country` + `year_built` from `ArcticTradeLanes-Dataset`. Spec: [SHIP-FLEET-DENSIFY.md](./SHIP-FLEET-DENSIFY.md). CI helper: `node scripts/check-ship-fleet.mjs`.

## 2026-09-07 — Port/layer `iso2` stamps

Atlas point layers now carry ISO 3166-1 alpha-2 `iso2` (UN/LOCODE-first, country-name fallback; reject `NULL`/short fake codes). Spec: [PORT-ISO2.md](./PORT-ISO2.md). CI helper: `node scripts/check-port-iso2.mjs`.


## 2026-09-07 — Lane waypoint gazetteer (unresolved → 0)

Manifest `unresolved_lane_waypoints` cleared (8 → 0) via paren-safe waypoint split + schematic sea/port anchors (Bergen, Ningbo, North Sea, Laptev/East Siberian/Chukchi, Hamburg/Felixstowe). Live apex+www densified Kristiansand–Kirkenes (7 verts) and NSR China–Europe (12 verts). Spec: [LANES-WAYPOINTS.md](./LANES-WAYPOINTS.md). CI helper: `node scripts/check-lane-waypoints.mjs`.

## 2026-09-07 — Lane start/end teleport guard

Wrong `start_port_id` on ARC-LANE-026 pointed at Homer AK and drew an Alaska→Norway jump. Fixed port ids (Kristiansand `ARC-PORT-172`, Ningbo `ARC-PORT-173`), Kirkenes Port lat typo, and a 5 000 km start/end↔waypoint haversine guard (`lane_teleport_drops` on manifest). Spec: [LANE-TELEPORT.md](./LANE-TELEPORT.md). CI helper: `node scripts/check-lane-teleport.mjs`.

UM: `filterPeoplePins` / `filterEventPins` already accept `lon`/`longitude`/`latitude` aliases + Arctic-safe swap detect (no SPA redeploy this cycle).


## 2026-09-07 — Airport program_id dedupe + properties.id

Dropped duplicate `ARC-AIR-011` Inuvik AIF modernization row (`arctic_airports` 12→11). Builder skips duplicate `program_id` on EXTRA_POINT_LAYERS (`extra_id_drops` in manifest) and mirrors Feature ids into `properties.id`. Live atlas 1345→1344. Spec: [AIRPORT-ID-DEDUPE.md](./AIRPORT-ID-DEDUPE.md). CI helper: `node scripts/check-extra-ids.mjs`.

## 2026-09-07 — facility / program pin dedupe + UN/LOCODE fill

Dropped stacked Davie Defense Texas shipyard (`ARC-SHIP-066`) and duplicate CanNor NIEOP-ERS program (`ARC-PROG-525`); filled six public UN/LOCODEs; builder soft-dedupes program name+coord and shipyard ids. Live atlas **1344 → 1342**. See [FACILITY-DEDUPE.md](./FACILITY-DEDUPE.md).


## 2026-09-07 ~15:30 MSK
- Dropped Barrow alias + Kjøllefjord NULL duplicate; filled 12 UNECE LOCODEs; separated Shanghai Waigaoqiao/Jiangnan coords; builder `_clean_unlocode` guard. See `PORT-LOCODE-QA.md`.
