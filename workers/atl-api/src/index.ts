// atl-api (api.arctictradelanes.com) — Phase 3 placeholder. NOT deployed.
// Planned (spec §9.2): /v1/agents/register, /v1/objects, /v1/lanes/compare (x402 v2), /v1/exports, /a2a.
import { json } from '../../shared/util';

export interface Env { DB: D1Database; ATL_ORIGIN: string }

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname === '/healthz') {
      try { await env.DB.prepare('SELECT 1').first(); return json({ d1: 'ok' }); } catch { return json({ d1: 'error' }, 503); }
    }
    // Free object facts mirror the static fact pages; this stub only redirects to them for now.
    const m = /^\/v1\/objects\/(ARC-[A-Z]+-\d{1,5})$/.exec(url.pathname);
    if (m) return Response.redirect(`${env.ATL_ORIGIN}/object/${m[1]}`, 302);
    return json({ error: 'not_implemented', see: 'spec §9.2 (Phase 3)' }, 501);
  },
} satisfies ExportedHandler<Env>;
