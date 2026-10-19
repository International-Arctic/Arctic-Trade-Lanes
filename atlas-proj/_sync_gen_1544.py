#!/usr/bin/env python3
"""gis-loop-1019-1544 (from _sync_gen_0913): replace every atlas copy that is byte-identical to the previous generation
(2026-10-14T07:26:36Z) with the new build. Files not matching the old md5 are left alone."""
import hashlib, os, shutil, sys

NEW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/atl_new_0913"
REF = sys.argv[3] if len(sys.argv) > 3 else "/home/workspace/ArcticTradeLanes.com/arctic-trade-lanes"
ROOTS = ["/home/workspace/ArcticTradeLanes.com", "/home/workspace/ArcticTradeLanes-Dataset"]
NAMES = ["atlas.3996.geojson", "atlas.4326.geojson", "atlas.wgs84.geojson", "atlas.geojson", "atlas.manifest.json"]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

old = {n: md5(os.path.join(REF, n)) for n in NAMES}
new = {n: os.path.join(NEW, n) for n in NAMES}
for n in NAMES:
    assert os.path.getsize(new[n]) > 0, n
mode = sys.argv[2] if len(sys.argv) > 2 else "dry"
hits = []
for r in ROOTS:
    for dp, dns, fns in os.walk(r):
        dns[:] = [d for d in dns if d not in ("node_modules", ".git")]
        for fn in fns:
            if fn in old:
                p = os.path.join(dp, fn)
                if os.path.islink(p):
                    continue
                try:
                    if md5(p) == old[fn]:
                        hits.append((p, fn))
                except OSError:
                    pass
print("old-gen copies:", len(hits), "dirs:", len({os.path.dirname(p) for p, _ in hits}))
if mode == "apply":
    for p, fn in hits:
        tmp = p + ".tmp-1544"
        shutil.copyfile(new[fn], tmp)
        os.replace(tmp, p)
    print("replaced", len(hits))
