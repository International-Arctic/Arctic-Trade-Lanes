#!/usr/bin/env python3
"""gis-loop-1019-1721: finalize + sync new atlas generation.

1) Overlay: in the fresh parent-builder output (/tmp/atl_new_1721, has ref/ne_10m_land -> 25 water-routed lanes + land-mask fan),
   keep the currently-live (13:47:29Z) versions of ARC-RAIL-008, ARC-RAIL-009, ARC-SHIP-073 (neutral wording) and ARC-PORT-157,
   so the net change vs live = ARC-PORT-132 densify + restoring the 25 water-routed lanes that the 13:47 nested build dropped
   (nested atlas-proj has no ref/ne_10m_land.geojson, so lane water routing silently skipped).
2) Sync: replace every atlas copy byte-identical to the 12:50:43Z or 13:47:29Z generation.
"""
import hashlib, json, os, shutil, sys

NEW = "/tmp/atl_new_1721"
LIVE_DIR = "/home/workspace/ArcticTradeLanes.com/arctic-trade-lanes/atlas-proj"   # 13:47:29Z gen
G1250_DIR = "/home/workspace/ArcticTradeLanes.com/arctic-trade-lanes"             # 12:50:43Z gen
ROOTS = ["/home/workspace/ArcticTradeLanes.com", "/home/workspace/ArcticTradeLanes-Dataset"]
NAMES = ["atlas.3996.geojson", "atlas.4326.geojson", "atlas.wgs84.geojson", "atlas.geojson", "atlas.manifest.json"]
KEEP = {"ARC-RAIL-008", "ARC-RAIL-009", "ARC-SHIP-073", "ARC-PORT-157"}
mode = sys.argv[1] if len(sys.argv) > 1 else "dry"


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# --- overlay ---
for n in NAMES[:4]:
    p = os.path.join(NEW, n)
    src = "atlas.3996.geojson" if n == "atlas.3996.geojson" else "atlas.4326.geojson"
    live = json.load(open(os.path.join(LIVE_DIR, src)))
    L = {f["properties"].get("id"): f for f in live["features"]}
    d = json.load(open(p))
    k = 0
    for i, f in enumerate(d["features"]):
        fid = f["properties"].get("id")
        if fid in KEEP and fid in L:
            d["features"][i] = L[fid]; k += 1
    assert k == len(KEEP), (n, k)
    if mode == "apply":
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(d, fh)
    print("overlay", n, k)

old = set()
for dd in (LIVE_DIR, G1250_DIR):
    for n in NAMES:
        old.add((n, md5(os.path.join(dd, n))))
hits = []
for r in ROOTS:
    for dp, dns, fns in os.walk(r):
        dns[:] = [x for x in dns if x not in ("node_modules", ".git")]
        for fn in fns:
            if fn in NAMES:
                p = os.path.join(dp, fn)
                if os.path.islink(p):
                    continue
                try:
                    if (fn, md5(p)) in old:
                        hits.append((p, fn))
                except OSError:
                    pass
print("old-gen copies:", len(hits), "dirs:", len({os.path.dirname(p) for p, _ in hits}))
if mode == "apply":
    for p, fn in hits:
        tmp = p + ".tmp-1721"
        shutil.copyfile(os.path.join(NEW, fn), tmp)
        os.replace(tmp, p)
    print("replaced", len(hits))
