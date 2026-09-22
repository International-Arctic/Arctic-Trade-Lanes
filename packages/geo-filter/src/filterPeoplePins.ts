/** Client-side people/event pin QA (shared with UnicornsMap $UM-Radar). Apache-2.0 */
export type PeoplePinLike = {
  slug?: string;
  name?: string;
  lat?: number;
  lng?: number;
  lon?: number;
  coords?: [number, number];
  [k: string]: unknown;
};

export type PeopleFilterStats = {
  accepted: number;
  dropped: number;
  reasons: Record<string, number>;
};

export type PeoplePinQuarantine<T extends PeoplePinLike = PeoplePinLike> = {
  pin: T;
  reason: string;
};

export type PeopleFilterOptions = {
  eps?: number;
  /** When true, also return dropped pins with reasons (QA / toggle debug). Default false. */
  accumulateQuarantine?: boolean;
};

function bump(r: Record<string, number>, k: string) { r[k] = (r[k] || 0) + 1; }

function lonLat(p: PeoplePinLike): [number, number] | null {
  // GeoJSON Point (event/people payloads sometimes arrive as Features).
  const geom = (p as any).geometry;
  if (geom && geom.type === 'Point' && Array.isArray(geom.coordinates) && geom.coordinates.length >= 2) {
    const lng = Number(geom.coordinates[0]);
    const lat = Number(geom.coordinates[1]);
    if (Number.isFinite(lng) && Number.isFinite(lat)) return [lng, lat];
  }
  if (Array.isArray(p.coords) && p.coords.length >= 2) {
    const lng = Number(p.coords[0]);
    const lat = Number(p.coords[1]);
    if (Number.isFinite(lng) && Number.isFinite(lat)) return [lng, lat];
  }
  // Nested location / venue blobs used by UnicornsMap event collage feeds.
  const loc = (p as any).location;
  if (loc && typeof loc === 'object') {
    const lng = Number(loc.lng ?? loc.lon ?? loc.longitude ?? loc.x);
    const lat = Number(loc.lat ?? loc.latitude ?? loc.y);
    if (Number.isFinite(lng) && Number.isFinite(lat)) return [lng, lat];
  }
  // Accept common GIS aliases + numeric strings ("60.1") without forcing callers to normalize first.
  const lng = Number(p.lng ?? p.lon ?? (p as any).longitude ?? (p as any).x);
  const lat = Number(p.lat ?? (p as any).latitude ?? (p as any).y);
  if (Number.isFinite(lng) && Number.isFinite(lat)) return [lng, lat];
  return null;
}

/** Scraper / CMS placeholders that survive naive Number() but are not real pins. */
function looksSentinel(lng: number, lat: number): boolean {
  const absL = Math.abs(lat);
  const absG = Math.abs(lng);
  // Classic 999 / 9999 / -999 placeholders (also caught by OOB, but keep an explicit reason).
  if (absL === 999 || absG === 999 || absL === 9999 || absG === 9999) return true;
  // Exact (1,1) / (-1,-1) junk often left by broken geocoders (Gulf of Guinea is never our venue).
  if ((absL === 1 && absG === 1) || (lat === 0 && absG === 1) || (lng === 0 && absL === 1)) return true;
  return false;
}

/**
 * Classic swap: latitude field holds a longitude (|lat| > 90) while lng still looks like a latitude.
 * Do NOT use high-latitude heuristics — Arctic / Nordic HQ pins are valid.
 */
function looksSwapped(lng: number, lat: number): boolean {
  return Math.abs(lat) > 90 && Math.abs(lng) <= 90;
}

/** Drop null-island / OOB / NaN / sentinel / lat-lng swap / exact slug+coord dupes. Soft-dedupe identical name+point. */
export function filterPeoplePins<T extends PeoplePinLike>(
  pins: T[],
  opts?: PeopleFilterOptions,
): { accepted: T[]; stats: PeopleFilterStats; quarantine: PeoplePinQuarantine<T>[] } {
  const eps = opts?.eps ?? 1e-5;
  const accumulate = opts?.accumulateQuarantine === true;
  const reasons: Record<string, number> = {};
  const accepted: T[] = [];
  const quarantine: PeoplePinQuarantine<T>[] = [];
  const seenSlug = new Set<string>();
  const seenPoint = new Set<string>();

  const drop = (pin: T, reason: string) => {
    bump(reasons, reason);
    if (accumulate) quarantine.push({ pin, reason });
  };

  for (const pin of pins || []) {
    const pt = lonLat(pin);
    if (!pt) { drop(pin, 'missing_coords'); continue; }
    const [lng, lat] = pt;
    if (!Number.isFinite(lng) || !Number.isFinite(lat)) { drop(pin, 'nan_coords'); continue; }
    if (looksSentinel(lng, lat)) { drop(pin, 'sentinel_coords'); continue; }
    if (Math.abs(lng) <= 1e-4 && Math.abs(lat) <= 1e-4) { drop(pin, 'null_island'); continue; }
    if (looksSwapped(lng, lat)) { drop(pin, 'swapped_lat_lng'); continue; }
    if (Math.abs(lat) > 90 || Math.abs(lng) > 180) { drop(pin, 'out_of_bounds'); continue; }

    const slug = String(pin.slug || '').toLowerCase();
    if (slug) {
      if (seenSlug.has(slug)) { drop(pin, 'duplicate_slug'); continue; }
      seenSlug.add(slug);
    }
    const name = String(pin.name || '').toLowerCase();
    const qLng = Math.round(lng / eps) * eps;
    const qLat = Math.round(lat / eps) * eps;
    const key = `${name}|${qLng}|${qLat}`;
    if (seenPoint.has(key)) { drop(pin, 'duplicate_point'); continue; }
    seenPoint.add(key);
    accepted.push(pin);
  }

  return {
    accepted,
    stats: { accepted: accepted.length, dropped: (pins?.length || 0) - accepted.length, reasons },
    quarantine,
  };
}

/** Same QA for event venue pins. */
export function filterEventPins<T extends PeoplePinLike>(pins: T[], opts?: PeopleFilterOptions) {
  return filterPeoplePins(pins, opts);
}
