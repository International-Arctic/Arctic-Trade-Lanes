# Home ad inventory — 2026-10-05 (~21:35 MSK priority)

One SPA template change on `src/pages/Home.tsx` (all 22 locales). Slots sit **outside** the map canvas.

## Home slot ids
| Slot id | Kind | Size | Placement |
|---|---|---|---|
| `atl-ad-home-top` | home-top | 728×90 / 320×100 | Under H1, above map |
| `atl-ad-home-inc-1` | home-inc | banner/adaptive in strip | Below-map strip |
| `atl-ad-home-inc-2` | home-inc | banner/adaptive in strip | Below-map strip |
| `atl-ad-home-providers` | providers | slim ~44px | Below-map partner row |
| `atl-ad-side` | side | 300×600 | Desktop sticky (kept; top offset clears home-top) |
| `atl-ad-mstick` | mstick | 320×50 | Mobile sticky (kept; map chrome clears bar) |

## R-A blocks Aleksei should create (fill `public/ads-config.js`)
- `atl-ad-home-top` + `atl-ad-home-top:mobile`
- `atl-ad-home-inc-1`, `atl-ad-home-inc-2`
- `atl-ad-home-providers`
(plus existing content/rail ids when ready)

Autoplacement **20141282** unchanged. Arctic-panel SSR untouched. `/funding` untouched.
