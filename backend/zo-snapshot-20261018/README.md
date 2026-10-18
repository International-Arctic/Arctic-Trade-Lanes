# Zo backend snapshot (2026-10-18)

**This is a read-only snapshot, not a maintained source tree.** It copies backend files that run the live
ArcticTradeLanes.com server on Zo (`ArcticTradeLanes.com/arctic-trade-lanes`), which were untracked in git
until Zo commit `e332c6aab` (2026-10-18). It exists so these files can be restored if the Zo folder is lost again
(see the 2026-10-13 incident).

| path | what it is |
|---|---|
| `cluster.ts` | service entrypoint (`bun run cluster.ts`): SO_REUSEPORT worker cluster around `server.ts` |
| `src/api/` | Hono routes: discovery, fact pages, x402 routes, SEO middleware, render cache/compression (`perfMiddleware.ts`), load governor |
| `src/services/` | AIS ingest (public ArcGIS feeds, off unless `ATL_AIS_INGEST=1`) and WebSocket server |
| `scripts/static-pages/` | `build_pages.py` (same as `site/static-pages/`), `rebuild_pages.sh` (atomic per-file rebuild of `pages/`), `daily_loop.sh` (daily 00:07 MSK scheduler) |
| `zo-app.gitignore` | the `.gitignore` added to the Zo app (keeps `.env*`, keys and secrets files out of git) |

Not included: `server.ts` (kept on Zo with dated backups), data, atlas files, `node_modules`, any `.env`.

Secrets: none. All configuration is read from `process.env` (e.g. `DEEPSEEK_API_KEY`, `ATL_*`); no keys,
tokens or credentials are in these files. The `0x211D…9Cea` address in `x402Routes.ts` is the public x402
receiving address already published at `/.well-known/x402.json`.
