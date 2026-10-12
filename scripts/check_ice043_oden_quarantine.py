#!/usr/bin/env python3
"""Lock check: ARC-ICE-043 I/B Oden must stay quarantined (gis-ice043-1535).

ARC-ICE-043 vessel_name literally declares "same as ARC-ICE-033". Both rows are
the Swedish Maritime Administration Polar Class 2 icebreaker Oden (built 1988).
Builder drops any icebreaker whose name matches ``same as ARC-ICE-\\d+``
(toggle ATL_ICE_SAME_AS_DROP=0). Keep ARC-ICE-033 as the sole map feature.

Usage: python3 scripts/check_ice043_oden_quarantine.py [atlas.wgs84.geojson]
"""
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
if "ARC-ICE-043" in feats:
    f = feats["ARC-ICE-043"]
    lon, lat = f["geometry"]["coordinates"][:2]
    errs.append(
        f"ARC-ICE-043 still on atlas at {lat},{lon} — expected quarantine drop "
        f"(duplicate of ARC-ICE-033 Oden; vessel_name declared same-as)"
    )
f33 = feats.get("ARC-ICE-033")
if not f33:
    errs.append("ARC-ICE-033 missing (canonical Oden pin)")
else:
    name = (f33.get("properties") or {}).get("name") or ""
    if "Oden" not in name:
        errs.append(f"ARC-ICE-033 unexpected name: {name!r}")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = f33["geometry"]["coordinates"][:2]
print(
    f"OK ARC-ICE-043 quarantined (absent); ARC-ICE-033 Oden kept at "
    f"{lat:.5f},{lon:.5f} (layer={f33['properties'].get('layer')})"
)
