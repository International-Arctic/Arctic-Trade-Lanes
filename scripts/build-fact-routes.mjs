#!/usr/bin/env node
// Emit factpages/.routes.json — the exact URL -> file map the origin serves from ./factpages.
//
// Why a manifest: the fact-page set is ~29k files. Walking that tree at boot, in every
// cluster worker, on a 9p mount is seconds of startup per worker and pure repetition.
// One small JSON read replaces it, and it keeps the URL scheme in exactly one place.
//
// Usage: node scripts/build-fact-routes.mjs [--out factpages]
import fs from 'node:fs';
import path from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).map((a, i, all) =>
    a.startsWith('--') ? [a.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true] : null,
  ).filter(Boolean),
);

const ROOT = process.cwd();
const OUT = path.resolve(ROOT, args.out || 'factpages');
const PREFIXES = new Set(['port', 'program', 'city', 'shipyard', 'industry', 'airport', 'rail', 'lane', 'vessel', 'rescue']);
const INDEX_LAYERS = new Set(['ports', 'programs', 'cities', 'shipyards', 'industry', 'airports', 'rail', 'lanes', 'tankers', 'icebreakers', 'rescue']);

if (!fs.existsSync(OUT)) {
  console.error(`[fact-routes] ${path.relative(ROOT, OUT)} not found; run scripts/build-fact-pages.mjs first`);
  process.exit(1);
}

/** URL prefix for a language. English is the source locale and lives at the bare path. */
const pfx = (lang) => (lang === 'en' ? '' : `/${lang}`);

const routes = {};
let objectPages = 0;
let indexPages = 0;
let sitemaps = 0;

const langs = fs.readdirSync(OUT, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);

for (const lang of langs) {
  const langDir = path.join(OUT, lang);

  if (lang === 'sitemaps') {
    for (const f of fs.readdirSync(langDir)) {
      if (!f.endsWith('.xml')) continue;
      routes[`/sitemaps/${f}`] = `sitemaps/${f}`;
      sitemaps++;
    }
    continue;
  }

  for (const entry of fs.readdirSync(langDir, { withFileTypes: true })) {
    if (entry.isFile()) continue;
    const layerDir = path.join(langDir, entry.name);

    if (entry.name === '_index') {
      for (const f of fs.readdirSync(layerDir)) {
        if (!f.endsWith('.html')) continue;
        const layer = f.slice(0, -5);
        if (!INDEX_LAYERS.has(layer)) continue;
        routes[`${pfx(lang)}/${layer}`] = `${lang}/_index/${f}`;
        indexPages++;
      }
      continue;
    }

    if (!PREFIXES.has(entry.name)) continue;
    for (const f of fs.readdirSync(layerDir)) {
      if (!f.endsWith('.html')) continue;
      const slug = f.slice(0, -5);
      routes[`${pfx(lang)}/${entry.name}/${slug}`] = `${lang}/${entry.name}/${f}`;
      objectPages++;
    }
  }
}

const payload = {
  generated_at: new Date().toISOString(),
  source: 'scripts/build-fact-routes.mjs',
  langs: langs.filter((l) => l !== 'sitemaps').length,
  object_pages: objectPages,
  index_pages: indexPages,
  sitemaps,
  total: Object.keys(routes).length,
  routes,
};

const target = path.join(OUT, '.routes.json');
const tmp = `${target}.tmp`;
fs.writeFileSync(tmp, JSON.stringify(payload));
fs.renameSync(tmp, target);

console.log(
  `[fact-routes] ${payload.total} URLs (${objectPages} object + ${indexPages} index + ${sitemaps} sitemap) ` +
    `across ${payload.langs} languages -> ${path.relative(ROOT, target)} ` +
    `(${(fs.statSync(target).size / 1048576).toFixed(2)} MB)`,
);
