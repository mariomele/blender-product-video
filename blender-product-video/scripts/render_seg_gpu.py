# Renders shot [a,b] stretched to (b-a+1+extra) frames via subframe sampling (motion is procedural, no sims), JPG, resumable.
# usage: blender -b file.blend --python render_seg_gpu.py -- a b extra outdir [res%=100] [WxH] [--redo x y]
# Without WxH the resolution saved in the .blend is kept.
# Env: SPP (samples, default 40 at 100% else 12; SPP_FINAL still works), JPG_Q (1-100, default 75),
#      OUT_FPS (output fps; if it differs from the .blend fps the shot is resampled via subframes, same duration).
# Writes <outdir>/n with the number of output frames.
# --redo x y: re-render (overwrite) only the output frames sampling master frames x..y; same a, b, extra as before.
import bpy, sys, os, math
args = sys.argv[sys.argv.index('--')+1:]
redo = None
if '--redo' in args:
    i = args.index('--redo'); redo = (float(args[i+1]), float(args[i+2])); del args[i:i+3]
a, b, extra = map(int, args[:3]); out = args[3]
res = float(args[4]) if len(args) > 4 else 100
s = bpy.context.scene
r = s.render
if len(args) > 5: r.resolution_x, r.resolution_y = map(int, args[5].split('x'))
r.resolution_percentage = int(res)
s.cycles.device = "GPU"; s.cycles.use_denoising = True
s.cycles.samples = int(os.environ.get('SPP') or os.environ.get('SPP_FINAL') or (40 if res == 100 else 12))
r.image_settings.file_format = 'JPEG'; r.image_settings.quality = int(os.environ.get('JPG_Q', 75))
os.makedirs(out, exist_ok=True)
L = b - a + 1; fps = r.fps / r.fps_base
N = round((L + extra) * float(os.environ.get('OUT_FPS') or fps) / fps)  # same seconds at the output fps
nf = os.path.join(out, 'n')
if redo and os.path.exists(nf): N = int(open(nf).read())  # --redo keeps the frame count of the first render
open(nf, 'w').write(str(N))
for n in range(N):
    path = os.path.join(out, f"f{n+1:04d}.jpg")
    t = a + n * (L - 1) / max(N - 1, 1)  # first and last frame of the shot are kept exactly
    if redo and not redo[0] - 1 < t < redo[1] + 1: continue  # +-1: subframes next to the range blend into it
    if os.path.exists(path) and not redo: continue
    f = math.floor(t); s.frame_set(f, subframe=t - f)
    r.filepath = path
    bpy.ops.render.render(write_still=True)
