#!/usr/bin/env node
// Served-vs-canonical ports.csv drift check (gis-loop-1020-1348).
// Canonical: data/ports.csv. Served copies (static vault roots): dist/data/ports.csv, public/data/ports.csv.
// Exits 1 and lists differing port_id rows if any served copy is not byte-identical to canonical.
// Optional: --live <url> also fetches a live copy (e.g. https://arctictradelanes.com/data/ports.csv?v=ci) and compares it.
// Usage: node scripts/check-served-ports-sync.mjs [--live URL]
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";

const CANON = "data/ports.csv";
const SERVED = ["dist/data/ports.csv", "public/data/ports.csv"];
const md5 = (s) => createHash("md5").update(s).digest("hex").slice(0, 8);

function rows(text) {
  // minimal RFC4180 split into records keyed by first field (port_id)
  const out = new Map(); let rec = [], field = "", q = false;
  const push = () => { rec.push(field); field = ""; };
  const end = () => { push(); if (rec.length > 1) out.set(rec[0], rec.join("\u001f")); rec = []; };
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { field += c; i++; } else q = false; } else field += c; }
    else if (c === '"') q = true; else if (c === ",") push();
    else if (c === "\n") end(); else if (c !== "\r") field += c;
  }
  if (field || rec.length) end();
  return out;
}

function compare(label, text, canonText, canon) {
  if (text === canonText) { console.log(`OK   ${label} ${md5(text)} == canonical`); return 0; }
  const r = rows(text);
  const ids = new Set([...canon.keys(), ...r.keys()]);
  const diff = [...ids].filter((k) => canon.get(k) !== r.get(k));
  console.log(`FAIL ${label} ${md5(text)} != canonical ${md5(canonText)}; rows differ: ${diff.join(", ") || "(byte-level only)"}`);
  return 1;
}

const canonText = readFileSync(CANON, "utf8");
const canon = rows(canonText);
let bad = 0;
for (const p of SERVED) {
  if (!existsSync(p)) { console.log(`SKIP ${p} (missing)`); continue; }
  bad |= compare(p, readFileSync(p, "utf8"), canonText, canon);
}
const li = process.argv.indexOf("--live");
if (li > 0 && process.argv[li + 1]) {
  const res = await fetch(process.argv[li + 1], { headers: { "cache-control": "no-cache" } });
  bad |= compare(`live ${process.argv[li + 1]} (${res.status})`, await res.text(), canonText, canon);
}
process.exit(bad);
