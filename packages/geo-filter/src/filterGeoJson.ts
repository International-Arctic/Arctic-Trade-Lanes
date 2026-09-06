/** Pure client-side GeoJSON QA — International-Arctic/Arctic-Trade-Lanes packages/geo-filter */
export type FilterStats = { accepted: number; quarantined: number; reasons: Record<string, number> };
export type FilterOptions = {
  arcticHint?: boolean;
  nullIslandEps?: number;
  dupPointEps?: number;
  unstackSchematic?: boolean;
  unstackRadiusDeg?: number;
  arcticLayers?: string[];
};

const DEFAULT_ARCTIC_LAYERS = ['ports','port','tankers','icebreakers','lanes','shipyards','rescue','airports'];

function bump(reasons: Record<string, number>, reason: string) {
  reasons[reason] = (reasons[reason] || 0) + 1;
}

function firstLonLat(geom: any): [number, number] | null {
  if (!geom || geom.coordinates == null) return null;
  const walk = (c: any): [number, number] | null => {
    if (!Array.isArray(c) || c.length === 0) return null;
    if (typeof c[0] === 'number' && typeof c[1] === 'number') return [c[0], c[1]];
    return walk(c[0]);
  };
  return walk(geom.coordinates);
}

function layerOf(f: any): string {
  const p = f.properties || {};
  return String(p.layer || p.type || p.kind || 'unknown');
}

function featureId(f: any): string | null {
  if (f.id != null && String(f.id).length) return String(f.id);
  const p = f.properties || {};
  for (const k of ['id', 'fid', 'feature_id', 'uuid', 'slug']) {
    if (p[k] != null && String(p[k]).length) return String(p[k]);
  }
  return null;
}

export function schematicOffset(lon: number, lat: number, index: number, total: number, radiusDeg = 0.28): [number, number] {
  const golden = 2.399963229728653;
  const ang = index * golden;
  const r = radiusDeg * Math.sqrt((index + 1) / Math.max(total, 1));
  const dlat = r * Math.cos(ang);
  const cosLat = Math.max(Math.cos((lat * Math.PI) / 180), 0.2);
  const dlon = (r * Math.sin(ang)) / cosLat;
  return [lon + dlon, lat + dlat];
}

export function filterGeoJson(fc: any, opts: FilterOptions = {}) {
  const nullEps = opts.nullIslandEps ?? 1e-4;
  const dupEps = opts.dupPointEps ?? 1e-5;
  const arcticLayers = new Set(opts.arcticLayers || DEFAULT_ARCTIC_LAYERS);
  const reasons: Record<string, number> = {};
  const accepted: any[] = [];
  const quarantine: any[] = [];
  const seenIds = new Set<string>();
  const seenPoints = new Set<string>();
  const stackBuckets = new Map<string, any[]>();
  const features = Array.isArray(fc?.features) ? fc.features : [];

  for (const raw of features) {
    if (!raw || raw.type !== 'Feature') {
      bump(reasons, 'invalid_feature');
      quarantine.push({ type: 'Feature', geometry: null, properties: { reason: 'invalid_feature' } });
      continue;
    }
    const pt = firstLonLat(raw.geometry);
    if (!pt) {
      bump(reasons, 'missing_coords');
      quarantine.push({ ...raw, properties: { ...(raw.properties || {}), reason: 'missing_coords' } });
      continue;
    }
    const [lon, lat] = pt;
    if (!Number.isFinite(lon) || !Number.isFinite(lat)) {
      bump(reasons, 'nan_coords');
      quarantine.push({ ...raw, properties: { ...(raw.properties || {}), reason: 'nan_coords' } });
      continue;
    }
    if (Math.abs(lon) <= nullEps && Math.abs(lat) <= nullEps) {
      bump(reasons, 'null_island');
      quarantine.push({ ...raw, properties: { ...(raw.properties || {}), reason: 'null_island' } });
      continue;
    }
    if (Math.abs(lat) > 90 || Math.abs(lon) > 180) {
      bump(reasons, 'out_of_bounds');
      quarantine.push({ ...raw, properties: { ...(raw.properties || {}), reason: 'out_of_bounds' } });
      continue;
    }
    const layer = layerOf(raw);
    const id = featureId(raw);
    if (id) {
      const idKey = `${layer}::${id}`;
      if (seenIds.has(idKey)) {
        bump(reasons, 'duplicate_id');
        quarantine.push({ ...raw, properties: { ...(raw.properties || {}), reason: 'duplicate_id' } });
        continue;
      }
      seenIds.add(idKey);
    }
    const qLon = Math.round(lon / dupEps) * dupEps;
    const qLat = Math.round(lat / dupEps) * dupEps;
    const pointKey = `${layer}|${qLon}|${qLat}`;
    const name = String((raw.properties || {}).name || '');
    const namePointKey = `${pointKey}|${name.toLowerCase()}`;
    if (seenPoints.has(namePointKey)) {
      bump(reasons, 'duplicate_point');
      quarantine.push({ ...raw, properties: { ...(raw.properties || {}), reason: 'duplicate_point' } });
      continue;
    }
    seenPoints.add(namePointKey);

    const southReview = Boolean(opts.arcticHint && arcticLayers.has(layer) && lat < 50);
    if (southReview) bump(reasons, 'arctic_review_tagged');
    const tagged = southReview
      ? { ...raw, properties: { ...(raw.properties || {}), position_review: 'south_of_50n' } }
      : raw;

    if (opts.unstackSchematic && ['tankers', 'icebreakers', 'ships', 'vessel'].includes(layer)) {
      const bucket = stackBuckets.get(pointKey) || [];
      bucket.push(tagged);
      stackBuckets.set(pointKey, bucket);
      continue;
    }
    accepted.push(tagged);
  }

  if (opts.unstackSchematic) {
    const radius = opts.unstackRadiusDeg ?? 0.28;
    for (const [, bucket] of stackBuckets) {
      const n = bucket.length;
      bucket.forEach((f, i) => {
        const pt = firstLonLat(f.geometry)!;
        if (n === 1) { accepted.push(f); return; }
        const [olon, olat] = schematicOffset(pt[0], pt[1], i, n, radius);
        accepted.push({
          ...f,
          geometry: { type: 'Point', coordinates: [Number(olon.toFixed(6)), Number(olat.toFixed(6))] },
          properties: {
            ...(f.properties || {}),
            position_quality: 'schematic_route_anchor',
            position_stack_size: n,
            position_stack_index: i,
            position_anchor: [pt[0], pt[1]],
          },
        });
        bump(reasons, 'schematic_unstacked');
      });
    }
  }

  return {
    accepted: { type: 'FeatureCollection', features: accepted },
    quarantine: { type: 'FeatureCollection', features: quarantine },
    stats: { accepted: accepted.length, quarantined: quarantine.length, reasons } as FilterStats,
  };
}

export function filterGeoJsonAccepted(fc: any, opts?: FilterOptions) {
  return filterGeoJson(fc, { unstackSchematic: true, ...opts }).accepted;
}
