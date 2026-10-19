#!/usr/bin/env python3
"""gis-loop-1019-1837 (owner decisions 2026-10-19):
A) Sync Dataset CSV text for ARC-RAIL-008, ARC-RAIL-009, ARC-SHIP-073 to the live neutral wording (live atlas = official
   text). RAIL-009 keeps the Dataset's own latitude/longitude, confidence (93) and last_verified (2026-09-06); only text
   columns are taken from live. Removes the need for the per-build live overlay used in earlier cycles.
B) Cross-reference ARC-PORT-079 (Skarfabakki berth) and ARC-PORT-066 (Vör terminal building) as the same Reykjavík
   cruise terminal; they stay SEPARATE features (not merged). Appends a note to ports.csv sources and to both
   builder position_note entries. No coordinate changes.
Line-level edits only (target rows rewritten; every other byte untouched). Idempotent via TAG.
Usage: python3 _patch_neutral_xref_1837.py LIVE_WGS84_GEOJSON [dry|apply] ROOT...
"""
import csv, glob, io, json, os, shutil, sys

TAG = "gis-loop-1019-1837"
live_path, mode, roots = sys.argv[1], sys.argv[2], sys.argv[3:]
L = {f["properties"]["id"]: f["properties"] for f in json.load(open(live_path, encoding="utf-8"))["features"]}
MAPS = {
    "rail_corridors.csv": ({"program_name": "name", "country": "country", "city": "city", "program_type": "type",
                            "key_benefits": "benefits", "eligibility": "eligibility", "operator": "operator",
                            "status": "status", "official_url": "url", "sources": "sources"},
                           ["ARC-RAIL-008", "ARC-RAIL-009"]),
    "shipbuilding_facilities.csv": ({"shipyard_name": "name", "location": "location", "country": "country",
                                     "specialization": "specialization", "arctic_vessel_capability": "arctic_capable"},
                                    ["ARC-SHIP-073"]),
}
X079 = ("CROSS-REF (owner decision 2026-10-19, " + TAG + "): same Reykjavík cruise terminal as ARC-PORT-066 (Vör "
        "terminal building, OSM way/1391146178, ~0.15 km NW); kept as a separate feature, not merged: ARC-PORT-079 = "
        "Skarfabakki berth/quay, ARC-PORT-066 = Vör terminal building")
X066 = ("CROSS-REF (owner decision 2026-10-19, " + TAG + "): same Reykjavík cruise terminal as ARC-PORT-079 "
        "(Skarfabakki berth, OSM way/108336302, ~0.15 km SE); kept as a separate feature, not merged: ARC-PORT-066 = "
        "Vör terminal building, ARC-PORT-079 = Skarfabakki berth/quay")
XREF = {"ARC-PORT-079": X079, "ARC-PORT-066": X066}
# RAIL-009: owner keeps the Zo Dataset's newer verified date / confidence / coordinates (text from live)
KEEP = {"ARC-RAIL-009": {"latitude": "62.8981", "longitude": "135.3215", "confidence": "93", "last_verified": "2026-09-06"}}

def ser(row):
    b = io.StringIO(); csv.writer(b, lineterminator="").writerow(row); return b.getvalue()

def skip(rp):
    return "node_modules" in rp or ".bak" in rp or "/_b" in rp or "/bak" in rp or "/.git/" in rp

seen = set(); changed = []
for r in roots:
    for name in list(MAPS) + ["ports.csv"]:
        for p in glob.glob(r + "/**/" + name, recursive=True):
            rp = os.path.realpath(p)
            if rp in seen or skip(rp): continue
            seen.add(rp)
            raw = open(rp, encoding="utf-8", newline="").read()
            nl = "\r\n" if "\r\n" in raw else "\n"
            lines = raw.split(nl)
            hdr = next(csv.reader([lines[0]]))
            hit = False
            for i, line in enumerate(lines):
                rid = line.split(",", 1)[0].strip('"')
                if name == "ports.csv":
                    if rid not in XREF: continue
                    row = next(csv.reader([line]))
                    if ser(row) != line: print("WARN reserialize differs", rid, rp)
                    k = hdr.index("sources")
                    if TAG in row[k]: print("already", rid, rp); continue
                    row[k] = (row[k] + " | " + XREF[rid]) if row[k] else XREF[rid]
                    lines[i] = ser(row); hit = True; print("xref", rid, rp)
                    continue
                cmap, ids = MAPS[name]
                if rid not in ids: continue
                row = next(csv.reader([line]))
                if ser(row) != line: print("WARN reserialize differs", rid, rp)
                diffs = []
                for col, prop in cmap.items():
                    k = hdr.index(col); want = L[rid].get(prop, "")
                    if row[k] != want:
                        diffs.append((col, len(row[k]), len(want))); row[k] = want
                for col, want in KEEP.get(rid, {}).items():
                    k = hdr.index(col)
                    if row[k] != want: diffs.append((col, row[k], want)); row[k] = want
                if diffs:
                    lines[i] = ser(row); hit = True
                    print("neutral", rid, rp, diffs, "kept conf/verified/lat/lon:",
                          row[hdr.index("confidence")], row[hdr.index("last_verified")],
                          row[hdr.index("latitude")], row[hdr.index("longitude")])
                else:
                    print("in-sync", rid, rp)
            if hit:
                changed.append(rp)
                if mode == "apply":
                    shutil.copy2(rp, rp + ".bak-" + TAG)
                    open(rp, "w", encoding="utf-8", newline="").write(nl.join(lines))

# builder position_note cross-refs
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or skip(rp): continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read(); s0 = s
        for pid, note in XREF.items():
            head = '            "' + pid + '": {\n'
            if s.count(head) != 1: print("builder entry count", pid, s.count(head), rp); continue
            a = s.index(head); b = s.index('"position_note": "', a); e = s.index('",\n', b)
            if TAG in s[b:e]: print("builder already", pid, rp); continue
            if s.index("},", a) < b: print("builder entry lacks position_note", pid, rp); continue
            s = s[:e] + "; " + note + s[e:]
            print("builder xref", pid, rp)
        if s != s0:
            changed.append(rp)
            if mode == "apply":
                shutil.copy2(rp, rp + ".bak-" + TAG); open(rp, "w", encoding="utf-8").write(s)
print(mode, "files changed", len(changed))
for c in changed: print("  ", c)
