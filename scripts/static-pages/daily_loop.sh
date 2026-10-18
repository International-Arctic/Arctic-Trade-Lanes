#!/usr/bin/env bash
# Long-running scheduler (Zo user service, mode=process): rebuild ./pages once per MSK day at/after 00:07.
# Checks every 5 min; catches up on start if today's build is missing. Failures are logged and retried next tick.
APP=/home/workspace/ArcticTradeLanes.com/arctic-trade-lanes
WORK=/home/workspace/ArcticTradeLanes.com/_pages-build
mkdir -p "$WORK"
while true; do
  today=$(TZ=Europe/Moscow date +%F); hm=$(TZ=Europe/Moscow date +%H%M)
  last=$(cat "$WORK/last-built" 2>/dev/null || true)
  if [ "$last" != "$today" ] && [ "$hm" -ge 0007 ]; then
    bash "$APP/scripts/static-pages/rebuild_pages.sh" "$today" >>"$WORK/rebuild.log" 2>&1 || echo "$(date -u +%FT%TZ) rebuild FAILED" >>"$WORK/rebuild.log"
  fi
  sleep 300
done
