/**
 * Client-side country normalisation for people/org/event pins (UnicornsMap $UM-Radar, ATL). Apache-2.0
 *
 * Problem (live 2026-10-05): /api/radar/geojson.json derives `country` as the last comma part of
 * `city`, so "Seoul" -> country "Seoul", "New York, NY" -> "NY", "San Francisco, CA" -> "CA"
 * (California, not Canada), and free-text notes leak in ("USA — Hugging Face HQ (...)").
 * 198 of 600 primaries had country === locality; 81 distinct country strings for ~45 countries.
 *
 * This resolves every pin to an ISO 3166-1 alpha-2 code (`countryIso2`) with a provenance tag
 * (`country_quality`). Display names are left to the client (`Intl.DisplayNames`) so each locale
 * renders its own name and no editorial label is baked into the data. Neutral by construction:
 * the only reference is the ISO 3166-1 code list; nothing is inferred from politics or opinion.
 * Additive: the raw `country` field is never overwritten.
 */
export type CountryQuality =
  | 'iso_or_name'      // raw country is a recognised ISO code or country name/alias
  | 'us_state_tail'    // raw tail is a US state code (NY, CA, TX...) in "City, ST"
  | 'city_gazetteer'   // raw tail was a city / city-state name (Seoul, Singapore, Dubai...)
  | 'multi_city_first' // "A / B" multi-seat string; resolved from the first resolvable token
  | 'unresolved';

export type CountryResult = { iso2: string | null; quality: CountryQuality; raw: string };

const NAMES: Record<string, string> = {
  'usa': 'US', 'us': 'US', 'united states': 'US', 'united states of america': 'US', 'u.s.': 'US', 'u.s.a.': 'US',
  'uk': 'GB', 'gb': 'GB', 'united kingdom': 'GB', 'great britain': 'GB', 'england': 'GB', 'scotland': 'GB',
  'uae': 'AE', 'ae': 'AE', 'united arab emirates': 'AE',
  'south korea': 'KR', 'korea': 'KR', 'republic of korea': 'KR', 'kr': 'KR',
  'singapore': 'SG', 'sg': 'SG', 'hong kong': 'HK', 'hk': 'HK', 'taiwan': 'TW', 'tw': 'TW',
  'france': 'FR', 'fr': 'FR', 'india': 'IN', 'canada': 'CA', 'greece': 'GR', 'saudi arabia': 'SA', 'ksa': 'SA',
  'spain': 'ES', 'germany': 'DE', 'russia': 'RU', 'russian federation': 'RU', 'japan': 'JP', 'switzerland': 'CH',
  'australia': 'AU', 'ukraine': 'UA', 'poland': 'PL', 'malaysia': 'MY', 'estonia': 'EE', 'lithuania': 'LT',
  'netherlands': 'NL', 'israel': 'IL', 'vietnam': 'VN', 'viet nam': 'VN', 'indonesia': 'ID', 'sweden': 'SE',
  'egypt': 'EG', 'curaçao': 'CW', 'curacao': 'CW', 'ireland': 'IE', 'argentina': 'AR', 'finland': 'FI',
  'türkiye': 'TR', 'turkiye': 'TR', 'turkey': 'TR', 'latvia': 'LV', 'philippines': 'PH', 'thailand': 'TH',
  'denmark': 'DK', 'bahrain': 'BH', 'kenya': 'KE', 'serbia': 'RS', 'brazil': 'BR', 'china': 'CN',
  'colombia': 'CO', 'peru': 'PE', 'portugal': 'PT', 'monaco': 'MC', 'kazakhstan': 'KZ', 'italy': 'IT',
  'norway': 'NO', 'iceland': 'IS', 'greenland': 'GL', 'austria': 'AT', 'belgium': 'BE', 'qatar': 'QA',
  'mexico': 'MX', 'nigeria': 'NG', 'south africa': 'ZA', 'new zealand': 'NZ', 'luxembourg': 'LU',
};

// Unambiguous US state / DC postal codes, used ONLY as the tail of "City, ST" (never as a bare
// country, because CA/IN/DE/ID... are also ISO country codes).
const US_STATES = new Set('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split(' '));


// Full US state names ("Chicago, Illinois"). Georgia and Washington are omitted on purpose:
// both collide with a country / city name.
const US_STATE_NAMES = new Set(["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont", "virginia", "west virginia", "wisconsin", "wyoming"]);

// City (or city-state) -> ISO2 for tails seen without a country part. Extend via `extraCities`.
const CITIES: Record<string, string> = {
  'seoul': 'KR', 'busan': 'KR', 'dubai': 'AE', 'abu dhabi': 'AE', 'new york': 'US', 'new york city': 'US', 'nyc': 'US',
  'san francisco': 'US', 'laguna beach': 'US', 'miami': 'US', 'riyadh': 'SA', 'milan': 'IT', 'amsterdam': 'NL',
  'paris': 'FR', 'astana': 'KZ', 'chongqing': 'CN', 'jakarta': 'ID', 'athens': 'GR', 'bali': 'ID', 'toronto': 'CA',
  'london': 'GB', 'geneva': 'CH', 'zurich': 'CH', 'mumbai': 'IN', 'delhi': 'IN', 'new delhi': 'IN', 'tel aviv': 'IL',
  'kyiv': 'UA', 'taipei': 'TW', 'riga': 'LV', 'frankfurt': 'DE', 'tokyo': 'JP', 'berlin': 'DE', 'moscow': 'RU',
  'murmansk': 'RU', 'tromsø': 'NO', 'tromso': 'NO', 'reykjavik': 'IS', 'nuuk': 'GL', 'anchorage': 'US',
};

function clean(s: string): string {
  return s
    .replace(/\([^)]*\)/g, ' ')        // drop "(reported license domicile)" etc.
    .split(/\s[—–-]\s/)[0]             // drop " — Hugging Face HQ ..." notes
    .replace(/\s+/g, ' ')
    .trim();
}

function lookupToken(tok: string, extra?: Record<string, string>): { iso2: string; q: CountryQuality } | null {
  const t = clean(tok);
  if (!t) return null;
  const low = t.toLowerCase();
  if (NAMES[low]) return { iso2: NAMES[low], q: 'iso_or_name' };
  if (extra && extra[low]) return { iso2: extra[low], q: 'city_gazetteer' };
  if (CITIES[low]) return { iso2: CITIES[low], q: 'city_gazetteer' };
  if (US_STATE_NAMES.has(low)) return { iso2: 'US', q: 'us_state_tail' };
  // "Hawthorne CA" / "Kent WA" inside multi-seat strings
  const m = t.match(/\b([A-Z]{2})$/);
  if (m && US_STATES.has(m[1]) && t.length > 2) return { iso2: 'US', q: 'us_state_tail' };
  return null;
}

/** Resolve one pin's country. Reads `country`, then the tail of `city`, then `locality`. */
export function resolveCountry(
  p: { country?: unknown; city?: unknown; locality?: unknown; properties?: Record<string, unknown> },
  opts?: { extraCities?: Record<string, string> },
): CountryResult {
  const src = (p && (p as any).properties) || p || {};
  const raw = String(src.country ?? '').trim();
  // "Wyoming, USA (public HQ) · Dubai, UAE": the pin sits on the FIRST seat, so only read that one.
  const city = String(src.city ?? '').split(/\s+[·•|]\s+/)[0].trim();
  const extra = opts?.extraCities
    ? Object.fromEntries(Object.entries(opts.extraCities).map(([k, v]) => [k.toLowerCase(), v.toUpperCase()]))
    : undefined;

  const cityParts = city.split(',').map((s) => s.trim()).filter(Boolean);
  const tail = cityParts.length > 1 ? clean(cityParts[cityParts.length - 1]) : '';

  // 1) "City, ST" US state tail beats a bare 2-letter country read (CA = California here).
  const tailHead = tail.split(/\s*\/\s*/)[0];
  if (tailHead && US_STATES.has(tailHead.toUpperCase()) && tailHead.length === 2 && tailHead === tailHead.toUpperCase()) {
    return { iso2: 'US', quality: 'us_state_tail', raw };
  }
  // 2) Multi-seat city strings: the first seat's own country part wins over the worker's tail.
  if (String(src.city ?? '').match(/\s+[·•|]\s+/) && tail) {
    const hit = lookupToken(tail, extra);
    if (hit) return { iso2: hit.iso2, quality: 'multi_city_first', raw };
  }
  // 3) Whole raw country (cleaned) as a name/ISO/city.
  for (const cand of [raw, String(src.locality ?? ''), cityParts[0] || '']) {
    if (!cand) continue;
    const parts = clean(cand).split(/\s*\/\s*/).filter(Boolean);
    if (parts.length === 1) {
      const hit = lookupToken(parts[0], extra);
      if (hit) return { iso2: hit.iso2, quality: hit.q, raw };
    } else {
      for (const part of parts) {
        const hit = lookupToken(part, extra);
        if (hit) return { iso2: hit.iso2, quality: 'multi_city_first', raw };
      }
    }
  }
  return { iso2: null, quality: 'unresolved', raw };
}

/**
 * Annotate pins (flat objects or GeoJSON Features) with `countryIso2` + `country_quality`.
 * Returns shallow copies; never mutates input; never overwrites `country`.
 */
export function normalizePinCountries<T extends Record<string, any>>(
  pins: T[],
  opts?: { extraCities?: Record<string, string> },
): { pins: T[]; stats: { total: number; resolved: number; byQuality: Record<string, number>; unresolvedRaw: Record<string, number> } } {
  const byQuality: Record<string, number> = {};
  const unresolvedRaw: Record<string, number> = {};
  let resolved = 0;
  const out = (pins || []).map((pin) => {
    const r = resolveCountry(pin, opts);
    byQuality[r.quality] = (byQuality[r.quality] || 0) + 1;
    if (r.iso2) resolved++; else unresolvedRaw[r.raw || '(empty)'] = (unresolvedRaw[r.raw || '(empty)'] || 0) + 1;
    const add = { countryIso2: r.iso2, country_quality: r.quality };
    if (pin && pin.type === 'Feature' && pin.properties) {
      return { ...pin, properties: { ...pin.properties, ...add } } as T;
    }
    return { ...pin, ...add } as T;
  });
  return { pins: out, stats: { total: out.length, resolved, byQuality, unresolvedRaw } };
}
