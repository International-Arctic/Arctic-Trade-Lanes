# Industry coarse-approx densify — Cycle E (live atlas `2026-09-08T10:18:41Z`)

Moved five low-precision industry pins (~0–1 decimal degree) onto verifiable OSM Nominatim industrial / mine / settlement points. Neutral OSM sourcing only.

| id | was | now | rationale / sources |
|----|-----|-----|---------------------|
| `ARC-FAC-001` Norwegian Hydrogen Tornio | approx `65.78, 24.15` | Tornion satama / Röyttä `65.7598189, 24.1574679` | OSM landuse=industrial Tornion satama, Röyttä |
| `ARC-FAC-003` Oulun Energia Laanila | approx `65.06, 25.47` | Laanilan teollisuuspuisto `65.0341110, 25.5178198` | OSM Laanilan teollisuuspuisto, Takalaanila |
| `ARC-FAC-331` Malmbjerg Mo | coarse `-21.5, 72.0` | historic mine `71.9605614, -24.2798494` | OSM historic=mine Malmbjerg (Scoresby Sund) — large lon correction |
| `ARC-FAC-339` Arctic Way CLS Jan Mayen | approx `-8.4, 70.99` | Olonkinbyen `70.9224474, -8.7159894` | OSM place=hamlet Olonkinbyen |
| `ARC-FAC-395` IðunnH2 Helguvík e-SAF | approx `-22.42, 64.0` | Helguvík depot zone `64.0179298, -22.5569368` | OSM landuse=construction Ný Olíubirgðastöð í Helguvík |

Skipped `ARC-FAC-330` Sarfartoq this cycle — Nominatim returned a different cape (`Sarfartooq` Avannaata); await verified carbonatite complex coords.

Dataset: `International-Arctic/ArcticTradeLanes-Dataset` `arctic_industrial_facilities.csv` (`bb94955`). Builder: Zo `atlas-proj/build_atlas.py`. Static atlas aliases only — no App.tsx / SPA redeploy. Apex + www + Zo origin verified.

### CI additions

`scripts/check-industry-centroid-densify.mjs` Cycle E asserts each of the five ids left the coarse approx and sits in the OSM site band.

---

# Industry centroid densify (2026-09-08)

## Cycle D — Hammerfest Markoppneset vs Rypefjorden (live `2026-09-08T09:18:30Z`)

Last remaining industry 3-dp stack: Barents Blue (`ARC-FAC-344`) and GreenH (`ARC-FAC-358`) both sat on the Hammerfest town pin (~`70.6633, 23.682`). Densified to distinct OSM sites ~29 km apart.

| id | was | now | rationale / sources |
|----|-----|-----|---------------------|
| `ARC-FAC-344` Barents Blue | town `70.6633, 23.6822` | Markoppneset `70.4734, 24.2640` | OSM Nominatim Markoppneset (Markopp / Márgohppi); barentsblue.no Markoppneset / Kvalsund–Repparfjord municipal option |
| `ARC-FAC-358` GreenH Hammerfest | town `70.6633, 23.6821` | Rypefjorden `70.6370, 23.6757` | OSM Fjordaveien Indrefjord + Rypefjorden bay; EnergyWatch / GreenH Rypefjorden maritime bunkering |

Dataset: `arctic_industrial_facilities.csv`. Builder: Zo `atlas-proj/build_atlas.py`. Static atlas aliases only — no App.tsx / SPA redeploy. Apex + www + Zo origin verified.

---

# Industry centroid densify (earlier cycles)

Map UX: stacked `industry` pins on shared town centroids looked like duplicate facilities and bounced GIS users. This cycle densifies verifiable sites off the worst stacks.

## Changes (live atlas generated `2026-09-08T06:13:21Z`)

| id | was | now | rationale / sources |
|----|-----|-----|---------------------|
| `ARC-FAC-366` Narvik Green Ammonia | Narvik port `68.4386, 17.4279` | Bjerkvik `68.5492, 17.5571` | Statkraft + High North News: plant locality Bjerkvik / Lailasletta–Kvandal, not Narvik Havn; OSM Bjerkvik |
| `ARC-FAC-309` Arctic World Archive | Longyearbyen `78.2232, 15.6267` | Gruve 3 `78.2384, 15.4446` | Wikipedia/Wikidata + OSM `Gruve 3` |
| `ARC-FAC-367` Hotellneset diesel plant | near-town `78.2172, 15.6397` | Hotellneset `78.2486, 15.4880` | OSM Hotellneset; Sysselmesteren KU for Hotellneset plant |
| `ARC-FAC-305` Svalbard Energi utility | Longyearbyen centroid | `78.2465, 15.4920` | ops near Hotellneset plant (distinct from 367) |
| `ARC-FAC-311` Global Music Vault | Longyearbyen centroid | `78.2370, 15.4500` | Gruve 3 / Platåberget vault cluster (near AWA) |
| `ARC-FAC-310` Where2O / Tilsig office | Longyearbyen centroid | `78.2238, 15.6350` | town innovation-office offset |
| `ARC-FAC-318` Svalbard fibre landing | Longyearbyen centroid | `78.2275, 15.6080` | harbour / coastal terminal approach |
| `ARC-FAC-312` Kystutviklingssenteret | Kirkenes centroid | `69.7275, 30.0520` | Thon Senter / Storgata area |
| `ARC-FAC-313` beredskapshub | Kirkenes centroid | `69.7300, 30.0410` | civic/admin north offset |
| `ARC-FAC-360` Energy Cluster | Kirkenes centroid | `69.7270, 30.0505` | co-located with Kystutviklingssenteret, slight offset |
| `ARC-FAC-361` Maritime Industrial Cluster | Kirkenes centroid | `69.7225, 30.0565` | toward KILA logistics area |
| `ARC-FAC-306` Sitnasuak | Nome shared pin | `64.4998, -165.4035` | Front St pier / fuel terminal offset |
| `ARC-FAC-400` Emerald Nuclear Nome study | Nome shared pin | `64.5040, -165.4120` | harbour-approach study pin |

Dataset: `International-Arctic/ArcticTradeLanes-Dataset` `arctic_industrial_facilities.csv`. Builder: Zo `ArcticTradeLanes.com/atlas-proj/build_atlas.py`. Live aliases: `/atlas.4326.geojson` + `/data/atlas.4326.geojson` (apex + www).

## CI

```bash
node scripts/check-industry-centroid-densify.mjs atlas.4326.geojson
```

Neutral sourcing only — institutional OSM / Wikipedia / Statkraft / municipal pages. No editorial slant in labels.

---

## Follow-up densify (live atlas generated `2026-09-08T06:46:37Z`)

Unstacked remaining industry town-centroid piles (Murmansk ×4, Bakki/Húsavík ×2, Boden ×2, Arkhangelsk ×2). Neutral OSM / port-registry anchors only.

| id | was | now | rationale / sources |
|----|-----|-----|---------------------|
| `ARC-FAC-316` Rosatom Western TLU | Murmansk city `68.9585, 33.0827` | Fishing Port Tralovaya `68.9610, 33.0450` | Reoriented to Murmansk Sea Fishing Port infra (www1.ru + City Murmansk) |
| `ARC-FAC-336` Kola Farwater | same city centroid | MCSP `68.9841, 33.0610` | Ship agency at commercial port (= `ARC-PORT-001`) |
| `ARC-FAC-346` NSR year-round / SCF Arc7 | same city centroid | Atomflot campus `69.0135, 33.0936` | OSM Atomflot / Rosta campus — icebreaker co-management base |
| `ARC-FAC-386` Arctic Invest Shipping | same city centroid | MCSP offset `68.9860, 33.0550` | Murmansk home-port registry near MCSP |
| `ARC-FAC-332` Bakki Eco-Industrial Park | Húsavík `66.0446, -17.3383` | Bakki industrial `66.0703, -17.3322` | OSM industrial building Bakki / Norðausturvegur; bakki.nordurthing.is |
| `ARC-FAC-334` E-Valor e-fuel | same Húsavík pin | Bakki pad `66.0680, -17.3360` | MoU host site inside Bakki park (offset from 332) |
| `ARC-FAC-319` Stegra green steel | Boden town `65.8252, 21.6893` | Stegra stålverk `65.8096, 21.7941` | OSM `landuse=construction` STEGRA stålverk (Södra Svartbyn) |
| `ARC-FAC-368` Bodenxt / Industrial Park | — | kept Boden municipal `65.8252, 21.6893` | Municipal platform stays at town HQ |
| `ARC-FAC-342` Severny Proekt fleet | Arkhangelsk city | Sea Port `64.5393, 40.5185` | Fleet base = `ARC-PORT-002` |
| `ARC-FAC-385` Polar Trans Port rail terminal | same city pin | inland rail `64.5520, 40.5480` | Rear-base railway terminal N/E of seaport (msp29.ru) |

Dataset: `arctic_industrial_facilities.csv`. No App.tsx / SPA redeploy — static atlas aliases only (`/atlas.*` + `/data/atlas.*` on apex+www).

### CI additions

`scripts/check-industry-centroid-densify.mjs` now also asserts:

1. Murmansk industry quartet (`316/336/346/386`) no longer share one exact 4-dp coord.
2. Bakki pair (`332/334`) not on Húsavík town pin; both in Bakki industrial band.
3. Stegra (`319`) off Boden municipal centroid, inside Södra Svartbyn plant band.
4. Arkhangelsk pair (`342/385`) distinct 4-dp coords.

---

## Cycle C densify (live atlas generated `2026-09-08T08:33:51Z`)

Last exact industry stack on a shared town centroid: Utqiaġvik (Barrow) ASRC + UIC both at `-156.7887, 71.2906`. Densified to OSM Nominatim building addresses on Agvik Street (Browerville) — distinct corps, ~45 m apart, ~220–240 m off town pin.

| id | was | now | rationale / sources |
|----|-----|-----|---------------------|
| `ARC-FAC-011` ASRC HQ | town `-156.7887, 71.2906` | `71.2920855, -156.7836743` | OSM Nominatim way `8986804` — 1230 Agvik St; LinkedIn/ASRC list Utqiaġvik HQ at 1230 Agvik |
| `ARC-FAC-013` UIC HQ | same town pin | `71.2921895, -156.7849046` | OSM Nominatim way `500271960` — 1250 Agvik St; MapQuest/UIC corporate HQ |

Also restored crawler-friendly bare `/data/atlas.geojson` (+ root `/atlas.geojson`) as a **byte alias of** `atlas.4326.geojson` / `atlas.wgs84.geojson` (was SPA HTML). Apex + www verified JSON Content-Type.

Dataset: `arctic_industrial_facilities.csv`. Static atlas aliases only — no App.tsx / SPA redeploy.

### CI additions

`scripts/check-industry-centroid-densify.mjs` also asserts:

1. `ARC-FAC-011` / `ARC-FAC-013` are not on the Utqiaġvik town pin and do not share exact 4-dp coords.
2. Both sit in the Browerville Agvik St band (~71.291–71.293 N, ~156.786–156.782 W).
