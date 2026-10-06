# NOTES — ATL MVP build, owner-independent parts (2026-10-06)

Tracking: #60 · Spec: `docs/mvp/ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md` · Zo tip `361dbb0` (on top of `b8c3589`)

## 1. Neutral-content data cleanup (spec §8, owner-approved)
Wording removed from free-text fields only. Geometry, IDs and all other fields are byte-identical (parse-verified). Applied to every live alias (`/`, `/data/`, `/atlas/`, dist, public), to the matching CSV rows, and to the Dataset and OSS copies.

| Object | Field | Change |
|---|---|---|
| ARC-SHIP-073 | arctic_capable | trailing clause about technology access removed |
| ARC-PROG-010 | eligibility | qualifier phrase removed |
| ARC-PROG-201 | eligibility | trailing review clause removed |
| ARC-PROG-273 | benefits | qualifier removed from the supply clause |
| ARC-PROG-339 | eligibility | trailing clause removed |
| ARC-PROG-339 | status | parenthetical qualifier removed |
| ARC-PROG-696 | benefits | parenthetical removed |
| ARC-PROG-716 | benefits | qualifier removed from the local-suppliers clause |
| ARC-FAC-312 | benefits | trailing restructuring phrase removed |
| ARC-FAC-328 | status | qualifier removed |
| ARC-FAC-328 | sources | German-language parenthetical removed (extra hit found by the lint) |
| ARC-FAC-342 | sources | vessel-status qualifier removed |
| ARC-FAC-368 | benefits | wording changed to "approved by Transportstyrelsen" |
| ARC-RAIL-008 | benefits | wording changed to "approved by Transportstyrelsen" |
| atlas.manifest.json | arctic_reference.RU.notes | trailing clause removed |

Lint (`node scripts/lint-neutral.mjs`): 0 hits on the live atlas files and on all generated pages. The term list is stored as salted hashes (`scripts/neutral-terms.sha256.json`); the plaintext list stays private.
Not changed (outside the approved scope, needs an owner decision): 3 `sources` fields in CSV-only rows (ARC-SHIP-049, ARC-PORT-138, ARC-CITY-099) and 4 lines in `info/Latest_Developments_2025_2026_2027.json`.

## 2. Discovery files (spec §5.2, §5.4, §9.4)
- `/.well-known/agent-card.json` + `/.well-known/agent.json` (same file, byte-identical, `application/json`): skills `atlas_lookup` (live), `lane_compare` (lane records live; the paid compare endpoint is planned), `route_optimize` (live, legacy x402 v1 at 5 USDC, or the free tier).
- `/llms.txt`: "Accounts & agents (new)" section appended by `scripts/append-discovery.mjs` after `build_seo.ts`. Existing content is kept.
- `/robots.txt`: `Sitemap: https://arctictradelanes.com/sitemaps/index.xml` appended. `/sitemap.xml` is unchanged.
- Not added yet: `/.well-known/x402-v2.json` and `/.well-known/mcp.json`, because `api.`, `mcp.` and `id.` are not live.

## 3. Fact pages (spec §11)
`scripts/build-fact-pages.mjs` (no network) → `./factpages` (served by an additive middleware in `server.ts` before the SPA fallback). `public/data/slugs.json` holds stable slugs: kebab-case, ASCII-folded, de-duplicated, append-only.
- 11 layers × 22 languages. Per language: ports 140 indexable / 15 noindex, programs 713 / 0, cities 49 / 54, shipyards 69 / 1, industry 110 / 0, airports 10 / 0, rail 14 / 0, lanes 27 / 0, tankers 51 / 0, icebreakers 56 / 0, rescue 7 / 0.
- Totals: 28,952 object pages + 242 layer index pages. 27,654 sitemap URLs in 220 shards (`/sitemaps/{prefix}-{lang}.xml`), which equals indexable pages + index pages.
- Build gates: neutral lint 0, JSON-LD parses (29,194 pages), hreflang reciprocal (23 links per page), page count = sitemap count. On any failure the build exits 1 and keeps the previous output. The build skips work when its inputs are unchanged (`factpages/.inputs.sha256`).
- `/object/{atlas_id}` → 301 to the typed URL from the origin. Unknown slugs return a real 404 page. `/?focus={id}&layer=` centres the polar map (additive).

## 4. Brands strip (spec §12), flag OFF
22 `ready` logos downloaded once from Wikimedia Commons into `public/assets/brands/`, with `ATTRIBUTION.md` (Tschudi logo is CC BY-SA 4.0 and gets a visible credit line). Component `src/components/ArcticBrandsStrip.tsx` with heading and disclaimer in 22 locales. It renders only when the build sets `VITE_ATL_BRANDS_STRIP=1`; the default is OFF. Brand-wording lint: `scripts/lint-brand-wording.mjs` (0 hits).

## 5. Accounts Workers
Branch `mvp/accounts-workers`: `workers/atl-id|atl-api|atl-mcp` (wrangler.toml with Phase 0 bindings and placeholder IDs), `workers/migrations/0001_init.sql`, Phase 1 handlers (magic link, consent + double opt-in, one-click unsubscribe, outbox → Queue → R2, reconciler). Not deployed; blocked on spec §13.

## Protected surfaces
These hashes were taken before and after deploy, with volatile timestamps ignored, and match: `/.well-known/x402.json` cce6bc87e11d52d5, `/api/x402/schema` 78bf3d90aba98a01, `/api/x402/status` 3f7b411315fb7c70, `/api/alpha/status` d1890e408e111de4. The homepage JSON-LD @graph types, the H1, the og image and the 6 ad slot ids are unchanged.
