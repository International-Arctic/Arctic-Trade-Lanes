// atl-mcp (mcp.arctictradelanes.com) — Phase 3 placeholder. NOT deployed.
// Planned (spec §5.3/§9.3): OAuthProvider (workers-oauth-provider, KV OAUTH_KV) + McpAgent at /mcp with
// search_objects, get_object, list_layers (free) and compare_lanes, export_layer, route_optimize (x402 paidTool).
import { json } from '../../shared/util';

export interface Env { OAUTH_KV: KVNamespace }

export default {
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname === '/healthz') return json({ ok: true, phase: 'scaffold' });
    return json({ error: 'not_implemented', see: 'spec §5.3 (Phase 3)' }, 501);
  },
} satisfies ExportedHandler<Env>;
