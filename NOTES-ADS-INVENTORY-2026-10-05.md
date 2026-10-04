# ATL ad inventory — explicit Yandex RTB slots + /advertise (2026-10-05)

Owner-approved (Aleksei Dolgikh @alexdolbun, 2026-10-05). Additive change on the Zo origin
(`ArcticTradeLanes.com/arctic-trade-lanes`, service `svc_UpoHDo9rDHs`). Yandex Autoplacement 20141282
stays in every page `<head>` unchanged. App source is not mirrored here; this repo carries the two public
files (`public/ads-config.js`, `public/atl-ads.js`) and this note.

## Slot ids (stable)
| id | kind | reserved size | where |
|---|---|---|---|
| `atl-ad-top` | top banner | min-height 90px, 728px wide (desktop) / 100px, 320px (under 1024px) | under the page header / H1 |
| `atl-ad-inc-1..n` | in-content | min-height 250px, up to 728px wide, responsive | between sections, 2-3 on long pages |
| `atl-ad-side` | sticky sidebar | 300x600, `position:fixed` right rail | desktop only (>=1024px); body gets `padding-right:324px` so it never covers content |
| `atl-ad-mstick` | mobile sticky bottom bar | 64px (+ safe-area), close button | mobile only (<1024px); body gets `padding-bottom`; closed state remembered per session |

Each slot is an empty `<aside id="…" data-yandex-rtb-slot="…" data-atl-ad="kind">` with a subtle
"Advertisement" label and an inner `<div id="yandex_rtb_<slot id>">` render target
(React component `src/components/AdSlot.tsx`: `AdSlot`, `AdRails`, `AdvertiseLink`).

### Slots per page type
- Home `/` (full-screen map app): `atl-ad-side` + `atl-ad-mstick` (rails; collapsed until mapped)
- Content pages: `/opportunity` top + inc-1..2; `/china-polar-silk-road` top + inc-1..3; `/pricing` top + inc-1..2;
  `/arctic-economic-atlas` top + inc-1..2; `/collaborate` top + inc-1; `/account` top + inc-1 — plus the two rails (all 22 locales)
- `/advertise` (new): top + inc-1 + rails
- Arctic-panel SSR pages (`ssr/**`, 154 files: /people/* and /events/* panel slugs): Autoplacement only, 0 extra slots, no /advertise link

## Config mechanism
`/ads-config.js` (loaded synchronously in `<head>` before Yandex `context.js`) sets
`window.ATL_AD_SLOTS = { "<slot id>": "R-A-<partner id>-<n>" }`. `/atl-ads.js` initialises `window.yaContextCb`
and calls `Ya.Context.AdvManager.render({ blockId, renderTo: "yandex_rtb_<slot id>" })` only for mapped,
visible slots. Lookup order: `<id>:mobile` (under 1024px) → `<id>` → family key (`atl-ad-inc`, rendered with `pageNumber = n`).
`window.ATL_AD_RESERVE = { inline: true, rails: false }`: unmapped inline slots keep reserved space (zero CLS);
unmapped rails stay collapsed (decided before first paint, so no shift).

To activate: edit `public/ads-config.js` (and `dist/ads-config.js` for an instant change), then bump `?v=` on the two
`<script … vite-ignore>` tags in `index.html` + rebuild/restart, because Cloudflare/browsers cache `.js` for 4h (`max-age=14400`).

## /advertise
New SPA route `/advertise` + `/:lang/advertise` (EN, RU, ZH texts; other locales use the EN fallback), added to the sitemap.
Lists the placements and sizes, a high-level audience description (no traffic numbers), the contact partners@arctictradelanes.com,
and a note that direct buys can be paid in crypto via the existing x402 rail (`/.well-known/x402.json`, unchanged).
Linked from the footer of every SPA content page.

## Untouched
`server.ts` (incl. Arctic-panel SSR middleware), x402 files/routes, JSON/API routes, `/ads.txt`, atlas GeoJSON/manifest,
DNS and the Cloudflare edge worker (`/advertise`, `/ads-config.js`, `/atl-ads.js` already pass through to Zo on the apex).
