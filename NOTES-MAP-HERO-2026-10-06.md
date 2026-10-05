# NOTES — Home GIS map hero fix + carousel UX (2026-10-06)

## Root cause
`.atl-home-map` was absolutely positioned with bottom = bottom-chrome + safe-area + `--atl-home-bottom-ad`. Rule `[data-atl-home]:has(.atl-home-below-ads .atl-ad:not(.atl-ad-off)){--atl-home-bottom-ad:500px}` (540px <=1023px) fired even for EMPTY slots, collapsing the map: 500x689 -> 0px, 390x844 -> 108px, 1728x1117 -> 431px (39%). `.atl-home-below-ads` (absolute, z30: agenda + dashed empty ads) took the map's place. OpenLayers itself was fine.
Secondary: a minifier-merged nested `:has()` selector invalidated a top-ad override rule (Chrome drops whole rule).

## Fix (additive)
- Bottom-ad reserve neutralised; below-ads strip static, in flow after hero. Map height clamp(360px,70svh,720px) desktop / max(320px,62svh) <=1023px, min 320px. ResizeObserver -> resize -> OL updateSize.
- `.atl-ad:not(.atl-ad-filled){display:none}`; atl-ad-filled set only on real render (AdSlot.tsx + atl-ads.js). 6 slot IDs kept.
- Coach card only when map > 200px.
- Badge 'Arctic GIS Atlas · EPSG:3996' + 'Open full GIS atlas' -> /arctic-economic-atlas, 22 langs (src/i18n/homeHero.ts).
- <420px header compaction; H1 text kept in DOM.
- OSINT controls panel collapsed by default on desktop.
- Agenda carousel: 300px / 78vw cards, 16:9, 12px/1.4 captions clamp 3, single Photo credits disclosure (licences + BY-SA kept), 44px arrows, dots, scroll-snap, RTL.
- Note: PolarStereographicMap.tsx commit also captures previously-uncommitted, already-live map work.

## Numbers (after; /, /ru, /ar identical)
500x689: map 500x427 @y48, tiles 99% nonblank, CLS 0
390x844: map 390x523 @y48, tiles 87%, CLS 0
1728x1117: map 1728x720 @y48 (64%), tiles 68%, CLS 0.003-0.005
JSON-LD valid (10 ImageObject), SSR H1, og image unchanged. server.ts x402 / Arctic-panel carve-out / ads-config untouched.

## Yandex Autoplacement 20141282
Loader snippet correct (context.js + ap-loader.js data-page-id). ap-loader requests https://an.yandex.ru/auto_placement/?page-id=20141282 (correct format) -> 404: no active Autoplacement config for this page/domain. Enable/approve Autoplacement for the block in the RSYa UI (activation ~20 min). ID unchanged.
