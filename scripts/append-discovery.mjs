#!/usr/bin/env node
// Append-only additions to the generated public/llms.txt and public/robots.txt (run after scripts/build_seo.ts).
// Existing content is kept byte-for-byte; the additions are appended once (idempotent marker check).
import fs from 'node:fs';
const LLMS = 'public/llms.txt', ROBOTS = 'public/robots.txt';
const add = fs.readFileSync('mvp-static/llms-accounts-agents.txt', 'utf8');
function append(file, marker, text) {
  const cur = fs.readFileSync(file, 'utf8');
  if (cur.includes(marker)) return console.log(`[discovery] ${file}: already has "${marker}"`);
  fs.writeFileSync(file, cur + (cur.endsWith('\n') ? '' : '\n') + text);
  console.log(`[discovery] ${file}: appended "${marker}"`);
}
append(LLMS, '## Accounts & agents (new)', add.replace(/^\n/, '\n'));
append(ROBOTS, 'Sitemap: https://arctictradelanes.com/sitemaps/index.xml', '\n# ATL fact pages (sharded sitemaps, 22 languages)\nSitemap: https://arctictradelanes.com/sitemaps/index.xml\n');
// agent.json must be byte-identical to agent-card.json
const a = fs.readFileSync('mvp-static/.well-known/agent-card.json'), b = fs.readFileSync('mvp-static/.well-known/agent.json');
if (!a.equals(b)) { fs.writeFileSync('mvp-static/.well-known/agent.json', a); console.log('[discovery] agent.json re-synced to agent-card.json'); }
JSON.parse(a.toString('utf8'));
