# Arctic Trade Lanes

Open GIS OSINT scaffolding for **[ArcticTradeLanes.com](https://arctictradelanes.com)** — Northern Sea Route, Polar Silk Road, and Arctic-8 economic activity (2026–2036).

Owner: [Aleksei Dolgikh](https://x.com/alexdolbun) (`@alexdolbun`) · Org: [International-Arctic](https://github.com/International-Arctic)

## Live product

| Surface | URL |
|---------|-----|
| Map + OSINT | https://arctictradelanes.com |
| Pricing / x402 | https://arctictradelanes.com/pricing |
| Agent discovery | https://arctictradelanes.com/.well-known/x402.json |
| Atlas (EPSG:3996) | https://arctictradelanes.com/atlas.3996.geojson |
| Alpha API status | https://arctictradelanes.com/api/alpha/status |

**Projection:** EPSG:3996 (IBCAO Polar Stereographic) primary.

## Commercial rails (cashflow first)

- **Free** — atlas + map; 10 route runs/day/IP
- **Pro** — `$49`/mo or **`5 USDC`** per run via x402 on **Base**
- **Enterprise** — custom / SLA — contact `@alexdolbun`

Settlement wallet (USDC Base): `0x211D91beD006f7bB3Eaf97496260a8F905298Cea`  
Bankr: https://bankr.bot?ref=um-radar · ref `RN982CZZ-BNKR`

Paid Panstar SKU example:

```bash
curl -sS -H 'x402-payment: x402:0x211D91beD006f7bB3Eaf97496260a8F905298Cea:5' \
  'https://arctictradelanes.com/api/x402/fulfill?slug=panstar-korea-nsr'
```

Native `$ATL` is **not** minted until paid waypoints + cashflow are proven.

## Repo layout

```
LICENSE
README.md
CONTRIBUTING.md
CITATION.cff
docs/commercial.md
docs/DATA.md
dataset/README.md          # full CSV sync lands here (Zo is control plane)
info/                      # non-canonical research notes (quarantined)
```

Control plane for production data remains **Zo** (`ArcticTradeLanes-Dataset` + `ArcticTradeLanes.com`). This org is the public OSS face.

## Corridors

Russia (AZRF / NSR) · Canada North · Alaska (USA) · Korea / Japan / China (Polar Silk Road) · Nordics / Greenland / Iceland.



## GIS quality + community

Standing quality bar: [`docs/GIS-QUALITY.md`](docs/GIS-QUALITY.md) · client filter spec: [`docs/CLIENT-GEO-FILTER.md`](docs/CLIENT-GEO-FILTER.md)

**OSS engineers with Arctic / polar GIS interest:** open Issues labeled `help wanted` / `good first issue`, or start from [CONTRIBUTING.md](CONTRIBUTING.md). Companion dataset: [ArcticTradeLanes-Dataset](https://github.com/International-Arctic/ArcticTradeLanes-Dataset). Collaborate page: https://arctictradelanes.com/collaborate

## License

Apache-2.0 for scaffolding. Dataset packages may use CC-BY-4.0 / ODbL — see `dataset/README.md`.


## Docs
- [Atlas download aliases](docs/ATLAS-DOWNLOAD-ALIASES.md)
