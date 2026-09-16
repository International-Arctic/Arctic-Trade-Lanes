# ARC-SHIP-005 Onega → Petrozavodsk densify (2026-09-16)

**Problem:** Onega Shipyard was pinned at Arkhangelsk city soft-coords `64.54,40.52` (wrong city).

**Fix:** Move to OSM [way/41865465](https://www.openstreetmap.org/way/41865465) (Онежский судостроительно-судоремонтный завод Конструкторские бюро) centroid `61.7829435,34.4023099` in Petrozavodsk on Lake Onega. Wikidata [Q27346605](https://www.wikidata.org/wiki/Q27346605) Onego Shipyard.

**Also:** ARC-SHIP-010 Helsinki Shipyard densified onto [way/4260855](https://www.openstreetmap.org/way/4260855) `60.15649896,24.92729275` (Hietalahti). ARC-SHIP-009 Arctech left alone to avoid a new soft-stack on the same complex.

**CI:** `scripts/check-ship005-onega-petrozavodsk-densify.mjs`, `scripts/check-ship010-helsinki-hietalahti-densify.mjs`.

Politically neutral — OSM/Wikidata geometry only.
