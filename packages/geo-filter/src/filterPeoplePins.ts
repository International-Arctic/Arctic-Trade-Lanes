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

function bump(r: Record<string, number>, k: string) { r[k] = (r[k] || 0) + 1; }

function lonLat(p: PeoplePinLike): [number, number] | null {
  if (Array.isArray(p.coords) && p.coords.length >= 2) {
    const [lng, lat] = p.coords;
    if (Number.isFinite(lng) && Number.isFinite(lat)) return [lng, lat];
  }
  const lng = (p.lng ?? p.lon) as number | undefined;
  if (Number.isFinite(lng as number) && Number.isFinite(p.lat as number)) return [lng as number, p.lat as number];
  return null;
}

/** Classic swap: latitude field holds a longitude (|lat| > 90) while lng still looks like a latitude. */
function looksSwapped(lng: number, lat: number): boolean {
  return Math.abs(lat) > 90 && Math.abs(lng) <= 90;
}

/** Drop null-island / OOB / NaN / lat-lng swap / exact slug+coord dupes. Soft-dedupe identical name+point. */
export function filterPeoplePins<T extends PeoplePinLike>(pins: T[], opts?: { eps?: number }): { accepted: T[]; stats: PeopleFilterStats } {
  const eps = opts?.eps ?? 1e-5;
  const reasons: Record<string, number> = {};
  const accepted: T[] = [];
  const seenSlug = new Set<string>();
  const seenPoint = new Set<string>();

  for (const pin of pins || []) {
    const pt = lonLat(pin);
    if (!pt) { bump(reasons, 'missing_coords'); continue; }
    const [lng, lat] = pt;
    if (!Number.isFinite(lng) || !Number.isFinite(lat)) { bump(reasons, 'nan_coords'); continue; }
    if (Math.abs(lng) <= 1e-4 && Math.abs(lat) <= 1e-4) { bump(reasons, 'null_island'); continue; }
    if (looksSwapped(lng, lat)) { bump(reasons, 'swapped_lat_lng'); continue; }
    if (Math.abs(lat) > 90 || Math.abs(lng) > 180) { bump(reasons, 'out_of_bounds'); continue; }

    const slug = String(pin.slug || '').toLowerCase();
    if (slug) {
      if (seenSlug.has(slug)) { bump(reasons, 'duplicate_slug'); continue; }
      seenSlug.add(slug);
    }
    const name = String(pin.name || '').toLowerCase();
    const qLng = Math.round(lng / eps) * eps;
    const qLat = Math.round(lat / eps) * eps;
    const key = `${name}|${qLng}|${qLat}`;
    if (seenPoint.has(key)) { bump(reasons, 'duplicate_point'); continue; }
    seenPoint.add(key);
    accepted.push(pin);
  }

  return {
    accepted,
    stats: { accepted: accepted.length, dropped: (pins?.length || 0) - accepted.length, reasons },
  };
}

/** Same QA for event venue pins. */
export function filterEventPins<T extends PeoplePinLike>(pins: T[], opts?: { eps?: number }) {
  return filterPeoplePins(pins, opts);
}
