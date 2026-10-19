#!/usr/bin/env python3
"""gis-loop-1019-1721: restore ARC-PORT-157 Murmansk Arctic Gate Marine Terminal densified row (gis-port157-0943,
Mishukovo OSM way/129872684 69.0451678/33.0406397, conf 88, last_verified 2026-10-13) in every ports.csv copy that
regressed to the soft 68.9800/33.0000 (conf 75). The densified row is what the live atlas and GitHub
ArcticTradeLanes-Dataset already carry; only the CSV copies had drifted back."""
import base64, csv, glob, gzip, io, json, os, shutil, sys
ROW = json.loads(gzip.decompress(base64.b64decode(
    "H4sIAMsq1moC/4VVbW/iOBD+K6NKK4EUkwQohaL7QNlVxW1p90pvT6e91cpJhuBNYmdth27uQ3/7jRMO0l7VQ0LyC2aet7G/nC3ul+zT3f0DC88vzjw4W1e64NJksNCxFTFcc4uw5lpIhAfUhZA8h95aaZOp+rTyWWllOR3KrMhEH/6qhkE4hivMua6M4JJFPM4wgY8q53DFayiq3IpCJXR4V0WutIOyXD38yYIgdPP7ytBJN5rMBsH4PJxcTN1sNKJZMBnNGsDd73AaNB83XsXIthrxVLF3XeVb2FiNvOjDIxoLZqc0gkSuYS3MrsrUXs0hqvLMAyVyKLVKqtgaD2IlLScRNI23qK3Ixd80gV5JvM2u/xJKo+XbKsHNzZKkfKFtR/ejjLPZO7hRqTBu5wOBSOv28EHfvgfhO7jFPBfkVV5zrfZ8DinKQSL0ABYy0VjDVSU5MXTQPmmxd872/uvQr58bMl+oHCuVthQMFszGo0u426zhkdd+OJxNL4aT6fgkGux4kaOFW+VYkLFw8sw/GTYHtd2CUVsLk+lgRnY1m/SB3tPFYAxZ0Z+/Gb0y51J2c/SGj6Uywgolv/2oeC5s/YtBa3MsUNpvtINzuF5t4Ld2kwRWJQyD4YSFAQtH8BTMLscjWG8+fgUhLeot/zmIVeFLfDRa0cCqkhmrtEDjh0E4GY/8rqB0ao9u37zJiIz0XnPXO3F8Tszr9o7Lqk9R9Y8B9WB4zkbBGqxfa0jQiFRSZoUmnWKuUwVPxHLqgUZXEzWpuSg1hI782HOpAUrNi9CQLXaHEdcknlGRQb1H3cghZFIZq2vGZcKwge9HuKNlxnPMDC1rllcZdQnKTBmWavdLFy3m3GRCsuJw6zDKHGeJStKaJchz5sBjwqLaLQtDR2Oa4k9iuxex9UOKWBD+74XkARnBo5wkfMG2KsEqUozk6jZ5I2mjbafZvddSR8Jo3CpdDFwufJRE/thSLUmtvmNsn/HkbhlZmxAXSAoST6kfeUp3lltoULYY//XTg+dn+i7iVOu7qjRxJgDWP1aIKpEnbQczgscOqKCXKnJOqoPBApY7EQnTKCQKCmjSqkHh8eA9xlhE2AIheYqSmpw6ipA0114jEdDfd276NmT9Adwu1h/g/WqzWF+trn9fPKzubi8pWVRGxha2WhVwfH2CUQg3fC85LBW5d3pp7hVFNCZ03AkuktOl2O0pYVw6OyD8P4gOa6+F154ceygwcFfdtHlWTq1/9vUfHy4/qhgHAAA=")).decode())
assert ROW[0] == "ARC-PORT-157" and ROW[4] == "69.0451678", ROW[:6]
roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or ".bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        has_trailing = raw.endswith("\n")
        rows = list(csv.reader(io.StringIO(raw)))
        hit = False
        for i, row in enumerate(rows):
            if row and row[0] == "ARC-PORT-157" and (row[4], row[5]) == ("68.9800", "33.0000") and len(row) == len(ROW):
                rows[i] = list(ROW); hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-loop-1019-1721-p157")
            buf = io.StringIO(); csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out); n += 1
            print("restored", rp)
print("files", n)
