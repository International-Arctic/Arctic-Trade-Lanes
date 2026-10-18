#!/usr/bin/env python3
"""Idempotent additive patch for server.ts (ATL v2, 2026-10-18). Marker: ATL-V2-HOOK.
Usage: python3 patch_server_v2.py server.ts [out.ts]"""
import sys
src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding="utf8").read()
if "ATL-V2-HOOK" in s:
    print("already patched"); open(dst, "w", encoding="utf8").write(s); sys.exit(0)
def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f"anchor count mismatch ({s.count(old)} != {count}): {old[:80]!r}")
    s = s.replace(old, new)
rep('import atlIntakeRoutes from "./src/home/intakeRoutes";\n',
    'import atlIntakeRoutes from "./src/home/intakeRoutes";\n'
    '// ATL-V2-HOOK (2026-10-18): hubs, companies registry, sitemaps, hero/flags/logos/sprint, FX endpoint. Kill switch ATL_V2=0.\n'
    'import { v2HomeInject, v2Match, v2PageInject } from "./src/home/v2/atlV2";\n'
    'import atlV2Routes from "./src/home/v2/v2Routes";\n')
rep('app.route("/", atlIntakeRoutes);\n', 'app.route("/", atlIntakeRoutes);\napp.route("/", atlV2Routes);\n')
rep('const PAGE_HEADERS: Record<string, string> = { "Cache-Control": "public, max-age=300" };',
    'const PAGE_HEADERS: Record<string, string> = { "Cache-Control": "public, max-age=300, s-maxage=3600, stale-while-revalidate=600" };')
rep('const HOME_X_HEADERS: Record<string, string> = { "X-ATL-Home": "extras" };',
    'const HOME_X_HEADERS: Record<string, string> = { "X-ATL-Home": "extras", "Cache-Control": "public, max-age=120, s-maxage=600, stale-while-revalidate=600" };\n'
    'const V2_HEADERS: Record<string, string> = { "Cache-Control": "public, max-age=600, s-maxage=3600, stale-while-revalidate=86400", "X-ATL-V2": "page" };\n'
    'const V2_TYPES: Record<string, string> = { xml: "application/xml; charset=UTF-8", webp: "image/webp", json: "application/json; charset=UTF-8" };')
rep('return renderedResponse(renderCache.cacheHtml(key, readFileSync(file, "utf8")), c, { ...PAGE_HEADERS, "X-ATL-Page": m[2] });',
    'return renderedResponse(renderCache.cacheHtml(key, v2PageInject(readFileSync(file, "utf8"), m[1] || "en", m[2])), c, { ...PAGE_HEADERS, "X-ATL-Page": m[2] });')
rep('entry = renderCache.cacheHtml(ck, injectHomeExtras(seoHtml(key, getShell()), m[1] || "en"));',
    'entry = renderCache.cacheHtml(ck, v2HomeInject(injectHomeExtras(seoHtml(key, getShell()), m[1] || "en"), m[1] || "en"));')
MW = '''  // ATL V2 (2026-10-18): /[lc/]country/<iso2>, /[lc/]companies, /[lc/]company/<slug>, /sitemaps/atl-v2-<lc>.xml,
  // /sitemap-index.xml, /atl-hero/*. Template-rendered from src/home/v2 + data/arctic-brands; unknown slugs fall through
  // to the 404 gate unchanged. No ads/payment/token on these pages. Kill switch: ATL_V2=0.
  app.use(async (c, next) => {
    if (c.req.method !== "GET" && c.req.method !== "HEAD") return next();
    const hit = v2Match(c.req.path);
    if (!hit) return next();
    if (hit.kind === "html") {
      const warm = renderCache.lookup(hit.key);
      if (warm) return renderedResponse(warm, c, V2_HEADERS);
      let html: string | null = null;
      try {
        html = hit.body() as string | null;
      } catch (err) {
        console.error(`[atl-v2] ${c.req.path} -> ${err instanceof Error ? err.message : String(err)}`);
        return next();
      }
      if (!html) return next();
      return renderedResponse(renderCache.cacheHtml(hit.key, html), c, V2_HEADERS);
    }
    let body: string | Uint8Array | null = null;
    try { body = hit.body(); } catch { return next(); }
    if (body == null) return next();
    const cc = hit.kind === "webp" ? "public, max-age=604800, immutable" : "public, max-age=3600, s-maxage=3600";
    return new Response(body, { headers: { "Content-Type": V2_TYPES[hit.kind], "Cache-Control": cc, "X-ATL-V2": hit.kind } });
  });
'''
rep('  // NEUTRAL PEOPLE PAGES (2026-10-18)', MW + '  // NEUTRAL PEOPLE PAGES (2026-10-18)')
open(dst, "w", encoding="utf8").write(s)
print("patched ->", dst)
