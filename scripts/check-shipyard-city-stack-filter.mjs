#!/usr/bin/env bun
/**
 * Assert client filterGeoJson quarantines the locked shipyard↔city centroid_clone.
 * Usage: bun scripts/check-shipyard-city-stack-filter.mjs [atlas.4326.geojson]
 */
import { readFileSync } from 'node:fs';
import { filterGeoJson } from '../packages/geo-filter/src/filterGeoJson.ts';

const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const { quarantine, stats } = filterGeoJson(g, { quarantineCentroidClones: true });
const qIds = new Set(
  (quarantine.features || [])
    .filter((f) => (f.properties || {}).reason === 'centroid_clone')
    .map((f) => (f.properties || {}).id),
);

const need = ['ARC-SHIP-069', 'ARC-PORT-034', 'ARC-PORT-069', 'ARC-PORT-153'];
const missing = need.filter((id) => !qIds.has(id));
if (missing.length) {
  console.error('filterGeoJson failed to quarantine:', missing.join(', '), 'stats', stats);
  process.exit(1);
}
console.log('check-shipyard-city-stack-filter: pass quarantined', need.join(', '), 'reasons', stats.reasons);
