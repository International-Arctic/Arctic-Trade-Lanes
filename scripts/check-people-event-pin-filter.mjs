#!/usr/bin/env bun
/**
 * UM / ATL shared people+event pin QA smoke (packages/geo-filter).
 * No atlas rebuild required — pure client-side filter.
 *
 * Usage: bun scripts/check-people-event-pin-filter.mjs
 */
import {
  filterPeoplePins,
  filterEventPins,
} from '../packages/geo-filter/src/filterPeoplePins.ts';

const fixtures = [
  { slug: 'ok-arctic', name: 'Ok Arctic', lat: 61.5, lng: -165.5 },
  { slug: 'null-island', name: 'Null', lat: 0, lng: 0 },
  { slug: 'dup', name: 'First', lat: 1, lng: 2 },
  { slug: 'dup', name: 'Second', lat: 3, lng: 4 },
  { name: 'swapped', lat: 120, lng: 55 },
  { name: 'oob', lat: 10, lng: 200 },
  { name: 'missing' },
  { name: 'soft', lat: 70.1, lng: 30.1 },
  { name: 'soft', lat: 70.1, lng: 30.1 },
  { slug: 'lon-alias', name: 'Lon alias', latitude: 68.9, longitude: 33.0 },
  { slug: 'string-coords', name: 'String Coords', lat: '69.1', lng: '18.9' },
];

const { accepted, stats, quarantine } = filterPeoplePins(fixtures, {
  accumulateQuarantine: true,
});

const expectReasons = {
  null_island: 1,
  duplicate_slug: 1,
  swapped_lat_lng: 1,
  out_of_bounds: 1,
  missing_coords: 1,
  duplicate_point: 1,
};

let failed = 0;
if (stats.accepted !== 5) {
  console.error('expected accepted=5 (ok-arctic, first dup slug, soft, lon-alias, string-coords), got', stats.accepted, accepted.map((p) => p.slug || p.name));
  failed++;
}
for (const [k, n] of Object.entries(expectReasons)) {
  if ((stats.reasons[k] || 0) !== n) {
    console.error('reason mismatch', k, 'want', n, 'got', stats.reasons[k]);
    failed++;
  }
}
if (quarantine.length !== 6) {
  console.error('quarantine length want 6 got', quarantine.length);
  failed++;
}

// Event alias must behave identically
const ev = filterEventPins(
  [
    { slug: 'evt-ok', lat: 64.1, lng: -21.9 },
    { slug: 'evt-ni', lat: 0, lon: 0 },
  ],
  { accumulateQuarantine: true },
);
if (ev.stats.accepted !== 1 || (ev.stats.reasons.null_island || 0) !== 1) {
  console.error('filterEventPins alias smoke failed', ev.stats);
  failed++;
}

if (failed) process.exit(1);
console.log('check-people-event-pin-filter: pass', stats);
