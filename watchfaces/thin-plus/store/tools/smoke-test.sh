#!/usr/bin/env bash
# Run from the thin-plus project root. Tests the existing PBW without rebuilding.
set -euo pipefail
export SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy SDL_RENDER_DRIVER=software PYTHONUNBUFFERED=1
out=store/evidence/final-smoke
mkdir -p "$out"
for platform in aplite basalt chalk diorite emery flint gabbro; do
  pebble kill > "$out/${platform}-kill.log" 2>&1
  pebble install --emulator "$platform" build/thin-plus.pbw > "$out/${platform}-install.log" 2>&1
  date -u +%FT%TZ > "$out/${platform}-observation.txt"
  set +e
  timeout --foreground --kill-after=5s --signal=INT 26s pebble logs --emulator "$platform" --no-color > "$out/${platform}-runtime.log" 2>&1
  result=$?
  set -e
  date -u +%FT%TZ >> "$out/${platform}-observation.txt"
  echo "logs exit status: $result (124 is the expected observation timeout)" >> "$out/${platform}-observation.txt"
  if [[ "$result" != 124 && "$result" != 0 ]]; then exit "$result"; fi
  pebble screenshot --emulator "$platform" --no-open "$out/${platform}-default.png" > "$out/${platform}-capture.log" 2>&1
  echo "$platform: final PBW installed, logs observed for 26 seconds, screenshot captured"
done
pebble kill > "$out/cleanup.log" 2>&1
