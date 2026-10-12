#!/usr/bin/env node
/**
 * CI: ARC-SHIP-022 VT Halter Marine must stay quarantined (no atlas pin).
 * Same Pascagoula yard as ARC-SHIP-068 Bollinger Mississippi (WD Q29093553 alias).
 * Usage: node scripts/check-ship022-halter-quarantine.mjs [atlas.wgs84.geojson]
 */
import fs from 'node:fs';

const path = process.argv[2] || 'atlas.wgs84.geojson';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const ids = new Set();
for (const f of data.features || []) {
  const id = f.id || (f.properties || {}).id;
  if (id) ids.add(id);
}
const errors = [];
if (ids.has('ARC-SHIP-022')) errors.push('ARC-SHIP-022 should be absent from atlas (duplicate of ARC-SHIP-068)');
if (!ids.has('ARC-SHIP-068')) errors.push('ARC-SHIP-068 Bollinger Mississippi must remain present');
if (errors.length) {
  console.error('ship022 quarantine QA failed:\n' + errors.join('\n'));
  process.exit(1);
}
console.log('OK: ARC-SHIP-022 quarantined; ARC-SHIP-068 present');
