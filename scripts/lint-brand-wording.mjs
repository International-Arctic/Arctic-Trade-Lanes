#!/usr/bin/env node
// Brand-strip wording lint (ATL MVP spec §12). Fails (exit 1) if the brands strip, its translations or its
// data use relationship wording. The strip may only say that a company is *covered on the atlas*.
// Usage: node scripts/lint-brand-wording.mjs [files...]
// Default scope: brands_* / brand_alt / logo_credits keys in i18n/labels.*.json, src/components/ArcticBrandsStrip.tsx,
// src/data/brands-strip.json, public/assets/brands/brands.json.
import fs from 'node:fs';
import path from 'node:path';

export const BANNED = [
  // en
  'partner', 'trusted by', 'customer', 'client', 'used by', 'powered by', 'in collaboration with',
  // ru
  'партнер', 'партнёр', 'клиент', 'заказчик', 'доверяют', 'при поддержке', 'на базе', 'в сотрудничестве', 'используют',
  // zh
  '合作伙伴', '伙伴', '客户', '信赖', '信任', '合作', '技术支持', '使用者',
  // ja
  'パートナー', '顧客', 'お客様', '導入企業', '協力', '信頼', '提供：',
  // ko
  '파트너', '고객', '협력', '신뢰',
  // el
  'συνεργάτ', 'πελάτ', 'σε συνεργασία',
  // de / nl / da / nb / sv
  'kunden', 'klanten', 'kunder', 'vertrauen', 'in zusammenarbeit', 'in samenwerking', 'i samarbejde', 'i samarbeid', 'i samarbete', 'betrouwd',
  // fr / es / it / pt
  'partenaire', 'socios', 'parceiro', 'cliente', 'clienti', 'en collaboration', 'en colaboración', 'in collaborazione', 'em colaboração', 'propulsé par', 'con la tecnología',
  // tr / ar / hi / vi / id
  'ortak', 'müşteri', 'شريك', 'شركاء', 'عملاء', 'عميل', 'بالتعاون', 'साझेदार', 'ग्राहक', 'सहयोग', 'đối tác', 'khách hàng', 'hợp tác', 'mitra', 'pelanggan', 'klien', 'bekerja sama',
  // fi / is
  'kumppan', 'asiakka', 'yhteistyö', 'samstarf', 'viðskiptavin',
];

const lc = (s) => s.normalize('NFC').toLocaleLowerCase('und');
export function lintBrandText(text) {
  const t = lc(text);
  return BANNED.filter((w) => t.includes(lc(w)));
}

function defaultTargets(root) {
  const out = [];
  const i18n = path.join(root, 'i18n');
  if (fs.existsSync(i18n)) for (const f of fs.readdirSync(i18n)) if (/^labels\.[a-z]+\.json$/.test(f)) out.push({ file: path.join(i18n, f), keys: /^(brands?_|logo_credits)/ });
  for (const f of ['src/components/ArcticBrandsStrip.tsx', 'src/data/brands-strip.json', 'public/assets/brands/brands.json']) {
    const p = path.join(root, f);
    if (fs.existsSync(p)) out.push({ file: p });
  }
  return out;
}

function textOf(t) {
  const raw = fs.readFileSync(t.file, 'utf8');
  if (t.keys) { const j = JSON.parse(raw); return Object.entries(j).filter(([k]) => t.keys.test(k)).map(([, v]) => String(v)).join('\n'); }
  return raw;
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('lint-brand-wording.mjs')) {
  const args = process.argv.slice(2);
  const targets = args.length ? args.map((file) => ({ file })) : defaultTargets(process.cwd());
  let hits = 0;
  for (const t of targets) {
    const found = lintBrandText(textOf(t));
    if (found.length) { hits += found.length; console.error(`[brand-lint] ${path.relative(process.cwd(), t.file)}: ${found.join(', ')}`); }
  }
  console.log(`[brand-lint] ${targets.length} files, ${hits} hits`);
  if (hits) process.exit(1);
}
