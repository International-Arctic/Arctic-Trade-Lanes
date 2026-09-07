# Airport / extra-layer ID dedupe (2026-09-07)

## Bug

`arctic_airports.csv` carried **two** `ARC-AIR-011` rows for the same Inuvik (YEV/CYEV) AIF modernization pin. Live atlas emitted 12 airport features with a duplicate Feature.id, so the map stacked two near-identical pins and client `filterGeoJson` duplicate_id quarantine could only paper over the dataset debt.

`ARC-AIR-005` (runway + access-road upgrade) remains a **distinct** Inuvik program pin and is kept.

## Fix (Zo control plane)

1. Dataset: keep one `ARC-AIR-011` (higher-confidence / first occurrence); airports `12 → 11`.
2. `build_atlas.py` EXTRA_POINT_LAYERS: skip duplicate `program_id` within each layer; surface skips as `extra_id_drops` on `atlas.manifest.json`.
3. `_feat`: mirror stable ids into `properties.id` so client filters / UI keep working if Feature.id is stripped downstream.
4. Rebuilt atlas synced to `dist/` + `public/` (+ `/data` aliases). Live apex+www: **1344** features, airports **11**, `generated` `2026-09-07T11:12:19Z`.

## CI helper

```bash
node scripts/check-extra-ids.mjs path/to/arctic_airports.csv
# or against a FeatureCollection:
node scripts/check-extra-ids.mjs --geojson path/to/atlas.4326.geojson --layer airports
```

Fails non-zero when any `program_id` / Feature.id repeats inside a layer.

## Community

Good first issue: wire `check-extra-ids.mjs` into GitHub Actions on Dataset + atlas PRs; extend to `industry` / `rail` / `rescue` / `programs`.
