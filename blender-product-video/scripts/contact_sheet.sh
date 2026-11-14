#!/bin/bash
# usage: contact_sheet.sh <video> <out.jpg> [every_s=1] [cols=6]   one frame every N seconds, tiled into a grid
V=$1; O=$2; E=${3:-1}; C=${4:-6}; FF=$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V"); N=$(echo "$D/$E" | bc); [ "$N" -lt 1 ] && N=1
[ "$N" -lt "$C" ] && C=$N; R=$(( (N + C - 1) / C ))
"$FF" -y -loglevel error -i "$V" -vf "fps=1/$E,scale=480:-2,tile=${C}x${R}:padding=6:margin=6" -frames:v 1 "$O" && echo "SHEET_OK $N frames -> $O"
