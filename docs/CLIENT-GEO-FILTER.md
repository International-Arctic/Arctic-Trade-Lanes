# Client-side geo filter (spec)

Target: run in the browser (or edge Worker) with **near-zero serving cost**.

## Quarantine rules (v0)

Drop or flag a feature when any hold:

| Rule | Test |
|------|------|
| Null island | lon≈0 && lat≈0 (ε 1e-4) without explicit `allowNullIsland` |
| Out of world | \|lat\| > 90 or \|lon\| > 180 |
| Arctic focus (ATL) | Prefer lat ≥ 50 for NSR-primary layers; below → `review` not hard-drop |
| NaN / missing | non-finite coordinates |
| Duplicate id | same `id` / `properties.id` within layer |
| Duplicate point | same lon/lat within ε 1e-5 and same layer type |

## Output

- `accepted: FeatureCollection`
- `quarantine: FeatureCollection` + `reason` property
- Counters for QA dashboards

## Reference sketch (TypeScript)

```ts
export type FilterStats = { accepted: number; quarantined: number; reasons: Record<string, number> };

export function filterGeoJson(fc: GeoJSON.FeatureCollection, opts?: { arcticHint?: boolean }): {
  accepted: GeoJSON.FeatureCollection;
  quarantine: GeoJSON.FeatureCollection;
  stats: FilterStats;
} {
  // implement per table above; keep pure + side-effect free for OSS reuse
  throw new Error('implement in PR — see help-wanted issues');
}
```

PRs welcome that ship a tested `filterGeoJson` under `dataset/` or a tiny `packages/geo-filter` later.


## People / event pins (`filterPeoplePins`)

Import `@international-arctic/geo-filter/people`.

Reasons: `missing_coords`, `nan_coords`, `null_island`, `sentinel_coords` (999/9999 or exact `(1,1)` / axis-unit junk), `swapped_lat_lng` (|lat|>90 while |lng|≤90), `out_of_bounds`, `duplicate_slug`, `duplicate_point`.

Also accepts GeoJSON `geometry: { type: "Point", coordinates: [lng, lat] }`, nested `location.{lat,lng|lon|longitude}`, and `x`/`y` aliases (2026-09-22 ~11:20 MSK).

Also exported: `filterEventPins` (same rules) for venue pins. Do not use high-latitude heuristics — Nordic / Arctic HQ pins are valid.

## Centroid-clone quarantine (2026-09-14)

Ports stamped `geo_quality: centroid_clone` (exact city pin match) are quarantined client-side by default (`quarantineCentroidClones`). Fallback: proposed/planned ports sharing a city pin at 3 decimal places. See [CENTROID-CLONE-QUARANTINE-2026-09-14.md](./CENTROID-CLONE-QUARANTINE-2026-09-14.md).

## People filter quarantine accumulate (2026-09-14 ~17:57 MSK)

`filterPeoplePins` / `filterEventPins` now always return `quarantine: []` and accept optional `accumulateQuarantine: true` to fill dropped pins with `{ pin, reason }` for QA — default callers that only use `.accepted` / `.stats` are unchanged. Live UnicornsMap.com bundle already drops null-island / OOB / swap / dupes (no SPA redeploy this cycle).

## CI (2026-09-15)

```bash
bun scripts/check-people-event-pin-filter.mjs
node scripts/check-centroid-clone-remaining.mjs dataset/atlas.4326.geojson
node scripts/check-shipyard-city-stack.mjs dataset/atlas.4326.geojson
```

Shipped after Issue #32 hard-port re-check found no verifiable OSM densify for Obskaya/Chevak/Steensby. People/event smoke covers UnicornsMap pin QA without SPA redeploy.
