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

Reasons: `missing_coords`, `nan_coords`, `null_island`, `swapped_lat_lng` (|lat|>90 while |lng|≤90), `out_of_bounds`, `duplicate_slug`, `duplicate_point`.

Also exported: `filterEventPins` (same rules) for venue pins. Do not use high-latitude heuristics — Nordic / Arctic HQ pins are valid.
