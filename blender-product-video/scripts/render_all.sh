#!/bin/bash
# usage: [SPP=n] [JPG_Q=1-100] render_all.sh <project_dir> <edl.txt> [res%=100] [fps=24] [WxH]
#   Any combination: res% (100 -> final_jpg, else preview_jpg), output fps (a shot whose .blend has another fps is
#   resampled via subframes, same duration), SPP (default 40 at 100%, else 12), JPG_Q (default 95).
#   WxH overrides the resolution saved in each .blend (e.g. 1920x1080, 1080x1920, 1080x1080).
# EDL line: <n> <file.blend> <first> <last> [extra=0] [skip_head=0]
#   extra: frames added by subframe stretch (voice-over room); skip_head: rendered frames left out of the edit.
# Resumable: existing JPGs are skipped. Output: <project>/final_jpg (or preview_jpg) + final.mp4 + timings.json
# Exit 2 = HANG: no new frame for HANG_MIN minutes (default 10), usually a GUI Blender open while rendering on Metal.
P=$1; EDL=$2; RES=${3:-100}; FPS=${4:-24}; WH=$5; HANG=$(( ${HANG_MIN:-10} * 60 )); HERE=$(cd "$(dirname "$0")" && pwd)
B=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}; FF=$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)
GUI=$(ps -axo pid=,command= | grep -e "$B" -e 'MacOS/Blender' | grep -v -e ' -b' -e grep)
[ -n "$GUI" ] && { echo "GUI_BLENDER_OPEN: chiudilo prima (Metal headless si blocca):"; echo "$GUI"; exit 3; }
SPP=${SPP:-${SPP_FINAL:-$([ "$RES" = 100 ] && echo 40 || echo 12)}}; export SPP JPG_Q=${JPG_Q:-95} OUT_FPS=$FPS
cd "$P" || exit 1
OUT=final_jpg; [ "$RES" != 100 ] && OUT=preview_jpg; mkdir -p "$OUT"; L=$OUT/list.txt; : > $L
T=$OUT/timings.json; echo "[" > $T; start=0; sep=""
count() { ls "$1"/f*.jpg 2>/dev/null | wc -l | tr -d ' '; }
while read n f a b x s; do
  [ -z "$n" ] && continue; ext=${x:-0}; dir="$OUT/${n}_${f%.blend}_${a}"
  # frames made with another b/extra/res map to different times: set them aside (never delete), start the shot again
  par="$f $a $b $ext $RES $WH|$FPS $SPP $JPG_Q"
  # (no params file, or one without fps/quality, comes from an older run: adopt it as is)
  old=$(cat "$dir/params" 2>/dev/null)
  if [ -n "$old" ] && [ "$old" != "$par" ] && [ "$old" != "${par%|*}" ] && [ "$(count "$dir")" -gt 0 ]; then
    mv "$dir" "$dir.old_$(date +%Y%m%d_%H%M%S)"; echo "PARAMS_CHANGED $dir: vecchi frame spostati in $dir.old_*"
  fi
  mkdir -p "$dir"; echo "$par" > "$dir/params"
  for i in 1 2 3; do
    [ -f "$dir/n" ] && [ "$(count "$dir")" -eq "$(cat "$dir/n")" ] && break
    "$B" -b "$f" --python "$HERE/gpu_setup.py" --python "$HERE/render_seg_gpu.py" -- $a $b $ext "$dir" $RES $WH > "$dir.log" 2>&1 &
    pid=$!; last=$(count "$dir"); idle=0
    while kill -0 $pid 2>/dev/null; do
      sleep 15; now=$(count "$dir")
      if [ "$now" != "$last" ]; then last=$now; idle=0; else idle=$((idle+15)); fi
      [ $idle -ge $HANG ] && { kill $pid; echo "HANG $dir: nessun frame nuovo da ${HANG_MIN:-10} min (vedi $dir.log)"; exit 2; }
    done
  done
  want=$(cat "$dir/n" 2>/dev/null || echo $((b-a+1+ext))); have=$(count "$dir")
  s=$(( ${s:-0} * want / (b-a+1+ext) ))  # skip_head is in .blend frames
  [ "$have" -eq "$want" ] || { echo "MISSING $dir $have/$want"; exit 1; }
  ls "$dir"/f*.jpg | tail -n +$(( ${s:-0} + 1 )) | sed "s|^|file '$PWD/|;s|$|'|" >> $L
  k=$((want - ${s:-0}))
  echo "$sep {\"scene\": $n, \"file\": \"$f\", \"start\": $(echo "scale=3; $start/$FPS" | bc), \"end\": $(echo "scale=3; ($start+$k)/$FPS" | bc), \"frames\": $k}" >> $T
  start=$((start+k)); sep=","
  echo "$dir DONE $(date +%H:%M)"
done < "$EDL"
echo "]" >> $T
"$FF" -y -loglevel error -r $FPS -f concat -safe 0 -i $L -c:v libx264 -crf 14 -pix_fmt yuv420p -r $FPS "$OUT/final.mp4" && echo "FINAL_OK $(wc -l < $L) frames -> $OUT/final.mp4 $T"
