#!/usr/bin/env bun
/**
 * UnicornsMap $UM-Radar people/org/event pin QA (packages/geo-filter 0.1.6).
 *
 * 1) Fixture asserts (offline, CI-safe):
 *    - siteAware dedupe keeps real multi-site locations, drops a site that sits on its own primary.
 *    - unstackSharedPoints fans every exact shared-point stack, keeps position_anchor, leaves singletons.
 * 2) Optional live audit (`--live`): fetches https://unicornsmap.com/api/radar/geo.json and
 *    /api/radar/geojson.json and prints stack / dup / country-field metrics. Never fails CI on live drift.
 *
 * Usage: bun scripts/check-um-geo-quality.mjs [--live]
 */
import { filterPeoplePins, unstackSharedPoints } from '../packages/geo-filter/src/filterPeoplePins.ts';

let failed = 0;
const fail = (...a) => { console.error('FAIL', ...a); failed++; };
const key = (lng, lat) => `${Math.round(lng * 1e5)}|${Math.round(lat * 1e5)}`;

// --- fixture 1: siteAware dedupe on a primary+site GeoJSON feed --------------------------------
const F = (slug, kind, lng, lat, extra = {}) => ({
  type: 'Feature', geometry: { type: 'Point', coordinates: [lng, lat] },
  properties: { slug, name: slug, kind, ...extra },
});
const feed = [
  F('joe', 'primary', 126.92663, 37.52539),
  F('joe', 'site', 126.92663, 37.52539, { label: 'Event' }),            // same point as its primary -> drop
  F('tesla', 'primary', -97.62, 30.22),
  F('tesla', 'site', -121.94, 37.49, { label: 'Fremont factory' }),     // real second site -> keep
  F('tesla', 'site', -121.94, 37.49, { label: 'Fremont factory' }),     // exact repeat -> drop
  F('ghost', 'primary', 0, 0),                                          // null island -> drop
];
const legacy = filterPeoplePins(feed);
const aware = filterPeoplePins(feed, { siteAware: true, accumulateQuarantine: true });
if (legacy.stats.accepted !== 2) fail('legacy accepted want 2 (sites lost to duplicate_slug) got', legacy.stats.accepted);
if (aware.stats.accepted !== 3) fail('siteAware accepted want 3 got', aware.stats.accepted, aware.quarantine.map((q) => q.reason));
if ((aware.stats.reasons.site_coincident_with_primary || 0) !== 1) fail('want 1 site_coincident_with_primary', aware.stats.reasons);
if ((aware.stats.reasons.duplicate_slug || 0) !== 1) fail('want 1 duplicate_slug (repeat site)', aware.stats.reasons);
if ((aware.stats.reasons.null_island || 0) !== 1) fail('want 1 null_island', aware.stats.reasons);

// --- fixture 2: shared-point fan on flat pins ------------------------------------------------
const flat = [
  ...Array.from({ length: 74 }, (_, i) => ({ slug: `nyc-${String(i).padStart(2, '0')}`, lat: 40.7128, lng: -74.006 })),
  { slug: 'solo', lat: 59.33, lng: 18.07 },
];
const fanned = unstackSharedPoints(flat);
const seen = new Set();
let maxKm = 0;
for (const p of fanned) {
  const lat = p.display_lat ?? p.lat, lng = p.display_lng ?? p.lng;
  seen.add(key(lng, lat));
  if (p.position_anchor) {
    const [alng, alat] = p.position_anchor;
    if (alng !== p.lng || alat !== p.lat) fail('anchor must equal untouched true lat/lng', p.slug);
    const dy = (lat - alat) * 111.32, dx = (lng - alng) * 111.32 * Math.cos((alat * Math.PI) / 180);
    maxKm = Math.max(maxKm, Math.hypot(dx, dy));
  }
}
if (seen.size !== fanned.length) fail('fan left stacked pins', fanned.length - seen.size);
if (maxKm > 5) fail('fan radius too wide km', maxKm.toFixed(2));
const solo = fanned.find((p) => p.slug === 'solo');
if (solo.position_quality || solo.display_lat != null) fail('singleton must pass through untouched');
const again = unstackSharedPoints(flat);
if (JSON.stringify(again) !== JSON.stringify(fanned)) fail('fan must be deterministic');

// --- fixture 3: GeoJSON feature fan keeps anchor in properties --------------------------------
const gj = unstackSharedPoints([F('a', 'primary', 2.3522, 48.8566), F('b', 'primary', 2.3522, 48.8566)]);
if (!gj.every((f) => f.properties.position_quality === 'shared_point_fan' && f.properties.position_anchor[0] === 2.3522)) fail('geojson fan meta');
if (key(...gj[0].geometry.coordinates) === key(...gj[1].geometry.coordinates)) fail('geojson fan still stacked');

console.log(failed ? `check-um-geo-quality: ${failed} FAIL` : `check-um-geo-quality: fixtures OK (fan max ${maxKm.toFixed(2)} km)`);

// --- optional live audit ------------------------------------------------------------------------
if (process.argv.includes('--live')) {
  const stackStats = (pts) => {
    const m = new Map();
    for (const [lng, lat] of pts) { const k = key(lng, lat); m.set(k, (m.get(k) || 0) + 1); }
    const st = [...m.values()].filter((n) => n > 1);
    return { stacks: st.length, stacked: st.reduce((a, b) => a + b, 0), biggest: Math.max(0, ...st) };
  };
  try {
    const geo = await (await fetch('https://unicornsmap.com/api/radar/geo.json')).json();
    const pins = geo.pins || [];
    const before = stackStats(pins.map((p) => [p.lng, p.lat]));
    const fan = unstackSharedPoints(pins);
    const after = stackStats(fan.map((p) => [p.display_lng ?? p.lng, p.display_lat ?? p.lat]));
    console.log('live geo.json pins', pins.length, 'before', before, 'after fan', after);
  } catch (e) { console.log('live geo.json skipped:', String(e)); }
  try {
    const fc = await (await fetch('https://unicornsmap.com/api/radar/geojson.json')).json();
    const pts = (fc.features || []).filter((f) => f.geometry?.type === 'Point');
    const legacyLive = filterPeoplePins(pts);
    const awareLive = filterPeoplePins(pts, { siteAware: true });
    const countryIsCity = pts.filter((f) => f.properties.kind === 'primary' && f.properties.country && f.properties.country === f.properties.locality).length;
    console.log('live geojson features', pts.length,
      '| legacy filter keeps', legacyLive.stats.accepted, legacyLive.stats.reasons,
      '| siteAware keeps', awareLive.stats.accepted, awareLive.stats.reasons,
      '| primary rows with country === locality', countryIsCity);
  } catch (e) { console.log('live geojson.json skipped:', String(e)); }
}
process.exit(failed ? 1 : 0);
