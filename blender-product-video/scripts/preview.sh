#!/bin/bash
# usage: preview.sh <file.blend> <first> <last> <step> <out_dir> [res%=25] [spp=8]
#   storyboard: step = scene fps (1 frame per second) -> <out_dir>/grid.jpg
#   low-fps preview: step = 2 on a 24 fps scene -> 12 fps <out_dir>/preview.mp4 (real-time speed)
# Always writes both grid.jpg and preview.mp4. Resumable.
F=$1; A=$2; Z=$3; STEP=$4; OUT=$5; RES=${6:-25}; SPP=${7:-8}; HERE=$(cd "$(dirname "$0")" && pwd)
B=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}; FF=$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)
mkdir -p "$OUT"
"$B" -b "$F" --python "$HERE/gpu_setup.py" --python "$HERE/preview.py" -- $A $Z $STEP "$OUT" $RES $SPP > "$OUT/render.log" 2>&1
FPS=$(grep -m1 '^FPS' "$OUT/render.log" | cut -d' ' -f2)
N=$(ls "$OUT"/f*.jpg 2>/dev/null | wc -l | tr -d ' ')
[ "$N" -eq "$(grep -m1 '^COUNT' "$OUT/render.log" | cut -d' ' -f2)" ] || { echo "MISSING $N frames, see $OUT/render.log"; exit 1; }
COLS=$(( N < 6 ? N : 6 )); ROWS=$(( (N + COLS - 1) / COLS ))
"$FF" -y -loglevel error -pattern_type glob -i "$OUT/f*.jpg" -vf "scale=480:-2,tile=${COLS}x${ROWS}:padding=6:margin=6" -frames:v 1 "$OUT/grid.jpg"
"$FF" -y -loglevel error -framerate "$FPS/$STEP" -pattern_type glob -i "$OUT/f*.jpg" -c:v libx264 -crf 23 -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "$OUT/preview.mp4"
echo "PREVIEW_OK $N frames, $(echo "scale=1; $FPS/$STEP" | bc) fps -> $OUT/grid.jpg $OUT/preview.mp4"
