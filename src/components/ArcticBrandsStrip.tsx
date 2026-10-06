import React from 'react';
import data from '../data/brands-strip.json';
import { useLang } from '../i18n';

// Feature flag (spec §12): OFF unless the build sets VITE_ATL_BRANDS_STRIP=1. Default build renders nothing.
export const ATL_BRANDS_STRIP_ON = String((import.meta as any).env?.VITE_ATL_BRANDS_STRIP ?? '0') === '1';

type Strings = { brands_heading: string; brands_disclaimer: string; brand_alt: string; logo_credits: string };

export default function ArcticBrandsStrip() {
  const ctx = useLang() as any;
  if (!ATL_BRANDS_STRIP_ON) return null;
  const lang: string = (ctx && ctx.lang) || 'en';
  const s: Strings = (data.strings as Record<string, Strings>)[lang] || (data.strings as Record<string, Strings>).en;
  const brands = [...data.brands].sort((a, b) => a.brand.localeCompare(b.brand, 'en', { sensitivity: 'base' }));
  return (
    <section className="atl-brands" data-atl-brands-strip aria-labelledby="atl-brands-h">
      <style>{`.atl-brands{max-width:1200px;margin:24px auto;padding:12px 16px;text-align:center}
.atl-brands h2{font-size:14px;font-weight:600;letter-spacing:.02em;color:#cbd5e1;margin:0 0 10px}
.atl-brands ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:10px 14px}
.atl-brands li a{display:inline-flex;align-items:center;height:40px;padding:6px 10px;border-radius:6px;background:rgba(248,250,252,.92)}
.atl-brands img{height:28px;width:auto;max-width:140px;object-fit:contain;filter:grayscale(1);opacity:.8;transition:filter .2s,opacity .2s}
.atl-brands li a:hover img,.atl-brands li a:focus-visible img{filter:none;opacity:1}
.atl-brands p{font-size:11px;line-height:1.45;color:#94a3b8;margin:10px auto 0;max-width:820px}
.atl-brands p a{color:#94a3b8;text-decoration:underline}`}</style>
      <h2 id="atl-brands-h">{s.brands_heading}</h2>
      <ul>
        {brands.map((b) => (
          <li key={b.slug}>
            <a href={`/object/${b.atlas_id}`} title={b.brand}>
              <img src={b.file} alt={s.brand_alt.replace('{brand}', b.brand)} height={28} loading="lazy" decoding="async" />
            </a>
          </li>
        ))}
      </ul>
      <p>{s.brands_disclaimer}</p>
      <p>
        {s.logo_credits}:{' '}
        {data.credits.map((c, i) => (
          <span key={c.brand}>
            {i ? '; ' : ''}
            {c.brand} logo by {c.author}, <a href={c.license_url} rel="license noopener" target="_blank">{c.license}</a>, via{' '}
            <a href={c.source} rel="noopener" target="_blank">Wikimedia Commons</a>
          </span>
        ))}
        {' · '}
        <a href="/assets/brands/ATTRIBUTION.md">ATTRIBUTION</a>
      </p>
    </section>
  );
}
