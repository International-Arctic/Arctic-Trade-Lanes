#!/usr/bin/env node
/** Run every scripts/check* lock with the repository's local atlas inputs. */
import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(repoRoot);

const atlas4326 = resolve('atlas.4326.geojson');
const atlasWgs84 = resolve('atlas.wgs84.geojson');
const atlas3996 = resolve('atlas.3996.geojson');
const manifest = resolve('atlas.manifest.json');

const jsArgs = new Map([
  ['check-city-airport-dedupe.mjs', [atlas4326]],
  ['check-extra-ids.mjs', ['--geojson', atlas4326, '--layer', 'airports']],
  ['check-facility-dedupe.mjs', [atlas4326]],
  ['check-lane-teleport.mjs', [atlas4326, manifest]],
  ['check-lane-waypoints.mjs', [manifest]],
  ['check-port-city-centroid-densify.mjs', [atlas4326]],
  ['check-port-iso2.mjs', [atlas4326]],
  ['check-program-seat-stack.mjs', [atlas4326]],
  ['check-reference-rings.mjs', [atlasWgs84, atlas3996]],
  ['check-ship-fleet.mjs', [atlas4326]],
  ['check-shipyard-column-shift.mjs', [atlas4326]],
  ['check-shipyard-pins.mjs', [atlas4326]],
  ['check-vardo-city-port-dedupe.mjs', [atlas4326]],
]);

const checks = readdirSync('scripts')
  .filter((name) => /^check.*\.mjs$/.test(name))
  .sort();

if (!checks.length) throw new Error('No scripts/check* files were found.');
for (const path of [atlas4326, atlasWgs84, atlas3996, manifest]) {
  if (!existsSync(path)) throw new Error(`Required quality-check input is missing: ${path}`);
}

const failed = [];
for (const name of checks) {
  const script = join('scripts', name);
  const command = process.execPath;
  const args = ['--import', 'tsx', script, ...(jsArgs.get(name) || [])];

  console.log(`\n=== ${script} ===`);
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    env: process.env,
    stdio: 'inherit',
    timeout: 5 * 60_000,
  });
  if (result.error || result.status !== 0) {
    failed.push(name);
    console.error(`FAILED ${script}${result.error ? `: ${result.error.message}` : ` (exit ${result.status ?? 'unknown'})`}`);
  }
}

console.log(`\nRan ${checks.length} checks; ${failed.length} failed.`);
if (failed.length) {
  console.error(`Failed checks: ${failed.join(', ')}`);
  process.exitCode = 1;
}
