# Yandex Autoplacement 20141282 — ArcticTradeLanes.com (2026-09-30)

Owner-approved (Aleksei Dolgikh @alexdolbun, 2026-09-30). Additive, HTML-only change on the Zo origin
(`ArcticTradeLanes.com/arctic-trade-lanes`, service `svc_UpoHDo9rDHs`). No App.tsx change, no redesign.

Snippet inserted inside `<head>` (immediately before `</head>`), idempotent on the marker
`Yandex Autoplacement 20141282`:

```html
<!-- Yandex Autoplacement 20141282 -->
<script src="https://yandex.ru/ads/system/context.js" async></script>
<script data-page-id="20141282" src="https://yandex.ru/ads/system/ap-loader.js" async></script>
```

## Where
- `index.html` (SPA template → `dist/index.html` via `vite build`; covers `/`, all 22 `/<locale>` routes and SPA fallbacks through `seoHtml`)
- `ssr/**/*.html` — 154 Arctic-panel SSR pages (AIM Congress 2026 event + Dmitriev, Chekunkov, Chibis, Nikolaev, Dovlatov, Panov × 22 locales)
- `scripts/ssr_arctic_panel/gen.py` — `YANDEX_AP` constant added to the page template so regenerated SSR pages keep the tag
- `server.ts` SSR middleware untouched.

## Not touched
- JSON/API routes: `/.well-known/x402.json`, `/v1/.well-known/x402.json`, `/api/*`, `/data/*.geojson`, `/atlas/atlas.manifest.json`, atlas GeoJSON — byte-identical (sha256 checked before/after on apex).
- No Content-Security-Policy header or meta existed, so none was added.
- No DNS / Cloudflare changes.
