# Arctic agenda SEO image strip — 2026-10-05

Live on Zo tip `a5a1e23` (svc_UpoHDo9rDHs). Additive Home-only strip `#atl-home-agenda`
between `atl-ad-home-providers` and `.atl-home-inc-row`. Map + 6 ad slots untouched.

## Assets (this commit)
- `public/img/arctic-agenda/<slug>-{480,960,1440}.{webp,jpg}` — 60 files
- `public/img/og/international-arctic-forum-2025-murmansk-og-1200x630.jpg` (~90 KB)

## Live SPA (Zo workspace; not fully mirrored here)
- `src/data/arcticAgenda.ts`, `src/i18n/agenda.ts`, `src/components/ArcticAgendaStrip.tsx`
- Home H1 keyword + Funding/Advertise nav; ItemList ImageObject; sitemap `image:image` ×22 homes
- Caption links allowlist only; no sanctions/OFAC; no `/people/*`

## CLS (Chromium PerformanceObserver, 2026-10-05 ~22:30 MSK)
| URL | viewport | CLS | LCP ms | agenda cards | 6 ads |
|---|---|---|---|---|---|
| / | desktop | 0.017 | 1892 | 10 | yes |
| /ru | desktop | 0.003 | 1436 | 10 | yes |
| /ar | desktop | 0.006 | 1380 | 10 | yes |
| / | mobile | 0.088 | 976 | 10 | yes |
| /ru | mobile | 0.005 | 1020 | 10 | yes |
| /ar | mobile | 0.012 | 1100 | 10 | yes |

Prior mobile CLS after ads work was ~0.176 (map init). Lighthouse unavailable; PO used.
Screenshots: box `/workspace/atl-seo-images/out/{en,ru,ar}-{desktop,mobile}.png`
