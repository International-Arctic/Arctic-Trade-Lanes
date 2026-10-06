#!/usr/bin/env node
// ATL neutral-content lint (spec §8). Fails (exit 1) on any hit.
// The term list is NOT published: scripts/neutral-terms.sha256.json holds salted SHA-256 hashes of
// normalized stems/phrases; the plaintext list lives in the private ops repo.
// Matching: text is NFKD-folded, lower-cased, tokenized on non-letters/digits; every window of up to 3
// tokens is tested by prefix (so a stem matches its inflections). CJK runs are tested by substring.
// Hits are reported by file + location + hash prefix only, never the matched word.
// Usage: node scripts/lint-neutral.mjs [--terms file] [--quiet] <file|dir> ...
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
let TERMS = null;
export function loadTerms(file = process.env.ATL_NEUTRAL_TERMS || path.join(HERE, 'neutral-terms.sha256.json')) {
  const j = JSON.parse(fs.readFileSync(file, 'utf8'));
  TERMS = { salt: j.salt, set: new Set(j.hashes), heads: new Set(j.heads || []), lengths: j.lengths.slice().sort((a, b) => a - b) };
  return TERMS;
}
const norm = (s) => s.normalize('NFKD').replace(/\p{M}+/gu, '').toLowerCase().replace(/ё/g, 'е');
const CJK = /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u;
const H = (s) => crypto.createHash('sha256').update(TERMS.salt + s).digest('hex');
const memo = new Map();
// prefix test of string s against the hashed term set, only for prefix lengths >= minLen
function prefixHit(s, minLen = 0) {
  const cps = [...s];
  for (const L of TERMS.lengths) {
    if (L < minLen) continue;
    if (L > cps.length) break;
    const h = H(cps.slice(0, L).join(''));
    if (TERMS.set.has(h)) return h.slice(0, 8);
  }
  return null;
}
function tokInfo(t) {
  let r = memo.get(t);
  if (r) return r;
  r = { hit: prefixHit(t), head: TERMS.heads.has(H(t)) };
  if (memo.size > 2e6) memo.clear();
  memo.set(t, r);
  return r;
}
/** Returns an array of hash-prefix ids for every banned stem found in `text` (empty = clean). */
export function lintText(text) {
  if (!TERMS) loadTerms();
  if (text == null) return [];
  const toks = norm(String(text)).split(/[^\p{L}\p{N}]+/u).filter(Boolean);
  const out = [];
  for (let i = 0; i < toks.length; i++) {
    const t = toks[i];
    if (CJK.test(t)) {
      const c = [...t];
      for (let j = 0; j < c.length; j++) { const r = prefixHit(c.slice(j, j + 8).join('')); if (r) out.push(r); }
      continue;
    }
    const info = tokInfo(t);
    if (info.hit) { out.push(info.hit); continue; }
    if (info.head && i + 1 < toks.length) {
      const r = prefixHit(toks.slice(i, i + 3).join(' '), [...t].length + 2);
      if (r) out.push(r);
    }
  }
  return out;
}
export const isClean = (text) => lintText(text).length === 0;

function* walkJson(o, p = '$') {
  if (typeof o === 'string') yield [p, o];
  else if (Array.isArray(o)) for (let i = 0; i < o.length; i++) yield* walkJson(o[i], `${p}[${i}]`);
  else if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) { yield [`${p}.${k}#key`, k]; yield* walkJson(v, `${p}.${k}`); }
}
export function lintFile(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const hits = [];
  if (/\.(geo)?json$/i.test(file)) {
    let j = null; try { j = JSON.parse(raw); } catch { /* fall through to text */ }
    if (j) {
      const ids = new Map();
      if (Array.isArray(j.features)) j.features.forEach((f, i) => ids.set(i, f?.properties?.id || f?.id));
      for (const [p, s] of walkJson(j)) for (const h of lintText(s)) {
        const m = p.match(/^\$\.features\[(\d+)\]\.properties\.([^.#[]+)/);
        hits.push({ file, where: m ? `${ids.get(+m[1])}.${m[2]}` : p, term: h });
      }
      return hits;
    }
  }
  raw.split('\n').forEach((line, i) => { for (const h of lintText(line)) hits.push({ file, where: `line ${i + 1}`, term: h }); });
  return hits;
}
const TEXT_EXT = /\.(html?|xml|json|geojson|txt|md|csv|tsv|mjs|js|ts|tsx|css|svg)$/i;
export function* listFiles(p) {
  const st = fs.statSync(p);
  if (st.isFile()) { yield p; return; }
  for (const e of fs.readdirSync(p, { withFileTypes: true })) {
    if (e.name === 'node_modules' || e.name === '.git') continue;
    const q = path.join(p, e.name);
    if (e.isDirectory()) yield* listFiles(q); else if (TEXT_EXT.test(e.name)) yield q;
  }
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2); const targets = []; let quiet = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--terms') loadTerms(args[++i]); else if (args[i] === '--quiet') quiet = true; else targets.push(args[i]);
  }
  if (!TERMS) loadTerms();
  let files = 0; const all = [];
  for (const t of targets) for (const f of listFiles(t)) { files++; all.push(...lintFile(f)); }
  if (!quiet || all.length) for (const h of all.slice(0, 500)) console.log(`HIT ${h.file} :: ${h.where} :: term#${h.term}`);
  console.log(`[lint-neutral] ${files} files, ${all.length} hits`);
  process.exit(all.length ? 1 : 0);
}
