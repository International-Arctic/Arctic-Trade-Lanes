# GIS Quality Loop — gis-fac352-1146 (2026-10-12 ~11:46 MSK)

## Win: ARC-FAC-352 duplicate quarantine

Soft industry audit (0.05/0.1° grid, no `position_quality`) found **2** remaining coarse pins after soft-integer audit cleared: **ARC-FAC-008** Sovinoye/Shelf-M (deposit-area centroid; no public precise site — left alone) and **ARC-FAC-330** Sarfartoq (already on GEUS 66°30′N / 51°15′W — authoritative).

**ARC-FAC-352** NunaGreen Utoqqarmiut Kangerluarsunnguat (Buksefjorden) Hydropower Project at soft `64.16 / -51.60` is a **duplicate** of densified **ARC-FAC-005** (same expansion, 76.9 MW; GEM wiki `63.9211 / -50.8909`; Wikidata Q1366227 P625 `63.92111111 / -50.89055556`). Soft pin was **~43.6 km NW** of FAC-005.

Quarantine (SHIP-022 / Vard-025 pattern): cleared `latitude`/`longitude` on FAC-352 across Dataset + site CSV mirrors; atlas builder drops empty-coord rows. FAC-005 remains the sole Buksefjorden map feature.

## Live
- Atlas gen `2026-10-12T08:52:27Z`, **1318** features (was 1319); industry **109** (was 110).
- Geometry change: FAC-352 removed only.
- Soft-integer audit still **0**; coarse-industry remaining: FAC-008 (intentional deposit centroid), FAC-330 (GEUS grid).
- Lock: `scripts/check_fac352_buksefjorden_quarantine.py`
- CSV backups: `*.bak-gis-fac352-*`
