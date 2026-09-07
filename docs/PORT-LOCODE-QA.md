# Port UN/LOCODE QA

Neutral GIS attribute QA for ArcticTradeLanes ports. Codes come from the UNECE UN/LOCODE code list (datasets/un-locode). Do not invent 5-letter codes.

## 2026-09-07 cycle (~15:30 MSK)

### Dropped alias / duplicate port rows
| id | reason |
|---|---|
| `ARC-PORT-037` | Barrow Port — same USBRW pin as `ARC-PORT-056` Utqiagvik (Barrow) Port |
| `ARC-PORT-103` | Kjøllefjord expansion with `NULL` LOCODE — duplicate of `ARC-PORT-095` |

### Filled / corrected LOCODEs (UNECE-verified)
| id | code | place |
|---|---|---|
| ARC-PORT-058 | USPMV | Port MacKenzie, AK |
| ARC-PORT-085 | USMTM | Metlakatla, AK |
| ARC-PORT-095 | NOKJF | Kjøllefjord (was NOKJL) |
| ARC-PORT-116/117/131 | USOME | Nome, AK (was USNOM — TX Nome collision) |
| ARC-PORT-119 | GLGOH | Nuuk logistics hub |
| ARC-PORT-128 | RUIDG | Indiga |
| ARC-PORT-133 | CACHV | Churchill (was incomplete CHV) |
| ARC-PORT-149 | SJBAR | Barentsburg |
| ARC-PORT-159 | NOSKN | Stokmarknes / Hadsel Havn |
| ARC-PORT-171 | RUVNN | Port Elga within Vanino seaport |

### Shipyard coordinate densify (distinct facilities)
| id | fix |
|---|---|
| ARC-SHIP-036 Waigaoqiao | 31.3667, 121.5667 (Pudong) |
| ARC-SHIP-037 Jiangnan Changxing | 31.3533, 121.6917 |

### Builder guard
`build_atlas._clean_unlocode` rejects `NULL` / 3-letter stubs / non-5-char codes and maps `USNOM`→`USOME`.

Live atlas after rebuild: **171 ports**, **1340** features, generated `2026-09-07T13:02:02Z`.

## 2026-09-07 cycle (~16:12 MSK)

### LOCODE typo
| id | was | now | note |
|---|---|---|---|
| `ARC-PORT-021` | `CAIqaluit` | `CAIQL` | UNECE CA+IQL Iqaluit (was city-name paste; builder rejected as non-5-char) |

### Builder guard
`build_atlas._clean_unlocode` also maps `CAIQALUIT` / `CAIQAL` / `CAIQA` → `CAIQL`.

Live atlas: **171 ports**, **1337** features, generated `2026-09-07T13:22:52Z`.
