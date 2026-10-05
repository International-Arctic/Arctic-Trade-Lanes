# NOTES — Home GIS hero POLISH release (2026-10-06)
Follows hero fix 9c96e69. Additive; JSON-LD (10 ImageObject), SSR H1, og image, server.ts x402, Arctic-panel carve-out, ads-config untouched.

1. Onboarding: '30-second start' is now a small dock chip (bottom-left, with x). Card opens only on tap, compact 300px; dismissal persisted (localStorage atl_coach_done).
2. Desktop: '2026–2036 Arctic Sprint' card and 'NSR transit tests' news card collapsed by default into toggles (dock chip / top-right chip). Content kept in DOM (hidden).
3. Header: H1 never shrinks (shrink-0); decorative 'Arctic GIS OSINT · 2026–2036 sprint' span -> sr-only; nav row hidden <640px (max-sm:hidden), scrolls otherwise; H1 keyword sr-only <768px (kept in DOM).
4. Map overlays: single top-centre stack (GIS badge, then feed-status chip below so the badge never shifts); CRS label below ARCTIC SCREEN on mobile; ARCTIC SCREEN width leaves the OSINT-controls toggle free; OL zoom moved bottom-left above the dock; desktop layer chips moved below the screen panel.
5. First-paint race: map no longer waits for /api/vessels (was ~2–4s of 'Loading layers' before OL even mounted); ResizeObserver(container) -> map.updateSize() + rAF updateSize; atlas/land fetches retry 3x with backoff; badge rendered independent of data. Cold-load test 8/8 OK at 500x689, cache disabled.
6. AR + all non-EN: agenda title/intro/credit/h1Keyword/nav + 10 items alt/caption translated for 19 locales (src/i18n/agendaLocales.ts, merged in agendaCopy). Strip already read i18n; the bundle map was pointing 19 locales at EN. Filter chips: scroll with end fade + RTL-correct mask/padding.
7. Carousel arrows visible at all widths (40px <1024, 44px desktop).
8. Yandex Autoplacement 20141282: snippet/URL format correct; an.yandex.ru/auto_placement/?page-id=20141282 -> 404 = no active Autoplacement config for the block/domain in RSYa. ID unchanged.

Metrics (/, /ru, /ar): 500x689 map 500x427 (62%) CLS 0–0.014; 390x844 390x523 (62%) CLS 0.003–0.012; 1728x1117 1728x720 (64%) CLS 0.003–0.005.
