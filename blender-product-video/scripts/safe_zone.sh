#!/bin/bash
# usage: safe_zone.sh <WxH> [reels|stories|tiktok|all] [in out]   safe zone of a 9:16 frame
# Prints the margins in px and the CSS insets for HyperFrames. With in/out (image or video) it draws the guides:
# green = safe line (important texts always inside), red = limit for secondary elements and graphics (tolerance 20% top/bottom, 10% sides).
# Margins measured on 1080x1920 (platform UI, 2026), scaled to WxH. "all" = the strictest of the three, the default.
WH=$1; P=${2:-all}; W=${WH%x*}; H=${WH#*x}; FF=$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)
case $P in            # top bottom left right
  reels)   M="220 430 60 130" ;;  # header; caption+audio; action buttons on the right
  stories) M="250 250 60 60"  ;;  # progress bar+profile; reply bar
  tiktok)  M="130 484 60 140" ;;  # Following/For You; caption stack; action rail on the right
  all)     M="250 484 60 140" ;;
  *) echo "platform: reels|stories|tiktok|all"; exit 1 ;;
esac
read T B L R <<< "$(echo $M | awk -v w=$W -v h=$H '{printf "%d %d %d %d", $1*h/1920+.5, $2*h/1920+.5, $3*w/1080+.5, $4*w/1080+.5}')"
read t b l r <<< "$(echo $T $B $L $R | awk '{printf "%d %d %d %d", $1*.8+.5, $2*.8+.5, $3*.9+.5, $4*.9+.5}')"
echo "$P $W x $H  safe: top $T bottom $B left $L right $R  -> area $((W-L-R))x$((H-T-B)) from x=$L y=$T"
echo "limit (tolerance 20% top/bottom, 10% sides): top $t bottom $b left $l right $r"
echo "CSS: .safe { position:absolute; inset: ${T}px ${R}px ${B}px ${L}px; }"
[ -z "$4" ] && exit 0
"$FF" -y -loglevel error -i "$3" -vf "drawbox=x=$l:y=$t:w=$((W-l-r)):h=$((H-t-b)):color=red@0.9:t=3,drawbox=x=$L:y=$T:w=$((W-L-R)):h=$((H-T-B)):color=lime@0.9:t=3" "$4" && echo "SAFE_OK -> $4"
