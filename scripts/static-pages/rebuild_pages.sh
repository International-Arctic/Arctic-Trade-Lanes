#!/usr/bin/env bash
# Rebuild /funding + /advertise static pages (44 files) into ./pages, atomically per file.
# Build happens in a temp dir on the same filesystem; each file is then mv'd (rename(2)) over the live
# one, so a request never sees a missing or half-written page. server.ts re-reads ./pages after the
# render-cache TTL (120 s), so no restart is needed.
set -euo pipefail
APP=/home/workspace/ArcticTradeLanes.com/arctic-trade-lanes
WORK=/home/workspace/ArcticTradeLanes.com/_pages-build
mkdir -p "$WORK"
cd "$APP"
D="${1:-$(TZ=Europe/Moscow date +%F)}"
TMP=$(mktemp -d "$WORK/build.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
python3 scripts/static-pages/build_pages.py data/arctic-funding-programs-2026.csv "$TMP" "$D"
N=$(find "$TMP" -name '*.html' | wc -l)
[ "$N" -eq 44 ] || { echo "abort: expected 44 html files, got $N" >&2; exit 1; }
find "$TMP" -name '*.html' -size -5k | grep -q . && { echo 'abort: undersized page' >&2; exit 1; }
rm -rf "$WORK/prev"; cp -a pages "$WORK/prev"
(cd "$TMP" && find . -name '*.html' -printf '%P\n') | while read -r f; do
  mkdir -p "pages/$(dirname "$f")"; chmod 644 "$TMP/$f"; mv -f "$TMP/$f" "pages/$f"
done
echo "$D" > "$WORK/last-built"
echo "$(date -u +%FT%TZ) build-date=$D files=$N funding=$(stat -c%s pages/funding.html)B" | tee -a "$WORK/rebuild.log"
