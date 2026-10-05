#!/usr/bin/env bash
# gis-aliassync-1313 (2026-10-05): copy the freshly built atlas into EVERY served alias dir.
# Mirror of the Zo control-plane script ArcticTradeLanes.com/atlas-proj/sync_atlas_aliases.sh.
# Layout assumed: <root>/atlas-proj/out (build output) and <root>/arctic-trade-lanes/{,atlas,data,public,public/atlas,public/data,dist,dist/atlas,dist/data}.
# Usage: bash sync_atlas_aliases.sh [src_dir]   (default: atlas-proj/out next to this script)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${1:-$HERE/out}"
SITE="$HERE/../arctic-trade-lanes"
FILES=(atlas.3996.geojson atlas.4326.geojson atlas.wgs84.geojson atlas.geojson atlas.manifest.json)
DIRS=("$HERE" "$SITE" "$SITE/atlas" "$SITE/data" "$SITE/public" "$SITE/public/atlas" "$SITE/public/data" "$SITE/dist" "$SITE/dist/atlas" "$SITE/dist/data")
for f in "${FILES[@]}"; do [ -s "$SRC/$f" ] || { echo "missing $SRC/$f" >&2; exit 1; }; done
gen=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['generated'])" "$SRC/atlas.manifest.json")
for d in "${DIRS[@]}"; do
  [ "$(cd "$d" 2>/dev/null && pwd)" = "$(cd "$SRC" && pwd)" ] && continue
  mkdir -p "$d"
  for f in "${FILES[@]}"; do cp -f "$SRC/$f" "$d/$f.tmp" && mv -f "$d/$f.tmp" "$d/$f"; done
done
ref=$(md5sum "$SRC/atlas.wgs84.geojson" | cut -d' ' -f1)
bad=0
for d in "${DIRS[@]}"; do
  for f in atlas.wgs84.geojson atlas.4326.geojson atlas.geojson; do
    h=$(md5sum "$d/$f" | cut -d' ' -f1); [ "$h" = "$ref" ] || { echo "MISMATCH $d/$f"; bad=1; }
  done
  g=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['generated'])" "$d/atlas.manifest.json")
  [ "$g" = "$gen" ] || { echo "STALE $d/atlas.manifest.json $g"; bad=1; }
done
echo "synced generation $gen into ${#DIRS[@]} dirs (bad=$bad)"
exit $bad
