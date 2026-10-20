#!/usr/bin/env python3
"""gis-loop-1020-0913 (owner decision 2026-10-19): Reykjavík UN/LOCODE check against the official UNECE list.
UNECE UN/LOCODE Iceland (https://service.unece.org/trade/locode/is.htm) lists `IS REY  Reykjavík  function 1 (port)
status AC  date 0212  IATA REK  6409N 02157W`; there is no ISREK entry (REK is the IATA city code). Both
ARC-PORT-066 (Vör terminal building) and ARC-PORT-079 (Skarfabakki berth/quay) are set to ISREY; they stay separate,
cross-referenced features. No coordinate / confidence / last_verified change.
ports.csv: unlocode cell of 079 ISREK->ISREY; verification note appended to the sources cell of 066 and 079.
build_atlas.py: ARC-PORT-079 position_note `UN/LOCODE ISREK` -> `UN/LOCODE ISREY` + short note.
Line-level edits only (target rows rewritten; every other byte untouched). Idempotent via TAG.
Usage: python3 _patch_unlocode_0913.py [dry|apply] ROOT...
"""
import csv, glob, io, os, shutil, sys
TAG = "gis-loop-1020-0913"
mode, roots = sys.argv[1], sys.argv[2:]
SRC = ("UN/LOCODE check (owner decision 2026-10-19, " + TAG + "): official UNECE UN/LOCODE list for Iceland "
       "(service.unece.org/trade/locode/is.htm) gives IS REY = Reykjavík (function 1 port, status AC, 0212, IATA REK, "
       "6409N 02157W); no ISREK entry exists (REK is the IATA code)")
NOTE = {"ARC-PORT-079": SRC + "; unlocode ISREK -> ISREY. Same terminal as ARC-PORT-066 (both ISREY), kept separate",
        "ARC-PORT-066": SRC + "; unlocode ISREY confirmed (unchanged). Same terminal as ARC-PORT-079 (both ISREY), kept separate"}
WANT = {"ARC-PORT-079": ("ISREK", "ISREY"), "ARC-PORT-066": ("ISREY", "ISREY")}
def ser(row):
    b = io.StringIO(); csv.writer(b, lineterminator="").writerow(row); return b.getvalue()
def skip(rp):
    return "node_modules" in rp or ".bak" in rp or "/_b" in rp or "/bak" in rp or "/.git/" in rp
seen = set(); changed = []
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or skip(rp): continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(nl)
        hdr = next(csv.reader([lines[0]]))
        if "unlocode" not in hdr or "sources" not in hdr: print("SKIP header", rp); continue
        ku, ks, kla, klo = hdr.index("unlocode"), hdr.index("sources"), hdr.index("latitude"), hdr.index("longitude")
        hit = False
        for i, line in enumerate(lines):
            rid = line.split(",", 1)[0].strip('"')
            if rid not in WANT: continue
            row = next(csv.reader([line]))
            if ser(row) != line: print("WARN reserialize differs", rid, rp)
            old, new = WANT[rid]
            if TAG in row[ks] and row[ku] == new: print("already", rid, rp); continue
            if row[ku] not in (old, new): print("SKIP unexpected unlocode", rid, row[ku], rp); continue
            ll = (row[kla], row[klo])
            u0 = row[ku]; row[ku] = new
            row[ks] = (row[ks] + " | " + NOTE[rid]) if row[ks] else NOTE[rid]
            assert (row[kla], row[klo]) == ll
            lines[i] = ser(row); hit = True
            print("row", rid, u0, "->", new, "coords", ll, rp)
        if hit:
            changed.append(rp)
            if mode == "apply":
                shutil.copy2(rp, rp + ".bak-" + TAG)
                open(rp, "w", encoding="utf-8", newline="").write(nl.join(lines))
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or skip(rp): continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read(); s0 = s
        head = '            "ARC-PORT-079": {\n'
        if s.count(head) != 1: print("builder entry count", s.count(head), rp); continue
        a = s.index(head); b = s.index('"position_note": "', a); e = s.index('",\n', b)
        seg = s[b:e]
        if TAG in seg: print("builder already", rp); continue
        if "UN/LOCODE ISREK" not in seg: print("builder: no ISREK mention", rp)
        seg = seg.replace("UN/LOCODE ISREK", "UN/LOCODE ISREY")
        seg += ("; UN/LOCODE corrected ISREK -> ISREY per the official UNECE UN/LOCODE list for Iceland (IS REY = "
                "Reykjavík; ISREK is not listed, REK is the IATA code), " + TAG)
        s = s[:b] + seg + s[e:]
        print("builder 079 note", rp)
        if s != s0:
            changed.append(rp)
            if mode == "apply":
                shutil.copy2(rp, rp + ".bak-" + TAG); open(rp, "w", encoding="utf-8").write(s)
print(mode, "files changed", len(changed))
for c in changed: print("  ", c)
