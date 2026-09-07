# Port stack dedupe + UNECE LOCODE QA (2026-09-07)

## Problem
Map UX degraded when project/feasibility/agency rows shared the exact same WGS84 pin and UN/LOCODE as an operational harbour (Nome×5, Longyearbyen×3, Churchill×3, Luleå×3, etc.). Separately, Vardø was tagged with IATA `VAW` / typo `NOVAD` instead of UNECE **`NOVAO`**, and Primorsky krai “Novy Port” (Far East MTOR concept at ~42.6N) collided with Arctic Yamal Novy Port naming.

## Fixes (dataset + build_atlas)
1. **LOCODE fills/fixes** (UNECE `datasets/un-locode` verified):
   - `ARC-PORT-032` / `094` / `165`: `NOVAW`/`NOVAD` → **`NOVAO`** (Vardø)
   - Fills: Clyde River **`CACLR`**, Nikiski **`USNIK`**, Helguvík **`ISHEL`**, Bolungarvík **`ISBOL`**, Argentia **`CANWP`** (not CAARG=Arborg MB), Kalvåg **`NOKVG`**, Korf **`RUKRF`**
2. **Dropped** 15 non-facility / same-pin overlays from `ports.csv` (investment programmes, road reconstruction, feasibility studies, agency rows, Primorsky Novy Port).
3. **`build_atlas` soft-dedupe**: identical cleaned UN/LOCODE + rounded lon/lat keeps lowest `port_id`; extras land in `port_alias_drops` (8 remaining expansion rows filtered at build).
4. `_clean_unlocode` maps `NOVAW` → `NOVAO` (IATA leakage).

## Live
- https://arctictradelanes.com/data/atlas.manifest.json — ports **171→148**, features **1337→1314**, `crs_primary` 3996
- CI: `node scripts/check-port-stack.mjs [atlas.4326.geojson]`
- Related: `scripts/check-port-unlocode.mjs`

Politically neutral OSINT hygiene — no editorial layer changes.
