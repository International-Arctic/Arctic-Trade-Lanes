#!/usr/bin/env python3
"""gis-loop-1020-1152: regression gate + sync for the metadata-only ARC-PORT-101 builder stamp
(position_quality=facility_site, position_note, position_anchor; adapted from _sync_gen_1120.py).
Gate (3996/4326/wgs84/geojson): ids+order identical; top-level identical except `generated`; diffs only in
ARC-PORT-101 properties (NO geometry change vs the 08:30:55Z gen); MUST_EQ features equal to live; 1317 feats; 25 water_routed;
563 position_fan_mask; display_offset count == live; previously fixed ports (incl. 101) geometry-equal.
apply: copy to out/, then replace every atlas copy byte-identical to the 08:30:55Z gen under ROOTS.
"""
import hashlib, json, os, shutil, sys
NEW = "/tmp/atl_new_1152"
LIVE_DIR = "/home/workspace/ArcticTradeLanes.com/atlas-proj/out"
ROOTS = ["/home/workspace/ArcticTradeLanes.com", "/home/workspace/ArcticTradeLanes-Dataset"]
NAMES = ["atlas.3996.geojson", "atlas.4326.geojson", "atlas.wgs84.geojson", "atlas.geojson", "atlas.manifest.json"]
ALLOWED = {"ARC-PORT-101": {"position_quality", "position_note", "position_anchor"}}  # NO GEOMETRY
MUST_EQ = ["ARC-PORT-014", "ARC-PORT-139", "ARC-PORT-135", "ARC-PORT-034", "ARC-PORT-066", "ARC-PORT-079", "ARC-PORT-068", "ARC-PORT-083", "ARC-PORT-148", "ARC-RAIL-008", "ARC-RAIL-009", "ARC-SHIP-073"]
FIXED = ["ARC-PORT-%03d" % n for n in (12, 14, 25, 36, 39, 53, 65, 66, 79, 83, 89, 93, 101, 104, 107, 109, 113, 114, 119, 132, 134, 135, 139, 140,
                                        157, 158, 159, 160, 165)]
mode = sys.argv[1] if len(sys.argv) > 1 else "dry"
def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
old_md5 = {n: md5(os.path.join(LIVE_DIR, n)) for n in NAMES}
print("live out md5", {k: v[:8] for k, v in old_md5.items()})
bad = 0
for n in NAMES[:4]:
    live = json.load(open(os.path.join(LIVE_DIR, n)))
    L = {f["properties"].get("id"): f for f in live["features"]}
    d = json.load(open(os.path.join(NEW, n)))
    N = {f["properties"].get("id"): f for f in d["features"]}
    tl = {x: v for x, v in live.items() if x not in ("features", "generated")}
    tn = {x: v for x, v in d.items() if x not in ("features", "generated")}
    if tl != tn: print("GATE top-level differs", n, [k for k in set(tl) | set(tn) if tl.get(k) != tn.get(k)]); bad = 1
    if [f["properties"].get("id") for f in live["features"]] != [f["properties"].get("id") for f in d["features"]]:
        print("GATE id order differs", n); bad = 1
    diffs = {}
    for a, b in zip(live["features"], d["features"]):
        if a != b:
            fid = a["properties"].get("id")
            keys = {k for k in set(a["properties"]) | set(b["properties"]) if a["properties"].get(k) != b["properties"].get(k)}
            if a["geometry"] != b["geometry"]: keys.add("GEOMETRY")
            if a.keys() != b.keys(): keys.add("FEATURE_KEYS")
            diffs[fid] = keys
    for fid, keys in diffs.items():
        if fid not in ALLOWED or not keys <= ALLOWED[fid]: print("GATE unexpected diff", n, fid, sorted(keys)); bad = 1
    for fid in MUST_EQ:
        if N[fid] != L[fid]: print("GATE must-equal changed", n, fid); bad = 1
    for fid in FIXED:
        if fid in L and N[fid]["geometry"] != L[fid]["geometry"]: print("GATE fixed port moved", n, fid); bad = 1
    wr = sum(1 for f in d["features"] if f["properties"].get("geometry_quality") == "water_routed")
    fm = sum(1 for f in d["features"] if "position_fan_mask" in f["properties"])
    do = sum(1 for f in d["features"] if "display_offset" in f["properties"])
    do_l = sum(1 for f in live["features"] if "display_offset" in f["properties"])
    print(n, "feats", len(d["features"]), "diffs", {k: sorted(v) for k, v in diffs.items()}, "water_routed", wr,
          "fan_mask", fm, "display_offset", do, "/live", do_l, "gen", d.get("generated"),
          "crs", d.get("crs", {}).get("properties", {}).get("name"))
    if len(d["features"]) != 1317 or wr != 25 or fm != 563 or do != do_l: print("GATE counts", n); bad = 1
    if N["ARC-PORT-101"]["properties"].get("position_quality") != "facility_site": print("GATE 101 pq missing", n); bad = 1
    g = N["ARC-PORT-101"]["geometry"]; print("   ARC-PORT-101", L["ARC-PORT-101"]["geometry"]["coordinates"], "->", g["coordinates"], N["ARC-PORT-101"]["properties"].get("position_quality"))
    if "4326" in n or "wgs84" in n or n == "atlas.geojson":
        c = g["coordinates"]
        if abs(c[1] - 70.466932) > 1e-6 or abs(c[0] - -68.597123) > 1e-6: print("GATE 101 coords wrong", n, c); bad = 1
        for pid, (la, lo) in {"ARC-PORT-139": (69.6757237, 18.989445), "ARC-PORT-135": (61.764832, 4.8758683), "ARC-PORT-157": (69.0451678, 33.0406397), "ARC-PORT-079": (64.1550151, -21.8620629), "ARC-PORT-083": (66.5576559, -52.0679314)}.items():
            cc = N[pid]["geometry"]["coordinates"]
            if abs(cc[1] - la) > 1e-6 or abs(cc[0] - lo) > 1e-6: print("GATE fixed coord wrong", n, pid, cc); bad = 1
print("GATE", "FAIL" if bad else "PASS")
if bad or mode != "apply": sys.exit(1 if bad else 0)
for n in NAMES: shutil.copy2(os.path.join(NEW, n), os.path.join(LIVE_DIR, n))
old = set(old_md5.items()); hits = []
for r in ROOTS:
    for dp, dns, fns in os.walk(r):
        dns[:] = [x for x in dns if x not in ("node_modules", ".git")]
        for fn in fns:
            if fn in NAMES:
                p = os.path.join(dp, fn)
                if os.path.islink(p) or os.path.realpath(dp) == os.path.realpath(LIVE_DIR): continue
                try:
                    if (fn, md5(p)) in old: hits.append(p)
                except Exception: pass
for p in hits:
    tmp = p + ".tmp1152"; shutil.copy2(os.path.join(NEW, os.path.basename(p)), tmp); os.replace(tmp, p)
print("synced copies", len(hits), "dirs", len({os.path.dirname(h) for h in hits}))
