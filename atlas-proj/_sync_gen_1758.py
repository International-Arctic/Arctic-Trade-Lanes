#!/usr/bin/env python3
"""gis-loop-1019-1758: overlay + regression gate + sync for the ARC-PORT-079 Skarfabakki densify.
1) Overlay: keep live (14:30:44Z) ARC-RAIL-008/009 + ARC-SHIP-073 (neutral wording; Dataset inputs still carry older text).
2) Gate: every feature except ARC-PORT-079 must be identical to live (ids, order, props, geometry); 1317 feats;
   25 water_routed lanes; 563 position_fan_mask; 101 ship water fans (display_offset/anchor unchanged via identity);
   today's fixed ports byte-equal.
3) apply: copy to out/, then replace every atlas copy byte-identical to the 14:30:44Z gen under ROOTS.
"""
import hashlib, json, os, shutil, sys
NEW = "/tmp/atl_new_1758"
LIVE_DIR = "/home/workspace/ArcticTradeLanes.com/atlas-proj/out"
ROOTS = ["/home/workspace/ArcticTradeLanes.com", "/home/workspace/ArcticTradeLanes-Dataset"]
NAMES = ["atlas.3996.geojson", "atlas.4326.geojson", "atlas.wgs84.geojson", "atlas.geojson", "atlas.manifest.json"]
KEEP = {"ARC-RAIL-008", "ARC-RAIL-009", "ARC-SHIP-073"}
TARGET = "ARC-PORT-079"
FIXED = ["ARC-PORT-104", "ARC-PORT-107", "ARC-PORT-113", "ARC-PORT-114", "ARC-PORT-119", "ARC-PORT-132", "ARC-PORT-134",
         "ARC-PORT-140", "ARC-PORT-157", "ARC-PORT-158", "ARC-PORT-159", "ARC-PORT-160", "ARC-PORT-165", "ARC-PORT-066"]
mode = sys.argv[1] if len(sys.argv) > 1 else "dry"
def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
old_md5 = {n: md5(os.path.join(LIVE_DIR, n)) for n in NAMES}
bad = 0
for n in NAMES[:4]:
    src = "atlas.3996.geojson" if n == "atlas.3996.geojson" else "atlas.4326.geojson"
    live = json.load(open(os.path.join(LIVE_DIR, src)))
    L = {f["properties"].get("id"): f for f in live["features"]}
    p = os.path.join(NEW, n); d = json.load(open(p))
    k = 0
    for i, f in enumerate(d["features"]):
        fid = f["properties"].get("id")
        if fid in KEEP: d["features"][i] = L[fid]; k += 1
    assert k == len(KEEP), (n, k)
    # gate
    tl = {x: v for x, v in live.items() if x not in ("features", "generated")}
    tn = {x: v for x, v in d.items() if x not in ("features", "generated")}
    if tl != tn: print("GATE top-level differs", n, set(tl) ^ set(tn)); bad = 1
    ids_l = [f["properties"].get("id") for f in live["features"]]; ids_n = [f["properties"].get("id") for f in d["features"]]
    if ids_l != ids_n: print("GATE id order differs", n); bad = 1
    diffs = [a["properties"].get("id") for a, b in zip(live["features"], d["features"]) if a != b]
    if diffs != [TARGET]: print("GATE unexpected diffs", n, diffs); bad = 1
    N = {f["properties"].get("id"): f for f in d["features"]}
    for fid in FIXED:
        if N[fid] != L[fid]: print("GATE fixed port changed", n, fid); bad = 1
    wr = sum(1 for f in d["features"] if f["properties"].get("geometry_quality") == "water_routed")
    fm = sum(1 for f in d["features"] if "position_fan_mask" in f["properties"])
    do = sum(1 for f in d["features"] if "display_offset" in f["properties"])
    do_l = sum(1 for f in live["features"] if "display_offset" in f["properties"])
    print(n, "feats", len(d["features"]), "diffs", diffs, "water_routed", wr, "fan_mask", fm, "display_offset", do, "/live", do_l,
          "gen", d.get("generated"), "crs", d.get("crs", {}).get("properties", {}).get("name"))
    if len(d["features"]) != 1317 or wr != 25 or fm != 563 or do != do_l: print("GATE counts", n); bad = 1
    t = N[TARGET]; print("  target", t["geometry"]["coordinates"], t["properties"].get("position_quality"))
    if mode == "apply" and not bad:
        with open(p, "w", encoding="utf-8") as fh: json.dump(d, fh)
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
    tmp = p + ".tmp1758"; shutil.copy2(os.path.join(NEW, os.path.basename(p)), tmp); os.replace(tmp, p)
print("synced copies", len(hits), "dirs", len({os.path.dirname(h) for h in hits}))
