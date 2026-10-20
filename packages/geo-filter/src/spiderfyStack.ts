/**
 * 0.1.8: spiderfy-on-click + "approximate location" flag for shared-point pins. Apache-2.0
 *
 * Alternative to `unstackSharedPoints` (0.1.6) for viewers that prefer NOT to move pins:
 * true coordinates are never rewritten. Stacks stay as one marker until the user clicks/expands
 * them; `spiderfyLegs` then lays the members out on a circle (small stacks) or an Archimedean
 * spiral (large stacks) in screen-pixel space at the current zoom, so legs are readable at any
 * zoom and collapse back onto the true point. Framework-free: works with MapLibre, Leaflet,
 * OpenLayers or a plain <canvas>. Display-only and data-neutral (geometry/display only).
 */
import type { PeoplePinLike } from './filterPeoplePins.ts';

export type SharedPointStack = {
  /** Exact shared point [lng, lat] (as served). */
  anchor: [number, number];
  /** Indices into the input array, stable order by slug. */
  members: number[];
  size: number;
};

function pinLonLat(p: any): [number, number] | null {
  if (!p) return null;
  const g = p.geometry;
  if (g && g.type === 'Point' && Array.isArray(g.coordinates)) {
    const [x, y] = g.coordinates;
    if (Number.isFinite(x) && Number.isFinite(y)) return [x, y];
  }
  const lng = p.lng ?? p.lon ?? (Array.isArray(p.coords) ? p.coords[0] : undefined);
  const lat = p.lat ?? (Array.isArray(p.coords) ? p.coords[1] : undefined);
  if (Number.isFinite(lng) && Number.isFinite(lat)) return [Number(lng), Number(lat)];
  return null;
}

function slugOf(p: any, i: number): string {
  return String(p?.slug ?? p?.properties?.slug ?? i);
}

/** Group pins that share one exact point (within `eps` degrees, default 1e-5 ≈ 1 m). */
export function groupSharedPoints<T extends PeoplePinLike>(pins: T[], opts?: { eps?: number; minSize?: number }): SharedPointStack[] {
  const eps = opts?.eps ?? 1e-5;
  const minSize = opts?.minSize ?? 2;
  const buckets = new Map<string, { anchor: [number, number]; members: number[] }>();
  (pins || []).forEach((p, i) => {
    const pt = pinLonLat(p);
    if (!pt) return;
    const k = `${Math.round(pt[0] / eps)}|${Math.round(pt[1] / eps)}`;
    const b = buckets.get(k) || { anchor: pt, members: [] };
    b.members.push(i);
    buckets.set(k, b);
  });
  const out: SharedPointStack[] = [];
  for (const b of buckets.values()) {
    if (b.members.length < minSize) continue;
    b.members.sort((a, c) => slugOf(pins[a], a).localeCompare(slugOf(pins[c], c)));
    out.push({ anchor: b.anchor, members: b.members, size: b.members.length });
  }
  return out.sort((a, b) => b.size - a.size || a.anchor[0] - b.anchor[0] || a.anchor[1] - b.anchor[1]);
}

export type ApproxFlagOptions = {
  eps?: number;
  /**
   * Stacks of at least this many distinct pins are treated as a shared fallback point
   * (city centroid, HQ approximation, venue fallback). Default 3: two people at one office
   * can be a real shared address; three or more on one 4–5 decimal point almost never are.
   */
  minStack?: number;
};

/**
 * Adds display hints without touching coordinates (shallow copies):
 * - `location_precision`: 'shared_point' for members of a stack >= minStack, else 'point'
 * - `approximate_location`: true for shared_point members (UI can say "approximate location")
 * - `shared_point_size`: stack size (1 for singletons)
 * GeoJSON features get the hints in `properties`; flat pins get them at top level.
 */
export function flagApproximateLocations<T extends PeoplePinLike>(pins: T[], opts?: ApproxFlagOptions) {
  const minStack = opts?.minStack ?? 3;
  const stacks = groupSharedPoints(pins, { eps: opts?.eps, minSize: 2 });
  const size = new Map<number, number>();
  for (const s of stacks) for (const i of s.members) size.set(i, s.size);
  let flagged = 0;
  const out = (pins || []).map((p: any, i) => {
    if (!pinLonLat(p)) return p;
    const n = size.get(i) ?? 1;
    const approx = n >= minStack;
    if (approx) flagged++;
    const meta = {
      location_precision: approx ? 'shared_point' : 'point',
      approximate_location: approx,
      shared_point_size: n,
    };
    if (p.geometry && p.geometry.type === 'Point') return { ...p, properties: { ...(p.properties || {}), ...meta } };
    return { ...p, ...meta };
  }) as T[];
  return { pins: out, stacks, stats: { pins: out.length, flagged, stacks: stacks.length, stacksAtOrAboveMin: stacks.filter((s) => s.size >= minStack).length } };
}

export type SpiderfyOptions = {
  /** Map zoom (Web Mercator, 512 px tiles as in MapLibre). */
  zoom: number;
  tileSize?: number;
  /** Members up to this count go on a single circle; more use a spiral. Default 9. */
  circleMax?: number;
  /** Min pixel spacing between neighbouring legs. Default 28 px (fits a 24 px marker). */
  legPx?: number;
  /** Spiral growth per turn in px. Default max(legPx, 30) so turns never overlap. */
  spiralPx?: number;
};

const D2R = Math.PI / 180;

function project([lng, lat]: [number, number], scale: number): [number, number] {
  const s = Math.sin(Math.max(-85.0511, Math.min(85.0511, lat)) * D2R);
  return [((lng + 180) / 360) * scale, (0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI)) * scale];
}

function unproject([x, y]: [number, number], scale: number): [number, number] {
  const lng = (x / scale) * 360 - 180;
  const n = Math.PI - (2 * Math.PI * y) / scale;
  const lat = (180 / Math.PI) * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n)));
  return [Number(lng.toFixed(7)), Number(lat.toFixed(7))];
}

/**
 * Pixel offsets for n spider legs around (0,0). Circle for n <= circleMax (circumference sized
 * so neighbours are >= legPx apart), Archimedean spiral above (markercluster-style), deterministic.
 */
export function spiderfyOffsetsPx(n: number, opts?: Omit<SpiderfyOptions, 'zoom'>): [number, number][] {
  const circleMax = opts?.circleMax ?? 9;
  const legPx = opts?.legPx ?? 28;
  const spiralPx = opts?.spiralPx ?? Math.max(legPx, 30);
  const out: [number, number][] = [];
  if (n <= 0) return out;
  if (n === 1) return [[0, 0]];
  if (n <= circleMax) {
    const r = Math.max(legPx, (legPx * n) / (2 * Math.PI));
    const start = -Math.PI / 2; // first leg straight up (north)
    for (let i = 0; i < n; i++) {
      const a = start + (i * 2 * Math.PI) / n;
      out.push([r * Math.cos(a), r * Math.sin(a)]);
    }
    return out;
  }
  // Archimedean spiral: r grows by spiralPx per turn, arc step ~= legPx.
  let angle = 0;
  let r = legPx;
  const b = spiralPx / (2 * Math.PI);
  for (let i = 0; i < n; i++) {
    out.push([r * Math.cos(angle - Math.PI / 2), r * Math.sin(angle - Math.PI / 2)]);
    angle += legPx / r;
    r = legPx + b * angle;
  }
  return out;
}

/**
 * Display positions [lng, lat] for the members of one stack at the given zoom.
 * Only for drawing the expanded stack + leg lines; the pins' own coordinates are untouched.
 */
export function spiderfyLegs(anchor: [number, number], n: number, opts: SpiderfyOptions): [number, number][] {
  const scale = (opts.tileSize ?? 512) * Math.pow(2, opts.zoom);
  const [cx, cy] = project(anchor, scale);
  return spiderfyOffsetsPx(n, opts).map(([dx, dy]) => unproject([cx + dx, cy + dy], scale));
}

/**
 * Convenience: GeoJSON FeatureCollection of leg end points (with the member's properties plus
 * `spider_anchor`, `spider_index`) and leg LineStrings, ready for a MapLibre source on click.
 */
export function spiderfyStackGeoJson<T extends PeoplePinLike>(pins: T[], stack: SharedPointStack, opts: SpiderfyOptions) {
  const legs = spiderfyLegs(stack.anchor, stack.size, opts);
  const features: any[] = [];
  stack.members.forEach((pi, i) => {
    const src: any = pins[pi];
    const props = { ...(src?.properties || src || {}), spider_anchor: stack.anchor, spider_index: i, spider_size: stack.size };
    delete props.geometry;
    features.push({ type: 'Feature', geometry: { type: 'Point', coordinates: legs[i] }, properties: { ...props, spider_role: 'leg_end' } });
    features.push({ type: 'Feature', geometry: { type: 'LineString', coordinates: [stack.anchor, legs[i]] }, properties: { slug: props.slug, spider_role: 'leg_line' } });
  });
  return { type: 'FeatureCollection', features };
}
