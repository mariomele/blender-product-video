#!/bin/bash
# usage: deliver.sh <video.mp4> <out_dir> [max_mb=28]
# Writes the delivery files:
#   master.mp4  H.264 high quality, audio normalised to -14 LUFS / -1 dBTP (social and web standard), faststart
#   light.mp4   same video under max_mb (for phone, WhatsApp, email), bitrate computed from the duration
V=$1; O=$2; MAX=${3:-28}; FF=$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)
mkdir -p "$O"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
HASA=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$V")
if [ -n "$HASA" ]; then A=(-af loudnorm=I=-14:TP=-1:LRA=11 -c:a aac -b:a 192k -ar 48000); AL=(-af loudnorm=I=-14:TP=-1:LRA=11 -c:a aac -b:a 128k -ar 48000); AK=128
else A=(-an); AL=(-an); AK=0; fi
"$FF" -y -loglevel error -i "$V" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart "${A[@]}" "$O/master.mp4" || exit 1
VK=$(echo "$MAX * 8 * 1024 * 0.95 / $D - $AK" | bc)   # kbit/s left for video, 5% container margin
[ "$VK" -lt 300 ] && { echo "TOO_LONG: ${D}s non sta in ${MAX} MB con qualità accettabile"; exit 1; }
"$FF" -y -loglevel error -i "$V" -c:v libx264 -preset slow -b:v ${VK}k -maxrate ${VK}k -bufsize $((VK*2))k -pix_fmt yuv420p -movflags +faststart "${AL[@]}" "$O/light.mp4" || exit 1
for f in master light; do echo "$f.mp4 $(du -m "$O/$f.mp4" | cut -f1) MB"; done
[ -n "$HASA" ] && "$FF" -hide_banner -i "$O/master.mp4" -af ebur128 -f null - 2>&1 | grep -A1 'Integrated loudness' | tail -1
echo "DELIVER_OK -> $O"
