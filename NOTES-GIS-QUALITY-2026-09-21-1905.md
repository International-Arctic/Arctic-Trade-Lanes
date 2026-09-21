# GIS Quality Loop — 2026-09-21 ~19:05 MSK

## Outcome
- **No new shipyard densify** this cycle (Wuchang + Sembcorp blocked on OSM tag bar).
- **Material atlas win:** rebuilt + synced static atlas so **live** `arctictradelanes.com/data/atlas.geojson` now carries prior **ARC-SHIP-038** Hudong densify (was still soft `31.27/121.54` on live / `www` / `dist` after 17:54 CSV ship).

## Wuchang ARC-SHIP-039 (PRIMARY — blocked)
- Soft pin remains `30.5900,114.3100` (Wuhan).
- WD **Q29841232** Wuchang Shipbuilding Industry Group / 武昌船舶重工集团 — P31 shipyard+business; **no P625**; site wuchuan.com.cn notes Yangluo/Shuangliu relocation.
- OSM candidates reviewed:
  - **way/947969003** `武船重工` Nominatim `30.6455245,114.5599270` (`landuse=industrial`; official_name=**武船重型工程股份有限公司** Heavy Engineering subsidiary — **not** clear shipyard footprint).
  - **relation/8886600** 中国长航船舶重工…青山船厂 — **wrong company** (Sinotrans & CSC Qingshan).
- No `industrial=shipyard` / clear shipyard landuse+name hit near soft or Yangluo this cycle (Overpass busy/timeouts; lz4 returned only the above).

## Sembcorp ARC-SHIP-033 (fallback — blocked by tag bar)
- Soft `1.2600,103.8300` (Singapore).
- OSM **way/1004233134** Sembcorp Marine Tuas Boulevard Yard Nominatim `1.2543436,103.6130677` — `landuse=industrial`, alt_name=`Sembcorp Marine Tuas Shipyard`, website ok.
- **Missing `industrial=shipyard`** — per standing bar, do not densify until tagged.

## Skips / quarantine unchanged
- Hyundai ARC-SHIP-034 soft: avoid dup vs ARC-SHIP-058.
- Naval Group #43 / Ulstein #37 leave alone.
- PORT-034/069, SHIP-069, Zvezda, Wrangell untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-21T16:05:02Z**, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.
- Synced Dataset + www/public/dist/arctic-trade-lanes **incl. dist/data** (prod Bun.file path) — **no SPA redeploy / App.tsx / vite build**.
- Softish shipyards still **14** (no new densify).
- Live verified: ARC-SHIP-038 → `31.279704,121.569853`.

## Next preferred
- Wuchang: need OSM `industrial=shipyard` (or clear shipyard name+landuse) at Yangluo/Shuangliu WSIC yard — help-wanted #45.
- Sembcorp: add `industrial=shipyard` on way/1004233134 then densify.
