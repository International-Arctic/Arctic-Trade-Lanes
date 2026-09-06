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
