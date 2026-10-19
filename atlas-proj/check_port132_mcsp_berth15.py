#!/usr/bin/env python3
"""Lock: ARC-PORT-132 Murmansk NSR container terminal at MCSP berth 15 densify."""
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EXPECT = ("68.9846667", "33.0631667")
errors = []
for p in ROOT.rglob("ports.csv"):
    if "node_modules" in str(p) or ".bak" in p.name: continue
    for row in csv.DictReader(p.open(encoding="utf-8")):
        if row.get("port_id") == "ARC-PORT-132":
            if (row["latitude"], row["longitude"]) != EXPECT:
                errors.append(f"{p}: {row['latitude']}/{row['longitude']}")
            break
for atlas in [ROOT / "data" / "atlas.geojson", ROOT / "atlas-proj" / "atlas.geojson"]:
    if not atlas.exists(): continue
    d = json.load(atlas.open())
    for f in d["features"]:
        props = f.get("properties") or {}
        if props.get("id") == "ARC-PORT-132":
            lon, lat = f["geometry"]["coordinates"][:2]
            if abs(lat - float(EXPECT[0])) > 1e-5 or abs(lon - float(EXPECT[1])) > 1e-5:
                errors.append(f"{atlas}: {lat}/{lon}")
            if props.get("position_quality") != "facility_site":
                errors.append(f"{atlas}: position_quality={props.get('position_quality')}")
            break
if errors:
    print("FAIL"); print("\n".join(errors)); sys.exit(1)
print("OK ARC-PORT-132", EXPECT[0], EXPECT[1], "facility_site")
