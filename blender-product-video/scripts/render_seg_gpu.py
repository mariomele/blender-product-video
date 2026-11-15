# Renders shot [a,b] stretched to (b-a+1+extra) frames via subframe sampling (motion is procedural, no sims), JPG, resumable.
# usage: blender -b file.blend --python render_seg_gpu.py -- a b extra outdir [res%=100] [WxH] [--redo x y]
# Without WxH the resolution saved in the .blend is kept. Env: SPP_FINAL (default 40), JPG_Q (default 95).
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
s.cycles.samples = int(os.environ.get('SPP_FINAL', 40)) if res == 100 else 12   # SPP_FINAL: final renders faster
r.image_settings.file_format = 'JPEG'; r.image_settings.quality = int(os.environ.get('JPG_Q', 95))   # JPG_Q 1-100: smaller files or max quality
os.makedirs(out, exist_ok=True)
L = b - a + 1; N = L + extra
for n in range(N):
    path = os.path.join(out, f"f{n+1:04d}.jpg")
    t = a + n * (L - 1) / max(N - 1, 1)  # first and last frame of the shot are kept exactly
    if redo and not redo[0] - 1 < t < redo[1] + 1: continue  # +-1: subframes next to the range blend into it
    if os.path.exists(path) and not redo: continue
    f = math.floor(t); s.frame_set(f, subframe=t - f)
    r.filepath = path
    bpy.ops.render.render(write_still=True)
